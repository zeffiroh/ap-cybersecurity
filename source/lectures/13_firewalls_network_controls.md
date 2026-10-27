---
deck:
  title: Firewalls & Network Controls
  kicker: Class 13
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 13
  description: How firewalls decide what traffic is allowed to exist on a network, and where they fall short.
  topics: [Firewall Purpose, Stateful/Stateless Firewalls, ACLs, Traffic Filtering]
---

---
title: Firewalls & Network Controls
cover: true
---
:::text class=sub
The gatekeeper deciding which packets even get to try
:::

:::image src="images/13_firewall_overview.png" alt="Conceptual diagram of a firewall positioned between a trusted internal network and the untrusted Internet, with traffic arrows showing allowed and blocked packets" caption="Firewalls enforce policy at the network boundary, separating trusted internal networks from untrusted external ones" width=full
:::

::::columns
::col::
:::list heading="Core Concepts" style=plain
- Packet Filtering
- Stateful Inspection
- Access Control Lists (ACLs)
- Deep Packet Inspection (DPI)
:::
::col::
:::list heading="Control Mechanisms" style=plain
- Network Address Translation (NAT)
- Zone-Based Policies
- Application Layer Filtering
- Threat Intelligence Integration
:::
::col::
:::list heading="Standards & Frameworks" style=plain
- NIST SP 800-41 (Firewall Policy Guide)
- ISO/IEC 27033 (Network Security)
- RFC 4949 (Internet Security Glossary)
:::
::::
:::notes
Firewalls serve as the foundational network security control, acting as a gatekeeper that enforces access policies by inspecting and filtering network traffic based on predetermined security rules. At their core, firewalls implement packet filtering mechanisms that evaluate packets against rule sets specifying which traffic to permit or deny. These rules typically consider attributes such as source and destination IP addresses, port numbers, and protocol types.

Modern firewalls extend beyond static packet filtering through stateful inspection, which tracks the state of active connections and makes dynamic decisions based on the context of traffic flows. This approach significantly enhances security by ensuring that only legitimate, established connections are allowed to pass through the network perimeter.

Access Control Lists (ACLs) form the basis of many firewall rule implementations, providing a structured method for defining traffic permissions. They are widely used in both hardware and software-based firewalls to enforce network segmentation and limit lateral movement within networks. The deployment of firewalls aligns with key cybersecurity frameworks such as NIST Special Publication 800-41, which provides comprehensive guidance on firewall policy development and configuration, and ISO/IEC 27033, which outlines best practices for network security controls.

In practice, firewalls operate at multiple layers of the OSI model, from basic network-layer filtering to advanced application-layer inspection. This layered approach enables organizations to defend against a wide range of threats, from simple unauthorized access attempts to sophisticated application-layer attacks. As network architectures evolve, firewalls continue to adapt, incorporating technologies such as deep packet inspection (DPI), intrusion prevention systems (IPS), and threat intelligence feeds to provide comprehensive network security coverage.

Historically, firewall technology dates to 1988, when Bill Cheswick and Steve Bellovin at Bell Labs developed the first packet-filtering gateway, followed by Digital Equipment Corporation (DEC) deploying a commercial packet filter in 1989. Check Point Software introduced stateful inspection with FireWall-1 in 1994, fundamentally shifting the paradigm from per-packet evaluation to session-aware filtering. Today, Next-Generation Firewalls (NGFWs) from vendors such as Palo Alto Networks and Cisco (FirePOWER) incorporate deep packet inspection, application identification (App-ID), and threat intelligence integration. The 2013 Target data breach, in which attackers used compromised HVAC vendor credentials to traverse insufficiently segmented networks, illustrates the catastrophic consequences of inadequate firewall policy and network segmentation, reinforcing the continued importance of robust firewall configuration aligned with NIST SP 800-125B guidance on virtualized firewall architectures.
:::

%%%

---
unit: Foundations
code: FWL
title: What Is a Firewall?
---
:::callout style=soft
A **firewall** is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules. It establishes a barrier between trusted internal networks and untrusted external networks, such as the Internet.
:::

:::image src="images/13_firewall_decision_process.png" alt="Diagram showing the firewall packet evaluation pipeline: packet arrives, rules evaluated top to bottom, action applied (Allow/Deny/Log/Alert), packet forwarded or dropped" caption="A firewall evaluates every packet against an ordered rule set and applies the first matching action, Allow, Deny, Log, or Alert" width=full
:::

:::flow
1. Packet arrives at the firewall interface
2. Rule set evaluated sequentially from top to bottom
3. First matching rule action applied: Allow, Deny, Log, or Alert
4. Permitted packets forwarded to destination; denied packets dropped
5. All events logged for audit trail and forensic review
:::

::::columns
::col::
:::list heading="Core Functions" style=plain
- Packet filtering
- Stateful inspection
- Proxy services
- Network Address Translation (NAT)
:::
::col::
:::list heading="Deployment Types" style=plain
- Hardware-based
- Software-based
- Cloud-hosted
- Next-Generation Firewalls (NGFW)
:::
::col::
:::list heading="Rule Enforcement" style=plain
- Allow
- Deny
- Log
- Alert
:::
:::pullquote
Every attack from last class still has to cross this checkpoint first.
:::
::::

:::notes
A firewall serves as the first line of defense in network security architecture by enforcing access control policies at network boundaries. It operates by evaluating packets or sessions against a defined rule base, determining whether traffic should be permitted, denied, or further inspected. This mechanism is essential in mitigating threats such as unauthorized access, port scanning (e.g., CVE-2002-1749), and service exploitation.

Firewalls implement various techniques to achieve traffic control. At the most basic level, **packet filtering** firewalls inspect headers of individual packets, such as source/destination IP addresses, protocol types (TCP, UDP, ICMP), and port numbers. More advanced systems use **stateful inspection**, which tracks the state of active connections and makes decisions based on the context of traffic flow. Modern **Next-Generation Firewalls (NGFWs)** extend these capabilities by integrating intrusion prevention systems (IPS), deep packet inspection (DPI), and application-layer filtering.

According to NIST Special Publication 800-41 Revision 1, firewalls are critical components for maintaining network segregation and enforcing boundary protection. They support compliance with frameworks like ISO/IEC 27001 by providing mechanisms to control information flows and reduce attack surface exposure. While not infallible, particularly against encrypted or application-layer attacks, firewalls remain foundational in layered defense strategies.

The importance of correct firewall configuration is underscored by real-world breach case studies. The 2013 Target Corporation breach, which exposed 40 million payment card records, partly stemmed from inadequate network segmentation: a vendor-managed HVAC system shared network access with point-of-sale infrastructure, allowing attackers to pivot laterally once they compromised vendor credentials. Properly enforced firewall rules isolating payment systems (as mandated by PCI DSS Requirement 1.3) could have significantly limited the blast radius of that intrusion. Similarly, the 2020 SolarWinds supply chain attack highlighted that perimeter firewalls alone cannot prevent threats originating from trusted software update channels. NIST SP 800-53 Control AC-4 (Information Flow Enforcement) specifically addresses the need for firewall policies that enforce information flow restrictions across defined security boundaries, reinforcing that firewalls must be part of a comprehensively managed security program rather than a standalone safeguard.
:::

%%%

---
unit: Types
code: SLF
title: Stateless Firewalls
---
:::callout style=soft
A **stateless firewall** operates by inspecting individual packets in isolation, applying a static rule set without retaining any context or state information from previous packets. This design prioritizes speed and simplicity over deep session awareness.
:::

:::image src="images/13_stateless_firewall.png" alt="Diagram of a stateless firewall inspecting a single packet in isolation, showing the packet header fields (src IP, dst IP, port, protocol) being compared against a static ACL rule table without any connection state memory" caption="Stateless firewalls evaluate each packet independently against a fixed rule set, fast, but blind to session context" width=full
:::

:::flow
1. Packet arrives at the network interface
2. Header fields extracted: source IP, destination IP, port numbers, protocol
3. Fields compared against static ACL rule set from top to bottom
4. First matching rule action applied: Allow or Deny
5. Packet forwarded or dropped, no state information retained
:::

:::list heading="Key Characteristics" style=plain
- Operates on a per-packet basis with no memory of prior traffic
- Evaluates static fields: source/destination IP, port numbers, protocol type
- High performance due to minimal processing overhead
- Lacks the ability to detect packet sequence anomalies or session hijacking
- Vulnerable to certain spoofing and DoS attacks due to absence of state tracking
:::

::::columns
::col::
:::table
| Feature              | Stateless Firewall         |
|----------------------|----------------------------|
| Packet Inspection    | Individual, Isolated       |
| Resource Usage       | Low                        |
| Rule Dependency      | Static ACLs                |
| Session Awareness    | None                       |
| Performance          | High                       |
| Security Limitations | Susceptible to spoofing    |
:::
::col::
:::table
| Protocol Layer       | Supported                  |
|----------------------|----------------------------|
| Network Layer        | IPv4, IPv6                 |
| Transport Layer      | TCP, UDP, ICMP (basic)     |
| Application Layer    | No inspection              |
| Connection Tracking  | Not supported              |
:::
::::

:::notes
A stateless firewall, also referred to as a static packet-filtering firewall, represents the foundational model of network access control. Defined in NIST Special Publication 800-41 Rev. 1, this firewall type inspects each packet based solely on predefined criteria such as source and destination IP addresses, transport protocol (e.g., TCP, UDP), and port numbers. It does not maintain any record of active connections or prior packet exchanges, which differentiates it from its more advanced counterpart, the stateful firewall.

This architectural choice results in high-speed packet processing and low resource consumption, making it suitable for environments where performance is prioritized over granular security. However, the lack of session context introduces significant limitations. For instance, it cannot determine whether an incoming packet is part of a legitimate ongoing communication or a maliciously crafted packet that simply matches an allowed rule. This limitation renders stateless firewalls vulnerable to IP spoofing, certain denial-of-service (DoS) attacks, and unauthorized access attempts that exploit rule-based oversights.

In practice, stateless firewalls are often deployed at network boundaries where basic filtering is sufficient, or in high-throughput scenarios such as DDoS mitigation layers. They are typically implemented using Access Control Lists (ACLs) on routers or simple filtering rules in software-based firewalls. While they offer minimal protection against advanced threats, they remain a critical baseline control in defense-in-depth strategies, as outlined in ISO/IEC 27001 Annex A controls for boundary protection.

Several specific vulnerabilities exploit the stateless firewall's inability to track packet sequences. The classic IP fragment overlap attack (CVE-1999-0242, also known as the Teardrop attack) sent malformed fragmented packets whose overlapping offsets caused vulnerable TCP/IP stacks to crash, and stateless filters that allowed fragmented traffic were unable to detect the malformation because they inspected fragments in isolation. Similarly, TCP RST spoofing attacks (documented in CVE-2004-0230) can terminate legitimate connections because a stateless firewall permits any packet matching the source/destination IP and port, regardless of sequence number validity. RFC 2827 (Network Ingress Filtering) was published precisely to address the IP spoofing problem at the ISP router level, mandating that service providers block packets whose source addresses do not match legitimate customer address space. The 2016 Mirai botnet attacks further demonstrated stateless filtering's limits: compromised IoT devices with unrestricted outbound internet access (common in ISP border configurations with minimal stateless filtering) were able to generate Tbps-scale UDP reflection floods. These examples collectively reinforce why stateless filtering, while valuable for performance-sensitive perimeter roles, must be supplemented by stateful inspection in any environment handling sensitive data.
:::

%%%

---
unit: Types
code: STF
title: Stateful Firewalls
---
:::callout style=soft
A **stateful firewall** maintains dynamic state information for each active network connection. It inspects not only individual packets but also their context within a communication session, allowing or denying traffic based on the connection's current state (e.g., NEW, ESTABLISHED, RELATED, INVALID).
:::

:::image src="images/13_stateful_firewall.png" alt="Diagram of a stateful firewall with a connection state table showing NEW, ESTABLISHED, RELATED, and INVALID states alongside a packet flow illustrating how return traffic is validated against the state table" caption="Stateful firewalls maintain a dynamic connection table, validating each packet against its session context before allowing it through" width=full
:::

::::columns
::col::
:::flow
1. Initial packet arrives
2. Firewall inspects and creates state entry
3. State table updated
4. Return traffic validated against state
5. Matching packets allowed; mismatched dropped
:::
::col::
:::table
| Connection State | Description                        |
|------------------|------------------------------------|
| NEW              | First packet of a new connection   |
| ESTABLISHED      | Part of an existing connection     |
| RELATED          | Related to an existing connection  |
| INVALID          | Cannot be identified or tracked    |
:::
::col::
:::list heading="Key Protocols & Standards"
- TCP/IP state tracking
- RFC 793 (TCP specification)
- NIST SP 800-91 (Firewall Policy Guide)
- ISO/IEC 27001 (Information Security Controls)
:::
::::

:::notes
A stateful firewall operates by maintaining a state table that tracks the status of all active connections passing through it. Unlike stateless firewalls, which evaluate each packet in isolation based solely on static rules such as IP addresses and port numbers, stateful firewalls understand the context of traffic flows. This enables them to make more intelligent decisions about what traffic to allow or block.

When a new connection is initiated, such as a TCP SYN packet from a client to a server, the firewall inspects the packet and creates an entry in its state table. This entry typically includes source and destination IP addresses, port numbers, protocol type, and the current connection state (e.g., NEW). As the connection progresses, the firewall updates the state accordingly, such as marking it as ESTABLISHED once the handshake is complete.

Return traffic is then validated against this state table. Only packets that match an existing, legitimate connection are permitted through. This mechanism significantly enhances security by preventing unsolicited inbound traffic, which is a common vector for attacks such as IP spoofing or TCP SYN flooding.

The concept aligns with guidelines from NIST Special Publication 800-91, which emphasizes the importance of maintaining secure firewall configurations and monitoring connection states to enforce network segmentation. Similarly, ISO/IEC 27001 highlights the need for secure boundary protection mechanisms, of which stateful inspection is a core component.

This approach effectively closes the gap left by stateless filtering, where malicious actors could potentially bypass simple rule sets. As a result, stateful firewalls have become a foundational element of modern network security infrastructure.

Despite their advantages, stateful firewalls are not invulnerable. State table exhaustion attacks, commonly known as SYN flood attacks, deliberately send large volumes of half-open TCP connections, filling the firewall's state table until it can no longer track new legitimate connections. CVE-2018-0151 disclosed a memory exhaustion vulnerability in Cisco IOS stateful firewall implementations that could be exploited via crafted TCP packets to trigger a denial-of-service condition, illustrating that even the state-tracking mechanism itself can become an attack surface. On Linux systems, stateful inspection is widely implemented through the Netfilter/nf_conntrack kernel subsystem, used by iptables and nftables. Properly tuning connection tracking table limits (e.g., nf_conntrack_max) and timeout values is essential to prevent resource exhaustion in high-traffic environments, a consideration documented in CIS Benchmarks for Linux and reinforced by NIST SP 800-123 guidance on server hardening.
:::

%%%

---
unit: Comparison
code: CMP
title: Stateless vs Stateful
---

