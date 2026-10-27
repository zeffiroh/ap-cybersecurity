---
deck:
  title: IDS, IPS & Monitoring
  kicker: Class 14
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 14
  description: Catching what the firewall let through, detection, prevention, logs, and SIEM basics.
  topics: [Intrusion Detection, Intrusion Prevention, Alerts, Logs, Monitoring, SIEM]
---

---
title: IDS, IPS & Monitoring
cover: true
---
:::text class=sub
What happens to the traffic the firewall decided to allow
:::
:::list style=chips
- IDS
- IPS
- SIEM
:::

:::image src="images/14_ids_ips_overview.png" alt="Overview diagram showing the relationship between IDS, IPS, and SIEM: a firewall on the left permits traffic, an IDS passively observes it, an IPS inline blocks threats, and a SIEM at the top aggregates alerts from both for correlation and analyst review" caption="IDS, IPS, and SIEM form the detection and response layer behind the firewall, catching what the perimeter lets through" width=full
:::

:::notes
This class builds directly on the firewall concepts from Class 13 by answering the question that firewalls cannot: once traffic is permitted onto the network, how do we know whether it is actually safe? Intrusion Detection Systems (IDS) and Intrusion Prevention Systems (IPS) exist precisely to provide that visibility and enforcement capability beyond the perimeter.

An IDS is a passive monitoring technology, it observes copies of network traffic or system events and generates alerts when suspicious patterns are detected, but it does not interfere with the traffic itself. This distinguishes it fundamentally from an IPS, which sits inline in the data path and can actively block, drop, or modify traffic in real time. The passive/active distinction is operationally significant: an IDS misconfiguration results in missed alerts, while an IPS misconfiguration can block legitimate traffic and disrupt business operations.

Security Information and Event Management (SIEM) platforms represent the third leg of this triad. Rather than inspecting traffic directly, a SIEM aggregates log data and security events from across the entire infrastructure, firewalls, IDS/IPS, endpoints, servers, and applications, and applies correlation rules to identify attack patterns that span multiple systems and time windows. An individual alert from an IDS may appear benign in isolation; the SIEM reveals that the same source IP triggered authentication failures on ten different systems in the prior hour, elevating it to a credible threat indicator.

Together, IDS, IPS, and SIEM implement the **Detect** function of the NIST Cybersecurity Framework (CSF), which mandates continuous monitoring and anomaly identification as a complement to prevention-focused controls. NIST SP 800-94 (Guide to Intrusion Detection and Prevention Systems) provides detailed guidance on the architecture, deployment, and management of these systems. Understanding how these three technologies interact, and where each has blind spots, is essential for any security operations role, from SOC analyst to security architect, and forms the conceptual foundation for tools explored in the Splunk Fundamentals course.
:::

%%%

---
unit: Foundations
code: MON
title: Beyond the Firewall
---

:::callout style=soft
Firewalls operate on predefined rules and observable packet headers, but they cannot assess the intent or behavior of the traffic they permit. This limitation necessitates additional layers of security that focus on detection, analysis, and response.
:::

:::image src="images/14_beyond_firewall.png" alt="Diagram showing permitted traffic flowing past a firewall into a detection layer where IDS, IPS, and behavioral analysis tools inspect the traffic, with alerts flowing up to a SIEM for correlation and analyst review" caption="After the firewall permits traffic, detection systems take over, inspecting behavior, correlating events, and surfacing threats the perimeter missed" width=full
:::

:::pullquote
If prevention fails silently, detection is what makes it loud.
:::

:::flow
1. Traffic passes through firewall (rule-based allow decision)
2. IDS captures a copy of traffic via network TAP or SPAN port
3. Payload and behavior analyzed against signatures and baselines
4. IPS (if inline) intercepts and blocks high-confidence threats
5. Alerts and events forwarded to SIEM for multi-source correlation
6. SIEM triggers analyst review and incident escalation if warranted
:::

::::columns
::col::
:::list heading="Key Limitations of Firewalls" style=plain
- Stateless inspection lacks context
- Cannot detect application-layer attacks
- Blind to insider threats
- No behavioral analysis
- Evasion via encryption or tunneling
:::

::col::
:::list heading="Detection Layer Responsibilities" style=plain
- Behavioral anomaly detection
- Protocol compliance checking
- Payload analysis
- Correlation across data sources
- Real-time alerting and logging
:::
::::

:::notes
The fundamental limitation of firewalls lies in their static, rule-based approach to traffic filtering. As defined in NIST SP 800-41 Rev. 1, firewalls inspect packets based on IP addresses, ports, and protocols, but they lack the ability to evaluate the semantic content or behavioral intent of the traffic. This creates a critical gap: an attacker can embed malicious payloads within seemingly legitimate protocols (e.g., HTTP, DNS) that pass firewall rules but carry threats such as command-and-control communications or data exfiltration.

To address this, Intrusion Detection Systems (IDS) and Intrusion Prevention Systems (IPS) extend network visibility by performing deep packet inspection (DPI), analyzing application-layer data, and identifying patterns associated with known attacks or anomalous behavior. These systems implement mechanisms aligned with the NIST Cybersecurity Framework (CSF), particularly the "Detect" function, which emphasizes continuous monitoring and anomaly identification.

For example, CVE-2021-44228 (Log4Shell) demonstrated how a firewall might allow a vulnerable application to receive a malicious string via an HTTP header, which then triggers remote code execution. Only through behavioral monitoring or signature-based detection could such an event be flagged post-breach. This illustrates why layered defense models like the ISO/IEC 27001 risk management framework emphasize complementary controls beyond perimeter defenses.

Detection systems also support compliance with standards such as PCI DSS, which mandates real-time monitoring and alerting for security events. By implementing both signature-based and anomaly-based detection methods, organizations can detect known threats (e.g., exploit kits) and unknown or zero-day behaviors (e.g., lateral movement).

The "assume breach" philosophy, formalized in NIST SP 800-207 (Zero Trust Architecture), represents the clearest articulation of why detection layers are indispensable. Rather than optimizing solely for preventing initial access, assume-breach postures invest heavily in detection speed and response capability, accepting that determined adversaries will eventually find a way in. The 2021 Microsoft Exchange Server vulnerabilities (CVE-2021-26855, ProxyLogon) illustrated this starkly: attackers who exploited the flaw before patches were available communicated exclusively over HTTPS to port 443, a universally permitted port that no perimeter firewall would block. Detecting such intrusions required behavioral monitoring, looking for anomalous IIS worker process spawning child shells, unusual outbound connections from Exchange, and new webshell files in the OWA directory, capabilities that only exist in the detection layer behind the firewall. Understanding this gap is what motivates the IDS, IPS, and SIEM technologies covered in this class.
:::

%%%

---
unit: Detection
code: IDS
title: Intrusion Detection Systems (IDS)
---
:::callout style=soft
An **Intrusion Detection System (IDS)** is a security technology designed to monitor network traffic, host activities, or system logs for signs of malicious behavior or policy violations. When suspicious activity is detected, the IDS generates alerts for further investigation, but does **not** take action to prevent or block the activity.
:::

:::image src="images/14_ids_architecture.png" alt="Diagram of an IDS deployment showing a network TAP or SPAN port feeding a copy of traffic to an IDS sensor, which analyzes the traffic and sends alerts to a SIEM console; the live traffic continues flowing uninterrupted to its destination, illustrating the passive out-of-band nature of IDS" caption="An IDS receives a mirrored copy of traffic, it analyzes without interfering, making it a passive observer that alerts but cannot block" width=full
:::

:::flow
1. Network traffic or system events captured via SPAN port, TAP, or local agent
2. Traffic parsed and decoded at relevant protocol layers
3. Compared against signature database (known attack patterns) and behavioral baseline
4. Match or deviation triggers alert generation with metadata (timestamp, src/dst, signature ID)
5. Alert logged and forwarded to SIEM or analyst console for triage and investigation
:::

:::list heading="Core Functions of an IDS" style=plain
- Continuously monitors network traffic or system events
- Analyzes data using signature-based, anomaly-based, or behavior-based detection methods
- Compares observed activity against known attack patterns or baseline behavior
- Generates alerts or logs when potential intrusions are detected
- Provides forensic data for post-incident analysis
:::

::::columns
::col::
:::table
| Feature            | Description |
|--------------------|-------------|
| **Monitoring Scope** | Network (NIDS), Host (HIDS), or hybrid |
| **Detection Method** | Signature-based, Anomaly-based, Heuristic |
| **Response Action**  | Alerting only (no blocking) |
| **Deployment Mode**  | Passive (out-of-band or mirrored traffic) |
:::
::col::
:::table
| Acronym | Full Name                     | Role |
|---------|-------------------------------|------|
| NIDS    | Network-based IDS             | Monitors network traffic |
| HIDS    | Host-based IDS                | Monitors system logs and file integrity |
| SIEM    | Security Information and Event Management | Aggregates and correlates IDS alerts |
| CVE     | Common Vulnerabilities and Exposures | Used to identify known attack signatures |
:::
::::

:::notes
An Intrusion Detection System (IDS) serves as a foundational element of network and system security monitoring. Its primary role is to detect potentially malicious activities by analyzing traffic, logs, or system behavior in real time. Unlike an Intrusion Prevention System (IPS), an IDS is a passive technology, it observes and alerts but does not intervene to stop threats.

IDS technologies are typically categorized into two main types: **Network-based IDS (NIDS)** and **Host-based IDS (HIDS)**. NIDS monitors network traffic for malicious patterns by inspecting packets in real time, often deployed at strategic points such as network gateways or switch mirror ports. HIDS, on the other hand, resides on individual hosts and monitors system logs, file integrity, and process behavior to detect anomalies or signs of compromise.

Detection mechanisms in IDS can be broadly grouped into three categories:
- **Signature-based detection** compares observed activity against a database of known attack signatures (e.g., specific exploit patterns from CVE entries). This method is effective for identifying well-known threats but struggles with zero-day attacks.
- **Anomaly-based detection** establishes a baseline of normal behavior and flags deviations. While more adaptive, it can produce false positives if baselines are poorly defined.
- **Heuristic or behavior-based detection** uses machine learning or rule-based logic to identify suspicious activity that does not match known signatures.

According to **NIST Special Publication 800-94**, "Guide to Intrusion Detection and Prevention Systems," IDS is central to situational awareness and supports incident response by providing early warning of potential intrusions. It is often integrated with **SIEM** platforms to enhance correlation and automate alert triage.

While an IDS enhances visibility, it does not inherently improve system security unless its alerts are actively reviewed and acted upon. As such, IDS is most effective when part of a layered defense strategy that includes active response mechanisms such as IPS or endpoint protection platforms.

The leading open-source IDS/IPS platforms in production SOC environments include **Snort** (maintained by Cisco Talos, with a commercial ruleset), **Suricata** (developed by the Open Information Security Foundation, supporting multi-threading for high-throughput environments), and **Zeek** (formerly known as Bro, focused on high-fidelity network metadata generation for behavioral analysis rather than signature alerting). These tools are widely deployed as network sensors feeding into SIEM platforms such as Splunk. A cautionary real-world example: during the 2014 JPMorgan Chase breach, which exposed data on 83 million customers, post-incident analysis revealed that security monitoring tools had generated alerts that were not escalated promptly, partly due to the volume of noise from untuned detection rules. This case reinforced the critical operational principle that an IDS delivers value only when its alert pipeline is actively monitored, triaged, and acted upon, a point emphasized in NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide) guidance on continuous monitoring and alert management workflows.
:::

%%%

---
unit: Prevention
code: IPS
title: Intrusion Prevention Systems (IPS)
---
:::callout style=soft
An **Intrusion Prevention System (IPS)** is an active security technology positioned **inline** with network traffic, capable of **real-time detection and automatic mitigation** of malicious activity by dropping packets, resetting connections, or blocking traffic flows.
:::

:::image src="images/14_ips_inline.png" alt="Diagram showing an IPS deployed inline in the network data path between two network segments, with all traffic passing through the IPS inspection engine; the IPS drops a malicious packet (red X) while forwarding legitimate packets (green checkmark), illustrating its active enforcement role" caption="An IPS sits inline in the data path, all traffic must pass through it, giving it the authority to drop, block, or modify packets in real time" width=full
:::

:::pullquote
An IPS is an inline, proactive enforcement layer, not just a passive observer.
:::

::::columns
::col::
:::list heading="Key Functions of an IPS"
- Real-time traffic analysis
- Protocol compliance checking
- Signature-based threat detection
- Anomaly-based behavioral analysis
- Automated response and blocking
- Logging and alerting capabilities
:::
::col::
:::list heading="IPS Deployment Modes"
- **Inline (In-band):** Directly in the data path; can block traffic
- **Passive (Out-of-band):** Monitors mirrored traffic; functions like IDS
- **Hybrid/Tap Mode:** Partial inline; monitors and alerts, with optional blocking
:::
::::

:::notes
An Intrusion Prevention System (IPS) represents a critical evolution from the Intrusion Detection System (IDS), introducing not only visibility but also **automated enforcement capabilities**. Unlike an IDS, which operates out-of-band and merely observes a copy of traffic (often via port mirroring or network taps), an IPS is placed **directly in the network data path**, enabling it to **intercept, inspect, and intervene** in real time.

This inline positioning grants the IPS the authority to **drop malicious packets**, **reset Transmission Control Protocol (TCP) sessions**, or **block entire connections** based on predefined policies or threat signatures. This capability aligns with **NIST Special Publication 800-94**, which outlines best practices for network intrusion detection and response, emphasizing the role of real-time defensive systems in reducing attack surface and dwell time.

However, this power introduces **operational risk**: a **false positive** in an IPS can result in **legitimate traffic being blocked**, potentially disrupting business operations or violating service-level agreements (SLAs). This is in contrast to an IDS, where false positives result only in alerts, not service interruption. Therefore, **tuning and policy validation** are essential to maintaining both security and availability.

Modern IPS solutions often integrate with threat intelligence feeds, support **deep packet inspection (DPI)**, and implement **stateful protocol analysis** to detect deviations from expected behavior. They are commonly deployed in enterprise perimeters, data centers, and cloud environments to enforce network-layer security policies. Examples of IPS technologies include **Snort Inline**, **Cisco FirePOWER**, and **Palo Alto Networks' threat prevention engine**.

From a compliance perspective, frameworks such as **ISO/IEC 27001** and **NIST Cybersecurity Framework (CSF)** recognize automated threat response mechanisms like IPS as part of a layered defense strategy. In incident response scenarios, an IPS can provide immediate mitigation, reducing the window of exposure before human analysts intervene, a concept central to **MITRE ATT&CK's** "Network Denial of Service" and "Impair Defenses" mitigation strategies.

In real-world deployments, IPS systems must be carefully architected to avoid becoming a **single point of failure**. Techniques such as **high availability (HA) clustering**, **bypass switches**, and **graceful degradation to fail-open or fail-close modes** are used to ensure network continuity even during system failure or maintenance.

The evolution toward cloud-native IPS capabilities is also reshaping deployment models. AWS GuardDuty performs threat detection by analyzing VPC Flow Logs, DNS query logs, and CloudTrail events using machine learning and threat intelligence, functioning conceptually as a cloud-scale IDS. Azure Defender for Network provides inline threat prevention for Azure Virtual Network environments. These cloud-native tools eliminate the hardware bypass and high-availability complexity of physical inline appliances, but introduce their own operational considerations around coverage scope, latency, and the shared responsibility model. NIST SP 800-144 (Guidelines on Security and Privacy in Public Cloud Computing) addresses how organizations should think about these controls within cloud environments.
:::

%%%

---
unit: Comparison
code: CMP
title: IDS vs IPS
---

:::image src="images/14_ids_vs_ips.png" alt="Side-by-side diagram comparing IDS (passive, out-of-band, receives mirrored traffic copy, generates alerts only) and IPS (active, inline, all traffic passes through it, can block and drop packets); both feed alerts to a SIEM console at the top" caption="IDS observes and reports; IPS observes and enforces, the deployment mode (out-of-band vs inline) determines which role a system plays" width=full
:::

