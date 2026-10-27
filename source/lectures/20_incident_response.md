---
deck:
  title: Incident Response
  kicker: Class 20
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 20
  description: The formal process for what happens after a breach is confirmed, contain, eradicate, recover, communicate.
  topics: [Detection, Containment, Eradication, Recovery, Communication]
---

%%%
---
title: Incident Response
cover: true
---
:::text class=sub
Structured Incident Handling, Containment Strategies, and NIST SP 800-61 Rev. 2 Standards
:::

:::image src="images/20_incident_response_overview.png" alt="Overview diagram of the four NIST SP 800-61 incident response phases arranged in a clockwise cycle: Preparation, Detection and Analysis, Containment Eradication and Recovery, and Post-Incident Activity, connected by arrows" caption="The NIST SP 800-61 Rev. 2 incident response lifecycle: a continuous, self-improving cycle that converts each incident into stronger organizational defenses." width=full
:::

:::list style=chips
- CSIRT Team Composition & Roles
- NIST SP 800-61 Rev. 2 Lifecycle
- Containment, Eradication & Recovery Mechanics
- Post-Incident Activity & Lessons Learned
:::

:::notes
Welcome to Class 20, "Incident Response." In our previous lectures, we covered system security from initial hardening and access control to the detection of host-level attacks. We learned how to identify indicators of compromise. Today, we will explore the formal processes organizations follow when a security breach is confirmed.

An effective security architecture recognizes that compromise is always possible. When an incident occurs, the difference between minor containment and a catastrophic data breach often depends on the organization's preparation. We will analyze incident handling using the industry standard, NIST Special Publication 800-61 Rev. 2 (Computer Security Incident Handling Guide). We will study the composition of the Computer Security Incident Response Team (CSIRT), walk through the four phases of the incident lifecycle, and examine containment strategies. By the end of this lecture, you will understand how to design and execute a structured incident response plan. Let's begin by defining what constitutes a security incident.

The publication NIST SP 800-61 Rev. 2 was released in August 2012 and remains the authoritative industry reference for structured incident response. Organizations that fail to prepare formal incident response capabilities face significantly higher breach costs: the IBM Cost of a Data Breach Report 2023 found that organizations with a tested incident response team and plan saved an average of $1.49 million compared to those without one. This financial impact underscores the strategic importance of the material covered in this class. Notable incidents that demonstrate the cost of poor incident response include the 2017 Equifax breach, where delayed detection and slow containment resulted in the exposure of 147 million consumer records and over $1.4 billion in total costs, and the 2021 Colonial Pipeline ransomware attack, where inadequate preparation for operational technology (OT) systems led to a six-day shutdown of critical fuel infrastructure across the U.S. East Coast.
:::

%%%
---
unit: Foundations
code: INC
title: What Is an Incident?
---
:::callout style=soft
An **incident** is defined by NIST SP 800-61 Rev. 2 as a violation or imminent threat of violation of computer security policies, acceptable use policies, or standard security practices.
:::

:::image src="images/20_csirt_team_structure.png" alt="Organizational chart showing CSIRT team roles radiating from a central Incident Manager node, with Security Analysts, Legal Counsel, and Public Relations as labeled branches, each showing their primary responsibilities" caption="CSIRT team structure: a cross-functional group that combines technical analysis, legal oversight, and communications to manage incidents from detection through resolution." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="The CSIRT Team"
:::list style=plain
- **Incident Manager:** Directs the response effort and coordinates communication.
- **Security Analysts:** Analyze logs, perform memory forensics, and contain systems.
- **Legal Counsel:** Advises on disclosure requirements and regulatory compliance.
- **Public Relations:** Manages communications with customers and the media.
:::
::::
::col::
::::card heading="Incident vs. Event"
:::list style=plain
- **Event:** Any observable occurrence in a system or network (e.g., a user logging in, a firewall blocking a packet).
- **Incident:** An adverse event that negatively impacts the confidentiality, integrity, or availability of systems or data.
:::
::::
::::

:::steps
1. **Observe:** A security tool (SIEM, EDR, IDS) logs an event that exceeds a detection threshold.
2. **Evaluate:** A SOC analyst reviews the event against policy definitions and available threat intelligence.
3. **Classify:** Determine whether the event meets the NIST definition of an incident, adverse impact to CIA.
4. **Prioritize:** Assign a severity level (P1 Critical through P4 Low) based on affected data and systems.
5. **Activate:** Notify the CSIRT and initiate the formal incident response lifecycle.
:::

:::notes
To manage security operations, we must distinguish between standard system events and security incidents. A system event is any observable occurrence within a network or host. Modern networks generate millions of events daily, such as a user connecting to a file share or a server rebooting. Most of these events are benign.

An incident is an adverse event that threatens the confidentiality, integrity, or availability of an information system. For example, a single failed login attempt is a standard event. However, ten thousand failed login attempts from a single IP address within one minute is an adverse event that indicates a brute-force attack. When an incident is confirmed, the Computer Security Incident Response Team (CSIRT) is activated. The CSIRT is a cross-functional group that includes technical security analysts, legal counsel, and public relations staff. This team works together to contain the threat and limit organizational liability.

The distinction between events and incidents is formalized across multiple standards. ISO/IEC 27035-1:2023 (Information Security Incident Management) defines an information security incident as "one or multiple related and identified information security events that can harm an organization's assets or compromise its operations." In practice, incident classification often follows a severity matrix. A P1 (Critical) incident might involve active data exfiltration of customer records, triggering immediate executive notification and regulatory reporting timelines under GDPR (72-hour breach notification) or HIPAA (60-day breach notification). A P4 (Low) incident might be an isolated phishing email that was blocked before payload delivery. The CSIRT structure described here reflects guidance in NIST SP 800-61 Rev. 2, which emphasizes that effective incident response requires cross-functional collaboration. The 2013 Target breach provides a sobering example: the security operations team received FireEye alerts indicating an active compromise but did not escalate them through the proper CSIRT chain, delaying containment and enabling the extraction of forty million card records.
:::

%%%
---
unit: Lifecycle
code: LFC
title: The Incident Response Lifecycle
---
:::callout style=soft
NIST SP 800-61 Rev. 2 organizes the incident handling process into a **four-phase cyclical lifecycle**, ensuring continuous feedback and security improvement.
:::

:::image src="images/20_nist_lifecycle.png" alt="Clean circular flow diagram with four labeled segments, Preparation, Detection and Analysis, Containment Eradication and Recovery, Post-Incident Activity, connected by arrows forming a complete cycle, with a feedback arrow from Post-Incident back to Preparation" caption="The NIST SP 800-61 Rev. 2 cyclical lifecycle: each completed incident feeds lessons back into preparation, closing security gaps before the next event." width=full
:::

:::code language=mermaid caption="NIST SP 800-61 Rev. 2 Incident Response Lifecycle"
graph LR
    Prep[1. Preparation] --> Det[2. Detection & Analysis]
    Det --> Cont[3. Containment, Eradication & Recovery]
    Cont --> Post[4. Post-Incident Activity]
    Post --> Prep
    Det -->|Continuous Feedback| Prep
:::

:::notes
NIST SP 800-61 Rev. 2 defines a structured, four-phase lifecycle for incident response. Rather than a linear process, the lifecycle is cyclical. Feedback from active security incidents is used to update defensive configurations and response plans, preparing the organization for future threats.

The four phases are: 1. Preparation; 2. Detection and Analysis; 3. Containment, Eradication, and Recovery; and 4. Post-Incident Activity. The lifecycle's structure emphasizes that security operations must be ongoing. For example, the lessons learned during the post-incident phase are used to update employee training and firewall configurations. This feedback loop is essential for maintaining resilience as attacker techniques evolve.

The four-phase cyclical structure of NIST SP 800-61 Rev. 2 reflects a fundamental principle of security operations: incidents are not isolated events but opportunities for systematic improvement. This approach mirrors the Plan-Do-Check-Act (PDCA) cycle used in ISO/IEC 27001:2022 (Information Security Management Systems). The feedback loop between Post-Incident Activity and Preparation is particularly critical. For example, during the 2014 Sony Pictures breach, attackers exfiltrated terabytes of data over weeks without detection. A post-incident analysis revealed significant gaps in network monitoring and data loss prevention (DLP) controls. Had a lessons-learned feedback loop been in place from prior incidents, these gaps might have been identified and closed earlier. The cyclical nature also means that the lifecycle never truly ends: new threat intelligence gathered during post-incident analysis feeds directly into updated detection signatures and refined incident response procedures, improving organizational resilience over time. ISO/IEC 27035-2:2023 provides additional guidance on planning and preparing for incident response capabilities within this lifecycle model.
:::

%%%
---
unit: Lifecycle
code: PRE
title: "Phase 1: Preparation"
---
:::callout style=soft
**Preparation** involves establishing the policies, tools, and communication channels required to respond to incidents before they occur.
:::

:::image src="images/20_preparation_phase.png" alt="Split diagram showing the two preparation pillars: Policy and Infrastructure on the left (IRP document, communication channels, jump kit) and Resilience Testing on the right (tabletop exercise participants around a table, red team adversary icon, backup storage cylinder)" caption="Phase 1, Preparation: organizational readiness is built before incidents occur through documented plans, pre-staged tools, and regular testing exercises." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Policy & Infrastructure"
:::list style=plain
- **Incident Response Plan (IRP):** Written procedures defining roles, severity levels, and escalation paths.
- **Out-of-Band Communication:** Secure backup communication channels (e.g., encrypted messaging, satellite phones) for use if the primary network is compromised.
- **Jump Kits:** Pre-configured laptops loaded with forensic tools (e.g., FTK Imager, Wireshark, Volatility) and network cables.
:::
::::
::col::
::::card heading="Resilience Testing"
:::list style=plain
- **Tabletop Exercises:** Simulation workshops where stakeholders walk through hypothetical incident scenarios.
- **Red Teaming:** Active, adversary-simulation exercises designed to test detection and response capabilities.
- **Immutable Backups:** Implementing isolated, offline backups to ensure recovery options.
:::
::::
::::

:::steps
1. **Develop IRP:** Document roles, severity definitions, escalation paths, and regulatory notification timelines in a written Incident Response Plan.
2. **Assemble Jump Kits:** Pre-configure forensic laptops with FTK Imager, Wireshark, Volatility, write-blockers, and spare network hardware.
3. **Establish Backup Infrastructure:** Deploy immutable, air-gapped backups and conduct quarterly restoration tests to verify integrity.
4. **Configure Out-of-Band Channels:** Set up encrypted secondary communication (separate from corporate infrastructure) for use when the primary network may be monitored by an attacker.
5. **Conduct Training:** Execute tabletop exercises and red team engagements annually to test and refine response readiness.
:::

:::notes
The preparation phase is the foundation of incident response. It is during this phase that organizations build the capabilities needed to handle incidents. Without preparation, response efforts can become uncoordinated, leading to errors that delay containment or destroy evidence.

Key preparation activities include developing an Incident Response Plan (IRP), establishing communication channels, and assembling analyst "jump kits." Jump kits contain pre-configured laptops with forensic tools, write-blockers, and network taps, allowing analysts to acquire evidence without modifying the source media. Additionally, organizations run tabletop exercises. These exercises bring stakeholders together to discuss how they would handle simulated incidents, helping identify gaps in communication before a real breach occurs.

NIST SP 800-61 Rev. 2 provides a detailed preparation checklist that extends beyond the items covered on this slide. Communication is particularly critical: during a major incident, an attacker who has compromised the primary network may also be monitoring internal email and messaging systems. This is why out-of-band communication, using cellular networks, encrypted messaging apps on non-corporate devices, or dedicated incident response phones, is essential. The jump kit concept is formalized in guidance from the SANS Institute, which recommends including hardware write-blockers to prevent accidental modification of evidence during forensic acquisition. Tabletop exercises, as defined in NIST SP 800-84 (Guide to Test, Training, and Exercise Programs for IT Plans), should simulate realistic scenarios relevant to the organization's threat profile. The 2021 Colonial Pipeline ransomware attack revealed that the company did not have a tested IRP for operational technology (OT) systems, contributing to the six-day shutdown. ISO/IEC 27035-2:2023 further specifies that preparation should include establishing relationships with external resources such as law enforcement (e.g., FBI Cyber Division) and incident response service providers before an incident occurs.
:::

%%%
---
unit: Lifecycle
code: DET
title: "Phase 2: Detection & Analysis"
---
:::callout style=soft
**Detection and Analysis** focuses on identifying security incidents, validating alerts, and determining the scope and impact of the compromise.
:::

:::image src="images/20_detection_analysis_phase.png" alt="Flowchart showing the detection and analysis process: SIEM and EDR alerts feed into a triage funnel, valid incidents progress through scoping and correlation, and emerge as a severity-classified incident with a documented attacker timeline" caption="Phase 2, Detection and Analysis: raw alerts are filtered, validated, and enriched into a scoped incident with a confirmed attacker timeline before escalation." width=full
:::