:::image src="images/13_stateless_vs_stateful_comparison.png" alt="Side-by-side comparison diagram of a stateless firewall (no memory, evaluates each packet independently) and a stateful firewall (maintains a session state table, validates packet context), highlighting the session state table as the key differentiator" caption="The session state table is what separates stateful firewalls from stateless ones, it provides the context needed for intelligent traffic decisions" width=full
:::

::::columns
::col::
:::callout
**Stateless Firewalls**
Operate at Layer 3/4, inspecting individual packets without retaining session context.
:::
:::list heading="Characteristics" style="tight"
- No memory of previous packets
- Fast and lightweight
- Rule-based on static fields: IP, port, protocol
- Vulnerable to certain spoofing and DoS attacks
:::
::col::
:::callout
**Stateful Firewalls**
Maintain state tables to track active connections and validate packet sequences.
:::
:::list heading="Characteristics" style="tight"
- Tracks connection states: NEW, ESTABLISHED, RELATED, INVALID
- Enforces protocol compliance (e.g., TCP handshake)
- Provides deeper context for filtering decisions
- Resistant to certain types of session hijacking
:::
::col::
:::table
| Feature              | Stateless            | Stateful                   |
|----------------------|----------------------|----------------------------|
| Memory of connections| None                 | Tracks active connections  |
| Speed                | Faster, simpler      | Slightly more overhead     |
| Security             | Basic filtering      | Context-aware filtering    |
| Typical use          | Simple ACLs, routers | Enterprise network perimeters |
:::
::::

:::notes
In network security, the distinction between stateless and stateful firewalls lies in how they process and evaluate network traffic. Stateless firewalls operate primarily at Layers 3 and 4 of the OSI model, making decisions based solely on static header information, such as source IP, destination IP, protocol type, and port numbers, without retaining any knowledge of prior packets. This makes them fast and efficient, but inherently limited in their ability to detect anomalies or illegitimate traffic that mimics legitimate patterns.

In contrast, stateful firewalls maintain a dynamic state table (also known as a connection table) that records the status of active connections. Each TCP or UDP session is tracked through its lifecycle, including states such as NEW, ESTABLISHED, RELATED, and INVALID, as defined in RFC 4787 and commonly implemented in systems like iptables or Cisco ASA. This enables the firewall to enforce protocol compliance and detect deviations, such as unsolicited incoming packets that do not belong to any known session.

From a standards perspective, NIST Special Publication 800-96 emphasizes the importance of stateful inspection in enforcing secure network communications, particularly in demilitarized zones (DMZs) and enterprise perimeters. CVEs such as CVE-2019-11510 have highlighted vulnerabilities in stateless filtering mechanisms that fail to validate session context, leading to unauthorized access.

While stateful firewalls introduce computational overhead due to memory and processing demands for maintaining session state, the trade-off is significantly improved security posture. As such, most modern network security architectures, including those aligned with ISO/IEC 27001 and NIST SP 800-207 (Zero Trust), favor stateful inspection as a foundational control for traffic filtering and micro-segmentation.

In practice, many enterprise architectures combine both approaches strategically. High-performance border routers at the network edge often deploy stateless ACLs to filter at line rate, blocking known-bad source IP ranges, enforcing ingress filtering per RFC 2827, and rejecting obviously invalid protocol combinations, while stateful firewalls sit behind them at the DMZ perimeter enforcing connection-level policy. This tiered model balances throughput demands with the security assurance of session awareness. Compliance frameworks reinforce this distinction: PCI DSS Requirement 1.2 explicitly mandates stateful inspection for firewalls protecting cardholder data environments, and AWS Security Groups, a widely-used cloud security control, implement stateful filtering by default, automatically allowing return traffic for established connections without additional inbound rules. Understanding the trade-offs between these two models is fundamental to designing scalable, secure network architectures.
:::

%%%

---
unit: ACLs
code: ACL
title: Access Control Lists (ACLs)
---
:::callout style=soft
An **Access Control List (ACL)** is an ordered set of rules that explicitly permits or denies traffic based on defined criteria such as source/destination IP addresses, port numbers, and protocol types. ACLs form the foundational mechanism for enforcing network-level access control in firewalls, routers, and switches.
:::

:::image src="images/13_acl_rule_evaluation.png" alt="Diagram of ACL rule evaluation showing a packet being compared against rules 1 through 4 in sequence, with an arrow stopping at the first match and an implicit deny-all at the bottom of the rule list" caption="ACLs use first-match-wins logic, packet evaluation stops the moment a rule matches, making rule order critically important" width=full
:::

:::steps heading="ACL Rule Evaluation Process"
1. Packet arrives and is compared against Rule 1
2. If matched: apply action (Allow or Deny) and stop evaluation
3. If not matched: advance to Rule 2 and repeat comparison
4. Continue sequentially until a matching rule is found
5. If no rule matches: implicit deny-all rule applied, packet dropped
:::

:::table
| Rule Order | Action | Criteria |
|------------|--------|----------|
| 1          | Allow  | Traffic from trusted internal network (e.g., 192.168.10.0/24) |
| 2          | Deny   | Traffic from known-malicious IP range (e.g., 203.0.113.0/24) |
| 3          | Allow  | HTTPS traffic (TCP port 443) from any source |
| 4          | Deny   | All other traffic (implicit deny-all rule) |
:::

:::text
ACLs operate on a **first-match-wins** basis. This means that the firewall or router evaluates each packet against the rules in sequence, from top to bottom. Once a match is found, the corresponding action (permit or deny) is applied, and further rule evaluation stops. This behavior makes rule ordering critical to the correct enforcement of policy.
:::

:::list heading="Key Characteristics of ACLs" style=plain
- **Ordered Evaluation**: Rules are processed sequentially.
- **Explicit vs Implicit Rules**: Explicit rules are defined by administrators; an implicit "deny all" rule typically exists at the end.
- **Stateless by Default**: Standard ACLs do not track connection state (unlike stateful firewalls).
- **Granular Filtering**: Can filter based on Layer 3 (IP) and Layer 4 (TCP/UDP) attributes.
:::

:::notes
Access Control Lists (ACLs) are a foundational element of network security, widely implemented in routers, switches, and firewalls to regulate traffic flow based on predefined security policies. Each ACL consists of an ordered sequence of rules that define whether to permit or deny packets based on attributes such as source and destination IP addresses, transport layer protocols (e.g., TCP, UDP, ICMP), and port numbers.

The **order of rules** is critical in ACL operation due to the first-match-wins logic. For example, if a broad permit rule is placed before a more specific deny rule, the deny rule may never be evaluated, leading to unintended access. This principle aligns with the **principle of least privilege**, a core tenet in cybersecurity frameworks such as NIST SP 800-53 and ISO/IEC 27001, which advocates for granting only the minimum necessary access to perform a function.

ACLs are typically classified into two types:
- **Standard ACLs**: Filter traffic based only on source IP address. These are less granular and generally applied closer to the destination.
- **Extended ACLs**: Provide more granular control by filtering on source/destination IP, protocol, and port numbers. These are typically applied closer to the source to minimize unnecessary traffic propagation.

Most network devices implement an **implicit deny** rule at the end of every ACL. This ensures that any traffic not explicitly permitted is denied by default, reducing the risk of unintentional exposure. Misconfigurations in ACLs have historically led to critical vulnerabilities, such as those exploited in CVE-2016-6652, where improper rule ordering allowed unauthorized network access.

In modern network architectures, ACLs are often augmented by stateful inspection and application-layer filtering, but they remain a core component of defense-in-depth strategies.

ACL misconfigurations represent one of the most common causes of unauthorized network access in enterprise environments. IP fragment-based attacks (CVE-2003-0567) exploit the fact that standard ACLs may not correctly handle fragmented packets, allowing subsequent fragments carrying malicious payloads to bypass rules that only matched the first fragment's port information. NIST SP 800-53 Control AC-3 (Access Enforcement) maps directly to ACL implementations, requiring that information systems enforce approved authorizations for logical access to information resources. Enterprise-scale ACL management is further complicated by rule bloat: Cisco IOS supports up to 65,535 ACL entries per interface, and organizations with large legacy rule sets frequently carry thousands of redundant or shadowed rules accumulated over years of network changes. Dedicated firewall policy management tools such as Tufin Orchestration Suite and AlgoSec Firewall Analyzer are widely used to audit ACL rule bases, identify shadowed or conflicting entries, and demonstrate compliance with PCI DSS Requirement 1.1.6, which mandates documentation and justification of all permitted services, protocols, and ports.
:::

%%%

---
unit: Filtering
code: TRF
title: Traffic Filtering Criteria
---

:::image src="images/13_traffic_filtering_criteria.png" alt="Layered diagram showing the OSI model with firewall filtering criteria mapped to each layer: Layer 3 (IP addresses), Layer 4 (ports and protocol), Layer 7 (application identifiers and payload), with an arrow indicating the packet flow through each inspection layer" caption="Modern firewalls apply filtering criteria across multiple OSI layers, from IP addresses and ports at L3/L4 to application signatures and payload content at L7" width=full
:::

:::flow
1. Packet arrives at the firewall
2. Layer 3 evaluated: source and destination IP addresses checked against policy
3. Layer 4 evaluated: port numbers and protocol type (TCP/UDP/ICMP) verified
4. Direction evaluated: inbound or outbound relative to the protected zone
5. Extended inspection applied if enabled: DPI, time-based rules, application-layer identifiers
6. Allow or Deny decision applied based on the first matching rule
:::

::::columns
::col::
:::list heading="Core Filtering Dimensions" style=plain
- Source and destination IP address
- Source and destination port number
- Protocol type (TCP, UDP, ICMP, etc.)
- Traffic direction (inbound vs outbound)
:::
::col::
:::list heading="Extended Filtering Capabilities" style=plain
- Packet payload inspection (deep packet inspection)
- Time-based rules (schedule-based access)
- Interface or zone-based filtering
- Application layer identifiers (e.g., HTTP headers)
:::
::::
:::notes
At the heart of stateless and stateful packet filtering lies the ability to make allow/deny decisions based on specific attributes of network traffic. These attributes, known as filtering criteria, are derived directly from the structure of the IP packet and session context. The most fundamental criteria include the source and destination IP addresses, which identify the communicating endpoints; the source and destination port numbers, which specify the sending and receiving services or applications; and the protocol field, which indicates whether the packet is using TCP, UDP, ICMP, or another protocol. These fields are part of the IP header and transport layer headers, as defined in RFC 791 (IP) and RFC 793 (TCP).

Additionally, firewalls evaluate the direction of traffic, whether it is inbound (entering the protected network) or outbound (leaving it). This directional context is critical for implementing security policies that, for example, permit internal users to initiate outbound web requests while blocking unsolicited inbound connections, which are more commonly associated with attacks. Directionality is especially important in perimeter defense strategies outlined in NIST Special Publication 800-41 Rev. 1 on firewall policies.

Modern firewalls extend these basic criteria through deep packet inspection (DPI), enabling them to analyze payload contents, detect application signatures, and enforce time-based rules. These extended capabilities allow for more granular control, aligning with ISO/IEC 27001 Annex A controls on network security and access restrictions. For instance, a firewall might block traffic to known-malicious domains identified in threat intelligence feeds, or restrict access to certain services during non-business hours to reduce attack surface.

Together, these filtering dimensions form the basis of access control mechanisms that enforce network segmentation and protect against threats such as port scanning (e.g., CVE-2002-1745) or unauthorized service access. Understanding these criteria is essential for designing secure network architectures and implementing defense-in-depth strategies.

Next-generation firewall platforms extend Layer 7 filtering significantly beyond basic port and protocol identification. Palo Alto Networks' App-ID technology fingerprints over 3,000 applications regardless of port or protocol, enabling policy enforcement based on actual application behavior rather than the port number, addressing the problem of applications that evade port-based rules by running on non-standard or dynamic ports. Cisco's NBAR (Network Based Application Recognition) offers similar capabilities within IOS platforms. Time-based ACLs allow organizations to restrict access to sensitive resources (e.g., database management ports) to defined business hours, reducing the attack window during periods of reduced monitoring. Zone-based filtering, where network segments are assigned security zones (e.g., Inside, DMZ, Outside) and inter-zone traffic is explicitly permitted or denied, provides a scalable model for managing complex enterprise segmentation policies, aligned with NIST SP 800-41 Rev. 1 Appendix A recommendations for multi-zone firewall architectures.
:::

%%%

---
unit: Placement
code: PLC
title: Where Firewalls Sit
---

:::image src="images/13_firewall_placement.png" alt="Network topology diagram showing three firewall placement scenarios: a perimeter firewall between the Internet and a DMZ, an internal segmentation firewall between corporate network zones (Finance, HR, Operations), and a host-based firewall icon on an individual laptop endpoint" caption="Firewalls can be deployed at the network perimeter, between internal segments, and directly on host endpoints, each layer addresses a different threat vector" width=full
:::

::::columns
::col::
:::list heading="Common Firewall Placements" style=plain
- **Network Perimeter**, Between internal network and untrusted external networks (e.g., Internet)
- **Internal Segmentation**, Between internal network zones (e.g., HR, Finance, DMZ)
- **Host-Based**, Running locally on individual endpoints or servers
:::
::col::
:::callout style=soft
Each placement serves a distinct security function and aligns with defense-in-depth strategies outlined in **NIST SP 800-41 Rev. 1** and **ISO/IEC 27033-3**.
:::
::::
:::notes
Firewalls are not limited to the network perimeter. In fact, modern security architectures emphasize layered defenses, where firewalls are strategically placed at multiple points within the network infrastructure to enforce policy, limit lateral movement, and contain breaches.

At the **network perimeter**, firewalls act as the first line of defense, filtering traffic between the internal network and the Internet. These are often deployed in front of a Demilitarized Zone (DMZ), which hosts public-facing services like web and email servers. Perimeter firewalls typically implement stateful packet inspection (SPI) and may integrate intrusion prevention systems (IPS) to detect and block malicious traffic. This aligns with **NIST SP 800-41 Rev. 1**, which emphasizes secure firewall configuration and placement.

**Internal segmentation firewalls** are used to enforce trust boundaries within the network. For example, a firewall may separate the finance department from the rest of the enterprise network, limiting access based on role or need-to-know. This approach is critical in mitigating the impact of lateral movement following an initial breach, as seen in incidents like **CVE-2020-1472 (Zerologon)**, where attackers moved laterally after compromising a single host.

**Host-based firewalls**, such as Windows Defender Firewall or iptables on Linux, run directly on endpoints and provide granular control over inbound and outbound traffic. They are especially important for mobile devices or laptops that may connect to untrusted networks. These firewalls enforce local policy even when the device is outside the corporate perimeter, supporting the **zero-trust** model promoted by **NIST SP 800-207**.

Together, these placements form a multi-layered defense strategy, reducing the attack surface and increasing the difficulty for adversaries to achieve their objectives.

