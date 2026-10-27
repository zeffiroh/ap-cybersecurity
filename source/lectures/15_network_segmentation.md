---
deck:
  title: Network Segmentation
  kicker: Class 15
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 15
  description: VLANs, isolation, and why a well-segmented network turns one breach into a contained incident.
  topics: [VLANs, Isolation, Secure Architecture, Defense in Depth, Reducing Attack Spread]
---

---
title: Network Segmentation
cover: true
---
:::text class=sub
If an attacker gets in, segmentation decides how far they can actually go
:::
::::columns
::col::
:::list heading="Core Segmentation Mechanisms" style=plain
- Virtual Local Area Networks (VLANs)
- Subnetting and routing controls
- Firewalls (stateful and next-gen)
- Network Access Control (NAC)
:::
::col::
:::list heading="Strategic Principles" style=plain
- Defense in Depth
- Principle of Least Privilege
- Zero Trust Network Architecture
- Microsegmentation
:::
::col::
:::list heading="Standards & Frameworks" style=chips
- NIST SP 800-207 (Zero Trust)
- ISO/IEC 27001/2
- NIST CSF
- MITRE ATT&CK (TA0008: Lateral Movement)
:::
::::
:::image src="images/15_network_segmentation_overview.png" alt="Corporate network architecture diagram divided into four isolated zones, DMZ, office VLAN, server VLAN, and guest network, with firewalls and routers enforcing boundaries between each segment, and color-coded traffic paths showing permitted versus blocked inter-zone communication" caption="Network segmentation architecture, dividing a single network into isolated zones so an attacker who breaches one zone cannot freely reach the others" width=full:::
:::
:::notes
Network segmentation is a foundational security control that divides a network into discrete, logically or physically isolated zones to limit the spread of cyber threats. The core idea is to enforce boundaries that restrict an attacker's ability to move laterally after an initial breach, a tactic commonly observed in real-world incidents such as those documented under MITRE ATT&CK's TA0008: Lateral Movement. By implementing segmentation, organizations apply the principle of least privilege at the network layer, ensuring that even if one segment is compromised, the attacker cannot easily access critical assets in other zones.

Segmentation can be implemented through various mechanisms. VLANs (IEEE 802.1Q) are commonly used at the data link layer to isolate broadcast domains, though they must be carefully configured with proper access control lists (ACLs) to prevent VLAN hopping attacks such as those exploited in CVE-2019-15987. Subnetting at the network layer, combined with strict routing rules and firewalls, adds another level of control. Modern approaches also include microsegmentation, which enforces granular policies at the workload level, often seen in software-defined perimeters and Zero Trust architectures.

Frameworks such as NIST SP 800-207 emphasize the importance of network segmentation within a Zero Trust model, where no implicit trust is granted based on network location. ISO/IEC 27001 also mandates network controls under Annex A.13 to protect information in networks. These standards guide organizations in designing segmentation strategies that align with broader risk management and compliance objectives.
:::

%%%

---
unit: Foundations
code: SEG
title: Why Segment a Network?
---

:::callout style=soft
**Network segmentation** is a defensive architecture strategy that partitions a network into logically or physically isolated zones to limit the spread of threats, reduce attack surfaces, and enforce security policies. By creating boundaries between systems, segmentation ensures that a compromise in one zone does not automatically lead to access across the entire network.
:::

:::pullquote
Remember lateral movement from Class 3? Segmentation is built to stop it cold.
:::

:::flow
Attacker achieves initial access on endpoint in Zone A
Lateral movement attempt begins, SMB, RDP, WMI probes issued toward adjacent segments
VLAN boundary and ACL encountered, unauthorized cross-segment traffic dropped
Alert generated in SIEM, security team notified of anomalous inter-VLAN probe
Attacker contained to Zone A, blast radius limited to the initially compromised segment
:::

::::columns
::col::
:::list heading="Key Security Goals of Segmentation" style=plain
- Contain breaches and limit blast radius
- Enforce least-privilege access
- Improve monitoring and control
- Meet compliance requirements (e.g., PCI DSS, HIPAA)
:::
::col::
:::list heading="Common Threats Mitigated" style=plain
- Lateral movement (e.g., SMB, WMI, RDP relays)
- Data exfiltration across zones
- Propagation of malware or ransomware
- Unauthorized access to critical assets
:::
::col::
:::list heading="Segmentation Benefits" style=plain
- Reduces attack surface
- Enhances forensic analysis
- Supports microsegmentation strategies
- Aligns with Zero Trust principles
:::
::::

:::image src="images/15_lateral_movement_blocked.png" alt="Side-by-side comparison diagram: on the left, a flat network where a single red compromised endpoint has unrestricted network paths to all other systems including finance servers and HR databases; on the right, a segmented network where VLAN boundaries and ACL-deny symbols block those same lateral paths, confining the attacker icon to the initial breach zone while other segments remain green and intact" caption="Flat vs. segmented network, in a flat topology lateral movement is unrestricted; in a segmented topology each VLAN boundary is a policy-enforced checkpoint that must be explicitly crossed" width=full:::
:::
:::notes
Network segmentation is a foundational security practice rooted in the principle of **defense in depth**. It is designed to counteract one of the most critical phases in the cyber attack lifecycle: **lateral movement**. As defined in the MITRE ATT&CK framework (TA0008), lateral movement techniques allow adversaries to move through a network after gaining initial access, seeking high-value targets such as domain controllers, databases, or executive systems. Without segmentation, attackers can exploit flat network topologies to pivot freely using protocols like SMB, WMI, or PowerShell remoting.

Segmentation enforces **network zoning**, where each zone is governed by access control policies that restrict traffic based on business need and risk level. This aligns with **NIST SP 800-207**, the Zero Trust Architecture model, which assumes no implicit trust and continuously validates every transaction. Similarly, **ISO/IEC 27001** Annex A.13 emphasizes network controls and segregation as key mechanisms for protecting information assets.

In real-world incidents, such as the **WannaCry ransomware outbreak (CVE-2017-0144)**, organizations with effective segmentation were able to limit the spread of the worm, whereas flat networks experienced widespread disruption. Segmentation also supports compliance frameworks like **PCI DSS Requirement 11.2**, which mandates network segmentation to isolate cardholder data environments.

Ultimately, segmentation transforms a single, vulnerable attack surface into multiple, smaller, manageable perimeters, each with its own monitoring, logging, and access control mechanisms. This layered approach significantly raises the cost and complexity of an attack, making it a cornerstone of resilient network design.
:::

%%%

---
unit: VLANs
code: VLN
title: VLANs (Virtual LANs)
---
:::callout style=soft
A **VLAN (Virtual Local Area Network)** is a logical grouping of devices within a network that behaves as if they are on separate physical LANs, even when connected to the same switching infrastructure. VLANs partition a single physical switch into multiple, isolated broadcast domains.
:::

:::list heading="Core Benefits of VLANs" style=plain
- **Broadcast Domain Isolation**: Limits broadcast traffic to within each VLAN, reducing network congestion.
- **Enhanced Security**: Segments traffic so that devices in one VLAN cannot directly communicate with those in another without a Layer 3 device.
- **Scalability and Flexibility**: Enables dynamic grouping of users and resources without physical reconfiguration.
- **Compliance and Risk Mitigation**: Supports regulatory frameworks such as NIST SP 800-53 and ISO/IEC 27001 by enforcing network segmentation.
:::

:::table
| VLAN ID | Purpose               | Example Use Case             |
|---------|------------------------|------------------------------|
| 10      | Finance Department     | Sensitive financial systems  |
| 20      | HR Department          | Employee records             |
| 30      | Guest Access           | Visitor or BYOD devices      |
| 99      | Management/IT          | Administrative control       |
:::

:::image src="images/15_vlan_architecture.png" alt="Physical switch hardware diagram with color-coded port groups: ports 1–4 labeled VLAN 10 Finance (green), ports 5–8 labeled VLAN 20 HR (blue), ports 9–12 labeled VLAN 30 Guest (orange), and ports 13–16 labeled VLAN 99 Management (grey), broadcast domain boundaries drawn around each group with IEEE 802.1Q tag labels on the trunk uplink port connecting to the router" caption="VLAN port assignment on a single physical switch, four isolated broadcast domains created through IEEE 802.1Q tagging, each color-coded group operating as an independent logical LAN" width=full:::
:::
:::notes
A VLAN (Virtual Local Area Network) is a foundational mechanism in modern switched networks that enables administrators to logically segment a physical network infrastructure into multiple, independent broadcast domains. This segmentation is achieved through the IEEE 802.1Q tagging standard, which inserts a 4-byte VLAN tag into Ethernet frames to identify which VLAN the frame belongs to. As a result, even if two devices are physically connected to the same switch, they will be isolated from each other unless they are assigned to the same VLAN or routed through a Layer 3 device.

This logical isolation is crucial for both performance and security. From a performance standpoint, VLANs reduce the size of broadcast domains, limiting the scope of broadcast traffic such as ARP requests, which can otherwise degrade network efficiency. From a security perspective, VLANs enforce a boundary that prevents devices in one VLAN from directly accessing traffic in another. This is particularly important in environments where sensitive data must be protected from less secure zones, for instance, isolating guest Wi-Fi traffic (VLAN 30) from internal corporate systems (VLAN 10).

However, VLANs are not inherently secure against all threats. Misconfigurations, such as VLAN hopping attacks (e.g., CVE-2019-12754), can allow malicious actors to traverse VLAN boundaries. Therefore, proper implementation requires adherence to best practices such as disabling unused VLANs, avoiding VLAN 1 for user traffic, and implementing inter-VLAN routing with access control lists (ACLs). These controls align with guidelines from NIST SP 800-53, particularly controls related to network segmentation (SC-7) and boundary protection.

In essence, VLANs are a critical component of defense-in-depth strategies, enabling organizations to enforce network micro-segmentation and reduce the attack surface within their infrastructure.
:::

%%%

---
unit: VLANs
code: VLN
title: How VLANs Work
---
:::flow
Device sends untagged traffic
Switch assigns VLAN ID (based on port or protocol)
Switch forwards traffic only within same VLAN
Inter-VLAN communication requires routing
:::

:::callout
VLANs logically segment a physical switch into multiple broadcast domains. Traffic is tagged with a VLAN ID (802.1Q standard), which determines its forwarding path. Inter-VLAN communication must pass through a Layer 3 device, enforcing policy control.
:::

:::image src="images/15_vlan_tagging_802q.png" alt="Annotated Ethernet frame diagram showing the IEEE 802.1Q VLAN tag inserted between the Source MAC address and EtherType fields, the 4-byte tag is exploded to show its three sub-fields: 3-bit Priority Code Point (PCP), 1-bit Drop Eligible Indicator (DEI), and 12-bit VLAN Identifier (VID), with a switch forwarding decision flowchart below illustrating how the VID value determines which output ports receive the frame and which are excluded" caption="IEEE 802.1Q VLAN tagging, a 4-byte tag inserted into each Ethernet frame carries the 12-bit VLAN ID that determines the frame's forwarding path through the switch fabric" width=full:::
:::
:::notes
Virtual Local Area Networks (VLANs) operate at Layer 2 of the OSI model and enable network administrators to create logically separate broadcast domains over a shared physical infrastructure. Defined primarily under the IEEE 802.1Q standard, VLANs allow switches to tag Ethernet frames with a 12-bit VLAN identifier (VID), supporting up to 4094 unique VLANs (0 and 4095 are reserved). When a device sends traffic, the switch assigns a VLAN tag based on the ingress port configuration or through protocol-based classification.

Once tagged, the switch uses the VLAN ID to determine the forwarding table for that frame. It will only forward the frame to ports that are members of the same VLAN, effectively isolating broadcast and multicast traffic within that segment. This containment reduces broadcast storms and improves network performance and security.

For traffic to move from one VLAN to another, it must traverse a Layer 3 routing device, typically a router or a Layer 3 switch. This inter-VLAN routing point acts as a policy enforcement point where access control lists (ACLs), firewall rules, or network address translation (NAT) can be applied. This design aligns with the defense-in-depth principle outlined in NIST SP 800-207, Zero Trust Architecture, where traffic between segments is not implicitly trusted and must be inspected.

VLAN misconfigurations have historically led to vulnerabilities such as VLAN hopping (e.g., CVE-2019-12754), where attackers exploit improper tagging to gain access to unintended network segments. Proper implementation requires adherence to standards such as IEEE 802.1Q and network hardening practices recommended by ISO/IEC 27001 and NIST guidelines.
:::

%%%

---
unit: Isolation
code: ISO
title: Isolation Strategies
---
::::columns
::col::
:::table
| Zone | Purpose |
|---|---|
| DMZ (Demilitarized Zone) | Hosts public-facing services, isolated from the internal network |
| Internal network | Houses sensitive systems, not directly reachable from the internet |
| Guest network | Isolated for visitor devices with no access to internal resources |
:::
::col::
:::callout
Network segmentation through isolation zones is a foundational security practice aligned with **NIST SP 800-207 Zero Trust Architecture** and **ISO/IEC 27001 Annex A.13**. These zones enforce least-privilege access and reduce attack surface by logically or physically separating systems based on trust levels and data sensitivity.
:::
::::

:::flow
External request arrives at perimeter firewall, evaluated against ingress policy
If request targets a public-facing service, routed to DMZ web or email server
DMZ server responds, internal network is never directly reachable from this path
If request targets an internal resource, second firewall evaluates authenticated credentials
Internal user reaches sensitive zone only via policy-approved, monitored routing path
Any deviation from approved path is logged and alerted in the SIEM
:::

:::image src="images/15_isolation_zones_dmz.png" alt="Three-zone network architecture diagram: the Internet is on the left, a perimeter firewall in the center-left, the DMZ zone in the middle containing a web server and email gateway icon, a second internal firewall on the right of the DMZ, and the internal network on the far right containing employee workstations and a database server, red X arrows show blocked direct attack paths from internet to internal network while green arrows show permitted traffic flows between zones with protocol labels (HTTPS, SMTP)" caption="DMZ isolation architecture, two firewalls create a buffer zone that exposes public services without granting attackers direct access to the trusted internal network" width=full:::
:::
:::notes
Network isolation strategies are essential components of a defense-in-depth security model. They involve the logical or physical separation of network segments to limit the propagation of threats and restrict unauthorized access to sensitive systems. This approach aligns with **NIST Special Publication 800-207**, which emphasizes the principles of Zero Trust Architecture, where no implicit trust is granted to any entity inside or outside the network perimeter.

The **Demilitarized Zone (DMZ)** is a semi-trusted network segment positioned between the internal network and the untrusted internet. It hosts services that must be accessible from the internet, such as web servers, email gateways, or FTP servers. By isolating these systems in the DMZ, organizations ensure that even if a server is compromised, attackers cannot directly access internal systems. The DMZ is typically protected by a combination of firewalls implementing strict ingress and egress rules, as outlined in **ISO/IEC 27033-3:2010**, which provides guidelines for network security architectures.

The **Internal Network** is the most trusted zone, containing sensitive systems such as databases, internal applications, and employee workstations. Access to this zone is strictly controlled and monitored, often requiring multi-factor authentication and encrypted communication channels. Network segmentation within the internal network may further isolate critical assets, such as financial systems or HR databases, in alignment with **NIST SP 800-53** access control policies.

The **Guest Network** is an isolated segment intended for temporary users, such as visitors or contractors. Devices connected to this network are typically restricted from accessing internal resources and are often subject to captive portal authentication and time-based access controls. This strategy mitigates the risk of lateral movement in the event of device compromise, a tactic commonly exploited in attacks such as those leveraging **CVE-2021-34527 (PrintNightmare)** or other lateral movement techniques.

These isolation strategies are not merely architectural preferences but are mandated by compliance frameworks such as **PCI DSS (Requirement 1.2.1)** for cardholder data environments and **HIPAA** for protecting electronic protected health information (ePHI). Effective implementation requires continuous monitoring, regular firewall rule audits, and integration with identity and access management (IAM) systems.
:::

