---
deck:
  title: Physical Security
  kicker: Class 10
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 10
  description: The overlooked layer of security, locks, badges, theft, tampering, and environmental controls.
  topics: [Physical Vulnerabilities, Unauthorized Access, Theft, Tampering, Environmental Controls]
---

---
title: Physical Security
cover: true
---
:::text class=sub
No firewall stops someone who can simply walk up and unplug the server
:::
:::image src="images/10_physical_security_overview.png" alt="Concentric zone diagram of a secured facility: outer perimeter fence, building entry checkpoint, secure server room, and individual device cabinet at the center, each zone labeled with example controls" caption="Physical security is a layered discipline, each concentric zone must hold independently so that no single failure grants an attacker access to the core" width=full
:::
::::columns
::col::
:::list heading="Core Threats" style=plain
- Unauthorized Access
- Tampering
- Theft
- Vandalism
- Environmental Hazards
:::
::col::
:::list heading="Key Defenses" style=plain
- Access Control Systems
- Surveillance & Monitoring
- Environmental Controls
- Secure Facility Design
- Incident Response Procedures
:::
::col::
:::callout style=soft
Physical security is the foundation of all other security domains. Without it, digital safeguards such as firewalls, encryption, and intrusion detection systems become irrelevant.
:::
::::
:::notes
Physical security refers to the protection of tangible assets including hardware, facilities, and personnel from unauthorized access, damage, or disruption. Unlike logical or network security, which focuses on protecting data in transit or at rest through cryptographic or software-based mechanisms, physical security addresses threats that exploit real-world vulnerabilities, such as an intruder physically accessing a server room or stealing a laptop.

The statement "No firewall stops someone who can simply walk up and unplug the server" illustrates a fundamental principle: layered defense must include both cyber and physical controls. Firewalls, intrusion detection systems (IDS), and endpoint protection are rendered ineffective if an attacker gains direct physical access to critical infrastructure. This concept aligns with NIST Special Publication 800-116, which emphasizes the importance of securing physical access to information systems as part of a comprehensive security framework.

Common physical threats include unauthorized entry (e.g., tailgating or using stolen credentials), hardware tampering (such as insertion of USB devices for malicious purposes), theft of devices containing sensitive data (as seen in many CVEs related to unencrypted storage), and environmental hazards like fire or flooding. ISO/IEC 27001 and NIST SP 800-53 provide detailed guidance on implementing physical access controls, environmental monitoring, and incident response procedures to mitigate these risks.

Effective physical security strategies often involve multiple overlapping layers, including perimeter fencing, biometric access controls, surveillance systems, secure locking mechanisms, and trained security personnel. These measures must be integrated with organizational policies and regularly audited to ensure compliance and resilience against evolving threats.

The importance of physical security is further underscored by real-world incidents where its absence led to significant breaches. For example, in 2014, attackers physically accessed a secure area at a financial institution by tailgating an employee, subsequently installing a hardware device that enabled months of covert data exfiltration, an intrusion that bypassed all network-layer defenses entirely. CompTIA Security+ SY0-701 explicitly includes physical security as a core domain, reflecting industry consensus that no cybersecurity program is complete without addressing tangible, location-based threats. Organizations that treat physical security as secondary to logical controls create a foundational vulnerability that sophisticated adversaries are well-prepared to exploit.
:::

%%%

---
unit: Foundations
code: PHY
title: Why Physical Security Matters
---

::::columns
::col::
:::callout style=soft
If an attacker can physically touch a device, almost every digital protection on it becomes far easier to bypass.
:::

::col::
:::pullquote
"If they can touch it, they can own it."
:::
::::

:::image src="images/10_physical_attack_vectors.png" alt="Labeled diagram of a laptop showing physical attack entry points: RAM slots (cold boot attack), USB/Thunderbolt ports (DMA attack), BIOS chip (firmware tampering), keyboard connector (hardware keylogger), and SPI flash (bus probing)" caption="Modern computing hardware has multiple physical attack surfaces, each represents a vector that bypasses operating system and software-layer defenses entirely" width=full
:::

:::list heading="Examples of Physical Access Attacks" style=plain
- Cold boot attacks to extract encryption keys from RAM
- DMA attacks via Thunderbolt or PCIe ports
- JTAG debugging to bypass boot protections
- Side-channel analysis (e.g., power, EM emissions)
- Hardware implant installation
:::

:::table
| Attack Vector         | Digital Equivalent        | Physical Requirement       |
|-----------------------|----------------------------|----------------------------|
| Cold Boot             | Memory scraping            | Direct RAM access          |
| USB Drop Attack       | Social engineering + malware | Unattended system access   |
| Evil Maid             | Privilege escalation       | Physical access + time     |
| Bus Probing (e.g., SPI)| Firmware dumping           | Board-level access         |
| Bootkit Installation  | Rootkit deployment         | Pre-boot system access     |
:::

:::notes
Physical security forms the foundational layer of any comprehensive security architecture. While much of cybersecurity focuses on logical controls, authentication, encryption, network segmentation, these mechanisms can be rendered ineffective if an adversary gains physical access to computing systems. This principle is well-documented in NIST Special Publication 800-12, "An Introduction to Computer Security," which emphasizes that physical protection is a prerequisite for maintaining logical safeguards.

When attackers have physical access, they can exploit hardware-level vulnerabilities that are otherwise shielded by software-based defenses. For example, cold boot attacks (CVE-2008-0850) allow adversaries to extract cryptographic keys from volatile memory shortly after power loss. Similarly, Direct Memory Access (DMA) attacks exploit high-speed I/O interfaces like Thunderbolt to bypass operating system protections and directly read from or write to system memory.

The concept aligns with the MITRE ATT&CK framework's "Physical Access" technique (T1200), which highlights how adversaries leverage proximity to deploy malicious payloads or extract sensitive data. ISO/IEC 27001 also mandates physical security controls under Annex A, specifically A.11, to protect information assets from unauthorized physical access, damage, or interference.

Ultimately, physical security is not just about locks and cameras, it is about preserving the integrity of the entire digital security stack. Without it, even the strongest encryption and access controls become theoretical.

The practical implications are significant: a determined attacker with fifteen minutes of unmonitored physical access to a workstation can install a hardware keylogger, clone a drive, extract RAM contents, or plant a persistent firmware-level backdoor, all without leaving a trace in any software log. This is why NIST SP 800-53 Control PE-3 (Physical Access Control) mandates that organizations enforce physical access authorizations at all entry points to facilities containing information systems, and why CompTIA Security+ emphasizes physical controls as a foundational domain alongside network and application security. Physical security is not a niche concern, it is the precondition for every other security control working as intended.
:::

%%%

---
unit: Vulnerabilities
code: VUL
title: Physical Vulnerabilities
---
::::columns
::col::
:::list heading="Common Physical Weak Points" style=plain
- Unlocked doors or propped-open secure areas
- Exposed network ports in public or unsupervised areas
- Unattended, unlocked computers
- Visible passwords written on sticky notes
:::
::col::
:::callout style=soft
Physical vulnerabilities often represent the weakest link in an organization's security posture due to human error, convenience trade-offs, and inadequate enforcement of access control policies.
:::
::::

:::image src="images/10_common_vulnerabilities.png" alt="Four-panel illustration of common physical vulnerabilities: panel 1 shows a propped-open secure door; panel 2 shows an exposed RJ45 network port in a public hallway; panel 3 shows an unattended unlocked laptop; panel 4 shows a sticky note on a monitor with a written password" caption="Physical vulnerabilities are often created by human behavior, not hardware failure, convenience decisions that bypass security controls are among the most exploited attack surfaces in enterprise environments" width=full
:::

:::notes
Physical vulnerabilities refer to exploitable weaknesses in the tangible environment of an organization, including facilities, hardware, and human behavior, that can be leveraged to gain unauthorized access or cause harm. These vulnerabilities are often easier to exploit than digital ones because they typically require no specialized tools or technical expertise. Instead, they rely on opportunity, social engineering, or simple negligence.

Examples include doors left unlocked or propped open, which violate physical access controls outlined in standards such as NIST Special Publication 800-116 and ISO/IEC 27001 Annex A.11. Similarly, exposed network ports in public areas allow attackers to directly connect to internal networks, bypassing perimeter defenses. This is especially problematic in environments where network access control (NAC) or port security mechanisms are not implemented, as referenced in RFC 3162 and IEEE 802.1X standards.

Unattended, unlocked workstations are another frequent issue, enabling what is known as "tailgating" or "shoulder surfing" attacks. These are addressed in part by user awareness training and technical controls like automatic screen locking, as recommended by NIST SP 800-63B. Additionally, passwords written on sticky notes or stored insecurely violate basic authentication security principles and are frequently cited in incident reports and CVE entries related to insider threats and social engineering.

These vulnerabilities underscore the importance of layered physical security frameworks, integrating both procedural safeguards and technical controls to reduce risk.

Addressing physical vulnerabilities requires both technical enforcement and cultural change. Technical mitigations include deploying Network Access Control (NAC) systems that reject unauthenticated devices connected to exposed ports, enforcing mandatory screen lock policies via Group Policy or MDM (Mobile Device Management), and installing door sensors that alert security operations if a secure door is held open beyond a threshold time. However, technology alone is insufficient if employees routinely prop doors open for convenience or write credentials in visible locations. This is why ISO/IEC 27001 Annex A.7 (Human Resource Security) and NIST SP 800-50 (Building an Information Technology Security Awareness and Training Program) both emphasize security awareness training as an essential complement to physical controls. A single employee who holds the door for a stranger because it seemed impolite not to can invalidate thousands of dollars in access control infrastructure, making human behavior one of the most critical variables in physical security programs.
:::

%%%

---
unit: Access
code: ACC
title: Unauthorized Access
---
:::callout style=soft
**Tailgating**, also known as **piggybacking**, is a physical security breach technique in which an unauthorized individual follows an authenticated person into a restricted area without presenting valid credentials.
:::

:::image src="images/10_tailgating_prevention.png" alt="Side-by-side diagram: left panel shows the tailgating attack (unauthorized person following an authorized badge-holder through a door); right panel shows prevention controls (mantrap airlock, turnstile, anti-passback sensor, and a sign reminding employees to challenge unknown individuals)" caption="Tailgating exploits social courtesy and the physical design of standard doorways, prevention requires both hardware barriers and a trained security culture" width=full
:::

:::list heading="Common Tailgating Scenarios" style=plain
- An attacker waits near a secured entry point and enters immediately after an authorized individual uses their access card.
- The intruder may carry items that appear to hinder their movement, prompting the authorized person to hold the door.
- In some cases, the attacker may impersonate delivery personnel or maintenance staff to gain trust.
- Credential cloning, social engineering, or borrowing another person's badge are also forms of unauthorized access leveraging tailgating principles.
:::

::::columns
::col::
:::table
| Technique        | Description                                       | Risk Level |
|------------------|---------------------------------------------------|------------|
| Passive Tailgating | Intruder simply walks in behind an authorized user | Medium     |
| Active Tailgating  | Intruder engages with the user to encourage door holding | High       |
| Credential Misuse  | Using stolen, cloned, or borrowed access cards     | Critical   |
:::
::col::
:::steps heading="Prevention Strategies"
1. Deploy anti-passback systems to detect multiple entries without exit logging.
2. Install turnstiles, mantraps, or optical token readers at entry points.
3. Conduct regular security awareness training emphasizing challenge protocols.
4. Enforce a "challenge politely" policy for all personnel.
5. Monitor access logs and use video surveillance for anomaly detection.
:::
::::

:::notes
Tailgating represents a significant vulnerability in physical access control systems because it exploits human behavior rather than technical flaws. It is a low-tech, high-effectiveness method used by attackers to bypass perimeter defenses without requiring tools or specialized knowledge. This technique is particularly effective in environments where employees are not trained to recognize or respond to unauthorized access attempts.

From a security framework perspective, tailgating directly violates principles outlined in **NIST Special Publication 800-116**, which emphasizes the importance of identity verification and access control enforcement. Similarly, **ISO/IEC 27001** requires organizations to implement physical security perimeters and access controls to protect sensitive information and assets.

Tailgating can be categorized into two types: **passive** and **active**. Passive tailgating occurs when an unauthorized person simply follows an authorized individual through a secured entry without interaction. Active tailgating involves the intruder engaging with the authorized person, often through social manipulation, to encourage them to hold the door open.

Organizations often underestimate the risk associated with tailgating, yet it has been a contributing factor in numerous real-world breaches, including insider threats and targeted attacks. For example, in **CVE-2021-34792**, a vulnerability in certain access control systems allowed for credential bypass, which could be exploited in conjunction with tailgating to gain deeper physical access.

Effective countermeasures include implementing physical barriers such as mantraps or turnstiles, deploying access control systems with anti-passback capabilities, and conducting continuous security awareness training. Employees must be trained to understand that holding a door for a stranger is not a courtesy, it is a potential security failure. A culture of verification, supported by policy and technology, is essential to mitigate this persistent threat.

The anti-passback control deserves particular emphasis as a technical countermeasure. Anti-passback systems enforce a logical rule that a credential cannot be used to enter a secured area twice in sequence without a corresponding exit event, meaning a tailgater who follows someone through a door cannot then use their own credential at an inner checkpoint without triggering an alert. NIST SP 800-116 specifically recommends anti-passback as a mechanism for detecting and deterring unauthorized entry in federal facilities. When combined with video surveillance correlation and access log auditing, anti-passback creates a technical record of anomalous entry patterns that security personnel can review and investigate, transforming a physical control into a detective mechanism as well as a preventive one.
:::

%%%

---
unit: Theft
code: THF
title: Theft
---
:::list heading="What's actually at risk" style=plain
- The device itself, replaceable, but not free
- The data stored on it, often far more valuable than the hardware
- Documents left in the open, or recoverable from the trash ("dumpster diving")
- Removable media (USB drives, external HDDs), easily misplaced or stolen
- Credentials or tokens left unsecured on desks or in common areas
:::

:::pullquote
A stolen laptop is a hardware loss. An unencrypted stolen laptop is a data breach.
:::

:::image src="images/10_theft_impact_chain.png" alt="Chain diagram showing theft impact progression: physical theft of device → attacker gains access to unencrypted data → credential and identity extraction → lateral access to corporate systems → regulatory breach notification required under GDPR/HIPAA → financial and reputational consequences" caption="The impact of device theft extends far beyond hardware replacement cost, an unencrypted stolen device initiates a chain of data exposure consequences" width=full
:::

:::steps heading="Theft Mitigation Layers"
1. Encrypt all endpoint devices using full-disk encryption (BitLocker for Windows, FileVault for macOS, LUKS for Linux) so stolen hardware yields no readable data
2. Enroll all devices in Mobile Device Management (MDM) to enable remote wipe capability and enforce encryption policy
3. Apply physical cable locks and secure mounting hardware for workstations, servers, and kiosk systems
4. Train employees to secure devices in public spaces and report loss or theft within defined timeframes per incident response policy
5. Implement secure media disposal procedures per NIST SP 800-88 (Guidelines for Media Sanitization) for decommissioned storage
:::

::::columns
::col::
:::callout style=soft
**Impact of Unsecured Devices**
- Data exposure without encryption
- Identity theft via stored credentials
- Regulatory penalties under GDPR, HIPAA, or SOX
:::
::col::
:::callout style=line
**Common Attack Vectors**
- Unattended workstations
- Shoulder surfing
- Social engineering for physical access
- Dumpster diving for printed reports or media
:::
::::

:::notes
Theft, while one of the most straightforward physical security threats, often masks deeper risks that extend well beyond the replacement cost of stolen hardware. The true impact of theft lies in unauthorized access to sensitive data, which can lead to identity theft, corporate espionage, regulatory penalties, and reputational damage.

According to NIST Special Publication 800-124, "Guidelines for Managing the Security of Mobile Devices in the Enterprise," unencrypted mobile devices pose a significant risk for data loss. When a device such as a laptop, smartphone, or USB drive is stolen without proper encryption or access controls, it can result in a reportable data breach under frameworks like the General Data Protection Regulation (GDPR) or the Health Insurance Portability and Accountability Act (HIPAA).