Cloud environments introduce an additional dimension to firewall placement that follows the same principles in a software-defined model. AWS Security Groups implement host-level stateful filtering at the virtual machine level, while AWS Network ACLs provide stateless subnet-level filtering, mirroring the perimeter and host-based placement model in the cloud. Microsoft Azure Network Security Groups (NSGs) and Google Cloud VPC Firewall Rules offer analogous capabilities. The concept of microsegmentation, described in NIST SP 800-207 as a core Zero Trust principle, extends internal segmentation to individual workloads: each application or service is protected by its own firewall policy, dramatically reducing the blast radius of any single compromise. This approach is particularly effective against the lateral movement techniques cataloged in the MITRE ATT&CK framework (e.g., T1021, Remote Services), where attackers traverse flat networks after initial access.
:::

%%%

---
unit: Limits
code: LIM
title: What Firewalls Don't Stop
---

:::image src="images/13_firewall_limitations.png" alt="Diagram showing traffic that passes through a firewall checkpoint but still carries threats: encrypted HTTPS payloads hiding malware (TLS tunnel), a phishing email delivered via SMTP, an insider using authorized credentials, and a credential-stuffing login over a permitted SSH port" caption="Firewalls answer 'Is this traffic allowed?', not 'Is this traffic safe?' Allowed traffic can still carry attacks" width=full
:::

:::list heading="Core Limitations of Firewalls" style=plain
- **Social Engineering Attacks**: Phishing emails leveraging allowed protocols (e.g., SMTP, HTTPS) bypass firewall inspection because the traffic itself is legitimate.
- **Encrypted Malicious Traffic**: Use of TLS/SSL encryption masks malicious payloads within normal HTTPS traffic, preventing deep packet inspection without decryption.
- **Insider Threats**: Attackers with internal network access using authorized applications and communication channels remain undetected by traditional rule-based filtering.
- **Credential Abuse**: Stolen but valid credentials used over permitted services (e.g., SSH, RDP, API gateways) appear as legitimate user activity.
:::

::::columns
::col::
:::callout style=line
Firewalls enforce policy, not intent.
:::
::col::
:::callout style=soft
They answer *"Is this traffic allowed?"*  
Not *"Is this traffic safe?"*
:::
::::

:::notes
Firewalls are essential components of network defense-in-depth strategies, but they operate fundamentally at the perimeter level, applying access control rules based on IP addresses, ports, and protocols. As such, they are inherently limited in their ability to detect or prevent threats that exploit higher-layer semantics or abuse legitimate services.

One critical limitation lies in their inability to assess **intent** or **context**. For example, a phishing email delivered via SMTP or a malicious link accessed over HTTPS appears as standard, permitted traffic. The firewall has no visibility into the payload's malicious nature unless explicitly configured with advanced inspection capabilities like intrusion prevention systems (IPS) or application-layer filtering, which still may be circumvented through encryption.

Similarly, **encrypted traffic** poses a significant challenge. Modern malware often uses HTTPS to evade detection, leveraging legitimate domains and certificates. Without TLS decryption capabilities, which introduce privacy, performance, and legal considerations, firewalls cannot inspect the contents of these sessions. This aligns with NIST SP 800-97 guidelines on mobile device security, which emphasize the need for secure tunneling and encrypted communications that can inadvertently shield malicious behavior.

In the case of **insider threats**, whether malicious or compromised accounts, attackers already inside the network can move laterally using allowed protocols and services. Traditional firewalls lack the behavioral analytics or user-entity behavior profiling (UEBA) necessary to detect anomalies in internal traffic patterns.

Finally, **credential theft and misuse**, such as those seen in breaches involving CVE-2021-44228 (Log4Shell) or credential stuffing attacks, allow adversaries to authenticate through valid entry points. These sessions mimic normal user behavior and are indistinguishable from legitimate use when inspected solely by static rule sets.

Thus, while firewalls provide crucial boundary enforcement, they must be complemented by endpoint protection, network monitoring (e.g., SIEM), identity management, and advanced threat detection frameworks to achieve comprehensive security coverage.

Several emerging attack techniques specifically target firewall blind spots. DNS-over-HTTPS (DoH) encapsulates DNS queries within encrypted HTTPS traffic destined for port 443, completely bypassing traditional DNS-based filtering and threat intelligence lookups that rely on inspecting unencrypted DNS traffic. ICMP tunneling tools such as ptunnel encapsulate arbitrary data within ICMP echo packets that most firewalls permit for network diagnostic purposes. The 2020 SolarWinds Orion supply chain attack (CVE-2020-10148) demonstrated that even legitimate, signed software update mechanisms can deliver backdoors through permitted outbound channels, the SUNBURST malware communicated with command-and-control servers over standard HTTPS, making it indistinguishable from normal Orion telemetry traffic to any perimeter firewall. Zero Trust Network Access (ZTNA) architectures, as defined in NIST SP 800-207, directly address these limitations by eliminating implicit trust from network location and requiring continuous verification of identity and device posture for every access request, regardless of whether the user is inside or outside the perimeter.
:::

%%%

---
unit: Summary
code: SUM
title: The Gatekeeper, Not the Guarantee
---

:::image src="images/13_defense_in_depth.png" alt="Concentric ring diagram showing layered defenses: outermost ring is the firewall (perimeter), next ring is IDS/IPS (detection), inner ring is endpoint protection and SIEM (monitoring and response), with an attacker outside and protected assets at the center" caption="The firewall is the outermost gate, but defense in depth requires detection, monitoring, and response layers behind it" width=full
:::

:::pullquote
Stateful firewalls and ACLs decide what traffic is even allowed to exist on the network, but allowed traffic can still carry an attack.
:::

::::columns
::col::
:::list heading="Core Firewall Concepts" style=plain
- Traffic Filtering
- Access Control Lists (ACLs)
- Stateful vs Stateless Inspection
- Zone-Based Policies
:::
::col::
:::list heading="Limitations of Firewalls" style=plain
- Cannot inspect encrypted payloads
- Vulnerable to application-layer attacks
- Misconfigurations allow bypass (e.g., CVE-2019-11510)
- Do not prevent insider threats
:::
::col::
:::list heading="Defense in Depth Layers" style=plain
- Intrusion Detection Systems (IDS)
- Endpoint Protection
- Network Monitoring
- Secure Configuration Management
:::
::col::
:::list heading="Standards & Frameworks" style=plain
- NIST SP 800-41 (Firewall Policy)
- ISO/IEC 27033 (Network Security)
- RFC 4949 (Internet Security Glossary)
:::
::col::
::::

:::notes
Firewalls serve as critical network perimeters, enforcing access control policies by filtering traffic based on predefined rules such as IP addresses, port numbers, and protocol types. However, their role must be contextualized within a layered security architecture. A firewall acts as a gatekeeper, not a guarantee, because it operates primarily at Layers 3 and 4 of the OSI model and cannot fully inspect higher-layer content, especially when encrypted or encoded.

For example, while a stateful firewall maintains session context to track connection states and prevent certain types of spoofing attacks, it cannot detect malicious payloads embedded in otherwise legitimate protocols like HTTP or DNS. This limitation was exploited in vulnerabilities such as CVE-2019-11510, where attackers bypassed perimeter controls through misconfigured SSL VPNs.

According to NIST Special Publication 800-41 Rev. 1, firewalls should be part of a broader network security strategy that includes intrusion detection systems (IDS), secure configuration practices, and continuous monitoring. Similarly, ISO/IEC 27033 emphasizes that network security mechanisms must work in concert across multiple layers to provide comprehensive protection.

Thus, while firewalls are essential for reducing the attack surface and enforcing network segmentation, they must be augmented with complementary controls such as host-based protections, behavioral analytics, and application-aware filtering to address threats that traverse permitted channels.

The NIST Cybersecurity Framework (CSF) provides a useful lens for understanding firewalls' place in the broader security program. Firewalls map primarily to the **Protect** function, specifically PR.AC (Identity Management and Access Control) and PR.PT (Protective Technology), implementing boundary enforcement and network segmentation. However, the CSF's **Detect** function (DE.CM, Security Continuous Monitoring) requires capabilities that firewalls alone cannot provide: intrusion detection systems, SIEM platforms, and endpoint detection and response (EDR) tools fill this gap by providing visibility into traffic that firewalls have already permitted. The **Respond** and **Recover** functions require incident response playbooks, forensic logging retention (per NIST SP 800-92), and backup strategies that operate entirely independently of the firewall layer. Operationally, firewall rule bases must be treated as living documents subject to regular review and auditing. NIST SP 800-41 Rev. 1 recommends periodic firewall policy reviews to remove stale rules, tighten overly permissive entries, and validate that the rule base reflects current business requirements, a discipline reinforced by compliance frameworks including PCI DSS Requirement 1.1.7 (review firewall rules at least every six months) and ISO/IEC 27001 Annex A control A.13.1.1 (network controls). Without regular review, firewall rule bases accumulate technical debt that directly increases the organization's attack surface over time.
:::

%%%

---
unit: NGFW
code: NGF
title: Next-Generation Firewalls (NGFW)
---
:::callout style=soft
A **Next-Generation Firewall (NGFW)** is a deep-packet inspection firewall that combines traditional stateful inspection with application awareness, user identity tracking, intrusion prevention, and integration with external threat intelligence feeds. Gartner coined the term in 2009 to describe this consolidated security platform.
:::

:::code language=mermaid caption="NGFWs stack multiple inspection engines, from packet headers all the way to application identity and threat signatures, in a single policy enforcement point"
flowchart BT
  S["Stateful packet inspection"] --> A["Application identification (App-ID)"]
  A --> U["User identity mapping (User-ID)"]
  U --> T["Threat prevention: IPS, antivirus, URL filtering"]
  T --> D["TLS decryption and sandboxing"]
:::

::::columns
::col::
:::list heading="NGFW Capabilities" style=plain
- Application identification regardless of port/protocol
- User-identity-based policy (e.g., Active Directory integration)
- Integrated IPS with signature and behavioral detection
- SSL/TLS inspection and decryption
- URL filtering and web categorization
- Threat intelligence feed integration
:::
::col::
:::table
| Capability         | Traditional Firewall | NGFW              |
|--------------------|---------------------|-------------------|
| App identification | Port-based only     | Deep inspection   |
| User awareness     | None                | AD/LDAP mapping   |
| IPS                | Separate appliance  | Integrated        |
| TLS inspection     | Not supported       | Supported         |
| Threat intel       | Static ACLs         | Dynamic feeds     |
:::
::::

:::notes
Next-Generation Firewalls represent the convergence of multiple distinct security functions into a single, policy-driven enforcement platform. Traditional firewalls filtered based on Layer 3 and Layer 4 attributes, IP address, port, and protocol. The fundamental problem this created was the "port-to-application" assumption: if port 443 was allowed, all HTTPS traffic was permitted, regardless of the application running over it. NGFWs break this assumption by performing deep packet inspection at Layer 7, identifying the actual application in use and applying policy based on that identity.

Palo Alto Networks introduced the App-ID concept, which uses a combination of signatures, protocol decoding, and behavioral heuristics to identify over 3,000 applications accurately. Cisco's Firepower Threat Defense (FTD) and Check Point's Next Generation Threat Prevention (NGTP) platforms use comparable approaches. This means that even if an application tries to disguise itself on a standard port (such as a peer-to-peer application running on TCP 80), the NGFW can identify and block it.

User-identity integration connects firewall policy to Active Directory or LDAP users and groups, enabling policies such as "allow Finance group to access TCP 1433 (SQL Server) from the internal network but deny the same from all other users." This aligns with NIST SP 800-53 Control AC-3 (Access Enforcement) and the principle of least privilege. The NGFW queries the directory service in real time to map IP-to-user associations, providing granular visibility into who is doing what on the network.

SSL/TLS decryption is one of the most operationally significant, and controversial, NGFW capabilities. As of 2024, over 90% of web traffic is encrypted with TLS. Without decryption, the firewall is effectively blind to the majority of traffic it processes. NGFW TLS inspection works by acting as a man-in-the-middle: it decrypts inbound and outbound TLS sessions, inspects the plaintext, re-encrypts, and forwards. This introduces privacy, legal, and performance considerations that organizations must address in their acceptable use policies and privacy notices, particularly under GDPR and CCPA frameworks. NIST SP 800-52 Rev. 2 provides guidance on TLS implementation requirements for federal systems and offers a useful baseline for enterprise TLS inspection policy design. The CVE-2021-44228 Log4Shell vulnerability demonstrated the value of NGFW IPS signatures: within 24 hours of public disclosure, major NGFW vendors had published IPS signatures capable of detecting and blocking Log4j exploitation attempts in HTTP headers, a detection capability completely unavailable in traditional port-and-protocol firewalls.

A next-generation firewall policy that permits or blocks by application (for example Palo Alto App-ID or Cisco FTD application rules) contrasts with a traditional rule that permits all traffic to TCP port 443: the former controls which application uses the port, the latter only the port itself.
:::

%%%

---
unit: Architecture
code: DMZ
title: DMZ Architecture
---
:::callout style=soft
A **Demilitarized Zone (DMZ)** is a perimeter network segment that exposes public-facing services to the Internet while isolating them from the trusted internal network. A classic DMZ uses two firewalls, an outer firewall facing the Internet and an inner firewall protecting internal resources, with servers that must be Internet-accessible placed in the zone between them.
:::

:::code language=mermaid caption="The classic dual-firewall DMZ isolates public-facing services: outer firewall permits Internet-to-DMZ traffic; inner firewall strictly limits DMZ-to-internal access"
flowchart LR
  I["Internet"] --> F1["Firewall 1 (outer)"]
  F1 --> DMZ["DMZ<br/>web server, email server, DNS server"]
  DMZ --> F2["Firewall 2 (inner)"]
  F2 --> LAN["Internal network"]
:::

:::steps heading="Traffic Policy in a DMZ"
1. Internet clients may reach DMZ servers on specific ports (e.g., TCP 443 for the web server)
2. DMZ servers may not initiate connections into the internal network
3. Internal clients may reach DMZ servers for approved services
4. Internal clients initiate outbound Internet connections via the outer firewall
5. Direct Internet-to-internal traffic is blocked by both firewalls
:::

::::columns
::col::
:::list heading="What Goes in the DMZ" style=plain
- Public-facing web servers
- Email relay servers (MTA)
- External DNS resolvers
- VPN concentrators / remote access gateways
- Reverse proxies and load balancers
:::
::col::
:::list heading="Key Policy Rules" style=plain
- Internet → DMZ: Allowed on specific ports only
- DMZ → Internal: Denied by default (very limited exceptions)
- Internal → DMZ: Allowed for management and monitoring
- DMZ → Internet: Allowed for updates and threat intelligence
:::
::::

:::notes
The DMZ concept dates to military terminology where a demilitarized zone is a buffer region separating hostile parties. In networking, the DMZ serves the same purpose: it is a controlled buffer between the hostile Internet and the trusted internal network where public-facing services can live without being directly connected to internal resources containing sensitive data.

The dual-firewall DMZ architecture is the most security-conscious design. The outer firewall (sometimes called the access firewall or screening router) accepts inbound Internet connections on specific permitted ports, typically TCP 80 (HTTP) and TCP 443 (HTTPS) for a web server, or TCP 25 (SMTP) for a mail relay, and forwards them to the appropriate DMZ server. The inner firewall (sometimes called the choke firewall) enforces a strict deny-by-default policy against any traffic originating from the DMZ toward the internal network. This is critical: if a DMZ server is compromised, the inner firewall prevents the attacker from using it as a pivot point to reach internal databases, domain controllers, or workstations.