%%%

---
unit: Strategy
code: DID
title: Defense in Depth, Revisited
---
:::callout style=soft
Defense in Depth is a foundational security principle that emphasizes layering multiple defensive controls to protect systems and data. In the context of network segmentation, this translates into structuring networks with multiple isolated zones, each enforcing its own access controls and monitoring mechanisms.
:::

::::columns
::col::
:::flow
Perimeter firewall
DMZ
Internal segmentation
Sensitive system
:::
::col::
:::list heading="Key Layers in Network Defense"
- **Perimeter Firewall**: First line of defense; filters traffic between untrusted and trusted networks.
- **DMZ (Demilitarized Zone)**: Isolated subnet for public-facing services; limits exposure of internal systems.
- **Internal Segmentation**: Logical or physical separation of internal network zones (e.g., HR, R&D, Finance).
- **Sensitive System Isolation**: Critical assets placed in highly restricted, monitored network segments.
:::
::col::
:::callout style=line
Each layer must function independently and enforce distinct security policies. A compromise at one layer should not automatically lead to a breach at the next.
:::
::::

:::image src="images/15_defense_in_depth_network.png" alt="Concentric circle diagram showing four defensive network layers from outermost to innermost: Perimeter Firewall (grey outer ring), DMZ (blue ring), Internal Segmentation (green ring), and Sensitive System Isolation (red core), a threat actor icon sits outside the outermost ring with labeled attack path arrows being blocked at each successive ring, with NIST SP 800-53 control references annotated at each layer boundary" caption="Defense-in-depth network layers, each concentric ring is an independent security control that an attacker must breach sequentially, raising the attack cost at every step" width=full:::
:::
:::notes
Defense in Depth is a strategic security model that originated in military doctrine and has since been widely adopted in information security. The principle is straightforward yet powerful: no single security control is infallible, so multiple independent layers of defense should be implemented to slow, deter, or stop adversaries. In the context of network segmentation, this translates into a structured, multi-tiered network architecture where each segment enforces its own access control and monitoring policies.

The first layer typically involves a **perimeter firewall**, which filters traffic between the external internet and the internal network. This firewall enforces coarse-grained rules to block known malicious traffic and restrict access to necessary services only. However, perimeter defenses alone are insufficient, as demonstrated by attacks such as those exploiting vulnerabilities like CVE-2021-44228 (Log4Shell), which can bypass edge protections if internal systems are not properly segmented.

The second layer often includes a **DMZ (Demilitarized Zone)**, a network segment that isolates publicly accessible services such as web servers and email gateways. By placing these systems in a DMZ, organizations limit the impact of a compromise. Even if a server in the DMZ is breached, attackers are still separated from the internal network by additional layers of segmentation.

Further internal segmentation subdivides the internal network into **logical or physical zones** based on function, sensitivity, or user roles. For example, systems handling financial data may be isolated from those used by the HR department. This limits lateral movement, an attacker who compromises one system cannot automatically access all others. Standards such as **NIST SP 800-207 (Zero Trust Architecture)** and **ISO/IEC 27001** emphasize the importance of network segmentation as a means to enforce least privilege and reduce attack surface.

Finally, the most sensitive systems, such as databases containing personally identifiable information (PII) or critical infrastructure controls, are often placed in **highly restricted segments** with enhanced monitoring, encryption, and access logging. This final layer ensures that even if earlier defenses are breached, critical assets remain protected.

The strength of defense in depth lies in the independence and diversity of its controls. Each layer should implement different types of protection (e.g., firewalls, intrusion detection systems, endpoint protection) and enforce distinct policies. This layered approach aligns with frameworks like the **MITRE ATT&CK Matrix**, which identifies lateral movement (TA0008) as a common tactic used by adversaries after initial compromise. Proper segmentation directly counters this tactic by increasing the cost and complexity of an attack.

Ultimately, defense in depth through network segmentation is not just about slowing attackers, it's about providing multiple opportunities for detection and response. It transforms a flat, vulnerable network into a series of controlled environments where security teams can detect anomalies, isolate threats, and respond effectively.
:::

%%%

---
unit: Containment
code: CON
title: Reducing Attack Spread
---
:::callout style=soft
Well-designed segmentation limits an attacker to the segment they actually breached, turning a potential organization-wide disaster into a contained incident.
:::

:::pullquote
Segmentation doesn't prevent the first breach. It controls what happens after.
:::

:::flow
Attacker compromises endpoint in Office VLAN
Lateral movement probes issued toward Server VLAN and Finance VLAN
VLAN ACL drops unauthorized cross-segment traffic at the Layer 3 boundary
Firewall logs generate alert, security team receives notification in SIEM
Incident response team isolates and quarantines the Office VLAN segment
Investigation and remediation proceed while Server and Finance VLANs remain fully operational
:::

:::image src="images/15_attack_spread_containment.png" alt="Network segmentation containment diagram showing five labeled VLAN segments arranged around a central firewall: Office VLAN contains a single red compromised endpoint icon, lateral movement arrows extend from it toward Server VLAN and Finance VLAN but are blocked by red shield-and-X ACL denial symbols at each segment boundary, adjacent Server, Finance, Guest, and DMZ segments remain green with 'Protected' labels, and a timeline bar below shows breach contained within minutes to the initial zone" caption="Segmentation limits blast radius, the attacker is confined to the initially compromised VLAN while adjacent high-value segments continue to operate normally" width=full:::
:::
:::notes
Here's the honest framing for segmentation: it's not really designed to stop the very first compromise. It's designed for what happens next. Even if an attacker fully compromises one device on one segment, well-designed isolation means they're stuck there, unable to freely reach payroll, customer databases, or critical infrastructure on a completely separate segment.

The principle behind attack spread reduction through segmentation is elegantly simple: grant access only where required, and the blast radius of any breach remains tightly bounded. This concept, enforcing the principle of least privilege at the network layer, is codified in **NIST SP 800-53 AC-4 (Information Flow Enforcement)**, which requires organizations to control information flows within and between interconnected systems in accordance with defined security policy. Equally, **NIST SP 800-207 (Zero Trust Architecture)** establishes that no implicit trust should be granted based solely on network location; every access request must be validated against policy regardless of whether the source is inside or outside a traditional perimeter.

Real-world incidents powerfully illustrate this principle. The **2013 Target Corporation breach** began with attackers gaining initial access through a third-party HVAC vendor's credentials, a classic supply-chain entry point. Because Target's point-of-sale (POS) systems were insufficiently isolated from the rest of the corporate network, attackers traversed from the HVAC monitoring systems directly to POS terminals, ultimately exfiltrating payment card data for approximately 40 million customers and an additional 70 million customer records. A properly segmented architecture isolating vendor access to a dedicated management VLAN with no routing to POS systems would have contained this breach to a single business-unit segment, turning a $200 million catastrophe into a significantly more limited incident.

Similarly, during the **WannaCry ransomware outbreak of 2017 (CVE-2017-0144)**, organizations with flat network topologies saw the SMBv1-exploiting worm propagate rapidly across entire corporate environments. Organizations with effective VLAN segmentation, separating manufacturing floors, administrative offices, and server infrastructure into distinct zones with firewall-controlled routing, reported significantly limited spread. **NIST SP 800-82 (Guide to Industrial Control Systems Security)** specifically emphasizes network segmentation as critical for protecting operational technology (OT) environments from exactly this threat class.

The **MITRE ATT&CK framework (TA0008: Lateral Movement)** documents over 17 specific techniques adversaries use to traverse network environments, from Pass-the-Hash (T1550.002) to exploitation of Remote Services (T1021). Each technique depends on reaching remote systems via the network. Segmentation transforms this challenge: instead of unlimited access across a flat topology, the attacker must identify and exploit a specific authorized routing path between segments, each monitored and controlled at the boundary.

**ISO/IEC 27001:2022 Annex A.8.22 (Segregation in Networks)** explicitly requires organizations to separate groups of information services, users, and information systems based on trust levels, reinforcing that segmentation is not merely a technical best practice but a formal compliance requirement for certified organizations.
:::

%%%

---
unit: Practice
code: ARC
title: Segmentation in Practice
---
:::table
| Segment | What lives there |
|---|---|
| Guest Wi-Fi | Visitor devices only |
| Office VLAN | Employee workstations |
| Server VLAN | Internal applications and databases |
| DMZ | Public website, public-facing email gateway |
:::

:::steps
1. **Inventory and classify assets** by sensitivity and business function, identify which systems handle regulated data (PII, PCI, PHI) and require the highest isolation level.
2. **Design the VLAN scheme**, assign VLAN IDs to each zone (e.g., Guest: VLAN 30, Office: VLAN 10, Servers: VLAN 20, DMZ: VLAN 50) and formally document the inter-VLAN routing policy.
3. **Configure switch access ports**, assign each physical port to the appropriate untagged VLAN; configure trunk ports to carry only explicitly permitted VLAN IDs (prune all others).
4. **Implement inter-VLAN routing with ACLs**, route between zones only through a Layer 3 switch or stateful firewall enforcing least-privilege policy; restrict the Office VLAN to approved protocols and ports when accessing the Server VLAN.
5. **Apply egress filtering at the DMZ boundary**, ensure DMZ servers cannot initiate unsolicited connections to the internal network; all DMZ-to-internal traffic must match an explicitly permitted rule or be dropped.
6. **Monitor, log, and audit**, collect inter-VLAN firewall logs in a SIEM, review ACL rules quarterly, and validate segmentation effectiveness through periodic internal penetration testing.
:::

:::image src="images/15_segmentation_in_practice.png" alt="Small organization network diagram with four labeled zones arranged around a central firewall/router core: Guest Wi-Fi VLAN (orange zone, captive portal icon, internet access only), Office VLAN (blue zone, employee workstation icons), Server VLAN (green zone, database and application server icons), and DMZ (purple zone, public web server and email gateway icons), thin green arrows show permitted inter-zone traffic flows with protocol labels (HTTPS, SMTP) and bold red X symbols show blocked direct cross-zone paths from guest to office or server segments" caption="Practical four-zone segmentation for a small organization, each zone enforces least-privilege access with firewall-controlled inter-VLAN routing and no direct guest-to-internal paths" width=full:::
:::
:::notes
Here's what a reasonably segmented small organization might actually look like. Guests are fully isolated. Employee workstations sit on their own VLAN, separate from servers. Servers holding real business data sit on yet another VLAN, with tightly controlled routing between them. And anything public-facing lives in the DMZ, kept apart from everything sensitive inside.

The four-zone model shown here, Guest Wi-Fi, Office VLAN, Server VLAN, and DMZ, represents a minimum viable segmentation architecture appropriate for small-to-medium organizations. Each zone boundary is an enforced policy checkpoint where all inter-zone traffic must pass through an authorized routing device, enabling inspection, logging, and access control. This architecture directly implements the concepts outlined in **NIST SP 800-41 Rev. 1 (Guidelines on Firewalls and Firewall Policy)**, which recommends firewall placement at every zone boundary with deny-by-default rulesets.

**Guest Wi-Fi isolation** is perhaps the highest-impact, lowest-cost control in this architecture. Consumer devices connecting to a business network represent an unmanaged endpoint risk, they may carry malware, lack current patches, or be operated by individuals with adversarial intent. By routing all guest traffic to an internet breakout with no routing to Office or Server VLANs, the organization ensures that a fully compromised guest device cannot reach internal systems. This is implemented by assigning guest wireless SSIDs to a dedicated VLAN (e.g., VLAN 30) and enforcing a captive portal with bandwidth throttling to prevent abuse.

The separation of the **Office VLAN from the Server VLAN** is equally critical. Many devastating ransomware attacks, including those executed by LockBit, BlackCat/ALPHV, and Cl0p, begin by compromising a workstation through phishing, then use RDP, SMB, or Windows Management Instrumentation (WMI) to traverse from workstations to servers. Access from the Office VLAN to the Server VLAN should be restricted to specific approved protocols on approved ports (e.g., TCP 443 for HTTPS to an internal intranet, TCP 1433 for database access only from authorized application servers) rather than permitting broad IP-to-IP communication.

The **DMZ** serves as the organization's published interface for the outside world. Services like web servers, email gateways, and VPN concentrators must be externally accessible but must never hold direct routing access to internal database or Office VLANs. Firewall rules governing the DMZ-to-Internal boundary should follow a deny-all default with explicitly approved exceptions only, a posture consistent with **NIST SP 800-53 SC-7 (Boundary Protection)** and **PCI DSS Requirement 1.3 (Prohibit Direct Public Access to Systems in the Cardholder Data Environment)**.

**ISO/IEC 27001:2022 Annex A.8.22 (Segregation in Networks)** mandates that organizations formally document their network segregation approach and review it periodically. Quarterly firewall rule audits, combined with automated network access control (NAC) solutions such as Cisco ISE or Aruba ClearPass, ensure that segmentation boundaries remain effective as the network evolves and new devices are added.
:::

%%%

---
unit: Summary
code: SUM
title: Containing the Breach You Couldn't Prevent
---
:::pullquote
VLANs and isolation don't make a network unbreachable, they make sure one breach doesn't mean every breach.
:::

:::list style=chips
- VLANs
- Isolation
- Defense in Depth
- Attack Spread
:::

:::image src="images/15_breach_containment_summary.png" alt="Abstract grid diagram representing a network as a nine-cell matrix of segments, the center cell is highlighted red and labeled 'Initial Breach Zone' with a small attacker icon confined within it, while thick VLAN boundary lines separate it from the eight surrounding cells labeled 'Protected Segment' in green, a small legend in the corner maps red to 'Compromised' and green to 'Operational'" caption="Segmentation as a containment strategy, the breach stays where it started while the rest of the organization continues to operate normally" width=full:::
:::
:::notes
Today's lesson sits comfortably alongside everything from firewalls to detection: no single layer is perfect, so the goal is making sure a failure in one layer doesn't cascade into a failure everywhere. Next class, we shift from the network itself to the devices sitting on it, malware and the attacks that target individual machines directly.

The central insight of this class, that segmentation's primary value lies not in preventing initial compromise but in containing its consequences, represents a fundamental shift from perimeter-centric thinking to a resilience-oriented security posture. This philosophical shift is articulated throughout **NIST SP 800-207 (Zero Trust Architecture)**, which explicitly states that network location is no longer a sufficient basis for granting trust. Every access decision must be evaluated individually, regardless of which network segment the requesting entity sits on, and all traffic between segments must be treated as potentially untrusted until verified.

This lesson connects directly to the broader cyber resilience frameworks emerging from NIST and ISO. **NIST SP 800-160 Volume 2 (Developing Cyber Resilient Systems)** describes four core resilience capabilities: anticipate, withstand, recover, and adapt. Network segmentation directly enables the "withstand" capability, the ability to continue operating in a degraded but functional state while a cyber incident is contained to a limited zone. An organization with properly segmented networks can isolate a compromised segment, redirect critical operations to unaffected zones, and maintain business continuity while the incident is investigated and remediated, all without taking the entire organization offline.

The financial and operational impact of segmentation failures underscores its business value. The **2017 NotPetya attack** (attributed to the Russian Sandworm group, exploiting the same CVE-2017-0144 EternalBlue vulnerability used by WannaCry) caused an estimated $10 billion in global damages. Maersk, the global shipping company, lost approximately $300 million and was forced to reinstall 45,000 PCs and 4,000 servers across 130 countries in ten days due to a flat, insufficiently segmented network architecture. Companies that had implemented more mature segmentation, separating logistics systems from office infrastructure and isolating regional networks from the global backbone, were able to contain damage to specific business units or geographic regions, demonstrating that segmentation investment directly translates to reduced financial exposure and faster recovery times.