One notable example is the 2006 theft of a laptop from the U.S. Department of Veterans Affairs, which exposed personal data of over 26 million veterans. The device was unencrypted, leading to a major incident requiring public disclosure and policy changes.

Physical theft also includes seemingly low-tech methods such as dumpster diving, where attackers retrieve discarded documents, storage media, or printouts containing sensitive information. This technique is particularly effective in environments lacking proper document destruction policies compliant with standards such as NIST SP 800-88 (Guidelines for Media Sanitization).

Organizations must implement layered defenses including full-disk encryption (e.g., BitLocker, FileVault), secure disposal procedures, physical access controls, and employee awareness training to mitigate these risks effectively.

The regulatory dimension of theft extends beyond the immediate incident. Under GDPR Article 33, organizations must notify the relevant supervisory authority within 72 hours of becoming aware of a personal data breach, a requirement triggered by the theft of any unencrypted device containing personal data of EU residents. HIPAA's Breach Notification Rule similarly mandates notification to affected individuals, the Department of Health and Human Services, and in some cases the media for breaches affecting 500 or more individuals. The financial consequences can be severe: the average cost of a healthcare data breach in 2023 exceeded $10 million according to IBM's Cost of a Data Breach Report. Full-disk encryption is the most effective single control for preventing theft from becoming a reportable breach, an encrypted device in an attacker's hands provides no accessible data, transforming what would be a notification-triggering incident into a hardware insurance claim.
:::

%%%

---
unit: Tampering
code: TMP
title: Tampering
---
:::list heading="What tampering looks like" style=plain
- A card skimmer attached to a payment terminal or ATM
- A malicious USB device planted in an open port
- An "evil maid" attack, briefly accessing an unattended device to install malware
- Hardware keyloggers inserted into keyboard cables or inside devices
- Replacement of firmware or BIOS chips with malicious versions
- Physical access used to extract cryptographic keys via side-channel methods
:::

:::callout style=soft
Tampering is a form of physical threat where an adversary alters a system's hardware, firmware, or operational environment to enable persistent unauthorized access or data exfiltration. It often precedes or enables logical attacks and is a critical concern in both enterprise and consumer environments.
:::

:::image src="images/10_tampering_methods.png" alt="Four-panel diagram illustrating tampering vectors: panel 1 shows a card skimmer overlay on an ATM keypad; panel 2 shows a malicious USB device being inserted into a server port; panel 3 shows the evil maid attack with a laptop open in a hotel room; panel 4 shows a hardware keylogger plugged between keyboard and computer" caption="Tampering attacks share a common characteristic, they leave no trace in software logs and can persist across reboots, OS reinstalls, and software-level security scans" width=full
:::

:::notes
Tampering refers to the deliberate physical manipulation of a computing device, peripheral, or supporting infrastructure to compromise its integrity, availability, or confidentiality. This type of attack is particularly insidious because it often leaves no trace in digital logs and can persist across reboots, reimaging, or even full OS reinstalls if the compromise is embedded in hardware or firmware.

Common tampering vectors include the installation of card skimmers on ATMs or point-of-sale terminals (e.g., CVE-2019-16935), which capture magnetic stripe or PIN data. Similarly, malicious USB devices such as Rubber Ducky or Bash Bunny tools exploit the plug-and-play trust model of modern operating systems to execute pre-programmed attacks upon insertion. These attacks align with the NIST SP 800-150 framework, which emphasizes the need for physical access controls and device integrity checks to mitigate such risks.

Another well-known tampering scenario is the "evil maid" attack, where an adversary gains brief, unsupervised physical access to a device, often in hospitality or shared office environments. During this window, they may install bootkits, firmware rootkits, or hardware keyloggers. These attacks are especially relevant to the ISO/IEC 27001 physical security controls, particularly A.11.1 and A.11.2, which govern secure areas and equipment security.

Tampering also intersects with supply chain threats, such as those outlined in NIST SP 800-161, where adversaries compromise hardware or firmware during manufacturing or transit. The 2018 Bloomberg report on malicious chips in Supermicro servers (though contested) illustrates how tampering at scale can undermine trust in hardware platforms.

Defensive strategies include tamper-evident seals, secure boot mechanisms (as defined in NIST SP 800-155), physical access logging, and regular hardware integrity assessments. Organizations should also implement policies restricting unattended devices and enforce device lockdown features such as USB port disabling and firmware write-protection.

Detection of tampering is as important as prevention. Tamper-evident seals on equipment housings, server chassis intrusion detection switches (which log a BIOS event when a case is opened), and periodic visual inspections of externally accessible ports are practical detective controls. For high-security environments, Trusted Platform Module (TPM) chips, referenced in NIST SP 800-155, provide hardware-rooted attestation that boot firmware has not been modified between power cycles. An organization's ability to detect tampering early is the difference between containing a targeted attack and suffering months of undetected persistent access.
:::

%%%

---
unit: Controls
code: CTL
title: Physical Access Controls
---
:::image src="images/10_access_control_layers.png" alt="Layered access control diagram showing three nested security zones: outer zone (badge reader and CCTV), middle zone (mantrap with two interlocked doors), and inner zone (biometric scanner at server room entry); a security guard is shown at the outer checkpoint with a clear line of sight to all zones" caption="Physical access control is most effective when multiple verification mechanisms are layered, each successive zone requires stronger authentication and provides a checkpoint to detect unauthorized entry" width=full
:::

:::flow
Person approaches secured entry point  
→ Credential presented (badge, PIN, or biometric)  
→ Identity verified against access control database  
→ Mantrap or airlock cycles if required for inner zones  
→ Access event logged with timestamp, identity, and location  
→ Entry granted or denied; anomaly triggers security alert
:::

::::columns
::col::
:::table
| Control | Purpose |
|---|---|
| Badge / key card | Restrict entry to authorized individuals |
| Mantrap | A small space allowing only one verified person through at a time |
| Biometric scanner | Verify identity using a fingerprint or face scan |
| Security guard | Human judgment and challenge ability badges can't provide |
:::
::col::
:::callout
Physical access controls are essential components of a defense-in-depth security strategy. They prevent unauthorized individuals from physically accessing sensitive areas such as data centers, server rooms, or corporate offices.
:::
::::
:::notes
Physical access controls form a foundational layer in the security architecture of any organization. These controls are tangible mechanisms designed to limit entry to physical spaces based on authorization and identity verification. They operate under the principle of layered defense, where multiple controls are used in conjunction to reduce the risk of unauthorized access.

The most common form of physical access control is the use of badge or key card systems. These typically rely on technologies such as RFID (Radio Frequency Identification) or magnetic stripe encoding. While effective at restricting general access, these systems are vulnerable to credential sharing, cloning (as seen in CVE-2019-15941 related to certain RFID implementations), and tailgating. Therefore, they are often augmented with additional controls.

A mantrap is a physical security device designed to prevent unauthorized access by creating a controlled, confined space between two sets of interlocked doors. Only one person can pass through at a time, and both doors cannot be open simultaneously. This mechanism is particularly effective in high-security environments and aligns with NIST SP 800-116 guidelines for physical access control systems.

Biometric scanners enhance identity verification by using unique physiological characteristics such as fingerprints, iris patterns, or facial features. These systems reduce reliance on easily compromised credentials. However, they are not infallible, issues such as false acceptance rates (FAR), false rejection rates (FRR), and spoofing attacks (e.g., using high-resolution photos or fake fingerprints) must be considered. ISO/IEC 30107 provides standards for biometric presentation attack detection.

Finally, human security guards introduce cognitive and situational awareness elements that automated systems cannot replicate. Guards can interpret behavioral cues, respond to anomalies, and enforce policies dynamically. This aligns with the human element emphasized in ISO 27001 Annex A.7, which addresses human resource security.

Together, these controls implement a multi-layered physical security framework. No single control is sufficient on its own; rather, they must be strategically combined to enforce authentication, authorization, and accountability in physical spaces.
:::

%%%

---
unit: Environment
code: ENV
title: Environmental Controls
---
:::image src="images/10_environmental_controls.png" alt="Data center cross-section diagram showing: overhead FM-200 clean agent fire suppression nozzles, CRAC precision cooling units with hot-aisle/cold-aisle airflow arrows, UPS battery cabinet connected to a diesel generator via an automatic transfer switch, and dual redundant power distribution units feeding server racks" caption="Environmental controls protect hardware from non-human threats, fire, heat, humidity, and power disruption, that no software security control can mitigate" width=full
:::
::::columns
::col::
:::list heading="Protecting the infrastructure itself" style=plain
- Fire suppression systems designed for electronics, not just water sprinklers
- Climate control to prevent overheating of servers and equipment
- Uninterruptible power supplies (UPS) and backup generators
- Redundant systems so one environmental failure doesn't cause an outage
:::
::col::
:::callout style=soft
Environmental controls are essential to maintaining system availability, integrity, and safety. These systems protect against natural and mechanical failures that could otherwise lead to catastrophic downtime or data loss.
:::
::::
:::table
| Control Type           | Purpose                                 | Example Technologies                     |
|------------------------|-----------------------------------------|------------------------------------------|
| Fire Suppression       | Prevent equipment damage from fire      | FM-200, Novec 1230, pre-action sprinklers |
| Thermal Management     | Maintain optimal operating temperatures | CRAC units, liquid cooling, hot aisles   |
| Power Continuity       | Ensure uptime during outages            | UPS, diesel generators, ATS              |
| Redundancy             | Eliminate single points of failure      | Dual PDUs, redundant HVAC, failover PSUs |
:::
:::notes
Environmental controls form a foundational layer of physical security by safeguarding IT infrastructure from non-human threats such as fire, temperature extremes, humidity, and power disruptions. These controls are critical for ensuring system availability, data integrity, and continuity of operations, especially in data centers and server rooms where downtime can result in significant financial and operational consequences.

Fire suppression systems in data environments must avoid using water as the primary suppressant due to the risk of electrical damage and data loss. Instead, clean agent fire suppression systems such as FM-200 (Halon alternative) or Novec 1230 are commonly used. These agents suppress fire through chemical interruption and are safe for use around sensitive electronics. Pre-action sprinkler systems, which require both heat detection and confirmation from a secondary system before releasing water, are also used in high-security data environments as a last-resort measure.

Climate control systems regulate temperature and humidity to maintain optimal operating conditions for electronic equipment. Overheating can lead to hardware failure, performance degradation, or even permanent damage. Standards such as ASHRAE TC 9.9 provide guidelines for data center environmental conditions, typically recommending temperatures between 18–27°C (64–80°F) and relative humidity levels of 40–60%. Precision cooling systems like Computer Room Air Conditioners (CRAC) or Computer Room Air Handlers (CRAH) are commonly deployed for this purpose.

Uninterruptible Power Supplies (UPS) provide short-term battery-backed power during outages, allowing for graceful shutdown or transition to backup generators. Generators, in turn, supply longer-term power but require automatic transfer switches (ATS) to ensure seamless switching. The IEEE Std 446 (IEEE Orange Book) outlines best practices for emergency and standby power systems in industrial and commercial facilities.

Redundancy is implemented across all environmental systems to eliminate single points of failure. This includes redundant power paths (e.g., dual PDUs), multiple cooling units, and geographically diverse power feeds. The concept aligns with NIST SP 800-34, which emphasizes the importance of contingency planning and system resilience.

Failures in environmental controls have led to real-world incidents, such as the 2011 Amazon Web Services outage caused by a power failure and subsequent generator malfunction (CVE-2011-5260), which affected numerous high-profile websites. These incidents underscore the importance of robust environmental monitoring and fail-safe mechanisms.

Environmental controls are not merely auxiliary systems, they are integral to the overall security and resilience of physical infrastructure. Their design, implementation, and maintenance must align with recognized standards such as ISO/IEC 27001 for information security management and NIST SP 800-53 for security and privacy controls.
:::

%%%

---
unit: Strategy
code: DID
title: Defense in Depth, Physically
---
:::callout style=soft
Defense in depth is a foundational security strategy that originated in military doctrine and has been widely adopted in cybersecurity. In the physical security domain, it refers to the implementation of multiple layers of protection across different spatial and functional zones, from the outer perimeter to the core asset.
:::

:::image src="images/10_defense_in_depth.png" alt="Concentric rings diagram labeled from outside to inside: Perimeter (fence, gate, lighting, patrol), Building Entry (badge reader, security desk, biometric), Secure Room (keypad lock, mantrap, motion sensors, CCTV), Device (cable lock, tamper-evident seal, locked cabinet), each ring color-coded with a list of controls and the purpose each layer serves" caption="Physical defense in depth, each concentric zone is an independent barrier; an attacker who defeats one layer still faces the next, significantly raising the cost and time of a successful intrusion" width=full
:::

::::columns
::col::
:::list heading="Physical Security Layers" style=plain
- Perimeter security (fences, gates, lighting)
- Building access control (turnstile, mantrap, badge readers)
- Room-level security (biometric locks, surveillance)
- Device-level protection (locked cabinets, cable locks)
:::
::col::
:::table
| Layer            | Example Controls                        | Purpose                              |
|------------------|-----------------------------------------|--------------------------------------|
| Perimeter        | Fencing, bollards, patrols              | Deter and delay unauthorized entry   |
| Building Entry   | Access cards, biometrics, security desks| Authenticate and log personnel       |
| Secure Room      | Keypad locks, motion sensors            | Restrict access to sensitive areas   |
| Device           | Locks, tamper-evident seals             | Prevent physical tampering           |
:::
::col::
:::flow
Perimeter
  ↓
Building Entry
  ↓
Secure Room
  ↓
Device
:::
::::

:::notes
Defense in depth, also known as "layered security," is a strategic approach that emphasizes redundancy in protective measures. In cybersecurity, this means deploying multiple defensive tools such as firewalls, intrusion detection systems, and endpoint protection. In the physical world, it translates to overlapping barriers that cumulatively increase the difficulty for an adversary to reach a target.

Each physical layer serves a distinct function. The **perimeter layer** (e.g., fences, gates, and lighting) is designed to deter opportunistic threats and delay determined attackers. According to **NIST SP 800-116**, physical access control systems should be part of a layered approach to protect federal information systems. The **building entry layer** introduces authentication and accountability through mechanisms like badge readers, biometric scanners, or security personnel. This layer ensures only authorized individuals can proceed further.

The **room-level layer** (e.g., server rooms or data vaults) often incorporates more stringent controls such as biometric locks, mantraps, or continuous monitoring. These controls align with **ISO 27001 Annex A** physical security guidelines, which emphasize restricting physical access to information processing facilities. Finally, the **device layer** focuses on securing individual assets, such as servers or network equipment, using locks, tamper-evident seals, or secure mounting systems.

This layered model ensures that if one control fails, for instance, a stolen access card bypasses the building entry, subsequent layers (e.g., room locks, device cages) still provide protection. Real-world breaches, such as the **CVE-2021-44228 (Log4Shell)** exploitation in data centers, underscore the importance of physical safeguards even when cyber vulnerabilities are present. An attacker with physical access can bypass network controls entirely, making defense in depth critical across both domains.

The layered approach also provides time, the most underappreciated value in physical security. Each layer an attacker must defeat takes time and creates opportunities for detection. A well-designed physical security program integrates detective controls (CCTV, access log alerts, motion sensors) at each layer so that a breach of the outer layer triggers investigation before the inner layers are reached. NIST SP 800-53 Control PE-6 (Monitoring Physical Access) requires organizations to monitor physical access to facilities and review physical access logs regularly. Defense in depth without monitoring is merely a delaying tactic; with monitoring, it becomes a system for catching intruders before they reach critical assets.
:::

%%%

---
unit: Summary
code: SUM
title: The Layer You Can Touch
---
:::pullquote
Every digital defense in this course assumes the hardware underneath it is physically protected, today's class is why that assumption has to hold.
:::

:::image src="images/10_physical_security_summary.png" alt="Security stack pyramid with physical security as the base layer, topped by network security, then application security, then data security at the apex, an arrow on the left labels each layer; a crack running through the base layer is shown propagating upward through all layers above it, illustrating how physical compromise invalidates everything built on top" caption="Physical security is the foundation of the entire security stack, a compromise at the base layer invalidates every protection mechanism built above it" width=full
:::