A single-firewall DMZ using three interfaces (Internet, DMZ, Internal) on one device is simpler and cheaper but provides weaker security, if the single firewall is compromised, both the DMZ and internal network are exposed simultaneously. NIST SP 800-41 Rev. 1 Section 4.2 specifically discusses multi-tier firewall architectures and recommends the dual-firewall model for environments requiring strong separation between public services and internal resources.

The Target 2013 breach is the canonical example of why DMZ policy must be strictly enforced between vendor-accessible systems and internal cardholder data environments. The HVAC vendor's access should have been confined to a DMZ-equivalent management segment with zero inbound access from that segment to the POS network, a control that was either absent or misconfigured. PCI DSS Requirement 1.3 directly mandates that firewalls prohibit direct inbound or outbound traffic between the Internet and the cardholder data environment, requiring all such traffic to pass through the DMZ. The 2007 TJX Companies breach, the largest retail breach of its era, compromising 94 million credit card records, similarly involved inadequate segmentation between wireless access points in the parking lot and the internal network, with no DMZ enforcement blocking lateral pivot.

In a dual-firewall DMZ, an attacker who exploits a SQL injection flaw in the web server is still blocked from the database by the inner firewall; without that inner firewall the same compromise reaches the database directly. The inner boundary is what contains the breach.
:::

%%%

---
unit: Architecture
code: ZBF
title: Zone-Based Firewall Policies
---
:::callout style=soft
**Zone-Based Firewalling** organizes network interfaces into named security zones and defines inter-zone traffic policies rather than per-interface rule sets. Traffic within the same zone is permitted by default; traffic between zones requires an explicit policy. This model scales more cleanly than interface-centric ACLs in complex multi-segment networks.
:::

:::code language=mermaid caption="Zone-based policies define inter-zone relationships rather than per-interface rules, easier to reason about and audit in large segmented networks"
flowchart LR
  O["Outside (Internet)"] -->|"allow 443"| D["DMZ"]
  O -.-x|"deny"| IN["Inside (Corporate)"]
  IN -->|"allow"| O
  IN -->|"allow"| D
  D -.-x|"deny"| IN
  M["Management"] -->|"allow SSH"| D
  M -->|"allow SSH"| IN
  O -.-x|"deny"| M
:::

:::table
| Source Zone  | Destination Zone | Default Policy | Example Exception |
|--------------|------------------|----------------|-------------------|
| Outside      | DMZ              | Deny           | Permit TCP 443 to web server |
| Outside      | Inside           | Deny           | None, always blocked |
| DMZ          | Inside           | Deny           | Permit TCP 1433 from app server to DB (controlled) |
| Inside       | Outside          | Permit         | Block known-bad categories via URL filter |
| Inside       | DMZ              | Permit         | Management and monitoring traffic |
| Management   | All Zones        | Permit (limited) | SSH, SNMP, syslog only |
:::

:::list heading="Zone-Based Model Advantages" style=plain
- Scales to large networks without per-interface rule sprawl
- Logical grouping mirrors business function (Finance zone, Guest zone, PCI zone)
- Default-deny between zones enforces least privilege at the architecture level
- Simplifies auditing, policy intent is readable from zone-pair definitions
:::

:::notes
Traditional interface-based ACL management becomes unwieldy as networks grow. A router with eight interfaces, each with inbound and outbound ACLs, requires managing sixteen ACL rule sets, and the relationship between them is not immediately obvious from the rule text. Zone-based firewalling, standardized in Cisco IOS Zone-Based Policy Firewall (ZBF) since IOS 12.4(6)T and supported natively in Cisco ASA, Palo Alto PAN-OS, and Fortinet FortiOS, addresses this by abstracting interfaces into zones and defining policy between zone pairs.

The fundamental rule of zone-based firewalling is: traffic between interfaces in the same zone flows freely by default; traffic crossing a zone boundary is denied by default unless an explicit zone-pair policy permits it. This implements deny-by-default at the architectural level, the most secure posture per NIST SP 800-53 Control SC-7 (Boundary Protection), which requires organizations to implement subnetworks for publicly accessible system components and deny all other traffic as the default.

Zone design should reflect the organization's security domains. A typical enterprise zone model includes: Outside (the Internet, untrusted), DMZ (public-facing services), Inside (corporate internal network), Guest (visitor and IoT devices), Management (network device management plane), and PCI (payment card environment, if applicable). Each zone carries an implicit trust level, and zone-pair policies explicitly define what can flow between trust levels.

Cisco's implementation uses class-maps to identify traffic and policy-maps to define actions (inspect, pass, drop), which are then applied to zone-pairs with the zone-pair security command. The "inspect" action creates stateful sessions, while "pass" is stateless, an important distinction when designing policies for bidirectional traffic. FortiOS implements the same concept through firewall policies applied between source and destination interface groups (zones).

The practical auditing benefit is significant. When a compliance auditor asks "what traffic can reach your payment card database?", an administrator with zone-based policy can immediately show the PCI-to-Inside zone-pair policy containing a single rule permitting TCP 1433 from the specific application server, versus searching through dozens of per-interface ACLs trying to reconstruct the same picture. PCI DSS Requirement 1.2.1 mandates restricting inbound and outbound traffic to only that necessary for the cardholder data environment, and zone-based architectures make demonstrating this compliance substantially easier.

:::

%%%

---
unit: Technology
code: DPI
title: Deep Packet Inspection (DPI)
---
:::callout style=soft
**Deep Packet Inspection (DPI)** examines the data portion (payload) of a network packet in real time, going beyond Layer 3 and Layer 4 header analysis to inspect application content, detect signatures, and enforce policy at Layer 7. DPI enables firewalls to identify and control specific applications, detect embedded threats, and enforce content policies that port-based filtering cannot achieve.
:::

:::code language=mermaid caption="DPI lifts the lid on the packet payload, where threats hide inside otherwise legitimate protocols"
flowchart TB
  subgraph SH["Shallow inspection"]
    direction LR
    h1["IP header: checked"] --- h2["TCP header: checked"] --- h3["Payload: not read"]
  end
  subgraph DPI["Deep packet inspection"]
    direction LR
    d1["IP header: checked"] --- d2["TCP header: checked"] --- d3["Payload: read, malware signature found"]
  end
  SH ~~~ DPI
:::

:::flow
1. Packet arrives and headers are parsed (Layer 3/4, standard inspection)
2. Application protocol decoder reassembles the session stream
3. Payload content matched against signature database (CVE signatures, malware hashes, application fingerprints)
4. Behavioral heuristics applied to detect novel or obfuscated threats
5. Policy action applied: Allow, Block, Alert, or Reset session
:::

::::columns
::col::
:::list heading="DPI Use Cases" style=plain
- Malware detection in HTTP/SMTP/FTP payloads
- Application identification (e.g., BitTorrent on port 80)
- Data Loss Prevention (DLP), detect PII in outbound traffic
- Intrusion detection signature matching
- SSL/TLS decryption for encrypted payload inspection
:::
::col::
:::list heading="DPI Limitations" style=plain
- High computational cost at line rate
- Ineffective without TLS decryption for encrypted traffic
- Privacy and legal concerns for employee monitoring
- Requires frequent signature updates to detect new threats
- Sophisticated attackers can fragment or encode payloads to evade
:::
::::

:::notes
Deep Packet Inspection represents the evolution of firewall technology from a protocol-centric control to a content-aware one. Where traditional firewalls ask "what port is this traffic on?", DPI asks "what is this traffic actually doing?" This distinction is critical because the modern Internet has largely moved to a small number of ports, primarily TCP 443 (HTTPS) and TCP 80 (HTTP), that carry an enormous diversity of application types, only some of which may be appropriate for a given network environment.

DPI operates by reassembling the stream of packets belonging to a session and analyzing the reconstructed application-layer data against a set of detection mechanisms. These include protocol-specific decoders (which understand the structure of HTTP, SMTP, DNS, FTP, and hundreds of other protocols), signature databases (which match byte patterns associated with known malware, exploits, or specific applications), and heuristic engines (which flag behavioral anomalies that match no specific signature but indicate potentially malicious activity).

In practice, DPI is the engine behind several critical security functions. Intrusion Prevention Systems (IPS) use DPI to match network traffic against CVE-based exploit signatures, for example, the signature detecting CVE-2014-6271 (Shellshock) looks for bash function definition patterns in HTTP CGI environment variables, something only discoverable by inspecting the HTTP payload. Data Loss Prevention (DLP) uses DPI to scan outbound traffic for patterns matching credit card numbers, Social Security numbers, or classified document identifiers, enabling organizations to block unauthorized exfiltration. Application visibility and control platforms use DPI to identify over 3,000 distinct application signatures, enabling granular policy decisions.

The computational cost of DPI is substantial. Processing packet payloads at multi-gigabit line rates requires specialized hardware acceleration, Application-Specific Integrated Circuits (ASICs) or Field-Programmable Gate Arrays (FPGAs) in dedicated DPI appliances. This is why enterprise-class NGFW hardware is significantly more expensive than commodity routing hardware performing stateless ACL enforcement. NIST SP 800-94 provides guidance on intrusion detection and prevention systems, including DPI-based implementations, recommending that organizations carefully evaluate performance requirements when selecting and deploying DPI capabilities.

The privacy dimension of DPI is legally significant. In the United States, the Electronic Communications Privacy Act (ECPA) and the Wiretap Act impose restrictions on intercepting wire communications, with employer network monitoring typically covered by consent provisions in acceptable use policies. In the European Union, GDPR Article 5's data minimization principle and Article 13's transparency requirements create additional compliance obligations for organizations deploying DPI to inspect employee communications. Legal review of DPI deployment scope, particularly SSL/TLS decryption of personal communications, should be a prerequisite before deployment in any organization operating under EU jurisdiction.

Deep packet inspection reads the payload, so over plain HTTP it sees the full request including headers, while over HTTPS the payload is opaque. This is why TLS inspection is required for DPI to work on encrypted traffic, and why that inspection raises its own privacy and trust questions.
:::

%%%

---
unit: Checkpoint
code: CHK1
title: Mid-Lecture Checkpoint
---
:::callout style=soft
Pause and check your understanding before we move into more advanced topics. These questions map directly to concepts covered so far in this lecture.
:::

:::list heading="Review Questions" style=plain
- 1. What is the key difference between a stateless and a stateful firewall? Give a specific attack that one stops and the other misses.
- 2. An ACL has these rules in order: (1) Permit TCP any 192.168.1.0/24 eq 443, (2) Deny TCP 10.0.0.5 any eq 443, (3) Deny any any. Will traffic from 10.0.0.5 to 192.168.1.10 port 443 be permitted or denied? Why?
- 3. Name two types of attacks that a correctly configured perimeter firewall cannot stop, and explain why each bypasses the firewall.
- 4. In a DMZ architecture, why is the inner firewall the more important of the two? What does it protect against?
- 5. What is the implicit deny rule, and why is it essential to ACL security?
:::

::::columns
::col::
:::callout style=line
**Expected answers:** Review slides FWL, SLF, STF, ACL, and DMZ.
:::
::col::
:::callout style=soft
**Instructor:** Cold-call 2–3 students on questions 2 and 3. Question 2 tests ACL first-match understanding; question 3 tests critical thinking beyond the slides.
:::
::::

:::notes
This checkpoint is designed as a five-minute interactive break at the mid-point of the lecture, approximately after the DMZ slide. It serves two purposes: reinforcing recall of the first half's material and activating thinking before the more complex topics that follow (NGFW, DPI, NAT, host-based firewalls).

Walking through the answers in order: Question 1, the state table. A stateless firewall allows a TCP RST packet forged with the correct source/destination IP and port (CVE-2004-0230) because it has no idea whether a valid TCP session was established; a stateful firewall validates the RST against its state table and drops forged RSTs not matching an established session. Question 2 is a deliberate trap. Rule 1 permits TCP from any source to 192.168.1.0/24 port 443. Traffic from 10.0.0.5 to 192.168.1.10:443 matches Rule 1 first, the action is permit, and evaluation stops. Rule 2 (deny 10.0.0.5) is never reached. The traffic is permitted, which is the wrong answer most students give without carefully working through first-match logic. This is exactly the kind of ACL misconfiguration that creates real-world vulnerabilities, NIST SP 800-41 Rev. 1 warns explicitly about the importance of rule ordering, and Cisco's own ACL documentation notes that more specific rules must precede more general ones to function as intended. If you wanted to deny 10.0.0.5 access to 192.168.1.0/24 port 443, Rule 2 would need to appear before Rule 1.

Question 3 should generate discussion. Good answers include: phishing delivered over SMTP (the SMTP connection itself is legitimate, the firewall has no visibility into the email content unless it runs DPI with SMTP inspection); credential stuffing over HTTPS (valid credentials used against a permitted service look identical to legitimate login traffic); ICMP tunneling (ICMP echo is typically permitted for diagnostic purposes); and supply chain attacks like SolarWinds (traffic originates from a trusted internal host using a legitimate software update channel). The key conceptual point is that firewalls enforce policy, not intent, they can only act on what they can observe in packet headers and, with DPI, payload content.

Question 4 reinforces the DMZ concept: the outer firewall's compromise means the attacker gains control of a host with Internet connectivity, but the inner firewall's strict deny-by-default policy prevents that compromised host from reaching internal databases or domain controllers. The inner firewall is the last line of defense preventing a DMZ compromise from becoming a full internal breach.

ACL rule ordering is a common error: because rules are evaluated top to bottom and the first match wins, a broad early rule can shadow a specific later one, so a permit placed above a deny silently overrides it.
:::

%%%

---
unit: Technology
code: NAT
title: Network Address Translation (NAT) and Firewalls
---
:::callout style=soft
**Network Address Translation (NAT)** modifies the source and/or destination IP addresses of packets as they pass through a router or firewall, mapping private internal addresses to public routable addresses. NAT is often deployed on the same device as the perimeter firewall, providing an incidental layer of obscurity for internal network topology while enabling internet access from non-routable RFC 1918 address space.
:::

:::code language=mermaid caption="NAT rewrites packet addresses at the perimeter, internal IPs never appear on the Internet, and unsolicited inbound packets have no NAT entry to match"
flowchart LR
  P["Inside host<br/>192.168.1.50:51000"] -->|"outbound"| F["NAT firewall"]
  F -->|"source rewritten"| I["Internet<br/>seen as 203.0.113.10:62001"]
  I -->|"reply to 203.0.113.10:62001"| F
  F -->|"translated back"| P
  T["NAT table<br/>192.168.1.50:51000 ⇄ 203.0.113.10:62001"] -.- F
:::

::::columns
::col::
:::list heading="NAT Types" style=plain
- **Static NAT**: One private IP maps permanently to one public IP (used for servers)
- **Dynamic NAT**: Pool of public IPs assigned dynamically to internal hosts
- **PAT (Port Address Translation)**: Many internal IPs share one public IP using unique port numbers, also called NAT overload or masquerading
:::
::col::
:::table
| Property            | NAT Behavior                                   |
|---------------------|------------------------------------------------|
| RFC 1918 addresses  | 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16     |
| Inbound unsolicited | Dropped, no NAT entry exists                  |
| Outbound sessions   | Tracked in NAT table; return traffic permitted  |
| Port reuse (PAT)    | Up to ~65,000 sessions per public IP           |
:::
::::