::::columns
::col::
:::table
| Aspect | IDS (Intrusion Detection System) | IPS (Intrusion Prevention System) |
|---|---|---|
| **Deployment Mode** | Passive (out-of-band) | Active (inline) |
| **Primary Function** | Detect and alert | Detect, alert, and prevent |
| **Response Capability** | None; logs and notifies | Automatic blocking or dropping |
| **Network Impact** | Minimal; no disruption | Potential to disrupt traffic |
| **False Positive Risk** | Alert fatigue | Service disruption |
| **Latency Impact** | None | Introduces delay |
:::
::col::
:::callout
**Key Insight:**  
IDS serves as a *sentinel*, observing and reporting anomalies, while IPS functions as a *gatekeeper*, capable of enforcing policy by halting malicious activity in real time.
:::
::::
:::notes
Intrusion Detection Systems (IDS) and Intrusion Prevention Systems (IPS) are foundational components of network security monitoring, yet they differ fundamentally in their operational roles and deployment architectures.

An IDS operates in a **passive monitoring** mode, typically receiving a copy of network traffic via aSPAN (Switched Port Analyzer) or TAP (Test Access Point). It inspects traffic for known attack signatures or behavioral anomalies but cannot influence the flow of data. When a potential threat is identified, the system generates an alert, commonly via syslog, SNMP traps, or integration with a SIEM (Security Information and Event Management) platform. This model aligns with **NIST SP 800-94**, which outlines best practices for network monitoring and intrusion detection.

In contrast, an IPS is deployed **inline**, meaning all traffic must pass through it. This enables the system to not only detect threats but also to **actively block or modify packets** in real time. The ability to drop malicious traffic provides immediate protection but introduces potential risks. A false positive in an IPS can result in **legitimate traffic being blocked**, leading to service outages or user disruption. This necessitates careful tuning and policy management, as referenced in **ISO/IEC 27001** controls related to network security and incident response.

The trade-off between detection and prevention is central to choosing between IDS and IPS. While an IDS provides comprehensive visibility with minimal risk, an IPS offers responsive enforcement at the cost of increased complexity and potential for operational impact. In many environments, a **hybrid approach** is used: an IDS for monitoring and forensics, and an IPS for high-confidence threat blocking in critical zones.

In practice, the choice between IDS and IPS deployment, or the use of both in complementary roles, is guided by the sensitivity of the monitored zone and the organization's risk tolerance. PCI DSS Requirement 11.4 mandates the use of intrusion-detection and/or intrusion-prevention techniques at the perimeter and at critical points inside the cardholder data environment (CDE), explicitly allowing either technology depending on placement and policy configuration. Financial services organizations often deploy IDS on internal network segments (where false positives from IPS would disrupt trading or payment processing) while deploying IPS inline at the perimeter DMZ (where blocking known-malicious traffic outweighs the disruption risk). Network TAPs are generally preferred over SPAN ports for IDS deployments in high-fidelity environments because TAPs provide full-duplex packet capture without the packet loss that SPAN ports can introduce under high load, a distinction documented in NIST SP 800-94 Appendix A on sensor deployment options.
:::

%%%

---
unit: Methods
code: SIG
title: Detection Methods
---

:::image src="images/14_detection_methods.png" alt="Split diagram comparing signature-based detection (left: a packet being matched against a database of known attack patterns, with a CVE reference label) and anomaly-based detection (right: a behavioral baseline shown as a normal distribution curve, with an outlier data point flagged as anomalous), with a center label showing that both methods can be combined in hybrid detection" caption="Signature-based detection is fast and precise for known threats; anomaly-based detection can catch novel attacks, hybrid approaches use both in tandem" width=full
:::

:::flow
1. Network event or packet captured by the detection engine
2. Event compared against known signature database (signature-based check)
3. If signature match found: alert generated with CVE reference and confidence score
4. If no signature match: event evaluated against behavioral baseline (anomaly-based check)
5. Statistical deviation or heuristic rule violation triggers potential anomaly alert
6. Alert enriched with context (asset data, threat intel) and forwarded to SIEM
:::

::::columns
::col::
:::table
| Method | How it works | Trade-off |
|---|---|---|
| Signature-based | Matches known attack patterns | Fast and accurate, but misses new/unknown attacks |
| Anomaly-based | Flags deviations from normal behavior | Can catch new attacks, but more false positives |
:::
::col::
:::callout
Detection methods form the core logic behind intrusion detection and prevention systems. Each method reflects a distinct philosophy of threat identification and comes with inherent strengths and limitations.
:::
::::
:::notes
Intrusion Detection Systems (IDS) and Intrusion Prevention Systems (IPS) rely on two foundational detection paradigms: **signature-based** and **anomaly-based** detection. These methods define how network traffic, system calls, or user behavior are analyzed to identify potential security threats.

**Signature-based detection** operates by comparing observed activities against a database of predefined attack signatures. These signatures are typically derived from known vulnerabilities, such as those cataloged in the Common Vulnerabilities and Exposures (CVE) database, or from documented exploit patterns. This approach is conceptually similar to how traditional antivirus software identifies malware. It is highly effective at detecting well-known threats with low false positive rates, and it performs efficiently in high-throughput environments. However, it is inherently reactive, it cannot detect zero-day attacks or polymorphic malware that alters its signature to evade detection. Standards such as NIST SP 800-94 emphasize the importance of maintaining updated signature databases to ensure continued effectiveness.

In contrast, **anomaly-based detection** takes a proactive stance by establishing a baseline of normal system or network behavior, often through statistical modeling, machine learning, or heuristic analysis. Any deviation from this baseline is flagged as a potential anomaly. This method is capable of identifying previously unknown attacks, including novel variants of malware or insider threats. However, it tends to produce a higher number of false positives, as not all anomalies are malicious. The challenge lies in accurately defining "normal" behavior, which can vary significantly across different environments. ISO/IEC 27001 and NIST SP 800-61 both highlight the importance of tuning anomaly detection models to reduce noise while preserving sensitivity to true threats.

Both methods are often used in tandem to balance detection accuracy with coverage, a concept known as hybrid or blended detection. This layered approach aligns with defense-in-depth strategies recommended in frameworks such as the NIST Cybersecurity Framework (CSF).

A third detection paradigm, **behavioral or heuristic detection** using machine learning, has grown significantly with the emergence of User and Entity Behavior Analytics (UEBA) platforms and AI-driven security tools such as Darktrace and Vectra. These systems model individual user and device behavior over time and flag deviations that neither signatures nor static baselines would catch. This is particularly effective against "living off the land" (LotL) attacks, a MITRE ATT&CK technique (T1059) where attackers use legitimate, pre-installed tools such as PowerShell, WMI, or certutil to execute malicious operations that produce no distinct file-based signature. The 2020 SolarWinds SUNBURST intrusion used LotL techniques extensively, communicating over legitimate DNS and HTTPS channels; post-incident analysis showed that behavioral ML models detecting unusual Orion process DNS query patterns were among the few technical controls capable of flagging the activity before the breach was publicly disclosed. Signature-based detection alone would have been entirely blind to this class of attack.
:::

%%%

---
unit: Logs
code: LOG
title: Logs, The Raw Material
---
:::callout style=soft
A **log** is a time-stamped, structured or unstructured record of a system event. These events may include authentication attempts, network connections, file access, system errors, or security alerts. Logs serve as the foundational data for audit trails, forensic investigations, and intrusion detection.
:::

:::image src="images/14_log_sources.png" alt="Diagram showing multiple log source categories (network infrastructure, operating systems, applications, security tools) with arrows flowing into a central log aggregation point, then into a SIEM platform for analysis; log format labels (syslog, EVTX, CLF, CEF) are shown on each source arrow" caption="Logs flow from every infrastructure component into a central collection point, the raw material that powers all detection, forensics, and compliance reporting" width=full
:::

:::flow
1. System, network, or application event occurs
2. Log entry generated in native format (syslog, EVTX, CLF, CEF, NetFlow, etc.)
3. Log collected by agent (e.g., Splunk Universal Forwarder) or syslog forwarder
4. Transmitted securely over encrypted channel (TLS) to centralized log storage
5. Normalized, indexed, and retained per policy (e.g., 90 days hot, 1 year archive)
6. Available for real-time SIEM correlation, forensic search, and compliance audit
:::

:::list heading="Common Log Sources" style=plain
- **Network Infrastructure**: Routers, switches, firewalls (e.g., Cisco ASA, Palo Alto)
- **Operating Systems**: Windows Event Logs, Linux syslog, auditd
- **Applications**: Web servers (Apache, Nginx), databases (MySQL, PostgreSQL), custom apps
- **Security Tools**: IDS/IPS systems (Snort, Suricata), EDR solutions, antivirus logs
:::