::::columns
::col::
:::list heading="Physical Threats" style=chips
- Unauthorized Access
- Theft
- Tampering
- Environmental Hazards
:::

::col::
:::list heading="Control Categories" style=plain
- **Preventive**: Locks, biometrics, mantraps
- **Detective**: Motion sensors, CCTV, tamper-evident seals
- **Corrective**: UPS systems, fire suppression
:::
::col::
:::table
| Threat            | Example CVE/Standard         | Impact                      |
|-------------------|------------------------------|-----------------------------|
| Tailgating        | N/A (Physical)               | Unauthorized access         |
| Hardware theft    | N/A                          | Data loss, compliance breach|
| DMA attacks       | CVE-2019-19781 (Cold Boot)    | Memory scraping             |
| Power fluctuation | N/A                          | System downtime             |
:::
::col::
:::callout style=soft
Physical security underpins all logical controls. A compromised device invalidates all cryptographic protections.
:::
::::

:::notes
Physical security represents the foundational layer of the security stack, the tangible, real-world protection of computing infrastructure. Without it, all upper-layer digital defenses such as encryption, authentication, and access control become theoretically irrelevant. This is because an attacker with physical access to a device can bypass or subvert nearly any software-based protection mechanism.

For example, an adversary with physical access can exploit Direct Memory Access (DMA) ports, perform cold boot attacks to extract cryptographic keys from RAM (as seen in CVE-2019-19781), or simply remove storage drives for offline analysis. These attacks circumvent operating system-level protections entirely, demonstrating why physical access is often equated with root access in security literature.

Standards such as NIST SP 800-116 and ISO 27001 emphasize the importance of layered physical controls. These include preventive mechanisms like biometric access systems and mantraps, detective tools such as surveillance cameras and intrusion detection systems, and corrective infrastructure like uninterruptible power supplies (UPS) and fire suppression systems.

Environmental controls are especially critical in data centers, where temperature regulation, humidity control, and power stability directly affect system integrity. A single power surge or overheating event can lead to service outages or permanent hardware damage, undermining availability and potentially exposing sensitive data.

This lecture underscores that physical security is not optional, it is the base upon which all other security domains are built. As we move into network security in the next unit, we will assume this layer is intact, just as real-world security architectures do.

The three control categories, preventive, detective, and corrective, map directly to the security control taxonomy in NIST SP 800-53 and ISO/IEC 27001. Preventive controls reduce the probability of a security event occurring (locks, biometrics, mantraps). Detective controls identify that an event has occurred or is occurring (CCTV, access logs, tamper-evident seals, motion sensors). Corrective controls limit the damage after an event and restore normal operations (UPS systems enabling graceful shutdown, fire suppression protecting equipment, incident response procedures). CompTIA Security+ SY0-701 tests candidates' ability to classify controls by this taxonomy across all domains, physical controls are a primary example used to make these categories concrete. Recognizing that the same taxonomy applies to both physical and logical security domains is a key conceptual bridge as this course moves from physical protections to network and application security layers in subsequent classes.
:::

%%%

---
unit: Biometrics
code: BIO
title: Biometric Authentication, Deep Dive
---
:::callout style=soft
Biometric authentication uses physiological or behavioral characteristics to verify identity. Unlike passwords or badges, biometrics cannot be borrowed, shared, or forgotten, but they cannot be changed if compromised.
:::

:::image src="images/10_biometric_types.png" alt="Grid of six biometric modality icons: fingerprint scanner, iris recognition camera, facial recognition overlay, hand geometry reader, voice waveform analyzer, and keystroke dynamics graph, each labeled with its False Acceptance Rate (FAR) and primary use case" caption="Biometric modalities differ significantly in accuracy, cost, and susceptibility to spoofing, selecting the right modality requires balancing security requirements against operational constraints" width=full
:::

:::table
| Modality          | FAR (typical) | FRR (typical) | Spoofing Risk   | Cost     |
|-------------------|---------------|---------------|-----------------|----------|
| Fingerprint       | 0.001%        | 0.1%          | Medium (gelatin prints) | Low  |
| Iris Recognition  | 0.0001%       | 0.08%         | Low (requires live eye) | High |
| Facial Recognition| 0.001%        | 0.3%          | Medium (3D mask) | Medium  |
| Hand Geometry     | 0.1%          | 0.2%          | Low              | Medium   |
| Voice Recognition | 0.5%          | 2%            | High (recording) | Low      |
| Keystroke Dynamics| 1%            | 5%            | Very High        | Very Low |
:::

:::list heading="Key Concepts for Security+" style=plain
- **FAR (False Acceptance Rate)**: The probability that an unauthorized user is incorrectly accepted, a security failure
- **FRR (False Rejection Rate)**: The probability that an authorized user is incorrectly rejected, an availability failure
- **CER / EER (Crossover Error Rate)**: The point where FAR = FRR; lower CER indicates more accurate system
- **Liveness detection**: Countermeasure to presentation attacks using photos, recordings, or synthetic replicas
:::

:::notes
Biometric authentication systems are increasingly common in enterprise physical security because they bind identity to a person's physical presence rather than to a possession (badge) or a secret (PIN). However, deploying biometrics involves careful consideration of statistical accuracy, legal compliance, privacy implications, and attack resistance.

The two primary error rates used to evaluate biometric systems are the False Acceptance Rate (FAR) and the False Rejection Rate (FRR). FAR measures how often the system incorrectly accepts an unauthorized individual, a security failure that could allow an intruder to enter a restricted area. FRR measures how often the system incorrectly rejects a legitimate user, an availability failure that creates operational friction and can lead employees to prop doors open or share credentials to bypass the system, thereby defeating its purpose. These two rates are inversely related: adjusting a system's sensitivity threshold to reduce FAR typically increases FRR, and vice versa. The Crossover Error Rate (CER), also called the Equal Error Rate (EER), is the threshold where FAR equals FRR and serves as a single benchmark for comparing the overall accuracy of different biometric systems. Lower CER values indicate better systems.

ISO/IEC 30107 (Biometric Presentation Attack Detection) defines standards for detecting when an attacker presents a synthetic or copied biometric trait to fool the scanner. Liveness detection, the ability to distinguish a live finger from a gelatin replica, or a live face from a photograph, is a critical countermeasure against presentation attacks. Modern fingerprint scanners use capacitive sensing to detect blood flow, and facial recognition systems increasingly use structured light (IR dot projection) to build 3D maps of faces that photographs cannot replicate.

A critical limitation of biometrics that distinguishes them from passwords is irrevocability: if a biometric database is compromised, the affected individuals cannot change their fingerprints or irises the way they would change a password. For this reason, NIST SP 800-76 (Biometric Specifications for Personal Identity Verification) recommends storing only biometric templates, mathematical representations derived from the scan, rather than raw images, and applying cryptographic protection to template databases. This limits the utility of a stolen database to an attacker while preserving the ability to re-enroll users with updated templates.

Phone fingerprint and face unlock are biometric authentication using low-cost modalities built into the device. Phone biometrics are typically local-only: the template never leaves the device, a privacy-preserving design that enterprise systems may not match. GDPR classifies biometric data as a special category requiring explicit consent and heightened protection, so deployment in European workplaces is more regulated than elsewhere.
:::

%%%

---
unit: Surveillance
code: SURV
title: CCTV and Physical Surveillance Systems
---
:::image src="images/10_cctv_coverage.png" alt="Top-down floor plan of an office building with camera placement annotations: entry/exit corridors covered by wide-angle cameras, server room entrance with PTZ camera and motion detection zone highlighted, parking area covered by infrared night-vision cameras, and blind-spot analysis showing gaps between fixed camera fields of view" caption="Camera placement must be deliberately designed to eliminate blind spots at critical chokepoints, CCTV that does not cover the exact point of entry provides no forensic value after an incident" width=full
:::

::::columns
::col::
:::list heading="Surveillance System Components" style=plain
- Fixed cameras for continuous coverage of chokepoints
- PTZ (pan-tilt-zoom) cameras for operator-directed monitoring
- Infrared / night-vision cameras for low-light environments
- Network Video Recorders (NVR) for digital storage and retrieval
- Video analytics software for motion detection and anomaly alerting
- Display monitors at security operations center (SOC)
:::
::col::
:::callout style=soft
CCTV serves three security functions: **deterrence** (visible cameras discourage bad actors), **detection** (real-time monitoring identifies incidents in progress), and **forensics** (recordings provide evidence for investigation and prosecution after an event).
:::
::::

:::table
| Consideration      | Requirement                                 | Standard / Reference         |
|--------------------|---------------------------------------------|------------------------------|
| Retention period   | Minimum 30–90 days depending on sector      | HIPAA, PCI DSS 9.4.6, SOX   |
| Resolution         | Sufficient to identify faces at entry points| NIST SP 800-111              |
| Coverage gaps      | Zero tolerance at classified entry points   | NIST SP 800-116              |
| Tamper protection  | Cameras must be tamper-evident and alarmed  | ISO/IEC 27001 A.11.1.1       |
| Privacy compliance | Signage required; avoid restrooms/changing areas | GDPR Article 6, local law |
:::

:::notes
Closed-Circuit Television (CCTV) systems are among the most widely deployed physical security controls, providing continuous visual coverage of facility entry points, corridors, parking areas, and sensitive rooms such as server rooms and data vaults. The term "closed circuit" historically referred to the fact that the video feed was transmitted over a dedicated, private circuit rather than broadcast, distinguishing it from broadcast television. Modern IP-based camera systems have largely replaced analog CCTV, but the term persists in industry and regulatory language.

Effective CCTV deployment requires deliberate design rather than ad hoc camera placement. A common mistake is placing cameras where they will record an incident's aftermath rather than the incident itself, for example, a camera positioned to record a hallway rather than the door through which an intruder entered. Security practitioners use camera coverage mapping, also called a "field of view analysis," to identify blind spots and ensure that every critical entry point, including fire exits that are sometimes overlooked, is covered with at least two overlapping camera angles to eliminate single points of failure in coverage.

NIST SP 800-111 recommends that video surveillance systems in federal facilities be designed to capture images at sufficient resolution to identify individuals at the camera's maximum intended range. For entry-point cameras, this typically requires cameras capable of capturing facial detail at distances up to six meters, which in practice means high-definition IP cameras rather than older analog systems. Recording resolution should not be compromised to save storage costs, blurry footage has no forensic value.

Retention requirements vary by regulatory framework. PCI DSS Requirement 9.4.6 requires that video recording from surveillance systems covering cardholder data environments be retained for at least three months. Healthcare organizations subject to HIPAA may face longer retention requirements under state law. Organizations should consult with legal counsel to establish compliant retention periods and implement automated deletion policies at the end of the retention window to minimize privacy risk.

A frequently overlooked aspect of CCTV systems is their own security. IP cameras that are not patched are themselves attack targets, CVE-2021-36260 affected millions of Hikvision cameras worldwide, allowing unauthenticated remote code execution and potentially giving attackers the ability to disable recording or access live feeds. CCTV systems must be managed as part of the organization's vulnerability management program, not treated as standalone appliances that are deployed and forgotten.

Broad surveillance has a real security benefit, but how much is appropriate is a policy and ethics question, not a technical one, as the debates over city-wide camera networks and airport facial recognition show.
:::

%%%

---
unit: Design
code: MNT
title: Mantraps and Airlock Design
---
:::callout style=soft
A **mantrap** (also called an airlock or sally port) is a physical access control mechanism consisting of two interlocked doors separated by a small chamber. The fundamental design rule: only one door can open at a time, and entry to the inner door requires positive verification after the outer door closes.
:::

:::image src="images/10_mantrap_design.png" alt="Cross-section blueprint of a mantrap installation: outer door with card reader labeled 'Zone 1, Public'; enclosed chamber with overhead camera, weight sensor, and occupancy detector; inner door with biometric scanner labeled 'Zone 2, Restricted'; control panel showing interlocking logic states; guard station with override console and alarm panel" caption="Mantrap design combines physical containment with layered verification, the occupancy sensor prevents two people from entering simultaneously while the two-door interlock prevents straightforward tailgating" width=full
:::

:::steps heading="Mantrap Entry Sequence"
1. Person presents badge or card at outer door reader, access to outer zone granted
2. Person enters the chamber, outer door closes and locks automatically
3. Occupancy sensor confirms only one person is present (weight or video analytics)
4. Person presents second factor (PIN or biometric) at inner door reader
5. If identity verified and occupancy confirms single occupant: inner door unlocks
6. All events logged with timestamps; guard alerted for any anomaly or failed verification
:::

:::table
| Feature               | Security Benefit                              | Cost/Complexity |
|-----------------------|-----------------------------------------------|-----------------|
| Two-door interlock    | Physically prevents tailgating                | Medium          |
| Occupancy detection   | Detects two people attempting simultaneous entry | High           |
| Two-factor inner auth | Ensures credential alone is insufficient      | Medium          |
| Guard override        | Human judgment for edge cases                 | High (staffing) |
| Video in chamber      | Forensic record of every entry attempt        | Low             |
:::

:::notes
Mantraps address a fundamental limitation of standard door-and-badge-reader access control systems: they provide no physical mechanism to prevent an unauthorized person from following an authorized person through the door. In a standard access-controlled doorway, the badge reader's job ends the moment the door is unlocked, what happens physically after that is beyond the system's capability to control. A mantrap solves this by transforming entry from a momentary event into a controlled process with a physical containment zone between the outer and inner barriers.

The two most important design elements are the door interlock and the occupancy verification system. The door interlock, implemented through electrical contacts and a controller that monitors both door positions, ensures that if the outer door is open, the inner door cannot open, and vice versa. This is a physical enforcement of the "one at a time" policy that cannot be circumvented by credential sharing. The occupancy verification system, implemented using either a weight-sensitive floor panel, infrared beam arrays, or overhead video analytics, detects whether more than one person has entered the chamber. If two people enter together, the inner door will not open regardless of the credentials presented.

Mantraps are classified under NIST SP 800-116 as a high-assurance physical access control mechanism and are recommended for facilities requiring Assurance Level 4 (the highest level), which includes locations housing classified government information, critical infrastructure control systems, and high-value financial assets. They are also required by some compliance frameworks for data center environments where multiple PCI DSS or HIPAA-regulated systems are housed.

A key operational consideration is the guard override capability. Automated mantraps create situations that require human judgment, for example, a person using a wheelchair may trigger the occupancy sensor as "two occupants" due to the chair's weight, or a person with a physical disability may not be able to present a biometric sample. Guard override consoles allow security personnel to observe the chamber via video and manually authorize entry in exceptional circumstances while maintaining a logged record of the decision. This human-in-the-loop capability is essential for both accessibility compliance (Americans with Disabilities Act requirements apply to building entry systems) and operational resilience.

The term "sally port" comes from military architecture: the small controlled gates in fort walls that let defenders "sally forth" without opening the main gate. The principle of controlled, one-at-a-time passage with verification is ancient; only the technology has changed, from portcullis and guards to electronic interlocks and biometric readers.
:::

%%%

---
unit: Perimeter
code: PER
title: Perimeter Security Controls
---
:::image src="images/10_perimeter_security.png" alt="Aerial illustration of a corporate campus perimeter showing: anti-ram vehicle bollards at entrance road, perimeter chain-link fence with barbed wire topper, guard booth at vehicle gate, CPTED-compliant landscape design (low shrubs providing no concealment, clear sight lines), security lighting on poles at 20-meter intervals, and signage declaring the area a controlled access zone" caption="Perimeter security establishes the outermost defensive boundary, its purpose is to deter opportunistic attackers, delay determined attackers, and channel all legitimate entry through observable, controlled chokepoints" width=full
:::

::::columns
::col::
:::list heading="Physical Barrier Types" style=plain
- Chain-link fencing with barbed wire or razor wire topper
- Concrete Jersey barriers and anti-ram bollards (vehicle barriers)
- Perimeter walls (masonry or reinforced concrete for high-security sites)
- Crash-rated gates meeting ASTM F2656 or DOS SD-STD-02.01 standards
- Security lighting (minimum 2 foot-candles at perimeter per IES standards)
:::
::col::
:::list heading="CPTED Principles Applied to Perimeter" style=plain
- **Natural Surveillance**: Landscape design that maintains clear sight lines, low ground cover, trimmed trees, no concealment near entry points
- **Territorial Reinforcement**: Signage, fencing, and lighting that clearly communicate the boundary between public and controlled space
- **Access Control**: Channeling traffic through observable, guarded chokepoints rather than allowing multiple unmonitored entry paths
- **Maintenance**: Broken fencing, burned-out lights, and overgrown vegetation signal neglect and invite opportunistic intrusion
:::
::::