:::notes
NAT was originally developed to address IPv4 address exhaustion, defined in RFC 1631 (1994) and later standardized in RFC 3022, by allowing thousands of internal hosts sharing RFC 1918 private addresses to share one or a small pool of public IP addresses. In most small and medium enterprise environments, the perimeter firewall performs PAT (Port Address Translation), translating all outbound sessions so they appear to originate from the single public IP assigned by the ISP.

The security relationship between NAT and firewalling is frequently misunderstood. NAT provides an incidental security benefit: because inbound unsolicited packets have no corresponding NAT translation table entry, the firewall drops them, there is no internal IP address to forward them to. This effectively prevents direct inbound connection attempts to internal hosts from the Internet. However, this is a side effect of address translation, not a security control. NAT is not a firewall. An attacker who compromises an internal host that has an active outbound NAT session can use that session to receive inbound data (the attacker controls the server the session was initiated to). Malware routinely exploits this by using reverse shells that initiate outbound connections from the victim to the attacker's server, creating a NAT-traversing command-and-control channel.

Static NAT is used for servers that must accept inbound connections, a web server in the DMZ, for example, gets a static NAT mapping from a public IP to its DMZ private IP on TCP 443. The firewall's ACL then explicitly permits inbound TCP 443 traffic to that public IP. Without the explicit ACL permit, the NAT mapping alone would not allow the connection, NAT and firewall rules work together. This is a common configuration error: administrators sometimes configure a static NAT entry but forget to create the corresponding firewall permit rule, or vice versa.

IPv6 eliminates the technical need for NAT since every device can have a globally unique address. However, NAT remains ubiquitous in IPv4 networks and is likely to persist for decades alongside IPv6. NIST SP 800-119 addresses IPv6 security considerations, including the implications of eliminating NAT, organizations transitioning to IPv6 must rely on explicit firewall rules to provide the equivalent protection that NAT incidentally provided in IPv4 environments.

NAT is an operational mechanism, not a security control. Malware that opens an outbound connection from inside the network, a reverse shell, traverses NAT normally, because NAT permits outbound flows and maps the return traffic back. NAT therefore offers no protection against active malware already running on an internal host.
:::

%%%

---
unit: Technology
code: HBF
title: Host-Based Firewalls
---
:::callout style=soft
A **host-based firewall** is a software firewall that runs directly on a specific endpoint, workstation, server, or virtual machine, and controls inbound and outbound traffic for that host independently of network-level controls. Host-based firewalls enforce policy at the last mile, protecting the host even when network firewalls are bypassed, misconfigured, or absent.
:::

:::code language=mermaid caption="Host-based firewalls protect the endpoint regardless of what network it is connected to, critical for mobile devices on untrusted networks"
flowchart LR
  A["Attacker on the same<br/>public Wi-Fi"] -.-x|"inbound connection blocked"| H["Laptop with host-based firewall"]
  W["Public Wi-Fi: no perimeter firewall"] --- H
  H -->|"outbound traffic allowed"| I["Internet"]
:::

::::columns
::col::
:::list heading="Common Host-Based Firewalls" style=plain
- **Windows Defender Firewall** (built into Windows 10/11/Server)
- **iptables / nftables** (Linux kernel Netfilter framework)
- **pf (Packet Filter)** (macOS and BSD systems)
- **ufw (Uncomplicated Firewall)** (Ubuntu Linux front-end for iptables)
- **CrowdStrike Falcon / SentinelOne** (EDR platforms with integrated host firewall)
:::
::col::
:::list heading="Key Capabilities" style=plain
- Per-application inbound and outbound rules
- Network profile awareness (Domain, Private, Public)
- Block unsolicited inbound connections on untrusted networks
- Log all blocked and allowed connections for forensic review
- Enforce policy even when network perimeter controls are absent
:::
::::

:::notes
Host-based firewalls address a critical gap in perimeter-only security architectures: the perimeter assumes everything inside is trusted, but modern work patterns routinely place endpoints outside the perimeter, on coffee shop Wi-Fi, hotel networks, home broadband, or cloud providers, where no corporate perimeter firewall exists. A host-based firewall provides the same boundary enforcement function at the endpoint level.

Windows Defender Firewall (formerly Windows Firewall, introduced in Windows XP SP2 following the Blaster worm outbreak of 2003 that exploited the unprotected RPC service on TCP 135) supports three network profiles: Domain (used when connected to corporate Active Directory network), Private (home or trusted network), and Public (untrusted network). Policies can be more restrictive in the Public profile, blocking all unsolicited inbound connections while allowing only explicitly approved applications to receive traffic. Group Policy Objects (GPOs) allow enterprise administrators to centrally deploy and enforce host-based firewall policy across all domain-joined Windows endpoints, aligning with NIST SP 800-41 Rev. 1 recommendations for host-based firewall management.

On Linux, the Netfilter framework in the kernel provides the underlying packet filtering capability, controlled via iptables (legacy) or nftables (current). The iptables INPUT chain controls inbound traffic, OUTPUT controls outbound, and FORWARD controls traffic being routed through the host. A minimal secure baseline would accept established/related return traffic, accept loopback, accept SSH from specific management CIDRs, and drop everything else. The CIS Benchmarks for each Linux distribution provide specific iptables and nftables configuration recommendations that organizations should implement as a baseline configuration standard.

The Blaster worm (CVE-2003-0026) and Sasser worm (CVE-2004-0210) both propagated via Windows services listening on network ports with no host-based firewall blocking access. The subsequent addition of Windows Firewall in XP SP2 dramatically reduced the attack surface for similar attacks. This historical context underscores why CIS Control 4 (Secure Configuration of Enterprise Assets) specifically includes host-based firewall enablement as a required configuration for all endpoint operating systems. NIST SP 800-123 (Guide to General Server Security) similarly mandates enabling host-based firewalls on all servers and configuring them to permit only necessary inbound services.

The host firewall built into a desktop operating system, such as Windows Defender Firewall, enforces inbound and outbound rules at the endpoint, a layer independent of the network firewall.
:::

%%%

---
unit: Technology
code: WAF
title: Web Application Firewalls (WAF)
---
:::callout style=soft
A **Web Application Firewall (WAF)** operates at Layer 7 (the application layer) and specifically analyzes HTTP and HTTPS traffic to detect and block web application attacks, including SQL injection, cross-site scripting (XSS), and OWASP Top 10 vulnerabilities. Unlike network firewalls that operate at Layer 3/4, WAFs understand the semantics of HTTP requests and responses.
:::

:::code language=mermaid caption="A WAF sits in the HTTP request path, inspecting application-layer content that network firewalls cannot see"
flowchart LR
  I["Internet clients"] --> W["Web application firewall"]
  W -.-x|"blocked: request matches an SQL injection rule"| X["Malicious POST"]
  W -->|"clean requests only"| A["Web application server"]
:::

:::table
| Attack Type         | Network Firewall | NGFW with DPI | WAF         |
|---------------------|------------------|----------------|-------------|
| SQL Injection       | Cannot detect    | Partially      | Yes         |
| XSS                 | Cannot detect    | Partially      | Yes         |
| CSRF                | Cannot detect    | No             | Yes         |
| DDoS (volumetric)   | Rate limiting    | Limited        | Rate limiting/challenge |
| Port scanning       | Yes              | Yes            | N/A         |
| Malformed HTTP      | No               | Partially      | Yes         |
| Bot traffic         | No               | Limited        | Yes (CAPTCHA/fingerprinting) |
:::

:::list heading="WAF Deployment Modes" style=plain
- **Reverse Proxy**, WAF sits in front of the web server and terminates all HTTP connections (most common)
- **Transparent Bridge**, WAF inline without changing IP routing (less common)
- **Out-of-Band / Monitor Mode**, WAF receives a copy of traffic for detection only, no blocking capability
- **Cloud WAF / CDN-integrated**, Cloudflare, AWS WAF, Akamai, traffic routed through cloud WAF before reaching the origin server
:::

:::notes
The OWASP Top 10, the definitive list of the most critical web application security risks, updated in 2021, defines the threat categories that WAFs are primarily designed to address: injection (A03), broken authentication (A07), security misconfiguration (A05), and others. Network firewalls permitting inbound TCP 443 traffic to a web server are entirely blind to what is in the HTTP payload of that permitted traffic. A SQL injection attack arrives in the URL query string or POST body of an otherwise legitimate HTTPS connection, the network firewall sees a valid TLS session on permitted port 443 and forwards it without inspection. The WAF, which terminates the TLS session and inspects the HTTP content, can detect the "' OR '1'='1" injection pattern and block the request before it reaches the application.

WAF rule sets include both signature-based detection (matching known attack patterns like those in the OWASP ModSecurity Core Rule Set, which contains over 900 rules covering the OWASP Top 10) and anomaly-based detection (scoring requests based on multiple suspicious indicators and blocking those exceeding a threshold). Commercial WAFs from vendors such as Imperva, F5 (formerly Shape Security), and Cloudflare supplement these with machine learning models trained on large volumes of attack traffic.

CVE-2017-5638 (Apache Struts remote code execution via Content-Type header manipulation) caused the Equifax breach of 2017, exposing 147 million Americans' personal data. Equifax had a WAF in place but had failed to update its SSL certificate for the WAF's inspection capability, leaving it unable to inspect the encrypted traffic through which the attack arrived for approximately two months before the breach. This case study directly illustrates both the value of WAFs, a properly functioning WAF with updated signatures would have blocked the exploitation attempt, and the operational discipline required to maintain them.

AWS WAF integrates with CloudFront, Application Load Balancer, and API Gateway, providing rule-based filtering at the cloud edge for organizations hosting applications on AWS infrastructure. AWS WAF Managed Rules from AWS and third-party vendors (CrowdStrike, Imperva) provide continuously updated rule groups aligned with OWASP Top 10 categories. NIST SP 800-44 (Guidelines on Securing Public Web Servers) recommends WAF deployment as a mitigating control for web application vulnerabilities, particularly for applications that cannot be immediately patched against known vulnerabilities, the WAF acts as a virtual patch while the software fix is developed and deployed.

PCI DSS Requirement 6.6 requires organizations to either review public-facing web applications for security or place a web application firewall in front of them, making a WAF a compliance requirement, not only a best practice, for any organization processing card payments online.
:::

%%%

---
unit: Comparison
code: IDS
title: Firewall vs IDS vs IPS
---
:::callout style=soft
Firewalls, Intrusion Detection Systems (IDS), and Intrusion Prevention Systems (IPS) are complementary but distinct controls. Firewalls enforce access policy at the boundary; IDS passively monitors for suspicious activity and alerts; IPS actively inspects inline and blocks detected threats. Understanding which control does what prevents dangerous gaps from misplaced assumptions.
:::

:::code language=mermaid caption="Firewalls block by policy; IDS alerts passively; IPS blocks actively based on detected malicious behavior, each fills a distinct role"
flowchart TB
  subgraph FW["Firewall: inline, blocks by rule"]
    direction LR
    I1["Internet"] --> F["Firewall"] --> N1["Internal network"]
  end
  subgraph IDS["IDS: copy of traffic, alerts only"]
    direction LR
    I2["Internet"] --> N2["Internal network"]
    I2 -.->|"network tap"| D["IDS sends alerts"]
  end
  subgraph IPS["IPS: inline, blocks attacks it detects"]
    direction LR
    I3["Internet"] --> P["IPS"] --> N3["Internal network"]
  end
  FW ~~~ IDS ~~~ IPS
:::

:::table
| Characteristic         | Firewall                        | IDS                              | IPS                               |
|------------------------|---------------------------------|----------------------------------|-----------------------------------|
| Deployment position    | Inline (blocking)               | Out-of-band (monitoring)         | Inline (blocking)                 |
| Primary function       | Access control by policy        | Detect and alert on anomalies    | Detect and block threats inline   |
| Action on threat       | Block per rule (policy-driven)  | Alert only, no blocking         | Block automatically               |
| False positive risk    | Low (rules are explicit)        | Medium–High                      | High (can block legitimate traffic) |
| Traffic visibility     | Header-level (with DPI: payload)| Full session content             | Full session content              |
| State awareness        | Stateful                        | Stateful (session reassembly)    | Stateful                          |
| NIST reference         | SP 800-41                       | SP 800-94                        | SP 800-94                         |
:::

:::list heading="When Each Control Applies" style=plain
- **Firewall**: Enforce boundary access policy, what traffic is permitted at all
- **IDS**: Audit and forensics, detect attacks on traffic already permitted by the firewall
- **IPS**: Supplement firewall with behavioral detection, block attacks that arrive on permitted ports/protocols
:::

:::notes
A common architectural mistake is assuming that one of these controls replaces the others. They are explicitly complementary, addressing different security questions at different points in the traffic flow.

The firewall answers: "Is this type of traffic allowed by policy?" It enforces predetermined rules, permit TCP 443 from anywhere to the web server, deny everything else. It has no visibility into whether permitted traffic is benign or malicious; that is not its function. Its decision is policy-driven, deterministic, and fast.

The IDS answers: "Does this traffic look like an attack?" It operates out-of-band, receiving a copy of traffic via a network tap or SPAN port, analyzing it against signatures and behavioral models, and generating alerts. Because it is out-of-band, it cannot block traffic, it can only alert. This means an attack that triggers an IDS alert has already reached its destination network; the organization must respond after the fact. The benefit is zero impact on traffic flow, a misconfigured IDS cannot cause outages. NIST SP 800-94 (Guide to Intrusion Detection and Prevention Systems) differentiates IDS and IPS implementations and discusses deployment considerations for each.

The IPS answers the same question as the IDS but is deployed inline, traffic passes through it before reaching its destination. When the IPS detects a threat, it drops the packet and resets the session. The tradeoff is that false positives (legitimate traffic incorrectly flagged as malicious) result in blocking real users. High-confidence signatures (known exploit patterns for specific CVEs) are appropriate for aggressive IPS blocking mode; behavioral detections with higher false positive rates should be deployed in alert-only mode initially until tuned. CVE-2021-44228 (Log4Shell) produced high-confidence IPS signatures within hours of disclosure, organizations with deployed IPS systems were able to block exploitation attempts immediately while patching was underway.

NGFWs have largely consolidated the IPS function into the firewall platform, the Palo Alto Threat Prevention subscription, Cisco Firepower's Snort-based IPS engine, and Fortinet FortiGate's IPS module all deliver inline IPS capability from the same policy console as the firewall rules. This convergence simplifies management but requires careful policy design to avoid the false positive problem causing the firewall to block legitimate traffic.

The MITRE ATT&CK framework provides a useful mapping: firewalls primarily address Initial Access tactics (TA0001) by blocking inbound attack vectors; IDS/IPS address broader detection across the kill chain, including lateral movement (TA0008) and command-and-control (TA0011). Organizations should map their IDS/IPS signature coverage against ATT&CK techniques relevant to their threat model to identify detection gaps.