:::steps
1. **Alert Triage:** Reviewing alerts from security tools (SIEM, EDR) to filter out false positives.
2. **Scoping & Documentation:** Determining which hosts, accounts, and data repositories are affected.
3. **Correlation:** Analyzing network traffic logs, system events, and memory captures to reconstruct the attacker's timeline.
4. **Prioritization:** Assigning a severity level based on the business impact and the sensitivity of the affected data.
5. **Notification:** Escalating the incident to appropriate stakeholders based on communication protocols.
:::

:::notes
Detection and Analysis is often the most challenging phase of the incident response lifecycle. Modern security teams receive thousands of alerts daily, many of which are false positives. The first step is triage, where analysts evaluate alerts to confirm whether an incident has occurred.

Once an incident is validated, the team must determine its scope. This scoping involves analyzing logs and memory captures to identify affected systems and accounts. The team constructs a timeline to track the attacker's lateral movement through the network. Based on this analysis, the incident is assigned a severity level. This severity determines the escalation path, indicating when executive leadership, legal counsel, and public relations should be notified. Accurate scoping is essential for preventing incomplete containment, which can leave active threats in the network.

The detection and analysis phase is where the endpoint telemetry discussed in Class 19 is operationalized within the incident response framework. NIST SP 800-61 Rev. 2 identifies several key detection sources: SIEM systems correlating logs from multiple sources; network-based intrusion detection systems (IDSes) detecting anomalous traffic patterns; and endpoint detection and response (EDR) tools identifying malicious process behaviors. The Equifax 2017 breach is an illustrative example of failed detection and analysis: the attackers exploited CVE-2017-5638 (Apache Struts remote code execution) and were present in the network for 78 days before detection, largely because an expired TLS certificate prevented HTTPS traffic inspection by the network IDS. Severity prioritization during triage should be guided by the value of affected data and systems. NIST SP 800-61 Rev. 2 recommends assigning functional impact (e.g., none, minimal, significant) and information impact (e.g., suspected unauthorized disclosure, confirmed data breach) to guide escalation decisions. MITRE ATT&CK's Initial Access (TA0001) and Discovery (TA0007) tactics are typically the focus of timeline reconstruction during this phase.
:::

%%%
---
unit: Lifecycle
code: CON
title: "Phase 3a: Containment Strategies"
---
:::callout style=soft
**Containment** seeks to limit the impact of an incident by preventing lateral movement, data exfiltration, or further resource damage while security teams formulate a permanent fix.
:::

:::image src="images/20_containment_strategies.png" alt="Network topology diagram showing a compromised host being isolated: firewall rules block outbound connections, switch port configuration cuts LAN access, and a traffic redirection arrow points the attacker's traffic toward a honeypot node" caption="Phase 3a, Containment: a compromised host is quarantined from the network while attacker activity is optionally redirected to a honeypot for continued intelligence collection." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Containment Methods"
:::list style=plain
- **Network Isolation:** Modifying switch port configurations or firewall rules to isolate compromised hosts from the network.
- **Credential Revocation:** Disabling compromised user accounts and administrative keys.
- **Traffic Redirection:** Routing attacker traffic to a sandbox or honeypot to monitor their activities.
:::
::::
::col::
::::card heading="Decision-Making Metrics"
:::list style=plain
- **Operational Impact:** Assessing the business cost of shutting down affected services.
- **Evidence Preservation:** Selecting containment methods that preserve system memory for analysis.
- **Feasibility:** Evaluating the time and resources required to implement the containment strategy.
:::
::::
::::

:::steps
1. **Assess Scope:** Confirm all affected hosts and accounts based on the Detection and Analysis findings.
2. **Preserve Evidence:** Capture a volatile memory (RAM) image from affected systems before implementing any network changes.
3. **Select Strategy:** Choose an isolation method that balances the security need against business impact.
4. **Implement Isolation:** Modify firewall ACLs or switch port configurations to quarantine compromised hosts.
5. **Revoke Credentials:** Disable all compromised user accounts, API keys, and service account tokens.
6. **Verify Containment:** Confirm via network traffic analysis that no further lateral movement is occurring.
:::

:::notes
Containment is the first operational phase after an incident is confirmed. Its objective is to limit damage and prevent the attacker from moving laterally to other systems. Containment is often a dynamic process, requiring security teams to make critical decisions under time pressure.

Security teams select containment strategies based on the nature of the attack. Network isolation is a common approach, where switch port configurations or firewall rules are modified to isolate compromised hosts. For credential-based attacks, the team focuses on disabling compromised accounts and keys.

Choosing a containment strategy requires balancing security needs against business operations. For example, isolating a critical server can disrupt customer operations, causing financial loss. However, leaving it connected risks further lateral movement. The team must evaluate these metrics, selecting containment methods that stop the threat while preserving volatile memory for forensic analysis.

NIST SP 800-61 Rev. 2 identifies two categories of containment: short-term and long-term. Short-term containment involves immediate actions to limit damage, such as disconnecting affected hosts from the network. Long-term containment involves more durable changes, such as deploying additional monitoring controls and hardening adjacent systems while eradication is prepared. The decision to isolate versus monitor an attacker is sometimes deliberate: redirecting attacker traffic to a honeypot allows the CSIRT to observe the attacker's lateral movement techniques, collecting valuable intelligence about their tools and objectives. This technique must be carefully weighed against the risk of additional data exposure. The 2016 Bangladesh Bank SWIFT heist demonstrates the consequences of insufficient containment: attackers who had gained access to the bank's SWIFT terminals submitted fraudulent transfer requests totaling $951 million before containment was executed, with $81 million successfully transferred. Evidence preservation during containment, specifically capturing RAM before isolating systems, is critical per ISO/IEC 27037:2012 guidelines to ensure forensic admissibility of collected data.
:::

%%%
---
unit: Lifecycle
code: REC
title: "Phase 3b: Eradication & Recovery"
---
:::callout style=soft
**Eradication** involves removing the root causes of the incident, such as malware payloads, backdoors, and compromised credentials. **Recovery** restores systems to normal operations while verifying security settings.
:::

:::image src="images/20_eradication_recovery.png" alt="Two-panel diagram: the left panel labeled Eradication shows a malware icon being removed from a system and a patch being applied; the right panel labeled Recovery shows a server being rebuilt from a clean gold image with a monitoring graph showing enhanced alerting post-restoration" caption="Phase 3b, Eradication and Recovery: root causes are removed and systems are rebuilt from trusted baselines before returning to production under enhanced monitoring." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Eradication Procedures"
:::list style=plain
- **Malware Removal:** Scanning and cleaning systems, or rebuilding them from trusted images.
- **Vulnerability Remediation:** Applying patches to address the exploits used for initial access.
- **Credential Reset:** Enforcing enterprise-wide password resets for all affected accounts.
:::
::::
::col::
::::card heading="Recovery & Verification"
:::list style=plain
- **Safe Restoration:** Restoring data from known-clean backups.
- **Gradual Phase-In:** Returning systems to service in stages to avoid resource overload.
- **Continuous Monitoring:** Implementing enhanced logging and alerts for a set period to verify the threat is gone.
:::
::::
::::

:::steps
1. **Remove Malware:** Wipe compromised systems and rebuild from trusted, verified gold images rather than attempting in-place cleaning.
2. **Patch Vulnerabilities:** Apply all available patches for the exploit used to gain initial access before restoring the system to production.
3. **Reset Credentials:** Execute enterprise-wide credential resets, including service accounts and the KRBTGT account if domain credentials were exposed.
4. **Restore from Backup:** Recover data from the most recent known-clean backup and verify integrity via hash comparison.
5. **Phase-In Gradually:** Return systems to service in stages, monitoring each for signs of re-infection before proceeding.
6. **Maintain Enhanced Monitoring:** Apply tighter SIEM correlation thresholds and expanded logging for a defined post-recovery period (typically 7–14 days).
:::

:::notes
After containing the threat, the team moves to Eradication and Recovery. Eradication focuses on removing the root causes of the incident. This involves deleting malware, closing backdoors, and resetting compromised credentials. It also requires patching the vulnerability used by the attacker to gain access. If the vulnerability is not addressed, the attacker can quickly re-compromise the system upon restoration.

Once eradication is complete, the recovery phase begins. The team restores systems to normal operations. Where possible, systems are rebuilt from trusted, clean images rather than cleaned in place, ensuring no remnants of the malware remain. Data is restored from clean backups, and systems are brought back online gradually.

After restoration, enhanced monitoring is maintained for a set period (typically 7 to 14 days). This monitoring verifies that the eradication was successful and that the attacker has not re-entered the system.

The distinction between cleaning and rebuilding a compromised system is critical. NIST SP 800-61 Rev. 2 recommends rebuilding from trusted images wherever operationally feasible, as cleaning attempts often miss persistent backdoors embedded in firmware, boot sectors, or deeply nested registry keys. The 2018 Marriott International breach illustrates the risk of incomplete eradication: attackers from the APT40 group (MITRE Group G0065) maintained access to Starwood's reservation database for four years, partially because the initial compromise was not fully eradicated before Marriott's acquisition. Credential reset is one of the most critical eradication steps. If an attacker has extracted the Active Directory NTDS.dit database (which contains password hashes for all domain accounts), a full enterprise-wide credential reset, including service accounts and the KRBTGT account to invalidate all existing Kerberos tickets, is required. This procedure is documented in Microsoft's guidance on recovering from a Golden Ticket attack (MITRE ATT&CK T1558.001). The enhanced monitoring period post-recovery typically applies tighter SIEM correlation thresholds and deploys additional network sensors aligned with NIST SP 800-137 continuous monitoring requirements.
:::

%%%
---
unit: Lifecycle
code: PST
title: "Phase 4: Post-Incident Activity"
---
:::callout style=soft
**Post-Incident Activity** involves conducting a "Lessons Learned" review to analyze the team's performance, identify process improvements, and update security controls.
:::

:::image src="images/20_post_incident_review.png" alt="Process diagram showing the lessons-learned review workflow: a timeline reconstruction feeds into a control assessment, which feeds into an RCA report, which feeds into IRP and baseline updates, which circle back to the Preparation phase of the lifecycle" caption="Phase 4, Post-Incident Activity: a structured lessons-learned review converts incident findings into documented improvements that strengthen the next response cycle." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Lessons Learned Objectives"
:::list style=plain
- **Timeline Verification:** Reconstructing the incident chronology to identify gaps in detection.
- **Control Assessment:** Evaluating the performance of existing security controls.
- **Process Improvement:** Updating the Incident Response Plan (IRP) based on lessons learned.
:::
::::
::col::
::::card heading="Key Questions to Address"
:::list style=plain
- Exactly what occurred, and at what times?
- How well did the staff perform during the incident?
- What actions were taken, and did they follow the IRP?
- What information was needed that was not available?
- How can we prevent similar incidents in the future?
:::
::::
::::

:::steps
1. **Schedule the Meeting:** Convene the lessons-learned review within 1–2 weeks of incident resolution (NIST SP 800-61 Rev. 2 recommendation), while details remain fresh.
2. **Reconstruct the Timeline:** Document the full attack chronology from initial access to eradication, referencing SIEM logs and forensic artifacts.
3. **Evaluate Controls:** Assess which security controls performed effectively and which failed or were absent during the incident.
4. **Draft the RCA Report:** Compile findings into a Root Cause Analysis report with prioritized remediation recommendations and control gaps identified.
5. **Update the IRP:** Revise the Incident Response Plan, security baselines, and detection rules based on the lessons learned to prepare for future incidents.
:::

:::notes
The post-incident phase is often overlooked as teams rush back to normal operations. However, this phase is critical for improving long-term security. Conducting a "Lessons Learned" review allows the organization to learn from the incident and strengthen its defenses.

NIST SP 800-61 Rev. 2 recommends holding a lessons-learned meeting within one to two weeks of the incident. This meeting brings the CSIRT and key stakeholders together to discuss the response. The team reviews the incident timeline, evaluates the performance of security controls, and identifies process improvements.

The findings are documented in a Root Cause Analysis (RCA) report. This report details how the attacker gained access, what systems were affected, and what controls are needed to prevent recurrence. The lessons learned are then used to update the Incident Response Plan, ensuring the team is better prepared for future threats.

NIST SP 800-61 Rev. 2 Chapter 3.4 specifies that lessons-learned meetings should occur within 1–2 weeks of incident resolution, while details remain fresh. The RCA report produced from this meeting serves multiple organizational functions: it provides technical documentation for engineering teams implementing control improvements; it serves as a compliance artifact demonstrating due diligence under frameworks such as PCI DSS, HIPAA, and SOC 2; and it may be required for regulatory breach notifications under GDPR Article 33 or state breach notification laws. ISO/IEC 27035-1:2023 further specifies that post-incident activity should include updating the organization's risk register to reflect newly identified threat vectors. The 2017 Equifax breach post-incident analysis revealed that a known Apache Struts vulnerability (CVE-2017-5638) had not been patched despite being present on the organization's own scanner-detected list. This finding, that the vulnerability was known but unpatched, led to the CISO's resignation and congressional hearings, demonstrating that RCA findings carry executive and regulatory consequences well beyond technical remediation.
:::