:::notes
Perimeter security is the outermost layer of physical defense and serves three primary functions: deterrence, delay, and detection. A well-designed perimeter deters opportunistic attackers by signaling that the target is actively defended; it delays determined attackers by imposing physical barriers that require time and tools to defeat; and it enables detection by channeling all legitimate and illegitimate traffic through observable chokepoints covered by surveillance and guard positions.

Crime Prevention Through Environmental Design (CPTED) is a multidisciplinary approach to deterring criminal behavior through environmental design. Developed by criminologist C. Ray Jeffery in 1971 and further elaborated by Oscar Newman's concept of "defensible space," CPTED principles have been incorporated into physical security planning standards including NIST SP 800-116 and the Department of Defense's Unified Facilities Criteria (UFC 4-020-01). The four primary CPTED principles are natural surveillance (designing spaces so legitimate users can observe potential criminal behavior), territorial reinforcement (clearly delineating boundaries between public and controlled space), natural access control (guiding pedestrian and vehicle traffic to minimize unobserved entry), and maintenance (keeping the environment in good repair to signal active occupancy and care).

Vehicle barriers deserve specific attention in the context of perimeter security for facilities with road access. Standard bollards are designed to stop vehicles at specified impact speeds; crash-rated bollards meeting ASTM F2656 standards are certified to stop a 15,000 lb vehicle traveling at 50 mph within a defined penetration distance. The 1995 Oklahoma City bombing, in which a truck bomb caused 168 fatalities, directly accelerated the adoption of vehicle barrier standards around government and critical infrastructure facilities, leading to what is now known as "standoff distance" requirements that mandate a minimum separation between vehicle barriers and building exteriors.

Security lighting is often undervalued but is one of the most cost-effective perimeter controls. The Illuminating Engineering Society (IES) specifies minimum footcandle requirements for security applications: perimeter boundaries typically require at least 0.5 to 2 footcandles, while entry points and parking areas require 2 to 5 footcandles for effective video surveillance. Inadequate lighting directly reduces the effectiveness of CCTV systems and creates concealment opportunities for attackers.

Perimeter security appears in daily life at airports, hospitals, courthouses and stadiums. The 2017 Manchester Arena bombing accelerated the adoption of vehicle and pedestrian perimeter controls, such as bollards and crowd barriers, at public venues, a direct example of how real events shape the controls practitioners deploy.
:::

%%%

---
unit: CaseStudy
code: CS1
title: Case Study, ATM Card Skimmer Attacks
---
:::callout style=soft
Card skimming is the physical installation of a fraudulent device on an ATM, fuel pump, or payment terminal that captures payment card data without the cardholder's knowledge. It is one of the most economically damaging physical tampering attacks targeting financial infrastructure.
:::

:::image src="images/10_atm_skimmer_case_study.png" alt="Side-by-side comparison of a legitimate ATM card slot versus a skimmer overlay: the skimmer is shown as a thin plastic shell that fits over the factory card reader, with a labeled internal diagram showing the magnetic stripe reading coil, a coin-sized wireless transmitter, and a pinhole camera aimed at the PIN pad, next to a photograph of actual recovered skimmer hardware from a law enforcement case" caption="Modern skimmers are manufactured to match the target ATM's color and texture precisely, visual inspection alone is insufficient, and physical manipulation of the card reader is the primary detection method" width=full
:::

:::steps heading="How a Skimmer Attack Works"
1. Attacker fabricates a skimmer overlay matched to the target ATM model using 3D printing or injection molding
2. Attacker installs the overlay on the card slot in seconds; a secondary pinhole camera or overlay keypad captures PINs
3. Captured data is stored on internal flash memory or transmitted wirelessly in real time
4. Attacker returns to retrieve data (or it is transmitted remotely); cloned cards are manufactured and used for cash withdrawals
5. Discovery: bank fraud detection identifies abnormal withdrawal patterns from cards used at the same ATM
:::

:::table
| Attack Component    | Technology Used              | Detection Method                     |
|---------------------|------------------------------|--------------------------------------|
| Magnetic stripe read| Thin copper coil overlay     | Physical jiggle test, anti-skimmer jammer |
| PIN capture         | Pinhole camera or PIN overlay| Camera indicator check, hand shielding |
| Data exfiltration   | Bluetooth / GSM transmitter  | RF detection sweep by technician     |
| Concealment         | Color-matched 3D printed shell| Visual inspection, UV markings       |
:::

:::notes
ATM card skimming represents the intersection of physical tampering and financial fraud, and it illustrates how physical security failures translate directly into quantifiable financial losses at scale. The FBI estimates that ATM skimming costs U.S. financial institutions over $1 billion annually. Globally, the European Association for Secure Transactions (EAST) reported thousands of ATM skimming incidents annually across European markets before contactless card adoption began to reduce magnetic stripe dependency.

The attack lifecycle begins with reconnaissance: skilled skimming operations identify ATM models (often the Diebold Nixdorf Opteva series or NCR SelfServ family) and fabricate overlay components using consumer 3D printers or injection molding equipment, producing plastic overlays that precisely match the target machine's color, texture, and dimensions. Installation takes as little as three to five seconds for experienced attackers, fast enough to be performed in a busy environment without attracting attention.

The technical countermeasures deployed by ATM manufacturers and banks include jitter mechanisms (which cause the card transport motor to move irregularly, making it difficult for an overlay coil to read the magnetic stripe cleanly), green-LED card-entry illumination (which makes it visually apparent to customers when a foreign overlay is present), and ultrasonic anti-skimming modules (which jam the magnetic read head in any overlay device that may be installed). These are referenced in EMVCo's security requirements for payment terminals.

The primary customer-facing countermeasure, and the reason banks universally advise customers to "cover the PIN pad when entering your PIN", is that even if a skimmer captures the magnetic stripe data, a separately captured PIN is required to create a functional counterfeit card. Without the PIN, the stolen stripe data can only be used for card-not-present fraud, which is more difficult to execute at scale than ATM withdrawals. EMV chip technology has significantly reduced skimming profitability in markets with high chip adoption because chip transactions generate a unique cryptogram for each transaction that cannot be replicated from static card data, however, "shimming" attacks targeting chip readers have emerged as a successor technique.

Physical attacks on ATMs span a spectrum, from low-tech skimming overlays to jackpotting that commands the machine to dispense all its cash, and some rely on OS-level exploits after access to service ports (for example CVE-2019-16935 in certain ATM platforms). All share one precondition: physical access to the terminal.
:::

%%%

---
unit: CaseStudy
code: CS2
title: Case Study, The Evil Maid Attack
---
:::callout style=soft
The **evil maid attack** is a class of physical attack in which an adversary gains brief, unsupervised access to an unattended device, such as a laptop left in a hotel room, and uses that access to install persistent malware, extract keys, or create a backdoor that survives rebooting and full OS reinstallation.
:::

:::code language=mermaid caption="The evil maid attack exploits the gap between a device's encryption protection (which only protects data when the device is off) and the unprotected pre-boot environment where an attacker can install persistent firmware-level malware"
flowchart TB
  A["Hour 0<br/>Laptop left in a hotel room"] --> B["Hour 1<br/>Intruder enters with a master key"]
  B --> C["Hours 1-2<br/>Boots from external media, plants a bootkit, leaves"]
  C --> D["Hour 3<br/>Owner returns, notices nothing, types disk password"]
  D --> E["Later<br/>Password or data sent to the intruder"]
  F["Defenses: Secure Boot, TPM-sealed keys,<br/>firmware passwords, never leave devices unattended"] -.- C
:::

:::list heading="What an Evil Maid Can Do in 20 Minutes" style=plain
- Boot from a USB drive to access unencrypted partitions or modify the bootloader
- Install a firmware rootkit in UEFI that persists across OS reinstalls and hard drive replacement
- Insert a hardware keylogger to capture the disk encryption passphrase when the owner next logs in
- Clone the hard drive entirely for offline analysis
- Extract the TPM-sealed disk encryption key using a bus probing attack if TPM is not PIN-protected
:::

:::steps heading="Defenses Against Evil Maid"
1. Enable UEFI Secure Boot to prevent loading of unsigned boot code; prevent disabling from BIOS settings with a BIOS password
2. Configure TPM with a pre-boot PIN so that disk decryption requires PIN entry, not just physical TPM presence
3. Enable BitLocker or FileVault with a pre-boot authentication PIN (not auto-unlock via TPM alone)
4. Apply tamper-evident seals to laptop screws and ports; photograph device position before leaving
5. Never leave sensitive devices unattended in hotel rooms, use the hotel safe or take the device with you
6. Enable remote attestation to detect unauthorized firmware modifications upon reconnection to corporate network
:::

:::notes
The evil maid attack was formally named and described by security researcher Joanna Rutkowska in 2009, who demonstrated that full-disk encryption solutions, including TrueCrypt, which was considered the gold standard at the time, could be compromised by an attacker with brief physical access who modified the bootloader to capture the encryption passphrase before handing execution to the encrypted OS. The name refers to the hotel maid who cleans rooms in the owner's absence, but the attack is equally applicable to any scenario where an adversary can access an unattended device: a laptop left in an unlocked office, a device surrendered at a border crossing, or hardware left at an equipment repair shop.

The fundamental vulnerability exploited by the evil maid attack is the gap between the protection provided by full-disk encryption and the unprotected pre-boot environment. Full-disk encryption protects data when the device is powered off, an attacker who steals an encrypted drive cannot read its contents. However, when the device is powered on, the bootloader must run before encryption keys are loaded and the OS starts. The bootloader itself is typically stored unencrypted (or in a small unencrypted partition) so that the BIOS/UEFI can execute it. An evil maid attack modifies this unprotected bootloader to log the user's passphrase when they next enter it.

UEFI Secure Boot addresses this vector by requiring that all code executed during the boot process be cryptographically signed by a trusted key. An attacker cannot substitute a malicious bootloader without also possessing the signing key. However, Secure Boot alone is insufficient if the UEFI settings themselves can be modified, which requires a separate BIOS password to prevent. This is why NIST SP 800-147 (BIOS Protection Guidelines) recommends setting a strong BIOS/UEFI password and disabling boot from external media in UEFI settings to prevent an attacker from simply booting from a USB drive to bypass Secure Boot.

The TPM (Trusted Platform Module) provides hardware-rooted attestation but must be configured correctly to resist evil maid attacks. In its default configuration, BitLocker on Windows uses TPM-only authentication: the disk encryption key is sealed to the TPM and released automatically at boot without user input, which means an attacker with physical access can simply power on the laptop and the disk will decrypt transparently. Enabling BitLocker with a pre-boot PIN (Network Unlock or PIN + TPM mode) requires the user to enter a PIN at every boot before the key is released, which means an evil maid who modifies the bootloader to capture the PIN still has to return and wait for the user to next unlock the device, creating a timing window and forensic opportunity.

The evil maid attack motivates travel-security policies: keeping laptops in carry-on rather than checked luggage, and rules about leaving devices in hotel rooms. Some high-security organizations issue wiped "burner" laptops for travel to certain jurisdictions, so any firmware-level compromise never reaches corporate networks.
:::

%%%

---
unit: Framework
code: NIST
title: NIST SP 800-53 Physical Controls Framework
---
:::callout style=soft
NIST Special Publication 800-53 "Security and Privacy Controls for Information Systems and Organizations" defines the PE (Physical and Environmental Protection) control family, the authoritative federal framework for physical security, widely adopted beyond government as a best-practice baseline.
:::

:::image src="images/10_nist_pe_controls.png" alt="Hierarchical tree diagram of NIST SP 800-53 PE control family: root node 'PE, Physical and Environmental Protection' branches into ten sub-families including PE-2 Physical Access Authorizations, PE-3 Physical Access Control, PE-6 Monitoring Physical Access, PE-8 Visitor Access Records, PE-13 Fire Protection, PE-14 Environmental Controls, PE-15 Water Damage Protection, PE-18 Location of Information System Components, PE-19 Information Leakage, and PE-20 Asset Monitoring, each with a brief description and baseline applicability (LOW/MOD/HIGH)" caption="The NIST SP 800-53 PE control family provides a structured, tiered framework for physical security requirements, each control has LOW, MODERATE, and HIGH baseline variants scaled to the system's impact level" width=full
:::

:::table
| Control | Title                          | Key Requirement                                           | Baseline |
|---------|--------------------------------|-----------------------------------------------------------|----------|
| PE-2    | Physical Access Authorizations | Maintain list of authorized individuals; review quarterly | LOW+     |
| PE-3    | Physical Access Control        | Enforce authorizations at all facility entry points       | LOW+     |
| PE-6    | Monitoring Physical Access     | Monitor physical access; review logs; investigate anomalies| LOW+    |
| PE-8    | Visitor Access Records         | Maintain visitor log for 2+ years; escort all visitors    | LOW+     |
| PE-13   | Fire Protection                | Employ fire suppression and detection devices             | LOW+     |
| PE-14   | Environmental Controls         | Maintain temperature/humidity within defined ranges       | LOW+     |
| PE-18   | Location of System Components  | Position components to minimize potential damage          | MOD+     |
| PE-19   | Information Leakage            | Protect against emanation-based information disclosure    | MOD+     |
:::

:::notes
NIST Special Publication 800-53 Revision 5, published in September 2020, is the foundational catalog of security and privacy controls for U.S. federal information systems and serves as a widely adopted reference standard for private sector organizations as well. The Physical and Environmental Protection (PE) control family contains twenty-three controls addressing every aspect of physical security from access authorization through environmental protection to information leakage through electromagnetic emanations.

The PE control family is organized around a three-tier baseline system: LOW, MODERATE, and HIGH, corresponding to the impact level of the information system as determined by the FIPS 199 categorization process. A system classified as HIGH impact, one whose compromise would have severe or catastrophic consequences for organizational operations, assets, or individuals, requires implementation of all PE controls including enhanced controls such as PE-19 (Information Leakage), which addresses TEMPEST-style attacks in which electromagnetic emissions from computing equipment are captured and analyzed to reconstruct screen or keyboard data.

PE-3 (Physical Access Control) is the cornerstone of the control family and requires organizations to enforce physical access authorizations at all entry and exit points to the facility containing the information system; maintain physical access audit logs; control access to areas officially designated as publicly accessible; escort visitors; and review physical access logs for anomalies at a frequency defined by organizational policy. The HIGH baseline enhancement requires organizations to use two forms of identification for access to facilities housing HIGH-impact systems.

PE-6 (Monitoring Physical Access) requires organizations to monitor physical access to the facility where information systems reside through the use of physical intrusion alarms and surveillance equipment. Critically, PE-6 requires not only collecting this monitoring data but also reviewing physical access logs at a defined frequency, organizations that install cameras but never review footage are technically non-compliant. The enhanced HIGH baseline requires correlating physical access logs with electronic access logs to detect anomalies such as a person badging in at the front door but not appearing in subsequent electronic access records for internal systems, which could indicate badge use by an unauthorized person.

PE-8 (Visitor Access Records) establishes that all visitors to facilities housing information systems must be documented and escorted. Visitor logs must be retained for a minimum period defined in the organization's record retention policy, with the NIST baseline suggesting at least two years. This control directly addresses scenarios in which an insider threat or social engineering attack uses a visitor pretext to introduce an unauthorized individual into a restricted facility.

FedRAMP authorization, required for cloud providers selling to the U.S. government, requires satisfying the NIST SP 800-53 Physical and Environmental Protection (PE) controls, so the hosting data center must have documented physical controls, third-party assessments and PE-specific incident procedures. Cloud-security and government-contracting roles encounter these controls regularly.
:::

%%%

---
unit: Disposal
code: DSP
title: Dumpster Diving and Secure Disposal
---
:::callout style=soft
**Dumpster diving** is the practice of searching through discarded materials, physical trash, recycling bins, or unsecured disposal containers, to retrieve documents, storage media, or hardware that contain sensitive information. It requires no technical skills and is often legal unless the waste is on private property.
:::