The difference between an IDS and an IPS is positional: an IDS sits out of band and sees a packet only after it has already arrived at its target, while an IPS sits inline and can stop the packet before it arrives. Position in the topology determines the security outcome.
:::

%%%

---
unit: Operations
code: LOG
title: Firewall Logging and Monitoring
---
:::callout style=soft
A firewall that does not log is a security control that cannot be audited, investigated, or improved. Firewall logs provide the evidentiary record of what traffic was permitted and denied, forming the foundation for incident detection, forensic investigation, and compliance reporting. Without structured logging and active monitoring, attackers can operate undetected on permitted channels for extended periods.
:::

:::code language=mermaid caption="Firewall logs feed the SIEM, raw permit/deny events become meaningful threat intelligence only when correlated and monitored"
flowchart LR
  F["Firewall logs"] --> S["SIEM"]
  E["Endpoint logs"] --> S
  A["Authentication logs"] --> S
  S --> AL["Correlated alerts"]
  S --> DB["Dashboards"]
  S --> CR["Compliance reports"]
:::

:::list heading="Essential Firewall Log Fields" style=plain
- **Timestamp**, When the event occurred (synchronized via NTP)
- **Source IP and port**, Originating endpoint and application
- **Destination IP and port**, Target endpoint and service
- **Protocol**, TCP, UDP, ICMP, etc.
- **Action**, Permit or Deny
- **Rule matched**, Which ACL rule was triggered
- **Interface / zone**, Which network segment was involved
- **Byte and packet counts**, Session volume (useful for detecting data exfiltration)
:::

::::columns
::col::
:::callout style=line
Denied traffic is just as valuable as permitted traffic, repeated denies from the same source indicate reconnaissance.
:::
::col::
:::list heading="SIEM Correlation Use Cases" style=plain
- Detect port scans (high deny rate from single source)
- Identify beaconing (periodic outbound connections at regular intervals)
- Alert on connections to known-malicious IPs
- Baseline traffic patterns to detect anomalies
:::
::::

:::notes
Firewall logs are among the most valuable data sources in a security operations center (SOC). They provide a complete record of network-level access attempts, both successful (permitted) and unsuccessful (denied). This distinction is important: many organizations configure logging only for denied traffic, missing the visibility into what is successfully traversing their network. Comprehensive logging of both permitted and denied events is the correct approach, though it requires more storage and processing capacity.

NIST SP 800-92 (Guide to Computer Security Log Management) provides foundational guidance on log management, including retention periods (typically 90 days online, one year archived for compliance), log integrity protection, and centralized log aggregation. PCI DSS Requirement 10.5 mandates that audit logs be protected from modification and retained for at least one year, with three months immediately available for analysis, directly applicable to firewall logs in payment card environments.

The syslog protocol (RFC 5424) is the near-universal standard for transmitting firewall log events to centralized SIEM platforms such as Splunk, IBM QRadar, Microsoft Sentinel, and open-source alternatives like the Elastic Stack (ELK). Structured log formats, CEF (Common Event Format) from ArcSight, LEEF (Log Event Extended Format) from QRadar, or the emerging OCSF (Open Cybersecurity Schema Framework) standard, improve interoperability between firewall platforms and SIEM ingestion.

Active monitoring of firewall logs enables several critical detection capabilities. Port scan detection: an attacker probing the network will generate a high rate of denied connection attempts across multiple destination ports from the same source IP, a pattern easily detected by thresholding deny events per source. Command-and-control beaconing detection: malware that checks in with a C2 server on a regular interval generates periodic outbound connections at fixed or jittered intervals, creating a temporal pattern detectable through statistical analysis of firewall permit logs. The 2020 SolarWinds SUNBURST backdoor, for example, beaconed to avsvmcloud[.]com, organizations with DNS logging and firewall log correlation could have detected this unusual domain contact if monitoring was in place.

The Zeek (formerly Bro) network security monitoring platform augments traditional firewall logging by generating rich connection logs from network traffic, including protocol analysis, file extraction metadata, and behavioral profiling, without requiring integration with the firewall platform itself. It is widely used in enterprise and government SOCs to provide the application-layer visibility that firewall ACL logs alone cannot deliver.

A SIEM query that ranks the top sources of denied firewall traffic surfaces reconnaissance activity directly, because scanning hosts generate large numbers of blocked connection attempts.
:::

%%%

---
unit: Framework
code: PCI
title: PCI DSS Firewall Requirements
---
:::callout style=soft
The **Payment Card Industry Data Security Standard (PCI DSS)** version 4.0 contains mandatory firewall requirements for any organization that stores, processes, or transmits cardholder data. Requirement 1 ("Install and Maintain Network Security Controls") is the most prescriptive firewall framework in any major compliance standard and provides a practical operational checklist.
:::

:::code language=mermaid caption="PCI DSS Requirement 1 prescribes specific firewall architecture and configuration controls around the cardholder data environment"
flowchart LR
  I["Internet"] --> P["Perimeter firewall<br/>stateful inspection"]
  P --> D["DMZ<br/>payment application"]
  D --> F["Inner firewall"]
  F --> CDE["Cardholder data environment"]
  R["PCI DSS Requirement 1: network security controls,<br/>restrict traffic into and out of the CDE,<br/>review rules every six months"] -.- F
:::

:::table
| PCI DSS Req. | Requirement Description                                                              |
|--------------|--------------------------------------------------------------------------------------|
| 1.2.1        | Restrict inbound and outbound traffic to that which is necessary for the CDE         |
| 1.2.2        | Secure and synchronize all network security control configuration files              |
| 1.3.1        | Restrict inbound traffic to the CDE to only that which is necessary                 |
| 1.3.2        | Restrict outbound traffic from the CDE to only that which is necessary               |
| 1.3.3        | Implement anti-spoofing measures to detect and block forged source IP addresses      |
| 1.4.1        | Network security controls between trusted and untrusted networks                    |
| 1.5.1        | Security controls for computing devices that connect to both untrusted and CDE networks |
:::

:::list heading="Key Operational Requirements" style=plain
- Formal documented firewall change management process
- Firewall rule review at minimum every six months (Req. 1.2.7)
- No direct connections between the Internet and the CDE (Req. 1.3.3)
- Personal firewall software on all mobile/employee-owned devices (Req. 1.5.1)
:::

:::notes
PCI DSS is the most operationally detailed compliance framework for firewall configuration in the payment industry. Published by the PCI Security Standards Council (a consortium of Visa, Mastercard, American Express, Discover, and JCB), PCI DSS version 4.0 (released March 2022, mandatory compliance from March 2025) restructured Requirement 1 to focus on network security controls broadly rather than specifically on firewalls, acknowledging that software-defined networking, cloud environments, and microsegmentation have expanded the implementation options beyond traditional hardware firewalls.

The cardholder data environment (CDE) is the regulatory target: all systems that store, process, or transmit primary account numbers (PANs, the 16-digit card number), sensitive authentication data (CVV, PIN), or that are on the same network segment as systems that do. The firewall requirements are designed to isolate the CDE from all other networks and the Internet, limiting the exposure of cardholder data to the smallest possible segment of the network.

Requirement 1.3 prohibits any direct route between the Internet and any system component in the CDE. All inbound Internet traffic destined for the CDE must pass through a DMZ where it is inspected and proxied, a direct connection is never permitted. This is precisely the control that was absent or misconfigured in the Target 2013 breach: the HVAC vendor's network access provided a path that could reach the POS network in the CDE without proper firewall enforcement of this isolation principle.

The six-month rule review requirement (1.2.7) is one of the most commonly cited findings in PCI QSA assessments. Organizations that have not conducted a formal documented review of all firewall rules within the past six months receive a finding regardless of the actual quality of their rules. The review must document the business justification for each permit rule, "why is this port open, for what application, for what users?", and rules with no documented justification must be removed. This process directly combats the rule sprawl problem discussed earlier.

The anti-spoofing requirement (1.3.3) maps to RFC 2827 ingress filtering at the perimeter firewall, blocking packets arriving from the Internet with source IP addresses in private RFC 1918 ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) or other non-routable ranges, since such packets must be forged (legitimate Internet traffic cannot originate from those addresses). This simple ACL rule catches a wide range of spoofing-based attacks.

For organizations using cloud infrastructure, PCI DSS 4.0 Guidance clarifies that AWS Security Groups, Azure NSGs, and GCP VPC Firewall Rules qualify as "network security controls" satisfying Requirement 1 provided they are configured and managed according to the same principles, restrict to necessary traffic, review regularly, document changes. Cloud-native controls do not exempt organizations from the requirement; they provide an alternative implementation path.

PCI scoping separates the cardholder data environment, POS terminals, payment processing servers and systems holding the primary account number, from out-of-scope systems such as HR and segmented inventory. The scope boundary drives the firewall segmentation design.
:::

%%%

---
unit: Framework
code: ZTN
title: Zero Trust and Firewalls
---
:::callout style=soft
**Zero Trust** is a security model that eliminates implicit trust based on network location, requiring continuous verification of identity, device health, and authorization for every access request. NIST SP 800-207 defines Zero Trust Architecture (ZTA) and fundamentally changes the role of the network perimeter firewall from the primary access control to one enforcement point among many.
:::

:::code language=mermaid caption="Zero Trust places the Policy Decision Point at the center and surrounds each resource with a Policy Enforcement Point, network location provides no trust by itself"
flowchart LR
  IAM["IAM: identity"] --> PDP["Policy Decision Point"]
  MDM["MDM: device posture"] --> PDP
  TI["Threat intelligence"] --> PDP
  PDP -->|"allow or deny"| P1["PEP: app gateway"]
  PDP -->|"allow or deny"| P2["PEP: microsegment"]
  P1 --> R1["Application"]
  P2 --> R2["Database"]
:::

::::columns
::col::
:::callout style=line
**Perimeter model:** Trust the network; verify at the edge.
:::
:::callout style=soft
**Zero Trust model:** Never trust, always verify, regardless of network location.
:::
::col::
:::list heading="Zero Trust Principles (NIST SP 800-207)" style=plain
- All resources authenticated and authorized on every access
- Least privilege access, just enough, just in time
- Continuous monitoring and validation of security posture
- Network location is not sufficient to grant trust
- Dynamic policy enforcement based on identity and context
:::
::col::
:::list heading="Firewall's Role in ZTA" style=plain
- Microsegmentation between workloads (Policy Enforcement Points)
- Identity-based policy rules (user and device, not just IP)
- NGFW inspects traffic between microsegments
- Integrates with IAM for context-aware access decisions
- Logs feed continuous monitoring platform
:::
::::

:::notes
The traditional perimeter security model, sometimes called "castle and moat", assumes that everything inside the network perimeter is trusted and everything outside is untrusted. The firewall sits at the moat, controlling what gets in. This model was designed for an era when employees worked from a fixed office location on corporate-managed devices connected to a corporate-managed network. That architecture no longer describes most organizations: employees work from home, coffee shops, and hotels; applications have moved to SaaS platforms outside the perimeter; and cloud infrastructure has erased the traditional network boundary.

The Jericho Forum first articulated the "de-perimeterization" problem in 2004, noting that the traditional firewall perimeter was dissolving and that security architecture needed to evolve. NIST SP 800-207, published in August 2020, provides the authoritative federal definition of Zero Trust Architecture and identifies seven tenets, including: all communication is secured regardless of network location; access to individual enterprise resources is granted on a per-session basis; access is determined by dynamic policy; all enterprise-owned and associated devices are monitored; no resource is inherently trusted based solely on being on an enterprise network segment.

The practical implication for firewall architecture is significant. In a Zero Trust model, the perimeter firewall does not disappear, it continues to enforce boundary controls, but the trust model shifts. Internal traffic between workloads, previously trusted because it was "inside" the network, is now treated with the same suspicion as external traffic. Every east-west connection between application tiers must be authorized. This is implemented through microsegmentation, where each workload or application tier is surrounded by a software firewall policy (implemented through NGFWs, host-based firewalls, or SDN-based controls like VMware NSX or Cisco ACI) that enforces least-privilege inter-workload communication.

Google's BeyondCorp project, published in a series of papers beginning in 2014, is the most prominent real-world Zero Trust implementation. Google eliminated VPN access entirely for its corporate network, instead making all internal applications accessible via HTTPS through an access proxy that enforces per-request authentication and device posture checks. This architecture made the network perimeter irrelevant, the access control decision is made at the application level regardless of where the user is connecting from.

The 2020 SolarWinds breach again illustrates why Zero Trust matters: the attackers operated within a "trusted" internal network position for months after initial access, exploiting the implicit trust granted to the SolarWinds Orion system. In a microsegmented Zero Trust architecture, even a compromised software update agent would find its outbound communications restricted to approved destinations and verified against policy, the lateral movement and C2 communications that defined the SolarWinds intrusion would have been either prevented or significantly more detectable.

The core change in Zero Trust is from IP-based to identity-based policy. A stolen laptop connected to the corporate network is "internal" and a traditional firewall grants it access; Zero Trust grants none until it verifies the user's identity, the device's security posture and the specific access entitlements.
:::

%%%

---
unit: CaseStudy
code: CS1
title: Case Study, Target 2013 Breach
---
:::callout style=soft
The 2013 Target Corporation data breach exposed **40 million payment card records** and **70 million customer records**. It is the canonical case study for firewall segmentation failure: attackers used a compromised HVAC vendor's network credentials to pivot from a building management system into the point-of-sale (POS) network, where they installed RAM-scraping malware that captured card data at the moment of transaction.
:::

:::code language=mermaid caption="The Target breach followed a six-step kill chain, the critical failure was a network segmentation gap that permitted pivot from the HVAC vendor segment to the POS network"
flowchart TB
  A["1 Spear phishing of Fazio Mechanical, Target's HVAC vendor"] --> B["2 Vendor portal credentials stolen"]
  B --> C["3 Access to Target's vendor portal"]
  C --> D["4 Pivot to the point-of-sale network: weak segmentation"]
  D --> E["5 Memory-scraping malware on POS terminals"]
  E --> F["6 About 40 million card numbers exfiltrated"]
:::

:::steps heading="Attack Kill Chain"
1. Attacker sends spear-phishing email to Fazio Mechanical (HVAC vendor)
2. Citadel malware harvests Fazio's Target vendor portal credentials
3. Attacker authenticates to Target's vendor portal (legitimate credentials, permitted traffic)
4. Insufficient network segmentation allows pivot from vendor management zone to POS network
5. BlackPOS malware deployed on ~1,800 POS terminals, scrapes card data from memory during transaction
6. Exfiltration server staged inside Target's network; data transferred to external FTP server over 19 days
:::

::::columns
::col::
:::list heading="Failed Controls" style=plain
- No segmentation between HVAC vendor zone and POS network
- Vendor portal access not limited to HVAC-related systems only
- POS terminals on same network segment as vendor-accessible systems
- Security team received FireEye alerts but did not act on them
:::
::col::
:::list heading="Applicable Controls (NIST)" style=plain
- NIST SP 800-53 AC-4: Information Flow Enforcement
- NIST SP 800-53 SC-7: Boundary Protection
- PCI DSS Req. 1.3: No direct Internet-to-CDE connections
- PCI DSS Req. 12.8: Manage service provider relationships
:::
::::