%%%
---
unit: Synthesis
code: IRW
title: Incident Response Walkthrough
---
:::image src="images/20_ransomware_walkthrough.png" alt="Horizontal timeline diagram tracing a ransomware incident through the six NIST IR phases, with labeled milestones showing EDR alert, host isolation, drive wipe, backup restoration, and RCA completion, and forensic evidence callout boxes at each phase" caption="Ransomware incident walkthrough: a complete NIST lifecycle trace from EDR detection through post-incident RCA, showing evidence collected and actions taken at each phase." width=full
:::

:::table
| NIST Phase | Scenario Step (Symmetric Cryptographic Ransomware) | Action Taken by CSIRT | Forensic Evidence Preserved |
|---|---|---|---|
| **Preparation** | Baseline configuration active; offsite backups configured. | Pre-positioning EDR agents and backup infrastructure. | Secure gold images and configuration logs. |
| **Detection & Analysis** | EDR alerts on unauthorized bulk file encryption. | Analyst triages alert, confirms active ransomware, scopes affected hosts. | Volatile RAM image; Sysmon process creation logs. |
| **Containment** | Ransomware attempts lateral movement over SMB. | CSIRT isolates host network connections via switch configuration. | Firewall connection logs; active network sockets. |
| **Eradication** | Malware is isolated but remains on system disk. | Wiping host drives and rebuilding systems from trusted baselines. | Corrupt or encrypted disk sectors for analysis. |
| **Recovery** | Restoring business applications and services. | Restoring files from offsite backups; implementing enhanced EDR monitoring. | Backup integrity validation logs. |
| **Post-Incident** | IRP review and security control updates. | Conducting lessons-learned review and updating security baselines. | Root Cause Analysis (RCA) report. |
:::

:::notes
This walkthrough illustrates the incident response lifecycle in a ransomware scenario. In the preparation phase, the team has EDR agents deployed and offline backups configured. During detection, the EDR flags unauthorized file encryption. The analyst triages this alert and confirms the incident.

In the containment phase, the team isolates the affected hosts from the network, blocking lateral movement. Next, eradication is executed by wiping the drives and rebuilding the systems from clean images. During recovery, files are restored from backups, and enhanced monitoring is implemented to verify the system is secure. Finally, in the post-incident phase, the team reviews the response and updates security controls, completing the lifecycle.

The ransomware scenario in this table reflects a pattern commonly documented in FBI and CISA joint cybersecurity advisories. The Conti ransomware group, before its 2022 dissolution, was attributed with attacks on over 400 organizations globally using a playbook that closely mirrors the phases shown here: initial access via phishing or vulnerability exploitation, lateral movement using Cobalt Strike and legitimate admin tools, data exfiltration prior to encryption, and finally deployment of a symmetric AES-256 encryption routine that made file recovery impossible without the key. The NIST phases map specifically to the ATT&CK tactics observed: Initial Access (TA0001), Execution (TA0002), and Lateral Movement (TA0008) occur before detection; Exfiltration (TA0010) and Impact (TA0040) occur if containment is delayed. This walkthrough demonstrates that the value of immutable, offline backups is not theoretical, it is the single most effective recovery control against ransomware. CISA's advisory AA23-061A on Royal ransomware and the FBI's advisory on Hive ransomware both confirm that organizations with tested backup restoration procedures recovered significantly faster than those without. The forensic evidence preserved at each phase, RAM images, network logs, and Sysmon process trees, directly informs the eradication strategy and the post-incident RCA report.
:::

%%%
---
unit: Foundations
code: SEV
title: Incident Severity Classification
---
:::callout style=soft
**Severity classification** translates raw technical findings into business-risk language, driving escalation paths, response timelines, and regulatory notification decisions.
:::

:::image src="images/20_severity_classification.png" alt="Four-row color-coded severity matrix showing P1 Critical in red, P2 High in orange, P3 Medium in yellow, and P4 Low in green, each row listing example incident types, response SLA, and required stakeholder notifications" caption="Incident severity matrix: a standardized classification system that maps technical impact to business risk, response timelines, and notification requirements." width=full
:::

:::table
| Severity | Label | Example Incidents | Response SLA | Notifications Required |
|---|---|---|---|---|
| **P1** | Critical | Active data exfiltration; ransomware with system-wide encryption; APT lateral movement confirmed | Immediate, 15 min | CISO, Legal, PR, CEO, Regulators |
| **P2** | High | Confirmed unauthorized access; credential compromise with lateral movement; DDoS with service outage | 1 hour | CISO, Legal, Incident Manager |
| **P3** | Medium | Malware detected but contained; suspicious insider activity; phishing campaign with clicks | 4 hours | Incident Manager, Security Team Lead |
| **P4** | Low | Blocked phishing email; single failed login spike; routine policy violation | Next business day | On-call analyst |
:::

:::list style=plain
- **Functional Impact**, degree to which normal operations are disrupted (none / minimal / significant / catastrophic)
- **Information Impact**, whether sensitive data was accessed, exfiltrated, or destroyed
- **Recoverability**, expected time and resources needed to restore full normal operations
:::

:::notes
Severity classification is the bridge between technical analysis and organizational response. Without a shared severity language, security analysts and business executives will disagree on urgency, leading to delayed decisions and worsened outcomes. A formal severity matrix, like the one shown here, ensures that every stakeholder, from the on-call SOC analyst to the CEO, uses consistent definitions for what constitutes a critical versus a low-severity event.

NIST SP 800-61 Rev. 2 Section 3.2.6 introduces functional impact, information impact, and recoverability as the three axes of incident prioritization. Functional impact measures the degree to which the incident disrupts normal operations. An incident affecting a single workstation with no sensitive data access might have minimal functional impact. An incident that disables the organization's entire order processing system has catastrophic functional impact. Information impact assesses whether sensitive data was accessed or exfiltrated. Under GDPR Article 33, once personal data is confirmed to have been accessed by unauthorized parties, the 72-hour regulatory notification clock begins. HIPAA's Breach Notification Rule (45 CFR Part 164) similarly requires covered entities to notify individuals within 60 days of discovering a breach of protected health information (PHI). Recoverability estimates how long it will take to return to normal operations. This estimate informs business continuity decisions, for example, whether to activate disaster recovery infrastructure or invoke contractual SLA clauses with cloud providers. Severity classification requires both technical understanding and business context: a critical system being affected changes the rating dramatically even when the technical indicators are identical to a low-risk event.
:::

%%%
---
unit: Foundations
code: CSR
title: CSIRT Roles Deep-Dive
---
:::callout style=soft
An effective CSIRT blends technical, legal, communications, and executive roles, each with distinct responsibilities that must be clearly defined before an incident occurs.
:::

:::image src="images/20_csirt_roles_deepdive.png" alt="Detailed organizational diagram of a CSIRT showing six roles: Incident Commander at the top, with Security Analyst, Forensics Specialist, Threat Intelligence Analyst, Legal Counsel, and Communications Lead branching below, each with a brief responsibility summary" caption="CSIRT roles and responsibilities: the cross-functional team structure required to manage complex security incidents from technical analysis through executive communication." width=full
:::

:::table
| Role | Primary Responsibility | Key Skill | Output |
|---|---|---|---|
| **Incident Commander** | Overall coordination and decision authority | Leadership, time management | Status updates, escalation decisions |
| **Lead Security Analyst** | Technical investigation, log correlation | SIEM, EDR, packet analysis | Attack timeline, affected asset list |
| **Forensics Specialist** | Evidence acquisition and chain of custody | FTK, Volatility, write-blocking | Forensic images, chain-of-custody forms |
| **Threat Intelligence Analyst** | IOC enrichment and threat actor attribution | MITRE ATT&CK, OSINT | TI reports, IOC watchlists |
| **Legal Counsel** | Regulatory compliance, law enforcement liaison | Breach notification law | Notification letters, regulatory filings |
| **Communications Lead** | Internal and external messaging | Crisis communications | Press statements, staff notifications |
:::

:::notes
When an incident occurs, the pressure to act quickly can lead to chaotic, uncoordinated responses if roles are not pre-defined. The CSIRT structure formalizes accountability, every critical decision during an incident has an identified owner, and every output has an identified author.

The Incident Commander role is often misunderstood. This is not necessarily the most senior technical person; it is the person best equipped to coordinate multiple workstreams simultaneously, prioritize competing demands, and communicate clearly with executive leadership. During the 2021 Colonial Pipeline incident, the lack of a clear incident commander for operational technology (OT) systems contributed to delayed containment decisions. The Lead Security Analyst drives the technical investigation. In practice, this means managing multiple SIEM queries and EDR hunting sessions simultaneously while continuously updating the attack timeline. The Forensics Specialist must be activated early, before containment actions modify volatile memory or overwrite disk sectors. ISO/IEC 27037:2012 (Guidelines for Identification, Collection, Acquisition and Preservation of Digital Evidence) defines the principle of minimizing changes to digital evidence. The Threat Intelligence Analyst adds context to raw IOCs: a malicious IP address is much more actionable if an analyst can confirm it belongs to a known APT group, correlate it to a specific MITRE ATT&CK technique, and identify whether other organizations are reporting the same indicator. Legal Counsel ensures that actions taken during the incident, such as accessing employee accounts during investigation or preserving evidence, comply with local jurisdiction requirements. The Communications Lead manages both internal staff notifications, which prevent panic and rumor spread, and external communications, which protect the organization's reputation. If the Incident Commander is unavailable during a major incident, response stalls unless a backup is defined, which is why NIST SP 800-61 Rev. 2 Section 2.4 requires documented backup assignments for every CSIRT role.
:::

%%%
---
unit: Lifecycle
code: CHK1
title: "Mid-Lecture Checkpoint: Phases 1–2"
---
:::callout style=soft
Pause and check your understanding of NIST SP 800-61 phases 1 and 2 before proceeding to containment and recovery operations.
:::

:::image src="images/20_checkpoint_phases12.png" alt="Split quiz card layout with two columns labeled Phase 1 Preparation and Phase 2 Detection and Analysis, each containing three blank question prompts with answer space below, styled as a written knowledge check" caption="Checkpoint: self-assess your understanding of the first two NIST incident response phases before moving to operational containment." width=full
:::

:::list style=plain
**Answer these questions before moving forward:**
- What is the difference between a security event and a security incident under NIST SP 800-61?
- Name three items that should be included in an incident response team's "jump kit."
- What are the two categories of impact that NIST uses to prioritize incidents during triage?
- Why must volatile memory (RAM) be captured before network isolation of a compromised host?
- Which CSIRT role is responsible for external communications during a breach?
:::

:::callout style=soft
If you cannot answer all five questions from memory, review slides INC (What Is an Incident?) and DET (Phase 2: Detection & Analysis) before proceeding.
:::

:::notes
This checkpoint slide is designed to consolidate the foundational and detection-phase material before students encounter the more operationally intensive containment and eradication content. Research in instructional design consistently shows that spaced retrieval practice, recalling information shortly after learning it, significantly improves long-term retention compared to passive re-reading. This checkpoint operationalizes that principle within the lecture flow.

Let's work through the expected answers. First: a security event is any observable occurrence in a system or network, while a security incident is an adverse event that threatens the confidentiality, integrity, or availability of an information system. The key word is "adverse", not all events are incidents. Second: jump kits should contain a forensic laptop with pre-installed tools (e.g., FTK Imager, Volatility, Wireshark), hardware write-blockers, network cables and taps, portable storage media with verified clean-room capacity, and out-of-band communication devices. Third: NIST uses functional impact and information impact as the two prioritization axes, functional impact measures operational disruption, while information impact measures the sensitivity and extent of data accessed. Fourth: volatile memory (RAM) holds critical forensic artifacts including running processes, open network connections, encryption keys, and injected shellcode that disappear the moment power is cut or the network stack is reset. Capturing RAM before isolation preserves this evidence per ISO/IEC 27037:2012 guidelines. Fifth: the Communications Lead (or PR representative) is responsible for external communications. This role works closely with Legal Counsel to ensure statements do not expose the organization to additional liability.
:::

%%%
---
unit: Tools
code: SEM
title: "Tool Spotlight: SIEM for Incident Detection"
---
:::callout style=soft
A **Security Information and Event Management (SIEM)** system is the central nervous system of incident detection, aggregating logs from thousands of sources and applying correlation rules to surface actionable alerts.
:::

:::image src="images/20_siem_detection.png" alt="Architecture diagram showing log sources (firewalls, endpoints, cloud platforms, identity providers) feeding into a central SIEM platform with labeled components for log ingestion, normalization, correlation engine, and alert dashboard, with an arrow to SOC analyst workstation" caption="SIEM architecture: distributed log sources are normalized and fed into a correlation engine that produces prioritized alerts for SOC analyst review." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Core SIEM Functions"
:::list style=plain
- **Log Aggregation:** Collecting events from firewalls, endpoints, identity providers, and cloud platforms into a unified data store.
- **Normalization:** Converting logs from diverse formats into a common schema for consistent querying.
- **Correlation:** Applying detection rules that identify multi-event attack patterns across log sources.
- **Alerting:** Generating prioritized alerts when correlation thresholds are exceeded.
:::
::::
::col::
::::card heading="Common SIEM Platforms"
:::list style=plain
- **Splunk Enterprise Security**, market-leading SIEM with extensive integration ecosystem and SPL query language.
- **Microsoft Sentinel**, cloud-native SIEM on Azure with native M365 and Entra ID integration.
- **IBM QRadar**, on-premises SIEM widely deployed in financial and government sectors.
- **Elastic SIEM**, open-source option built on the Elastic Stack with EQL (Event Query Language) detection.
:::
::::
::::