:::image src="images/10_secure_disposal.png" alt="Three-panel comparison showing disposal methods: panel 1 labeled 'Inadequate' shows an intact hard drive in a trash bag; panel 2 labeled 'Better' shows a hard drive with a single drill hole through the platter; panel 3 labeled 'NIST SP 800-88 Compliant' shows a hard drive passed through an industrial degausser followed by a shredder with the resulting metal fragments labeled as certified destruction" caption="The adequacy of media disposal must match the sensitivity of the data it once held, physical destruction to NIST SP 800-88 standards is the only control that provides cryptographically assured irrecoverability" width=full
:::

:::table
| Media Type        | NIST SP 800-88 Clear Method  | NIST SP 800-88 Purge/Destroy Method          |
|-------------------|------------------------------|----------------------------------------------|
| HDD (magnetic)    | Overwrite all sectors 1x     | Degauss + shred or disintegrate              |
| SSD / Flash       | ATA Secure Erase command     | Shred to ≤2mm particles or incinerate        |
| Optical media     | N/A (overwrite not possible) | Shred or incinerate                          |
| Paper documents   | Cross-cut shred (DIN 66399 P-4)| Micro-cut shred (P-5/P-6) or incinerate    |
| USB drives        | ATA Secure Erase / overwrite | Shred or incinerate                          |
| Magnetic tape     | Degauss at appropriate Oe    | Shred or incinerate                          |
:::

:::list heading="What Dumpster Divers Find" style=plain
- Internal org charts, phone directories, and employee lists
- Printed reports containing financial data, customer PII, or health records
- Old hard drives, USB drives, and backup tapes with recoverable data
- Decommissioned access badges (especially if combined with tailgating)
- Device configuration printouts including IP addresses and passwords
- Shredded documents that were cross-cut rather than micro-cut (reassemblable)
:::

:::notes
Dumpster diving has been a documented intelligence-gathering and criminal technique since long before the digital era. Robert Cialdini's classic social engineering studies documented the practice, and Kevin Mitnick's accounts of his hacking activities (documented in "The Art of Intrusion") describe recovering physical documents from corporate trash that provided organizational intelligence used to support social engineering attacks. The technique remains relevant today because organizations frequently dispose of sensitive information without applying appropriate destruction controls.

The legal status of dumpster diving is jurisdiction-dependent. In the United States, the Supreme Court's 1988 decision in California v. Greenwood established that there is no reasonable expectation of privacy in garbage placed at the curb for collection, meaning that in many jurisdictions, retrieving information from publicly accessible waste containers is not illegal. This places the burden of protection entirely on the organization: once sensitive documents leave the building in an intact, readable form, they are effectively public. Private property restrictions apply on-premises, but once waste leaves the facility for collection, legal protection is typically lost.

NIST SP 800-88 "Guidelines for Media Sanitization" is the authoritative reference for organizations determining appropriate disposal methods for different media types. The standard defines three tiers of sanitization: Clear (logical techniques that protect against simple, non-laboratory recovery), Purge (more resistant techniques against laboratory attack), and Destroy (physically rendering the media unusable). For the majority of sensitive data environments, Purge or Destroy methods are appropriate. A common misconception is that deleting files or reformatting a drive constitutes adequate disposal, standard file deletion removes the file system pointers but leaves data intact on the storage medium and recoverable with freely available forensic tools.

Physical destruction methods must be matched to the media type. Magnetic degaussing, exposing media to a powerful alternating magnetic field, is effective for traditional magnetic hard drives and tape media but is completely ineffective for solid-state drives (SSDs), USB flash drives, and smartphones, which use NAND flash memory with no magnetic data encoding. Organizations that degauss SSDs believing the data has been destroyed are creating a serious disposal failure. For SSDs, either the manufacturer-provided Secure Erase command (if trusted and verifiable) or physical shredding to particles of two millimeters or less is required by NIST SP 800-88.

Paper document destruction deserves equal attention. DIN 66399 defines security levels for paper shredding from P-1 (strip cut, large particles) through P-7 (micro-cut suitable for top-secret documents). The frequently used cross-cut shredder, which produces rectangular particles, achieves approximately DIN P-4, which is suitable for general confidential documents but has been demonstrated to be reassemblable using software and sufficient time. Organizations handling highly sensitive documents such as healthcare records, financial data, or legal materials should use P-5 or higher micro-cut shredders or engage certified document destruction services that issue certificates of destruction.

Document reconstruction from improperly shredded waste is well documented, including in the Enron and Arthur Andersen case. The lesson is simple: if waste can be reassembled, an adversary can reassemble it, so the security of disposal must match the sensitivity of what is disposed.
:::

%%%

---
unit: Visitors
code: VIS
title: Visitor Management and Escort Policies
---
:::image src="images/10_visitor_management.png" alt="Flowchart of a visitor management lifecycle: pre-visit (host submits request, security approves, visitor receives confirmation with check-in instructions); arrival (visitor presents ID at reception, photo captured, badge printed with time-expiry and visitor designation, host notified); during visit (visitor escorted at all times in restricted zones, badge visible); departure (badge returned, log entry closed, access revoked automatically at badge expiry)" caption="A structured visitor management lifecycle ensures that every non-employee present in a facility is identified, authorized, logged, and escorted, creating an accountable record for every access event" width=full
:::

::::columns
::col::
:::list heading="Visitor Management Requirements" style=plain
- Pre-authorization by a named internal host before arrival
- Government-issued photo ID verification at reception
- Photo capture and visitor badge issuance with time-limited validity
- Host notification and escort requirement in restricted zones
- Access revoked automatically at badge expiry or check-out
- Visitor log retention (NIST PE-8 requires minimum two-year retention)
:::
::col::
:::callout style=soft
Visitors represent an elevated physical security risk because they lack the background screening, security training, and accountability that employees carry. Every visitor access event must be documented, authorized, time-limited, and escorted in restricted areas.
:::
::::

:::steps heading="Handling Unexpected Visitors"
1. Visitor presents at reception without prior authorization, do not grant access pending verification
2. Reception contacts the visitor's claimed host to verify relationship and business purpose
3. If host confirms: proceed with standard badge and escort process; document the late authorization
4. If host cannot be reached or denies the visitor: politely decline entry and offer to schedule a future visit
5. Log the incident regardless of outcome, an unauthorized access attempt is a security event
6. Security team reviews unexpected visitor patterns during periodic access log audits
:::

:::notes
Visitor management is an often-underinvested component of physical security programs, frequently treated as a reception function rather than a security function. The distinction matters: reception-managed visitor logs often prioritize convenience and hospitality over accountability, while security-managed visitor programs treat every non-employee access event as a potential security risk that must be controlled, documented, and audited.

NIST SP 800-53 Control PE-8 (Visitor Access Records) requires organizations to maintain a visitor access log including the visitor's name, the organization they represent, the date and time of access, and the name of the organizational personnel authorizing access. This log must be reviewed and retained for a minimum period defined in the organization's records retention schedule. The HIGH baseline enhancement for PE-8 adds the requirement that visitor access logs be reviewed at defined intervals to identify anomalies, for example, a contractor visiting a restricted area more frequently than their project scope would warrant.

Physical visitor badges serve multiple functions beyond identification. Time-limited validity, commonly implemented through holographic color-shifting materials or electronic expiry managed by the physical access control system, prevents visitors from retaining functional badges after their authorized visit ends. Visitor-specific badge colors or designs that are visually distinct from employee badges enable employees to identify and challenge visitors who are not accompanied by a host escort. This "challenge culture" is an essential complement to technical visitor management controls: if employees are trained to politely but directly question any unescorted visitor, tailgating through a visitor entry process becomes significantly more difficult.