:::notes
The Target breach is required reading for anyone designing or operating network security controls. It is not a story of sophisticated zero-day exploitation, it is a story of basic network segmentation failure. The attacker (believed to be a Ukrainian cybercriminal group) used stolen credentials to access a legitimate vendor portal, then exploited the absence of any firewall segmentation between the vendor management network and the payment card processing network to deploy malware across Target's POS infrastructure.

Fazio Mechanical Services was a Pennsylvania-based HVAC contractor that had electronic access to Target's network for remote monitoring and management of refrigeration and HVAC units in Target stores. Fazio's access was legitimately granted and represented exactly the kind of vendor relationship that PCI DSS Requirement 12.8 requires organizations to manage carefully, ensuring vendors with access to the cardholder data environment have appropriate security controls. Critically, Target's vendor portal granted access that extended beyond what was necessary for HVAC management. The principle of least privilege, codified in NIST SP 800-53 Control AC-6, requires that access be limited to the minimum necessary to perform the authorized function.

The segmentation failure was the decisive control gap. Once inside the vendor portal, the attacker could reach Target's POS network, the same network segment where PAN data was processed in cleartext in POS terminal RAM at the moment of card swipe. BlackPOS (also known as Kaptoxa) was a commercially available RAM-scraping malware that had been circulating in criminal forums since late 2012. It installed as a Windows service, intercepted the card data from the payment application's process memory between the card swipe and the transmission for authorization, and stored it locally before exfiltrating it. FireEye's malware detection system, which Target had recently installed, did generate alerts when BlackPOS was deployed, but Target's security operations team failed to escalate or act on them. This is a critical lesson: detection without response is insufficient. NIST SP 800-61 (Computer Security Incident Handling Guide) addresses the response process, emphasizing that detection outputs must be connected to documented response procedures and accountability.

Target's total breach-related costs exceeded $292 million, partially offset by $90 million in cyber insurance recovery. The breach resulted in the departure of both the CIO and CEO. Forty-seven state attorneys general pursued litigation. Congress held hearings. The breach directly accelerated the U.S. transition to EMV chip card technology, chip transactions encrypt the PAN during authorization, rendering RAM-scraped data useless, and prompted significant regulatory scrutiny of retail payment security practices.

The corrective controls are straightforward. A firewall rule explicitly denying all traffic from the vendor management network zone to the POS network zone would have stopped the lateral pivot. A requirement that vendor portal access be limited to the specific systems vendors need to manage would have constrained the blast radius of the credential theft. These are Requirement 1.2 (restrict traffic to the CDE to only necessary traffic) and Requirement 1.3.1 (restrict inbound traffic to the CDE). Both requirements existed in PCI DSS v2.0, which was the applicable standard at the time of the breach, Target was PCI DSS compliant, yet breached. Compliance is necessary but not sufficient. The spirit of the control, meaningful segmentation enforced operationally, is what mattered, and Target had the letter but not the spirit.

The 2013 Target breach, in which attackers reached point-of-sale systems through an HVAC vendor's network access, would have been contained by a few firewall rules: deny all traffic from the vendor VLAN to the POS VLAN, restrict vendor portal access to specific vendor server addresses, and block outbound connections from POS terminals except to the payment processor.
:::

%%%

---
unit: CaseStudy
code: CS2
title: Case Study, SolarWinds 2020
---
:::callout style=soft
The 2020 SolarWinds supply chain attack compromised the software build process of SolarWinds Orion, a widely-deployed IT monitoring platform, to insert the SUNBURST backdoor into a signed software update distributed to approximately 18,000 organizations, including multiple U.S. federal agencies. The attack demonstrated that perimeter firewalls are blind to threats originating from trusted software update channels.
:::

:::code language=mermaid caption="SUNBURST communicated via HTTPS to a C2 domain, indistinguishable from legitimate Orion telemetry to any perimeter firewall"
flowchart LR
  A["SUNBURST injected into<br/>the SolarWinds build"] --> B["Poisoned update on the<br/>legitimate update server"]
  B --> C["Installed as part of a<br/>trusted Orion update"]
  C --> D["Backdoor calls out to<br/>attacker infrastructure"]
  D --> E["Selected victims:<br/>second-stage access"]
:::

:::list heading="Attack Characteristics" style=plain
- **Initial Access**: Poisoned SolarWinds Orion software update (signed, legitimate distribution channel)
- **C2 Communication**: SUNBURST beaconed to avsvmcloud[.]com via HTTPS, indistinguishable from normal Orion traffic
- **Dormancy**: Malware waited 12–14 days after installation before activating to evade sandbox analysis
- **Lateral Movement**: Used valid tokens and credentials to move laterally, appeared as authorized access
- **Detection Gap**: Estimated 9-month dwell time before discovery by FireEye in December 2020
:::

::::columns
::col::
:::callout style=line
Every HTTPS connection on port 443 to a known domain looks legitimate to a firewall, including the SUNBURST C2 beacon.
:::
::col::
:::list heading="Lessons for Network Controls" style=plain
- Firewall allowlisting of software update destinations does not prevent poisoned updates
- DNS-based threat intelligence (blocking avsvmcloud[.]com) would have disrupted C2 if deployed
- Behavioral detection (Zeek, UEBA) can identify the regular beaconing interval
- Zero Trust device integrity checks could detect the unauthorized process
:::
::::

:::notes
The SolarWinds Orion attack, attributed to the Russian Foreign Intelligence Service (SVR) and the threat group known as Cozy Bear or APT29, represents the most sophisticated supply chain attack publicly disclosed to date. It exploited the fundamental trust that organizations place in signed software updates from vendors, a trust that is appropriately placed for legitimate software but creates a catastrophic blind spot when the vendor's build process is compromised.

SUNBURST (CVE-2020-10148) was injected into the SolarWinds Orion build pipeline through access to the SolarWinds development environment, likely via the SUNSPOT malware that was separately installed on the build server. The poisoned DLL was compiled into the legitimate Orion update package, signed with SolarWinds' legitimate code signing certificate, and distributed through SolarWinds' normal update delivery infrastructure. From the perspective of every security control at every victim organization, endpoint protection, network firewalls, email gateways, the update was indistinguishable from a legitimate software update.

Once installed, SUNBURST employed an extraordinarily cautious activation sequence. It checked for the presence of security software processes (Wireshark, Kaspersky, Carbon Black, CrowdStrike, and others), refused to activate if it found them, and then waited a random period between 12 and 14 days before making its first network connection. This dormancy period was designed to outlast the retention period of most sandbox analysis systems. It checked that the compromised host was domain-joined (indicating a legitimate enterprise network rather than an isolated sandbox), then began DNS-based encoded communications to stage 1 C2, followed by HTTPS communications to stage 2 infrastructure on avsvmcloud[.]com, a domain that had been registered to appear as a plausible Azure cloud subdomain.

The C2 traffic was HTTPS on port 443. Every organization affected had almost certainly configured their perimeter firewall to permit outbound HTTPS. There was no abnormal port, no known-malicious IP (the domain resolved to Azure infrastructure), and no unusual protocol. The firewall saw exactly what it was designed to see: a permitted, encrypted HTTPS connection from an enterprise server to a cloud service. This is the fundamental limitation described in the "What Firewalls Don't Stop" slide made concrete in one of the most significant intelligence operations in recent history.

Detection would have required either DNS-based threat intelligence (blocking or alerting on the specific avsvmcloud[.]com domain, Mandiant and CISA published indicators of compromise in December 2020, but retrospective detection required that organizations had retained DNS query logs), behavioral anomaly detection (noting that the Orion service was now making outbound HTTPS connections on a regular beaconing schedule different from its normal telemetry pattern), or network flow analysis (Zeek/Bro generating conn.log entries showing periodic connections to the same external destination from the Orion server).

The SUNBURST response produced CISA Emergency Directive 21-01, requiring federal agencies to immediately disconnect or power down SolarWinds Orion installations. It also accelerated NIST's work on software supply chain security, culminating in NIST SP 800-218 (Secure Software Development Framework) and directly influencing Executive Order 14028 (Improving the Nation's Cybersecurity, May 2021), which mandates software bill of materials (SBOM) requirements for software sold to the federal government, addressing the root cause problem of understanding what is actually in a software build.

SUNBURST's dormancy period and anti-sandbox checks show attackers who understood enterprise controls and designed the malware to evade each one in sequence. It is a case study in adversarial thinking about security architecture, the mindset defenders must develop.
:::

%%%

---
unit: Operations
code: FPL
title: Firewall Policy Lifecycle
---
:::callout style=soft
A firewall rule base is not a static configuration artifact, it is a living document that must be managed through a formal lifecycle: design, implement, review, audit, and retire. Without active lifecycle management, rule bases accumulate stale, overly permissive, and undocumented rules that expand the attack surface over time.
:::

:::code language=mermaid
flowchart LR
  D["Design<br/>business need, policy"] --> I["Implement<br/>change approval"]
  I --> M["Monitor<br/>logs, alerts"]
  M --> R["Review<br/>rule audit at least every six months"]
  R --> X["Retire<br/>remove unused rules"]
  X --> D
:::

:::steps heading="Firewall Change Management Process"
1. Business requirement identified, document the service, port, source, destination, and business justification
2. Security review, validate that the requested access meets least-privilege principles
3. Change approval, firewall change request reviewed by security team and change advisory board (CAB)
4. Implementation, rule added with a comment documenting justification, requester, and approval date
5. Testing, verify the rule permits intended traffic and does not expose unintended access
6. Monitoring, confirm rule is used; set expiration review date
7. Periodic review, audit all rules every six months; remove or tighten unused rules
:::

:::list heading="Common Rule Base Hygiene Issues" style=plain
- **Any/Any rules**: "Permit any any" rules that override intended restrictions, often added during troubleshooting and never removed
- **Shadowed rules**: Rules that can never match because an earlier rule has already matched all their traffic
- **Unused rules**: Rules that have not matched any traffic in the last 90 days, candidates for removal
- **Undocumented rules**: Rules with no comment explaining their purpose or authorizing party
:::

:::notes
Firewall rule base management is an operational discipline that directly determines the long-term security posture of the network. Technical debt accumulates in firewall rule bases just as it does in application code: rules are added to solve immediate problems, network changes make old rules obsolete, and without deliberate cleanup, the rule base grows into an unmaintainable tangle where the security team no longer understands what the rules collectively permit.

The PCI DSS six-month review requirement (Requirement 1.2.7 in PCI DSS v4.0) establishes a minimum review cadence that most security frameworks endorse. NIST SP 800-41 Rev. 1 recommends periodic rule reviews as part of ongoing firewall policy management. In practice, organizations with mature security programs review high-risk firewall changes (e.g., new permits to the CDE) within 24 hours and conduct comprehensive rule base reviews quarterly. The review process should produce documented evidence: a list of rules reviewed, the business justification for each permit rule, and the disposition of each reviewed rule (retained, tightened, or removed).

The "any/any" rule problem deserves special attention. During incident response or troubleshooting, network engineers frequently add broad permit rules to eliminate the firewall as a variable, "permit any any" to confirm whether the firewall is blocking the traffic. These troubleshooting rules must be removed immediately after the troubleshooting session, but in the urgency of incident response, documentation and cleanup are often overlooked. Automated rule analysis tools (Tufin, AlgoSec, Firemon) detect "any" source or "any" destination permit rules and flag them for review. An any/any rule in a production firewall is the digital equivalent of propping open the fire door, it defeats the entire purpose of the control.

Shadowed rules occur when a rule earlier in the ACL matches all traffic that a later rule intends to match, making the later rule unreachable. For example: Rule 3 permits TCP from 10.0.0.0/8 to any port 443. Rule 7 denies TCP from 10.0.0.100 to 172.16.1.50 port 443. Rule 7 is shadowed, any traffic from 10.0.0.100 to 172.16.1.50 port 443 was already permitted by Rule 3 and evaluation stopped. Rule 7 will never match. The intended deny is silently ineffective. This is particularly dangerous when the administrator believes a deny rule is protecting a specific sensitive server but the rule is actually dead. Automated rule analysis detects shadowed rules and is a standard feature of enterprise firewall management platforms.

Firewall rule expiration and justification documentation are operationally important for a subtle reason: staff turnover. A firewall rule added by a network engineer who left the organization two years ago, with no comment explaining its purpose, cannot be safely removed without investigation, removing it might break a production application. Organizations that maintain complete documentation for every rule (requester, approver, business justification, date added, associated change ticket) can evaluate and retire any rule confidently, regardless of who added it or when.

Firewall rule-set review identifies shadowed rules, leftover any/any troubleshooting rules that should have been removed, and rules lacking documented justification. This review is the operational skill most needed in firewall administration.
:::

%%%

---
unit: Misconceptions
code: FAQ
title: Common Misconceptions About Firewalls
---
:::callout style=soft
Firewalls are one of the most widely misunderstood security controls. These misconceptions lead to false confidence, inadequate complementary controls, and security gaps. Understanding what firewalls actually do, and do not do, is the foundation for building a sound layered security architecture.
:::

:::table
| Misconception                                 | Reality                                                                  |
|-----------------------------------------------|--------------------------------------------------------------------------|
| "We have a firewall, so we're secure"         | Firewalls enforce policy only, they cannot detect intent in allowed traffic |
| "NAT protects us like a firewall"             | NAT provides incidental obscurity, not access control, it is not a security control |
| "Encrypted traffic is safe"                   | TLS encryption hides threats from DPI, 90%+ of web traffic is encrypted |
| "Compliance means our firewall is secure"     | PCI/ISO compliance is a minimum bar; misconfigured compliant firewalls are common |
| "Firewalls stop insider threats"              | Firewalls filter network traffic, they have no visibility into user intent |
| "Outbound traffic doesn't need filtering"     | C2 beaconing, data exfiltration, and DNS tunneling all use outbound channels |
| "Host-based firewalls are redundant with network firewalls" | Host-based firewalls protect devices on untrusted networks outside the perimeter |
:::

:::notes
These misconceptions are not academic, each one represents a real pattern that causes real organizations to be breached. Working through each in turn:

"We have a firewall, so we're secure" is the most pervasive misconception. It conflates the presence of a control with the effectiveness of a security program. A firewall with a single allow-any rule, no logging, and no monitoring provides essentially no security value despite being technically present. The firewall's value comes from the policy it enforces, the logging it provides, and the monitoring that acts on those logs. Firewalls are necessary but not sufficient components of a security program.

"NAT protects us like a firewall" is technically incorrect in a specific way: NAT provides no access control. It prevents unsolicited inbound connections only because there is no translation table entry to forward them, not because any security policy evaluated and denied them. The moment an internal host initiates an outbound connection (even to a malicious server), NAT creates a table entry that permits return traffic. Malware routinely exploits this with reverse shells. An actual firewall with deny-by-default policy and explicit outbound allow rules is categorically different from relying on the incidental behavior of NAT.