Looking ahead to **Class 16**, the transition from network segmentation to malware and device-level attacks reflects the natural progression in defense-in-depth thinking. Once segmentation has been established at the network layer, the focus shifts to hardening individual devices within each segment, reducing the attack surface of each endpoint so that even when attackers achieve local access, their ability to execute payloads and establish persistence is constrained by host-level controls. These two layers, network segmentation and device hardening, form the backbone of a resilient enterprise security architecture compliant with **ISO/IEC 27001:2022** and **NIST CSF 2.0**, and together they define the environment that the next class's malware taxonomy is designed to attack.
:::

%%%

---
unit: VLANs
code: VLN
title: Trunk Ports vs. Access Ports
---
:::callout style=soft
Every switch port operates in one of two modes. **Access ports** carry traffic for a single VLAN and are used to connect end devices. **Trunk ports** carry tagged traffic for multiple VLANs simultaneously and connect switches, routers, and access points. Confusing the two is a classic misconfiguration that enables VLAN hopping attacks.
:::

:::table
| Feature | Access Port | Trunk Port |
|---|---|---|
| VLANs carried | Single (untagged) | Multiple (802.1Q tagged) |
| Connected to | End devices (PCs, phones, printers) | Switches, routers, APs |
| Frame tagging | No, tag stripped on ingress | Yes, VLAN tag preserved |
| Security risk | Low if assigned correctly | High if misconfigured, can allow VLAN hopping |
| Cisco IOS config | `switchport mode access` | `switchport mode trunk` |
:::

:::list heading="Trunk Port Hardening Checklist" style=plain
- Explicitly set trunk mode, never rely on DTP auto-negotiation (`switchport nonegotiate`)
- Prune unused VLANs from all trunk links (`switchport trunk allowed vlan`, whitelist only)
- Never use VLAN 1 as a native VLAN, reassign native VLAN to an unused ID (e.g., VLAN 999)
- Apply 802.1Q-aware BPDU Guard on access ports to prevent rogue switch injection
:::

:::image src="images/15_trunk_vs_access_ports.png" alt="Switch diagram showing three port types side by side: an access port on the left connecting a single workstation with a plain Ethernet frame labeled 'VLAN 10 only, untagged'; a trunk port in the center connecting two switches with multiple 802.1Q-tagged frames labeled VLAN 10, VLAN 20, VLAN 30 stacked on the link; and a misconfigured auto-trunk port on the right showing a DTP negotiation arrow and a red warning badge labeled 'VLAN hopping risk'" caption="Access vs. trunk ports, access ports serve single devices on one VLAN; trunk ports carry multiple tagged VLANs between infrastructure devices; DTP auto-negotiation on access ports creates an exploitable attack surface" width=full:::
:::
:::notes
Understanding the distinction between access ports and trunk ports is essential for anyone responsible for configuring or auditing a switched network. The correct assignment of port modes is the first line of defense against a class of attacks called VLAN hopping, where an attacker on one VLAN manipulates switch behavior to gain unauthorized access to a different VLAN without passing through an authorized Layer 3 routing device.

An **access port** is configured to belong to exactly one VLAN. When a device sends an untagged Ethernet frame into an access port, the switch internally assigns that frame to the configured VLAN and forwards it only within that broadcast domain. When the frame exits through another access port, the VLAN tag is stripped again, so the end device never sees it. This is the correct mode for all end-user devices: workstations, IP phones, printers, and IoT sensors.

A **trunk port** is configured to carry traffic for multiple VLANs simultaneously, using IEEE 802.1Q tags to distinguish which VLAN each frame belongs to. Trunk ports are used on links between switches (uplinks), between a switch and a router performing inter-VLAN routing, and between a switch and a wireless access point that must service multiple SSIDs mapped to different VLANs.

The critical security concern arises from **Dynamic Trunking Protocol (DTP)**, a Cisco proprietary protocol that allows switches to automatically negotiate trunk links. When DTP is left enabled on access ports, a default in many older Cisco IOS versions, an attacker can send crafted DTP frames to cause the switch to promote the port to trunk mode. This immediately grants the attacker access to all VLANs carried on that trunk. This attack vector is documented under **MITRE ATT&CK T1557 (Adversary-in-the-Middle)** and was historically leveraged in internal network penetration tests and red-team engagements.

The fix is explicit: set all access ports to `switchport mode access` and issue `switchport nonegotiate` to disable DTP. On trunk ports, explicitly whitelist only the VLANs that must traverse that link using `switchport trunk allowed vlan <id-list>`. Additionally, reassign the native VLAN, the VLAN on which untagged trunk traffic is placed, from the default VLAN 1 to an unused VLAN ID. VLAN 1 is the default native VLAN on Cisco switches, and double-tagging attacks (a second form of VLAN hopping, documented as CVE-2005-4440 class attacks) exploit this by sending frames tagged with VLAN 1 as the outer tag, which the first switch strips, leaving the inner tag to route the frame into the attacker's target VLAN at the next switch.

These hardening practices align with **CIS Benchmark for Cisco IOS** and **NIST SP 800-53 SC-7 (Boundary Protection)**, both of which specify that network devices must be configured to prevent unauthorized traversal of network boundaries. ISO/IEC 27033-4 also specifically addresses securing virtual networks including VLAN infrastructure.
:::

%%%

---
unit: VLANs
code: VLN
title: VLAN Hopping Attacks
---
:::callout style=soft
**VLAN hopping** is an attack technique where a malicious actor on one VLAN sends crafted traffic to gain unauthorized access to a different VLAN, bypassing the logical separation that VLANs are meant to enforce. Two primary methods exist: switch spoofing and double tagging.
:::

::::columns
::col::
:::list heading="Method 1: Switch Spoofing" style=plain
- Attacker sends DTP frames from their device
- Switch auto-negotiates and promotes port to trunk mode
- Attacker's device now receives all VLAN traffic on that trunk
- Exploit: DTP left enabled on access ports (`switchport mode dynamic auto`)
- Fix: `switchport mode access` + `switchport nonegotiate` on all access ports
:::
::col::
:::list heading="Method 2: Double Tagging" style=plain
- Attacker sends frame with two 802.1Q tags: outer = native VLAN, inner = target VLAN
- First switch strips outer (native VLAN) tag and forwards tagged frame into trunk
- Second switch reads inner tag and delivers frame to target VLAN
- Exploit: Native VLAN is VLAN 1 (default), attacker and switch share native VLAN
- Fix: Reassign native VLAN to an unused ID (e.g., VLAN 999) on all trunks
:::
::::

:::image src="images/15_vlan_hopping_double_tag.png" alt="Step-by-step double-tagging VLAN hopping diagram: Step 1 shows an attacker workstation sending an Ethernet frame with two nested 802.1Q tags (outer tag VLAN 1 in red, inner tag VLAN 20 in orange) into an access port; Step 2 shows Switch A stripping the outer VLAN 1 native tag and forwarding the frame with the VLAN 20 inner tag intact onto the trunk link; Step 3 shows Switch B reading the inner VLAN 20 tag and delivering the frame to a Finance server in VLAN 20, a red dotted line traces the full attack path from attacker to Finance segment" caption="Double-tagging VLAN hopping, by nesting a second 802.1Q tag inside a native-VLAN outer tag, an attacker bypasses VLAN isolation at the first switch and delivers frames directly into a target VLAN at the second switch" width=full:::
:::
:::notes
VLAN hopping is one of the more elegant Layer 2 attack techniques because it exploits not a software vulnerability but a design assumption: that switches will behave helpfully and automatically. Both primary VLAN hopping methods take advantage of default switch behaviors that prioritize ease of configuration over security.

**Switch spoofing** exploits DTP, Cisco's Dynamic Trunking Protocol. By default, many Cisco IOS switch ports are set to `dynamic auto` or `dynamic desirable` mode, meaning they will negotiate to become trunk ports if the connected device requests it. An attacker who understands this can send DTP frames from their laptop, using tools such as Yersinia, a network attack framework, to cause the switch to promote their access port to a trunk. Once trunking, the attacker's machine receives traffic from all VLANs traversing that trunk. This effectively defeats the isolation that VLANs are meant to provide. The fix is straightforward: explicitly configure every access port as `switchport mode access` and issue `switchport nonegotiate` to prevent DTP entirely. This is a required hardening step in the **CIS Cisco IOS Benchmark** and is consistent with **NIST SP 800-53 CM-7 (Least Functionality)**, which requires disabling unnecessary protocols and features.

**Double tagging** is more subtle and is notable because it works even when DTP is disabled. The attack requires that the attacker's access port share the same native VLAN as the trunk link's native VLAN, typically VLAN 1. The attacker crafts a frame with two 802.1Q headers: the outer header carries the native VLAN ID (e.g., VLAN 1) and the inner header carries the target VLAN ID (e.g., VLAN 20, Finance). When this frame arrives at the first switch, it performs its normal operation: it strips the outer VLAN 1 tag (because that is the native VLAN, and native VLAN traffic is transmitted untagged on trunks) and forwards the now single-tagged frame (inner tag: VLAN 20) onto the trunk. The second switch receives the frame and interprets the single VLAN 20 tag as a legitimate VLAN 20 frame, delivering it to a Finance segment host. Critically, this attack is **one-directional**, the response frame will route back to the Finance segment, not back to the attacker, making it useful for denial-of-service rather than full bidirectional exploitation. However, it remains a valid technique for injecting traffic into a supposedly isolated segment.

The remediation for double tagging is also straightforward: change the native VLAN on all trunk links from VLAN 1 to an unused VLAN ID that no end devices belong to (commonly VLAN 999 or VLAN 4094). This ensures that the attacker cannot share native VLAN with the trunk, breaking the outer-tag-stripping step of the attack. Additionally, explicitly tag native VLAN traffic using the command `vlan dot1q tag native` on Cisco platforms.

VLAN hopping through switch-port trunk negotiation (DTP) lets an attacker promote an access port to a trunk and reach other VLANs. Disabling dynamic trunk negotiation on access ports (switchport nonegotiate) prevents the promotion and closes the attack.

These attack techniques are referenced in **MITRE ATT&CK T1200 (Hardware Additions)** and more broadly relate to network-layer exploitation. From a compliance standpoint, **PCI DSS Requirement 1.3.2** mandates that all network access paths be explicitly authorized, implicitly requiring the hardening steps that prevent VLAN hopping.
:::

%%%

---
unit: VLANs
code: VLN
title: Inter-VLAN Routing
---
:::callout style=soft
VLANs create logical isolation, but users still need to reach services on other segments. **Inter-VLAN routing** is the controlled process of forwarding traffic between VLANs through a Layer 3 device, a router or Layer 3 switch, that applies access control policies before allowing any cross-segment traffic.
:::

:::flow
Host in VLAN 10 (Office) sends packet to IP address in VLAN 20 (Servers)
Host forwards packet to its default gateway, the Layer 3 router/switch interface
Router receives packet and evaluates ACL policy for VLAN 10 → VLAN 20 traffic
If policy permits: packet is routed and forwarded into VLAN 20
If policy denies: packet dropped, log entry written to SIEM
:::

:::table
| Method | How it works | Use case |
|---|---|---|
| Router-on-a-Stick | Single router port with 802.1Q subinterfaces for each VLAN | Small networks, limited port count |
| Layer 3 Switch (SVI) | Switch Virtual Interfaces route between VLANs internally | Medium-large networks, high throughput |
| Dedicated Firewall | Full stateful inspection at each VLAN boundary | High-security environments, PCI/HIPAA |
:::

:::image src="images/15_intervlan_routing_methods.png" alt="Three-panel comparison diagram of inter-VLAN routing methods: left panel shows a router-on-a-stick topology with one physical router port split into 802.1Q subinterfaces (g0/0.10 for VLAN 10, g0/0.20 for VLAN 20) connected to a switch trunk port; center panel shows a Layer 3 switch with Switch Virtual Interfaces (SVI) labeled VLAN 10 SVI and VLAN 20 SVI routing internally within the switch hardware; right panel shows two VLANs connected to a stateful firewall with inspection labels and ACL rule symbols at each interface, each panel has a pros-cons annotation" caption="Three inter-VLAN routing methods, router-on-a-stick for simplicity, Layer 3 SVI for throughput, dedicated firewall for maximum policy enforcement" width=full:::
:::
:::notes
Inter-VLAN routing is the essential complement to VLAN segmentation. Without it, VLANs would make networks unusable, Finance staff could never reach the file server, workstations could never access the internet, and IT could never manage remote systems. The security design challenge is therefore not whether to permit inter-VLAN traffic, but how to permit exactly what is necessary and nothing more.

The **router-on-a-stick** method uses a single physical router interface connected to a switch trunk port. The router interface is subdivided into logical subinterfaces, one per VLAN, each configured with an IP address that serves as the default gateway for devices in that VLAN. When a host in VLAN 10 needs to reach a host in VLAN 20, the packet is sent to the VLAN 10 subinterface, the router evaluates its routing table and ACLs, and if permitted, the packet is forwarded out the VLAN 20 subinterface and back down the trunk to the destination. This method is simple to configure but introduces a potential bottleneck because all inter-VLAN traffic passes through a single physical link. It is appropriate for small environments with modest traffic volumes.

**Layer 3 switching with Switch Virtual Interfaces (SVIs)** performs routing internally within the switch's hardware application-specific integrated circuits (ASICs), enabling wire-speed inter-VLAN routing without an external router. Each VLAN is assigned a virtual interface with an IP address serving as its default gateway. This method offers dramatically higher throughput than router-on-a-stick and is standard in medium-to-large enterprise deployments. However, Layer 3 switches typically offer less sophisticated policy enforcement than dedicated firewalls, ACLs are stateless and lack application-layer inspection.

The **dedicated firewall** approach routes all inter-VLAN traffic through a Next-Generation Firewall (NGFW) capable of stateful packet inspection, application identification, intrusion prevention, and deep packet inspection. This provides the richest policy enforcement capability but at higher cost and potential throughput limitations. For environments subject to PCI DSS, HIPAA, or other stringent compliance regimes, a dedicated firewall between VLANs is often required, **PCI DSS Requirement 1.2 (Build Firewall and Router Configurations That Restrict Connections Between Untrusted Networks and Any System Components in the Cardholder Data Environment)** effectively mandates this architecture.

From a **NIST SP 800-53** perspective, inter-VLAN routing points map directly to **SC-7 (Boundary Protection)**, which requires the implementation of boundary protection at the external boundary of information systems and at key internal boundaries within the system. Every VLAN boundary is precisely such an internal boundary.

A Layer 3 switch that routes between an Office VLAN and a Server VLAN with an "ip any any" ACL has not achieved segmentation: the VLANs exist structurally but the policy allows full traversal. This is the difference between structural segmentation and policy-enforced segmentation, a distinction that recurs in audits and in the CISSP.
:::

%%%

---
unit: Foundations
code: SEG
title: Physical vs. Logical Segmentation, Comparison
---
:::callout style=soft
Network segmentation can be achieved either **physically**, using separate hardware infrastructure for each zone, or **logically**, using software-defined boundaries like VLANs and software-defined networking (SDN) on shared hardware. Both approaches have distinct trade-offs in security strength, cost, and operational flexibility.
:::

:::table
| Dimension | Physical Segmentation | Logical Segmentation (VLANs/SDN) |
|---|---|---|
| Hardware | Separate switches, cables, NICs per zone | Shared switching infrastructure |
| Security strength | Highest, no shared hardware attack surface | High, dependent on correct configuration |
| Cost | High, significant hardware investment | Low, software configuration on existing hardware |
| Flexibility | Low, physical changes required for moves | High, policy changes via CLI or GUI |
| Risk | Hardware failure in one zone doesn't affect others | Misconfiguration can collapse boundaries |
| Typical use | Air-gapped OT/ICS, classified networks | Enterprise IT environments |
| Compliance reference | NIST SP 800-82 (ICS), CNSSP 17 (classified) | NIST SP 800-53 SC-7, PCI DSS Req. 1 |
:::