Social engineering attacks frequently exploit visitor management weaknesses. Common pretexts used by penetration testers and actual attackers include: posing as an IT vendor servicing equipment (exploiting the assumption that IT contractors move freely through facilities), arriving as a delivery person (exploiting the tendency to grant quick access to avoid disrupting operations), or claiming to be a scheduled visitor whose appointment was misrecorded (exploiting reception's desire to be helpful and accommodating). Organizations that do not enforce pre-authorization requirements or that routinely grant access to unverified visitors are providing attackers with a low-friction entry path.

The insider threat dimension of visitor management is equally important. Employees who are under investigation, recently terminated, or planning unauthorized information disclosure may use the visitor management system to introduce external accomplices. This is why access privileges for terminated employees must be revoked before the employee departs (not after), and why visitor pre-authorization must come from a current, active employee who can be held accountable for the visitor's conduct.

Physical penetration testing is a legitimate security service in which testers attempt to bypass physical controls by impersonating maintenance staff, delivery drivers or auditors. The question, as in Schneier's distinction between security theater and effective security, is always whether controls stop a determined, skilled adversary, not merely an unskilled one.
:::

%%%

---
unit: USB
code: USB
title: Tool Spotlight, USB Drop Attacks and Rogue Devices
---
:::callout style=soft
A **USB drop attack** is a social engineering and physical security exploit in which an attacker leaves a malicious USB device in a public or semi-public location near the target organization, relying on human curiosity to cause an employee to plug it into a corporate system, executing the attacker's payload.
:::

:::image src="images/10_usb_drop_attack.png" alt="Attack scenario illustration: top panel shows a USB drive lying in a parking lot labeled 'Q3 Salary Data'; middle panel shows an employee picking it up and inserting it into a laptop; bottom panel shows a network diagram with the laptop as a beachhead connecting back to an attacker's command-and-control server, dotted red lines show lateral movement across the internal network from the initial foothold" width=full caption="The USB drop attack turns human curiosity into a network intrusion vector, a single curious employee who plugs in a found device can provide an attacker with a foothold inside a network that is completely protected at the perimeter" 
:::

:::table
| Tool / Device         | Capability                                        | Detection Difficulty |
|-----------------------|---------------------------------------------------|----------------------|
| USB Rubber Ducky      | Emulates HID keyboard; types pre-programmed keystrokes at 1000 WPM | High (looks like USB drive) |
| Bash Bunny            | Multi-stage attacks; network spoofing, credential harvesting | High |
| O.MG Cable            | Weaponized charging cable with embedded Wi-Fi implant | Very High (looks like legitimate cable) |
| LAN Turtle            | Network implant disguised as USB Ethernet adapter | High |
| Malicious Charging Kiosk | Juice jacking via public USB charging port | Very High |
:::

:::steps heading="Defending Against Rogue USB Devices"
1. Enforce USB port lockdown via Group Policy or endpoint security tools, prevent all unauthorized USB storage devices from mounting
2. Deploy USB device control software (e.g., Symantec DCS, Microsoft Defender for Endpoint) that allowlists approved hardware IDs
3. Disable USB ports physically (epoxy fill or locking inserts) on systems in public-facing or unmonitored locations
4. Conduct user awareness training specifically addressing USB drop attacks; use simulated drop exercises to measure employee response
5. Monitor endpoint logs for unexpected USB device insertion events; alert on new device types not seen before
6. Implement network micro-segmentation so that a compromised endpoint's lateral movement capability is limited
:::

:::notes
The USB drop attack exploits one of the most consistently documented behaviors in security research: human curiosity combined with a desire to be helpful. A 2016 study by researchers at the University of Illinois, Urbana-Champaign ("Users Really Do Plug in USB Drives They Find") demonstrated that when 297 USB drives were dropped in public locations on a university campus, 45-98% were picked up and plugged in, with many users accessing files on the device. The study found that drives labeled with organizational labels (such as "Salary Data" or "Confidential") had higher plug-in rates than unlabeled drives, labels that suggest the drive belongs to someone, and implies returning it is the helpful thing to do.

From a technical perspective, the USB drop attack is effective because USB Human Interface Devices (HIDs), keyboards, mice, are trusted by operating systems by default and do not require user approval to begin sending input. A device like the Hak5 USB Rubber Ducky (CVE-2022-33004 covers a related attack vector) appears to the operating system as a USB keyboard and can type a pre-programmed sequence of keystrokes at speeds exceeding 1,000 words per minute, faster than any human typist and fast enough to execute a multi-stage attack payload in seconds before the user notices anything is happening. Defenses that rely on user awareness ("the user should notice something is happening") are insufficient against HID injection attacks because the attack completes before the user has time to react.

Juice jacking, the exploitation of public USB charging ports to exfiltrate data or install malware, deserves special mention because it targets a behavior that is ubiquitous and difficult to change: charging mobile devices in airports, hotels, and convention centers. The attack is possible because USB cables that carry power also carry data, and a malicious charging kiosk can initiate a data transfer or malware installation while appearing to simply charge the device. The FBI and CISA have both issued advisories recommending the use of AC power adapters rather than USB charging kiosks, and commercial "USB condom" devices, which pass power but block data pins, are a practical countermeasure for travelers.

Organizational countermeasures must address both the human and technical dimensions. User awareness training should include simulated USB drop exercises, a practice increasingly common in corporate security assessments, in which IT or security teams distribute mock USB drives in the parking lot or common areas and measure what percentage of employees plug them in, what percentage report them to security, and what percentage discard them. This creates a measurable baseline for the organization's human-layer vulnerability and provides data to justify investment in USB port lockdown controls.

Stuxnet (2010) is the best-known case of malicious USB delivery: because the target centrifuge networks were air-gapped, the payload reached them on infected drives carried by contractors with legitimate access, and it executed automatically on insertion by exploiting a Windows shortcut-handling flaw (CVE-2010-2568). Even air-gapped environments are vulnerable to malware delivered on removable media.
:::

%%%

---
unit: Checkpoint
code: CHK1
title: Mid-Lecture Checkpoint, Physical Security Concepts
---
:::callout style=soft
Pause and verify your understanding before moving forward. These questions reflect CompTIA Security+ SY0-701 exam objectives for the physical security domain.
:::

:::image src="images/10_checkpoint_quiz.png" alt="Illustration of a student at a desk reviewing flashcards, with icons representing each question topic: a card skimmer for Q1, a door sensor for Q2, a laptop with flames for Q3, a fire suppression nozzle for Q4, and a concentric ring diagram for Q5, each icon labeled with the corresponding question number" caption="Checkpoint questions are drawn directly from Security+ SY0-701 physical security objectives, if any answer is uncertain, revisit the relevant slide before proceeding" width=full
:::

:::list heading="Check Your Understanding" style=plain
- **Q1**: An attacker installs a thin overlay device on an ATM that reads card data and captures PINs via a hidden camera. What type of attack is this?
- **Q2**: Your organization uses badge readers at all entry points. An employee holds the door for a colleague who forgot their badge. What control would have prevented the unauthorized entry most effectively?
- **Q3**: A laptop encrypted with BitLocker is left unattended in a hotel room and an attacker modifies the bootloader to capture the passphrase on next login. What attack is described?
- **Q4**: A server room uses water-based sprinkler suppression. What is the primary security concern with this design in a data center environment?
- **Q5**: Which NIST SP 800-53 control family addresses physical and environmental protection?
:::

:::table
| Question | Answer | Explanation |
|----------|--------|-------------|
| Q1 | Card skimming (hardware tampering) | Overlay device on ATM card slot, physical tampering attack targeting payment systems |
| Q2 | Mantrap / airlock | A mantrap with single-occupancy enforcement would physically prevent the second person from passing without independent authentication |
| Q3 | Evil maid attack | Brief unsupervised physical access to install a bootloader modification, a firmware-level persistence technique |
| Q4 | Water damages electronic equipment | Fire suppression for data centers should use clean agents (FM-200, Novec 1230) that don't damage electronics |
| Q5 | PE, Physical and Environmental Protection | NIST SP 800-53 PE control family covers all physical and environmental security controls |
:::

:::notes
This mid-lecture checkpoint is designed to consolidate understanding of the physical security concepts covered so far before moving into deeper content on secure facility design, mobile device security, and compliance frameworks. Use these questions as a self-assessment, if any answer is unclear, the relevant slides should be reviewed before proceeding.

The checkpoint questions align directly with the CompTIA Security+ SY0-701 exam objectives in domain 2.4 "Explain the importance of physical security" and domain 4.1 "Given a scenario, apply common security techniques to computing assets." Physical security questions on the Security+ exam typically present a scenario describing a physical threat and ask the test-taker to identify the attack type, the most appropriate control, or the correct framework reference.

A common mistake in Security+ exam questions is confusing the classification of controls. The mantrap is a preventive control (it prevents tailgating from occurring), while CCTV is a detective control (it detects and records what occurs, but does not prevent it). The distinction between preventive, detective, and corrective controls is tested across multiple domains, and physical security controls provide some of the most intuitive examples because the physical mechanism makes the control type immediately obvious.

Regarding Q4 on water-based fire suppression: the concern is not that water suppression systems should never be used in facilities with computing equipment, but that they should not be the primary suppression agent for areas where electronic equipment is present and operating. Pre-action sprinkler systems, which require both a heat detection signal and a secondary confirmation before releasing water, are more appropriate than traditional wet-pipe or dry-pipe sprinkler systems, and even then, clean agent systems are preferred for high-value equipment rooms. The key principle is that fire suppression effectiveness must be balanced against the damage the suppression agent itself causes to the protected assets.

:::

%%%

---
unit: Misconceptions
code: FAQ
title: Common Misconceptions About Physical Security
---
:::callout style=soft
Physical security is often treated as "common sense", which leads to systematic underinvestment and incorrect assumptions about what controls actually protect against. Correcting these misconceptions is as important as learning the controls themselves.
:::

:::image src="images/10_physical_security_misconceptions.png" alt="Six thought bubbles each containing a misconception (shown with red X): 'Our building is locked, so we're secure'; 'Encryption makes physical theft irrelevant'; 'Security cameras deter all attackers'; 'Our badges can't be cloned'; 'Visitors always identify themselves honestly'; 'Physical security is IT's problem', each bubble connected by an arrow to a correction statement below it" caption="Misconceptions about physical security create systematic blind spots, the assumptions that feel most obviously true are often the ones most worth examining" width=full
:::

:::table
| Misconception | Why It's Wrong | Correct Understanding |
|---------------|----------------|----------------------|
| "Full-disk encryption makes theft irrelevant" | Pre-boot authentication weakness (TPM-only mode) still allows access on powered-on device | Encryption protects data-at-rest; TPM+PIN required to protect against evil maid; MDM remote wipe protects against physical access to powered-on devices |
| "Our badges use RFID so they can't be cloned" | Standard 125 kHz HID Prox cards are trivially cloned with a $20 device (Proxmark3) | Only HF cards with cryptographic challenge-response (MIFARE DESFire, iCLASS SE) provide meaningful anti-cloning protection |
| "Security cameras deter all attackers" | Determined attackers plan around visible cameras; nation-state and sophisticated criminal actors disable or blind cameras | CCTV deters opportunistic attackers; for high-security environments, camera tamper detection and redundant coverage are required |
| "Physical security is not IT's concern" | Physical access to IT assets directly enables logical compromise | Physical and logical security are inseparable; IT must define requirements for physical protection of systems |
| "Our data center is locked so the servers are safe" | Insider threat, supply chain tampering, and maintenance access bypass perimeter controls | Layered access control including zone restrictions for maintenance personnel and hardware integrity verification are required |
:::

:::notes
Physical security misconceptions arise from several sources: intuition-based security thinking ("it feels secure"), inadequate threat modeling that considers only external attackers rather than insiders or supply chain threats, and organizational silos that treat physical security as a facilities function separate from IT security. Each of these misconceptions represents a systematic gap that adversaries understand and exploit.

The RFID badge cloning misconception deserves extended discussion because it is both extremely common and extremely consequential. The majority of deployed access control systems in commercial buildings use 125 kHz proximity (Prox) cards, the same technology used in building access systems since the 1990s. These cards respond to reader queries with a fixed, unencrypted serial number and do not support any cryptographic authentication. A Proxmark3 device, available for approximately $300 and widely used by security researchers, can silently clone the credential from a standard HID card at distances of several centimeters while the card is still in someone's pocket or wallet. The attack takes less than a second and requires no physical contact. Organizations that believe their badge system prevents unauthorized access based on the mere fact that it is electronic and requires a badge are operating under a false assumption.

Modern high-frequency (13.56 MHz) smart card systems that implement cryptographic mutual authentication, such as MIFARE DESFire EV2 or HID iCLASS SE, provide genuine protection against cloning because the card and reader exchange cryptographic challenges that cannot be replayed without knowledge of the shared secret key. The card never transmits its credential in plaintext. Organizations upgrading aging access control infrastructure should prioritize migration to cryptographically protected card technologies as a primary security improvement.

The "physical security is not IT's concern" silo is particularly dangerous in organizations where physical security reports to facilities management rather than to the CISO's organization. In this model, physical security decisions, including the selection of access control systems, CCTV retention policies, and data center physical design, are made without input from information security practitioners who understand the threat model for the IT assets those physical controls are protecting. NIST SP 800-53 addresses this explicitly by placing the PE control family within the same framework as logical security controls, making the connection between physical and logical security an explicit organizational requirement rather than an optional best practice.

"Encryption makes physical theft irrelevant" is false in a way the Security+ exam tests. A device with TPM-only BitLocker and no PIN that is stolen while powered on decrypts transparently at boot, giving immediate access. Full-disk encryption protects only a device stolen while powered off, and only when configured with pre-boot authentication.
:::

%%%

---
unit: Comparison
code: CMP
title: Physical vs. Logical Security Controls, Comparison
---
:::callout style=soft
Physical and logical security controls address the same fundamental objectives, confidentiality, integrity, and availability, but through different mechanisms. Understanding how they map to each other reveals coverage gaps and prevents the false assumption that strong logical controls make physical controls unnecessary.
:::

:::image src="images/10_physical_vs_logical.png" alt="Two-column comparison diagram: left column 'Physical Controls' with icons for lock, camera, mantrap, fire suppression, badge reader, and cable lock; right column 'Logical Controls' with icons for firewall, IDS, access control list, backup system, authentication server, and encryption, connecting lines between columns show equivalent purpose: lock↔authentication, camera↔audit log, mantrap↔network segmentation, fire suppression↔backup/DR, badge reader↔identity provider, cable lock↔device encryption" caption="Physical and logical controls are functionally complementary, each addresses threats that the other cannot, and neither is a substitute for the other" width=full
:::

:::table
| Security Objective | Physical Control          | Logical Equivalent          | What Each Misses                            |
|--------------------|---------------------------|-----------------------------|---------------------------------------------|
| Authentication     | Badge / biometric reader  | Password / MFA              | Badge stolen; password phished              |
| Access Control     | Locked door / mantrap     | Firewall / ACL              | Door bypassed via tailgate; firewall bypassed via insider |
| Audit / Logging    | CCTV footage              | System access logs          | Camera has blind spot; log may be deleted   |
| Data Protection    | Cable lock / locked cabinet| Encryption                 | Cable cut; encryption bypassed via physical access to running device |
| Availability       | UPS / fire suppression    | Backup / disaster recovery  | Power failure cascades; data exists but system is inaccessible |
| Intrusion Detection| Motion sensor / guard     | IDS / SIEM                 | Sensor has coverage gaps; IDS misses physical-only attacks |
:::

:::notes
The comparison between physical and logical security controls reveals a fundamental principle that is easy to state but difficult to internalize: physical and logical security controls protect against distinct but overlapping threat categories, and neither category is a superset of the other. A strong physical security program cannot compensate for weak authentication systems, and a strong logical security program cannot compensate for an unlocked server room.

Consider authentication as an example. A badge-based physical access control system authenticates individuals to a physical space, it answers the question "is this person authorized to enter this room?" A password or MFA system authenticates individuals to an information system, it answers "is this person authorized to use this application or access this data?" These are different questions with different failure modes. Badge-based systems fail when badges are stolen, cloned, or shared. Password-based systems fail when passwords are phished, guessed, or stolen from a database breach. An organization that has excellent physical access control but weak password hygiene is vulnerable to remote attacks. An organization with strong passwords and MFA but poor physical access control is vulnerable to attackers who gain physical access to devices.

The audit and logging comparison is particularly instructive for understanding forensic investigation capabilities. CCTV footage provides a visual, real-time-timestamped record of who was physically present in a space, which is invaluable for investigations but requires continuous monitoring or event-triggered review to provide timely detection. System access logs provide a record of what credentials were used to authenticate to which systems at what times, but cannot identify if the person at the keyboard was the legitimate credential holder or an impostor. Combining physical and logical audit trails, cross-correlating badge access logs with system access logs, provides far stronger forensic capability than either alone. NIST SP 800-53 PE-6 Enhancement 1 specifically requires this cross-correlation for HIGH baseline systems.

The availability comparison highlights a gap that is often overlooked: logical backup and disaster recovery systems protect against data loss and system failure, but they do not protect against physical scenarios where the backup infrastructure itself is physically destroyed or unavailable. A comprehensive business continuity plan (per NIST SP 800-34) addresses both the logical and physical dimensions of availability, ensuring that critical data is backed up offsite and that physical facilities (including alternative work sites) are available if the primary facility is lost.

Organizations with mature logical security, strong SIEM, EDR and segmentation, often have physical gaps that undermine it. An intruder who reaches a network switch in an unlocked wiring closet can attach a tap or rogue access point inside the monitoring perimeter, bypassing the perimeter firewall entirely. Physical and logical security must be designed together.
:::

%%%

---
unit: Mobile
code: MOB
title: Mobile Device Physical Security
---
:::callout style=soft
Mobile devices, laptops, smartphones, and tablets, are the most physically vulnerable category of computing asset because they are designed to travel with their users into uncontrolled environments where physical security guarantees cannot be maintained.
:::

:::image src="images/10_mobile_physical_security.png" alt="Risk scenario map showing a mobile device in four high-risk physical environments: airport security checkpoint (device out of sight during X-ray), coffee shop (unattended while user gets a refill), hotel room (evil maid scenario), and shared office/co-working space (shoulder surfing), each location annotated with the specific physical threat and the corresponding countermeasure" caption="Mobile devices face elevated physical security risk in every environment outside the office, threat modeling must account for the full travel lifecycle, not just the endpoint configuration" width=full
:::

::::columns
::col::
:::list heading="Physical Threats Specific to Mobile Devices" style=plain
- Theft (opportunistic and targeted)
- Evil maid attack during hotel stays or border crossings
- Shoulder surfing in public spaces
- Juice jacking via malicious public charging ports
- Screen eavesdropping in open-plan workspaces
- Coercive access (compelled unlock at border crossings)
:::
::col::
:::steps heading="Mobile Device Hardening for Physical Security"
1. Enable full-device encryption with a strong PIN or passphrase (not biometric-only for high-risk environments)
2. Configure remote wipe via MDM, test wipe capability before travel
3. Use a privacy screen filter to prevent shoulder surfing
4. Carry your own charger and cable; avoid public USB charging kiosks
5. Enable auto-lock with a short timeout (30 seconds) and require authentication to wake
6. Report loss or theft immediately to enable remote wipe before battery death
:::
::::

:::table
| Control               | Threat Addressed               | NIST / CompTIA Reference      |
|-----------------------|-------------------------------|-------------------------------|
| Full-disk encryption  | Data theft from stolen device  | NIST SP 800-124, BitLocker/FileVault |
| MDM remote wipe       | Data exposure on lost device   | NIST SP 800-124               |
| Privacy screen filter | Shoulder surfing               | NIST SP 800-46                |
| Pre-boot PIN          | Evil maid / coerced unlock     | NIST SP 800-147               |
| Device tracking       | Theft recovery and location forensics | Apple Find My, Microsoft Find My Device |
:::

:::notes
Mobile devices present a unique physical security challenge because they exist at the intersection of two environments with fundamentally different security postures: the controlled, monitored enterprise environment where physical access controls, surveillance, and procedural safeguards provide baseline protection, and the uncontrolled public environment, airports, hotels, coffee shops, conference venues, where none of those baseline protections apply. Security programs that focus exclusively on endpoint configuration without addressing the physical context in which mobile devices operate leave a significant gap.

NIST SP 800-124 "Guidelines for Managing the Security of Mobile Devices in the Enterprise" provides the primary federal guidance for mobile device security and explicitly addresses the physical dimension. The publication recommends that organizations establish mobile device security policies covering authentication, encryption, remote wipe, and the specific requirements for high-risk travel scenarios such as international travel to nations with known history of device compromise at border crossings.

Border crossing scenarios deserve specific attention. Multiple nations' border agencies have legal authority to compel travelers to unlock electronic devices for inspection, and in some jurisdictions, devices may be retained for extended examination without the traveler's presence. For employees traveling to jurisdictions where this risk is elevated, organizations should consider issuing travel-specific "loaner" devices that contain no sensitive data, have fresh OS installations, and are configured with temporary credentials that can be revoked upon return. Any data needed for the trip should be accessed via cloud services using temporary credentials rather than stored locally. Upon return, the device should be assumed potentially compromised and reimaged before reconnecting to corporate networks.

Shoulder surfing, the practice of observing someone's screen or keyboard from proximity, is a simple, low-technology attack that is often overlooked in threat models focused on technical sophistication. In open-plan offices, coffee shops, and airplanes, a determined observer can capture credentials, confidential documents, or sensitive communications simply by positioning themselves near the target. Privacy screen filters, optical films that restrict the viewing angle of a screen so that the display is only readable from directly in front, are a simple, inexpensive countermeasure. NIST SP 800-46 (Guide to Enterprise Telework, Remote Access, and Bring Your Own Device Security) recommends privacy screens as a control for employees working in public locations.

Juice jacking countermeasures have evolved beyond the simple recommendation to avoid public USB chargers. Commercial "USB data blockers", pass-through devices that break the data pins while allowing power pins to pass through, are available for under $10 and provide effective protection against data channel attacks from malicious charging hardware. Many modern smartphones also implement "USB restricted mode" (Apple iOS) or similar protections that disable the data channel after a defined idle period or when the screen is locked, providing software-layer protection against juice jacking attacks.

Biometric and PIN authentication trade off differently under physical threat. Biometrics resist shoulder surfing but can be compelled, a finger placed on a scanner or a face held to a device. A strong PIN is vulnerable to shoulder surfing but cannot be compelled without cooperation. For travel to high-risk jurisdictions, a PIN plus device encryption gives stronger protection against coerced access than biometrics.
:::

%%%

---
unit: SupplyChain
code: SC
title: Supply Chain Physical Security Threats
---
:::callout style=soft
Supply chain attacks compromise hardware or firmware before or during delivery to the target organization. Unlike attacks that require physical access to the deployed system, supply chain attacks exploit the trust relationship between organizations and their hardware vendors.
:::

:::image src="images/10_supply_chain_tampering.png" alt="Timeline diagram of a supply chain attack: factory (hardware manufactured with embedded implant or backdoored firmware); shipping (package intercepted in transit and device modified); distribution center (counterfeit component substituted for genuine part); delivery to organization (tampered device deployed in production); activation (implant phones home or activates upon deployment), each stage labeled with example attack and detection method" width=full caption="Supply chain attacks can occur at any point between hardware manufacture and deployment, detection requires hardware integrity verification at each stage, not just perimeter security after deployment"
:::

:::list heading="Supply Chain Physical Attack Vectors" style=plain
- Hardware implants installed during manufacturing (nation-state level capability)
- Interdiction, package interception and modification during shipping (documented by NSA TAILORED ACCESS OPERATIONS)
- Counterfeit component substitution, genuine parts replaced with substandard or malicious counterfeits
- Firmware preloading, devices sold with pre-installed backdoored firmware
- Evil peripherals, USB devices, keyboards, or mice shipped with embedded attack hardware
:::

:::steps heading="Supply Chain Integrity Controls"
1. Purchase hardware from authorized, vetted distributors with chain-of-custody documentation
2. Verify hardware against manufacturer-published tamper evidence indicators (holographic seals, serial number databases)
3. Perform firmware integrity verification against manufacturer-published hash values before deployment
4. Establish an approved hardware vendor list and require security assessments for new vendors
5. For critical systems: mandate hardware security assessments including visual inspection and firmware analysis before deployment
6. Implement NIST SP 800-161 (Supply Chain Risk Management) practices including supplier vetting and contract security requirements
:::

:::notes
Supply chain physical security represents one of the most challenging threat categories in information security because it attacks the trust relationship that organizations place in their hardware vendors. Unlike network intrusions that can be detected by monitoring systems, or physical intrusions that can be prevented by access controls, a supply chain compromise inserts a malicious component before the organization's security program even has an opportunity to observe it. The compromised hardware arrives looking identical to legitimate hardware, passes visual inspection, and may operate normally, the malicious capability is latent, activating only under specific conditions.

The most widely cited supply chain hardware threat is the NSA's TAILORED ACCESS OPERATIONS (TAO) unit's alleged practice of "interdiction", intercepting hardware shipments to government and corporate targets and modifying the hardware before allowing it to continue to the recipient. This practice was described in detail by Der Spiegel in 2013 based on documents provided by Edward Snowden, and includes photos of NSA personnel modifying Cisco networking equipment in transit. The revelations prompted significant industry response, with multiple hardware vendors implementing enhanced packaging with tamper-evident features to detect interdiction.

The 2018 Bloomberg Businessweek report claiming that Chinese manufacturers had implanted spy chips on Supermicro server motherboards destined for major U.S. companies and government agencies was denied by the named companies and has not been independently verified. However, regardless of the specific veracity of that report, the threat model it describes, malicious hardware implants of the size of a pencil tip, embedded in server motherboards during manufacturing, providing persistent covert access, is technically feasible and has been demonstrated in laboratory settings. NIST SP 800-161 was developed specifically to address this threat category at the organizational level.

Counterfeit component substitution is a supply chain threat that is well-documented and regularly discovered in real deployments. The U.S. Government Accountability Office has published multiple reports documenting counterfeit electronic components, including microprocessors, memory chips, and network equipment, being sold to government contractors through gray-market distribution channels. Counterfeit components may fail earlier than genuine parts (reliability risk) or may contain modified functionality (security risk). The Department of Defense requires contractors to purchase electronic components only from authorized, vetted distributors and to verify component authenticity for certain critical applications.

NIST SP 800-161 "Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations" provides a comprehensive framework for managing supply chain risks, organized around four practices: identify supply chain risks, assess supply chain risks, respond to supply chain risks, and monitor for ongoing supply chain threats. The framework emphasizes that supply chain security is not a one-time assessment but an ongoing program that must be integrated with the organization's broader risk management processes.

Hardware interdiction, tampering with equipment in transit, shows that even high-security organizations are exposed to supply chain attacks if hardware acquisition is not secured. Verifying that a newly delivered server has not been tampered with is difficult, which is the heart of the problem.
:::

%%%

---
unit: CPTED
code: CPT
title: Secure Facility Design and CPTED
---
:::callout style=soft
**Crime Prevention Through Environmental Design (CPTED)** is a multidisciplinary approach that reduces criminal opportunity through deliberate design of the physical environment. Applied to information security, CPTED principles guide facility design to make unauthorized access naturally more difficult while making authorized access and legitimate activity more visible.
:::

:::image src="images/10_cpted_principles.png" alt="Facility design diagram illustrating four CPTED principles: Natural Surveillance, receptionist desk positioned with clear sight lines to all entry points and no obstructions; Territorial Reinforcement, clear signage and transition zones marking the boundary between public lobby and restricted areas; Natural Access Control, single controlled entry corridor eliminating informal entry paths; Maintenance, well-lit, clean, clearly maintained exterior signaling active occupancy and management" caption="CPTED transforms the physical environment itself into a security control, a well-designed facility makes unauthorized access more difficult and observable without requiring additional personnel or technology" width=full
:::

::::columns
::col::
:::list heading="Four Core CPTED Principles" style=plain
- **Natural Surveillance**: Design spaces so occupants naturally observe each other, reduce blind spots, maximize sight lines, position common areas where they overlook entry points
- **Territorial Reinforcement**: Use design elements to clearly communicate boundaries between public, semi-public, and restricted zones, fencing, landscaping, signage, and lighting that signal "this is controlled space"
- **Natural Access Control**: Guide movement through deliberate design, single entry points, pathways that channel traffic through observable locations, elimination of informal paths around official entry
- **Maintenance**: Keep the environment in good repair, the "broken windows" principle; neglect signals opportunity
:::
::col::
:::callout style=soft
CPTED is particularly effective as a **deterrent and detection** layer because it shapes attacker behavior, a determined attacker who cannot observe a way to move undetected is more likely to abandon the attempt or be observed preparing it.
:::
::::

:::notes
Crime Prevention Through Environmental Design (CPTED) emerged from criminological research in the 1970s but has been incorporated into contemporary physical security standards including NIST SP 800-116, the Department of Defense Unified Facilities Criteria (UFC 4-020-01), and the U.S. General Services Administration's (GSA) Physical Security Criteria for Federal Facilities. The underlying insight is that criminal behavior is partly shaped by opportunity, environments that present obvious, unobservable paths to targets attract criminal activity, while environments that signal active presence, clear boundaries, and natural observation of all movement deter it.

Natural surveillance is the most widely cited CPTED principle and has the strongest empirical support. Research by Oscar Newman ("Defensible Space," 1972) demonstrated that housing project designs that allowed residents to naturally observe common areas from their windows experienced significantly lower crime rates than designs with isolated corridors and stairwells that created unobservable spaces. Applied to corporate facilities, natural surveillance means positioning reception desks to provide clear sight lines to building entries, designing open-plan office spaces that provide visibility of movement within the facility, placing server rooms in interior locations away from exterior windows that would allow outside observation of equipment, and ensuring that CCTV camera placement is informed by sight-line analysis rather than ad hoc positioning.

Territorial reinforcement translates to the physical security principle of clearly delineated security zones. When the boundary between public and restricted space is ambiguous, for example, a building lobby where the reception desk is not clearly positioned at the natural transition point between public entrance and restricted office space, unauthorized individuals may move through the transition without being challenged, either because they appear to belong or because no one is positioned to challenge them. Clear signage, physical barriers at zone transitions, and distinct visual design elements (such as different flooring or wall colors that mark the entry to restricted areas) make zone boundaries unambiguous and create natural challenge points.

Natural access control is the CPTED principle most directly analogous to access control systems. A facility designed with a single entry point for authorized staff, a separate visitor entry point monitored by reception, and no informal paths around these entry points is naturally more secure than a facility with multiple unmonitored doors that provide convenient shortcuts for employees but also provide unmonitored entry for unauthorized individuals. Loading docks, smoking areas, and service entrances are frequently overlooked as informal entry points, CPTED analysis of a facility specifically examines all possible entry paths, not just official ones.

The maintenance principle, sometimes called the "broken windows theory" applied to physical security, reflects the observation that visible signs of neglect signal that a facility is not actively managed and therefore an easier target. A burned-out security light that goes unreplaced for weeks, graffiti that is not removed, or a broken fence panel that is not repaired each signal that the security controls are not actively maintained. Conversely, a facility that is visibly well-maintained communicates active management and deters attackers who select targets based on perceived ease.

Crime Prevention Through Environmental Design (CPTED) is increasingly part of physical security assessments under ISO 27001 and NIST CSF. Facilities built for convenience rather than security can often be improved with minor changes, repositioning a reception desk, adding signage, improving lighting, or removing shrubbery that conceals entry points, without major renovation.
:::

%%%

---
unit: DataCenter
code: DC
title: Data Center Physical Security Standards
---
:::image src="images/10_datacenter_physical.png" alt="Annotated data center floor plan showing: dual-path power distribution with separate PDU feeds from separate utility feeds; hot-aisle/cold-aisle containment with blanking panels in all empty rack units; raised floor cable management with fire stopping; biometric-controlled server room entry with mantrap; CCTV with no blind spots at all rack aisles; out-of-band management network with physical network separation; generator room with fuel storage labeled with capacity and runtime" caption="Enterprise data center physical security integrates access control, environmental protection, power resilience, and physical layout design into a single coherent security architecture" width=full
:::

::::columns
::col::
:::list heading="Tier Classification (Uptime Institute)" style=plain
- **Tier I**: Single path power and cooling; no redundancy; 99.671% availability (~28.8 hrs downtime/yr)
- **Tier II**: Redundant components; single path; 99.741% availability (~22 hrs/yr)
- **Tier III**: Multiple paths; one path active; concurrent maintainability; 99.982% (~1.6 hrs/yr)
- **Tier IV**: Fully fault tolerant; simultaneous maintainability; 99.995% (~26 min/yr)
:::
::col::
:::list heading="Physical Security by Zone" style=plain
- **Security Operations Center**: 24/7 monitoring of all physical and logical access systems
- **Mechanical/Electrical Rooms**: Locked separately from IT space; authorized maintenance personnel only
- **Server Cage/Hall**: Biometric + card access; monitored aisles; no visitor access without escort
- **Network Points of Presence (PoP)**: Locked with audit log; tamper-evident cable management
- **Shipping and Receiving**: Separate physical zone; all inbound hardware verified before admission to IT space
:::
::::

:::notes
Data centers represent the highest-stakes physical security environment in most organizations because they concentrate the critical infrastructure that supports all digital operations. A physical security failure in a data center, whether through unauthorized access, environmental damage, or equipment tampering, can have immediate, large-scale impact on organizational availability and data integrity. This concentration of risk justifies significantly higher investment in physical security controls than is typical for general office environments.

The Uptime Institute's Tier Classification system provides a widely adopted framework for categorizing data center reliability and resilience, which is closely linked to physical security design. Higher tier levels require not only greater infrastructure redundancy but also more sophisticated physical security architectures. A Tier IV facility, the highest classification, must be able to maintain operations during any single component failure, scheduled maintenance, or physical intrusion attempt at any single physical location within the facility. This requires that physical security systems themselves be redundant: a physical security system that can be disabled by cutting a single power feed or network connection does not meet Tier IV standards.

Physical separation of security zones within a data center is a critical design principle that reflects the need to enforce least-privilege access to different functional areas. Mechanical and electrical infrastructure rooms, containing cooling equipment, UPS systems, generators, and power distribution equipment, are often overlooked physical security targets. An attacker who gains access to an electrical room can potentially disrupt or destroy power distribution without ever entering the server hall, causing a denial-of-service attack that the most sophisticated server room access controls cannot prevent. These rooms must be separately controlled from IT spaces with independent access authorization lists.

The shipping and receiving zone is a frequently underestimated attack surface. Hardware delivered to a data center should be inspected and verified against purchase orders before admission to the IT space, held in a staging area where environmental controls do not apply to the live infrastructure, and tracked through a chain of custody process that documents every handler. NIST SP 800-161 specifically recommends that organizations establish receiving procedures that include visual inspection for tampering evidence, serial number verification against manufacturer records, and firmware integrity verification before deployment.

PCI DSS Requirement 9 (Restrict Physical Access to Cardholder Data) provides specific physical security requirements for environments that process payment card data, including: restricting physical access to systems in the cardholder data environment, logging and monitoring all physical access, protecting point-of-sale devices from tampering and substitution, and implementing a formal media destruction policy for all media containing cardholder data. Organizations seeking PCI DSS compliance will be assessed against these physical security requirements during their QSA (Qualified Security Assessor) audit.

Large cloud providers publish their data center physical security architecture. Because the provider's physical controls are the foundation of a customer's cloud security stack, understanding what the provider handles and what the customer still owns is essential to shared-responsibility analysis.
:::

%%%

---
unit: Checkpoint
code: CHK2
title: Checkpoint, Applied Physical Security Scenarios
---
:::callout style=soft
These scenario-based questions simulate the applied format of CompTIA Security+ SY0-701 performance-based questions on physical security. Work through each scenario before reviewing the answer.
:::

:::image src="images/10_applied_checkpoint.png" alt="Illustration of four scenario vignettes arranged in a 2x2 grid: top-left shows a construction worker in a hard hat badge-in at a corporate entry; top-right shows a server room with a UPS alarm flashing; bottom-left shows a laptop on a hotel bed with a tamper-evident sticker on the hinge; bottom-right shows an IT technician holding two USB drives, one labeled 'decommissioned drive'" caption="Applied physical security questions require selecting the correct control for a specific threat scenario, the answer depends on identifying the specific vulnerability before selecting the mitigation" width=full
:::

:::list heading="Scenario Questions" style=plain
- **Scenario A**: A contractor working on HVAC installation requests unescorted access to the server room because they find it "inconvenient" to wait for an escort. What policy should the security team enforce, and what NIST control supports it?
- **Scenario B**: A power outage lasts 45 minutes. The UPS kept servers running for 10 minutes before the generator started, but three minutes elapsed between UPS exhaustion and generator power, during which systems lost power. What control gap does this reveal?
- **Scenario C**: An employee traveling internationally returns and reports their laptop was examined at the border. They were required to unlock the device. What immediate actions should the security team take?
- **Scenario D**: An IT technician is decommissioning hard drives from servers that held PII data. They plan to delete all files and reformat the drives before donating them to a local school. Is this sufficient? What standard applies?
:::

:::table
| Scenario | Correct Answer | Rationale |
|----------|----------------|-----------|
| A | Enforce escort policy; no exceptions, PE-8 (Visitor Access Records) and PE-3 (Physical Access Control) require that all visitors be escorted in restricted areas | Operational convenience cannot override security policy; the exception to the escort requirement IS the vulnerability |
| B | Automatic Transfer Switch (ATS) delay exceeds UPS runtime buffer, power continuity plan has a gap; immediate: repair/replace ATS or extend UPS runtime; long-term: test failover under load | Environmental control gap: UPS and generator exist but integration timing is misconfigured |
| C | Assume device may be compromised; initiate remote wipe or quarantine; issue a replacement device; conduct forensic review of the returned device before reconnecting to corporate networks | Border crossing coercive access is an evil maid scenario, any device that left the user's control must be treated as potentially compromised |
| D | No, deletion and reformatting do not constitute adequate media sanitization for PII; NIST SP 800-88 requires physical destruction (shredding) or cryptographic erasure for drives containing PII before disposal | Drive data is recoverable after reformatting with standard forensic tools; donation = disclosure |
:::

:::notes
These applied scenario questions reflect the performance-based question format that CompTIA Security+ SY0-701 increasingly emphasizes, rather than simple recall of definitions, candidates must identify the vulnerability in a described scenario, select the appropriate control, and reference the applicable standard or framework. Practicing with scenario-based questions develops the applied reasoning skills that separate candidates who understand security principles from those who have merely memorized terminology.

Scenario A addresses the universal tension between operational convenience and security policy. The escort requirement for visitors in restricted areas exists specifically to prevent scenarios in which a visitor, regardless of their claimed identity or purpose, gains unsupervised access to sensitive equipment. A legitimate HVAC contractor has no need to be unescorted in a server room; the work can always be performed with an escort present. When an individual requests an exception to the escort policy, especially using pressure ("it's inconvenient"), this should be treated as a potential social engineering attempt and the request should be denied with a clear policy reference. The security team should document the request and the denial.

Scenario B illustrates the importance of testing environmental controls under realistic failure conditions. Organizations frequently implement UPS systems and generators but fail to test the complete failover sequence, particularly the Automatic Transfer Switch (ATS) timing, to verify that the transition from utility power to generator power occurs without a gap that exceeds the UPS battery runtime. The correct remediation depends on the specific gap: if the ATS switching time is 3 seconds and the UPS can sustain 10 minutes of load, there should be no gap, but if the UPS runtime has degraded due to aging batteries (a common operational issue), the 3-minute gap in Scenario B may indicate battery degradation rather than ATS misconfiguration. Regular load testing of UPS systems per IEEE Std 1188 (IEEE Recommended Practice for Maintenance, Testing, and Replacement of Valve-Regulated Lead-Acid (VRLA) Batteries) is essential.

Scenario C reflects the reality that border crossing coercive access is a known risk for business travelers to certain jurisdictions, and organizations must have a defined incident response procedure for it. The key principle is that any device that has been out of the user's physical control and has been unlocked or accessed by a third party must be assumed potentially compromised at the firmware level, an adversary with physical access and device unlock can install a firmware-level implant that survives OS reinstallation and is undetectable without specialized forensic analysis. Remote wipe addresses the immediate risk of data exposure but does not address firmware-level compromise. The correct response is to quarantine the device, issue a replacement, and conduct forensic analysis before allowing the returned device to reconnect to corporate networks.

Scenario D addresses a persistent and costly misconception about media disposal. File deletion and reformatting remove file system metadata (directory entries, allocation tables) but leave the underlying data on the storage medium unchanged and fully recoverable using freely available tools such as Autopsy, Recuva, or TestDisk. NIST SP 800-88 is unambiguous: for media that contained PII, Personally Identifiable Information, the minimum acceptable sanitization method is either Purge (ATA Secure Erase command, verified) or Destroy (physical shredding to ≤2mm particles). Donating reformatted drives containing PII to any recipient, even a charitable organization, constitutes a disclosure of personal data and may trigger breach notification obligations under applicable privacy law.

:::

%%%

---
unit: Locks
code: LCK
title: Lock Types and Physical Barrier Technology
---
:::callout style=soft
Physical locks are the oldest and most widely deployed physical access control mechanism. Modern security environments use multiple lock types in different contexts, selecting the appropriate lock technology for a given application requires understanding each type's strengths, vulnerabilities, and the attacks it is resistant to.
:::

:::image src="images/10_lock_types.png" alt="Comparison grid showing six lock technologies with labeled diagrams: pin tumbler deadbolt (showing pin stacks and shear line), cipher/combination padlock (showing dial and internal cam mechanism), electronic keypad lock (showing circuit board and solenoid release), smart card lock (showing RFID antenna and reader), biometric lock (showing fingerprint scanner optics), and high-security cylinder (showing additional security pins and anti-drill plate), each labeled with its primary vulnerability" caption="Lock technology selection must match the threat model, a lock that defeats picking may be vulnerable to bumping, shimming, or bypass, and all locks are vulnerable to physical force if the door frame is weak" width=full
:::

:::table
| Lock Type               | Primary Attack                    | Countermeasure / Upgrade Path         | Appropriate Use          |
|-------------------------|-----------------------------------|---------------------------------------|--------------------------|
| Standard pin tumbler    | Lock picking, bump key            | High-security cylinder (Medeco, Abloy)| Interior doors, low-risk |
| Key-in-knob (KiK)       | Bypassed by shimming / wrench attack | Upgrade to deadbolt               | Avoid for security-critical applications |
| Electronic keypad       | Code shoulder surfing, battery failure | Anti-eavesdrop keypad, backup power | Secondary doors, low-risk |
| Smart card / RFID       | Card cloning (125 kHz), tailgating | Cryptographic card (DESFire), anti-passback | Primary access control |
| Biometric               | Presentation attack, FAR spoofing | Liveness detection, dual-factor     | High-security inner zones |
| High-security cylinder  | Drilling, covert entry             | Anti-drill/anti-pick pins, audit logging | Server rooms, vaults     |
:::

:::list heading="Lock Bypass Techniques (for Threat Awareness)" style=plain
- **Lock picking**: Using tension wrenches and picks to manipulate pin stacks to the shear line
- **Bump key**: A specially cut key that causes all pins to briefly reach the shear line simultaneously when struck
- **Shimming**: Thin metal strip used to retract spring-loaded latches on knob locks
- **Under-door tool**: Retrieves an interior handle or lever from under a door gap without picking the lock
- **Relay attack**: Amplifies smart card signal between card and reader to enable unauthorized opening at distance
:::

:::notes
Lock selection is a fundamental physical security decision that is often made on the basis of cost or aesthetic preference rather than threat modeling. Understanding the attack techniques applicable to different lock types enables security practitioners to make informed decisions about which lock technologies are appropriate for specific applications and threat environments.

The pin tumbler lock, the basis of most household and commercial key locks, operates by aligning pin stacks to a shear line inside the cylinder when the correct key is inserted, allowing the cylinder to rotate and operate the locking mechanism. Lock picking exploits the mechanical tolerances inherent in pin tumbler designs: because the cylinder is never perfectly centered, applying rotational tension to the cylinder causes one pin stack at a time to bear weight against the shear line, allowing a picker to set each pin stack individually until all are at the shear line and the cylinder rotates. High-security cylinders (such as Medeco or Abloy Protec) address this by using angled or rotating pin stacks that must be set both to the correct height and to the correct angle, dramatically increasing the skill required for successful picking.

The bump key attack is particularly relevant to physical security practitioners because it can be performed by an unskilled attacker in seconds with a purpose-cut key blank and a mallet. The attack exploits Newton's third law applied to the pin stacks: striking a bump key inserted in the lock causes the pins to jump upward momentarily, and if rotational tension is applied at the exact moment all pins reach the shear line, the cylinder rotates. High-security cylinders with security pins (spool or serrated pins that create false set resistance) defeat bump key attacks by requiring the picker to feel and set each pin individually.

RFID card cloning deserves special emphasis because it represents the most commonly deployed but most widely misunderstood vulnerability in modern access control. Standard HID Prox cards (125 kHz), which remain the majority of deployed access control credentials globally, transmit an unencrypted, static serial number in response to any reader query. A Proxmark3 device can silently read and store this serial number from a card in someone's pocket within a few centimeters, and then transmit it to a compatible reader to gain access. The attack requires no special skill beyond operating the device, takes less than a second, and leaves no trace. Organizations that have invested in sophisticated biometric access control at server room entries but use standard Prox cards for building entry are protecting the inner perimeter while leaving the outer perimeter trivially bypassable. Upgrading to cryptographic cards with mutual authentication (MIFARE DESFire EV2 or HID iCLASS SE) eliminates the cloning vulnerability.

Physical barrier effectiveness depends not only on the lock but on the entire assembly, a high-security lock installed in a hollow-core door with a weak frame provides minimal additional protection because the door or frame can be defeated faster than the lock. Physical security assessments should evaluate not just the lock technology but the door material, frame construction, hinge security, and mounting hardware. ANSI/BHMA Grade 1 hardware standards define minimum performance requirements for commercial door hardware, and compliance with these standards should be a baseline requirement for security-critical installations.

Sophisticated electronic access control can be defeated in seconds by simple mechanical attacks: an under-door tool can catch an interior lever and open the door without touching the lock, leaving no entry in the access-control audit log. Assessments must evaluate bypass vectors that operate independently of the access-control system, not only the system itself.
:::

%%%

---
unit: Incident
code: INC
title: Physical Security Incident Response
---
:::callout style=soft
Physical security incidents, unauthorized access, theft, tampering, vandalism, or environmental emergencies, require a structured response process just as cyber incidents do. Many organizations have mature cyber incident response plans but lack equivalent physical security incident procedures.
:::

:::image src="images/10_physical_incident_response.png" alt="Incident response lifecycle adapted for physical security: Preparation (defined response procedures, contact trees, secure evidence collection kit); Detection/Identification (alarm activation, access log anomaly, visual observation, environmental alert); Containment (lock down affected area, disable compromised credentials, preserve physical evidence); Eradication (identify and remove threat actor or failed component); Recovery (restore access, replace compromised hardware, verify integrity); Post-Incident Analysis (root cause analysis, policy update, training update)" caption="Physical security incident response follows the same lifecycle as cyber incident response, the Preparation and Post-Incident Analysis phases are most commonly neglected, leaving organizations repeatedly vulnerable to the same attack type" width=full
:::

:::steps heading="Physical Intrusion Incident Response Steps"
1. **Detect**: Alarm activation, access log anomaly, CCTV alert, or personnel report triggers response
2. **Contain**: Lock down the affected zone immediately; disable access credentials that may have been compromised or cloned; preserve the scene for forensic investigation
3. **Notify**: Alert security operations, management, legal, and law enforcement as required by policy and local regulation
4. **Preserve Evidence**: Secure physical evidence (hardware, tamper evidence, written materials) before cleaning or remediation; preserve CCTV footage before it is overwritten by retention policy
5. **Investigate**: Correlate physical access logs with CCTV footage and logical system access logs; establish timeline; identify root cause
6. **Recover**: Restore normal operations; replace compromised hardware; update access credentials; repair physical damage
7. **Post-Incident Review**: Conduct formal lessons-learned analysis; update incident response procedures; revise physical security controls based on findings; conduct follow-up training
:::

:::notes
Physical security incident response is a domain that is frequently underdeveloped relative to cyber incident response in most organizations. The asymmetry exists partly because cyber incidents generate digital evidence that naturally flows into SIEM systems and incident management tools, while physical incidents generate physical evidence that requires deliberate collection and preservation processes that may not be defined. An organization that discovers a server room door has been forced open may not know whether to call facilities management, the security team, law enforcement, or all three, and the confusion itself may result in evidence being destroyed before it can be analyzed.

The NIST SP 800-61 "Computer Security Incident Handling Guide" provides the foundational incident response lifecycle that applies equally to physical and cyber incidents: Preparation, Detection and Analysis, Containment, Eradication and Recovery, and Post-Incident Activity. While NIST 800-61 focuses on computer security incidents, the framework maps directly to physical incidents: Preparation means having defined response procedures, trained responders, and required tools (evidence collection kits, documentation forms, secure storage for evidence) before an incident occurs.

Physical evidence preservation is the most time-critical and most commonly mishandled aspect of physical incident response. Physical evidence, including fingerprints, footprints, tamper evidence, hardware modifications, and written materials, can be destroyed in minutes by well-intentioned employees who clean the scene, touch surfaces, or move equipment before forensic documentation is completed. Response procedures must explicitly state that affected areas are to be treated as crime scenes until cleared by security or law enforcement, and must identify who has authority to clear the scene. Chain of custody documentation, recording who collected each piece of evidence, when, where, and how it was stored, is required for evidence to be admissible in subsequent legal proceedings.

CCTV footage is particularly time-critical because most systems overwrite recordings after a defined retention period. If a physical incident is identified three days after it occurred and the retention period is four days, there may be only 24 hours to preserve the relevant footage before it is overwritten. Incident response procedures should include an immediate step to preserve CCTV recordings covering the affected location for all timestamps in the incident window, copying them to secure storage that is not subject to the retention policy's automatic overwrite.

Regulatory notification requirements may apply to physical incidents that result in data exposure. GDPR Article 33 requires notification to the supervisory authority within 72 hours of becoming aware of a personal data breach, a physical intrusion that could have allowed access to systems containing EU personal data may trigger this requirement even if no confirmed data exfiltration occurred. Organizations must assess each physical security incident for potential data breach implications and engage legal counsel and privacy teams immediately when data exposure cannot be ruled out.

Post-incident analysis is the phase most commonly abbreviated or skipped, particularly when the immediate crisis is resolved and operational pressure to return to normal is high. This phase, which should include a structured lessons-learned session with all parties involved in the response, is where the most durable security improvements originate. Common findings from physical security post-incident reviews include: that the incident could have been detected earlier if logs had been reviewed more frequently; that access credentials should have been revoked sooner after the triggering event; that response procedures were unclear about who had authority to escalate; or that physical evidence was compromised by responders who were not trained in evidence preservation. Each finding should generate a specific, assignable corrective action with a defined completion date and owner.

Physical security incident response is generally underinvested: many organizations have no written procedure separate from their cyber incident plan. A simple procedure covering the most likely scenarios, unauthorized access, theft, fire and power failure, applies the concepts of this unit directly.
:::

%%%

---
unit: Summary
code: SUM2
title: Physical Security, Key Takeaways and Exam Prep
---
:::pullquote
Physical security is not a separate discipline from cybersecurity, it is the layer that determines whether every other security control has a chance to work.
:::

:::image src="images/10_key_takeaways.png" alt="Mind map with 'Physical Security' at the center, branching to eight labeled clusters: Threats (tailgating, theft, tampering, environmental), Controls (preventive/detective/corrective), Standards (NIST 800-53 PE, ISO 27001 A.11, NIST 800-88), Locations (perimeter, building, room, device), People (guards, escort policy, visitor management, training), Technology (biometrics, CCTV, mantraps, badge systems), Environment (fire suppression, cooling, UPS, redundancy), and Response (incident detection, evidence preservation, post-incident review)" caption="A complete physical security program integrates all eight clusters, gaps in any one area create exploitable vulnerabilities that sophisticated adversaries will find" width=full
:::

:::table
| CompTIA Security+ Objective | Key Concept | Slide Reference |
|-----------------------------|-------------|-----------------|
| 2.4, Physical Security | Tailgating, mantrap, anti-passback | Unauthorized Access, Mantrap Design |
| 2.4, Physical Security | Biometric FAR/FRR/CER | Biometric Authentication |
| 2.4, Physical Security | CCTV deterrence/detection/forensics | CCTV and Surveillance |
| 2.4, Environmental | UPS, generator, fire suppression | Environmental Controls |
| 2.4, Environmental | CPTED principles | Secure Facility Design |
| 4.1, Security Techniques | Encryption for theft mitigation | Theft, Mobile Device Security |
| 4.1, Security Techniques | NIST SP 800-88 media disposal | Dumpster Diving and Secure Disposal |
| 4.3, Vulnerability Management | Supply chain tampering | Supply Chain Physical Security |
:::

:::list heading="Five Things Every Security+ Candidate Must Know" style=plain
- **Tailgating vs. tailgating prevention**: tailgating exploits courtesy; mantrap + anti-passback prevents it
- **FAR vs. FRR**: FAR = unauthorized accepted (security failure); FRR = authorized rejected (availability failure); CER = where they cross
- **Evil maid = bootloader/firmware attack via brief physical access**: TPM+PIN + Secure Boot is the defense
- **NIST SP 800-88**: delete/reformat is NOT sufficient; Purge or Destroy required for sensitive data
- **Environmental controls are security controls**: fire suppression, cooling, and UPS protect availability, the "A" in CIA
:::

:::notes
This final summary slide consolidates the key concepts from the physical security unit and maps them directly to CompTIA Security+ SY0-701 exam objectives. Physical security is tested in multiple Security+ domains, not just as an isolated topic, it appears in questions about vulnerability management (supply chain), incident response (physical evidence), risk management (environmental controls and business continuity), and architecture and design (defense in depth, CPTED).

The five "must-know" items for the Security+ exam reflect the concepts most frequently tested in the physical security domain based on published exam objectives and candidate feedback. Tailgating prevention questions almost always test the candidate's ability to select the appropriate control from a list that includes both correct answers (mantrap, anti-passback) and common misconceptions (security cameras, which detect but do not prevent tailgating). Reading each answer choice carefully and identifying what the control does (preventive, detective, or corrective) before selecting is an essential exam strategy.

FAR, FRR, and CER are tested together because they represent the accuracy tradeoff inherent in biometric systems. Security+ questions typically present a scenario, for example, "a biometric system is rejecting authorized users too frequently; which metric should be adjusted?", and require the candidate to identify FRR as the metric that reflects rejection of authorized users and to understand that reducing FRR (making the system more permissive) will increase FAR (increasing the risk of accepting unauthorized users). The correct answer depends on the organization's risk tolerance and use case.

Media disposal (NIST SP 800-88) is tested in the context of both physical security and data security. The key distinction is that "clearing" (overwriting) provides protection against software-based recovery tools but not against laboratory-grade recovery, while "purging" (secure erase, degaussing for magnetic media) provides protection against laboratory recovery, and "destroying" (shredding, incineration) provides the highest assurance. The exam will present scenarios in which data sensitivity must be matched to disposal method, understanding the hierarchy of sanitization methods and when each is appropriate is essential.

Environmental controls as security controls is a conceptual bridge that many candidates miss. The CIA triad requires that security programs protect Confidentiality, Integrity, and Availability. Environmental controls, fire suppression, cooling systems, UPS, and generators, protect Availability. Treating them as "just facilities" rather than "security controls" reflects an incomplete understanding of the security domain. Security+ questions testing environmental controls often ask candidates to identify which control addresses which aspect of the CIA triad, or to select the appropriate control for a described availability threat.

The physical security unit as a whole has established that physical controls are not optional additions to an otherwise complete logical security program, they are the foundational layer on which every other security control depends. As the course progresses through network security, application security, and data security in subsequent units, the assumption throughout will be that the physical security layer is intact. The concepts covered in this unit explain why that assumption must hold, and what happens to the security stack when it does not.

On the Security+ exam, physical security questions often turn on precise terminology, such as the difference between a mantrap and a turnstile, or between the false acceptance rate (FAR) and false rejection rate (FRR). This precision separates passing and failing answers.
:::