"Encrypted traffic is safe" confuses confidentiality (what TLS provides to the endpoints) with security (the absence of malicious content). TLS encryption protects the privacy of the communication between the client and server, it does not prevent the server from sending malware or the client from being a compromised host exfiltrating data. From the firewall's perspective, encrypted traffic is opaque unless TLS inspection is deployed.

"Compliance means our firewall is secure" is disproven by the Target breach, Target was PCI DSS compliant at the time of the breach. Compliance frameworks set minimum requirements; they cannot anticipate every attack vector or verify that controls are operating effectively rather than merely configured. NIST's Cybersecurity Framework explicitly distinguishes between "implementing" controls and "verifying their effectiveness", compliance typically assesses the former.

"Outbound traffic doesn't need filtering" is a dangerous assumption that attackers actively exploit. Every C2 callback, DNS exfiltration, ICMP tunnel, and data exfiltration uses outbound connectivity. NIST SP 800-53 CA-3 (Information Exchange) and SC-7 (Boundary Protection) both address the need for monitoring and restricting outbound traffic as well as inbound. An egress filtering policy that permits outbound traffic only to known good destinations (allowlist-based) dramatically reduces the attack surface for C2 communication and data exfiltration.

SUNBURST communicated over outbound HTTPS on port 443, and so did the Orion server's legitimate update traffic, so a simple allow/deny by port cannot separate them. Distinguishing the two requires application-aware controls or DNS-based allow-listing, which is why strict egress filtering is harder than it first appears.
:::

%%%

---
unit: Comparison
code: CFW
title: Firewall Vendor Landscape
---
:::callout style=soft
The firewall market is served by a diverse set of vendors offering hardware appliances, virtual firewalls, and cloud-native implementations. Understanding the major platforms, their strengths, architectures, and differentiators, is essential for security professionals who will encounter them in enterprise environments, certifications, and vendor documentation.
:::

:::code language=mermaid caption="The firewall vendor landscape spans hardware appliances, virtual instances, cloud-native controls, and open-source platforms, each with distinct capabilities and use cases"
mindmap
  root((Firewall platforms))
    Traditional enterprise
      Cisco ASA
      Juniper SRX
    Next-generation
      Palo Alto PA-Series
      Fortinet FortiGate
      Check Point
    Cloud-native
      AWS security groups and Network Firewall
      Azure Firewall
    Host-based
      Windows Defender Firewall
      iptables and nftables
:::

:::table
| Vendor / Platform         | Type              | Key Differentiator                                      | Relevant Certification |
|---------------------------|-------------------|---------------------------------------------------------|------------------------|
| Palo Alto Networks PA/VM  | NGFW              | App-ID, User-ID, WildFire threat intelligence           | PCNSA, PCNSE           |
| Cisco Firepower (FTD)     | NGFW              | Snort IPS integration, Cisco ecosystem integration      | CCNA Security, CCNP Security |
| Fortinet FortiGate        | NGFW / UTM        | FortiOS, Security Fabric integration, price/performance | NSE certifications     |
| Check Point NGFW          | NGFW              | SmartConsole centralized management, Infinity platform  | CCSA, CCSE             |
| Cisco ASA                 | Traditional       | Mature stateful inspection, extensive deployment base   | CCNA, CCNP             |
| pfSense / OPNsense        | Open-source       | Free/community, flexible, widely used in SMB and labs   | None (community)       |
| AWS Network Firewall      | Cloud-native      | Suricata rule-based, VPC-integrated, managed service    | AWS Security Specialty |
| Azure Firewall            | Cloud-native      | Fully managed, FQDN filtering, Azure-native integration | AZ-500                 |
:::

:::notes
Security professionals do not operate in a vendor-neutral vacuum, they work with specific platforms that have distinct management interfaces, policy models, log formats, and troubleshooting approaches. Familiarity with the major platforms accelerates onboarding in new roles and is directly tested in vendor-specific certifications that are increasingly valued by employers.

Palo Alto Networks is widely recognized as the NGFW market leader (consistently positioned as a Leader in the Gartner Magic Quadrant for Network Firewalls). PAN-OS, the operating system running all Palo Alto firewall products, uses a unified security policy model where rules are based on App-ID (application identity), User-ID (mapped user identity from Active Directory), and Device-ID (device type and posture). The WildFire cloud-based threat prevention service provides near-real-time signature updates from samples detonated in a distributed sandbox, organizations see a threat signature within minutes of the first global instance being analyzed. Palo Alto VM-Series virtual firewalls and Prisma Cloud extend the same PAN-OS policy model to virtualized and cloud-native environments.

Cisco FirePOWER Threat Defense (FTD) merged the Cisco ASA stateful inspection engine with the Sourcefire IPS engine (acquired by Cisco in 2013, which developed the Snort open-source IPS engine). Snort is the most widely deployed IPS engine in the world, and the FTD's integration gives organizations access to the VRT (Vulnerability Research Team) rule set and the Cisco Talos Intelligence Group's threat intelligence. Cisco Firewall Management Center (FMC) provides centralized policy management, event analysis, and network topology visualization across FTD deployments.

Fortinet FortiGate occupies a strong position in the small-to-medium enterprise and branch office market, offering a consolidated Unified Threat Management (UTM) platform that integrates firewall, IPS, antivirus, URL filtering, and SD-WAN in a single appliance with FortiOS. The Security Fabric architecture interconnects FortiGate with Fortinet's endpoint protection (FortiClient), SIEM (FortiSIEM), and SOAR (FortiSOAR) products, enabling automated threat response workflows. FortiGate is frequently encountered in assessments because of its broad deployment base.

For students pursuing Cisco certifications (CCNA, CCNP Security, CCIE Security), the Cisco ASA and FTD platforms are the primary technical focus. The ASA command-line interface, with its access-group, access-list, and object-group commands, is a common exam topic. Understanding how ASA ACLs differ from IOS router ACLs (ASA uses real-time hits counters, supports object groups natively, and applies ACLs to interfaces in a specific direction) is essential for the certification track.

Open-source platforms (pfSense, OPNsense) deserve mention for lab environments and cost-sensitive deployments. pfSense, based on FreeBSD with the pf packet filter, provides a web-based management interface that closely mirrors enterprise concepts, firewall rules, NAT, VPN, traffic shaping, making it an excellent learning platform. Many security engineering candidates have pfSense running as their home lab firewall, which provides hands-on experience directly transferable to enterprise deployments. pfSense Community Edition is free; Netgate sells pfSense Plus with commercial support and additional features.

:::

%%%

---
unit: Operations
code: WEX
title: Worked Example, Designing a Firewall Rule Set
---
:::callout style=soft
Designing a firewall rule set requires translating business and security requirements into specific, ordered permit and deny rules following least-privilege principles. This worked example walks through the design process for a small web application deployment with a database backend.
:::

:::code language=mermaid caption="Working from the architecture outward: identify required traffic flows, then write the minimum set of rules that permits them and denies everything else"
flowchart LR
  U["Internet users"] -->|"TCP 443"| W["Web server (DMZ)"]
  W -->|"TCP 5432"| DB["Database server (internal)"]
  AD["Administrators (internal)"] -->|"TCP 22"| W
  AD -->|"TCP 22"| DB
  U -.-x|"everything else denied"| DB
:::

:::steps heading="Rule Design Process"
1. Document the required traffic flows (what needs to talk to what, on what port, in which direction)
2. Group sources and destinations using network objects for maintainability
3. Write the most specific permit rules first (narrowest source, destination, and port)
4. Add deny rules for explicitly known-bad traffic (threat intelligence blocklists, known-bad subnets)
5. Rely on the implicit deny-all to block everything not explicitly permitted
6. Add logging to all permit rules and all deny rules
7. Review for shadowed rules before implementation
:::

:::table
| Rule # | Action  | Source                  | Destination          | Protocol/Port | Purpose                              |
|--------|---------|-------------------------|----------------------|----------------|--------------------------------------|
| 1      | Permit  | Any (Internet)          | 203.0.113.10 (web)   | TCP 443        | HTTPS to web server                  |
| 2      | Permit  | 203.0.113.10 (web)      | 192.168.10.5 (DB)    | TCP 5432       | Web-to-DB (PostgreSQL)               |
| 3      | Permit  | 192.168.1.0/24 (admins) | 203.0.113.10 (web)   | TCP 22         | Admin SSH to web server              |
| 4      | Permit  | 192.168.1.0/24 (admins) | 192.168.10.5 (DB)    | TCP 22         | Admin SSH to DB server               |
| 5      | Deny    | Any                     | Any                  | Any            | Implicit deny-all (logged)           |
:::

:::notes
This worked example addresses a common and realistic deployment scenario: a web application fronted by HTTPS, with a backend database that the web server must reach, and administrative access for the operations team. The goal is to construct the minimum necessary rule set, sufficient to permit all required legitimate traffic, nothing more.

Step one is always to enumerate required traffic flows before touching the firewall console. The discipline of documenting flows before writing rules prevents both over-permitting (adding broad rules "just in case") and under-permitting (discovering missing rules in production). For this scenario: Internet users need HTTPS to the web server; the web server needs PostgreSQL access to the database; administrators need SSH to both servers for maintenance. These are the three functional requirements, each representing a specific traffic flow.

Rule 1 permits inbound HTTPS from any Internet source to the web server's public IP. The source is "Any" because we do not control which IP addresses our legitimate users come from. The destination is specifically the web server IP (not any DMZ server), and the port is specifically TCP 443 (not any port). This is correctly narrow on two of three dimensions.

Rule 2 permits TCP 5432 (PostgreSQL) from only the web server IP to only the database IP. This is the critical internal segmentation rule: the database should accept connections only from the application server, not from any other host. If the web server is compromised, this rule limits what the attacker can reach from it, they cannot reach any other internal host on the database port. This is least-privilege applied to east-west internal traffic, the core concept behind microsegmentation.

Rule 3 and Rule 4 restrict SSH administrative access to the administrator subnet only. SSH should not be accessible from the Internet (which would mean Rule 1's "Any" source could also be used for SSH brute force). Using a specific source subnet for management access is the correct approach; ideally this would be further restricted to specific named hosts within that subnet.

Rule 5 is the explicit logging of the implicit deny. Most firewalls implement an implicit deny-all but may not log it unless explicitly configured. Making the final deny explicit with logging ensures that all blocked traffic is recorded, the denied traffic logs are often the first indicator of reconnaissance, scanning, or misconfigured applications.

Common mistakes students make at this stage: placing a broad permit rule before the more specific deny (the ACL ordering trap from the checkpoint slide); using "any" for destination ports on rules that should be port-specific ("permit TCP any 192.168.10.5 any" instead of "permit TCP 203.0.113.10 192.168.10.5 eq 5432"); and omitting logging directives, which makes the rule set unauditable. Each of these mistakes has a real-world consequence, the first two create security gaps, the third creates an operational gap.

For the audit step, review the rule table for shadowed rules: is there any combination of sources and destinations from rules 1-4 that Rule 5's deny-all would already have caught before the specific rule? No, each rule is more specific than the catch-all, and they are ordered before it. Check for "any" in destination port fields on rules 1-4, none present, all are port-specific. Check that every server is reachable only for its intended function and from its intended source, the web server is reachable on TCP 443 from any source, and on TCP 22 only from the admin subnet. The database is reachable on TCP 5432 from only the web server, and on TCP 22 from only the admin subnet. The rule set correctly implements least privilege.

:::

%%%

---
unit: Summary
code: FIN
title: Lecture Summary, Firewalls & Network Controls
---

:::code language=mermaid caption="Every topic in this lecture connects back to the same principle: firewalls are one essential layer in a defense-in-depth strategy, not a complete solution in themselves"
flowchart TB
  T["<b>Firewall types</b><br/>stateless, stateful, NGFW, WAF, host-based"]
  D["<b>Deployment</b><br/>perimeter, DMZ, zone-based, cloud"]
  F["<b>Filtering</b><br/>ACLs, DPI, NAT"]
  O["<b>Operations</b><br/>logging, SIEM, rule review"]
  T --> D
  T --> F
  D --> O
  F --> O
:::

:::pullquote
A firewall without logging is a lock with no record of who turned the key. A firewall without complementary controls is a locked front door with an open window.
:::

::::columns
::col::
:::list heading="Firewall Types Covered" style=plain
- Stateless (packet filter)
- Stateful (connection-aware)
- Next-Generation (App/User/IPS)
- Web Application Firewall (WAF)
- Host-Based (endpoint enforcement)
:::
::col::
:::list heading="Architecture Patterns" style=plain
- Perimeter firewall
- DMZ (dual-firewall)
- Zone-based policy
- Cloud firewalls (AWS/Azure/GCP)
- Microsegmentation / Zero Trust
:::
::col::
:::list heading="Key Operational Principles" style=plain
- Implicit deny-all default
- Least-privilege rule design
- First-match-wins ACL ordering
- Regular rule base review and audit
- Log everything, permitted and denied
:::
::col::
:::list heading="Standards Referenced" style=plain
- NIST SP 800-41 (Firewall Policy)
- NIST SP 800-207 (Zero Trust)
- PCI DSS v4.0 Req. 1
- ISO/IEC 27001 / 27033
- RFC 2827 (Ingress Filtering)
:::
::::

:::notes
This lecture covered the complete spectrum of firewall technology, from the foundational concepts of packet filtering through to modern Zero Trust architectures. The key thread connecting every topic is that firewalls are access control enforcement mechanisms, they implement policy, and the quality of the security they provide is directly proportional to the quality of the policy they enforce.

The progression from stateless to stateful to next-generation firewalls represents a continuous expansion of context: stateless firewalls know only what is in the packet header; stateful firewalls add session context; NGFWs add application identity, user identity, and threat intelligence. Each generation addresses weaknesses in the previous model while introducing new operational complexity and, in some cases, new attack surfaces (state table exhaustion, TLS inspection privacy concerns).

The DMZ and zone-based architecture slides illustrated that firewall placement is as important as firewall configuration. A correctly configured firewall in the wrong position provides limited value; architectural design must ensure that all trust boundaries are enforced and that no path through the network exists that bypasses the intended controls. The Target breach made this concrete: the gap was not in the firewall technology but in the architectural decision to allow connectivity between the vendor management network and the POS network without enforcement.

The limitations section, expanded in the misconceptions slide and the case studies, is perhaps the most important conceptual contribution of the lecture. Students who leave with an understanding of what firewalls cannot do, and why, are equipped to identify the complementary controls needed to fill those gaps: IDS/IPS for behavioral detection of permitted traffic, WAF for application-layer attack prevention, SIEM for correlation and monitoring, EDR for endpoint visibility, and Zero Trust architectures for eliminating implicit trust from network location.

The worked example grounded the theoretical content in a practical skill: rule design. The ability to translate a business requirement into a correctly ordered, least-privilege firewall rule, and to audit an existing rule set for shadowed, redundant, and overly permissive entries, is a directly employable technical skill in network security roles.

For the next class, students should be prepared to discuss how intrusion detection systems complement the firewall controls covered today, and to think about what detection would have looked like in the Target and SolarWinds scenarios if comprehensive logging and SIEM correlation had been in place. Reading: NIST SP 800-94 Sections 1-3 (Guide to Intrusion Detection and Prevention Systems), available at nvlpubs.nist.gov.

:::