:::image src="images/15_physical_vs_logical_segmentation.png" alt="Side-by-side comparison diagram: left side labeled 'Physical Segmentation' shows two completely separate network stacks, Switch A with dedicated cables to Finance PCs and Switch B with dedicated cables to HR PCs, with no shared hardware between them and a physical air gap symbol in the center; right side labeled 'Logical Segmentation' shows a single shared switch with VLAN 10 and VLAN 20 port assignments color-coded, and a software boundary symbol between the two VLAN groups, cost and flexibility ratings annotated below each panel" caption="Physical vs. logical segmentation, physical separation provides the strongest isolation guarantee at highest cost; logical segmentation via VLANs delivers strong isolation at low cost with the trade-off of configuration-dependent security" width=full:::
:::
:::notes
The choice between physical and logical segmentation is fundamentally a risk-cost trade-off that should be driven by the sensitivity of the assets being protected, applicable compliance requirements, and operational constraints. Understanding this distinction is critical for security architects and appears regularly in security certification examinations and real-world design reviews.

**Physical segmentation** means that different network zones are implemented on entirely separate hardware, separate switches, separate cables, separate network interface cards in servers, and no shared infrastructure. The most extreme form of physical segmentation is an **air gap**: a complete physical separation where no data path exists between two systems, not even through a shared switch or router. Air gaps are mandated by regulations such as **CNSSP 17 (Committee on National Security Systems Policy)** for classified government networks and are recommended by **NIST SP 800-82** for critical operational technology (OT) systems such as industrial control systems (ICS) and SCADA. The security guarantee of physical segmentation is absolute in one respect: even a fully compromised switching software stack cannot create a traffic path between physically separate networks. However, this absolute guarantee comes at high hardware cost, significant cable plant complexity, and very low operational flexibility, adding a device to a new zone requires physical hardware changes.

**Logical segmentation** using VLANs, SDN, or other software-defined boundaries implements isolation on shared physical infrastructure. The security depends entirely on the correctness of the configuration and the absence of exploitable vulnerabilities in the switching software. As discussed in earlier slides, VLAN hopping attacks demonstrate that misconfigured logical boundaries can be defeated. However, when properly configured and hardened, logical segmentation provides strong isolation at a fraction of the hardware cost of physical segmentation and with much greater operational flexibility. Network administrators can reassign a device to a different VLAN with a single configuration command rather than physically re-cabling.

A key principle from **NIST SP 800-53 SC-7 (Boundary Protection)** is that the choice of implementation mechanism should be proportional to the risk level of the assets being protected. Critical infrastructure, air-gapped classified systems, and high-value OT networks warrant physical separation. Enterprise IT environments handling sensitive but not classified data typically implement logical segmentation with compensating controls, hardened switch configurations, NAC, and continuous monitoring, that together provide a security posture equivalent to the intent of physical segmentation.

The separation of IT and OT networks in manufacturing shows that segmentation choices are business-risk decisions, not only technical ones. After Stuxnet, many industrial organizations were advised to air-gap control systems; some chose cheaper logical VLAN separation instead, and several were later compromised through insufficiently hardened VLAN boundaries.
:::

%%%

---
unit: Foundations
code: SEG
title: Subnetting as a Segmentation Layer
---
:::callout style=soft
**Subnetting**, dividing a larger IP address block into smaller, routed subnetworks, is a Layer 3 complement to VLAN-based Layer 2 segmentation. Together, VLANs and subnets create segmentation that operates at both the data link and network layers, enabling granular routing policies and access control.
:::

:::list heading="How Subnetting Supports Segmentation" style=plain
- Each VLAN is assigned its own IP subnet (e.g., VLAN 10 = 192.168.10.0/24, VLAN 20 = 192.168.20.0/24)
- Routing between subnets is required to cross VLAN boundaries, creating a mandatory policy enforcement point
- ACLs and firewall rules are written in terms of IP addresses and subnets, subnetting enables precise policy scoping
- CIDR notation allows right-sizing subnets to the number of devices in each zone, reducing wasted IP space
:::

:::table
| Zone | VLAN ID | Subnet | Usable Hosts | Default Gateway |
|---|---|---|---|---|
| Office | 10 | 192.168.10.0/24 | 254 | 192.168.10.1 |
| Servers | 20 | 192.168.20.0/24 | 254 | 192.168.20.1 |
| Guest Wi-Fi | 30 | 192.168.30.0/24 | 254 | 192.168.30.1 |
| DMZ | 50 | 10.0.50.0/28 | 14 | 10.0.50.1 |
| Management | 99 | 10.0.99.0/29 | 6 | 10.0.99.1 |
:::

:::image src="images/15_subnetting_segmentation.png" alt="Network diagram overlaying VLAN labels and subnet CIDR blocks: five colored zones each labeled with their VLAN ID and subnet address, Office VLAN 10 in blue (192.168.10.0/24), Servers VLAN 20 in green (192.168.20.0/24), Guest VLAN 30 in orange (192.168.30.0/24), DMZ VLAN 50 in purple (10.0.50.0/28), Management VLAN 99 in grey (10.0.99.0/29), routing arrows between zones pass through a central Layer 3 switch with ACL filter symbols on each inter-zone path" caption="VLAN-to-subnet mapping, each VLAN is assigned its own IP subnet, so inter-VLAN routing always crosses a Layer 3 boundary where ACL and firewall policies are applied" width=full:::
:::
:::notes
Subnetting and VLANs are complementary tools that together create a two-layer segmentation architecture. While VLANs operate at Layer 2 (data link layer) to isolate broadcast domains, subnets operate at Layer 3 (network layer) to define routing boundaries. Assigning each VLAN its own subnet means that any communication between VLANs is automatically inter-subnet communication, requiring routing, and therefore traversing the Layer 3 policy enforcement point where ACLs and firewall rules operate.

The relationship is: every VLAN maps to exactly one subnet, and every device in that VLAN is assigned an IP address within that subnet. The default gateway for devices in the VLAN is the IP address of the Layer 3 routing interface for that VLAN, either a router subinterface (in router-on-a-stick topology) or a Switch Virtual Interface (SVI) on a Layer 3 switch. When a device needs to communicate with an IP address outside its own subnet, it sends the packet to its default gateway, which is the first hop where policy can be applied.

From a security policy writing perspective, subnetting is what makes ACL rules tractable. An ACL rule such as `permit tcp 192.168.10.0/24 192.168.20.0/24 eq 443` expresses a clear, auditable policy: hosts in the Office subnet may reach hosts in the Server subnet on TCP port 443 (HTTPS). Without subnetting, in a flat network where all devices share the same IP range, writing such rules would require listing individual IP addresses, which is both unscalable and error-prone.

**CIDR (Classless Inter-Domain Routing)** notation allows network architects to right-size each subnet for its zone's expected device count. The DMZ in the table above is assigned a /28, providing only 14 usable host addresses, appropriate for a small number of public-facing servers. The Management VLAN receives a /29 with only 6 usable addresses, limiting it to precisely the number of administrative devices that require access. This right-sizing is an application of the principle of least privilege at the IP address allocation level: if a zone can only hold 14 IP addresses, it structurally cannot support a large lateral movement campaign even if its VLAN boundary is breached.

**NIST SP 800-53 SC-7 (Boundary Protection)** and **SC-5 (Denial of Service Protection)** both reference subnetting as part of network architecture controls. **ISO/IEC 27033-3 (Network Security Architecture)** provides detailed guidance on combining VLANs and subnets to create defense-in-depth network architectures. **RFC 1918** defines the private address ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) that are standard for internal network segmentation, ensuring internal segments use non-routable addresses that cannot be directly targeted from the internet.

Designing a subnet allocation for zones such as Office, Servers, Guest, DMZ and Management ties subnetting arithmetic to security rationale: tight subnet sizing limits the hosts reachable within a zone and the scope of a broadcast domain.
:::

%%%

---
unit: Strategy
code: ZTA
title: Zero Trust Network Architecture
---
:::callout style=soft
**Zero Trust** is a security model that eliminates the concept of implicit trust based on network location. Under Zero Trust, no device, user, or connection is trusted by default, every access request is authenticated, authorized, and continuously validated regardless of whether it originates inside or outside the traditional network perimeter.
:::

:::list heading="Zero Trust Core Principles (NIST SP 800-207)" style=plain
- **Verify explicitly**: Authenticate and authorize every access request using all available data points (identity, device health, location, behavior)
- **Use least privilege access**: Limit user access with just-in-time and just-enough-access policies
- **Assume breach**: Minimize blast radius; segment access, encrypt all sessions, use analytics to detect anomalies
:::

:::table
| Traditional Perimeter Model | Zero Trust Model |
|---|---|
| Trust based on network location | Trust based on verified identity + device state |
| "Inside = trusted" assumption | No implicit trust for any location |
| Wide internal access after VPN login | Granular, policy-based per-session access |
| Flat internal network common | Microsegmentation required |
| Reactive detection | Continuous monitoring and re-verification |
:::