:::notes
The Security Information and Event Management (SIEM) system is the foundational technology enabling Phase 2 of the NIST incident response lifecycle. Without centralized log aggregation and correlation, security teams are forced to manually review logs across dozens of disconnected systems, an approach that scales poorly and introduces significant detection delays. The Verizon Data Breach Investigations Report consistently finds that the median time from initial compromise to detection remains measured in weeks or months for organizations without mature SIEM deployments.

A modern SIEM performs four core functions. Log aggregation collects raw events from every observable layer of the enterprise stack: perimeter firewalls, endpoint operating systems, identity and access management systems, cloud service provider APIs, and SaaS applications. Normalization converts these heterogeneous log formats into a common schema, for example, mapping the Windows Security Event ID 4624 (successful logon) and Linux PAM authentication messages into a unified "authentication success" field that can be queried consistently. Correlation is where detection actually occurs. Correlation rules encode attack patterns as logical queries that execute against incoming events in near-real-time. For example, a rule might fire an alert when five or more failed authentication attempts from the same source IP occur within 60 seconds, detecting brute-force attacks that would be invisible to any single log source. NIST SP 800-92 (Guide to Computer Security Log Management) provides guidelines for SIEM log retention periods, recommending a minimum of one year of searchable log data to support incident investigations. The Equifax breach (CVE-2017-5638) highlighted a critical SIEM blind spot: because an expired TLS certificate disabled SSL inspection, the attackers' HTTPS-encapsulated exfiltration traffic was invisible to the SIEM's network-based correlation rules for 78 days. This case demonstrates that SIEM effectiveness is bounded by the completeness of its log sources. A SIEM correlation query demonstrates the practical power of log analysis: counting failed-logon events (Windows Event ID 4625) by source address and flagging any source with more than a hundred reveals a brute-force attempt in a single query.
:::

%%%
---
unit: Tools
code: EDR
title: "Tool Spotlight: Endpoint Detection & Response"
---
:::callout style=soft
**Endpoint Detection and Response (EDR)** tools provide continuous behavioral monitoring at the host level, enabling detection of fileless malware, living-off-the-land attacks, and post-exploitation activity invisible to traditional antivirus.
:::

:::image src="images/20_edr_tool_spotlight.png" alt="Endpoint monitoring diagram showing an EDR agent on a Windows host collecting process telemetry, registry events, network connections, and file operations, transmitting to a cloud-based EDR console with a threat hunting interface and automated response workflow" caption="EDR architecture: agent-based host telemetry flows to a centralized console, enabling both automated threat response and analyst-driven threat hunting." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="What EDR Monitors"
:::list style=plain
- **Process Creation:** Every process spawned, with parent-child relationships and command-line arguments.
- **Network Connections:** Outbound connections from processes, enabling C2 traffic detection.
- **Registry Modifications:** Changes to persistence locations such as `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`.
- **File Operations:** Creation, modification, and deletion of files, especially in system directories.
:::
::::
::col::
::::card heading="EDR Platforms"
:::list style=plain
- **CrowdStrike Falcon**, cloud-native, widely used in enterprise environments.
- **Microsoft Defender for Endpoint**, deeply integrated with Windows telemetry and Microsoft Sentinel.
- **SentinelOne**, autonomous AI-driven response with rollback capabilities.
- **Carbon Black (VMware)**, strong in threat hunting with behavioral query language.
:::
::::
::::

:::notes
Endpoint Detection and Response technology was developed to address the fundamental limitation of traditional antivirus: signature-based detection cannot identify threats that have no known signature. Fileless malware, which executes entirely in memory using legitimate system tools, evades signature scanning completely. EDR addresses this by monitoring behavioral patterns rather than file content. The concept of behavioral monitoring for endpoint security was formalized by Gartner analyst Anton Chuvakin in 2013, who coined the term "EDR" to describe products that recorded endpoint events and provided detection and investigation capabilities.

EDR agents operate at the kernel level on monitored hosts, giving them visibility into every process creation event, including the parent-child process relationships that reveal attacker techniques. For example, when a phishing document triggers a Microsoft Word process that spawns PowerShell with an encoded command string, a classic Living-off-the-Land (LotL) attack pattern, the EDR records this relationship and flags it against behavioral detection rules aligned with MITRE ATT&CK technique T1059.001 (PowerShell). Network connection monitoring by the EDR enables detection of Command-and-Control (C2) traffic. When malware beacons to a C2 server, the EDR captures the process responsible for the connection, the destination IP and port, and the timing intervals, all of which can confirm C2 communication even before network-level detections fire. The CrowdStrike investigation of the 2020 SolarWinds SUNBURST breach demonstrated EDR capability at scale: the forensic trail reconstructed from endpoint telemetry across multiple customer environments revealed the sophisticated supply chain attack methodology in extraordinary detail. MITRE's ATT&CK Evaluations program annually tests EDR platforms against real-world adversary emulations, providing the industry's most rigorous third-party comparison of EDR detection capabilities. The MITRE ATT&CK Evaluations coverage heatmap for an EDR vendor shows concretely how detection capability maps to specific tactics and techniques, which is the practical value of the ATT&CK framework.
:::

%%%
---
unit: Tools
code: TI
title: Threat Intelligence in Incident Response
---
:::callout style=soft
**Cyber Threat Intelligence (CTI)** enriches raw IOCs with adversary context, converting an IP address or file hash into actionable knowledge about the threat actor's capabilities, objectives, and tactics.
:::

:::image src="images/20_threat_intelligence_ir.png" alt="Diamond model of intrusion analysis showing four nodes, Adversary, Capability, Infrastructure, and Victim, connected in a diamond shape with bidirectional arrows, with example annotations showing APT29 at Adversary, SUNBURST malware at Capability, a Cloudfront CDN domain at Infrastructure, and SolarWinds Orion at Victim" caption="Diamond Model of Intrusion Analysis: threat intelligence maps adversary capabilities and infrastructure to victim systems, enabling attribution and proactive detection." width=full
:::

:::list style=plain
- **Strategic CTI:** High-level intelligence about threat actor motivations, geopolitical context, and campaign objectives, used by executives and risk managers.
- **Operational CTI:** Intelligence about specific campaigns, TTPs (Tactics, Techniques, and Procedures), and targeting patterns, used by CSIRT planners.
- **Tactical CTI:** Specific IOCs (IP addresses, file hashes, domain names, YARA rules) directly consumable by SIEM, EDR, and firewall platforms.
- **MITRE ATT&CK:** Framework mapping observed techniques to known adversary groups, enabling TTP-based detection rather than IOC-only detection.
- **ISAC Sharing:** Industry-specific Information Sharing and Analysis Centers (FS-ISAC, H-ISAC) provide sector-relevant threat intelligence feeds.
:::

:::notes
Threat intelligence transforms the incident response process from reactive to informed. Without CTI, a CSIRT investigating an unknown malware sample is essentially starting from scratch: they must reverse-engineer the malware, identify its C2 infrastructure, and determine its objectives independently. With CTI, an analyst who identifies a known IOC, such as a file hash matching a YARA rule for APT29's SUNBURST implant, can immediately access a rich body of knowledge about the adversary's typical lateral movement techniques, exfiltration methods, and persistence mechanisms, enabling a far more targeted investigation.

The three tiers of CTI reflect different organizational consumers. Strategic CTI informs executive decisions, for example, intelligence indicating that a nation-state actor is targeting organizations in the financial sector with spear-phishing campaigns would prompt executive risk discussions and budget allocations for enhanced phishing defenses. Operational CTI guides CSIRT planning, understanding that a particular ransomware group typically spends 14 days conducting reconnaissance before deploying encryption payloads allows defenders to focus hunting efforts on early-stage intrusion indicators. Tactical CTI is the most immediately actionable: YARA rules can be deployed to EDR platforms, IP blocklists can be pushed to firewalls, and domain blacklists can be applied to DNS resolvers within hours of receipt. The Diamond Model of Intrusion Analysis, developed by Caltagirone, Pendergast, and Betz (2013), provides a structured framework for representing the relationship between adversaries, capabilities, infrastructure, and victims. During the SolarWinds investigation, the Diamond Model was used to connect the SUNBURST implant (capability) to the attacker-controlled Cloudfront domains (infrastructure) to the SolarWinds Orion build pipeline (victim), ultimately enabling attribution to the APT29 (Cozy Bear) threat actor group with high confidence. STIX (Structured Threat Information Expression) and TAXII (Trusted Automated eXchange of Intelligence Information) are the open standards for machine-readable CTI sharing, enabling automated IOC ingestion directly into SIEM platforms. An ATT&CK group page, for APT29 or Lazarus Group for example, with the Navigator heatmap, visually represents the techniques known to be in an adversary's arsenal, which directly informs detection-engineering priorities.
:::

%%%
---
unit: Lifecycle
code: IOC
title: Indicators of Compromise, Collection & Management
---
:::callout style=soft
**Indicators of Compromise (IOCs)** are forensic artifacts that provide evidence that a system has been compromised. Systematic IOC management enables detection across the enterprise during active investigations.
:::

:::image src="images/20_ioc_management.png" alt="IOC lifecycle diagram showing four stages: Discovery (IOC identified in forensic analysis), Enrichment (context added via threat intelligence platforms), Distribution (IOC pushed to SIEM, EDR, and firewall block lists), and Retirement (IOC aged out after staleness threshold exceeded)" caption="IOC management lifecycle: from discovery in forensic analysis through threat intelligence enrichment, enterprise-wide distribution, and eventual retirement." width=full
:::

:::table
| IOC Type | Example | Detection Platform | Reliability |
|---|---|---|---|
| **File Hash (MD5/SHA-256)** | `d41d8cd98f00b204e9800998ecf8427e` | EDR, AV | High (specific to the sample) |
| **IP Address** | `192.0.2.47` (C2 server) | Firewall, SIEM, EDR | Medium (easily changed by attacker) |
| **Domain Name** | `update.maliciouscdn[.]com` | DNS RPZ, SIEM, Proxy | Medium-High |
| **Registry Key** | `HKCU\Software\Classes\ms-settings\shell\open\command` | EDR, Windows Event Logs | High (technique-specific) |
| **YARA Rule** | Pattern matching on PE binary characteristics | EDR, malware sandbox | Very High (behavior-based) |
| **Network Pattern (Sigma)** | DNS queries with high-entropy subdomain strings | SIEM | High (beaconing detection) |
:::

:::notes
Indicators of Compromise are the raw material of forensic investigation. When an analyst discovers a piece of malware on a compromised host, they extract IOCs, the file hash, the C2 domain, the registry persistence key, the network signatures, and distribute these indicators across the enterprise's defensive stack to identify other affected systems and block further attacker activity. Understanding the different types of IOCs and their relative reliability is essential for effective incident response.

The Pyramid of Pain, introduced by security researcher David Bianco in 2013, provides an elegant framework for understanding IOC reliability. At the base of the pyramid are hash values, easy for defenders to detect but also easy for attackers to change by modifying a single byte of the malware binary. Network artifacts like IP addresses and domain names are moderately difficult for attackers to change but remain low-cost evasions. At the apex of the pyramid are TTPs (Tactics, Techniques, and Procedures), when defenders can detect attacker behavior (for example, detecting any process that uses DLL side-loading for persistence, regardless of the specific binary), they have reached the highest level of detection maturity. This is precisely why MITRE ATT&CK-based detection, using tools like Sigma rules for SIEM correlation, is considered more robust than IOC-only detection. During the SolarWinds SUNBURST investigation (CVE-2020-10148), FireEye researchers published YARA rules, Sigma rules, and network signatures within hours of discovery, enabling the global security community to rapidly scan for the implant. YARA, originally developed by Victor Manuel Alvarez at VirusTotal, allows analysts to write pattern-matching rules against binary content, memory, or file metadata. Sigma provides an equivalent for SIEM log detection, enabling cross-platform log query sharing. IOC management platforms, such as MISP (Malware Information Sharing Platform), OpenCTI, or commercial platforms like ThreatConnect, automate the enrichment, distribution, and retirement of IOCs at enterprise scale. IOC retirement is a frequently overlooked discipline: a two-year-old C2 IP address is likely reassigned to a legitimate cloud provider, and blocking it will cause false-positive disruptions. Most programs implement a 90-day default TTL for IP and domain IOCs. Community threat-sharing platforms such as MISP provide a large, diverse volume of shared threat intelligence at no cost, so substantial incident-response capability is available through open-source tooling and community collaboration.
:::