::::columns
::col::
:::table
| Log Type        | Example Source         | Protocol/Format         |
|-----------------|------------------------|--------------------------|
| System Logs     | Linux syslog           | syslog, journald         |
| Security Logs   | Windows Security Event Log | EVT/EVTX              |
| Network Logs    | Firewall               | syslog, CEF, NetFlow     |
| Application Logs| Apache HTTP Server     | Common Log Format (CLF)  |
:::
::col::
:::table
| Standard        | Purpose                          | Reference                  |
|-----------------|----------------------------------|----------------------------|
| NIST SP 800-92  | Guide to Computer Security Log Management | [NIST SP 800-92](https://csrc.nist.gov/publications/detail/sp/800-92/final) |
| ISO 27001/27002 | Information security management  | Audit logging controls     |
| RFC 3164        | The BSD syslog Protocol          | Legacy syslog format       |
| RFC 5424        | The Syslog Protocol (enhanced)   | Structured syslog format   |
:::
::::

:::notes
Logs are the fundamental building blocks of security monitoring and incident detection. A log entry, in its simplest form, is a timestamped record of an event that occurred on a system or network device. While a single log may appear insignificant, collectively, logs provide a comprehensive audit trail that enables security professionals to reconstruct events, detect anomalies, and respond to threats.

Logs are generated by nearly every component of an IT infrastructure. Firewalls produce logs of allowed and denied traffic; operating systems maintain audit logs of user logins and privilege changes; applications record errors, access attempts, and transactions. These logs often conform to standard formats such as syslog (RFC 3164 and RFC 5424), Common Log Format (CLF) for web servers, or Windows Event Log formats.

The value of logs is deeply tied to their integrity, availability, and structure. As outlined in NIST Special Publication 800-92, effective log management includes centralized collection, secure storage, and timely analysis. Without logs, intrusion detection systems (IDS) and security information and event management (SIEM) platforms would have no data to analyze for signs of compromise. For example, detecting a brute-force attack may rely on analyzing repeated failed login entries in authentication logs, or identifying a data exfiltration attempt may require correlating firewall and DNS query logs.

In real-world incidents, such as the exploitation of CVE-2021-44228 (Log4Shell), attackers often attempt to manipulate or erase logs to cover their tracks. This reinforces the criticality of not only collecting logs but also protecting their integrity and ensuring they are stored in a tamper-resistant manner.

Ultimately, logs are not just data, they are the raw material for visibility, accountability, and defense in cybersecurity.

Log integrity and chain of custody are especially critical when logs must serve as forensic evidence. NIST SP 800-86 (Guide to Integrating Forensic Techniques into Incident Response) requires that logs collected as potential evidence be acquired and preserved in a manner that demonstrates they have not been tampered with since collection, a requirement that makes immutable, write-once log storage (such as Amazon S3 Object Lock or write-once WORM storage) a best practice for security-sensitive environments. RFC 3161 (Internet X.509 PKI Time-Stamp Protocol) provides a mechanism for cryptographically timestamping log entries, providing non-repudiation and tamper evidence. The 2021 SolarWinds breach investigation was complicated by the fact that the SUNBURST malware deliberately avoided writing certain artifacts to Windows Event Logs and selectively removed log entries from Orion's own diagnostic logs, demonstrating concretely why log completeness, integrity verification, and centralized off-host storage are non-negotiable security controls. PCI DSS Requirement 10.5 mandates that audit logs be protected from modifications and that only individuals with a job-related need can view them, reinforcing these principles in compliance frameworks.
:::

%%%

---
unit: SIEM
code: SIM
title: SIEM Basics
---
:::callout style=soft
A **SIEM (Security Information and Event Management)** platform is a centralized system that aggregates, normalizes, and correlates security-relevant data (logs, events, alerts) from heterogeneous sources across an enterprise network to enable real-time analysis, threat detection, and compliance reporting.
:::

:::image src="images/14_siem_architecture.png" alt="Architecture diagram of a SIEM platform showing multiple data sources (firewall, IDS/IPS, endpoints, servers, applications) feeding logs via collectors into a central SIEM engine; inside the SIEM, labeled components show log ingestion, normalization, correlation engine, alert manager, dashboard, and storage backend" caption="A SIEM aggregates logs from every infrastructure layer into a single correlation engine, turning raw event data into actionable security intelligence" width=full
:::

::::columns
::col::
:::list heading="Core Functions of SIEM" style=plain
- Log Collection & Aggregation
- Event Normalization
- Real-Time Correlation
- Alerting & Notification
- Forensic Analysis & Reporting
:::
::col::
:::flow
Raw logs from endpoints, servers, firewalls, IDS/IPS
↓
Centralized log ingestion and parsing
↓
Normalization into common schema
↓
Correlation using rules or UEBA
↓
Alert generation and dashboard visualization
:::
::col::
:::table
| Component        | Purpose                                      |
|------------------|----------------------------------------------|
| Log Collector    | Gathers logs via agents, Syslog, APIs        |
| Correlation Engine | Applies rules to detect patterns          |
| Alert Manager    | Triggers notifications based on severity     |
| Dashboard        | Visualizes threats and trends                |
| Storage Backend  | Archives logs for forensics and compliance   |
:::
::::

:::notes
A Security Information and Event Management (SIEM) system serves as the nerve center for enterprise cybersecurity operations. Defined in NIST Special Publication 800-92, a SIEM integrates log management with real-time event correlation to detect anomalies and potential threats that may otherwise remain hidden in isolation. The fundamental architecture of a SIEM involves collecting logs from a wide range of sources, such as firewalls, intrusion detection systems, endpoint protection platforms, servers, and network devices, and normalizing them into a standardized format for consistent analysis.

The true value of a SIEM lies in its ability to perform correlation across multiple data sources using predefined rules or advanced analytics such as User and Entity Behavior Analytics (UEBA). For instance, while a single failed login attempt may be benign, a pattern of repeated authentication failures followed by a successful login, potentially indicative of a password-spraying or brute-force attack, can only be detected through cross-system correlation. This aligns with MITRE ATT&CK techniques such as T1110 (Brute Force) and T1078 (Valid Accounts), where adversaries attempt to gain access using legitimate credentials after reconnaissance.

SIEMs also play a critical role in regulatory compliance, supporting frameworks like ISO/IEC 27001 and NIST CSF by providing audit trails, incident response capabilities, and long-term log retention. Modern SIEM platforms often integrate with threat intelligence feeds and SOAR (Security Orchestration, Automation, and Response) tools to enhance detection accuracy and automate response workflows. Without a SIEM, organizations operate with fragmented visibility, increasing the risk of undetected breaches and non-compliance penalties.

In production SOC environments, leading SIEM platforms include **Splunk Enterprise Security** (the platform explored in Splunk Fundamentals), **IBM QRadar**, **Microsoft Sentinel** (cloud-native, built on Azure Log Analytics), and open-source alternatives such as **Wazuh** (SIEM + XDR on the ELK Stack) and **Graylog**. The effectiveness of a SIEM is largely determined by its **use case library**, the set of correlation rules, each typically mapped to a specific MITRE ATT&CK technique. For example, a use case for T1003 (OS Credential Dumping) might correlate Windows Event ID 4688 (new process creation) showing lsass.exe being accessed by a non-system process with a Sysmon Event ID 10 (process access) from the same host within a 60-second window. NIST SP 800-137 (Information Security Continuous Monitoring) provides the policy framework that mandates this type of use-case-driven continuous monitoring as a core organizational security capability, with SIEM platforms as the primary technical implementation vehicle.
:::

%%%

---
unit: Alerts
code: ALT
title: Alerts & Alert Fatigue
---

:::callout style=line
**Alert fatigue** is a critical operational challenge in cybersecurity monitoring, where an overwhelming volume of alerts, many of them false positives, leads to desensitization and reduced responsiveness by security analysts. This condition undermines the effectiveness of intrusion detection systems (IDS) and security information and event management (SIEM) platforms.
:::

:::image src="images/14_alert_fatigue.png" alt="Diagram showing a SOC analyst overwhelmed by a high volume of alert notifications, with a large proportion labeled 'False Positive' in grey and a small number labeled 'True Positive' in red; the analyst misses the true positive buried in the noise, illustrating the consequences of alert fatigue" caption="Alert fatigue occurs when false positives drown out true threats, the true positive gets lost in the noise, and real incidents go uninvestigated" width=full
:::

:::list heading="Strategies to Mitigate Alert Fatigue" style=plain
- **Rule Tuning**: Adjusting detection logic to suppress benign activity and reduce false positives.
- **Risk-Based Prioritization**: Assigning severity scores using frameworks like NIST SP 800-92 or CVSS to triage alerts.
- **Automated Triage and Enrichment**: Leveraging SOAR platforms and machine learning to filter and contextualize alerts before human review.
- **Alert Correlation**: Grouping related alerts to reduce redundancy and highlight attack patterns.
:::

::::columns
::col::
:::table
| Alert Type        | Description                             | Mitigation Strategy         |
|-------------------|-----------------------------------------|-----------------------------|
| True Positive     | Valid security incident                 | Immediate investigation     |
| False Positive    | Benign activity flagged as malicious    | Rule tuning, filtering      |
| False Negative    | Malicious activity not detected         | Improve detection logic     |
| Noise             | Low-value, repetitive alerts            | Suppression, aggregation    |
:::
::col::
:::steps heading="Alert Lifecycle Management"
1. **Detection**: Generated by IDS/IPS, SIEM, or EDR tools
2. **Triage**: Prioritized by severity and contextual data
3. **Investigation**: Analyst reviews and validates the alert
4. **Response**: Action taken to mitigate or remediate
5. **Feedback Loop**: Tuning rules based on outcomes
:::
::::

:::notes
Alert fatigue is a well-documented phenomenon in cybersecurity operations, particularly within Security Operations Centers (SOCs). It arises when security analysts are inundated with a high volume of alerts, many of which are false positives or low-fidelity signals, leading to desensitization and a decreased likelihood of responding to genuine threats. This degradation in analyst response directly correlates with an increased risk of successful attacks slipping through unnoticed, a concept closely related to the "cry wolf" syndrome in human psychology.

The root causes of alert fatigue are multifaceted. Legacy signature-based IDS systems often produce excessive alerts for benign anomalies. Modern environments, especially those leveraging cloud and microservices architectures, generate massive volumes of log data, further amplifying the signal-to-noise ratio. Without proper tuning and contextual enrichment, even advanced SIEM and EDR platforms can contribute to alert overload.

To combat this, organizations adopt several best practices aligned with NIST SP 800-92 (Guide to Computer Security Log Management) and ISO/IEC 27001 controls. These include implementing risk-based alert scoring using frameworks like CVSS or proprietary models, leveraging SOAR (Security Orchestration, Automation, and Response) platforms to automate triage, and applying machine learning to distinguish between noise and legitimate threats. Correlation engines are used to group related alerts into incidents, reducing redundancy and improving analyst efficiency.

Additionally, continuous feedback loops are essential. Analysts must regularly review alert outcomes to refine detection rules, ensuring systems evolve with the threat landscape. CVEs such as CVE-2021-44228 (Log4Shell) have historically caused massive alert spikes, underscoring the need for dynamic alert management strategies. Ultimately, managing alert fatigue is not just about reducing volume, it's about increasing the signal quality and restoring analyst trust in security systems.

The 2019 Capital One data breach, which exposed over 100 million customer records, provides a cautionary real-world example. A Web Application Firewall (WAF) generated alerts indicating unusual metadata service queries from the affected EC2 instances, but these alerts were not escalated in a timely manner, partly attributed to the volume of security events the team was managing at the time. The breach, which exploited a server-side request forgery (SSRF) vulnerability, was ultimately discovered externally rather than by internal monitoring, despite the presence of alerting mechanisms. This case is frequently cited in discussions of SOC maturity and the importance of building alert pipelines that prioritize signal quality over raw volume, with SOAR-driven automated enrichment reducing the time an analyst must spend on each alert before deciding whether to escalate or dismiss.
:::

%%%

---
unit: Synthesis
code: WFL
title: A Detection Workflow
---

:::image src="images/14_detection_workflow.png" alt="End-to-end detection workflow diagram showing: (1) firewall permitting a connection, (2) IDS observing the connection's behavior and matching a signature, (3) alert logged and sent to SIEM, (4) SIEM correlating with other events from the same IP, (5) analyst escalating to incident response, each step shown as a labeled stage in a left-to-right process flow" caption="Detection is a pipeline, not a single tool, traffic flows from the firewall through IDS observation, SIEM correlation, and analyst investigation before an incident is declared" width=full
:::

:::steps
Firewall allows a connection that matches its rules
IDS notices the connection's behavior matches a known attack pattern
An alert is logged and sent to the SIEM
The SIEM correlates it with other suspicious activity from the same IP
An analyst investigates and escalates to incident response
:::
::::columns
::col::
:::callout
**Detection in Context**

This workflow demonstrates how layered defenses operate in a real-world environment. Even when traffic is permitted by policy enforcement points like firewalls, behavioral analysis systems such as Intrusion Detection Systems (IDS) can identify malicious intent through signature matching or anomaly detection.
:::
::col::
:::callout
**Correlation & Escalation**

Security Information and Event Management (SIEM) platforms play a critical role in aggregating and correlating alerts across multiple sources. Analysts then use these correlated insights to make informed decisions about potential threats, triggering formal incident response procedures when necessary.
:::
::::
:::notes
In modern cybersecurity architectures, detection does not occur in isolation. Rather, it emerges from the orchestrated interaction of multiple defensive layers. This workflow illustrates a typical sequence of events in a network-based threat detection process, aligned with principles outlined in NIST SP 800-92 (Guide to Computer Security Log Management) and NIST SP 800-61 (Computer Security Incident Handling Guide).

The process begins when a firewall permits a connection because it conforms to predefined access control rules. However, compliance with policy does not guarantee benign intent. Advanced adversaries often exploit legitimate services or craft traffic that mimics normal behavior. This is where an Intrusion Detection System (IDS), operating on either signature-based or anomaly-based detection models, becomes essential. For example, Snort or Suricata rules may detect patterns associated with known exploits such as those cataloged under CVE entries like CVE-2021-44228 (Log4Shell).

Once the IDS identifies suspicious behavior, it generates an alert. This alert is typically forwarded to a centralized logging system or directly to a Security Information and Event Management (SIEM) platform such as Splunk, IBM QRadar, or ELK Stack. The SIEM performs temporal and contextual correlation, linking this alert with other related activities, such as repeated failed logins or lateral movement attempts from the same source IP address.

Finally, a security analyst reviews the correlated data. If the activity meets the organization's criteria for an incident, as defined in ISO/IEC 27035 or NIST SP 800-61, an escalation to the incident response team occurs. This transition marks the shift from detection to active investigation and remediation, forming the bridge to the next phase of the security lifecycle.

The mean time to detect (MTTD) and mean time to respond (MTTR) are the key operational metrics used to evaluate how effectively this workflow performs in practice. Industry benchmarks from the IBM Cost of a Data Breach Report (2023) show that organizations with mature SIEM and IDS/IPS programs detect breaches in an average of 197 days, versus 272 days for organizations without, and contain them 74 days faster, translating to an average cost reduction of over $1.5 million per breach. This data underscores why investing in detection pipeline maturity, from well-tuned IDS signatures to enriched SIEM correlation rules and trained SOC analysts following documented playbooks, directly and measurably reduces the financial and operational impact of security incidents. The escalation step in this workflow connects directly to the Incident Response lifecycle defined in NIST SP 800-61 Rev. 2: Preparation → Detection & Analysis → Containment, Eradication & Recovery → Post-Incident Activity.
:::

%%%

---
unit: Summary
code: SUM
title: Watching What Got Through
---

:::image src="images/14_watching_what_got_through.png" alt="Summary diagram showing a four-layer monitoring stack from bottom to top: Firewall (perimeter enforcement), IDS/IPS (traffic inspection and detection), SIEM (log aggregation and correlation), and SOC Analyst (human review and response); threat indicators flow upward through each layer, with the escalation path shown on the right side" caption="Post-firewall monitoring is where most real detections happen, IDS, IPS, and SIEM together provide the visibility that the perimeter alone cannot" width=full
:::

:::pullquote
Firewalls decide what's allowed. IDS, IPS, and SIEM decide what's actually happening, and that distinction is where most real detections happen.
:::

::::columns
::col::
:::list heading="Detection Layers" style=plain
- **Firewall**: First line of defense; enforces access control
- **IDS**: Passive detection of policy violations or anomalies
- **IPS**: Active prevention based on real-time analysis
- **SIEM**: Centralized log aggregation and correlation
:::
::col::
:::list heading="Post-Breach Monitoring" style=plain
- Behavioral anomaly detection
- Lateral movement tracking
- Credential misuse identification
- Data exfiltration alerts
:::
::col::
:::list heading="Response Mechanisms" style=plain
- Automated alerting and escalation
- Forensic log retention
- Integration with SOAR platforms
- Incident response playbooks
:::
::::

:::notes
This final conceptual module emphasizes the critical distinction between access control and behavioral monitoring. Firewalls operate at the network perimeter, making allow/deny decisions based on static rules such as IP addresses, ports, and protocols. However, once traffic is permitted through the firewall, it does not guarantee its benign nature. Modern adversaries exploit this trust by using legitimate channels, such as DNS tunneling (e.g., CVE-2021-34486), HTTPS encryption, or web-based command-and-control protocols, to conduct malicious activities within allowed traffic flows.

Intrusion Detection Systems (IDS) and Intrusion Prevention Systems (IPS) serve as secondary layers of inspection. While an IDS passively monitors network traffic for signatures or anomalies indicative of compromise (e.g., Snort rulesets or Suricata ETOpen/ETPro rules), an IPS takes active measures to block or modify suspicious packets in real time. These systems often implement both signature-based detection (aligned with NIST SP 800-94 guidelines on network monitoring) and anomaly-based detection that leverages machine learning or statistical models.

Security Information and Event Management (SIEM) systems like Splunk, IBM QRadar, or open-source alternatives such as Wazuh aggregate logs from endpoints, network devices, applications, and security tools. They apply correlation rules to detect multi-stage attacks that may evade single-point detection mechanisms. For example, a SIEM might correlate a successful phishing login (endpoint log) followed by unusual SMB connections (network log), indicating potential lateral movement consistent with techniques described in the MITRE ATT&CK framework (e.g., T1021.002 – SMB/Windows Admin Shares).

The key takeaway is that post-firewall visibility, what we term "watching what got through"—is where advanced persistent threats (APTs) are most likely to be detected. This aligns with the defense-in-depth strategy outlined in NIST SP 800-53 and ISO/IEC 27001, which advocate for layered monitoring and continuous assessment even after initial access controls have been satisfied.

The maturity of an organization's detection and response capability is assessed using models such as the **SOC Capability Maturity Model (SOC-CMM)** and the **NIST Cybersecurity Framework maturity tiers**, which distinguish between reactive organizations that respond only to known incidents (Tier 1) and adaptive organizations that perform continuous, risk-informed monitoring with automated threat hunting (Tier 4). Achieving higher maturity requires not just deploying IDS, IPS, and SIEM, but integrating them with threat intelligence platforms (TIPs), SOAR automation, and red team exercises to continuously validate detection coverage against evolving adversary techniques. The MITRE ATT&CK framework's Defender's perspective encourages organizations to map their current detection tooling against the ATT&CK matrix, identifying technique coverage gaps and prioritizing new detection rules accordingly, a practice that directly connects the concepts in this class to operational security engineering in the real world.
:::

%%%

---
unit: Architecture
code: TAP
title: Network TAP vs SPAN Port
---

:::callout style=soft
IDS sensors need a copy of live traffic to analyze. Two primary methods exist for delivering that copy: **Network TAPs** (Test Access Points), which are passive hardware devices, and **SPAN ports** (Switch Port Analyzer), which are software-configured mirror ports on a switch. The choice between them significantly affects detection fidelity.
:::

:::image src="images/14_tap_vs_span.png" alt="Side-by-side diagram showing a network TAP (left) inserted between two network devices, splitting the full-duplex fiber or copper signal and sending copies to an IDS sensor with zero packet loss and no switch CPU involvement; and a SPAN port (right) configured on a managed switch mirroring selected traffic to an IDS monitor port, with a warning label noting potential packet loss and switch CPU overhead under high load" caption="A TAP passively copies every bit on the wire; a SPAN port mirrors traffic through switch software, TAPs are lossless, SPAN ports can drop packets under load" width=full
:::

::::columns
::col::
:::table
| Attribute | Network TAP | SPAN Port |
|---|---|---|
| **Traffic Fidelity** | 100%, lossless, full-duplex | May drop packets under high load |
| **Switch CPU Impact** | None, hardware-passive | Yes, consumes switch resources |
| **Cost** | Higher (dedicated hardware) | Free, built into managed switches |
| **Physical Disruption** | Requires inline insertion | Configuration only |
| **Error Frame Capture** | Yes, sees all frame types | Often filtered by switch ASIC |
| **Best For** | High-fidelity forensic capture | Low-budget or temporary deployments |
:::
::col::
:::callout style=soft
The appropriate method differs between a regulated environment, such as a PCI DSS cardholder data environment, and a small office branch, which shows how risk tolerance and budget interact with technical architecture decisions.
:::
::::

:::notes
The mechanism by which an IDS sensor receives traffic for analysis is a fundamental architectural decision that directly affects detection quality. Two primary approaches are used: hardware network TAPs and software-configured SPAN ports on managed switches.

A **Network TAP** (Test Access Point) is a purpose-built hardware device that is inserted physically into a network link, typically between a firewall and a core switch, or at another critical choke point. The TAP passively splits the optical or electrical signal and sends a copy to the monitoring port without modifying or introducing latency to the original traffic path. Because the splitting is entirely hardware-passive, a TAP captures 100% of frames including malformed frames, physical-layer errors, and out-of-order packets that managed switch ASICs typically filter out. NIST SP 800-94 Section 3.1.2 explicitly recommends TAPs over SPAN ports for production IDS deployments where detection fidelity is critical, noting that SPAN ports "may not capture all traffic of interest" under high utilization conditions.

A **SPAN port** (also called a mirror port or port monitor) is configured entirely in software on a managed switch. An administrator specifies one or more source ports or VLANs whose traffic should be copied to a designated monitor port connected to the IDS sensor. SPAN ports are inexpensive (already built into any managed enterprise switch) and easy to reconfigure without physical access, making them popular for ad-hoc investigations or budget-constrained deployments. However, SPAN ports have well-documented limitations: under high switch backplane load, the mirror copy is deprioritized and packets are dropped before they reach the monitor port. The live traffic is never affected, but the IDS sensor silently loses visibility without any indication that packets are missing.

From a compliance standpoint, PCI DSS Requirement 10.6 mandates reviewing logs and security events for all system components in the cardholder data environment daily, a requirement predicated on those logs being complete. If a SPAN port drops packets during a peak transaction window, the IDS never generates an alert for attacks that occurred during that window, and the organization may incorrectly believe it has met its continuous monitoring obligations. This silent coverage gap is the primary reason that high-fidelity regulated environments standardize on hardware TAPs despite the additional hardware cost.

A network TAP copies every packet like a photocopier, while a SPAN port re-sends copies from the switch and can drop packets under load, as a typist re-typing a document might miss a line. This is why SPAN ports lose fidelity at high utilization and TAPs do not.
:::

%%%

---
unit: Architecture
code: NIDS
title: NIDS vs HIDS, Deployment Scope
---

:::callout style=soft
IDS deployments fall into two fundamental scopes: **Network-based IDS (NIDS)** monitors traffic at the network level, providing broad visibility across all hosts simultaneously; **Host-based IDS (HIDS)** is installed on individual endpoints, providing deep visibility into that host's internal state. Most enterprise environments deploy both.
:::

:::image src="images/14_nids_vs_hids.png" alt="Network diagram showing a NIDS sensor connected to a core switch via a TAP, with visibility across all east-west and north-south traffic between multiple hosts; beside it, three individual workstations each running a HIDS agent that monitors local system calls, file integrity, registry changes, and log events, with arrows from each agent to a central SIEM" caption="NIDS sees everything crossing the wire; HIDS sees everything happening inside the host, together they eliminate the blind spots each would have alone" width=full
:::

::::columns
::col::
:::list heading="NIDS Strengths" style=plain
- Broad visibility across all hosts simultaneously
- No agent installation required on endpoints
- Detects network-layer attacks (port scans, DDoS, protocol anomalies)
- Single sensor can cover entire network segment
- Attacker cannot tamper with sensor from compromised host
:::
::col::
:::list heading="HIDS Strengths" style=plain
- Sees encrypted traffic after decryption on the host
- Detects insider threats and local privilege escalation
- File integrity monitoring (FIM) for critical system files
- Monitors process creation, registry changes, and system calls
- Effective for detecting "living off the land" (LotL) attacks
:::
::::

:::table
| Attribute | NIDS | HIDS |
|---|---|---|
| **Blind to Encrypted Traffic** | Yes (unless decrypted) | No, sees plaintext post-decryption |
| **Coverage** | Entire network segment | Single host |
| **Attack Surface** | Low (passive, out-of-band) | Higher (agent runs on host) |
| **Examples** | Snort, Suricata, Zeek | OSSEC, Wazuh, Tripwire, Carbon Black |
:::

:::notes
The distinction between Network-based IDS (NIDS) and Host-based IDS (HIDS) is one of the most important architectural decisions in building a detection capability. Each class of system has complementary strengths and blind spots, and understanding these is essential for designing a complete monitoring program aligned with NIST SP 800-94 guidance.

**NIDS** places sensors at strategic network chokepoints, typically at the perimeter, between zones, or at the core distribution layer. Because it observes network traffic as a passive, out-of-band copy, NIDS can cover every host on a subnet simultaneously with a single sensor. It is particularly effective at detecting network reconnaissance techniques such as port scanning (MITRE ATT&CK T1046), protocol-level exploits, and north-south traffic anomalies. However, NIDS has a fundamental architectural blind spot: as TLS encryption has become near-universal (as of 2023, over 95% of web traffic is HTTPS according to Google Transparency Report data), NIDS sensors cannot inspect encrypted payloads without a TLS inspection proxy decrypting traffic inline. A NIDS sensor sees only that an encrypted connection was established, not what was transmitted. This means that command-and-control traffic over HTTPS, data exfiltration over encrypted channels, and application-layer attacks within TLS sessions are invisible to a NIDS without SSL/TLS decryption.

**HIDS** addresses this blind spot by operating after decryption, on the endpoint itself. Because the host's own stack processes the data, HIDS agents can observe plaintext application data regardless of transport encryption. HIDS is also the only mechanism capable of detecting certain host-centric attack techniques: file integrity monitoring (FIM) alerts when critical system files (e.g., /etc/passwd, Windows Registry Run keys) are modified; process monitoring detects when unusual parent-child process relationships appear (e.g., Microsoft Word spawning cmd.exe, a common indicator of macro-based phishing exploitation); and system call monitoring can detect privilege escalation attempts that never generate network traffic at all.

The primary weakness of HIDS is operational complexity and agent attack surface. Every managed endpoint must have the agent installed, updated, and running, a fleet management challenge at enterprise scale. Additionally, a sophisticated attacker who gains root or SYSTEM privileges on a host may be able to tamper with or disable the local HIDS agent. This is why NIST SP 800-94 recommends ensuring that HIDS log output is forwarded immediately to a remote, tamper-resistant SIEM, so even if the agent is killed, the logs it had already forwarded remain available for investigation. The combination of both NIDS and HIDS, feeding into a common SIEM, eliminates the respective blind spots of each and is the architecture used by mature SOC programs.

Data exfiltrated to a personal cloud account over HTTPS is invisible to a network IDS, which cannot read the encrypted payload, but visible to a host IDS or DLP agent that monitors the browser process on the endpoint. This is the encryption blind spot of network-based detection.
:::

%%%

---
unit: Tools
code: SNORT
title: Tool Spotlight, Snort
---

:::callout style=soft
**Snort** is the world's most widely deployed open-source network intrusion detection and prevention system. Originally created by Martin Roesch in 1998 and now maintained by Cisco Talos, Snort performs real-time traffic analysis and packet logging, using a powerful rule language to detect a wide variety of attacks and probes.
:::

:::image src="images/14_snort_tool.png" alt="Diagram showing Snort's processing pipeline: packets arrive from a network TAP or SPAN port, pass through the packet decoder (Ethernet/IP/TCP parsing), the preprocessor layer (stream reassembly, HTTP normalization, protocol inspection), the detection engine (rule matching against the Snort rule set), and the output plug-in layer (unified2 log, syslog, JSON, Splunk HEC); key components labeled include the rule file, alert threshold settings, and community and commercial rulesets" caption="Snort processes every packet through a pipeline of decoders, preprocessors, and the detection engine, matching against thousands of rules in microseconds" width=full
:::

:::list heading="Core Snort Modes" style=plain
- **Sniffer mode**: Reads packets off the network and displays them on the console (like tcpdump)
- **Packet logger mode**: Logs packets to disk for later analysis
- **NIDS mode**: Analyzes network traffic in real time against a rule set and generates alerts
- **Inline/IPS mode**: Deployed inline using NFQUEUE or IPFW to drop malicious packets
:::

:::table
| Component | Purpose |
|---|---|
| Rule Set | Community (free), ET Open (Emerging Threats), Talos Subscriber (paid) |
| Preprocessors | Stream reassembly, HTTP/SMTP/DNS normalization before rule matching |
| Detection Engine | Fast pattern matching against all active rules |
| Output Plug-ins | unified2, syslog, JSON, database, Splunk HEC |
:::

:::notes
Snort occupies a unique position in the IDS/IPS ecosystem: it is simultaneously the most widely deployed open-source NIDS tool, the foundation for a significant portion of commercial IDS products, and the platform whose rule language has effectively become the industry standard for signature-based network threat detection. Understanding how Snort works provides insight into the mechanics of network intrusion detection that apply equally to Suricata, Cisco FirePOWER (which is Snort-based), and many commercial appliances that license the Snort engine under the hood.

Snort's architecture follows a clear pipeline model. Raw packets are captured from the network interface (either passively via libpcap, or inline via NFQUEUE on Linux or IPFW on BSD). The packet decoder dissects the packet layer by layer, Ethernet frame, IP header, TCP/UDP/ICMP header, application-layer payload, and hands the decoded structure to the preprocessor layer. Preprocessors handle protocol normalization (HTTP URL decoding, SMTP command parsing, DNS query extraction) and stream reassembly, which reconstructs fragmented IP datagrams and TCP byte streams into the complete application-layer data that the detection engine will evaluate. This stream reassembly step is critical: without it, an attacker can trivially evade signature matching by splitting an exploit payload across multiple TCP segments.

The detection engine applies Snort's rule set to the normalized, reassembled traffic. A Snort rule consists of a rule header (action, protocol, source/destination IP and port) and rule options (content patterns, byte tests, PCRE regex, flow direction, CVE references). For example, a rule detecting CVE-2021-44228 (Log4Shell) in an HTTP request body uses a content match on the string "${jndi:" in the HTTP request URI or body fields. The Cisco Talos commercial subscription rule set includes thousands of such rules, updated typically within hours of a CVE's public disclosure.

Output plug-ins determine where detected events go. In a production SOC, Snort typically writes to unified2 binary format (consumed by Barnyard2 or Pulledpork for database insertion) or directly to a Splunk HTTP Event Collector (HEC) endpoint, providing near-real-time visibility in the SIEM dashboard. NIST SP 800-94 Section 4.3 specifically recommends that NIDS output be integrated with centralized logging and SIEM platforms to enable correlation and retention aligned with organizational log management policy.

Signature detection matches a known pattern, such as a specific string, in traffic. Its weakness is that a trivial transformation of the payload, for example URL-encoding the matched string, evades a naive content rule, which is why signatures must be written against robust invariants and paired with behavioral detection.
:::

%%%

---
unit: Tools
code: SURICATA
title: Tool Spotlight, Suricata & Zeek
---

:::callout style=soft
**Suricata** and **Zeek** are two open-source network security monitoring tools that complement Snort, Suricata as a high-performance multi-threaded IDS/IPS, and Zeek as a network metadata and behavioral analysis platform rather than a signature-matching engine.
:::

:::image src="images/14_suricata_zeek.png" alt="Split diagram: on the left, Suricata's multi-threaded packet processing architecture with multiple CPU cores running parallel detection threads, all processing the same network stream and writing EVE JSON output; on the right, Zeek's analysis pipeline converting raw packets into rich network metadata logs (conn.log, dns.log, http.log, ssl.log, files.log) that are forwarded to a SIEM for behavioral analysis, no signature matching shown for Zeek, emphasizing its metadata-first approach" caption="Suricata brings multi-core speed to signature matching; Zeek generates rich behavioral metadata that signatures alone would never produce" width=full
:::

::::columns
::col::
:::list heading="Suricata Advantages" style=plain
- Native multi-threading, scales to 40+ Gbps on commodity hardware
- Suricata rules are compatible with the Snort rule language (with extensions)
- Built-in TLS certificate logging and JA3 fingerprinting
- EVE JSON output natively parseable by Splunk, Elastic, and SIEM platforms
- Supports both IDS (passive) and IPS (inline via NFQUEUE) modes
:::
::col::
:::list heading="Zeek Advantages" style=plain
- Produces structured, queryable network metadata logs (conn.log, dns.log, http.log, ssl.log, files.log)
- Protocol analyzers extract application-layer semantics, not just packet bytes
- Scripting language for custom protocol analysis and behavioral detection
- Ideal for threat hunting, enables retrospective querying of network behavior
- JA3/JA3S TLS fingerprinting and certificate extraction built in
:::
::::

:::notes
While Snort defined the signature-based IDS paradigm, two other open-source tools have become essential components of modern network security monitoring programs: Suricata and Zeek. Each addresses limitations of the Snort model in different ways.

**Suricata**, developed by the Open Information Security Foundation (OISF), was designed from the ground up to exploit multi-core processor architectures. Snort's single-threaded processing model creates a throughput ceiling, on a busy 10 Gbps link, a single-threaded Snort instance may drop packets before it can inspect them, creating silent coverage gaps identical to the SPAN port overload problem discussed earlier. Suricata distributes packet processing across multiple CPU cores, enabling it to inspect full-rate traffic on 10 Gbps and even 40 Gbps links on commodity server hardware. Suricata uses the same Snort rule syntax (with extensions for specific Suricata-only keywords), so organizations can reuse existing rule investments while gaining the performance benefits of multi-threading. Suricata's EVE JSON output format has become a de facto standard for SIEM ingestion, Splunk, Elastic Stack, and Microsoft Sentinel all ship pre-built parsers for EVE JSON, making Suricata the most common open-source IDS back-end in production SOC environments today.

**Zeek** (formerly named Bro, renamed in 2018) takes a fundamentally different approach. Rather than matching packet streams against signature rules, Zeek acts as a protocol analyzer and network metadata generator. For each observed network connection, Zeek writes structured log entries capturing the semantics of the connection at the application layer: the HTTP request URI, method, host, user-agent, and response code (http.log); the DNS query name, type, and response (dns.log); TLS certificate details, cipher suite, and JA3 fingerprint (ssl.log); transferred file metadata including MD5/SHA1 hashes (files.log); and the basic five-tuple connection summary with bytes transferred and duration (conn.log). This metadata is queryable long after the raw packets have been discarded, enabling threat hunters to answer questions like "what DNS queries did host X make in the 30 minutes before this alert?" or "which hosts connected to an IP that has since been added to a threat intelligence blocklist?" MITRE ATT&CK detections for many techniques, particularly those involving DNS-based C2 (T1071.004) or HTTPS beaconing (T1071.001), are most effectively implemented using Zeek's dns.log and conn.log rather than signature rules, because the detection logic requires behavioral patterns (periodic connection intervals, consistent byte counts, unusual domain entropy) rather than specific payload content.

Flow-based monitoring tools such as Zeek record connection metadata rather than matching signatures, so they can catch patterns no signature can, for example the unusually high-entropy subdomains produced by the domain generation algorithm SUNBURST used for command and control, which stand out immediately in DNS logs.
:::

%%%

---
unit: Tools
code: SPLUNK
title: Tool Spotlight, Splunk as SIEM
---

:::callout style=soft
**Splunk** is the industry-leading data platform used as a SIEM in thousands of enterprise SOCs worldwide. It ingests machine data from any source, indexes it for fast search, and enables real-time alerting, dashboards, and correlation through its **Search Processing Language (SPL)**.
:::

:::image src="images/14_splunk_siem.png" alt="Splunk architecture diagram showing Universal Forwarders on endpoints and network devices sending data via Splunk's S2S protocol to an Indexer cluster; the Search Head provides the analyst interface with the SPL search bar, saved searches, correlation rules, and dashboards; an alert is shown firing from a saved SPL search and being routed to a ticketing system via Splunk's alert action framework" caption="Splunk ingests data from everywhere, indexes it for millisecond search, and exposes a powerful query language, making it the analyst's primary investigation interface" width=full
:::

:::flow
1. Universal Forwarder (UF) installed on endpoint or log source
2. UF reads log files or receives syslog and forwards to Heavy Forwarder or Indexer
3. Indexer parses, timestamps, and indexes events into buckets (hot → warm → cold → frozen)
4. Analyst searches indexed data using SPL via the Search Head
5. Saved searches run on schedule and fire alerts when conditions are met
6. Alerts route to email, PagerDuty, JIRA, or SOAR platform for incident tracking
:::

::::columns
::col::
:::list heading="Key Splunk Components" style=plain
- **Universal Forwarder**: Lightweight agent for log collection
- **Heavy Forwarder**: Pre-processes and routes data
- **Indexer**: Stores and indexes event data
- **Search Head**: Analyst interface and SPL execution engine
- **Splunk Enterprise Security (ES)**: SIEM app built on the Splunk platform
:::
::col::
:::callout style=soft
**SPL Basics:**  
`index=security sourcetype=wineventlog EventCode=4625 | stats count by src_ip | where count > 10`

This query counts failed Windows logon events (Event ID 4625) per source IP and surfaces any IP with more than 10 failures, a basic brute-force detection use case.
:::
::::

:::notes
Splunk occupies the dominant market position in enterprise SIEM deployments and is the platform that the Splunk Fundamentals course is built around, making it essential to understand how Splunk functions both as a data platform and as the analyst's primary investigation tool in a SOC environment.

At its core, Splunk is a data indexing and search engine optimized for machine-generated time-series data, log files, metrics, network flow records, alerts, and events from any technology in the infrastructure stack. Unlike relational databases that require a predefined schema before data is ingested, Splunk applies schema-at-search-time: raw log data is ingested and stored with minimal transformation, and the structure is interpreted at query time based on field extraction rules. This approach dramatically reduces the friction of onboarding new data sources, a new firewall model can be sending logs to Splunk within minutes by pointing its syslog output at a Splunk Universal Forwarder, even before formal parsing rules are configured.

The Universal Forwarder (UF) is a lightweight agent (approximately 10 MB on disk) that can be deployed on every endpoint in the environment. The UF tails log files, monitors Windows Event Log channels, and forwards data to Splunk Indexers over an encrypted TCP channel using Splunk's proprietary S2S protocol. This agent-based collection model is what enables HIDS-level visibility within the Splunk ecosystem, combined with Sysmon (Windows System Monitor) configuration on endpoints, the UF can forward rich process creation, network connection, and registry change events that are essential for detecting endpoint-level attack techniques.

The Search Processing Language (SPL) is the query interface that analysts use to investigate events and build detection rules. SPL follows a pipeline model where commands are chained with the pipe character: each command takes the output of the previous one as input. A typical SOC investigation might begin with a broad search (`index=network sourcetype=paloalto action=allowed dest_port=4444`) and then narrow scope through filtering, statistical aggregation (`stats count by src_ip`), time-based analysis (`timechart count by src_ip`), and enrichment via lookup tables that add asset context or threat intelligence data.

Saved searches form the foundation of SIEM alerting in Splunk. A saved search runs on a configurable schedule (e.g., every 5 minutes, every hour) and fires an alert action when the search returns results. Alert actions can create a notable event in Splunk Enterprise Security, send an email, call a webhook to a SOAR platform like Splunk SOAR (formerly Phantom), or open a ticket in JIRA or ServiceNow. NIST SP 800-137 (Information Security Continuous Monitoring) guidance maps directly to Splunk's saved search cadence, the recommendation to review critical security events within one hour corresponds to a saved search running every 15 minutes with an immediate page-out alert action for high-severity findings.

The most important SIEM query pattern is aggregate-then-rank: counting authentication failures by source address and sorting reveals which host is generating the most failed logins. This "stats then filter" pattern detects brute force, port scanning and other volume-based attacks.
:::

%%%

---
unit: Worked Example
code: SPL1
title: SPL Worked Example, Detecting a Brute-Force Attack
---

:::callout style=soft
This worked example walks through how a SOC analyst uses Splunk SPL to detect a password brute-force attack against Windows systems, starting from raw event data and building toward a production-ready detection rule.
:::

:::image src="images/14_spl_bruteforce.png" alt="Screenshot mockup of the Splunk search interface showing an SPL query for Windows Event ID 4625 failures, with a bar chart visualization displaying source IP addresses on the X axis and failure counts on the Y axis; one IP bar is highlighted in red showing over 500 failures in 10 minutes, clearly standing out from the baseline noise of single-digit failures from other IPs" caption="SPL turns raw Windows event data into a clear visual signal, one IP with 500+ failures in 10 minutes is impossible to miss on this chart" width=full
:::

:::steps
Step 1, Find all failed Windows logon events (Event ID 4625) in the last 60 minutes:
`index=wineventlog EventCode=4625 earliest=-60m`

Step 2, Aggregate by source IP and count failures:
`| stats count as failure_count by src_ip, user`

Step 3, Filter to IPs with more than 20 failures (brute-force threshold):
`| where failure_count > 20`

Step 4, Sort by failure count descending and enrich with asset data:
`| sort -failure_count | lookup asset_inventory ip_address as src_ip OUTPUT hostname, owner, department`

Step 5, Save as a scheduled alert running every 15 minutes, alerting when results > 0:
`Alert action: Create notable event in Splunk ES with severity=High`
:::

:::notes
This worked example demonstrates how a fundamental SOC detection use case, identifying password brute-force attacks, is implemented in Splunk from raw data to production alert. Walking through this step by step builds the SPL intuition that is the core analytical skill developed in the Splunk Fundamentals course.

The starting point is Windows Security Event ID 4625, which is logged by the Windows Security event subsystem every time an interactive, network, or remote authentication attempt fails. The Event ID 4625 record includes the target user account name, the source IP address of the authentication attempt, the logon type (network, interactive, service, batch), and the failure reason (wrong password, account locked, account disabled). This makes it an extremely rich data source for detecting credential-based attacks.

The SPL pipeline begins with a broad search filtering to the relevant index and event code, scoped to the last 60 minutes. The `stats count as failure_count by src_ip, user` command groups events by the source IP address and targeted username, counting how many failed attempts each combination generated in the time window. The `where failure_count > 20` filter removes the background noise of legitimate occasional authentication failures (users mistyping their password) and retains only IP-username combinations that exceed a threshold consistent with automated attack tooling.

The threshold value (20 in this example) is a tuning parameter that must be calibrated to the organization's environment. Too low a threshold produces excessive false positives from users who repeatedly mistype their password; too high a threshold allows attackers to perform slow-and-low brute-force attacks that fly under the radar. A common production approach is to set separate thresholds for different logon types, a lower threshold (5-10) for interactive domain logons, and a higher threshold (50-100) for service-account authentications that may legitimately retry more frequently.

The `lookup` command in Step 4 demonstrates SIEM enrichment, joining the raw alert data with an asset inventory table to add business context (hostname, asset owner, department). This enrichment transforms a bare IP address into "Finance Department workstation owned by John Smith," which dramatically improves the analyst's ability to assess severity and route the alert to the right team. NIST SP 800-61 Rev. 2 guidance on incident analysis emphasizes that enrichment reducing analyst investigation time is one of the highest-leverage investments in SOC maturity.

The MITRE ATT&CK technique this detection covers is T1110 (Brute Force), sub-technique T1110.001 (Password Guessing) or T1110.003 (Password Spraying). Password spraying, attempting a single common password against many accounts, produces a different statistical pattern: many different target usernames from a single source IP, rather than many attempts against a single username. An enhanced version of this detection would add a separate branch: `| stats dc(user) as unique_users_targeted by src_ip | where unique_users_targeted > 10` to catch the spraying variant.

A fixed alerting threshold can be replaced by a baseline-aware one that compares the current window against a rolling 30-day average for that source and alerts when it exceeds roughly two standard deviations above the mean. This implements anomaly detection without a separate machine-learning engine.
:::

%%%

---
unit: Framework
code: ATK
title: MITRE ATT&CK and IDS/IPS Coverage
---

:::callout style=soft
The **MITRE ATT&CK framework** is a globally accessible knowledge base of adversary tactics, techniques, and procedures (TTPs) based on real-world observations. It provides a common taxonomy for mapping IDS/IPS detection rules to specific adversary behaviors, enabling organizations to identify and address coverage gaps.
:::

:::image src="images/14_mitre_attack.png" alt="Partial MITRE ATT&CK Enterprise matrix showing the 14 tactic columns (Reconnaissance through Impact) with selected technique cells highlighted in green to indicate where IDS/IPS detection rules provide coverage and left in grey to show uncovered techniques; a legend shows green equals covered by network IDS rule, blue equals covered by HIDS or endpoint rule, and grey equals no current detection coverage" caption="Mapping IDS rules to the ATT&CK matrix reveals coverage, green cells have detections, grey cells are blind spots that need new rules or additional tooling" width=full
:::

:::table
| ATT&CK Tactic | Example Technique | IDS/IPS Detection Approach |
|---|---|---|
| Reconnaissance | T1046, Network Service Scanning | NIDS: detect port scan patterns (SYN flood, sequential port sweep) |
| Initial Access | T1190, Exploit Public-Facing Application | NIDS: signature for known CVE exploits; WAF correlation |
| Execution | T1059.001, PowerShell | HIDS: Sysmon Event ID 4104 (script block logging); EDR behavioral rule |
| Persistence | T1078, Valid Accounts | SIEM: anomalous logon time/location for known-valid credentials |
| Defense Evasion | T1070.001, Clear Windows Event Logs | HIDS: Event ID 1102 (audit log cleared) |
| Command & Control | T1071.004, DNS C2 | Zeek dns.log: high-entropy subdomains, unusual query frequency |
| Exfiltration | T1048.003, Exfiltration over HTTPS | NIDS: large outbound uploads to uncommon destinations; DLP |
:::

:::notes
The MITRE ATT&CK Enterprise matrix, first published in 2015 and continuously updated based on threat intelligence from government, vendor, and academic researchers, has become the de facto standard taxonomy for discussing adversary behavior in the cybersecurity industry. MITRE defines 14 tactic categories representing the stages and objectives of an adversary campaign, and within each tactic, hundreds of specific techniques describing exactly how adversaries achieve those objectives. The framework is directly relevant to IDS/IPS and SIEM operations because it provides a structured way to answer the question: "For which adversary techniques do we currently have detection rules, and for which ones are we blind?"

The practice of mapping detection coverage against the ATT&CK matrix is called **ATT&CK navigator mapping** and is performed using MITRE's free ATT&CK Navigator tool. A security team exports their current detection rule inventory (Snort rules, Splunk saved searches, EDR rules) and maps each rule to the technique(s) it detects. The resulting heatmap, colored green for techniques with detection coverage and grey for uncovered techniques, immediately visualizes where the most dangerous blind spots exist, enabling prioritized investment in new detection content.

Several specific technique-to-detection mappings are particularly important for students to internalize. T1046 (Network Service Scanning) is one of the easiest techniques to detect at the network layer: port scans generate highly distinctive traffic patterns (rapid sequential SYN packets to many different destination ports, with no corresponding ACK from open ports) that NIDS rules based on Snort's stream5 preprocessor and scan detection module can identify with high fidelity and very low false positive rates. Conversely, T1059.001 (PowerShell execution) is essentially invisible to NIDS, it produces no distinctive network traffic signature, and requires HIDS coverage via Windows PowerShell Script Block Logging (Event ID 4104) or Sysmon Event ID 1 (process creation) to detect. This contrast illustrates concretely why a detection program needs both NIDS and HIDS coverage.

T1071.004 (Application Layer Protocol: DNS for C2) is a particularly instructive example because it demonstrates how behavioral detection through Zeek network metadata can catch what no signature rule would identify. The SUNBURST malware (CVE-2020-10148 et al.) used DNS for initial C2 communications, encoding stolen data in the subdomain labels of queries to attacker-controlled domains. The queries were individually indistinguishable from legitimate DNS lookups, they used valid DNS syntax, reasonable TTLs, and HTTPS-protected channels. Detection required observing that a single host was generating an anomalously high volume of DNS queries to a small number of newly-registered domains with unusually high label entropy scores. This is exactly the kind of behavioral pattern that Zeek's dns.log enables analysts to detect through retrospective threat hunting or proactive anomaly detection queries in the SIEM.

NIST SP 800-53 Rev. 5 Control SI-4 (System Monitoring) requires organizations to monitor information systems to detect attacks and indicators of potential attacks. Mapping monitoring controls to ATT&CK techniques is the operational implementation of this requirement, providing auditable evidence that monitoring coverage addresses known adversary techniques rather than being a generic "we have an IDS" statement.

Mapping a specific breach, such as the 2021 Kaseya VSA ransomware incident (CVE-2021-30116), onto the ATT&CK techniques the attackers used shows which techniques a given set of monitoring tools would have detected and which would have required additional capability.
:::

%%%

---
unit: Misconceptions
code: FAQ
title: Common Misconceptions About IDS/IPS
---

:::callout style=line
Detection and prevention systems are frequently misunderstood, both by practitioners who overestimate their coverage and by managers who dismiss them as legacy technology. This slide addresses the most common misconceptions encountered in real SOC environments.
:::

:::image src="images/14_misconceptions.png" alt="A myth-versus-reality comparison graphic with five rows; each row shows a speech-bubble labeled Myth on the left containing a common misconception about IDS/IPS, and a checkmark box labeled Reality on the right containing the corrected understanding; the overall design uses red for myth and green for reality" caption="Clearing up common IDS/IPS misconceptions prevents both false confidence and unnecessary dismissal of these tools" width=full
:::

:::table
| Misconception | Reality |
|---|---|
| "An IPS protects against all threats" | IPS only blocks known, signatured threats inline, zero-days and encrypted C2 traffic evade it |
| "If the IDS isn't alerting, we're safe" | An untuned or under-resourced IDS may generate alerts that are simply not reviewed, silence ≠ safety |
| "More alerts = better security" | Alert volume without quality increases fatigue and causes real threats to be missed |
| "IDS is obsolete in a cloud environment" | Cloud environments need equivalent monitoring via cloud-native IDS (AWS GuardDuty, Azure Defender) |
| "Encrypted traffic makes IDS useless" | SSL inspection proxies, JA3 fingerprinting, and HIDS provide visibility into encrypted sessions |
| "One IDS covers the whole network" | East-west (lateral) traffic between internal segments is invisible to a perimeter-only IDS |
:::

:::notes
Addressing misconceptions about IDS and IPS is as important as explaining how the technologies work, because incorrect mental models lead directly to security program failures. These six misconceptions represent patterns that security architects and SOC analysts encounter repeatedly in real-world enterprise environments.

**Misconception 1: "An IPS protects against all threats."** This fundamentally misunderstands the signature-dependent nature of IPS detection. An IPS can only block traffic that matches a configured rule. On the day a zero-day exploit is first used in the wild, no IPS signature exists for it. The IPS inspection engine examines every byte of the malicious traffic and allows it through because it matches no known pattern. Additionally, even for known threats, an IPS is ineffective against encrypted payloads without inline TLS decryption, a capability that introduces significant privacy, legal, and performance complexity. The MITRE ATT&CK framework lists "Impair Defenses" (T1562) as a distinct tactic, and disabling or evading IPS is a sub-technique specifically because sophisticated attackers know how to make their traffic IPS-invisible.

**Misconception 2: "If the IDS isn't alerting, we're safe."** This is the most dangerous misconception in the list because it leads to false confidence at exactly the moment when a real breach may be occurring. As discussed in the alert fatigue slide, an analyst team overwhelmed with false positives may stop reviewing alert queues. A well-maintained IDS whose alert queue is never checked provides exactly the same operational protection as no IDS at all. The 2014 Target breach reinforced this point: the FireEye appliance deployed by Target generated accurate alerts about malicious activity, and those alerts were reviewed by a managed security service provider, but the escalation path to Target's security team was not followed. The IDS "was alerting", but nobody acted on the alerts. NIST SP 800-61 Rev. 2 specifically addresses this failure mode in its discussion of detection and analysis processes, emphasizing that detection systems must be paired with documented response procedures and clear escalation paths.

**Misconception 3: "More alerts = better security."** Volume of alerts is not a measure of detection quality. A poorly tuned IDS generating 50,000 alerts per day where 49,990 are false positives provides worse operational security than a well-tuned system generating 100 alerts per day where 95 are true positives, because analyst attention is a finite resource. PCI DSS Requirement 6.3.3 mandates regular review and testing of security controls, this implicitly includes evaluating alert quality, not just alert quantity.

**Misconception 4: "IDS is obsolete in a cloud environment."** This misconception arises from the (correct) observation that traditional hardware-based network TAPs and inline IPS appliances cannot be deployed in IaaS cloud environments where the customer does not control the physical infrastructure. However, cloud-native equivalents provide the same functional capabilities: AWS GuardDuty analyzes VPC Flow Logs, DNS query logs, and CloudTrail API call records using machine learning and threat intelligence; Azure Defender for Cloud provides network traffic analysis and alert generation equivalent to a traditional NIDS for Azure Virtual Network traffic; Google Cloud Security Command Center performs similar functions. NIST SP 800-144 (Guidelines on Security and Privacy in Public Cloud Computing) and the CSA Cloud Controls Matrix both map traditional on-premises security controls to their cloud-native equivalents.

**Misconceptions 5 and 6** relate to encryption and coverage scope, which were discussed in detail in the NIDS vs HIDS slide. The key insight to reinforce here is that IDS/IPS is never a single-tool solution, it is an architecture of complementary controls that together eliminate each other's blind spots.

:::

%%%

---
unit: Checkpoint
code: CHK1
title: Mid-Lecture Checkpoint
---

:::callout style=line
Pause and review. Before moving into log formats and SIEM architecture, check your understanding of IDS, IPS, and detection fundamentals.
:::

:::image src="images/14_checkpoint.png" alt="Illustration of a traffic light with a yellow caution signal lit, surrounded by key terms from the first half of the lecture: IDS, IPS, NIDS, HIDS, SPAN, TAP, signature-based, anomaly-based, Snort, Suricata, Zeek, SIEM, alert fatigue, indicating a moment to pause and consolidate understanding before proceeding" caption="Check your understanding before proceeding, can you explain each concept without looking at your notes?" width=full
:::

:::list heading="Self-Check Questions" style=plain
- What is the key difference between an IDS and an IPS in terms of network placement?
- Why might a SPAN port miss packets that a network TAP would capture?
- Which type of IDS, NIDS or HIDS, can see the content of encrypted HTTPS traffic? Why?
- What is a signature and what type of attack does signature-based detection struggle to catch?
- Name one open-source IDS tool and one open-source IPS tool.
- Why does a high volume of alerts sometimes make a SOC less secure, not more?
- What does SIEM stand for, and what two functions, S and EM, does it combine?
:::

:::callout style=soft
**Group Discussion:** A network administrator tells you: "We have Snort running on all our SPAN ports and our SIEM is receiving the alerts. We're fully covered." What three specific gaps or risks would you identify in this statement?
:::

:::notes
Mid-lecture checkpoints serve a critical pedagogical function: they create a structured opportunity for students to consolidate learning before new material builds on top of it, and they give the instructor diagnostic signal about which concepts need reinforcement before proceeding. Research in cognitive science (Roediger and Karpicke, 2006, "The Power of Testing Memory") demonstrates that retrieval practice, the act of trying to recall information without looking at notes, substantially improves long-term retention compared to re-reading or passive review.

The seven self-check questions on this slide are calibrated to cover the most important conceptual distinctions from the first half of the lecture. Students who can answer all seven without referring to their notes have developed the core mental model of IDS/IPS architecture and are ready to integrate the log management and SIEM content. Students who struggle with specific questions reveal exactly which concepts need reinforcement.

Walking through expected answers: (1) IPS is inline in the data path; IDS is out-of-band on a mirrored copy. (2) SPAN ports deprioritize mirror traffic under switch load and can drop packets; hardware TAPs are passive and lossless. (3) HIDS, because HIDS operates on the endpoint where TLS decryption has already occurred at the application layer; NIDS sees only encrypted ciphertext on the wire. (4) A signature is a specific byte pattern or rule encoding a known attack; signature-based detection cannot catch zero-day attacks (attacks that have not been seen and documented before). (5) Snort or Suricata (IDS), Snort inline or Suricata in IPS mode, or Cisco Firepower. (6) Alert fatigue, analysts become desensitized to high alert volumes and miss real threats buried in the noise. (7) SIEM = Security Information and Event Management; S = Security Information (log management, storage, normalization) and EM = Event Management (correlation, alerting, incident workflows).

The group discussion question about the administrator's "fully covered" claim targets three specific gaps: First, SPAN ports may drop packets under load, "running on SPAN ports" is not the same as capturing 100% of traffic. Second, Snort catches only known signatures, zero-days, encrypted C2, and behavioral anomalies evade it; Zeek or UEBA would be needed for behavioral coverage. Third, "SIEM is receiving alerts" does not mean alerts are being reviewed and acted upon, the alert-to-investigation pipeline requires staffed analysts following documented response playbooks.

:::

%%%

---
unit: Case Study
code: CS1
title: Case Study, SolarWinds SUNBURST (2020)
---

:::callout style=line
The **SolarWinds SUNBURST** attack is widely considered the most sophisticated supply-chain intrusion ever publicly disclosed. Understanding what existing IDS/IPS and SIEM controls did and did not detect helps illustrate where the technologies covered in this class succeed and where they face fundamental limits.
:::

:::image src="images/14_solarwinds_case.png" alt="Timeline diagram of the SolarWinds SUNBURST attack from October 2019 to December 2020 with seven labeled milestones: (1) initial SolarWinds build system compromise, (2) test backdoor inserted into Orion updates, (3) trojanized SUNBURST DLL distributed in legitimate Orion update, (4) 14-day dormancy period before activation, (5) DGA-based DNS C2 communications begin, (6) hands-on-keyboard activity at selected high-value targets, (7) public disclosure by FireEye, each milestone annotated with what IDS/IPS or SIEM visibility would have been available at that stage" caption="SUNBURST exploited the trust in digitally-signed software updates, a vector that bypasses every network-layer control and requires supply-chain and behavioral monitoring to detect" width=full
:::

:::list heading="What Controls FAILED to Detect SUNBURST" style=plain
- Perimeter IPS: SUNBURST C2 used legitimate HTTPS to avcdn.net, blocked by no firewall rule
- Signature-based IDS: The malicious DLL was digitally signed by SolarWinds, no AV or IDS signature existed
- Log-based detection: SUNBURST disabled Windows Defender, deleted VSS snapshots, and scrubbed Orion logs
- Network NIDS: C2 traffic blended with legitimate SolarWinds telemetry traffic patterns
:::

:::list heading="What Controls DID Detect SUNBURST" style=plain
- FireEye's internal Red Team tool theft triggered the discovery (December 2020)
- Anomalous Orion process DNS queries with high-entropy subdomains (Zeek-based detection)
- Unusual SAML token lifetimes and off-hours Azure AD authentication (SIEM behavioral rule)
- Memory-resident implant detected by some next-gen AV (CrowdStrike, Microsoft Defender ATP)
:::

:::notes
The SolarWinds SUNBURST attack, publicly disclosed in December 2020 following FireEye's disclosure of its own Red Team tool theft, represents a landmark case study in the limits of conventional IDS/IPS and SIEM detection when facing a nation-state adversary with deep operational security discipline. The attackers, subsequently attributed with high confidence to Russia's SVR foreign intelligence service (known by the threat actor designations APT29 and Cozy Bear), demonstrated a sophisticated understanding of every detection control deployed at their targets and methodically engineered their intrusion to avoid triggering any of them.

The attack chain began with a compromise of SolarWinds' software build environment, believed to have occurred as early as October 2019. The attackers first inserted a test backdoor that did nothing malicious, it merely checked whether the build pipeline would distribute the modified binary and whether the digital signing process would produce a valid SolarWinds certificate on the trojanized DLL. When these tests confirmed that their modification survived the build process intact and was digitally signed by SolarWinds, they proceeded to insert the full SUNBURST backdoor code in February-March 2020. The trojanized Orion update was distributed to approximately 18,000 organizations worldwide via the legitimate SolarWinds software update channel, including the US Treasury Department, CISA, DHS, the Pentagon, and scores of Fortune 500 companies.

From a network security perspective, every conventional control was effectively bypassed. The trojanized Orion DLL was digitally signed with a valid SolarWinds code-signing certificate, no AV or IDS signature matched it because it had never been seen before. After a hard-coded 14-day dormancy period (designed to ensure the binary had been deployed widely before any C2 communications occurred, reducing the ability to correlate initial infection with C2 activation), SUNBURST began communicating via DNS to a domain-generation algorithm (DGA) generating subdomains under avoscloud.com. The DGA subdomains encoded the victim organization's domain name and a unique victim ID, enabling the C2 operator to selectively activate second-stage implants only at the highest-value targets. This DNS-based initial C2 produced no network traffic that any existing signature-based NIDS rule would match, the DNS queries were syntactically valid, properly formatted, and the resolving domain had a legitimate-looking registration history.

The controls that did provide detection signal, and why they worked, are equally instructive. Zeek-based network metadata analysis of DNS query logs could identify the SUNBURST DGA subdomains because they had unusually high Shannon entropy (randomness) scores compared to legitimate human-readable domain names. Several threat intelligence vendors developed Zeek scripts and SIEM queries implementing this entropy-based detection within days of public disclosure. Additionally, the SUNBURST threat actor's lateral movement into Microsoft 365 and Azure Active Directory environments created detectable anomalies in authentication logs: forged SAML tokens with unusually long validity periods (years rather than hours), authentication from service accounts at unusual times, and impersonation of privileged accounts that had never previously authenticated from those IP ranges. Microsoft Sentinel and Splunk both published free detection rule packages for these Azure AD-layer indicators within 72 hours of the FireEye disclosure.

The CVE-2020-10148 designation was assigned to the SolarWinds Orion API authentication bypass that enabled unauthenticated remote code execution on affected Orion deployments as a separate, related vulnerability. NIST SP 800-161 (Supply Chain Risk Management Practices for Federal Information Systems) had addressed supply-chain security requirements years before this breach, but implementation maturity across the affected organizations varied dramatically, illustrating the gap between policy requirements and operational reality.

Against SUNBURST, detection value varied by stage: reconnaissance gave almost no signal; delivery bypassed network controls; installation offered a possible early warning through file-integrity monitoring of the Orion binary directory; command and control gave the strongest technical opportunity through DNS entropy analysis; and lateral movement is where most real detections occurred, through behavioral analytics on cloud identity. The mapping shows both the power and the limits of each technology.
:::

%%%

---
unit: Case Study
code: CS2
title: Case Study, Target Breach (2013)
---

:::callout style=soft
The **2013 Target data breach**, which exposed 40 million payment card records and 70 million customer records, is the canonical case study for IDS/IPS alert pipeline failures. The tools worked. The process failed.
:::

:::image src="images/14_target_breach.png" alt="Attack chain diagram of the Target breach showing five stages: (1) spear-phishing email to Fazio Mechanical (HVAC vendor), (2) credential theft and use of Target vendor portal, (3) lateral movement from vendor network to POS network, (4) Citadel malware installed on POS terminals, (5) FireEye alert generated and not escalated; each stage is annotated with the detection opportunity that existed and whether it was acted upon" caption="Target's FireEye system correctly detected and alerted on the malware, the breach succeeded because the alert escalation process was not followed" width=full
:::

:::flow
1. Attacker spear-phishes Fazio Mechanical (Target HVAC vendor), steals credentials
2. Attacker uses vendor credentials to access Target's supplier portal (legitimate entry point)
3. Lateral movement from vendor network segment to internal POS network (network segmentation failure)
4. Citadel/BlackPOS malware deployed on 1,800+ POS terminals (memory scraping card data)
5. FireEye sandbox detects malware and generates HIGH-severity alert
6. Alert sent to Bangalore-based managed SOC, not escalated per process
7. Data exfiltrated to staging server in Eastern Europe over 19 days
:::

:::callout style=line
**Key Lesson:** Detection alone is insufficient. The alert-to-escalation pipeline requires documented processes, trained analysts, and tested runbooks to convert a detection into a response.
:::

:::notes
The 2013 Target data breach stands apart from other high-profile breaches because the security tooling worked exactly as intended, and the breach succeeded anyway. This makes it the most instructive case study available for understanding the human and process dimensions of security monitoring, and it is directly relevant to every technology discussed in this class.

The attack began in mid-November 2013 when attackers, believed to be part of an Eastern European cybercrime operation, used credentials stolen from Fazio Mechanical Services, an HVAC and refrigeration contractor that had network access to Target's systems for electronic billing and remote monitoring of building automation systems. Target's vendor portal access control architecture allowed Fazio's network access to reach beyond the intended HVAC management segment and into the internal network, a network segmentation failure that is itself a violation of PCI DSS Requirement 1.3 (which mandates restricting inbound and outbound traffic to only that which is necessary for the cardholder data environment). The MITRE ATT&CK technique T1078 (Valid Accounts) covers exactly this attack vector: using legitimately stolen credentials to gain initial access.

Once inside Target's network, the attackers performed lateral movement to identify and access the Point-of-Sale (POS) systems network. PCI DSS Requirement 1.2 requires that systems storing, processing, or transmitting cardholder data be isolated in a network segment with strict access controls, a requirement that was not effectively implemented in Target's architecture, as the vendor network had reachable paths to the POS segment. The attackers deployed a variant of the BlackPOS memory-scraping malware (also known as Kaptoxa) on approximately 1,800 POS terminals. The malware operated by hooking into the Windows POS application's memory space and scraping unencrypted Track 1 and Track 2 card data from the magnetic stripe at the moment the card was swiped, before encryption could occur, a technique that defeats point-to-point encryption (P2PE) if the encryption is applied after the swipe data enters host memory.

Target had deployed FireEye network security appliances, and FireEye's sandboxing technology correctly identified the BlackPOS malware communicating with its C2 server and generated a HIGH-severity alert on November 30, 2013, six days before the attack was publicly disclosed. FireEye also generated alerts identifying the malware's internal propagation across the POS network. These alerts were reviewed by analysts at Target's managed SOC in Bangalore, India. According to the US Senate Commerce Committee investigation report published in March 2014, the Bangalore team reviewed the alerts and had the technical capability to remotely quarantine the infected systems, but did not do so, and did not escalate the alerts to Target's US-based security team. The breach continued for 19 more days, with card data being exfiltrated in stages to staging servers within Target's network and then to servers in Eastern Europe.

The post-breach investigation revealed that Target had configured FireEye with its automatic blocking feature disabled. The decision to disable automatic blocking is not inherently wrong, many organizations choose to run IPS capabilities in detection-only mode to avoid the operational risk of false positive blocking, but it requires compensating controls: trained analysts with clear runbooks and escalation paths who will take manual action when the system generates high-severity alerts. Target had the detection; it lacked the response process.

NIST SP 800-61 Rev. 2 provides detailed guidance on the incident response process that was absent at Target: documented detection and analysis procedures, defined severity criteria for escalation, clear escalation contacts and timeframes, and regular exercises to validate that the process works as intended. The Target breach drove PCI DSS to strengthen its requirements: PCI DSS v3.1 (2015) added explicit requirements for security awareness training for personnel who monitor security systems, and PCI DSS v4.0 (2022) includes Requirement 12.10.7, which mandates that security monitoring tools generate alerts for at-risk accounts and that response procedures for those alerts are documented and tested.

The Target breach illustrates the OODA loop (Observe, Orient, Decide, Act) applied to a SOC. The monitoring tool observed the threat and the team partially oriented by rating it high severity, but decide and act failed: there were no documented escalation criteria and no one with authority was notified. Effective SOC processes require all four stages to function and be tested under realistic conditions.
:::

%%%

---
unit: Architecture
code: LOG2
title: Log Formats and Normalization
---

:::callout style=soft
Logs from different systems arrive in dozens of incompatible formats. Before a SIEM can correlate events across sources, it must **normalize** them into a common schema, mapping vendor-specific field names to standard names like `src_ip`, `dest_port`, and `event_action`. This normalization step is often the most time-consuming part of SIEM deployment.
:::

:::image src="images/14_log_normalization.png" alt="Diagram showing three raw log entries in different formats (syslog RFC 3164 from a Linux firewall, Windows EVTX XML from a domain controller, and CEF from a Palo Alto firewall) all flowing into a SIEM normalization layer; below the normalization layer, three identical normalized event records appear with standardized field names: timestamp, src_ip, dest_ip, dest_port, user, action, illustrating how different raw formats produce equivalent normalized records" caption="Normalization maps vendor-specific field names to a common schema, without it, a SIEM cannot correlate a firewall deny log with a Windows failed-logon event from the same source IP" width=full
:::

:::table
| Log Format | Used By | Key Characteristics |
|---|---|---|
| **Syslog (RFC 3164/5424)** | Network devices, Linux systems, firewalls | Text-based, facility/severity fields, plain key-value or unstructured |
| **Windows EVTX (XML)** | Windows endpoints and servers | XML-structured, Event IDs, Provider/Channel hierarchy |
| **CEF (Common Event Format)** | ArcSight-origin; many security tools | `CEF:0\|Vendor\|Product\|Version\|SignatureID\|Name\|Severity\|Extension` |
| **LEEF (Log Event Extended Format)** | IBM QRadar ecosystem | Tab-delimited key-value pairs |
| **JSON** | Cloud services, modern apps, APIs | Schema-flexible, natively parseable by most SIEM platforms |
| **NetFlow/IPFIX** | Cisco routers, flow collectors | Binary flow records: 5-tuple + bytes/packets/duration, no payload |
:::

:::notes
Log normalization is the unglamorous but essential engineering work that makes SIEM correlation possible. When a security analyst writes a Splunk SPL query that correlates firewall logs with Windows authentication logs, both datasets must use the same field name for "source IP address", but a Palo Alto firewall log calls it `src`, a Cisco ASA syslog calls it `source_address`, and a Windows Security Event Log calls it `IpAddress` in the event XML. Without normalization, these three field names cannot be joined in a single query, and cross-source correlation is impossible.

The normalization challenge is compounded by semantic differences beyond field naming. Timestamps are a particularly problematic area: different log sources may use different timezone assumptions (UTC vs. local time), different timestamp formats (Unix epoch, ISO 8601, RFC 3339, or vendor-specific strings), and different precision levels (seconds, milliseconds, microseconds). A SIEM that ingests logs without careful timestamp normalization will produce false correlations where events appear to occur in the wrong sequence, or fail to correlate events that actually occurred within the same time window. NIST SP 800-92 specifically recommends that organizations implement NTP (Network Time Protocol) synchronization across all log sources and document the expected timezone and precision of each source to enable accurate log correlation.

The Common Event Format (CEF) was developed by ArcSight (now part of Micro Focus) as a standardization attempt, a structured syslog extension that encodes a fixed set of key security event attributes in a defined header, followed by optional key-value extension fields. CEF achieved significant adoption in the commercial security appliance market; Palo Alto Networks, Check Point, and many other vendors support CEF output. However, CEF's extension field space allows vendor-specific additions that are not standardized, meaning CEF-format logs from two different vendors still require parsing customization in the SIEM.

The Elastic Common Schema (ECS) and Splunk's Common Information Model (CIM) represent the two most widely used normalization schemas in modern SIEM deployments. ECS defines standard field names and types for the Elastic Stack (Elasticsearch, Logstash, Kibana), while Splunk CIM provides the normalization framework for Splunk, defining standard field names like `src_ip`, `dest_ip`, `user`, `action`, `transport`, `app`, and `signature` that enable Splunk add-ons for different data sources to map their vendor-specific fields to the CIM before search time. A Splunk search using `datamodel=Network_Traffic` will automatically use CIM-normalized fields regardless of whether the underlying data came from a Cisco ASA, a Palo Alto firewall, a Juniper SRX, or an AWS VPC Flow Log, as long as each source's add-on correctly maps to the CIM. The Splunk Fundamentals course introduces CIM as a core concept precisely because it is what makes cross-source correlation practical at scale.

NetFlow and its successor IPFIX deserve special mention because they represent a fundamentally different class of log data: rather than recording application-layer events, NetFlow records aggregate statistics about network flows (a flow being defined by its 5-tuple: source IP, destination IP, source port, destination port, protocol). NetFlow data contains no payload content, it simply records that a connection happened, how long it lasted, and how many bytes were transferred in each direction. This makes NetFlow useful for detecting volumetric anomalies (DDoS attacks, bulk data transfers, port scans) and for generating network topology maps, but useless for payload-based signature detection. SIEM platforms typically ingest NetFlow as a complementary data source alongside packet-based IDS logs, not as a replacement for them.

Normalization maps logs from different sources into one schema. The same "failed SSH login" event arrives in syslog, Windows Event Log and cloud JSON formats, and a single normalized query (for example by source address and a failure action) finds all three. Without normalization each format would need its own query.
:::

%%%

---
unit: Framework
code: ZERO
title: Zero Trust and Continuous Monitoring
---

:::callout style=soft
**Zero Trust Architecture (ZTA)** is a security model that eliminates implicit trust in any network location and instead requires continuous verification of every access request. Zero Trust does not replace IDS/IPS and SIEM, it makes them more critical by demanding that monitoring be pervasive, not just perimeter-focused.
:::

:::image src="images/14_zero_trust_monitoring.png" alt="Zero Trust architecture diagram showing an employee laptop, a cloud application, and an on-premises server, each connected to a Policy Enforcement Point (PEP) that evaluates every access request against a Policy Decision Point (PDP); surrounding the architecture, monitoring feeds (IDS sensor, SIEM, EDR, identity logs, cloud audit logs) all flow into the PDP to inform continuous trust evaluation; the diagram explicitly shows no 'trusted internal network' zone, every segment requires verification" caption="In Zero Trust, monitoring is not an add-on, continuous telemetry from IDS, SIEM, and EDR is the mechanism by which trust decisions are made and updated in real time" width=full
:::

:::list heading="Zero Trust Principles (NIST SP 800-207)" style=plain
- All resources are accessed securely regardless of network location
- Access is granted on a per-session basis with least-privilege
- Access to resources is determined by dynamic policy (device health, user identity, request context)
- All asset and network activity is monitored and logged
- The enterprise collects as much information as possible about assets, network infrastructure, and communications, and uses it to improve security posture
:::

:::callout style=soft
**Key Insight:** Zero Trust's "always verify" principle is operationally implemented through continuous monitoring. The Policy Decision Point evaluates IDS/SIEM telemetry in real time to adjust access decisions, making detection infrastructure a direct input to access control, not a separate, after-the-fact review process.
:::

:::notes
The Zero Trust security model, formalized in NIST SP 800-207 (Zero Trust Architecture) published in August 2020, represents a fundamental shift in how enterprise security architecture is conceived. The traditional perimeter security model, implicit trust for anything inside the network, explicit distrust for everything outside, was already showing cracks by the mid-2010s as mobile devices, cloud services, and remote work eroded the definition of a meaningful perimeter. The SolarWinds breach, the Kaseya VSA attack, and dozens of other sophisticated intrusions that used trusted supply-chain or partner access to bypass perimeter controls provided the final arguments for why perimeter trust cannot serve as the foundation of a security architecture.

NIST SP 800-207 defines Zero Trust around three core tenets that directly drive monitoring requirements. First, all data sources and computing services are considered resources, there is no "trusted internal network" where devices or users receive implicit permission to communicate freely. This means that east-west (lateral) network traffic between internal systems requires the same monitoring attention as north-south (external) traffic, a requirement that dramatically expands the scope of IDS/IPS sensor deployment compared to traditional perimeter-only architectures. Second, all communication must be secured regardless of network location, enforcing encryption everywhere means that NIDS sensors using traditional payload inspection face an encryption challenge across the entire internal network, not just at the perimeter. Third, access to individual enterprise resources is granted on a per-session basis with dynamic policy evaluation.

This third tenet is where Zero Trust most directly transforms the role of monitoring infrastructure. In a ZTA, the Policy Decision Point (PDP), the component that evaluates access requests and grants or denies access based on policy, consumes real-time telemetry from monitoring systems as an input to its trust evaluation. If an endpoint's EDR system reports that the device has connected to a known-malicious IP address in the past hour, the PDP can automatically downgrade that device's trust level and require step-up authentication or restrict its access to sensitive resources. If the SIEM detects an anomalous authentication pattern from a user account, the PDP can trigger a re-authentication challenge before allowing access to crown-jewel data. This feedback loop between detection (IDS/SIEM) and enforcement (PDP/Policy Enforcement Point) is the mechanism by which ZTA operationalizes the "continuous verification" principle.

NIST SP 800-207 Section 3.3 explicitly lists "monitoring and measurement" as a core ZTA activity, stating that "the enterprise collects as much information as possible about the current state of assets, network infrastructure, and communications and uses it to improve its security posture." This positions SIEM not as an optional monitoring tool but as a foundational architectural component of ZTA, the system that aggregates the telemetry enabling dynamic trust evaluation. Executive Order 14028 (Improving the Nation's Cybersecurity, May 2021) mandated that US federal agencies move toward Zero Trust architectures and specifically required enhanced logging and monitoring as prerequisite capabilities.

From a practical SOC operations perspective, Zero Trust increases monitoring surface area substantially. Every access request, every authentication event, every API call, and every network connection must be logged and available for real-time analysis. This log volume increase requires corresponding investment in SIEM scalability and log ingestion capacity. Cloud-native SIEM platforms (Microsoft Sentinel, Google Chronicle) with elastic storage and query capacity are better suited to ZTA log volumes than traditional on-premises SIEM appliances with fixed storage tiers.

Zero Trust reframes monitoring from a detective control that notices bad things after they happen into an input to preventive controls that continuously informs access decisions. The same technologies take on a different role, which justifies the monitoring investment to business stakeholders who undervalue detection alone.
:::

%%%

---
unit: Operations
code: SOC
title: The SOC Analyst Workflow
---

:::callout style=soft
A **Security Operations Center (SOC) analyst** is the human at the end of the detection pipeline. Understanding the analyst's workflow, from alert intake through investigation, escalation, and closure, reveals how the technical tools covered in this class translate into operational security outcomes.
:::

:::image src="images/14_soc_workflow.png" alt="SOC analyst workflow diagram showing six stages in a circular loop: (1) Alert Queue Review, analyst opens the SIEM dashboard and reviews new alerts by severity; (2) Initial Triage, analyst categorizes alert as true positive, false positive, or benign true positive within target SLA (e.g., 15 minutes for high severity); (3) Investigation, analyst pivots across SIEM, EDR, and threat intelligence to build timeline; (4) Escalation or Closure, escalates confirmed incidents to Tier 2/IR team or closes with documentation; (5) Response Coordination, Tier 2 analyst or IR team performs containment and eradication; (6) Post-Incident Tuning, detection rules updated based on lessons learned; arrows connect each stage in sequence and a feedback arrow returns from stage 6 to stage 1" caption="SOC analyst work is a continuous loop from alert to investigation to response to tuning, each cycle improves the detection pipeline for the next" width=full
:::

:::table
| SOC Tier | Role | Primary Tools | Escalation Trigger |
|---|---|---|---|
| Tier 1 | Alert triage and initial investigation | SIEM dashboard, basic EDR query, threat intel lookup | Confirmed true positive or ambiguous high-severity alert |
| Tier 2 | Deep investigation and incident management | Full SIEM search, EDR forensics, memory analysis, network packet capture | Active compromise or containment required |
| Tier 3 | Threat hunting, forensics, tooling development | All tools + custom scripting, malware analysis sandbox | Novel TTP requiring capability development |
| IR Team | Containment, eradication, recovery | All tools + legal/communications coordination | Declared security incident |
:::

:::notes
The detection technologies covered throughout this class, IDS sensors, IPS enforcement, SIEM correlation, and log management infrastructure, exist to serve one operational purpose: enabling a human analyst to detect, investigate, and respond to security threats faster and more accurately than would be possible without them. Understanding the SOC analyst's day-to-day workflow is essential because it reveals which capabilities actually matter operationally and where tool investments deliver the most value.

A typical Tier 1 SOC analyst begins a shift by reviewing the alert queue in the SIEM dashboard. Alert queues are ordered by severity (critical, high, medium, low) and by age, with the oldest unreviewed high-severity alerts at the top. The analyst's primary SLA obligation is to review every critical and high-severity alert within a defined timeframe, commonly 15 minutes for critical, 1 hour for high, aligned with NIST SP 800-61 Rev. 2 recommendations for incident detection and reporting timelines. The analyst performs initial triage to categorize each alert as: a true positive (confirmed malicious activity requiring escalation), a false positive (benign activity incorrectly flagged, requires documentation and rule feedback), or a benign true positive (accurately detected but non-threatening activity, e.g., a legitimate security scan detected by the IDS that was pre-authorized).

For a true positive or an ambiguous high-severity alert, the analyst begins investigation. Investigation involves pivoting across multiple data sources using the SIEM as the central interface: starting from the initial alert, querying for other events from the same source IP over the past 24 hours, checking the IP against threat intelligence feeds (e.g., VirusTotal, Shodan, commercial TI platforms), examining the destination host's endpoint logs in the EDR console for unusual process activity, and building a timeline of related events. This pivot-based investigation workflow is exactly what the Splunk SPL skills developed in this course enable, the ability to move fluidly from an initial alert to a comprehensive picture of the attack in progress.

The OODA loop (Observe, Orient, Decide, Act) framework from military decision theory maps directly onto SOC analyst workflow: Observe (receive the alert), Orient (gather context and pivot across data sources), Decide (classify as true positive/false positive and determine appropriate response), Act (escalate, close, or block). The speed at which an analyst can execute this loop, measured as Mean Time to Detect (MTTD) and Mean Time to Respond (MTTR), directly determines breach impact. IBM's Cost of a Data Breach Report (2023) found that organizations with AI-assisted SIEM tools reduced their average breach lifecycle by 108 days compared to organizations without these tools, and that this lifecycle reduction corresponded to an average cost saving of $1.76 million per breach.

Escalation to Tier 2 occurs when the Tier 1 analyst confirms a true positive or encounters a complex alert beyond their investigation scope. Tier 2 analysts have deeper technical skills and access to additional investigation tools: full SIEM search capability, EDR forensic investigation (live memory analysis, process tree reconstruction, file hash searching), network packet capture replay, and threat intelligence enrichment. Tier 2 analysts are also responsible for incident management, documenting the incident timeline, coordinating with asset owners, and managing the containment and eradication process.

Tier 3 analysts (often called threat hunters or senior detection engineers) are responsible for proactive threat hunting, searching for evidence of advanced adversary activity that has not triggered any automated alert, and for building new detection capabilities in response to emerging threat intelligence. The distinction between Tier 1 (reactive alert response) and Tier 3 (proactive threat hunting) represents opposite ends of the detection spectrum: Tier 1 operates the existing detection pipeline, while Tier 3 extends it.

Alert triage is a pivot-based investigation: a high-severity "possible SQL injection" alert leads to examining the source address's other activity, the targeted server's logs, the request contents and whether the attempt succeeded. The order of those pivots is the analyst skill being developed.
:::

%%%

---
unit: Architecture
code: CLOUD
title: Cloud-Native IDS/IPS, AWS GuardDuty
---

:::callout style=soft
Traditional hardware-based IDS/IPS cannot be deployed in IaaS cloud environments where customers do not control the physical network. Cloud providers offer native threat detection services that provide equivalent (and in some ways superior) capabilities by analyzing cloud-native telemetry sources unavailable on-premises.
:::

:::image src="images/14_cloud_ids.png" alt="AWS GuardDuty architecture diagram showing three input data sources feeding into the GuardDuty analysis engine: VPC Flow Logs (network traffic metadata between EC2 instances), CloudTrail Logs (API calls to AWS services, including identity and access events), and Route 53 DNS Query Logs (DNS lookups made from within the VPC); the GuardDuty engine uses machine learning and threat intelligence to generate findings, which are displayed in the GuardDuty console and optionally forwarded to Amazon Security Hub or a SIEM via EventBridge" caption="AWS GuardDuty analyzes cloud-native telemetry, VPC Flow Logs, CloudTrail API events, and DNS queries, to detect threats that a hardware IDS could never observe in a cloud environment" width=full
:::

::::columns
::col::
:::list heading="AWS GuardDuty Data Sources" style=plain
- **VPC Flow Logs**: Network traffic metadata (5-tuple + bytes/duration) between VPC resources
- **CloudTrail Management Events**: All AWS API calls, resource creation, IAM changes, config modifications
- **CloudTrail S3 Data Events**: Object-level access to S3 buckets (reads, writes, deletes)
- **Route 53 DNS Query Logs**: DNS lookups made from EC2 instances
- **EKS Audit Logs**: Kubernetes API server audit events for container workloads
:::
::col::
:::list heading="Example GuardDuty Finding Types" style=plain
- `UnauthorizedAccess:EC2/SSHBruteForce`, SSH brute force against EC2 instance
- `Trojan:EC2/BlackholeTraffic`, EC2 communicating with known C2 blackhole IP
- `Recon:IAMUser/MaliciousIPCaller`, AWS API calls from known-malicious IP
- `Impact:S3/MaliciousIPCaller`, S3 data access from malicious IP
- `Persistence:IAMUser/AnomalousBehavior`, Unusual IAM credential usage patterns
:::
::::

:::notes
The migration of enterprise workloads to Amazon Web Services, Microsoft Azure, and Google Cloud Platform has created a detection coverage gap that traditional hardware-based IDS/IPS cannot address. In an on-premises data center, a security team controls the physical network fabric, can insert hardware TAPs at any chokepoint, and can deploy NIDS sensors with full visibility into all traffic. In an IaaS cloud environment, the customer controls virtual machines and virtual networks but has no access to the physical infrastructure beneath them, and the cloud provider's physical switching fabric, where a traditional TAP would sit, is inaccessible to customers.

Cloud providers have addressed this gap by building native threat detection services that analyze cloud-specific telemetry sources that have no on-premises equivalent. AWS GuardDuty, launched in 2017 and continuously expanded, analyzes three primary data categories. VPC Flow Logs provide the network-layer equivalent of NetFlow data: for every connection between VPC resources, GuardDuty receives the source IP, destination IP, port, protocol, bytes transferred, and connection outcome. AWS CloudTrail records every API call made to any AWS service, EC2 instance creation, IAM role modification, S3 bucket policy changes, KMS key usage, providing a comprehensive audit trail of control-plane activity that has no analogue in on-premises environments. Route 53 DNS query logs provide visibility into every DNS lookup made from within the VPC, enabling detection of DNS-based C2 communications similar to the Zeek dns.log analysis described in earlier slides.

GuardDuty's threat detection engine applies machine learning models and threat intelligence from AWS's global threat intelligence network to these data sources. Rather than matching signatures, GuardDuty builds behavioral baselines for each account and flags deviations: an EC2 instance that has never previously made API calls to AWS STS suddenly requesting AssumeRole credentials is anomalous; a user account that has only ever authenticated from us-east-1 suddenly accessing resources from ap-northeast-1 is anomalous. These behavioral anomalies map directly to MITRE ATT&CK techniques for cloud environments (the ATT&CK Cloud matrix), such as T1078.004 (Valid Accounts: Cloud Accounts) and T1530 (Data from Cloud Storage).

Comparing AWS GuardDuty to traditional on-premises IDS reveals both advantages and limitations. On the advantage side, GuardDuty has zero deployment complexity, it is enabled with a single API call per account, requires no agents or sensors, introduces no network latency, and scales automatically to any traffic volume. On the limitation side, GuardDuty does not perform deep packet inspection, like NetFlow, VPC Flow Logs contain only metadata, not payload. Application-layer attacks (SQL injection, XSS, SSRF) within HTTPS traffic are not detectable by GuardDuty; these require application-layer WAF services (AWS WAF) or host-based controls. Additionally, GuardDuty's detection coverage is limited to AWS-specific telemetry, it provides no visibility into on-premises or multi-cloud environments. For organizations operating across multiple cloud providers, a cloud-agnostic SIEM that ingests GuardDuty findings, Azure Defender alerts, and GCP Security Command Center findings into a unified analysis platform is required.

NIST SP 800-144 (Guidelines on Security and Privacy in Public Cloud Computing) recommends that organizations deploying workloads in cloud environments ensure equivalent monitoring controls to on-premises requirements, explicitly noting that this may require using cloud-native services where traditional controls cannot be deployed. AWS GuardDuty is the primary technical implementation of this NIST guidance for AWS environments.

In the 2019 Capital One breach, a server-side request forgery flaw was used to steal AWS credentials and exfiltrate data from S3, activity that would have produced GuardDuty findings, but GuardDuty was not enabled on the account. Cloud-native security tools, like all tools, provide value only when deployed and monitored.
:::

%%%

---
unit: Operations
code: TUNE
title: Tuning IDS Rules, Reducing False Positives
---

:::callout style=soft
An untuned IDS generates so many false positives that analysts cannot identify real threats. **Tuning** is the ongoing operational process of adjusting detection rules to maintain high true-positive rates while suppressing the benign activity that generates noise. It is never finished, the environment changes continuously.
:::

:::image src="images/14_ids_tuning.png" alt="Graph showing alert volume over time before and after IDS tuning: the pre-tuning period shows a high flat baseline of daily alerts (predominantly false positives) with true positive events invisible against the noise; the post-tuning period shows a dramatically lower baseline with true positive events clearly visible as spikes above the baseline; annotation arrows point to specific tuning actions that caused the baseline to drop: suppressing scanner alerts, whitelisting vulnerability scanner IPs, and raising thresholds for authentication failure alerts" width=full
:::

:::steps
1. Identify high-volume false positive alert categories (e.g., vulnerability scanner traffic triggering IDS signatures)
2. Add suppression rules or thresholds for known-benign sources (e.g., whitelist scanner IP 10.0.0.50)
3. Adjust signature sensitivity thresholds for environment-specific noise (e.g., raise SSH failure threshold from 5 to 20 for jump host traffic)
4. Add context-based filtering (only alert if destination is a production server, not a dev/test system)
5. Validate that tuning changes do not create blind spots using red team simulation or replay of historical attack PCAPs
6. Document all tuning changes with rationale and approval in a change management record
:::

:::callout style=line
**Tuning Anti-Pattern:** Suppressing an entire rule category because it is "too noisy" removes all detection for that attack class. The correct approach is surgical tuning, suppress specific false positive sources, not the detection capability.
:::

:::notes
IDS tuning is one of the most critical and most frequently neglected operational responsibilities in a SOC environment. A freshly deployed IDS running an off-the-shelf commercial or community rule set will typically generate enormous alert volumes in a new environment, because the rules are written for a generic network and have no knowledge of the specific infrastructure, applications, and traffic patterns present. Without tuning, the alert queue quickly becomes unusable, analysts cannot find true positives in the noise, and the IDS de facto ceases to provide operational security value despite functioning correctly from a technical standpoint.

The tuning process begins with alert triage at volume: reviewing the highest-frequency alert categories and determining which ones are consistently false positives in this specific environment. Common sources of high-frequency false positives include: authorized vulnerability scanners (which trigger signatures for port scan, service enumeration, and exploit attempt patterns when they scan internal systems); network monitoring systems that probe services periodically (Nagios, PRTG, and similar tools that trigger authentication-related signatures); backup agents that make high-volume file transfer connections (triggering data transfer anomaly rules); and developer workstations running local web servers that trigger HTTP-based signatures.

For each category, the tuning response depends on the underlying cause. If the false positives come from a known, authorized source IP (e.g., the vulnerability scanner at 10.0.0.50), the appropriate tuning action is to suppress alerts from that specific source IP in the relevant rule categories, not to disable the rule globally, which would create a blind spot for attacker traffic that happens to look like a vulnerability scan. If the false positives result from a threshold that is calibrated too low for the environment's baseline (e.g., an SSH authentication failure threshold of 5 that fires constantly on a busy jump host), the appropriate action is to raise the threshold to a level where only anomalous traffic exceeds it, while documenting the rationale for the threshold change.

NIST SP 800-94 Section 4.3.2 explicitly addresses IDS tuning, recommending that organizations maintain detailed documentation of all tuning decisions including the original false positive analysis, the suppression or threshold change applied, and the impact assessment confirming that the change did not reduce coverage for true malicious traffic. This documentation serves two purposes: it creates an audit trail for compliance purposes, and it prevents future analysts from re-introducing tuning that had already been evaluated and rejected.

The most dangerous tuning anti-pattern is category-level suppression: disabling an entire rule category (e.g., all web application attack rules) because it generates too many false positives. This is operationally equivalent to simply not having detection for that category of attack. The correct diagnosis in this scenario is that the rule category needs higher-specificity tuning, adding application-layer context filters that limit the rule to fire only when the target is a production web server in the DMZ, not when the same traffic pattern occurs on a developer's workstation. Modern NIDS platforms (Suricata, Snort 3) support rule metadata and filter constructs that enable this kind of context-aware suppression.

Validation is the critical final step in any tuning change. Before deploying a tuning modification to production, security teams should validate that the change does not create a coverage gap by replaying historical attack PCAPs (packet captures of real or simulated attacks) through the updated rule set and confirming that true positive alerts are still generated. Tools like PCAPreplay, tcpreplay, and vendor-provided attack simulation frameworks enable this validation. Some organizations with mature red team programs also schedule periodic adversary simulation exercises specifically to validate IDS detection coverage, deliberately launching known attack techniques from internal test systems and confirming that alerts are generated and routed correctly through the investigation pipeline.

Reducing alert volume without reducing security means tuning aggressively on high-volume, well-understood false positives while preserving rare, high-severity, hard-to-detect signals. This forces an explicit engagement with the false-positive versus false-negative trade-off.
:::

%%%

---
unit: Synthesis
code: IR
title: IDS/IPS/SIEM and Incident Response
---

:::callout style=soft
IDS, IPS, and SIEM are **detection tools**, but their value is ultimately realized through **incident response**. Understanding how detection outputs connect to the NIST Incident Response lifecycle ensures that alerts translate into action, not just log entries.
:::

:::image src="images/14_ir_connection.png" alt="NIST SP 800-61 Incident Response lifecycle diagram showing four phases in a cycle: Preparation → Detection and Analysis → Containment, Eradication, and Recovery → Post-Incident Activity → back to Preparation; IDS and SIEM tools are highlighted in the Detection and Analysis phase with arrows showing their outputs feeding directly into incident declaration; an arrow from Post-Incident Activity back to IDS/SIEM shows the tuning feedback loop; the diagram also shows escalation paths from SOC analyst to IR Team during the Containment phase" caption="IDS and SIEM outputs feed directly into the Detection and Analysis phase of the NIST IR lifecycle, detection without response is observation without consequence" width=full
:::

:::table
| NIST IR Phase | IDS/IPS/SIEM Contribution |
|---|---|
| **Preparation** | Tuning rules, building playbooks, defining escalation criteria, testing alert pipelines |
| **Detection & Analysis** | IDS alerts trigger SIEM correlation; analyst investigates and declares incident |
| **Containment** | IPS blocks attacker IP; SIEM query identifies all affected hosts for isolation |
| **Eradication** | HIDS file integrity logs identify malicious files; SIEM timeline supports malware scope |
| **Recovery** | SIEM monitors recovery period for re-infection indicators |
| **Post-Incident Activity** | Alert tuning based on missed detections; new rules for novel TTPs observed |
:::

:::notes
The connection between IDS/IPS/SIEM detection capabilities and the formal Incident Response (IR) process is not automatic, it requires deliberate design of the escalation path, response playbooks, and feedback mechanisms that transform a detection alert into a managed security incident. NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide) is the primary reference framework for this design, providing a four-phase lifecycle that explicitly depends on detection infrastructure at its core.

**Preparation** is the phase where the groundwork for effective detection and response is laid. From the IDS/SIEM perspective, preparation includes deploying and tuning detection rules, building investigation playbooks for the most common alert types, defining severity thresholds that determine which alerts require immediate escalation versus which can be queued for next-business-day review, testing alert delivery pipelines to ensure alerts reliably reach the analyst queue, and conducting tabletop exercises where analysts work through hypothetical incident scenarios. NIST SP 800-61 Rev. 2 Section 3.1 provides a comprehensive checklist of preparation activities, and organizations that invest in preparation see measurably lower MTTD and MTTR, the key operational metrics for detection program effectiveness.

**Detection and Analysis** is where IDS and SIEM tools play their primary role. An IDS alert arrives in the SIEM, the SIEM correlates it with related events across data sources, and an analyst performs initial triage and investigation as described in the SOC Analyst Workflow slide. The critical output of this phase is an **incident declaration**, the formal determination that a security incident is occurring and that the IR team should be engaged. The determination criteria (what distinguishes an incident from a security event that requires investigation but not escalation) must be documented in the organization's incident classification policy, often aligned to severity tiers based on the affected system's criticality, the confidence level of the detection, and the potential business impact.

**Containment** represents the first response action and is where IPS capabilities directly contribute. If the attacker's traffic is being actively observed in the IPS sensor, the responding analyst can push a block rule to the IPS to terminate the connection in real time. More commonly, containment involves network isolation of affected hosts (removing them from the network segment), revoking compromised credentials, and identifying and quarantining all hosts that communicated with the attacker's infrastructure using SIEM queries ("show me all internal hosts that connected to IP 203.0.113.45 in the past 30 days"). This pivot query, using the initial incident's attacker IP as a search pivot across the entire environment, is one of the highest-value SIEM capabilities during containment.

**Eradication and Recovery** leverage HIDS and SIEM forensic data to identify all malicious artifacts (files, registry keys, scheduled tasks, backdoor accounts) for removal, and to scope the attack's impact across the affected environment. The SIEM timeline constructed during investigation provides the chronological sequence of attacker activity, enabling eradication teams to ensure they have removed all persistence mechanisms, not just the initially discovered ones. During recovery, the SIEM continues monitoring the recovered systems for re-infection indicators, returning alerts from the same attacker TTPs would indicate incomplete eradication.

**Post-Incident Activity** closes the feedback loop. NIST SP 800-61 Rev. 2 Section 3.4 mandates post-incident reviews (also called after-action reviews or lessons-learned sessions) for all significant incidents. From the IDS/SIEM perspective, post-incident review should explicitly address: which detection controls caught the incident and how quickly; which techniques the attacker used that were not detected by existing rules (creating new rule development priorities); whether alert routing and escalation functioned as designed; and what tuning changes would reduce similar false positives in the future. This post-incident analysis feeding back into detection rule updates is the mechanism by which a security monitoring program continuously improves, each incident makes the detection pipeline better for the next one.

A breach in which the attacker was active for 47 days before detection points to a failure in the Detect function of the NIST incident response lifecycle, and the remedy, better monitoring coverage, tuned alerting and tested escalation, integrates IDS architecture, SIEM tuning and analyst workflow.
:::

%%%

---
unit: Summary
code: RECAP
title: Class 14 Recap, Key Concepts
---

:::callout style=soft
Before moving to hands-on Splunk labs, review the core concepts from this class. IDS, IPS, logs, and SIEM are interconnected layers, each has a specific role, and each has limitations that the others compensate for.
:::

:::image src="images/14_class_recap.png" alt="Summary mind map with 'Class 14: IDS, IPS and Monitoring' at the center and six branches radiating outward: (1) IDS, passive, out-of-band, alerts only; (2) IPS, inline, active, blocks traffic; (3) Detection Methods, signature vs anomaly vs behavioral; (4) Logs, raw material, normalization, formats; (5) SIEM, aggregation, correlation, alerting; (6) Operations, alert fatigue, tuning, SOC workflow, IR; each branch shows 2-3 key sub-points as leaf nodes" caption="Every concept in this class connects, IDS generates alerts that SIEM correlates, logs are the shared medium, and SOC analysts and IR teams make it all operational" width=full
:::

::::columns
::col::
:::list heading="Technical Foundations" style=plain
- IDS = passive observer; IPS = inline enforcer
- NIDS covers the network; HIDS covers the host
- TAPs are lossless; SPAN ports can drop packets
- Signatures catch known threats; anomaly detection catches novel ones
- Snort, Suricata, Zeek are the leading open-source tools
:::
::col::
:::list heading="SIEM and Operations" style=plain
- SIEM aggregates, normalizes, and correlates logs from all sources
- Log normalization (CIM/ECS) is what makes cross-source queries possible
- Alert fatigue reduces SOC effectiveness, quality beats quantity
- IDS/SIEM feeds directly into the NIST IR lifecycle
- Tuning is continuous, rules must evolve with the environment
:::
::col::
:::list heading="Real-World Context" style=plain
- NIST SP 800-94: IDS/IPS guidance
- NIST SP 800-92: Log management guidance
- NIST SP 800-61: Incident response
- MITRE ATT&CK: Maps techniques to detection rules
- SolarWinds and Target breaches: What detection success and failure look like
:::
::::

:::notes
This recap slide serves as the conceptual anchor for everything covered in Class 14, synthesizing the technical, operational, and contextual threads into a coherent mental model before students transition to hands-on Splunk laboratory exercises.

The most important structural insight to reinforce is that IDS, IPS, logs, and SIEM are not independent tools, they are layers of a single detection architecture, each dependent on the others. An IDS without a SIEM to aggregate its alerts produces a log file that nobody reviews. A SIEM without well-tuned IDS inputs generates low-quality correlation results. Logs without normalization prevent cross-source correlation. Alerts without a trained SOC analyst following documented playbooks produce no security outcomes. The system works only when all layers function together, which is exactly what NIST SP 800-94 Section 3 describes as a "network security monitoring architecture", an integrated set of sensors, aggregators, analysis tools, and human processes operating in coordination.

The NIST framework references threaded throughout this class, SP 800-94 for IDS/IPS, SP 800-92 for log management, SP 800-61 for incident response, SP 800-207 for Zero Trust, are not arbitrary citations. They represent the authoritative guidance documents that security practitioners are expected to know when designing, deploying, and operating monitoring infrastructure. These documents are freely available from the NIST Computer Security Resource Center (csrc.nist.gov) and are directly referenced in compliance frameworks (PCI DSS, HIPAA, FedRAMP) that students may encounter in professional practice.

The MITRE ATT&CK framework reference connects the detection tools covered in this class to the adversary behaviors they are designed to detect. Students who internalize the habit of asking "which ATT&CK technique does this detection rule cover?" will build detection programs with systematic coverage rather than ad-hoc rule sets that leave predictable blind spots.

The two case studies, SolarWinds SUNBURST and the Target breach, represent opposite failure modes. SolarWinds demonstrated what happens when adversaries engineer their attack specifically to evade all signature-based and perimeter-focused controls, requiring behavioral and supply-chain monitoring capabilities that were not universally deployed. Target demonstrated what happens when detection works correctly but the human response process is broken, a cautionary reminder that technology alone cannot substitute for trained analysts, documented playbooks, and tested escalation procedures.

Looking ahead to the Splunk Fundamentals labs: the SPL skills developed in those sessions are the practical implementation of the detection and investigation concepts covered today. Every Splunk search that students write, filtering to specific Event IDs, aggregating by source IP, building detection rules, is directly applying the IDS alert triage, SIEM correlation, and incident investigation workflows described in this class. The abstract concepts become operational skills in the lab environment, and both are necessary for professional competency.

A monitoring program built with a budget for two tools and two people has no single correct composition: the right choice depends on the threat model, the environment (on-premises or cloud) and the team's existing skills. Reasoning through those trade-offs is the objective.
:::