:::image src="images/15_zero_trust_architecture.png" alt="Zero Trust architecture diagram showing the policy enforcement components: a central Policy Engine and Policy Administrator box connected to a Policy Enforcement Point (PEP) that sits inline between a subject (user and device icons) on the left and enterprise resources (application, data, and infrastructure icons) on the right, identity provider, device health signals, threat intelligence feeds, and activity logs are shown as inputs feeding into the Policy Engine, all data plane traffic flows through the PEP, with a continuous verification loop arrow circling back from the resource to the Policy Engine" caption="NIST SP 800-207 Zero Trust Architecture, every access request passes through a Policy Enforcement Point that consults the Policy Engine, which continuously evaluates identity, device posture, and behavioral signals before granting session-scoped access" width=full:::
:::
:::notes
Zero Trust Architecture (ZTA) represents the most significant evolution in network security thinking over the past decade. It was formalized by NIST in **Special Publication 800-207 (Zero Trust Architecture)**, published in August 2020, which established a comprehensive framework and vocabulary for implementing Zero Trust in enterprise environments. The US federal government subsequently mandated Zero Trust adoption across all federal agencies through **Executive Order 14028 (Improving the Nation's Cybersecurity, May 2021)** and the **OMB Memorandum M-22-09 (Moving the U.S. Government Toward Zero Trust Cybersecurity Principles, January 2022)**, which set specific Zero Trust maturity targets for federal agencies.

The philosophical core of Zero Trust is a rejection of the traditional "castle-and-moat" network model, where everything inside the perimeter was implicitly trusted. This model collapsed under the reality of modern threats: remote work connecting from untrusted networks, cloud services outside the perimeter, mobile devices that move between networks, and attackers who routinely achieve initial access inside the perimeter through phishing, credential theft, or supply-chain compromises. If the moat is breached, the castle has no interior defenses.

**NIST SP 800-207** defines three core logical components of ZTA: the **Policy Engine (PE)**, which makes access grant/deny decisions using policy and input data; the **Policy Administrator (PA)**, which executes the decisions of the PE by establishing or terminating communication paths; and the **Policy Enforcement Point (PEP)**, which is the inline gateway that enforces access decisions on the data plane. All enterprise resources, applications, data, services, devices, are protected behind a PEP, meaning every access attempt traverses a policy decision regardless of where the request originates.

From a network segmentation perspective, Zero Trust mandates and extends traditional VLAN-based segmentation through **microsegmentation**, the enforcement of granular, identity-aware policies at the individual workload or application level rather than just at the VLAN boundary. Where VLAN segmentation might permit all traffic from VLAN 10 (Office) to VLAN 20 (Servers) on TCP 443, a Zero Trust microsegmentation policy might permit only authenticated user Alice's laptop, running a compliant OS with current patches, to reach specifically the HR application server on port 443 between 8 AM and 6 PM on weekdays, and nothing else.

Commercially, ZTA is implemented through products such as **Palo Alto Networks Prisma Access**, **Zscaler Zero Trust Exchange**, **Google BeyondCorp Enterprise**, and **Cisco Duo + Umbrella**. Cloud-native implementations use service meshes (Istio, Linkerd) to enforce mTLS-authenticated, policy-controlled east-west traffic between microservices, an extension of Zero Trust principles to the application layer.

**ISO/IEC 27001:2022** does not explicitly mandate Zero Trust by name, but Annex A controls including A.8.2 (Privileged Access Rights), A.8.3 (Information Access Restriction), A.8.22 (Segregation in Networks), and A.8.16 (Monitoring Activities) collectively align with ZTA principles. Organizations implementing ISO 27001 certification alongside NIST SP 800-207 ZTA achieve strong alignment between their compliance posture and their technical security architecture.
:::

%%%

---
unit: Strategy
code: MIC
title: Microsegmentation
---
:::callout style=soft
**Microsegmentation** extends traditional VLAN-based segmentation to the individual workload level. Instead of enforcing policies only at VLAN boundaries (zone-to-zone), microsegmentation enforces policies between individual VMs, containers, or applications, even within the same VLAN. It is a core pillar of Zero Trust and cloud security architecture.
:::

:::list heading="Microsegmentation vs. Traditional VLAN Segmentation" style=plain
- **Traditional VLANs**: Policy enforced at zone boundary (North-South traffic between VLANs)
- **Microsegmentation**: Policy enforced between individual workloads (East-West traffic within and between VLANs)
- **Granularity**: VLANs group hundreds of devices; microsegmentation targets individual processes
- **Implementation**: VLANs use switch ACLs; microsegmentation uses hypervisor-level or SDN-based enforcement
- **Visibility**: Microsegmentation provides application-level flow mapping and policy recommendations
:::

:::flow
Discover all workloads and map their communication flows (automated baselining)
Classify workloads by sensitivity and business function
Define least-privilege policy for each workload-to-workload communication path
Deploy policy via hypervisor, SDN controller, or eBPF-based enforcement agents
Monitor for policy violations and iteratively refine, reject unclassified flows by default
:::

:::image src="images/15_microsegmentation_workloads.png" alt="Data center rack diagram showing virtual machines on two hypervisor hosts: on the left, a flat VLAN model where VM-1 through VM-6 all share VLAN 20 with unrestricted east-west arrows between every pair; on the right, a microsegmented model where each VM pair has a labeled policy tag (permit HTTPS only, deny all, permit DB port 5432) drawn inline between the VMs, a legend shows green arrows as permitted flows and red X arrows as denied flows, illustrating that microsegmentation controls traffic within the same VLAN, not just between VLANs" caption="Microsegmentation enforces workload-level policies within and between VLANs, controlling east-west traffic between individual VMs where traditional VLAN ACLs see only zone-level boundaries" width=full:::
:::
:::notes
Microsegmentation represents the logical evolution of VLAN-based segmentation into the modern data center and cloud era. While VLANs effectively segment networks at the zone level, separating departments, guest users, and server groups, they cannot control traffic between individual workloads that share the same VLAN. In a traditional model, two VMs in VLAN 20 (Servers) can communicate freely with each other on any protocol and port. If one of those VMs is compromised, the attacker can pivot to all other VMs in VLAN 20 without ever crossing a VLAN boundary or triggering an ACL. Microsegmentation closes this gap by enforcing policy at the workload-to-workload level.

The term "east-west traffic" refers to traffic that flows laterally between servers and services within a data center, as opposed to "north-south traffic," which flows between external clients and internal servers. As data centers have shifted from physical servers to virtual machines and containers, east-west traffic has grown to represent the majority of internal network traffic. Attackers who achieve initial access to a workload in a modern cloud environment rely heavily on east-west movement to escalate privileges and reach high-value targets. **MITRE ATT&CK T1021 (Remote Services)** and **T1570 (Lateral Tool Transfer)** are the primary techniques used for east-west lateral movement.

Microsegmentation is implemented through several technical mechanisms. In **VMware NSX** environments, the Distributed Firewall (DFW) runs in the hypervisor kernel and enforces policy on every virtual NIC of every VM, effectively placing a stateful firewall at the network edge of each workload without requiring traffic to traverse a physical appliance. In **Kubernetes** environments, **Network Policies** (enforced by CNI plugins such as Cilium, Calico, or Weave) define permitted pod-to-pod communication at the container level, with Cilium additionally using **eBPF** (extended Berkeley Packet Filter) to enforce policy with kernel-level performance. In public cloud environments, **AWS Security Groups**, **Azure Network Security Groups**, and **GCP VPC Firewall Rules** function as workload-level microsegmentation controls.

A key challenge in microsegmentation deployment is the initial discovery and mapping phase. Before policies can be written, security teams must understand which workloads legitimately communicate with which other workloads, a challenge in complex environments with hundreds of microservices. Tools such as **Illumio**, **Guardicore (now Akamai Guardicore Segmentation)**, and **vArmour** provide automated flow discovery and policy recommendation engines that baseline normal communication patterns and propose microsegmentation policies based on observed behavior, significantly reducing the policy authoring burden.

**NIST SP 800-207 Section 2.2** specifically identifies microsegmentation as one of three primary approaches to implementing Zero Trust Architecture (alongside software-defined perimeters and identity-aware proxies). **ISO/IEC 27001:2022 Annex A.8.22** aligns with microsegmentation by requiring segregation based on information classification, which microsegmentation enables at the workload level.

In a microservices environment the number of workload-to-workload (east-west) communication paths far exceeds what anyone could audit with traditional VLAN ACLs, which is why automated, identity-aware east-west policy enforcement is necessary. Service-mesh traffic dashboards make the scale of these flows visible.
:::

%%%

---
unit: CaseStudy
code: CS1
title: Case Study, Target Data Breach 2013
---
:::callout style=soft
The **2013 Target Corporation breach** is one of the most cited examples of network segmentation failure in cybersecurity history. Attackers exfiltrated payment card data for 40 million customers by exploiting an insufficiently isolated third-party vendor connection, a path that proper segmentation would have closed entirely.
:::

:::steps
1. **Initial access**: Attackers compromise Fazio Mechanical Services (an HVAC vendor) via phishing. Fazio had credentials to Target's vendor portal for electronic billing and HVAC monitoring.
2. **Pivot to internal network**: Target's vendor access was connected to the same internal network as POS systems, no VLAN or firewall boundary separated them.
3. **Malware installation**: BlackPOS (also known as Kaptoxa) is deployed to Target's point-of-sale terminals. It captures magnetic stripe data from RAM during the payment transaction window.
4. **Data staging and exfiltration**: Stolen card data is aggregated on an internal Target server then exfiltrated to an external FTP server in a sequence of outbound connections.
5. **Discovery**: First flagged by Target's own security tools (FireEye), alerts were generated and dismissed. Breach confirmed by external notification from the US Department of Justice in December 2013.
:::

:::image src="images/15_target_breach_timeline.png" alt="Attack timeline and network path diagram for the 2013 Target breach: five labeled stages along a horizontal arrow, Stage 1 shows a phishing email to Fazio Mechanical with credential theft icons; Stage 2 shows a dotted lateral movement arrow crossing from a vendor management zone to a POS network zone with no firewall symbol in between (gap highlighted in red); Stage 3 shows BlackPOS malware icon on a POS terminal with RAM scraping animation; Stage 4 shows a staging server with card data being bundled; Stage 5 shows an exfiltration arrow to an external FTP server, losses annotated: 40M card records, $200M+ total impact" caption="Target 2013 breach kill chain, the absence of a firewall or VLAN boundary between vendor access and POS systems allowed the attacker to traverse from an HVAC vendor portal to payment card terminals in a single lateral movement step" width=full:::
:::
:::notes
The Target breach of 2013 stands as a textbook case study in the consequences of insufficient network segmentation. Understanding the attack path in detail reveals how multiple, individually reasonable architectural decisions combined to create a catastrophic gap, and how a single additional segmentation control would have contained the breach to the vendor access zone.

The attack began in November 2013 when attackers, later attributed to a Ukrainian cybercriminal group, sent a phishing email to Fazio Mechanical Services, a Pennsylvania-based refrigeration and HVAC contractor that serviced Target stores. Fazio employees accessed Target's vendor portal using stolen credentials. Target's vendor portal was intended for electronic billing and contract management, routine, low-risk business functions. However, Target had connected the vendor access network to the same internal network used by its point-of-sale systems. This was the fundamental segmentation failure: **no VLAN boundary, firewall, or access control list separated the vendor access zone from the POS network**.

Once inside the vendor access network, attackers used it as a pivot point to reach Target's POS terminals. They deployed **BlackPOS** (also called Kaptoxa), a RAM-scraping malware that captures unencrypted payment card data from the process memory of POS software during the split-second window between card swipe and encryption. This technique, targeting **MITRE ATT&CK T1005 (Data from Local System)** and **T1057 (Process Discovery)**, exploited the fact that all payment card data must briefly exist in plaintext in RAM before encryption can be applied.

Over approximately three weeks from late November to mid-December 2013, BlackPOS exfiltrated data for approximately 40 million debit and credit card accounts and, in a separate database breach, personal information for approximately 70 million customers. The stolen card data was staged on an internal Target FTP server and then exfiltrated in batches to external servers in Eastern Europe using standard FTP.

Target's security tools, including a **FireEye** threat detection platform that had recently been deployed, generated alerts during the attack. Detailed post-incident analysis revealed that the alerts were reviewed and dismissed by the security operations team, a failure of security operations procedures that compounded the architectural failure. The breach was ultimately confirmed not by Target's own detection but by notification from the US Department of Justice in December 2013.

The remediation implication is straightforward and directly relevant to network segmentation: a firewall or VLAN ACL between the vendor access network and the POS network, configured to deny all traffic that was not explicitly required for HVAC monitoring, would have prevented the lateral movement entirely. The attacker would have been confined to the vendor portal zone with no path to POS terminals. **PCI DSS Requirement 1.3 (Restrict Inbound and Outbound Traffic to That Which Is Necessary for the Cardholder Data Environment)** directly mandates this control, Target's POS systems were in scope for PCI DSS, and the absence of this boundary represented a PCI DSS compliance failure. Target ultimately paid $18.5 million in a multistate settlement and incurred total breach costs estimated at over $200 million.

The 2013 Target breach, framed as a $200 million misconfiguration, shows the business value of segmentation. A single rule, denying all traffic from the vendor access VLAN to the POS VLAN except the HVAC monitoring protocol, would have prevented it. Segmentation was not complex or expensive in principle; the organizational process to implement it failed.
:::

%%%

---
unit: CaseStudy
code: CS2
title: Case Study, WannaCry Ransomware 2017
---
:::callout style=soft
The **WannaCry ransomware campaign (May 2017)** exploited an unpatched SMBv1 vulnerability (CVE-2017-0144, "EternalBlue") to propagate autonomously across flat, unsegmented networks. Organizations with effective VLAN segmentation contained the outbreak; those without it saw it spread to every reachable system within hours.
:::

::::columns
::col::
:::list heading="Attack Characteristics" style=plain
- **Exploit**: CVE-2017-0144 (EternalBlue), SMBv1 remote code execution
- **Vector**: Self-propagating worm, no user interaction required after initial seed
- **Spread method**: TCP port 445 scans across all reachable IP addresses
- **Payload**: File encryption + ransom demand in Bitcoin
- **Kill switch**: Domain `iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com`, registered by Marcus Hutchins
- **Attribution**: Lazarus Group (North Korea), per NSA/GCHQ/NCA assessment
:::
::col::
:::list heading="Impact by Sector" style=plain
- **NHS (UK)**: 80 of 236 NHS trusts affected, 19,000 appointments cancelled
- **Telefónica (Spain)**: Internal network largely disrupted
- **Deutsche Bahn**: Station display systems infected
- **Maersk**: Partial impact, contained in some regions
- **FedEx/TNT**: Estimated $400M loss
- **Total global damage**: Estimated $4–8 billion
:::
::::

:::image src="images/15_wannacry_propagation.png" alt="Two-panel propagation diagram: left panel shows WannaCry spreading on a flat network, a single infected endpoint at the top with red infection arrows radiating outward to all 24 other endpoints in the same IP range, representing 100% infection rate; right panel shows the same attack on a segmented network with three VLANs, infection is confined to the initial VLAN (8 of 8 endpoints in VLAN 10 infected) while firewall boundary blocks port 445 SMB traffic from reaching VLAN 20 and VLAN 30, showing 0% infection in adjacent VLANs, percentage labels annotate each panel" caption="WannaCry propagation on flat vs. segmented networks, TCP port 445 SMB scanning is blocked at VLAN boundaries where inter-VLAN firewall rules deny port 445, confining the worm to its initial segment" width=full:::
:::
:::notes
WannaCry is arguably the most impactful ransomware event in cybersecurity history in terms of breadth of disruption and clarity of the technical lesson it delivered. It is almost perfectly designed as a case study for network segmentation, because the variable that most directly predicted whether an organization contained or succumbed to the outbreak was the presence or absence of effective network segmentation, specifically, whether internal firewalls and VLAN ACLs blocked TCP port 445 (SMB) between network segments.

The technical foundation of WannaCry is the **EternalBlue exploit** (CVE-2017-0144), which was leaked from the NSA's toolkit by the Shadow Brokers hacker group in April 2017. EternalBlue exploits a buffer overflow vulnerability in the Windows SMBv1 protocol, enabling remote code execution without any user interaction, a so-called "wormable" vulnerability. Microsoft had issued **MS17-010** as a patch for this vulnerability in March 2017, six weeks before WannaCry launched. Organizations that had applied the patch or disabled SMBv1 were immune; those that had not were vulnerable.

WannaCry's propagation mechanism was brutally simple: upon infecting a system, it scanned every IP address reachable from the compromised machine on TCP port 445, attempting the EternalBlue exploit against each responding host. On a flat network, this meant the worm could reach every device in the organization within minutes, workstations, servers, printers, medical devices, industrial controllers, anything running Windows with SMBv1 enabled. The **UK National Health Service (NHS)** suffered particularly severe impact because many NHS trusts operated aging Windows XP systems (for which Microsoft had stopped releasing regular patches in 2014) interconnected on flat internal networks, creating an environment where a single infection propagated to thousands of endpoints.

Organizations with effective VLAN segmentation and inter-VLAN firewall rules blocking port 445 experienced dramatically different outcomes. When WannaCry infected an endpoint in a segmented network, its TCP port 445 scanning probes were blocked at the VLAN boundary firewall, preventing propagation beyond the initially infected VLAN. The total scope of infection was bounded by the size of the breached segment rather than the entire organization's endpoint population.

**NIST SP 800-82 (Guide to Industrial Control Systems Security)** specifically addresses this scenario, the propagation of IT-originated malware into operational technology (OT) networks, and recommends strict segmentation with deny-all-except-specifically-permitted inter-zone firewall policies as the primary mitigation. The WannaCry event accelerated adoption of this guidance across industries, particularly in healthcare and manufacturing, where OT and IT networks had historically been less rigorously separated.

The kill switch discovery by security researcher Marcus Hutchins, registering the hardcoded domain `iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com` that WannaCry used as a sandbox detection mechanism, provides an additional important security lesson: many malware samples include evasion features that double as accidental circuit breakers. However, organizations should never rely on such external interventions for containment, **NIST SP 800-61 (Computer Security Incident Handling Guide)** emphasizes that containment through network isolation (segmentation) must be a planned, internal capability, not dependent on researcher intervention.

WannaCry (May 2017) caused the NHS to cancel about 19,000 appointments, direct harm to patients. Blocking the SMB port (445) at inter-VLAN firewall boundaries would have most reduced exposure, with minimal disruption to legitimate operations.
:::

%%%

---
unit: Compliance
code: PCI
title: PCI DSS and Network Segmentation
---
:::callout style=soft
**PCI DSS (Payment Card Industry Data Security Standard)** is the most prescriptive compliance framework for network segmentation in commercial environments. Organizations that process, store, or transmit payment card data must isolate those systems in a defined **Cardholder Data Environment (CDE)** using segmentation controls that are formally tested and documented.
:::

:::list heading="Key PCI DSS v4.0 Segmentation Requirements" style=plain
- **Requirement 1.2**: Build and maintain network security controls restricting inbound and outbound traffic to/from the CDE
- **Requirement 1.3.2**: Restrict inbound traffic to the CDE to only that which is necessary and deny all other traffic
- **Requirement 1.3.3**: Restrict outbound traffic from the CDE to only that which is necessary
- **Requirement 1.4.1**: Network security controls must be implemented between trusted and untrusted networks
- **Requirement 12.5.2**: Confirm PCI DSS scope and segmentation controls are tested at least every six months
:::

:::table
| Scope Status | Description | Example Systems |
|---|---|---|
| In-scope (CDE) | Systems that store, process, or transmit CHD | POS terminals, payment servers, card databases |
| Connected-to-CDE | Systems with network connectivity to CDE | Authentication servers, logging systems |
| Out-of-scope | Isolated from CDE by tested segmentation | Guest Wi-Fi, HR systems, general office VLAN |
:::

:::image src="images/15_pci_dss_segmentation.png" alt="PCI DSS scoping diagram: three concentric zones labeled with scope status, innermost red zone labeled 'Cardholder Data Environment (CDE): In Scope' containing POS terminal, payment server, and card database icons; middle yellow zone labeled 'Connected-to-CDE Systems: In Scope' containing authentication server and log collector; outer green zone labeled 'Out of Scope (Segmented)' containing guest Wi-Fi and HR workstation icons, firewall icons with PCI DSS Req. 1.3 labels sit at each zone boundary, and a 'Tested segmentation' callout points to the outer boundary" caption="PCI DSS segmentation scoping, only systems in or connected to the CDE are in scope for PCI DSS requirements; out-of-scope systems require tested, documented segmentation controls to maintain their out-of-scope status" width=full:::
:::
:::notes
PCI DSS is the compliance framework most directly tied to network segmentation as a formal, auditable control. Developed by the **PCI Security Standards Council** (founded by American Express, Discover, JCB, Mastercard, and Visa), PCI DSS applies to any organization that accepts, processes, stores, or transmits payment card data. Version 4.0 of the standard, released in March 2022 and effective for compliance validation from March 2025, significantly strengthened segmentation requirements and introduced annual penetration testing of segmentation controls as a formal requirement.

The central concept in PCI DSS segmentation is the **Cardholder Data Environment (CDE)**: the set of systems, people, and processes that store, process, or transmit **cardholder data (CHD)** or **sensitive authentication data (SAD)**. PCI DSS requirements apply to all systems in the CDE and all systems connected to the CDE. The compliance burden of PCI DSS is directly proportional to CDE scope, the more systems are in scope, the more extensive the audit and the higher the compliance cost. Effective network segmentation is therefore not just a security control under PCI DSS but a **scope reduction tool**: by isolating CDE systems with tested segmentation, organizations can demonstrate that adjacent systems (HR, guest Wi-Fi, general office) are out of scope, dramatically reducing compliance complexity.

**PCI DSS Requirement 1** ("Install and Maintain Network Security Controls") is the primary segmentation requirement. It mandates that organizations implement network security controls, firewalls, ACLs, routing restrictions, that restrict all traffic to and from the CDE to only what is explicitly necessary. The default posture must be deny-all, with explicitly permitted exceptions documented and justified. All inbound and outbound CDE traffic must be logged.

**PCI DSS v4.0 Requirement 12.5.2** introduces a significant new obligation: the penetration testing of segmentation controls at least every six months and after any changes to segmentation infrastructure. This means that organizations can no longer simply implement VLAN boundaries and assume they are effective, they must actively test, using penetration testing techniques, that the boundaries hold under attack conditions. This directly drives demand for periodic internal network penetration tests that specifically attempt to bypass VLAN boundaries, test for VLAN hopping vulnerabilities, and validate that CDE systems cannot be reached from out-of-scope network segments.

The 2013 Target breach discussed earlier was a PCI DSS failure in addition to a security failure, Target was certified PCI DSS compliant at the time of the breach, which highlighted gaps in how compliance audits were conducted. The subsequent strengthening of PCI DSS penetration testing requirements (Requirements 11.4 and 12.5.2 in v4.0) was partly a direct response to this incident and others like it.

Segmentation reduces PCI DSS scope: a firewall blocking all traffic between an HR VLAN and the POS VLAN can take HR systems out of scope, subject to the segmentation testing required under the standard. This links segmentation directly to compliance cost.
:::

%%%

---
unit: Compliance
code: NAC
title: Tool Spotlight, Network Access Control (NAC)
---
:::callout style=soft
**Network Access Control (NAC)** solutions enforce security policy on every device before granting network access, verifying device identity, health posture, and authentication before assigning a device to the appropriate VLAN. NAC acts as the automated gatekeeper that makes segmentation dynamic and enforces it at the point of connection.
:::

:::list heading="What NAC Checks Before Granting Access" style=plain
- **Device identity**: Is this a corporate-managed device? (certificate-based 802.1X authentication)
- **User authentication**: Is the connecting user who they claim to be? (Active Directory / RADIUS)
- **Device posture**: Is the OS patched? Is antivirus running and up to date? Is disk encryption enabled?
- **Policy compliance**: Is the device compliant with corporate endpoint policy?
:::

:::flow
Device connects to switch port or wireless AP
NAC enforces 802.1X authentication, device presents certificate or credentials
RADIUS server validates identity and queries endpoint health database
Based on policy: device assigned to appropriate VLAN (Corporate, Guest, Quarantine)
Non-compliant devices assigned to Quarantine VLAN, remediation instructions served via captive portal
Compliant corporate devices placed on Corporate VLAN with full policy-approved access
:::

:::image src="images/15_nac_vlan_assignment.png" alt="NAC workflow diagram: a device connects to a switch port and is placed in an initial authentication VLAN, a 802.1X authentication exchange arrow points right to a RADIUS server (labeled Cisco ISE or Aruba ClearPass) which checks identity provider and endpoint health database, three outcome paths branch downward from the RADIUS server: left path labeled 'Compliant corporate device' places the device in VLAN 10 Corporate; center path labeled 'Guest or unmanaged device' places the device in VLAN 30 Guest; right path labeled 'Non-compliant corporate device' places the device in VLAN 99 Quarantine with a captive portal remediation message, each VLAN is labeled with its network access level" caption="NAC dynamic VLAN assignment, 802.1X authentication and endpoint posture assessment determine which VLAN a connecting device is placed in, enforcing segmentation policy automatically at the point of connection" width=full:::
:::
:::notes
Network Access Control (NAC) is the technology layer that transforms static VLAN assignments into dynamic, policy-driven access enforcement. Without NAC, VLAN membership is typically configured statically by port, a specific switch port is assigned to VLAN 10, and whatever device plugs into that port joins VLAN 10, regardless of whether it is a corporate laptop, a personal phone, a contractor's machine, or a malicious device brought in by an attacker with physical access. NAC replaces this static model with dynamic, identity-and-posture-based VLAN assignment.

The technical foundation of NAC is **IEEE 802.1X**, a port-based network access control standard that requires all connecting devices to authenticate to a RADIUS authentication server before being granted network access. The 802.1X exchange involves three parties: the **supplicant** (the connecting device's 802.1X client software), the **authenticator** (the switch or wireless access point), and the **authentication server** (a RADIUS server such as Microsoft NPS, Cisco ISE, or Aruba ClearPass). When a device connects, the switch blocks all traffic except 802.1X EAP frames and forwards the authentication request to the RADIUS server. The RADIUS server validates the device's certificate or user credentials against Active Directory or another identity provider and returns an authentication decision along with **RADIUS attributes**, including the `Tunnel-Private-Group-ID` attribute, which tells the switch which VLAN to place the authenticated device in.

This dynamic VLAN assignment enables several powerful security capabilities. First, it means that a corporate laptop plugging into any port anywhere on the network will always be placed in the correct corporate VLAN, regardless of which physical port or location it connects from, eliminating the risk of misplaced static VLAN assignments. Second, it means that an unknown device, a personal phone, a contractor laptop, a visitor's machine, that cannot present a valid corporate certificate will be placed in a Guest or Quarantine VLAN rather than being blocked entirely, providing a safer fallback than full network denial. Third, **endpoint posture assessment** adds a further layer: NAC solutions can query the connecting device's health state (OS patch level, antivirus status, disk encryption state) and place non-compliant devices in a Quarantine VLAN regardless of whether they present valid credentials. A corporate laptop with valid credentials but an unpatched OS gets quarantined until remediated.

**Cisco Identity Services Engine (ISE)** and **Aruba ClearPass** are the dominant enterprise NAC platforms, both capable of 802.1X enforcement, posture assessment, guest lifecycle management, and integration with SIEM and threat intelligence feeds. Both support **TrustSec** (Cisco) or **ClearPass Policy Manager** (Aruba) for applying dynamic segmentation tags (SGTs) to traffic flows rather than just VLANs, enabling even more granular east-west segmentation in large campus environments.

**NIST SP 800-53 AC-17 (Remote Access)** and **IA-3 (Device Identification and Authentication)** directly map to NAC capabilities, requiring that devices be identified and authenticated before being granted network access. **ISO/IEC 27001:2022 Annex A.8.1 (User Endpoint Devices)** and **A.8.5 (Secure Authentication)** similarly align with NAC posture assessment and 802.1X authentication.

In 802.1X network access control, the RADIUS Access-Accept response carries the VLAN assignment (the Tunnel-Private-Group-ID attribute), so the switch places the authenticated device into the correct VLAN dynamically. Understanding this at the packet level clarifies how NAC enforcement actually works.
:::

%%%

---
unit: Practice
code: ACL
title: Worked Example, Writing Inter-VLAN ACLs
---
:::callout style=soft
Access Control Lists (ACLs) are the rule sets that enforce which traffic is permitted or denied at VLAN boundaries. Writing ACLs correctly, specific, ordered, and defaulting to deny, is where segmentation policy is translated into enforceable network configuration.
:::

:::steps
1. **Define the policy in plain English first**: "Office workstations (VLAN 10) may access the internal web server (VLAN 20) on HTTPS only. No other VLAN 10 to VLAN 20 traffic is permitted."
2. **Identify the source and destination**: Source = 192.168.10.0/24 (VLAN 10), Destination = 192.168.20.50/32 (web server), Port = TCP 443.
3. **Write the specific permit rule**: `permit tcp 192.168.10.0 0.0.0.255 host 192.168.20.50 eq 443`
4. **Write the explicit deny for all other VLAN 10→20 traffic**: `deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255`
5. **Terminate with implicit deny-all** (already present on Cisco IOS; explicit `deny ip any any log` is best practice for logging)
6. **Apply the ACL to the correct interface in the correct direction**: Applied inbound on the VLAN 10 SVI (or outbound on the VLAN 20 SVI) on the Layer 3 switch.
:::

:::table
| Rule # | Action | Source | Destination | Port | Purpose |
|---|---|---|---|---|---|
| 10 | PERMIT | 192.168.10.0/24 | 192.168.20.50/32 | TCP 443 | Office → Web server HTTPS |
| 20 | PERMIT | 192.168.20.50/32 | 192.168.10.0/24 | established | Return traffic (stateless ACL) |
| 30 | DENY | 192.168.10.0/24 | 192.168.20.0/24 | any | Block all other Office→Server |
| 40 | DENY | any | any | any | Catch-all deny with logging |
:::

:::image src="images/15_acl_worked_example.png" alt="ACL configuration diagram with two panels: left panel shows Cisco IOS CLI syntax for the four ACL rules listed in the table, permit and deny statements in green and red text respectively, applied to interface Vlan10 with 'ip access-group OFFICE-TO-SERVER in' command; right panel shows a traffic flow decision flowchart with four branch points corresponding to the four rules, a packet labeled 'Office PC → Web Server:443' follows the green permit path through Rule 10; a packet labeled 'Office PC → DB Server:1433' is blocked at Rule 30 with a red X; a packet labeled 'Rogue device → Finance Server:22' is blocked at Rule 40, each blocked packet has a 'Log entry generated' annotation" caption="Inter-VLAN ACL in practice, four ordered rules implement a precise least-privilege policy allowing only HTTPS from office workstations to the web server while logging and blocking all other cross-segment traffic" width=full:::
:::
:::notes
Writing effective ACLs is a practical skill that bridges network administration and security architecture. An ACL that is too permissive defeats the purpose of segmentation; an ACL that is too restrictive breaks legitimate business operations. The worked example on this slide represents the minimum viable process for translating a security policy statement into an enforceable network configuration.

The most important discipline in ACL design is **policy-first authoring**: begin with a clear English-language statement of what should be permitted and why, before writing a single rule. This forces the author to think about the business requirement rather than the technical implementation, reducing the risk of "permit all because I can't figure out what specifically is needed." In mature organizations, ACL rules are associated with approved change requests that document the business justification, the approver, and the review date, ensuring that rules are not left in place indefinitely after the business need has expired.

The **Cisco IOS ACL syntax** for an extended named ACL uses the format `ip access-list extended <NAME>` followed by numbered or unnumbered sequence entries. Each entry specifies the action (permit or deny), the protocol (ip, tcp, udp, icmp), the source address with wildcard mask, the destination address with wildcard mask, and optionally a port specification. Wildcard masks are the bitwise inverse of subnet masks: a /24 subnet mask of 255.255.255.0 becomes a wildcard of 0.0.0.255, where 0 bits mean "must match" and 1 bits mean "don't care." This is a frequent point of confusion for students coming from iptables or firewall GUI environments where CIDR notation is standard.

A critical subtlety for **stateless ACLs** (which is what Cisco IOS extended ACLs are by default) is the need to explicitly permit return traffic. When the Office VLAN workstation initiates a TCP connection to the web server on port 443, the three-way handshake and subsequent data exchange involve the web server sending responses back to the workstation. Rule 20 in the example uses the `established` keyword, which matches TCP packets with the ACK or RST bit set, meaning packets that are part of an established session, not new initiations. Without Rule 20, the web server's response packets would be blocked by Rule 30, and the TCP connection would never complete. For UDP and ICMP, stateless ACLs require separate explicit return rules since there is no equivalent of the `established` keyword. This is one reason why stateful firewalls are preferred over stateless ACLs for complex inter-VLAN policies, they track session state automatically and permit return traffic implicitly.

The **implicit deny** at the end of every Cisco ACL (Rule 40 in the example, made explicit with logging) is one of the most important security properties of ACL-based access control. Any packet not matched by an earlier rule is silently dropped. Making this implicit deny explicit with a `log` keyword ensures that blocked traffic generates log entries, feeding into a SIEM for anomaly detection. This aligns with **NIST SP 800-53 AU-2 (Event Logging)** and **AU-3 (Content of Audit Records)**, which require that denied network access attempts be logged with sufficient detail (source IP, destination IP, protocol, port, timestamp) to support incident investigation.

Translating a policy ("servers reachable from office on 443 and 22 only; guest reaches the internet only") into ACL rules, applying them and verifying with test traffic exposes the common mistakes, wrong interface direction and wrong wildcard mask, that otherwise reach production.
:::

%%%

---
unit: Practice
code: DMZ
title: DMZ Architecture, Deep Dive
---
:::callout style=soft
The **Demilitarized Zone (DMZ)** is a semi-trusted network segment designed to host services that must be accessible from the internet while ensuring that internet-side attackers cannot directly reach the internal network. A properly designed DMZ requires two separate firewall boundaries, not just one.
:::

::::columns
::col::
:::list heading="Single Firewall DMZ (Avoid)" style=plain
- One firewall with three interfaces: external, DMZ, internal
- All zone separation enforced by a single device
- Single point of failure, if firewall is misconfigured or compromised, attacker reaches all zones
- Lower cost but substantially weaker security
:::
::col::
:::list heading="Dual Firewall DMZ (Recommended)" style=plain
- Separate external firewall between internet and DMZ
- Separate internal firewall between DMZ and internal network
- Defense in depth: attacker must compromise two independent devices to reach internal zone
- Preferred for PCI DSS, HIPAA, and high-sensitivity environments
:::
::::

:::flow
Internet traffic arrives at external firewall (Firewall 1)
Firewall 1 permits only allowed inbound protocols to DMZ (HTTPS:443, SMTP:25)
DMZ server processes request, initiates no connections to internal network
If DMZ server is compromised, internal firewall (Firewall 2) blocks all unauthorized access
Internal users initiate outbound connections to DMZ for management only, via explicit ACL permit
All DMZ-to-internal connections denied by default, exceptions logged and audited
:::

:::image src="images/15_dmz_dual_firewall.png" alt="Dual firewall DMZ architecture diagram: the Internet cloud is on the far left, a right-facing arrow from the Internet passes through Firewall 1 (labeled External Firewall, permits inbound 443 and 25 only) into the DMZ zone containing a Web Server and Email Gateway, a second right-facing arrow from the DMZ passes through Firewall 2 (labeled Internal Firewall, denies all DMZ-originated connections, permits internal-initiated management only) into the Internal Network containing an Application Server and Database, attack path arrows show an attacker breaching the web server but being blocked at Firewall 2, with a 'Breach contained to DMZ' callout" caption="Dual-firewall DMZ, two independent firewall boundaries ensure that compromise of a DMZ server does not grant an attacker a direct path to the internal network" width=full:::
:::
:::notes
The DMZ concept originates from military terminology, a demilitarized zone is a buffer area between opposing forces where neither side maintains a military presence. In networking, the DMZ plays an analogous role: it is a buffer zone between the untrusted internet and the trusted internal network, where services that must be publicly accessible are hosted without the internal network being directly exposed.

The critical architectural question for any DMZ is whether to use a **single firewall** or a **dual firewall** design. The single-firewall three-interface model uses one physical firewall appliance with separate interfaces for the external (internet-facing), DMZ, and internal networks. All traffic policy is enforced by a single device. While this is simpler and cheaper to operate, it creates a single point of failure: if the firewall is misconfigured, if a firewall vulnerability is exploited (as occurred with CVE-2022-1388, a critical F5 BIG-IP vulnerability with CVSS score 9.8), or if the management interface is compromised, an attacker may be able to reconfigure rules granting themselves direct internal access. The internal network's security is entirely dependent on the integrity of one device.

The **dual firewall model** places a separate firewall between the internet and the DMZ (external firewall) and another separate firewall between the DMZ and the internal network (internal firewall). Ideally, these are from different vendors with different operating systems and software codebases, so that a vulnerability in one vendor's product does not simultaneously compromise both boundaries. This is the architecture recommended in **NIST SP 800-41 Rev. 1 (Guidelines on Firewalls and Firewall Policy)** for high-value environments and is implicitly required by **PCI DSS Requirement 1.4.1**, which mandates that network security controls be implemented between the CDE and untrusted networks, with the CDE treated as requiring multiple independent protection layers.

An often-overlooked DMZ security requirement is **egress control on DMZ servers**, restricting what connections DMZ servers can initiate outbound into the internal network. The default assumption should be that a DMZ server must never be the initiating party for connections into the internal zone. Internal servers may initiate connections into the DMZ for management and monitoring purposes, but DMZ-originated connections toward internal systems should require an explicit, business-justified exception. This egress restriction is critical because many attack chains work in the following sequence: compromise a public-facing DMZ web server, then use that foothold to initiate connections from the DMZ into the internal network. If the internal firewall permits all established connections from the DMZ, this second-stage pivot succeeds trivially. A deny-by-default egress policy on the internal firewall closes this path.

**ISO/IEC 27033-4 (Securing Communications Between Networks Using Security Gateways)** provides detailed technical guidance on DMZ architecture, firewall placement, and egress filtering. **NIST SP 800-53 SC-7 (Boundary Protection)** requires that organizations implement boundary protection at all external boundaries and at key internal boundaries, the DMZ perimeter represents precisely this requirement.

The 2014 JPMorgan Chase breach (76 million households) began with access to a DMZ server that lacked two-factor authentication, followed by internal pivoting, a case that makes the requirement for egress controls and complete coverage of authentication concrete.
:::

%%%

---
unit: Foundations
code: MIS
title: Common Misconceptions About Segmentation
---
:::callout style=soft
Segmentation is one of the most frequently misunderstood security controls. Organizations often deploy VLANs or subnets and assume they have achieved security goals that the technology alone cannot deliver. Correcting these misconceptions is as important as teaching the correct implementation.
:::

:::table
| Misconception | Reality |
|---|---|
| "VLANs are secure by default" | VLANs are only as secure as their configuration, VLAN hopping, DTP exploitation, and misconfigured ACLs can defeat them |
| "If I have a firewall, I don't need VLANs" | Firewalls and VLANs are complementary, VLANs provide L2 isolation; firewalls provide policy enforcement at L3+ |
| "Segmentation means attackers can't get in" | Segmentation controls what happens after a breach, not whether one occurs, it limits blast radius, not initial access |
| "Once configured, segmentation is set-and-forget" | Networks change; VLANs must be audited quarterly and penetration tested to validate boundaries remain effective |
| "Microsegmentation replaces VLANs" | Microsegmentation operates at the workload level (L7); VLANs operate at L2, both serve different functions and are often complementary |
| "Guest Wi-Fi isolation is optional" | Guest Wi-Fi on a shared VLAN with corporate devices is a well-documented attack vector, isolation is a baseline control |
:::

:::image src="images/15_misconceptions_segmentation.png" alt="Six-panel myth-vs-reality infographic: each panel has a red myth speech bubble on the left and a green reality correction box on the right, myths include 'VLANs are secure by default,' 'Firewalls replace VLANs,' and 'Segmentation prevents all breaches', reality boxes cite NIST SP 800-53, IEEE 802.1Q, and MITRE ATT&CK references alongside brief corrective statements, a header reads 'Common Segmentation Misconceptions'" caption="Segmentation misconceptions, six widely held but incorrect beliefs about network segmentation, each corrected with technical and standards-based context" width=full:::
:::
:::notes
Misconceptions about network segmentation are dangerous precisely because they create a false sense of security. An organization that has deployed VLANs but believes those VLANs are inherently secure may not audit their configuration, test their boundaries, or review their ACLs, leaving misconfigurations in place indefinitely. This slide exists to explicitly surface and correct the most common of these misconceptions.

**"VLANs are secure by default"**, this is perhaps the most dangerous misconception. VLAN security is entirely configuration-dependent. A switch with default settings, including DTP enabled on all ports and VLAN 1 as the native VLAN, is vulnerable to VLAN hopping attacks that can be executed with freely available tools. The IEEE 802.1Q standard defines the tagging mechanism but does not mandate security hardening, that responsibility lies entirely with the network administrator. NIST SP 800-53 CM-6 (Configuration Settings) requires that all network devices be configured according to documented security configuration standards, explicitly addressing this misconception.

**"Segmentation prevents all breaches"**, this misconception leads organizations to treat segmentation as a prevention control when it is primarily a containment control. Segmentation does not prevent phishing, credential theft, VPN exploitation, or web application attacks. It prevents the lateral movement that follows those initial compromises from reaching all systems in the organization. Understanding this distinction is critical for correctly scoping incident response plans, when a breach occurs in a segmented network, the response should include containment of the affected segment while maintaining operations in unaffected zones.

**"Once configured, segmentation is set-and-forget"**, network environments are dynamic. New systems are added, VLANs are extended to accommodate operational needs, firewall rules accumulate exceptions over time, and trunk configurations drift. PCI DSS v4.0 Requirement 12.5.2 mandates that segmentation controls be tested at least every six months and after any significant change, this requirement exists precisely because organizations consistently discovered during breaches that their segmentation had drifted from the intended design. ISO/IEC 27001:2022 requires that network security controls be reviewed as part of the periodic management review of the information security management system.

**"Microsegmentation replaces VLANs"**, microsegmentation and VLANs operate at different layers and solve different problems. VLANs provide Layer 2 broadcast domain isolation and are managed at the network infrastructure level. Microsegmentation provides Layer 3-7 workload-level policy enforcement and is managed at the hypervisor, SDN, or container orchestration level. In a well-designed architecture, both coexist: VLANs segment the network into zones, and microsegmentation provides additional granularity within those zones. Replacing VLANs with microsegmentation alone would eliminate the Layer 2 isolation that prevents broadcast-based attacks and simplifies routing architecture.

Reading a security assessment report to identify which misconceptions an organization operates under, and the specific remediation for each, is the applied analysis required in penetration testing, architecture review and compliance audit.
:::

%%%

---
unit: Practice
code: CHK
title: Mid-Lecture Checkpoint
---
:::callout style=soft
Pause and consolidate. Before we move into advanced topics, make sure these core concepts are solid, they underpin everything that follows.
:::

:::list heading="Knowledge Check, Answer These Before Moving On" style=plain
- What is the difference between an access port and a trunk port, and why does DTP create a security risk on access ports?
- Describe the two VLAN hopping attack methods and the specific configuration change that mitigates each one.
- A company has Guest Wi-Fi, Office workstations, Servers, and a public website. Draw (or describe) the VLAN zones and which traffic flows should be explicitly permitted between them.
- What is the difference between a single-firewall DMZ and a dual-firewall DMZ? In which scenario would you recommend each?
- Why does Zero Trust treat network location as an insufficient basis for granting trust, and what does it use instead?
- What is microsegmentation, and how does it differ from VLAN-based zone segmentation?
:::

:::callout style=line
**If you can answer all six without looking at your notes, you have a solid foundation for the compliance and advanced architecture content ahead. If any are unclear, revisit the relevant slide before proceeding.**
:::

:::image src="images/15_checkpoint_review.png" alt="Chalkboard-style graphic divided into six panels arranged in a 2x3 grid, each panel contains one of the six knowledge check questions in white text on a dark background with a space below for a written answer, a header reads 'Mid-Lecture Checkpoint: Network Segmentation Fundamentals' and a footer reads 'Revisit the relevant slide for any question you cannot answer from memory'" caption="Mid-lecture knowledge check, six questions covering trunk ports, VLAN hopping, zone design, DMZ architecture, Zero Trust, and microsegmentation" width=full:::
:::
:::notes
This checkpoint slide is deliberately placed between the core technical content and the advanced compliance and architecture material that follows. It serves two purposes: first, to help students self-assess whether they have internalized the foundational concepts well enough to build on them; and second, to give the instructor real-time feedback about which concepts require additional explanation before proceeding.

The six questions are calibrated to cover the full breadth of the material covered so far. The access port vs. trunk port question tests practical switch configuration knowledge that directly supports VLAN hopping prevention. The VLAN hopping question tests recall of two specific attack mechanisms and two specific mitigations, a paired recall exercise that builds stronger retention than general concept questions. The zone design question is an applied synthesis task that requires students to translate business requirements into network architecture decisions, a skill directly relevant to security design roles. The DMZ question tests architectural trade-off analysis. The Zero Trust question tests conceptual understanding of why a paradigm shift occurred. The microsegmentation question tests the ability to distinguish between two complementary but distinct technologies that are often conflated.

For instructors using an active learning model, this checkpoint slide works well as a **think-pair-share** exercise: give students two minutes to individually write answers to each question, then pair them to compare and discuss, then call on pairs to share their answers for a brief whole-class discussion. This takes approximately 15 minutes but dramatically improves retention compared to passive listening.

Alternatively, in a flipped classroom model, this slide can be assigned as a pre-class preparation task, with students submitting written answers before class. The instructor reviews the submissions before class to identify common misconceptions and adjust the live session to address them directly, focusing class time on the concepts where students demonstrated gaps rather than repeating content they already understood.

:::

%%%

---
unit: Strategy
code: SDN
title: Software-Defined Networking and Segmentation
---
:::callout style=soft
**Software-Defined Networking (SDN)** decouples the network control plane from the data plane, allowing network segmentation and routing policies to be defined, modified, and enforced programmatically through a centralized controller rather than by configuring individual devices. SDN enables dynamic, automated segmentation at scale.
:::

::::columns
::col::
:::list heading="Traditional Networking" style=plain
- Control plane and data plane on each device
- Configuration via CLI on individual switches/routers
- Policy changes require touching multiple devices
- Static VLAN and ACL configurations
- Manual audit and change management
:::
::col::
:::list heading="SDN Networking" style=plain
- Centralized controller manages control plane
- Data plane (switching/routing) on hardware devices
- Policy changes made once in controller, pushed to all devices
- Dynamic segmentation policies updated via API
- Automated compliance checking and audit trail
:::
::::

:::flow
Security team defines new segmentation policy in SDN controller UI or API
Controller translates policy into OpenFlow or NETCONF rules
Rules are pushed to all relevant switches and routers simultaneously
Data plane devices enforce rules immediately, no manual device CLI changes required
Policy changes are logged and versioned in the controller, full audit trail maintained
:::

:::image src="images/15_sdn_segmentation.png" alt="SDN architecture diagram: at the top, a centralized SDN Controller box labeled with 'OpenFlow / NETCONF / RESTCONF API', below it, three horizontal layers: top layer labeled 'Application Layer' with a Security Policy App and NAC integration icon; middle layer labeled 'Control Plane (SDN Controller)' with a centralized policy engine; bottom layer labeled 'Data Plane' showing five physical switches with hardware forwarding tables, bidirectional arrows labeled 'Southbound API (OpenFlow)' connect the controller to each switch; a 'Policy Push' animation arrow shows a single controller command propagating to all five switches simultaneously" caption="SDN architecture, a centralized controller separates policy definition from hardware enforcement, enabling organization-wide segmentation policy changes to be applied to all devices simultaneously through a southbound API" width=full:::
:::
:::notes
Software-Defined Networking (SDN) represents a fundamental architectural shift in how network segmentation policies are defined, deployed, and managed. In traditional switched networks, each switch and router independently maintains its own control plane, the logic that decides how to forward packets. When a network administrator wants to change a VLAN assignment, ACL rule, or routing policy, they must log into each affected device individually and make the configuration change. In a large enterprise with hundreds of switches, a policy change might require hours of manual work and creates significant risk of inconsistency, devices that are missed in a policy update may have different behavior than intended.

SDN addresses this by separating the **control plane** (the intelligence that decides how packets should be forwarded) from the **data plane** (the hardware that actually forwards packets based on forwarding tables). In an SDN architecture, the control plane is centralized in a **controller**, a software platform such as **OpenDaylight**, **ONOS**, **Cisco ACI (Application Centric Infrastructure)**, or **VMware NSX**, while the data plane remains distributed across physical or virtual switching hardware. The controller communicates with the switches using **southbound APIs**, commonly **OpenFlow**, **NETCONF**, or **RESTCONF**, to push forwarding rules and policy updates to the data plane devices.

For network segmentation, this architecture has transformative implications. A segmentation policy change that once required manual CLI configuration on dozens of switches can be implemented as a single API call to the SDN controller, which propagates the change to all relevant devices simultaneously. This dramatically reduces implementation time, eliminates the risk of inconsistent device configurations, and creates a full audit trail in the controller of who made what policy change and when. This audit trail directly supports **NIST SP 800-53 AU-2 (Event Logging)** and compliance audit requirements under PCI DSS and ISO/IEC 27001.

**Cisco ACI (Application Centric Infrastructure)** is the dominant enterprise SDN platform for data center environments. ACI introduces the concept of **endpoint groups (EPGs)**, logical collections of workloads with common security requirements, and **contracts** that define the permitted traffic flows between EPGs. This model maps directly onto the security concept of segmentation zones, enabling fine-grained microsegmentation policies to be expressed in business terms (e.g., "Web Tier EPG can communicate with Application Tier EPG on port 8080") rather than in IP-address-centric ACL syntax. The ACI controller (APIC) then translates these contracts into hardware forwarding rules on Nexus switches automatically.

**VMware NSX** provides an analogous SDN capability for virtualized environments, implementing the Distributed Firewall (DFW) in the hypervisor kernel to enforce east-west microsegmentation between VMs without traffic needing to traverse a physical appliance.

Software-defined networking and data center fabrics (Cisco ACI, VMware NSX) are a growing specialization in network security. The conceptual step from VLANs on a switch to endpoint groups in a policy fabric is the architectural evolution this material prepares students to understand.
:::

%%%

---
unit: Compliance
code: AUD
title: Segmentation Audit Checklist
---
:::callout style=soft
Segmentation controls that are deployed but never verified provide false assurance. A structured audit checklist ensures that VLAN configurations, firewall rules, and access control policies remain effective, correctly configured, and aligned with current business requirements over time.
:::

:::list heading="Segmentation Audit Checklist (Quarterly Review)" style=plain
- **VLAN inventory**: Confirm all VLANs are documented with purpose, owner, subnet, and last-reviewed date
- **Trunk port audit**: Verify all trunk ports have explicit VLAN allowlists, no `switchport trunk allowed vlan all`
- **Native VLAN**: Confirm native VLAN on all trunks is not VLAN 1 and is not used by any end devices
- **DTP status**: Confirm all access ports have `switchport nonegotiate`, no auto-negotiation enabled
- **ACL review**: Review all inter-VLAN ACLs for deprecated rules, overly permissive entries, and missing deny-log
- **Firewall rule audit**: Remove rules that are no longer business-justified; verify deny-by-default is in place
- **DMZ egress**: Confirm DMZ servers cannot initiate connections to internal network, test with penetration testing
- **NAC posture**: Verify 802.1X is enforced on all access ports; test with uncertified device connection
- **Penetration test**: Test VLAN hopping (DTP, double-tag), document results and any remediation
- **PCI scope validation**: Reconfirm that out-of-scope systems cannot reach CDE, test bidirectionally
:::

:::image src="images/15_segmentation_audit_checklist.png" alt="Printable-style audit checklist graphic with ten numbered rows corresponding to the checklist items above, each row has a checkbox on the left, the audit item text in the center, a 'Frequency' column showing 'Quarterly' or 'Annual/Post-change,' a 'Responsible Team' column, and a 'Standard Reference' column citing NIST SP 800-53, PCI DSS, or ISO 27001 Annex A control references, the checklist header reads 'Network Segmentation Quarterly Audit Checklist' with a company logo placeholder and date field" caption="Network segmentation audit checklist, ten quarterly review items covering VLAN configuration, trunk hardening, firewall rules, NAC, and penetration testing, each mapped to a compliance standard reference" width=full:::
:::
:::notes
A segmentation audit is not a one-time activity, it is a recurring operational discipline that reflects the dynamic nature of real networks. Devices are added, VLANs are extended to accommodate new business units, firewall rule exceptions accumulate over time, and access ports are reconfigured during moves and changes. Without a regular review process, the segmentation architecture that was carefully designed and correctly implemented at one point in time will drift into a less secure state as the network evolves.

The audit checklist on this slide is designed to be performed quarterly as a minimum, and immediately after any significant network change, which aligns with **PCI DSS v4.0 Requirement 12.5.2**, which mandates segmentation testing at least every six months and after any changes to segmentation infrastructure. For organizations subject to PCI DSS, the penetration testing of segmentation controls (confirming that out-of-scope systems cannot reach the CDE) must be documented and retained as evidence for the annual QSA (Qualified Security Assessor) audit.

The **VLAN inventory** item deserves particular attention. Many organizations deploy VLANs over time without maintaining a comprehensive, up-to-date record of what each VLAN is for, who owns it, and when it was last reviewed. VLANs created for temporary purposes, a trade show, a contractor project, a pilot deployment, frequently remain in the switch configuration indefinitely after the original purpose has concluded. Undocumented VLANs with ambiguous ownership are a common audit finding and frequently represent orphaned network segments that may have relaxed access controls.

**Trunk port audits** are particularly important because trunk misconfigurations are invisible in normal operation, a trunk carrying more VLANs than intended will forward all traffic correctly; the misconfiguration only becomes apparent when a penetration tester exploits it. Using the command `show interfaces trunk` on a Cisco switch reveals exactly which VLANs are allowed on each trunk link. Any trunk with `VLANs allowed: 1-4094` (the default if no explicit pruning has been applied) should immediately be investigated and pruned to the minimum required VLAN set.

The **penetration testing** item is the most powerful validation control. All of the configuration checks above can be supplemented, but not replaced, by an active test where a security professional or automated tool attempts to actually cross VLAN boundaries using VLAN hopping techniques, unauthorized inter-VLAN routing, and firewall rule bypass techniques. **NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment)** provides detailed guidance on penetration testing methodology, including network segmentation validation as a specific test category.

**ISO/IEC 27001:2022 Annex A.8.22 (Segregation in Networks)** requires that network segregation controls be reviewed as part of the organization's ongoing information security management processes. The audit checklist approach described here provides a practical implementation of this requirement, with each checklist item traceable to a specific standard reference, supporting audit evidence collection and ISMS documentation.

A network audit checks for common segmentation misconfigurations: native VLAN left as VLAN 1, dynamic trunk negotiation enabled, and trunks that allow all VLANs rather than only those required. Documenting these findings is the substance of security operations and compliance work.
:::

%%%

---
unit: Strategy
code: OT
title: OT/ICS Network Segmentation
---
:::callout style=soft
**Operational Technology (OT)** and **Industrial Control Systems (ICS)**, including SCADA systems, PLCs, and industrial sensors, require the most stringent network segmentation of any environment. These systems often run legacy operating systems, cannot be patched, and control physical processes where a cyber incident can cause physical harm, safety failures, or environmental damage.
:::

::::columns
::col::
:::list heading="OT/ICS Segmentation Requirements" style=plain
- Physical or logical separation from corporate IT networks (air gap preferred)
- If IT-OT connectivity is required: one-directional data diodes or strictly controlled DMZ
- No direct internet connectivity for OT systems
- Protocol-aware firewall inspection (Modbus, DNP3, EtherNet/IP)
- Real-time monitoring for anomalous commands or process deviations
:::
::col::
:::list heading="Relevant Standards" style=plain
- NIST SP 800-82 Rev. 3 (Guide to OT Security)
- IEC 62443 (Industrial Automation and Control Systems Security)
- NERC CIP (North American Electric Reliability Corporation Critical Infrastructure Protection)
- ISA/IEC 62443-3-3 (System Security Requirements and Security Levels)
:::
::::

:::image src="images/15_ot_ics_segmentation.png" alt="Purdue Model network hierarchy diagram with five labeled levels: Level 0 (Field Devices, sensors and actuators) at the bottom, Level 1 (Basic Control, PLCs and RTUs), Level 2 (Supervisory Control, SCADA HMI), Level 3 (Manufacturing Operations, historian, MES) with a horizontal 'Industrial DMZ' band separating Levels 3 and 4, Level 4 (Business Logistics, corporate ERP, IT systems) at the top, firewall icons sit between each level transition, data flow arrows show one-directional historian data replication across the Industrial DMZ, and red X symbols block all direct Level 0–2 to Level 4 connections" caption="Purdue Model OT/ICS network segmentation, five operational levels separated by firewall boundaries and an Industrial DMZ that allows historian data replication from OT to IT without permitting any direct connectivity between control systems and the corporate network" width=full:::
:::
:::notes
Operational Technology (OT) and Industrial Control Systems (ICS) represent the highest-stakes network segmentation scenario in cybersecurity. Unlike corporate IT environments where a breach results in data loss or business disruption, an OT/ICS breach can affect physical processes, power grid stability, water treatment, oil pipeline pressure, manufacturing line safety, and nuclear reactor cooling systems. The consequences of an OT/ICS breach can include physical damage to equipment, environmental harm, and risk to human life. This uniquely high-stakes environment drives the most stringent segmentation requirements in any sector.

The **Purdue Model** (also called the Purdue Enterprise Reference Architecture, PERA) is the long-standing reference architecture for OT/ICS network segmentation. Published in the 1990s by Theodore J. Williams at Purdue University, it defines five hierarchical levels: Level 0 (physical field devices, sensors and actuators), Level 1 (basic control, PLCs and RTUs), Level 2 (supervisory control, SCADA HMI systems), Level 3 (manufacturing operations, historians, MES), and Level 4 (business logistics, corporate IT, ERP). The model mandates that each level be separated from adjacent levels by firewall boundaries, and that no direct connectivity exist between Level 0–2 control systems and Level 4 corporate networks.

The **Industrial DMZ** between Levels 3 and 4 is the critical boundary point where OT data (process historian data, production metrics) must be made available to corporate business intelligence and ERP systems without creating a bidirectional network path that could allow corporate IT malware or attackers to reach control systems. This is typically implemented using a **data diode**, a hardware device that physically enforces one-directional data flow, allowing data to flow from OT to IT but making it electronically impossible for any traffic to flow in the reverse direction, or through a highly restricted DMZ server that polls OT data and replicates it to IT-accessible storage with no reverse path.

The **Stuxnet worm (2010)** (CVE-2010-2568 and associated vulnerabilities) is the definitive case study for OT/ICS segmentation. Stuxnet was a sophisticated piece of malware that targeted Siemens S7-315 PLCs controlling centrifuges in Iran's uranium enrichment program at Natanz. Stuxnet propagated via infected USB drives (exploiting Windows zero-days) and, even in an air-gapped facility, reached the PLCs and caused them to spin centrifuges at damaging speeds while reporting normal operation to the monitoring systems. The Stuxnet incident proved that even physical air gaps can be bridged through USB-based propagation and social engineering, but it also demonstrated that the absence of proper OT-specific monitoring allowed the attack to proceed undetected for months.

**NIST SP 800-82 Rev. 3 (Guide to Operational Technology Security)**, published in 2023, provides comprehensive guidance on OT segmentation, recommending physical separation where possible and strict, protocol-aware firewall inspection where IT-OT connectivity is required. **IEC 62443** is the international standard series for Industrial Automation and Control System (IACS) security, defining security levels (SL 1–4) for different risk environments and prescribing corresponding segmentation requirements. **NERC CIP** (CIP-005: Electronic Security Perimeters) mandates specific segmentation requirements for bulk electric system cyber assets.

Operational-technology and industrial control system segmentation is a distinct, growing specialization in critical infrastructure security. The Purdue Model and the lesson of Stuxnet are its starting points, and certifications such as GICSP and ISA/IEC 62443 are valued in energy, utilities and manufacturing.
:::

%%%

---
unit: Summary
code: SUM2
title: Segmentation Architecture, Putting It All Together
---
:::callout style=soft
Network segmentation is not a single technology, it is a layered architecture combining VLANs, subnetting, firewalls, ACLs, NAC, microsegmentation, and continuous monitoring into a coherent defense-in-depth strategy. Each layer addresses a different attack surface and provides independent value.
:::

:::table
| Layer | Technology | What it prevents |
|---|---|---|
| Layer 2 | VLANs (802.1Q) | Broadcast-domain traversal, lateral movement within switch fabric |
| Layer 3 | Subnetting + ACLs | IP-level inter-zone traffic without policy approval |
| Layer 4 | Firewall stateful inspection | Port/protocol-based unauthorized cross-zone sessions |
| Layer 7 | NGFW + DPI | Application-level attacks, command-and-control, data exfiltration |
| Identity | NAC (802.1X) | Unauthorized device network access and VLAN assignment |
| Workload | Microsegmentation | East-west lateral movement between individual workloads |
| Monitoring | SIEM + NDR | Anomalous inter-zone traffic, policy violation detection |
:::

:::image src="images/15_segmentation_architecture_summary.png" alt="Full segmentation architecture reference diagram: a large corporate network divided into six clearly labeled zones, Internet, DMZ, Office VLAN, Server VLAN, OT/ICS, and Guest Wi-Fi, each separated by labeled security controls (external firewall, internal firewalls, Layer 3 switch with ACLs, NAC enforcement points), a SIEM platform at the top right shows log collection arrows from all zone boundary devices, individual workload microsegmentation policy icons appear within the Server VLAN, technology labels annotate each control layer (802.1Q, 802.1X, NGFW, SDN, NIST SP 800-207 ZTA)" caption="Complete segmentation architecture, seven security layers from VLAN isolation through microsegmentation and continuous monitoring, each enforcing a distinct policy boundary that together create defense-in-depth against lateral movement and breach propagation" width=full:::
:::
:::notes
The segmentation technologies covered in this class, VLANs, ACLs, firewalls, NAC and microsegmentation, form a single layered defense-in-depth architecture rather than a collection of separate tools, with each layer providing distinct and complementary value.

The **Layer 2 VLAN layer** provides the foundational broadcast domain isolation that prevents link-layer attacks and establishes the structural boundaries that all higher-layer controls are built upon. It is implemented in the switch fabric and operates at wire speed without performance impact.

The **Layer 3 subnetting and ACL layer** enables IP-level policy enforcement at VLAN boundaries. By assigning each VLAN its own subnet and applying ACLs at inter-VLAN routing points, organizations implement a coarse-grained least-privilege policy that restricts which IP ranges can communicate with which other IP ranges on which ports. This layer aligns with **NIST SP 800-53 AC-4 (Information Flow Enforcement)**.

The **Layer 4 stateful firewall layer** extends ACL-level controls with session state tracking, enabling return traffic to be automatically permitted without explicit rules while providing more sophisticated anomaly detection than stateless ACLs.

The **Layer 7 Next-Generation Firewall and Deep Packet Inspection layer** adds application identification, SSL/TLS inspection, and threat prevention capabilities that catch application-layer attacks that pass through port and protocol filters. This is particularly important for detecting command-and-control traffic that uses legitimate protocols (HTTPS, DNS) to blend in with normal traffic.

The **identity layer (NAC)** enforces that only authenticated, policy-compliant devices can access the network and that each device is placed in the correct VLAN based on identity and posture. This prevents unauthorized device attachment from exploiting static VLAN assignments.

The **workload microsegmentation layer** provides east-west policy enforcement within zones, closing the gap that traditional VLAN segmentation leaves between individual workloads in the same segment. It is the final technical layer before the monitoring layer.

The **monitoring layer (SIEM and NDR)** is what makes all other layers actionable. Without logging, alerting, and analysis of inter-zone traffic flows, policy violations that do occur will go undetected indefinitely. SIEM integration of firewall deny logs, NAC authentication failures, and ACL match statistics provides the visibility that turns segmentation from a static control into a dynamic detection mechanism. This aligns with **NIST SP 800-53 SI-4 (System Monitoring)** and **NIST CSF 2.0 Detect Function**.

Together, these seven layers implement the Zero Trust principles of **NIST SP 800-207**, verify explicitly, use least privilege access, and assume breach, at every level of the network stack. No single layer is sufficient alone; their combined effect is a security architecture where each layer reduces the risk that the previous layer fails to catch.

:::

%%%

---
unit: Summary
code: FIN
title: Class 15, Key Takeaways and Looking Ahead
---
:::pullquote
A well-segmented network is not unbreachable, it is resilient. The goal is not to stop every attack but to ensure that no single attack becomes a total disaster.
:::

:::list heading="What You Should Know After Today" style=plain
- **VLANs** segment Layer 2 broadcast domains; 802.1Q tagging enables multiple VLANs on shared infrastructure
- **Trunk ports vs. access ports**: misconfigurations enable VLAN hopping, DTP and native VLAN hardening are required
- **Inter-VLAN routing** must pass through a policy enforcement point (router, L3 switch, or firewall)
- **DMZ** architecture provides a buffer zone for public-facing services; dual-firewall design is preferred
- **Defense in depth** at the network layer means multiple independent segmentation controls, not just VLANs
- **Zero Trust** eliminates implicit trust based on network location; microsegmentation enforces workload-level policy
- **Compliance** (PCI DSS, HIPAA, ISO 27001) mandates formal segmentation, documentation, and periodic testing
- **Case studies** (Target 2013, WannaCry 2017) demonstrate that segmentation failures have real, measurable business consequences
- **Audit discipline** is as important as initial configuration, segmentation must be tested and reviewed continuously
:::

:::list heading="Coming Up in Class 16" style=chips
- Malware taxonomy
- Ransomware mechanics
- Host-level defense controls
- EDR and endpoint detection
:::

:::image src="images/15_class_summary_takeaways.png" alt="Summary infographic styled as a network map with nine labeled node icons connected by lines, each node corresponds to one of the nine bullet points in the takeaways list, with the node icon matching the concept (VLAN tag icon for 802.1Q, lock icon for Zero Trust, compliance document icon for PCI/HIPAA, shield icon for defense in depth), a 'You Are Here' marker on the node labeled 'Network Segmentation' with an arrow pointing toward a 'Class 16: Malware' node on the right edge of the diagram" caption="Class 15 key takeaways, nine core segmentation concepts mapped as a network, with a bridge arrow pointing to Class 16's malware and endpoint defense content" width=full:::
:::
:::notes
Class 15 has covered the full spectrum of network segmentation, from the foundational IEEE 802.1Q VLAN tagging standard through advanced microsegmentation, Zero Trust Architecture, OT/ICS segmentation, and compliance frameworks. Today's material is foundational for the rest of the course: every subsequent class on attack techniques implicitly assumes the network environment those attacks are operating within, and understanding segmentation gives students the ability to evaluate both how attacks propagate and what architectural controls constrain them.

The most important single insight from today, worth repeating at the close of class, is the distinction between **prevention and containment**. Segmentation is a containment control. It accepts the premise that initial access will sometimes occur and asks: how do we ensure that initial access does not become total access? This framing shifts the security posture from the impossible goal of preventing every breach to the achievable goal of ensuring that every breach is bounded, detected, and recoverable from. This is the core philosophy of **NIST SP 800-160 Volume 2 (Cyber Resiliency)** and the **NIST Cybersecurity Framework 2.0's Respond and Recover functions**, security is not just about preventing bad events but about maintaining the ability to operate through and recover from them.

The **Target 2013** and **WannaCry 2017** case studies bookend the practical lessons perfectly. Target demonstrates that a single missing VLAN boundary between a vendor access zone and a POS network turned a low-risk third-party credential compromise into one of the most costly retail breaches in history. WannaCry demonstrates that the presence or absence of port 445 blocks at VLAN boundaries was the single most consequential variable in determining how much of an organization was affected by a self-propagating worm. Both cases are studies in the business value of unglamorous, methodical network architecture, the kind of work that looks like undifferentiated infrastructure management until the day it saves an organization from catastrophe.

Looking ahead to **Class 16**, the focus shifts from the network to the individual device. Malware attacks against endpoints represent the most common initial access vector that segmentation is designed to contain, understanding how malware works at the host level, how ransomware encrypts files and demands payment, and how Endpoint Detection and Response (EDR) tools detect and respond to these threats will complete the picture of how layered security controls work together. Students who leave today's class understanding segmentation will approach Class 16's malware content with a richer contextual understanding of the environment that malware must operate within and the controls that constrain what it can do after initial execution.

A company with a large security budget, strong perimeter defenses and a flat internal network can be more vulnerable than one with a smaller budget and effective internal segmentation, because the flat network lets a single compromise spread unchecked. This is the architectural thinking that distinguishes security engineers from tool operators.
:::