%%%
---
unit: Lifecycle
code: MEM
title: Memory Forensics in Incident Response
---
:::callout style=soft
**Memory forensics** recovers volatile artifacts, running processes, injected shellcode, network sockets, and encryption keys, that exist only in RAM and are destroyed when a system is powered off.
:::

:::image src="images/20_memory_forensics.png" alt="Diagram showing a RAM chip with arrows pointing to extracted forensic artifacts: process list, network connection table, kernel module list, registry hive cached in memory, and injected shellcode detected via VAD (Virtual Address Descriptor) tree analysis" caption="Memory forensics artifacts: volatile data structures in RAM that reveal active attacker presence invisible to disk-based forensic analysis." width=full
:::

:::steps
1. **Acquire RAM Image:** Use a tool such as WinPmem, FTK Imager, or LiME (Linux Memory Extractor) to capture a raw memory image before any system changes are made.
2. **Run Volatility Profile:** Identify the operating system version and kernel build to select the correct Volatility 3 analysis profile.
3. **List Running Processes:** Execute `vol.py pslist` and `pstree` to identify suspicious parent-child process relationships.
4. **Identify Injected Code:** Run `malfind` to detect process memory regions with executable permissions that lack a backing file on disk (indicating code injection).
5. **Extract Network Connections:** Use `netscan` to recover active and recently closed network connections, including attacker C2 channels.
6. **Recover Encryption Keys:** Use specialized plugins (e.g., `bitlockerkeys`, `truecryptmaster`) to recover in-memory encryption keys if encrypted volumes are present.
:::

:::notes
Memory forensics is one of the most powerful capabilities available to incident responders, and also one of the most time-sensitive. The volatile data structures resident in RAM at the moment of compromise, running processes, open network connections, loaded kernel modules, and injected shellcode, provide irreplaceable evidence about attacker activities that is simply unavailable from disk-based analysis alone. This is especially true for fileless malware and advanced persistent threats that deliberately avoid writing to disk to evade forensic detection.

The Volatility Framework, originally developed by Aaron Walters and now maintained as Volatility 3 under the Volatility Foundation, is the industry standard open-source tool for memory analysis. Its plugin architecture supports hundreds of analysis modules, from basic process listing to sophisticated kernel rootkit detection. The `malfind` plugin is particularly important: it identifies memory regions within process virtual address space that are marked as executable but have no backing file on disk. This pattern is a strong indicator of process injection (MITRE ATT&CK T1055), where attacker shellcode is injected into the address space of a legitimate process such as explorer.exe or lsass.exe to evade process-based detections. The lsass.exe process deserves special attention: Windows stores NTLM password hashes and, in some configurations, cleartext credentials in the lsass process address space. The Mimikatz tool (used in countless real-world breaches including the 2017 NotPetya attack attributed to Russia's Sandworm group, CVE-2017-5754 family) exploits this to dump credentials directly from memory. Memory forensics using Volatility's `lsadump` plugin can identify whether Mimikatz was used against lsass, even if Mimikatz itself was never written to disk. ISO/IEC 27037:2012 emphasizes that memory acquisition must occur at the earliest possible stage of evidence collection, as it is the most volatile of all evidence types. The order of volatility, a foundational forensic principle, ranks evidence collection priority from most volatile (RAM, CPU registers) to least volatile (optical media, printed documents). A memory-analysis process-tree plugin (for example Volatility's pstree) run against a memory dump makes a malicious parent-child process relationship visible quickly, which is how investigators spot injected or spoofed processes.
:::

%%%
---
unit: Lifecycle
code: NET
title: Network Forensics & Log Analysis
---
:::callout style=soft
**Network forensics** uses captured packet data and flow records to reconstruct attacker communication, identify lateral movement paths, and detect data exfiltration, providing evidence independent of host-level artifacts.
:::

:::image src="images/20_network_forensics.png" alt="Network diagram showing a packet capture tap on the core switch, with arrows to Wireshark for full packet analysis, Zeek for protocol metadata extraction, and a NetFlow collector for traffic volume analytics, all feeding into a SIEM timeline correlation panel" caption="Network forensics toolkit: packet capture, Zeek metadata, and NetFlow volume analytics combine to provide independent evidence of attacker communication and data movement." width=full
:::

::::columns ratio=1:1
::col::
::::card heading="Network Evidence Sources"
:::list style=plain
- **PCAP (Full Packet Capture):** Complete record of all network traffic, enabling full payload reconstruction. Storage-intensive; typically kept for 72 hours on high-throughput networks.
- **NetFlow / IPFIX:** Metadata-only flow records (source/destination IP, port, byte counts, duration) retained for 30–90 days.
- **DNS Query Logs:** Full record of all DNS lookups, revealing C2 beaconing and data exfiltration via DNS tunneling.
- **Proxy Logs:** HTTP/HTTPS request records showing URLs accessed, user agents, and response sizes.
:::
::::
::col::
::::card heading="Key Detection Signatures"
:::list style=plain
- **Beaconing:** Periodic outbound connections at regular intervals to C2 servers, detectable via NetFlow timing analysis.
- **Large Outbound Transfers:** Data exfiltration produces anomalous outbound byte counts to external destinations.
- **DNS Tunneling:** High-entropy, unusually long DNS subdomain strings used to exfiltrate data or tunnel C2 commands.
- **Lateral Movement SMB:** Unusual SMB (port 445) connections between internal workstations, indicating Pass-the-Hash or PsExec activity.
:::
::::
::::

:::notes
Network forensics provides an evidence layer that is independent of and complementary to host-based forensics. An attacker who successfully removes malware from a compromised endpoint and clears Windows Event Logs cannot retroactively erase network flow records captured at a core switch. This independence makes network evidence particularly valuable for corroborating host-based findings and for reconstructing attacker activity on systems where disk evidence has been destroyed.

The Zeek (formerly Bro) network analysis framework is the industry-standard open-source tool for network forensics. Unlike Wireshark, which operates on captured PCAP files, Zeek analyzes live network traffic and produces structured log files (conn.log, dns.log, http.log, ssl.log, etc.) that are directly queryable for forensic analysis. This structured output is far more efficient to search than raw PCAP, making Zeek the preferred tool for high-volume enterprise network monitoring. DNS query logs are among the most underutilized forensic resources in typical enterprise environments. Attackers frequently use DNS tunneling, encoding data in subdomain labels of DNS queries, to exfiltrate information or receive C2 commands, because DNS traffic on port 53 is rarely blocked at organizational perimeters. The Iodine and dnscat2 tools, both freely available, implement DNS tunneling and are commonly used in penetration tests and real-world attacks alike. MITRE ATT&CK technique T1071.004 (Application Layer Protocol: DNS) documents this pattern. NetFlow analysis for beaconing detection uses statistical methods: legitimate user traffic follows irregular, human-driven timing patterns, while malware C2 beaconing follows precise regular intervals (e.g., every 300 seconds). Tools such as RITA (Real Intelligence Threat Analytics), developed by ActiveCountermeasures, automate beacon detection from NetFlow data. The 2020 SolarWinds investigation used DNS analysis to discover that the SUNBURST malware was using encoded victim organization identifiers in DNS subdomain labels to communicate with avsvmcloud.com, a finding that enabled FireEye to track the full scope of the breach across victim networks by analyzing passive DNS data. NIST SP 800-86 (Guide to Integrating Forensic Techniques into Incident Response) dedicates an entire chapter to network forensic procedures and evidence preservation. Reconstructing an application-layer conversation from a packet capture, following a TCP stream, is the same technique investigators use to identify the content of exfiltrated data.
:::

%%%
---
unit: Lifecycle
code: COC
title: Digital Evidence & Chain of Custody
---
:::callout style=soft
**Chain of custody** is a documented record of who handled digital evidence, when, and under what circumstances, ensuring that evidence is admissible in legal proceedings and cannot be challenged as tampered.
:::

:::image src="images/20_chain_of_custody.png" alt="Chain of custody form diagram showing fields for evidence item number, description, acquisition date and time, hash values before and after acquisition, handler name and signature at each transfer, and storage location, with a sample completed row for a forensic disk image" caption="Chain of custody documentation: every evidence transfer is recorded with handler identity, timestamp, and hash verification to ensure forensic integrity." width=full
:::

:::list style=plain
- **Write-Blocking:** Hardware or software write-blockers must be used during disk imaging to prevent any modification to source media.
- **Hash Verification:** SHA-256 hash of the source disk is computed before and after acquisition; matching hashes prove the image is forensically identical to the source.
- **Evidence Labeling:** Every piece of collected evidence receives a unique identifier, case number, and handler signature.
- **Secure Storage:** Digital evidence is stored in access-controlled, tamper-evident containers with an audited access log.
- **ISO/IEC 27037:2012:** The international standard defining best practices for digital evidence identification, collection, acquisition, and preservation.
:::

:::callout style=soft
Any break in chain of custody, such as an unlogged evidence transfer or a failure to write-block before imaging, may render the evidence inadmissible in legal proceedings and expose the organization to liability.
:::

:::notes
Chain of custody is the procedural backbone of forensic evidence management. Without it, even the most technically perfect forensic analysis may be challenged and excluded in legal proceedings, allowing threat actors to escape accountability and leaving organizations unable to recover losses through litigation or insurance claims. Understanding chain of custody is not optional for incident responders, it is a fundamental professional responsibility.

The principle of write-blocking is central to evidence integrity. When a forensic analyst images a hard drive without a write-blocker, the act of connecting the drive to an analysis system can modify metadata, such as file access timestamps, making it impossible to distinguish analyst activity from attacker activity. Hardware write-blockers (such as those manufactured by Tableau, a Opentext brand) physically interrupt the write signal line on drive interfaces (SATA, USB, etc.), making modification literally impossible at the hardware level. ISO/IEC 27037:2012 formalizes these requirements. The standard identifies three levels of digital evidence handler: Digital Evidence First Responders (DEFRs) who initially identify and secure digital evidence; Digital Evidence Specialists (DESs) who perform more complex acquisition tasks; and Digital Forensic Laboratories (DFLs) that provide controlled examination environments. In practice, during major incidents, organizations often bring in external forensic firms such as Mandiant (now part of Google Cloud), CrowdStrike Services, or Kroll to perform evidence acquisition under conditions that will meet legal standards. The Federal Rules of Evidence (FRE) in the United States and equivalent frameworks in other jurisdictions require that digital evidence meet standards for authenticity (Rule 901) and best evidence (Rule 1002). Hash verification using SHA-256 (rather than the now-deprecated MD5) provides cryptographic proof of authenticity. Real-world case: during the prosecution following the 2014 JPMorgan Chase breach, chain of custody documentation for terabytes of server logs was critical to supporting the criminal case against the attackers, who were ultimately convicted in 2023. A chain-of-custody form, freely available from SANS and the U.S. Department of Justice, records who handled evidence, when and how; completing each field during an incident is what makes the evidence admissible.
:::

%%%
---
unit: Communication
code: COM
title: IR Communication Planning
---
:::callout style=soft
**Incident communication** must be structured, timely, and audience-appropriate, different stakeholders require different levels of technical detail and have different legal obligations following a breach.
:::

:::image src="images/20_ir_communication_plan.png" alt="Communication flow diagram showing four stakeholder audiences radiating from a central Incident Manager node: Internal Technical Team receiving real-time technical updates, Executive Leadership receiving executive briefings, Regulators receiving formal breach notification letters, and Customers and Media receiving public statements" caption="IR communication planning: the Incident Manager coordinates four parallel communication tracks with audience-appropriate content and timing." width=full
:::

:::table
| Audience | Communication Type | Timing | Key Content |
|---|---|---|---|
| **Internal Technical Team** | Secure real-time channel (e.g., Signal, dedicated IR Slack workspace) | Continuous throughout response | IOCs, affected systems, task assignments, technical status |
| **Executive Leadership** | Executive briefing (verbal + written summary) | Every 4 hours during P1; daily for P2–P3 | Business impact, containment status, regulatory risk, PR implications |
| **Regulators** | Formal breach notification letter | GDPR: 72 hours; HIPAA: 60 days; State laws vary | Nature of breach, data categories affected, mitigation steps taken |
| **Customers / Public** | Press statement, customer email notification | After legal review; timing varies by regulation | What happened, what data was affected, what actions to take |
| **Law Enforcement** | FBI/CISA voluntary or mandatory report | As soon as the incident is confirmed | Technical IOCs, attacker TTPs, business impact |
:::

:::notes
Communication during an incident is as mission-critical as technical containment. Poorly managed communications can amplify reputational damage, create legal liability, and undermine employee confidence, sometimes causing more lasting harm than the technical breach itself. The communication plan must be developed and tested during the Preparation phase, not improvised under pressure during an active incident.

The first principle of incident communications is audience segmentation. The technical team needs real-time, granular information about attacker activity, IOCs, and system status. But providing this same technical detail in an executive briefing or a customer notification would be inappropriate and potentially counterproductive, executives need business-impact summaries, and customers need clear, actionable guidance. The second principle is secure channel selection. If an attacker has compromised the organization's email infrastructure, using that email system for CSIRT coordination exposes the entire response plan to the attacker. Out-of-band communication channels, pre-established during Preparation, are activated for CSIRT coordination during significant incidents. The 2017 Equifax breach communications represent a case study in what not to do: the company waited six weeks to notify the public after discovering the breach (the compromise was discovered on July 29, 2017 but disclosed on September 7, 2017), set up a poorly secured website for identity theft victims that was itself vulnerable to XSS attacks, and their executives sold company stock in the days between internal discovery and public disclosure, leading to insider trading investigations. The contrast is the 2021 Microsoft Exchange Server vulnerability (CVE-2021-26855, ProxyLogon): Microsoft coordinated with CISA and NSA before public disclosure, releasing emergency patches alongside a detailed technical advisory that enabled defenders to remediate before widespread exploitation. Under GDPR Article 33, breach notification to the relevant supervisory authority must occur "without undue delay and, where feasible, not later than 72 hours after having become aware of it." The phrase "where feasible" creates some flexibility, but organizations must document the reasons for any delay. GDPR Article 34 separately requires notification to affected data subjects "without undue delay" when the breach is likely to result in high risk to their rights and freedoms. A verbal executive briefing during a ransomware incident, in which a CEO asks "should we pay the ransom?", surfaces the business and ethical dimensions of incident response that technical analysis alone does not address.
:::

%%%
---
unit: CaseStudy
code: CS1
title: "Case Study: SolarWinds SUNBURST (2020)"
---
:::callout style=soft
The **SolarWinds SUNBURST attack** (December 2020) was the most sophisticated supply chain attack ever publicly documented, a nation-state operation that compromised the software build pipeline of SolarWinds Orion, a widely deployed IT monitoring platform used by government agencies and Fortune 500 companies.
:::

:::image src="images/20_solarwinds_case_study.png" alt="Attack chain diagram for the SolarWinds SUNBURST breach showing six stages from left to right: Build Pipeline Compromise, Trojanized Orion Update Package, Victim Download and Installation, 14-Day Dormancy Period, C2 Beacon via DNS to avsvmcloud.com, and Hands-on Keyboard Operations by APT29, with MITRE ATT&CK technique IDs labeled at each stage" caption="SolarWinds SUNBURST attack chain: APT29 compromised the SolarWinds build pipeline to deliver a trojanized Orion update to approximately 18,000 organizations, enabling selective targeted access." width=full
:::

:::steps
1. **Supply Chain Compromise (Oct 2019):** APT29 (Cozy Bear) infiltrated SolarWinds' software build environment and injected the SUNBURST backdoor into the Orion update build pipeline. (MITRE ATT&CK T1195.002)
2. **Trojanized Update Distribution (Mar–Jun 2020):** Approximately 18,000 organizations downloaded and installed the malicious Orion updates (versions 2019.4 through 2020.2.1).
3. **Dormancy Period (14 days):** SUNBURST deliberately remained dormant for 14 days after installation to evade sandbox analysis systems that use short observation windows.
4. **DNS-Based C2 Beaconing:** SUNBURST encoded victim system identifiers in DNS subdomain queries to avsvmcloud.com, enabling APT29 to selectively identify high-value targets for hands-on exploitation.
5. **Selective Targeting (~100 orgs):** From the 18,000 initial infections, APT29 selected approximately 100 high-value organizations for active exploitation, deploying the TEARDROP second-stage payload.
6. **Discovery (Dec 8, 2020):** FireEye discovered the breach while investigating the theft of its own Red Team tools, a P1 incident that revealed the broader SolarWinds compromise.
:::

:::notes
The SolarWinds SUNBURST attack is the definitive modern case study in supply chain security, advanced persistent threat operations, and large-scale incident response. It demonstrates how a well-resourced nation-state threat actor (assessed with high confidence to be Russia's SVR foreign intelligence service, operating as APT29/Cozy Bear) can execute a years-long operation of extraordinary sophistication and patience.

The attack's elegance from an adversarial perspective was its early-stage compromise. By targeting the software build pipeline rather than individual victim organizations, APT29 ensured that the malicious code carried a valid SolarWinds digital code-signing certificate and was distributed through the same trusted update mechanism that IT administrators had been using for years. This made the SUNBURST backdoor effectively invisible to traditional endpoint security tools that trusted signed software from known vendors. The 14-day dormancy period was a deliberate evasion technique targeting automated malware sandboxes. Most sandbox environments analyze samples for 60–300 seconds; even extended sandboxes rarely run samples for more than 24 hours. SUNBURST's 14-day delay ensured that by the time it activated, any sandbox analysis had long since completed without identifying malicious behavior. The MITRE ATT&CK technique T1497.003 (Virtualization/Sandbox Evasion: Time Based Evasion) directly captures this pattern. The use of DNS for C2 communication was another sophisticated evasion choice. DNS traffic is rarely blocked and is difficult to distinguish from legitimate IT operations without deep packet inspection. SUNBURST encoded victim organization identifiers, host names, and selected configuration data into DNS subdomain labels, enabling APT29 to conduct reconnaissance on all 18,000 victims without establishing any direct TCP connections to attacker infrastructure. The incident had cascading national security implications: affected organizations included the U.S. Departments of Treasury, State, Commerce, and Homeland Security. The Microsoft, FireEye, and GoDaddy joint takedown of the avsvmcloud.com C2 domain in December 2020 was a landmark example of public-private sector incident response coordination. From an IR perspective, the breach demonstrated that even mature organizations with significant security investments (FireEye, a leading cybersecurity firm, was itself a victim) can be compromised by sufficiently advanced adversaries, reinforcing that detection and response capability is as important as prevention. The CISA Emergency Directive ED 21-01, issued December 13, 2020, required all U.S. federal agencies to immediately disconnect SolarWinds Orion systems, a real-world example of government-level containment execution. FireEye's SUNBURST analysis (December 13, 2020) remains the most comprehensive public technical account of the breach; its Appendix C lists the YARA rules used to detect SUNBURST.
:::

%%%
---
unit: CaseStudy
code: CS2
title: "Case Study: Colonial Pipeline Ransomware (2021)"
---
:::callout style=soft
The **Colonial Pipeline ransomware attack** (May 2021) demonstrated how a single compromised password for a legacy VPN account could trigger a six-day shutdown of critical fuel infrastructure, leading to fuel shortages across the U.S. East Coast and a $4.4 million ransom payment.
:::

:::image src="images/20_colonial_pipeline_case_study.png" alt="Timeline infographic showing key events of the Colonial Pipeline incident: May 6 credential theft via dark web, May 7 ransomware deployment and pipeline shutdown, May 8 FBI notification and executive briefing, May 12 restart of pipeline operations, May 13 DarkSide decryptor key received after ransom payment, with NIST IR phase labels aligned to each milestone" caption="Colonial Pipeline ransomware timeline: a credential compromise led to a six-day shutdown of 5,500 miles of pipeline infrastructure, demonstrating the physical consequences of IT-layer ransomware attacks." width=full
:::

:::table
| Factor | Detail |
|---|---|
| **Threat Actor** | DarkSide ransomware group (Eastern Europe, likely Russia-affiliated) |
| **Initial Access Vector** | Compromised VPN password for a legacy account (found in a leaked password database on the dark web), no MFA was enabled |
| **Systems Affected** | IT business systems; OT pipeline operations proactively shut down as a precaution |
| **Impact** | 5,500 miles of pipeline offline for 6 days; fuel shortages in 11 U.S. states; White House emergency declaration |
| **Ransom Paid** | $4.4 million in Bitcoin to DarkSide (75 Bitcoin) |
| **Ransom Recovered** | $2.3 million recovered by DOJ/FBI via seizure of DarkSide Bitcoin wallet |
| **Root Cause** | Lack of MFA on legacy VPN; inadequate network segmentation between IT and OT environments |
:::

:::notes
The Colonial Pipeline ransomware attack is the most consequential cybersecurity incident affecting U.S. critical infrastructure in recent history. It provides essential lessons about the real-world physical consequences of IT-layer compromises, the critical importance of multi-factor authentication, and the challenges of incident response in operational technology environments.

The initial access vector was startlingly simple: a single set of credentials for a legacy VPN account that was no longer in active use but had not been deprovisioned. These credentials were found in a batch of leaked passwords available on the dark web, likely from an unrelated prior breach of a service where the same password was reused. This is a textbook illustration of MITRE ATT&CK technique T1078 (Valid Accounts) and the compound risk of credential reuse combined with the absence of multi-factor authentication. The decision to shut down pipeline operations was made by Colonial Pipeline executives as a precautionary measure, the ransomware had encrypted IT business systems, and without confidence in the security state of the OT environment controlling the physical pipeline, they chose to halt operations rather than risk the integrity of pipeline controls. This decision, while defensible from a safety perspective, had enormous economic consequences and directly triggered emergency fuel shortage declarations across 11 states. The incident reveals a critical gap in many organizations' incident response planning: the IRP covered IT systems, but the company did not have a tested incident response plan for the OT environment that physically controls pipeline operations. NIST SP 800-82 Rev. 3 (Guide to OT Security) specifically addresses this gap, recommending that ICS/SCADA environments have dedicated incident response procedures and tested playbooks for cyber-physical attack scenarios. The Department of Justice's partial recovery of the ransom payment, $2.3 million of the original $4.4 million, through seizure of a DarkSide Bitcoin wallet was a landmark law enforcement action demonstrating that cryptocurrency ransom payments are not as untraceable as threat actors often claim. The DarkSide group disbanded shortly after the Colonial Pipeline attack, almost certainly due to political pressure following the White House's public attribution. The CISA and FBI joint advisory AA21-131A on DarkSide ransomware, published in May 2021, remains a valuable technical reference. The FBI discourages ransom payments because they incentivize further attacks and do not guarantee recovery, but an organization facing an operational shutdown that affects public services can face an impossible choice. This tension is central to the ransom-payment decision.
:::

%%%
---
unit: Frameworks
code: ATK
title: MITRE ATT&CK Integration in Incident Response
---
:::callout style=soft
**MITRE ATT&CK** is a globally accessible knowledge base of adversary tactics, techniques, and procedures (TTPs) derived from real-world observations, providing a common language for describing attacker behavior across the incident response lifecycle.
:::

:::image src="images/20_mitre_attack_integration.png" alt="MITRE ATT&CK matrix excerpt showing the first five tactic columns, Reconnaissance, Resource Development, Initial Access, Execution, Persistence, with three to four technique boxes per column, and colored highlights showing which techniques were observed in a hypothetical ransomware incident" caption="MITRE ATT&CK matrix integration: mapping observed incident techniques to the framework enables systematic detection coverage assessment and proactive threat hunting." width=full
:::

:::table
| ATT&CK Tactic | Example Technique | Incident Phase Applied | Detection Method |
|---|---|---|---|
| Initial Access (TA0001) | T1566.001, Spearphishing Attachment | Detection & Analysis | Email security gateway logs, EDR file creation events |
| Execution (TA0002) | T1059.001, PowerShell | Detection & Analysis | Windows Event ID 4104, EDR process tree |
| Persistence (TA0003) | T1547.001, Registry Run Keys | Detection & Analysis / Post-Incident | EDR registry monitoring, Autoruns tool output |
| Lateral Movement (TA0008) | T1550.002, Pass the Hash | Containment | Windows Event ID 4624 (Logon Type 3), NetFlow analysis |
| Exfiltration (TA0010) | T1041, Exfiltration Over C2 Channel | Containment / Eradication | NetFlow anomaly detection, proxy logs |
| Impact (TA0040) | T1486, Data Encrypted for Impact | Detection & Analysis | EDR file modification monitoring, Sysmon Event ID 11 |
:::

:::notes
The MITRE ATT&CK framework has transformed how incident responders document, communicate, and hunt for adversary behavior. Before ATT&CK, incident reports often described attacker techniques in idiosyncratic, organization-specific language that made cross-organizational intelligence sharing difficult. ATT&CK provides a standardized, structured vocabulary that allows a FireEye analyst, an FBI agent, and a CISO at a hospital system to discuss attacker techniques using the same terminology and IDs, dramatically improving the efficiency of threat intelligence sharing and incident coordination.

The framework was originally developed by MITRE's CISA-funded Federally Funded Research and Development Center (FFRDC) in 2013 and has grown to document hundreds of techniques across 14 tactics, spanning Windows, macOS, Linux, cloud environments, and even mobile platforms. The framework is continuously updated as new attacker techniques are observed and reported by the security research community. In the context of incident response, ATT&CK serves three primary functions. During Detection and Analysis, investigators map observed behaviors to ATT&CK techniques to identify what tactic the attacker was pursuing at each stage of the intrusion. This mapping transforms raw forensic observations into a structured attack narrative. During Containment, ATT&CK technique context informs containment decisions, knowing that the attacker used Pass-the-Hash (T1550.002) means that simply resetting the compromised account's password is insufficient; NTLM hash rotation and network monitoring for Pass-the-Hash lateral movement patterns are also required. During Post-Incident Activity, ATT&CK provides the vocabulary for the RCA report and enables the security team to translate observed techniques into specific detection engineering requirements. For example, observing T1059.001 (PowerShell) during the incident should trigger creation of a SIEM rule detecting encoded PowerShell execution using Windows Event ID 4104 (Script Block Logging). The ATT&CK Navigator, available at mitre-attack.github.io/attack-navigator, allows teams to visually map their detection coverage against the full ATT&CK matrix, identifying blind spots in their detection capabilities before an attacker exploits them. This exercise, sometimes called a "purple team assessment," is one of the most valuable preparation activities an organization can undertake. Loading a public threat-actor layer such as APT29 into the ATT&CK Navigator and overlaying a detection-coverage layer produces a "detection gap" view that makes visible which of that actor's techniques are undetected.
:::

%%%
---
unit: Frameworks
code: REG
title: Legal & Regulatory Notification Requirements
---
:::callout style=soft
Following a confirmed breach, organizations face a complex web of **legal notification obligations** that vary by jurisdiction, industry, and data type, failure to comply can result in fines exceeding tens of millions of dollars.
:::

:::image src="images/20_regulatory_notifications.png" alt="World map with notification requirement callout boxes labeled by region: GDPR covering EU countries at 72 hours to supervisory authority, HIPAA covering U.S. healthcare at 60 days, PCI DSS covering global payment card data with immediate notification to card brands, and U.S. state breach notification laws showing a patchwork of different timelines across all 50 states" caption="Global breach notification landscape: organizations operating across jurisdictions must comply simultaneously with multiple overlapping notification frameworks with varying timelines and content requirements." width=full
:::

:::table
| Regulation | Jurisdiction / Sector | Notification Timeline | Recipient | Penalty for Non-Compliance |
|---|---|---|---|---|
| **GDPR Article 33** | EU / All sectors processing EU personal data | 72 hours to supervisory authority | Data Protection Authority (DPA) | Up to €20M or 4% of global annual revenue |
| **GDPR Article 34** | EU / All sectors | Without undue delay | Affected data subjects (if high risk) | Up to €20M or 4% of global annual revenue |
| **HIPAA Breach Notification Rule** | U.S. Healthcare / Business Associates | 60 days | HHS Office for Civil Rights; affected individuals | Up to $1.9M per violation category per year |
| **PCI DSS v4.0 (Req. 12.10)** | Global / Payment card processors | Immediate (within 24 hours of detection) | Acquiring bank; card brands (Visa, Mastercard) | Fines from $5K–$100K/month; card processing termination |
| **U.S. State Laws (e.g., CCPA)** | U.S. California | Expedient / 72 hours (CPRA) | California AG; affected residents | Up to $7,500 per intentional violation |
| **SEC Cybersecurity Rule (2023)** | U.S. Publicly traded companies | 4 business days after determining materiality | Form 8-K disclosure to SEC | SEC enforcement action |
:::

:::notes
The legal notification landscape is one of the most complex elements of incident response for organizations operating across multiple jurisdictions. A multinational company experiencing a data breach may simultaneously be subject to GDPR notification requirements in the EU, HIPAA requirements in the U.S. healthcare sector, PCI DSS requirements for payment card data, and varying breach notification laws across all 50 U.S. states, each with different timelines, content requirements, and recipient lists. Navigating this complexity in real time during an active incident is why Legal Counsel is a core CSIRT member who must be engaged from the moment an incident is classified.

GDPR Article 33's 72-hour notification requirement is frequently misunderstood. The clock starts when the organization "becomes aware" of the breach, a threshold that has been interpreted by EU Data Protection Authorities (DPAs) as occurring when the organization has "a reasonable degree of certainty" that an incident has occurred. This is not the same as certainty: organizations cannot delay notification while investigating the full scope of the breach. The Article 33(4) provision allows for phased notifications, an initial notification within 72 hours with available information, followed by supplemental notifications as investigation progresses. The U.S. Securities and Exchange Commission's new cybersecurity disclosure rule, adopted in July 2023 (17 CFR Parts 229 and 249), created a significant new obligation for publicly traded companies: material cybersecurity incidents must be disclosed in Form 8-K within four business days of determining that the incident is material. "Material" in the securities law context means information that a reasonable investor would consider important, a definition that covers many significant data breaches. This rule has already driven multiple high-profile public disclosures, including MGM Resorts International's 8-K filing following its September 2023 breach. HIPAA's 60-day notification window is the most permissive major notification timeline, reflecting the complexity of healthcare breaches involving PHI and the need for thorough investigation before notification. However, HIPAA also requires notification to HHS within 60 days of year-end for breaches affecting fewer than 500 individuals, these smaller breaches can accumulate to significant aggregate reporting obligations. The breach-notification timelines are maximum windows, not targets; delayed notification is routinely treated as an aggravating factor in regulatory enforcement. Best practice is to notify as soon as the material facts are known and supplement as more is learned, and organizations that notify promptly and cooperate consistently receive more favorable outcomes.
:::

%%%
---
unit: Comparison
code: CMP
title: "IR vs. DR vs. BCP: Understanding the Differences"
---
:::callout style=soft
**Incident Response (IR)**, **Disaster Recovery (DR)**, and **Business Continuity Planning (BCP)** are complementary but distinct disciplines, organizations need all three, and they must be integrated to function effectively during a major disruption.
:::

:::image src="images/20_ir_dr_bcp_comparison.png" alt="Three overlapping circles forming a Venn diagram: the left circle labeled Incident Response focuses on threat containment and eradication, the center overlap area shows shared activities like executive communication and damage assessment, the right circle labeled Disaster Recovery focuses on IT system restoration, and a surrounding outer ring labeled Business Continuity Planning encompasses all three as the strategic framework" caption="IR, DR, and BCP relationship: three complementary disciplines that must be integrated to manage the full spectrum of organizational disruptions from detection through full operational restoration." width=full
:::

:::table
| Dimension | Incident Response (IR) | Disaster Recovery (DR) | Business Continuity Planning (BCP) |
|---|---|---|---|
| **Primary Focus** | Containing and eradicating active security threats | Restoring IT systems and data after disruption | Maintaining business operations during any disruption |
| **Trigger** | Confirmed or suspected security incident | IT system failure (cyber, natural disaster, hardware) | Any event threatening business operations |
| **Time Horizon** | Hours to days (immediate response) | Hours to weeks (system restoration) | Days to months (sustained operations) |
| **Governing Standard** | NIST SP 800-61 Rev. 2 | ISO/IEC 27031; NIST SP 800-34 | ISO 22301 (Business Continuity Management) |
| **Key Metric** | Mean Time to Detect (MTTD); Mean Time to Respond (MTTR) | Recovery Time Objective (RTO); Recovery Point Objective (RPO) | Maximum Tolerable Period of Disruption (MTPD) |
| **Primary Owner** | CISO / Security Operations | CTO / IT Operations | COO / Enterprise Risk Management |
:::

:::notes
Students frequently conflate incident response, disaster recovery, and business continuity planning because all three address organizational resilience to disruptive events. Understanding the distinctions, and the critical integration points between them, is essential for designing mature organizational security programs.

Incident Response is the most narrowly scoped of the three. It is focused specifically on security events: unauthorized access, malware infections, data breaches, and similar threats. The IR process prioritizes security objectives: containing the threat, preserving evidence, and eradicating the attacker. Disaster Recovery is broader in scope, it addresses IT system restoration following any type of disruption, not just security incidents. DR planning defines Recovery Time Objectives (RTOs, how quickly systems must be restored) and Recovery Point Objectives (RPOs, how much data loss is acceptable). A common RTO for a critical financial system might be four hours; a common RPO might be 15 minutes, requiring near-real-time database replication. Business Continuity Planning is the broadest of the three frameworks. BCP ensures that essential business processes can continue operating during any disruption, even if IT systems are partially unavailable. BCP might activate manual workarounds for processes that normally run on automated systems, or relocate critical operations to an alternate facility. The three disciplines must be integrated to function effectively during major incidents. Consider the Colonial Pipeline attack: the IR team needed to contain and eradicate the ransomware (IR), IT needed to restore business systems from backups (DR), and the company needed to manage fuel delivery operations manually and coordinate with the government during the six-day outage (BCP). If these three programs operate in isolation, the gaps between them become critical failure points during real events. ISO 22301 (Business Continuity Management Systems) provides the international standard for BCP, while ISO/IEC 27031 (Guidelines for Information and Communication Technology Readiness for Business Continuity) bridges BCP and IT disaster recovery. NIST SP 800-34 Rev. 1 (Contingency Planning Guide for Federal Information Systems) provides equivalent guidance for U.S. government environments. The boundary between incident response, disaster recovery and business continuity is clearest by example: a ransomware attack encrypting HR systems is primarily incident response; a flood destroying primary infrastructure is disaster recovery; a key vendor going bankrupt and discontinuing a critical service is business continuity. The three disciplines hand off to each other.
:::

%%%
---
unit: Metrics
code: MET
title: IR Metrics, MTTD, MTTR, and MTTRe
---
:::callout style=soft
**Incident response metrics** translate the quality of security operations into measurable data that drives continuous improvement and enables benchmarking against industry standards.
:::

:::image src="images/20_ir_metrics.png" alt="Timeline diagram showing a security incident from compromise to full recovery with labeled measurement intervals: MTTD spanning from compromise to detection, MTTR spanning from detection to containment, and MTTRe spanning from containment to full recovery, with industry benchmark ranges annotated below each span" caption="MTTD, MTTR, and MTTRe: the three primary incident response metrics that quantify detection capability, response speed, and recovery effectiveness." width=full
:::

:::list style=plain
- **MTTD (Mean Time to Detect):** Average time from the initial compromise to discovery by the security team. Industry benchmark: organizations with mature security programs average 16 days (IBM Cost of a Data Breach 2023); global average is 204 days.
- **MTTR (Mean Time to Respond):** Average time from detection to initial containment actions. Mature SOCs target sub-1-hour MTTR for P1 incidents.
- **MTTRe (Mean Time to Recover):** Average time from containment to full restoration of normal operations. Ranges from hours (isolated malware) to months (major ransomware or supply chain attack).
- **False Positive Rate:** Percentage of alerts that are not actual incidents. High false positive rates (>90%) indicate tuning needs and analyst fatigue risk.
- **Incidents per Month by Severity:** Trend data revealing changes in threat volume, enabling proactive resource planning.
:::

:::callout style=soft
According to IBM's Cost of a Data Breach Report 2023, organizations that identified and contained a breach in under 200 days saved an average of $1.02 million compared to those that took longer. Every hour of improvement in MTTD and MTTR has direct financial impact.
:::

:::notes
Security metrics are the mechanism by which the CSIRT transforms subjective assessments ("our detection is getting better") into objective, evidence-based performance data. Without metrics, security programs cannot demonstrate improvement to leadership, cannot identify which investments are delivering results, and cannot benchmark their capabilities against industry peers. Metrics also create accountability, when MTTD and MTTR targets are published and tracked, there is organizational pressure to achieve them.

Mean Time to Detect (MTTD) is the most critical leading indicator of security program maturity. The industry-wide average MTTD of 204 days (IBM Cost of a Data Breach Report 2023) is a sobering benchmark: it means that the average compromised organization is operating normally, serving customers and processing transactions, for nearly seven months before anyone realizes an attacker is present. This extended dwell time allows attackers to conduct thorough reconnaissance, identify the most valuable data repositories, and establish multiple redundant persistence mechanisms that make eradication more complex. Organizations with mature security programs, characterized by comprehensive SIEM deployment, EDR coverage, and active threat hunting programs, achieve MTTD of 16 days or less, a 12x improvement that translates directly into reduced breach costs. Mean Time to Respond (MTTR) is a measure of operational efficiency: once an incident is detected, how quickly can the CSIRT execute containment actions? The target for P1 (Critical) incidents in well-resourced organizations is typically under one hour from detection to initial containment, meaning that CSIRT response procedures must be thoroughly documented, practiced, and executable without the delays of improvised decision-making. Achieving sub-hour MTTR for P1 incidents requires pre-approved response playbooks that eliminate the need for management approval before taking standard containment actions such as isolating a compromised host. Mean Time to Recover (MTTRe) measures the complete restoration of normal operations. For simple malware infections on isolated endpoints, MTTRe might be measured in hours. For major ransomware attacks affecting enterprise-wide systems, MTTRe can stretch to weeks, the 2019 Norsk Hydro ransomware attack took months to fully recover from, costing the company approximately $71 million. The False Positive Rate is a critical but often overlooked operational metric. Most enterprise SIEM deployments generate alert noise ratios of 90–97% false positives, meaning analysts spend the majority of their time investigating benign events. Alert fatigue from high false positive rates has been directly implicated in real-world breach failures: the 2013 Target breach included FireEye alerts that analysts dismissed during triage because the system was generating an overwhelming volume of notifications. IBM benchmark data indicates organizations save roughly $1.02 million per breach by bringing the detection-to-containment window below 200 days, which gives a per-day value for reducing mean time to detect and an intuitive sense of the return on monitoring investment.
:::

%%%
---
unit: Lifecycle
code: CHK2
title: "Mid-Lecture Checkpoint: Containment Through Metrics"
---
:::callout style=soft
Check your understanding of the operational phases and measurement of incident response before the synthesis walkthrough.
:::

:::image src="images/20_checkpoint_containment_metrics.png" alt="Six-question quiz card layout with questions covering containment strategies, eradication procedures, memory forensics, legal notification timelines, MITRE ATT&CK usage, and IR metrics, each with a response area below" caption="Checkpoint: consolidate your understanding of containment, eradication, and IR metrics before the synthesis walkthrough." width=full
:::

:::list style=plain
**Answer these questions before moving forward:**
- What is the difference between short-term and long-term containment as defined in NIST SP 800-61?
- Why is rebuilding a system from a clean image preferred over in-place malware removal during eradication?
- What is the "order of volatility" and how does it affect evidence collection sequencing?
- Under GDPR Article 33, when does the 72-hour notification clock begin?
- Name three MITRE ATT&CK tactics that are typically observable before a ransomware payload is deployed.
- What does MTTD measure, and what is the global industry average as of IBM's 2023 report?
:::

:::callout style=soft
If you cannot answer four or more of these questions confidently, review slides CON through MET before proceeding to the full lifecycle walkthrough.
:::

:::notes
This second checkpoint consolidates the operational and measurement content from the middle section of the lecture before students encounter the synthesis walkthrough. The questions are deliberately constructed to test not just recall but also application, for example, understanding when the GDPR notification clock begins requires students to understand the legal definition of "becomes aware," not just memorize a number. Similarly, the MITRE ATT&CK question requires students to apply the framework to a specific scenario rather than simply recite tactic names.

Working through the expected answers: Short-term containment in NIST SP 800-61 involves immediate actions to limit damage, typically isolating affected systems from the network. Long-term containment involves more durable measures implemented while eradication is being prepared, such as deploying temporary monitoring controls, hardening adjacent systems, and closing the vulnerability class used for initial access. Regarding rebuilding versus in-place cleaning: cleaning attempts are unreliable because sophisticated malware may persist in firmware, kernel modules, boot sectors, or deeply nested registry locations that cleaning tools miss. Rebuilding from a verified clean gold image guarantees the complete removal of all malicious code. The order of volatility ranks evidence by how quickly it disappears: CPU registers and cache → RAM → network connections → running processes → disk → logs → physical media. This ordering determines the sequence of evidence collection, RAM must be captured before disk imaging. The GDPR 72-hour clock begins when the organization "becomes aware" of the breach, interpreted by EU DPAs as when the organization has a reasonable degree of certainty that an incident involving personal data has occurred. It does not require certainty about the full scope. The three ATT&CK tactics observable before ransomware deployment typically include Initial Access (TA0001), Lateral Movement (TA0008), and Exfiltration (TA0010), most modern ransomware groups exfiltrate data before encrypting to enable double-extortion. MTTD is the Mean Time to Detect, the average time from initial compromise to discovery. The IBM 2023 global average is 204 days.
:::

%%%
---
unit: Misconceptions
code: FAQ
title: "Common Misconceptions About Incident Response"
---
:::callout style=soft
Several persistent myths about incident response lead organizations to underinvest in preparation and make suboptimal decisions during active incidents. Correcting these misconceptions is essential for sound security program design.
:::

:::image src="images/20_ir_misconceptions.png" alt="Six myth-vs-reality card pairs arranged in a two-column grid, each card showing a red X over the myth statement and a green checkmark over the corrected reality statement, covering topics including small business risk, antivirus sufficiency, paying ransoms, IR only being a technical function, breach equating to failure, and the sufficiency of backups alone" caption="Incident response misconceptions: six common myths that lead organizations to underinvest in or mismanage their response capabilities." width=full
:::

:::table
| Misconception | Reality |
|---|---|
| "We're too small to be a target." | 43% of cyberattacks target small businesses (Verizon DBIR 2023). Automated attacks do not discriminate by organization size. |
| "Our antivirus will catch everything." | Fileless malware, living-off-the-land techniques, and zero-day exploits routinely bypass signature-based AV. EDR and behavioral detection are required. |
| "Paying the ransom quickly resolves the incident." | FBI reports that 20% of victims who pay ransoms never receive a working decryption key. Payment also funds future attacks and does not address root cause. |
| "Incident response is just an IT problem." | Effective IR requires Legal, PR, HR, Executive leadership, and Finance involvement. The communications and regulatory dimensions are non-technical. |
| "A breach means our security team failed." | The NIST framework assumes breach is possible regardless of controls. IR effectiveness, not breach prevention alone, is the measure of security program maturity. |
| "If we have backups, we don't need an IR plan." | Backups support the recovery phase only. Without containment and eradication, restoring from backup into an attacker-controlled environment re-introduces the threat. |
:::

:::notes
Addressing common misconceptions about incident response is a critical component of security awareness at all organizational levels. These myths are not harmless, they translate directly into underinvestment in preparation, delayed escalation during active incidents, and poor decision-making under pressure.

The "too small to be a target" misconception is perhaps the most dangerous for small and medium businesses. Modern ransomware operations are largely automated: attackers use vulnerability scanners and credential stuffing tools to identify exploitable systems at internet scale, selecting victims based on vulnerability and ability to pay rather than organizational prominence. The Ryuk ransomware group, for example, was attributed with attacks on small hospitals, school districts, and local government agencies, organizations that attackers specifically targeted because they had limited security resources but high motivation to restore operations quickly. The antivirus misconception reflects a genuinely outdated security model. Signature-based antivirus, which dominated the endpoint security market for decades, detects known malware by matching file content against a database of malicious signatures. This approach is completely ineffective against fileless malware (which never writes to disk), living-off-the-land attacks (which repurpose legitimate system tools), and novel zero-day exploits (which have no existing signatures). The CrowdStrike Global Threat Report 2023 found that 71% of attacks observed involved malware-free techniques that bypass AV detection entirely. The ransom payment misconception deserves detailed treatment. Beyond the FBI's guidance that 20% of victims who pay never receive working decryption, there are several additional considerations: payment establishes the organization as a willing payer, making it a priority re-attack target; in some jurisdictions, paying ransoms to sanctioned entities may violate OFAC (Office of Foreign Assets Control) regulations, creating legal liability; and the root vulnerability that enabled the attack still exists after payment, leaving the organization exposed. The Sophos State of Ransomware 2023 report found that organizations that paid ransoms spent an average of $750,000 on recovery costs in addition to the ransom itself, compared to $375,000 for organizations that refused to pay, demonstrating that payment does not actually simplify recovery. The backup misconception is particularly insidious because it contains a grain of truth. Backups are essential and reduce the consequences of ransomware significantly. However, they only address the data destruction component of the attack. The attacker's access, the exploited vulnerability, and any established persistence mechanisms all remain active even after a successful backup restoration. Without containment and eradication, an organization that restores from backup without cleaning the environment will find itself re-encrypted within hours.
:::

%%%
---
unit: Synthesis
code: IRW
title: Incident Response Walkthrough
---
:::image src="images/20_ransomware_walkthrough.png" alt="Horizontal timeline diagram tracing a ransomware incident through the six NIST IR phases, with labeled milestones showing EDR alert, host isolation, drive wipe, backup restoration, and RCA completion, and forensic evidence callout boxes at each phase" caption="Ransomware incident walkthrough: a complete NIST lifecycle trace from EDR detection through post-incident RCA, showing evidence collected and actions taken at each phase." width=full
:::

:::table
| NIST Phase | Scenario Step (Symmetric Cryptographic Ransomware) | Action Taken by CSIRT | Forensic Evidence Preserved |
|---|---|---|---|
| **Preparation** | Baseline configuration active; offsite backups configured. | Pre-positioning EDR agents and backup infrastructure. | Secure gold images and configuration logs. |
| **Detection & Analysis** | EDR alerts on unauthorized bulk file encryption. | Analyst triages alert, confirms active ransomware, scopes affected hosts. | Volatile RAM image; Sysmon process creation logs. |
| **Containment** | Ransomware attempts lateral movement over SMB. | CSIRT isolates host network connections via switch configuration. | Firewall connection logs; active network sockets. |
| **Eradication** | Malware is isolated but remains on system disk. | Wiping host drives and rebuilding systems from trusted baselines. | Corrupt or encrypted disk sectors for analysis. |
| **Recovery** | Restoring business applications and services. | Restoring files from offsite backups; implementing enhanced EDR monitoring. | Backup integrity validation logs. |
| **Post-Incident** | IRP review and security control updates. | Conducting lessons-learned review and updating security baselines. | Root Cause Analysis (RCA) report. |
:::

:::notes
This walkthrough illustrates the incident response lifecycle in a ransomware scenario. In the preparation phase, the team has EDR agents deployed and offline backups configured. During detection, the EDR flags unauthorized file encryption. The analyst triages this alert and confirms the incident.

In the containment phase, the team isolates the affected hosts from the network, blocking lateral movement. Next, eradication is executed by wiping the drives and rebuilding the systems from clean images. During recovery, files are restored from backups, and enhanced monitoring is implemented to verify the system is secure. Finally, in the post-incident phase, the team reviews the response and updates security controls, completing the lifecycle.

The ransomware scenario in this table reflects a pattern commonly documented in FBI and CISA joint cybersecurity advisories. The Conti ransomware group, before its 2022 dissolution, was attributed with attacks on over 400 organizations globally using a playbook that closely mirrors the phases shown here: initial access via phishing or vulnerability exploitation, lateral movement using Cobalt Strike and legitimate admin tools, data exfiltration prior to encryption, and finally deployment of a symmetric AES-256 encryption routine that made file recovery impossible without the key. The NIST phases map specifically to the ATT&CK tactics observed: Initial Access (TA0001), Execution (TA0002), and Lateral Movement (TA0008) occur before detection; Exfiltration (TA0010) and Impact (TA0040) occur if containment is delayed. This walkthrough demonstrates that the value of immutable, offline backups is not theoretical, it is the single most effective recovery control against ransomware. CISA's advisory AA23-061A on Royal ransomware and the FBI's advisory on Hive ransomware both confirm that organizations with tested backup restoration procedures recovered significantly faster than those without. The forensic evidence preserved at each phase, RAM images, network logs, and Sysmon process trees, directly informs the eradication strategy and the post-incident RCA report.
:::

%%%
---
unit: Summary
code: SUM
title: Class 20 Review & Defense-in-Depth
---
:::pullquote
"Incident response is the ultimate validation of an organization's defense-in-depth architecture. Preparation and structured handling determine how successfully a threat is contained."
:::

:::image src="images/20_defense_in_depth_summary.png" alt="Concentric circle diagram showing defense-in-depth layers: Preparation at the outer ring, Detection and Analysis in the second ring, Containment Eradication and Recovery in the third ring, and Post-Incident Activity at the center, with NIST SP 800-61 labeled as the governing framework" caption="Defense-in-depth through incident response: each lifecycle phase adds a layer of organizational resilience, with lessons learned continuously hardening the outer rings." width=full
:::

:::list style=chips
- NIST SP 800-61 Rev. 2 Framework
- Incident vs. Event Distinction
- CSIRT Team Coordination & Communication
- Volatile Evidence Preservation (RAM)
- Cycle of Continuous Feedback & Lessons Learned
:::

:::notes
To wrap up Class 20, remember that incident response is a structured process for managing security breaches. While host hardening and access controls reduce vulnerability, an effective security strategy must plan for the possibility of compromise.

By implementing the NIST SP 800-61 Rev. 2 framework, coordinating the CSIRT, isolating threats during containment, and conducting lessons-learned reviews, organizations can manage security incidents and maintain operational resilience.

This concludes our module on host-level security and incident response. In our next module, Class 21, we will shift focus to application security, examining how to design and build software that resists attacks from the ground up.

The NIST SP 800-61 Rev. 2 framework is not the only available incident response standard. Organizations in specific sectors may reference complementary frameworks: ISO/IEC 27035-1:2023 (Information Security Incident Management) provides an internationally recognized standard aligned with ISO/IEC 27001; SANS Institute's PICERL model (Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned) is widely taught in practitioner training; and CISA Federal Incident Notification Guidelines specify mandatory reporting timelines for U.S. federal agencies. The lifecycle feedback loop covered in this class is measurable through key incident response metrics: Mean Time to Detect (MTTD), Mean Time to Respond (MTTR), and Mean Time to Recover. IBM's Cost of a Data Breach Report 2023 found that organizations with fully deployed security AI and automation reduced breach costs by an average of $1.76 million. Regulatory consequences for inadequate incident response continue to grow: GDPR Article 83 allows fines of up to €20 million or 4% of global annual revenue for failure to notify supervisory authorities of a breach within 72 hours. The skills developed in this incident response module, from CSIRT coordination to forensic evidence preservation, are foundational for the CompTIA Security+, CySA+, and (ISC)² CISSP certifications, in which incident response is a major examination domain. In Class 21, we will apply defense-in-depth principles to the application layer, examining secure software development and web application security.
:::
