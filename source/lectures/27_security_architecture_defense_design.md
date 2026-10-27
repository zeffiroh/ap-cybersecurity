---
deck:
  title: Security Architecture & Defense Design
  kicker: Class 27
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 27
  description: Layered security, control types, and the NIST CSF, assembling everything in this course into one architecture.
  topics: [Layered Security, Preventive/Detective/Corrective Controls, Security Planning]
---

%%%
---
title: Security Architecture & Defense Design
cover: true
---
:::text class=sub
Enterprise Frameworks, Control Typologies, and Zero Trust Architecture
:::

:::list style=chips
- Defense in Depth
- Control Classification
- NIST CSF 2.0
- Zero Trust (SP 800-207)
:::

:::image src="images/27_cover_security_architecture.png" alt="Isometric illustration of a layered enterprise security model: an outermost ring labeled Physical, then a ring labeled Network, then Application, then Data at the center; small shield icons mark each layer; an attacker figure at the perimeter faces multiple concentric rings; the NIST CSF six-function wheel (Govern, Identify, Protect, Detect, Respond, Recover) appears in the corner as an organizing framework" caption="Security architecture assembles individual controls into a unified, layered defense, each ring of protection compensating for the potential failure of the one before it." width=full
:::

:::notes
Welcome to Class 27. Throughout this course, we have analyzed individual security elements in depth: firewalls, intrusion detection systems, access control matrices, cryptographic algorithms, and secure coding practices. Today, we make a critical conceptual transition, from examining individual tools in isolation to studying security architecture and defense design as an integrated discipline.

Security architecture is the systematic practice of organizing, configuring, and managing these individual tools into a unified, intentional enterprise design that serves the organization's specific business objectives and risk profile. The distinction between "having tools" and "having an architecture" is not merely semantic. A firewall misconfigured to allow unnecessary traffic, a SIEM that generates thousands of alerts with no triage procedure, and an MFA deployment that covers only some accounts are all examples of tools purchased and deployed without architectural cohesion. The result is a collection of expensive systems that generate a false sense of security while leaving critical gaps.

To understand the practical consequences of architectural failure, consider several historical case studies. In the 2013 Target breach, one of the largest retail breaches in history, attackers entered via a third-party HVAC vendor's credentials, then moved laterally through the network to access point-of-sale systems. Target had security tools, including a sophisticated malware detection system that correctly flagged the attack, but lacked the processes and escalation architecture to act on the alerts before 40 million credit card numbers were stolen. In the 2017 Equifax breach, a known Apache Struts vulnerability (CVE-2017-5638) remained unpatched for over two months after a patch was available, because the organization lacked a coordinated vulnerability management architecture. In both cases, the failures were architectural, organizational, procedural, and design failures, not the absence of individual security tools.

In today's lecture, we will explore how professional frameworks guide organizations in building architectures that avoid these failure modes. We begin with SABSA and TOGAF, which provide business-aligned frameworks for making architectural decisions. We then examine Defense in Depth, the foundational strategy of layering independent controls so that the failure of any single one does not result in total compromise. We will study the full taxonomy of security controls defined in NIST SP 800-53, learning how to balance preventive, detective, and corrective controls across technical, administrative, and physical domains.

We will then examine Zero Trust Architecture as defined in NIST SP 800-207, the most important architectural paradigm shift of the past decade, driven by the dissolution of the traditional network perimeter through cloud computing, remote work, and mobile devices. Finally, we will explore the NIST Cybersecurity Framework 2.0, a comprehensive lifecycle model that ties together all these architectural concepts under a single, business-aligned framework. Secure design principles, including least privilege, fail-safe defaults, and economy of mechanism, provide the engineering rules that make each component of the architecture as robust as possible.

By the end of this lecture, you will be equipped to evaluate an organization's security posture, identify architectural gaps, and propose a coherent, multi-layered defense aligned to business risk. This is the analytical framework you will apply in Class 29's risk assessment project and Class 30's final capstone.
:::

%%%
---
unit: Foundations
code: ARCH
title: Architectural Frameworks & Principles
---
:::callout style=soft
Enterprise security architecture translates business objectives and risk tolerances into technical controls. It relies on standard frameworks like **SABSA** (Sherwood Applied Business Security Architecture) and **TOGAF** to align business, logic, and physical assets.
:::

::::columns ratio=1:1
::col::
::::card heading="The Architectural Deficit"
:::list style=tight
- **Siloed Controls:** Individual systems operating without coordinated policy enforcement.
- **Complexity Overhead:** Excess tools increase configuration errors and security gaps.
- **Reactive Posture:** Focusing entirely on past incidents rather than structured risk.
:::
::::
::col::
::::card heading="Core Architectural Goals"
:::list style=tight
- **Consistency:** Ensuring policy is enforced uniformly across host, network, and cloud.
- **Resilience:** Building systems that degrade gracefully under active attack.
- **Traceability:** Mapping every technical control to a specific business risk.
:::
::::
::::

:::steps
**Architecture Vision:** Define the scope, stakeholders, and business drivers, answering "what are we protecting, and why?", to bound the design effort before specifying any technical controls.
**Business Architecture:** Map critical business processes and information flows to identify which assets, data classifications, and third-party integrations require protection.
**Information Systems Architecture:** Document data flows, application interdependencies, and sensitivity classifications (e.g., PII, PHI, CUI) so controls can be calibrated to the value of what they protect.
**Technology Architecture:** Specify the hardware platforms, network topology, software stacks, and protocols that will implement the logical security requirements identified in the previous phase.
**Opportunities & Solutions:** Evaluate candidate controls against cost, risk-reduction value, and implementation feasibility, selecting the minimum set of well-integrated controls over a proliferation of point solutions.
**Governance & Review:** Establish audit procedures, compliance checkpoints, and continuous review mechanisms to validate that the implemented architecture remains effective as the business and threat landscape evolve.
:::

:::image src="images/27_architecture_frameworks.png" alt="Two-column comparison diagram: left column shows the SABSA matrix with rows labeled Contextual, Conceptual, Logical, Physical, Component, Operational and columns labeled Assets, Motivation, Function, Information, Location, Time, People, each cell representing a security question at a given abstraction level; right column shows TOGAF ADM cycle with labeled phases: Architecture Vision, Business Architecture, Information Systems Architecture, Technology Architecture, Opportunities and Solutions, Migration Planning" caption="SABSA (left) maps security across six architectural levels and six dimensions. TOGAF ADM (right) provides a repeatable cycle for developing and governing enterprise architectures." width=full
:::

:::notes
To design an effective enterprise defense, we must first establish a methodology for thinking about security holistically rather than as a collection of individual controls. When security controls are deployed in isolation, without reference to each other or to the business context they are meant to protect, they create a fragmented posture that is expensive to manage, difficult to audit, and prone to critical gaps.

Security architecture is the discipline that provides this holistic perspective. It begins with the recognition that security decisions must be derived from and traceable to business requirements. Installing an expensive next-generation firewall is not a security strategy; it is a procurement decision. A security strategy asks: what specific business assets are we protecting, from which specific threat actors, and what is the acceptable risk level given our budget and regulatory obligations?

Professional security architects use established frameworks to provide structure to this analysis. SABSA, the Sherwood Applied Business Security Architecture, uses a six-layer matrix (contextual, conceptual, logical, physical, component, and operational) crossed with six dimensions (assets, motivation, function, information, location, time, and people) to ensure no aspect of the security problem is overlooked. At the contextual layer, the architect asks what the business needs and why. At the logical layer, the architect defines which security services are required and how they interact. At the physical layer, the architect specifies products and protocols. This layered approach ensures that a decision to implement, say, multi-factor authentication is tied to specific business assets and risk scenarios, not merely adopted because it is fashionable.

TOGAF, the Open Group Architecture Framework, provides a structured process called the Architecture Development Method (ADM) for developing and governing enterprise architectures. The ADM cycle moves through phases including Architecture Vision, Business Architecture, Information Systems Architecture, Technology Architecture, and Governance. TOGAF ensures that security considerations are embedded in each phase of enterprise IT planning rather than being retrofitted after the fact.

Good architecture minimizes unnecessary complexity. This principle, sometimes called "economy of mechanism," is one of Saltzer and Schroeder's original 1975 secure design principles. Complex systems with many interacting components are inherently difficult to configure correctly, test thoroughly, and monitor effectively. Each additional component is a potential failure point and a potential attack surface. Security teams that respond to every threat by purchasing another tool eventually find themselves managing dozens of partially integrated systems, with more configuration burden than threat coverage. Effective architecture involves rationalizing the control set, choosing a smaller number of well-integrated, well-monitored controls over a proliferation of isolated point solutions.

The three core goals of any security architecture are consistency, resilience, and traceability. Consistency means that a security policy, for example, "all remote access requires MFA", is enforced identically across every system, including cloud workloads, legacy systems, and partner integrations. Resilience means the architecture degrades gracefully under attack: no single point of failure produces a total compromise. Traceability means every technical control can be mapped back to a documented business risk or regulatory requirement, enabling the organization to make rational cost-benefit decisions about its security investments.

ISO/IEC 27001:2022, the international standard for information security management systems, provides complementary governance structure to SABSA and TOGAF. While SABSA and TOGAF focus on the design and development of architectures, ISO 27001 offers a certifiable management system, its Annex A controls map directly to NIST SP 800-53 Rev. 5 control families, allowing organizations operating across U.S. federal and European regulatory environments to satisfy both frameworks through a single integrated control set, materially reducing compliance overhead.
:::

%%%
---
unit: Layering
code: DID
title: Layered Security & Defense in Depth
---
:::callout style=soft
**Defense in Depth (DiD)** is an architectural strategy that employs multiple, redundant security controls across different layers of the enterprise. If one control fails, subsequent layers prevent a total system compromise.
:::

:::code language=mermaid caption="Defense in Depth visualized as a series of concentric protection layers. An attacker targeting the Data layer at the center must successfully penetrate every outer layer, each of which operates independently and uses different technologies. The diversity of controls ensures that a vulnerability in one layer (e.g., a network firewall bypass) does not automatically defeat the others (e.g., host-level EDR and data encryption)."
graph TD
    Data["Data (AES-256, Database Access Controls)"] --> App["Application (WAF, Secure Coding, Input Validation)"]
    App --> Host["Host (EDR, OS Hardening, Patch Management)"]
    Host --> Net["Network (Microsegmentation, Firewalls, IDS/IPS)"]
    Net --> Perimeter["Perimeter (DDoS Mitigation, Boundary Routing)"]
    Perimeter --> Physical["Physical (Mantraps, Security Badges, Biometrics)"]
:::

:::image src="images/27_defense_in_depth_layers.png" alt="Concentric rings diagram with Data at the center in red, surrounded by rings labeled Application, Host, Network, Perimeter, and Physical from inside to outside; each ring contains 2-3 small icons representing the controls deployed at that layer (e.g., lock icon for encryption at Data layer, code icon for WAF at Application layer, shield icon for EDR at Host layer); a stick-figure attacker at the outermost edge faces an arrow pointing inward that is blocked at each successive ring with a stop sign" caption="Defense in Depth: each ring represents an independent layer of protection. An attacker must breach all layers to reach sensitive data. The independence of each layer ensures that a single failure does not cascade to a total compromise." width=full
:::

:::notes
Defense in Depth is the most fundamental design pattern in security architecture and the conceptual organizing principle behind every layered security deployment. The term originates from military strategy, specifically from the doctrine of deploying multiple, independent defensive lines rather than concentrating all resources at a single fortified perimeter. In the context of information security, it means deploying multiple independent controls across different technical layers and organizational domains, ensuring that no single failure is catastrophic.

The core assumption of Defense in Depth is that any individual security control can and eventually will fail. A password can be phished. An intrusion detection system can miss a novel zero-day payload. A firewall rule can be misconfigured. A patch may not be applied before it is exploited. Historical data strongly supports this assumption: virtually every significant breach involved the failure of at least one preventive control that should have stopped the attack. The question is not whether individual controls will fail, but whether the architecture as a whole is resilient enough to contain the impact of those failures.

A well-designed Defense in Depth architecture applies this principle at multiple distinct layers. At the physical layer, controls like mantraps, biometric access locks, security badges, CCTV surveillance, and physical security guards protect against unauthorized physical access to hardware. These controls operate completely independently of any software security measure. At the perimeter layer, DDoS mitigation services and boundary routing protect against volumetric network attacks. At the network layer, firewalls enforce segmentation policy, blocking unauthorized traffic flows between network segments. Intrusion Prevention Systems (IPS) inspect traffic for known attack signatures and block malicious connections. Microsegmentation divides the network into small, isolated security zones so that a compromised device cannot freely communicate with every other device.

At the host layer, Endpoint Detection and Response (EDR) agents monitor process execution, file system changes, and network connections in real time, detecting malicious behavior that network-layer controls cannot see because it occurs within an endpoint after legitimate access has been granted. OS hardening removes unnecessary services and software, reducing the attack surface. Patch management ensures known vulnerabilities are remediated. At the application layer, Web Application Firewalls (WAFs) inspect HTTP traffic for application-layer attacks like SQL injection and cross-site scripting. Secure coding practices prevent vulnerabilities from being introduced in the first place. Input validation ensures that data provided by users cannot be used to execute unintended operations. At the data layer, encryption at rest (AES-256) ensures that stolen data files cannot be read without the decryption key. Database access control lists restrict which accounts can query which tables, implementing least privilege at the data access level.

The value of this layering becomes clear when we trace an attacker's path in a well-defended environment. If an attacker phishes a user's password (defeating authentication), the network microsegmentation layer blocks them from reaching the database server directly. If they find a misconfigured firewall rule and reach the database host, the host EDR agent flags the anomalous connection attempt from an unexpected source. If they bypass EDR through a rootkit, the data is still protected by database-level access controls and encryption. At each stage, the attacker must find and exploit a different, independent vulnerability, dramatically increasing the probability of detection and containment.

NIST SP 800-53 Rev. 5 formalizes the control families relevant to each Defense in Depth layer. The System and Communications Protection (SC) family governs network and perimeter controls, SC-7 (Boundary Protection) mandates segmented DMZ architectures, and SC-5 (Denial-of-Service Protection) addresses perimeter-layer resilience. The System and Information Integrity (SI) family governs host and application controls, SI-3 (Malicious Code Protection) covers EDR deployment, and SI-7 (Software, Firmware, and Information Integrity) covers software supply-chain verification. Organizations subject to FISMA or FedRAMP must implement these controls at the Low, Moderate, or High baseline corresponding to their system categorization under FIPS 199.

This defense should be complemented by purple team exercises, where red team attackers simulate realistic adversaries and blue team defenders test detection and response capabilities. The goal is to empirically verify that each layer is actually working as designed, rather than assuming controls are effective without testing.
:::

%%%
---
unit: Controls
code: CTRL
title: Taxonomy of Security Controls (NIST SP 800-53)
---
:::callout style=soft
Security controls are classified both by **how** they act (Functional) and **where** they are implemented (Categorical). A mature architecture maintains a balanced distribution of these control types.
:::

:::table
| Control Category | Preventive (Stop) | Detective (Identify) | Corrective (Restore) |
|---|---|---|---|
| **Technical / Logical** | Firewalls, MFA, TLS Encryption, Access Control Lists (ACLs) | IDS/IPS, SIEM Log Analysis, Endpoint Detection & Response (EDR) | Automated Patching, Active Session Termination, Backups |
| **Administrative** | Security Policies, Least Privilege Policies, Security Awareness Training | Audits, Background Checks, Compliance Reviews | Incident Response Plans, Disaster Recovery Procedures |
| **Physical / Operational**| Mantraps, Fences, Biometric Access Locks | CCTV Cameras, Motion Sensors, Guard Patrol Logs | Fire Suppression Systems, UPS Backup Generators |
:::

:::image src="images/27_control_taxonomy_matrix.png" alt="3x3 grid diagram showing control taxonomy: columns labeled Preventive, Detective, Corrective; rows labeled Technical, Administrative, Physical; each of the 9 cells contains 3-4 example control names with small icons (lock for technical preventive, eye for technical detective, wrench for technical corrective, document for administrative, building for physical); heat map shading shows common organizational over-investment in Technical Preventive controls (highlighted in blue) versus under-investment in Administrative Corrective (highlighted in orange)" caption="The NIST SP 800-53 control taxonomy: mature security programs distribute investments across all nine cells. Most organizations over-invest in Technical Preventive controls while neglecting Administrative Corrective capabilities like incident response planning." width=full
:::

:::notes
Security controls are the specific mechanisms, policies, and procedures that implement security architecture decisions. NIST Special Publication 800-53 provides the most comprehensive catalog of security controls for federal information systems, but its taxonomy is widely used across private industry as well. Understanding how to classify controls using this taxonomy is essential for identifying gaps, justifying investments, and communicating security strategy to leadership.

The taxonomy has two dimensions. The first is functional: what role does the control play in the incident lifecycle? Preventive controls attempt to stop an attack before it succeeds. Detective controls identify when an attack is occurring or has occurred. Corrective controls limit the damage and restore operations after a compromise. A mature security program needs all three. An organization that invests only in preventive controls will be unprepared when, not if, an attacker bypasses those controls. An organization with only detective controls can identify attacks but cannot contain or recover from them efficiently.

The second dimension is categorical: where or how is the control implemented? Technical controls are implemented in hardware and software. They operate automatically, consistently, and at machine speed. Administrative controls are implemented through policies, procedures, and organizational practices. They depend on human execution and are therefore subject to human error, inconsistency, and compliance gaps. Physical controls protect the tangible environment, the buildings, hardware, and physical access paths.

Examining the 3x3 intersection of these dimensions reveals common architectural weaknesses. The upper-left cell, Technical Preventive, tends to be the most heavily invested category in most organizations. Firewalls, MFA systems, encryption, and ACLs are well-understood, vendor-marketed, and relatively easy to deploy. However, this focus creates blind spots. Organizations that invest heavily in technical preventive controls but neglect administrative corrective controls (the middle-right cell) are particularly vulnerable. When a breach occurs despite their preventive measures, they lack documented incident response procedures, trained incident response teams, and tested disaster recovery capabilities. The result is chaotic, slow, and costly incident handling.

Consider a concrete example of this imbalance. A financial services firm implements state-of-the-art network firewalls, endpoint MFA, and full-disk encryption on all laptops (Technical Preventive). However, they have no documented incident response plan (Administrative Corrective gap), no tested backup restoration procedure (Technical Corrective gap), and no physical security badges at server room entries (Physical Preventive gap). When an attacker compromises their VPN credentials and moves laterally to the file server, the firm's preventive controls failed and no adaptive response capability exists.

The goal of using this taxonomy is to conduct a control coverage assessment: mapping existing controls onto the 3x3 grid, identifying which cells are overinvested and which are underinvested, and directing the next round of security investment toward filling the gaps rather than adding redundant controls in already-covered areas. NIST SP 800-53 provides hundreds of specific control items across 20 control families, from Access Control (AC) to System and Communications Protection (SC), each mapped to functional categories and implementation guidance. NIST SP 800-171 provides a condensed subset for organizations handling Controlled Unclassified Information (CUI), and is foundational to the CMMC certification framework used in the U.S. defense industrial base.
:::

%%%
---
unit: Paradigm
code: ZTA
title: Zero Trust Architecture (NIST SP 800-207)
---
:::callout style=soft
**Zero Trust** is an architectural paradigm based on the principle of **"never trust, always verify."** It eliminates implicit trust based on network location, treating all traffic, internal and external, as hostile.
:::

::::columns ratio=1:1
::col::
::::card heading="Perimeter-Centric Model"
:::list style=tight
- **Implicit Trust:** Internal users and devices are assumed trustworthy.
- **Castle-and-Moat:** Strong perimeter defenses, but weak internal controls.
- **Lateral Movement:** Once inside, attackers can access most internal systems.
:::
::::
::col::
::::card heading="Zero Trust Model (SP 800-207)"
:::list style=tight
- **Explicit Verification:** Every request is authenticated and authorized.
- **Least Privilege:** Dynamic access based on user, device, and context.
- **Microsegmentation:** Network partitioned into isolated security zones.
:::
::::
::::

:::steps
**Step 1 – Establish Strong Identity:** Deploy phishing-resistant MFA (FIDO2/WebAuthn) for all user accounts and implement Privileged Access Management (PAM) to control administrative credentials with just-in-time provisioning.
**Step 2 – Validate Device Health:** Require device compliance checks, OS patching status, EDR agent active, disk encrypted, MDM enrolled, as a prerequisite condition evaluated by the Policy Decision Point before any resource access is granted.
**Step 3 – Define Dynamic Access Policies:** Configure the Policy Decision Point (PDP) with context-aware rules that evaluate user identity, device posture, network location, time-of-day, and resource sensitivity at every individual access request.
**Step 4 – Implement Microsegmentation:** Divide the internal network into workload-level or application-level segments, enforcing east-west traffic controls via software-defined networking or host-based firewalls so that a compromised workload cannot reach adjacent resources.
**Step 5 – Monitor Continuously & Refine:** Instrument all access paths with telemetry, feed data into SIEM and UEBA analytics to detect anomalous lateral movement attempts, and refine least-privilege policies as user roles and business processes evolve.
:::

:::image src="images/27_zero_trust_architecture.png" alt="Split diagram comparing perimeter-centric vs Zero Trust models: left half shows castle-and-moat with thick outer wall (firewall) and open flat interior where an attacker who crossed the wall can freely access all servers; right half shows Zero Trust with a Policy Decision Point in the center connected to a Policy Enforcement Point on every resource access path; each workstation, server, and database requires explicit authentication; microsegmentation walls divide every resource into isolated zones; color coding shows green for trusted verified sessions and red for blocked requests" caption="Left: the perimeter-centric model trusts all internal traffic, enabling lateral movement after a single perimeter breach. Right: Zero Trust requires explicit verification at every access point, with least-privilege dynamic policies and microsegmentation containing any compromise." width=full
:::

:::notes
For decades, enterprise network security relied on the perimeter-centric model, often called the "castle-and-moat" architecture. The basic premise was that the corporate network had a well-defined boundary, the perimeter, which was defended by firewalls, intrusion prevention systems, and VPN gateways. Anything inside the perimeter was implicitly trusted. A user on the corporate LAN could access file servers, databases, and printers without re-authentication, because their presence inside the perimeter was taken as evidence of legitimacy.

This model worked reasonably well when enterprise computing was confined to physical corporate offices with clear geographic and network boundaries. Employees worked on managed workstations, applications ran on internal servers, and the only external connections were carefully controlled internet access points. However, the modern enterprise is fundamentally different. Cloud platforms host critical business applications outside the traditional perimeter. Remote work means employees connect from home networks, coffee shops, and airports. Mobile devices and BYOD policies introduce unmanaged endpoints. Third-party contractors and supply-chain partners require access to internal resources. The perimeter has effectively dissolved.

More critically, the castle-and-moat model fails catastrophically when its single perimeter is breached. If an attacker compromises a VPN credential, phishes a legitimate employee's session token, or plants malware via a supply-chain attack, they enter the "trusted" interior and can move laterally with little resistance. The 2020 SolarWinds attack, where attackers inserted malicious code into a software update distributed to thousands of government and enterprise customers, illustrated this perfectly. Once the malicious update was installed on internal network nodes, the attacker had implicit trust and could access nearly any internal resource they chose.

NIST Special Publication 800-207 provides a formal definition and implementation guidance for Zero Trust Architecture (ZTA), published in 2020. ZTA rests on three core tenets. First, assume breach: design your architecture as if attackers are already inside the network, and focus on preventing lateral movement and data exfiltration rather than only on perimeter defense. Second, verify explicitly: every access request, regardless of its origin (internal or external), must be authenticated and authorized. There is no implicit trust. Third, use least-privilege access: access rights are granted dynamically based on the minimum access needed for the specific operation, evaluated in real time based on user identity, device health, location, and the sensitivity of the requested resource.

The technical implementation of ZTA, as described in NIST SP 800-207, introduces two key components: the Policy Decision Point (PDP) and the Policy Enforcement Point (PEP). When a subject (user or service) requests access to a resource, the PEP intercepts the request and forwards it to the PDP for evaluation. The PDP evaluates the request against a dynamic policy that considers continuous signals: Has the user's account been flagged for anomalous behavior? Is the device compliant with endpoint security policies (e.g., EDR agent running, OS patched, disk encrypted)? Is the requested resource sensitive? What is the user's typical access pattern? Based on these signals, the PDP grants or denies access, and may impose conditional requirements (such as step-up MFA for high-sensitivity resources).

Microsegmentation is the network implementation of Zero Trust. Rather than having a flat internal network where any device can communicate with any other device on TCP/IP, the network is divided into small, isolated segments, often at the workload or even individual process level. Each segment is protected by its own access controls. Database servers in one segment cannot receive connections from workstations unless explicitly authorized through the PDP/PEP framework. This ensures that a compromised workstation cannot directly reach the database, dramatically reducing the attacker's ability to move laterally.

Implementing Zero Trust is a journey, not a single deployment. Organizations typically begin by addressing identity (strong MFA, privileged access management), then progress to device health verification, then microsegmentation, and finally to workload-level access controls. Google's BeyondCorp model, published in a series of technical papers between 2014 and 2018, is the industry's most widely studied practical implementation of Zero Trust principles at scale.
:::

%%%
---
unit: Framework
code: CSF
title: The NIST Cybersecurity Framework 2.0
---
:::callout style=soft
The **NIST CSF 2.0** organizes cybersecurity activities into six high-level Functions. This lifecycle provides a comprehensive model for managing cybersecurity risk.
:::

:::flow
GOVERN: Establish strategy, policies, and oversight to manage cybersecurity risk
IDENTIFY: Inventory assets, assess risks, and define organizational context
PROTECT: Implement safeguards to prevent or limit cybersecurity events
DETECT: Monitor systems to identify cybersecurity anomalies and events
RESPOND: Execute containment, analysis, and mitigation plans during an active incident
RECOVER: Restore operations and systems back to baseline performance
:::

:::image src="images/27_nist_csf_functions_wheel.png" alt="Circular wheel diagram divided into six colored segments representing NIST CSF 2.0 functions: GOVERN at the center hub in dark blue (indicating it drives all other functions), IDENTIFY in blue, PROTECT in green, DETECT in yellow-orange, RESPOND in orange, RECOVER in red; each segment has 3-4 subcategory labels in smaller text; arrows between adjacent segments show the lifecycle flow; the GOVERN hub has lines radiating to all other five segments indicating its cross-cutting role" caption="NIST CSF 2.0 six-function wheel: GOVERN sits at the center, driving strategy for all five operational functions. The outer functions form a continuous improvement cycle from asset identification through recovery." width=half
:::

:::notes
To provide a common language and organizational structure for all the architectural concepts we have discussed, security professionals rely on the NIST Cybersecurity Framework. Originally published in 2014 in response to Executive Order 13636, the framework was substantially updated to version 2.0 in 2024 to reflect the evolution of the threat landscape, cloud adoption, supply chain security concerns, and the need for explicit governance structures.

The most significant change in CSF 2.0 is the addition of the GOVERN function as the sixth and central function of the framework. In CSF 1.1, governance was implicitly addressed within the IDENTIFY function. CSF 2.0 elevates it to a separate top-level function and places it at the center of the wheel diagram, explicitly recognizing that cybersecurity cannot be treated as a purely technical function managed by the IT department. Effective cybersecurity requires organizational leadership, board-level risk appetite statements, formal cybersecurity policies, executive accountability, and integration of cybersecurity into enterprise risk management processes.

The GOVERN function addresses questions such as: Who owns cybersecurity risk in our organization? What is our acceptable risk level? How are security requirements communicated to vendors and partners? How do we ensure that security policies are actually implemented and enforced across business units? Without clear answers to these questions, even the most technically sophisticated defenses will have gaps caused by organizational inconsistency and unclear accountability.

The five operational functions form a continuous improvement lifecycle that organizations should execute repeatedly, not as a one-time project. The IDENTIFY function provides the foundational awareness required for all other activities: an accurate inventory of hardware, software, data, and third-party relationships, combined with a risk assessment that prioritizes which assets require the most protection. Organizations that skip IDENTIFY often spend enormous resources protecting the wrong things, or discover during an incident that a critical system was never included in their security scope.

The PROTECT function encompasses the controls discussed in our Defense in Depth and control taxonomy discussions: access management, data protection, training, maintenance, and protective technology deployment. DETECT covers the monitoring capabilities, SIEM, EDR, network traffic analysis, that identify when protective controls are being defeated. DETECT capabilities directly determine the Mean Time to Detect (MTTD) metric, which is one of the strongest predictors of breach cost: the Ponemon Institute's annual Cost of a Data Breach Report consistently shows that breaches identified faster result in significantly lower total cost.

RESPOND and RECOVER collectively address organizational resilience. RESPOND encompasses the incident handling procedures, containment, eradication, forensic analysis, notification, that activate when a security event is detected. RECOVER addresses business continuity: how quickly can the organization restore normal operations, and at what residual risk level? Tested backup procedures, documented recovery runbooks, and crisis communication plans are all RECOVER-function elements that many organizations neglect until they are facing an active breach.

The framework's power lies in providing a shared vocabulary and conceptual model that allows technical security teams, business leadership, auditors, and regulators to communicate effectively. A CISO can discuss "our DETECT function maturity" with the Board without needing to explain the technical details of SIEM correlation rules. External auditors can evaluate CSF alignment systematically. Business leadership can make risk investment decisions using a consistent, normalized framework rather than responding ad hoc to whichever technology vendor made the most recent sales call.
:::

%%%
---
unit: Framework
code: IMPL
title: NIST CSF Profiles & Implementation Tiers
---
:::callout style=soft
The NIST CSF is not a rigid checklist; it is a tool for continuous improvement. Organizations use **Profiles** and **Tiers** to assess their current security posture and plan their security roadmap.
:::

::::columns ratio=1:1
::col::
::::card heading="Framework Profiles"
:::list style=tight
- **Current Profile:** Documenting the organization's existing security practices and outcomes.
- **Target Profile:** Mapping the desired security posture based on risk tolerance.
- **Gap Analysis:** Identifying and prioritizing actions to move from current to target.
:::
::::
::col::
::::card heading="Implementation Tiers"
:::list style=tight
- **Tier 1 (Partial):** Reactive, informal risk management with low integration.
- **Tier 2 (Risk Informed):** Structured risk awareness, but inconsistent execution.
- **Tier 3 (Repeatable):** Formally approved, organization-wide risk processes.
- **Tier 4 (Adaptive):** Continuous improvement using predictive analytics.
:::
::::
::::

:::steps
**Step 1 – Inventory Subcategories:** List all CSF 2.0 subcategories relevant to the organization's industry, regulatory obligations (e.g., HIPAA, PCI DSS, CMMC), and board-approved risk appetite.
**Step 2 – Score the Current Profile:** For each subcategory, document whether the outcome is fully achieved, partially achieved, or not yet addressed, creating an honest baseline of existing security practices.
**Step 3 – Define the Target Profile:** Based on regulatory requirements, peer benchmarks, and risk tolerance, assign target achievement levels to each subcategory, reflecting deliberate choices, not a blanket "implement everything."
**Step 4 – Perform Gap Analysis:** Calculate the delta between current and target scores; subcategories with the largest gaps and highest risk weighting become the highest-priority investment areas.
**Step 5 – Develop a Prioritized Roadmap:** Convert gap analysis findings into a sequenced project plan with named owners, budget estimates, implementation timelines, and measurable success criteria.
**Step 6 – Reassess Regularly:** Repeat the profile assessment at least annually and after any significant architectural change, breach event, or regulatory update to track progress and adapt the roadmap.
:::

:::image src="images/27_csf_profiles_tiers.png" alt="Two-part diagram: left part shows a horizontal 'Current vs Target Profile' gap analysis with a bar chart showing each CSF subcategory on the y-axis and current maturity vs target maturity scores on the x-axis, with the gap between them shaded in orange labeled 'Investment Priority'; right part shows a vertical maturity ladder with four rungs labeled Tier 1 Partial at the bottom through Tier 4 Adaptive at the top, with each rung annotated with characteristics of that tier's risk management maturity and an organization icon climbing the ladder" caption="CSF Profiles quantify the gap between current and target security posture. Implementation Tiers characterize the maturity of risk management processes, from ad-hoc reactive (Tier 1) to continuously adaptive (Tier 4)." width=full
:::

:::notes
The NIST Cybersecurity Framework is a flexible tool, not a compliance checklist that must be implemented exactly as written. Its power comes from how organizations use it to measure and improve their specific security posture over time. Two mechanisms enable this: Framework Profiles and Implementation Tiers.

Framework Profiles translate the abstract CSF functions and categories into a concrete description of an organization's specific security practices. The framework contains subcategories, specific, measurable security outcomes, organized under each function. A Current Profile documents the organization's existing achievement of each subcategory: which outcomes are fully achieved, which are partially achieved, and which are not yet addressed. This creates an honest, structured snapshot of the organization's security state.

The Target Profile documents the organization's goal state, the security outcomes it needs to achieve, based on its specific business context, industry threat landscape, regulatory requirements, and risk tolerance. A hospital handling protected health information (PHI) under HIPAA will have a different Target Profile from a small manufacturing firm or a retail operation subject to PCI DSS. The Target Profile is not necessarily "implement everything at the highest level", it reflects deliberate choices about where additional investment provides meaningful risk reduction.

The gap between the Current Profile and the Target Profile is the Gap Analysis. This analysis, when performed rigorously, produces a prioritized list of security activities the organization should invest in to move from its current posture to its target. Critically, it allows the organization to say, "We are already strong in Access Control and Identity Management, but we have significant gaps in Detection capabilities and Incident Response planning, so our next investment cycle should focus there." This evidence-based prioritization is far more defensible to leadership than generic vendor recommendations.

Implementation Tiers measure the maturity of an organization's risk management processes, not the presence of specific technical controls. This is an important distinction. An organization can have sophisticated technical tools but manage them in an ad-hoc, undocumented way, that organization would score at Tier 1 or Tier 2 despite its technology spending. Tiers measure process maturity, not technology inventory.

Tier 1 (Partial) organizations have informal, reactive risk management practices. Risk activities occur in response to incidents rather than proactively, and are not coordinated across business units. Security policies may not exist or may not be enforced consistently. This is common in small businesses and early-stage organizations. Tier 2 (Risk-Informed) organizations have begun to structure their risk management, with documented risk assessments and awareness of the threat environment, but these practices are inconsistently applied and are not integrated with enterprise risk management. Tier 3 (Repeatable) organizations have formally approved, organization-wide risk management policies and processes that are consistently executed across business units, with defined roles and accountability. The security program is integrated with broader enterprise risk management. Tier 4 (Adaptive) organizations continuously improve their security practices based on real-time threat intelligence and lessons learned, using metrics and analytics to dynamically adjust their risk management approach. This represents the most mature and operationally effective security posture.

Most organizations realistically aspire to Tier 3 as a sustainable long-term goal. Tier 4 requires significant ongoing investment in threat intelligence, analytics, and program governance that is economically justified primarily for large enterprises with high-value targets and mature security programs. The Tiers are not a hierarchy to race through; they are a calibration tool for honest self-assessment and meaningful planning.
:::

%%%
---
unit: Design
code: DSGN
title: Secure Design Principles
---
:::callout style=soft
First formalized by Saltzer and Schroeder in 1975, secure design principles serve as foundational rules for software, network, and system engineering.
:::

:::steps
**Least Privilege:** Users and processes should operate using the minimum set of privileges necessary to complete their tasks.
**Fail-Safe Defaults:** Access decisions should deny by default; if a security control fails, the system must revert to a secure state.
**Economy of Mechanism:** Keep designs simple; complex systems are harder to test, monitor, and configure.
**Separation of Duties:** Require multiple independent entities to complete sensitive tasks to prevent fraud or single-point failures.
**Defense in Depth:** Deploy multiple layers of defense to protect against the failure of any single control.
:::

:::image src="images/27_secure_design_principles.png" alt="Five-panel grid diagram, one panel per design principle: Panel 1 (Least Privilege) shows a user with a small key labeled 'minimal access' unable to open a large vault, contrasted with a smaller labeled door they can open; Panel 2 (Fail-Safe Defaults) shows a firewall power outage causing all traffic to be blocked by default rather than allowed through; Panel 3 (Economy of Mechanism) shows a simple lock mechanism vs a complex entangled mechanism labeled 'more attack surface'; Panel 4 (Separation of Duties) shows two people each holding half a key needed to unlock a server; Panel 5 (Defense in Depth) shows concentric rings each with a stop sign" caption="The five core secure design principles from Saltzer and Schroeder (1975), foundational engineering rules that apply equally to software architecture, network design, and operational procedures." width=full
:::

:::notes
Before discussing the enterprise architecture case study, we must examine the engineering principles that govern the design of individual components within a security architecture. These principles were originally articulated by Jerome Saltzer and Michael Schroeder in their foundational 1975 paper "The Protection of Information in Computer Systems," published in the Proceedings of the IEEE. Remarkably, they remain directly applicable, perhaps more relevant than ever, to modern cloud, container, and microservice architectures.

The principle of least privilege is arguably the most impactful and consistently under-implemented of all security design principles. It states that every process, user, and service should operate with the minimum set of privileges necessary to accomplish its intended function, and only for the time period it needs those privileges. In practice, this means a web application should have database credentials that allow it to read and write only the specific tables it needs, not credentials with full database administrator access. A developer should have access to the systems and data required for their work, not administrator access to production systems they do not manage. A service account running a backup job should have read access to the files it backs up, not write access that could allow a compromised backup agent to corrupt data.

The reason least privilege is so powerful is that it limits the blast radius of any individual compromise. When an attacker gains access to an account or process, they can only do what that account or process is allowed to do. If the compromised web application account cannot access the `/etc/passwd` file, the operating system configuration tables, or other database schemas, an attacker who hijacks that account gains far less leverage than they would with administrator privileges. Least privilege implementation requires effort, it demands that access rights be analyzed, documented, and enforced rather than assigned generously "to avoid operational friction", but the security dividend is enormous.

Fail-safe defaults addresses the behavior of systems when they encounter unexpected conditions or failures. The principle is straightforward: in the absence of explicit authorization, deny access. If an access control system crashes, all requests should be rejected, not granted. If a firewall rule engine encounters an ambiguous packet, it should drop the packet, not forward it. If a software authentication module encounters an error it cannot handle, it should fail closed (deny the operation) rather than fail open (permit the operation). This principle prevents attackers from deliberately triggering error conditions to bypass security controls, a technique known as error-based bypass.

Economy of mechanism counteracts a pervasive tendency in enterprise security: the accumulation of redundant tools and overly complex architectures in response to each new threat. Every additional component adds attack surface, configuration burden, interoperability complexity, and monitoring overhead. Simple, well-understood mechanisms that do one thing correctly are far more trustworthy than complex mechanisms with many interacting components. This principle manifests in software design as a preference for small, auditable codebases over monolithic systems; in network design as preference for clear, documented firewall rule sets over thousands of overlapping rules that no one fully understands.

Separation of duties applies the dual-control principle from physical security to information systems. Sensitive or high-consequence operations should require the involvement of at least two independent entities, such that no single person can complete the operation alone. In financial systems, the person who authorizes a wire transfer should be different from the person who processes it. In software development, the engineer who writes code should not be the same person who approves it for production deployment. In security operations, the person who administers firewall rules should not be the same person who audits firewall logs. Separation of duties prevents both fraudulent insider actions and the catastrophic impact of a single compromised account.

Defense in depth, the final principle, ties together all the other design principles under the architectural umbrella. As discussed in the layered security section, this principle mandates redundancy in defense mechanisms so that no single failure produces total compromise. These five principles, applied consistently across every layer of an architecture, produce systems that are not merely resistant to known attacks, but that degrade gracefully and generate meaningful signals when adversaries probe for weaknesses.
:::

%%%
---
unit: Case Study
code: CASE
title: Designing an Enterprise Architecture
---
:::callout style=soft
Let's analyze how secure design principles and control layers are applied to protect a high-value database containing personally identifiable information (PII).
:::

:::code language=mermaid caption="Enterprise architecture for PII database protection: traffic flows inward through progressively stricter controls. The external firewall eliminates non-HTTPS traffic. The WAF inspects application-layer payloads. An internal firewall restricts database protocol access to only the authorized application server. The database layer enforces encryption and EDR monitoring. SIEM aggregates logs from all layers for centralized visibility. Each layer uses different technology and operates independently, a failure at one layer triggers detection at the next."
graph TD
    Internet["Internet"] --> DDoS["DDoS Shield & Edge Router"]
    DDoS --> Firewall1["External Firewall (Denies all except HTTPS)"]
    Firewall1 --> DMZ["DMZ (Web Servers & WAF)"]
    DMZ --> Firewall2["Internal Firewall (Permits SQL from DMZ only)"]
    Firewall2 --> AppZone["Internal App Segment"]
    AppZone --> DB["DB Server (AES-256 Encrypted, EDR Active)"]
    
    DB --> SIEM["SIEM & SOC Monitoring (Real-time Audit Logs)"]
:::

:::image src="images/27_enterprise_dmz_architecture.png" alt="Network architecture diagram with labeled network zones: leftmost zone labeled Internet with cloud icon and attacker figure; center-left zone labeled DMZ containing web server, load balancer, and WAF icons; center zone labeled App Tier with application server; rightmost zone labeled Data Tier with database server and encryption lock icon; horizontal barriers between zones labeled Firewall 1 (external) and Firewall 2 (internal); a DDoS shield at the internet boundary; downward arrows from all zones pointing to SIEM icon at the bottom labeled SOC Monitoring; IP flow labels on firewall barriers show 'HTTPS only' and 'SQL from App only'" caption="Enterprise DMZ architecture for PII protection: three physically distinct network segments, two firewalls with distinct rule sets, application-layer inspection in the DMZ, and centralized SIEM monitoring across all zones." width=full
:::

:::notes
Let's walk through a concrete enterprise security architecture case study that applies all the principles and frameworks we have discussed in this lecture. Our scenario is protecting a database containing sensitive customer personally identifiable information (PII), a high-value target that is subject to regulatory requirements under GDPR, CCPA, and potentially HIPAA depending on the data types involved.

A naive architecture would place the database on a server with a public IP address, protected only by a username and password. This is unfortunately common in misconfigured cloud environments and small businesses. It fails catastrophically because the database port (typically TCP 3306 for MySQL or TCP 5432 for PostgreSQL) is directly accessible from the internet, and a single credential compromise or unpatched vulnerability exposes the entire database.

A secure architecture applies Defense in Depth principles by placing the database behind multiple independent layers of protection. Let's trace the path a legitimate user and a potential attacker must take.

All internet traffic first encounters the DDoS shield and edge routing layer. Cloud-based DDoS mitigation services, such as Cloudflare Magic Transit or AWS Shield, absorb volumetric denial-of-service attacks before they reach the datacenter. The edge router applies border-level filtering, dropping traffic from known malicious IP blocks and implementing rate limiting.

Traffic that passes DDoS mitigation reaches the external firewall. This firewall is configured with a default-deny policy (fail-safe defaults) and permits only HTTPS traffic on TCP port 443 destined for the web server IP addresses in the DMZ. All other ports and protocols are blocked. This immediately eliminates a vast category of network-layer attacks: port scanning, protocol exploitation, and connection attempts to backend database ports are blocked before they reach any application-serving system.

The Demilitarized Zone (DMZ) hosts the web-facing components: load balancers, web servers, and a Web Application Firewall (WAF). The WAF operates at the application layer (OSI Layer 7), inspecting the content of HTTP requests to detect and block application-layer attacks that the network firewall cannot see. SQL injection attempts, cross-site scripting payloads, path traversal attacks, and known exploit patterns are identified and blocked by the WAF. The DMZ is specifically designed so that these publicly accessible systems, if compromised, cannot directly access the internal database segment.

The internal firewall sits between the DMZ and the internal application zone. Its rule set is even more restrictive: it permits only database query traffic (TCP 3306/5432) from the specific IP addresses of the application servers in the DMZ to the database server in the internal segment. All other traffic, including SSH management access from the DMZ, is blocked. An attacker who compromises a web server in the DMZ cannot use that foothold to attack the database server directly, they must first bypass this internal firewall.

The database server itself operates in the most restricted zone. It runs an EDR agent that monitors all process execution, file system changes, and network connections in real time. The database files are encrypted at rest using AES-256, so that an attacker who gains physical access to the storage hardware or snapshots a disk image cannot read the data without the decryption key. Database access is controlled using least-privilege principles: the application has a dedicated database account with query permissions only on the specific tables it needs. The DBA has a separate account for administration tasks. Direct interactive logins to the database from application code are prohibited; prepared statements are required at the application layer to prevent SQL injection even if WAF rules are bypassed.

Finally, all components in this architecture ship their logs to a centralized SIEM platform, where a 24/7 SOC monitors for anomalies. If an attacker reaches the internal firewall and begins probing database ports, the SIEM generates an alert for an analyst to investigate. The layered architecture ensures that the attacker must sequentially breach multiple independent systems, each generating telemetry that provides detection opportunities, before reaching the protected data.
:::

%%%
---
unit: Summary
code: SUM
title: Designing a Resilient Architecture
---
:::callout style=soft
Effective security architecture is a continuous lifecycle of risk identification, control implementation, and iterative refinement.
:::

::::columns ratio=1:1
::col::
::::card heading="Key Takeaways"
:::list style=tight
- **Architecture over Tools:** Coordinated defenses are more effective than isolated systems.
- **Functional Balance:** Mature security programs invest in preventive, detective, and corrective controls.
- **NIST CSF Alignment:** Using standard frameworks aligns technical controls with business goals.
:::
::::
::col::
::::card heading="The Next Step"
:::list style=tight
- **Class 28 (Lab):** Applying these principles to analyze logs in a SOC environment.
- **Class 29 (Project):** Conducting a structured risk assessment for an organization.
- **Class 30 (Capstone):** Designing a complete defense strategy for an active threat scenario.
:::
::::
::::

:::image src="images/27_security_roadmap.png" alt="Horizontal roadmap graphic showing a left-to-right progression with four labeled milestones: Milestone 1 labeled 'Class 28: SOC Lab, apply detection skills' with magnifying glass icon; Milestone 2 labeled 'Class 29: Risk Assessment Project, proactive analysis' with clipboard icon; Milestone 3 labeled 'Class 30: Capstone, design and defend' with shield icon; Milestone 4 labeled 'Career: Security Architect, Analyst, Engineer' with graduation cap icon; connecting arrows between milestones show knowledge building progressively" caption="The remaining course milestones build sequentially: the SOC lab applies detection skills from this lecture, the risk assessment project applies proactive planning, and the capstone integrates everything into a complete defense design." width=full
:::

:::notes
In today's lecture, we connected the individual tools and concepts we have studied this term into a unified security architecture. We moved from examining isolated controls to understanding how Defense in Depth, Zero Trust, and the NIST Cybersecurity Framework 2.0 provide the structural scaffolding for enterprise-grade security programs.

We examined the taxonomy of security controls, distinguishing between preventive, detective, and corrective functions, and technical, administrative, and physical categories. The key insight from this taxonomy is that mature security programs intentionally distribute their investments across all nine cells of this matrix. Organizations that over-invest in Technical Preventive controls and neglect Administrative Corrective capabilities, particularly incident response planning and business continuity procedures, consistently suffer greater damage when preventive controls eventually fail.

We explored Zero Trust Architecture and why it has become the dominant architectural paradigm for modern enterprises. The dissolution of the traditional network perimeter through cloud computing, remote work, and mobile devices has made the castle-and-moat model obsolete. Zero Trust's three tenets, assume breach, verify explicitly, and enforce least privilege, provide a coherent response to a threat environment where attackers regularly operate from inside the network.

The NIST Cybersecurity Framework 2.0 provides the organizational model that ties these architectural concepts together under a business-aligned governance structure. The addition of the GOVERN function in CSF 2.0 reflects the reality that cybersecurity risk is ultimately a business risk requiring board-level ownership and organizational accountability, not just a technical problem for the IT department to solve in isolation.

Finally, we reviewed the five foundational secure design principles, least privilege, fail-safe defaults, economy of mechanism, separation of duties, and defense in depth, showing how these engineering rules apply at every layer of the architecture, from software design to network configuration to operational procedures.

The business case for investing in mature security architecture is increasingly well-documented. IBM's Cost of a Data Breach Report 2024 found that organizations with fully deployed Zero Trust architecture experienced average breach costs $1.76 million lower than those without ZTA in place. Organizations with mature AI and automation capabilities in their DETECT and RESPOND functions identified and contained breaches 108 days faster than organizations without these capabilities, and incurred $2.22 million less in total breach cost. These figures translate directly into the NIST CSF framework: the measurable financial benefit reflects the combined value of mature GOVERN (clear accountability and risk appetite), DETECT (fast identification), and RESPOND (rapid containment) function capabilities.

ISO/IEC 27001:2022 certification provides organizations a formal, third-party-validated mechanism to demonstrate architectural maturity to customers, regulators, and business partners. Its Annex A control structure maps directly to NIST SP 800-53 Rev. 5 control families, meaning organizations can satisfy both frameworks through a single integrated program. For students entering the cybersecurity profession, security architecture competencies are among the highest-demand skills in the industry, the (ISC)² Cybersecurity Workforce Study consistently identifies Security Architecture as a critical skill gap in enterprise security teams. Roles such as Security Architect, Cloud Security Architect, and Zero Trust Architect represent some of the most strategically impactful positions in the field.

In Class 28, you will step into the operational role of a Security Operations Center analyst. You will analyze real-format logs, apply the SIEM correlation concepts we introduced in this lecture, and practice the incident triage and containment decision-making that applies our NIST CSF DETECT and RESPOND functions. This hands-on laboratory will directly prepare you for Class 29's risk assessment project and the final capstone in Class 30. Thank you, and I will see you in the next class.
:::

%%%
---
unit: Case Study
code: TARGET
title: Case Study, The 2013 Target Breach
---
:::callout style=soft
The Target breach is one of the most studied examples of **architectural failure**: every individual tool worked, but the organization lacked the process architecture to act on the signals those tools generated.
:::

:::steps
**Phase 1 – Initial Access via Vendor Credentials:** Attackers spear-phished a third-party HVAC vendor (Fazio Mechanical) and stole their remote access credentials. Target's network allowed vendor remote access directly to the corporate network rather than isolating it in a restricted vendor zone.
**Phase 2 – Lateral Movement:** From the vendor foothold, attackers moved laterally to Target's internal point-of-sale (POS) network, a segment that should have been isolated from vendor remote access by firewall rules but was not properly segmented.
**Phase 3 – Malware Deployment:** Attackers deployed "BlackPOS" malware to POS terminals that scraped payment card data from RAM before encryption occurred (a RAM-scraping attack). The malware was correctly flagged by Target's FireEye security system.
**Phase 4 – Alert Ignored:** Target's Bangalore-based SOC received FireEye alerts but did not escalate them to the Minneapolis security team. The SIEM was configured to suppress automatic remediation. No human action was taken despite four separate automated alerts over six days.
**Phase 5 – Exfiltration:** 40 million credit card numbers and 70 million customer records were exfiltrated to attacker-controlled servers. The breach was ultimately discovered by the U.S. Department of Justice, not by Target's own detection systems.
:::

:::image src="images/27_target_breach_timeline.png" alt="Horizontal attack timeline with five labeled phases above a timeline bar: Phase 1 (November 12, 2013) labeled 'Vendor credential theft' with a phishing email icon; Phase 2 (November 15-27) labeled 'Lateral movement to POS network' with a network path icon; Phase 3 (November 27) labeled 'BlackPOS malware deployed, FireEye alert fires' with a warning triangle icon; Phase 4 (November 27 - December 12) labeled 'Alerts suppressed and ignored, 6-day window' with a muted bell icon; Phase 5 (December 13) labeled 'DOJ notifies Target, 40M cards compromised' with a police badge icon; a red bracket spanning Phases 3-5 is labeled 'Architectural failure: detection without response'" caption="Target's breach timeline: the attack was detected six days before exfiltration completed, but no action was taken. The failure was not technical, it was architectural: no process existed to escalate and act on the detection system's alerts." width=full
:::

:::notes
The 2013 Target retail breach is perhaps the most pedagogically valuable case study in security architecture failure because it illustrates a specific and critically important lesson: having security tools is not the same as having a security architecture. Target had invested heavily in sophisticated security technology, including a FireEye malware detection system that cost millions of dollars and was widely regarded as one of the most capable detection platforms available at the time. That system worked exactly as designed. It detected the BlackPOS malware on POS terminals and generated alerts. The breach happened anyway. The failure was entirely architectural.

Let us trace the attack from the beginning. In November 2013, attackers launched a spear-phishing campaign targeting Fazio Mechanical Services, a small Pennsylvania-based refrigeration and HVAC contractor that serviced Target locations. Fazio employees used their Target-provided remote access credentials to submit invoices and manage refrigeration monitoring through Target's Ariba vendor portal. The attackers stole these credentials using the Citadel banking trojan, a variant of Zeus.

The first architectural failure point is visible here: Target had granted a third-party vendor direct remote access to its corporate network without placing that access in an isolated vendor network segment. NIST SP 800-53 control SA-9 (External Information System Services) and CA-3 (System Interconnections) both require that third-party access be subject to security requirements equivalent to internal access, and explicitly recommend network isolation for vendor connections. Target did not implement this segregation. Once the attackers had Fazio's credentials, they were on Target's corporate network with relatively open access.

From that corporate network foothold, the attackers moved laterally to discover and reach Target's point-of-sale network, the internal segment that processes payment card transactions at retail terminals. This movement should not have been possible if proper network microsegmentation had been implemented. POS systems should exist in a highly restricted network zone with no inbound connectivity from corporate network segments and no outbound connectivity except to the payment processor. NIST SP 800-53 SC-7 (Boundary Protection) and PCI DSS Requirement 1.3 (Prohibit direct public access between the internet and the cardholder data environment) both directly address this segregation requirement. Again, Target's implementation had gaps.

On November 27, Thanksgiving Day, the single busiest shopping day of the year, the attackers deployed BlackPOS malware to approximately 1,800 Target POS terminals. BlackPOS is a RAM-scraping malware that reads payment card data from the terminal's memory during the brief window between card swipe and encryption, when the card number exists in plain text in RAM. This is a known attack category documented in CVE-2008-0688 class advisories and widely discussed in PCI security literature.

Target's FireEye system detected the BlackPOS malware installation within hours and generated alerts that were routed to Target's security operations center in Bangalore. The Bangalore SOC forwarded the alerts to Target's Minneapolis security team. What happened next represents the most significant architectural failure: nothing. The Minneapolis team did not act on the alerts. Target's FireEye deployment was configured in a mode where automatic remediation was disabled, a decision made to prevent false positives from disrupting retail operations during peak periods. This meant that human action was required to contain the threat, but no process existed to ensure that high-severity alerts received timely human response. Over six days, four separate FireEye alert escalations were ignored.

The breach was ultimately discovered not by Target's internal systems but by the U.S. Department of Justice, which contacted Target on December 12 after detecting card data appearing on criminal marketplaces. By that point, approximately 40 million credit and debit card numbers and 70 million customer records containing PII had been exfiltrated. Target eventually spent over $290 million in settlements, remediation, and legal costs, and both the CIO and CEO resigned.

The architectural lessons are crisp. First, third-party access must be isolated in a dedicated vendor network segment with the minimum necessary access, not attached to the general corporate network. Second, network microsegmentation must prevent POS systems from being reachable from corporate network zones. Third, detection systems are only valuable if the organizational architecture ensures alerts are reviewed, escalated, and acted upon within defined time windows. A SIEM with no incident response process is expensive noise. NIST SP 800-61 (Computer Security Incident Handling Guide) provides the process framework for ensuring detection events receive appropriate human response.

Target's failures map onto the NIST CSF functions: the vendor-access failure to Identify (asset inventory) and Protect (access management), the flat POS network to Protect (segmentation), and the suppressed alerts to Detect (anomaly detection) and Respond (incident response). The mapping makes the framework concrete.
:::

%%%
---
unit: Case Study
code: SOLAR
title: Case Study, The 2020 SolarWinds Supply Chain Attack
---
:::callout style=soft
The SolarWinds attack demonstrated that trusted software update channels can become attack vectors. It exploited **implicit trust** in vendor software, a foundational assumption that Zero Trust Architecture is specifically designed to eliminate.
:::

::::columns ratio=1:1
::col::
::::card heading="Attack Vector"
:::list style=tight
- **Supply Chain Compromise:** Attackers (APT29/Cozy Bear) inserted SUNBURST malware into the SolarWinds Orion software build pipeline.
- **Trusted Update:** The malicious update was cryptographically signed by SolarWinds and delivered through legitimate update channels to ~18,000 organizations.
- **Delayed Activation:** SUNBURST remained dormant for 12–14 days before activating, evading sandbox analysis.
:::
::::
::col::
::::card heading="Impact & Scale"
:::list style=tight
- **Victims:** U.S. Treasury, Commerce, Homeland Security, State Department, and dozens of Fortune 500 firms.
- **Duration:** Attackers had access for 8–9 months before discovery.
- **Discovery:** Discovered by FireEye, not by any government agency, when attackers tried to steal FireEye's own red team tools.
:::
::::
::::

:::table
| Architectural Lesson | NIST Control | ZTA Mitigation |
|---|---|---|
| Software updates are a trusted attack vector | SI-7: Software Integrity Verification | Code signing + build pipeline integrity attestation |
| Implicit network trust enabled lateral movement | SC-7: Boundary Protection | Microsegmentation, no implicit east-west trust |
| Privileged credentials used for persistence | AC-6: Least Privilege | PAM with just-in-time access; no standing privileges |
| Months before detection | SI-4: System Monitoring | UEBA baseline deviation alerts; cloud access anomaly detection |
:::

:::image src="images/27_solarwinds_supply_chain.png" alt="Flow diagram of the SolarWinds supply chain attack: leftmost box labeled 'SolarWinds Build Server' with a code file icon, attacked by a threat actor figure inserting a malicious code block labeled 'SUNBURST backdoor'; an arrow labeled 'Code signing (legitimate certificate)' leads to a 'Software Update Package' box; multiple arrows fan out from the update package to boxes labeled 'U.S. Treasury', 'DHS', 'FireEye', 'Fortune 500' representing victim organizations; inside each victim box, a dotted path shows SUNBURST communicating outbound to a C2 server labeled 'avsvmcloud.com'; a red lock icon marks the 8-month dwell time label" caption="The SolarWinds attack chain: the malicious code was inserted before the legitimate build and signing process, meaning victims received a cryptographically valid update containing a backdoor. The attack exploited organizational trust in vendor software, the exact assumption Zero Trust Architecture rejects." width=full
:::

:::notes
The SolarWinds supply chain attack, attributed to Russia's Foreign Intelligence Service (SVR) and the APT29 threat group (also known as Cozy Bear), represents one of the most sophisticated and architecturally significant cyberattacks in history. It was publicly disclosed in December 2020 after cybersecurity firm FireEye discovered that its own red team tools had been stolen. The attack's significance for security architecture education is that it exploited a category of implicit trust that most organizations' security architectures are entirely unprepared to address: trust in software vendors.

The attack began at SolarWinds' software development environment, likely in late 2019 or early 2020. The attackers compromised the Orion software build pipeline, the automated process that compiles, packages, and signs SolarWinds' network management software. They injected a sophisticated backdoor called SUNBURST into the Orion software's source code. Because the attackers modified the code at the build stage rather than tampering with distribution packages, the resulting software update was legitimately compiled, legitimately tested, and legitimately signed with SolarWinds' own cryptographic certificate. Nothing about the update appeared malicious from a traditional signature verification perspective.

Between March and June 2020, approximately 18,000 organizations downloaded the malicious Orion update through SolarWinds' normal software update channel. SUNBURST incorporated several sophisticated evasion techniques. It remained dormant for 12 to 14 days after installation before activating, which allowed it to survive sandbox analysis environments that typically run samples for only 24 to 72 hours. It communicated with command-and-control infrastructure using a domain generation algorithm (DGA) that produced subdomain names mimicking legitimate Orion network traffic patterns, making the outbound C2 communication difficult to distinguish from normal telemetry.

Once active, SUNBURST gave the attackers a persistent backdoor on victim networks, which they used to deploy a second-stage payload called TEARDROP to drop Cobalt Strike beacons for hands-on-keyboard access. The attackers then used legitimate credentials, tools, and protocols to move laterally through victim networks over a period of months, a technique specifically designed to blend in with normal administrative activity and evade behavioral detection systems looking for unusual processes or tools.

The architectural lessons from SolarWinds are profound and directly map to Zero Trust principles. First, software supply chains must be treated as potential attack vectors. NIST SP 800-161 Rev. 1, Cybersecurity Supply Chain Risk Management Practices, provides guidance on assessing and managing third-party software risk. SI-7 (Software, Firmware, and Information Integrity) in NIST SP 800-53 requires verifying the integrity of software before installation, but this verification must extend beyond simply checking the vendor's signature to include build pipeline attestation, reproducible builds, and software bill of materials (SBOM) validation.

Second, the lateral movement phase of the attack exploited implicit internal network trust, the castle-and-moat assumption. In a properly implemented Zero Trust Architecture, the SUNBURST backdoor's ability to move laterally would be severely constrained. Each connection attempt would require authentication and authorization, and anomalous connections from an Orion server to sensitive internal systems (Treasury workstations, email servers, source code repositories) would be blocked or flagged by the Policy Decision Point before they could succeed.

Third, the eight-to-nine-month dwell time before discovery reflects a fundamental DETECT function failure. User and Entity Behavior Analytics (UEBA) systems trained on baseline behavioral patterns for service accounts and network flows should have flagged the unusual communication patterns and credential usage. NIST SP 800-53 SI-4 (System Monitoring) and the NIST CSF DETECT function DE.CM-1 (Networks and network services are monitored) directly address this gap. Cloud Access Security Brokers (CASBs) monitoring identity provider logs should have flagged the unusual OAuth token usage that attackers exploited to access Microsoft 365 and Azure environments.

Executive Order 14028, signed in May 2021 in direct response to the SolarWinds attack, mandated Zero Trust Architecture adoption across the U.S. federal government and established requirements for software supply chain security, including SBOM requirements. This represents the most direct policy acknowledgment that perimeter-centric architectures are insufficient for modern threat environments.

SolarWinds motivates the "assume breach" tenet of Zero Trust: designing as though attackers are already inside with valid credentials surfaces microsegmentation, user-behavior analytics and privileged access management as the central defensive responses.
:::

%%%
---
unit: Deep Dive
code: SIEM
title: Tool Spotlight, SIEM Architecture & Operations
---
:::callout style=soft
A **Security Information and Event Management (SIEM)** platform is the central nervous system of a Security Operations Center. It aggregates, correlates, and analyzes log data from across the enterprise to detect threats that no single source would reveal.
:::

:::flow
Log Sources: Firewalls, EDR agents, Active Directory, cloud APIs, DNS, web proxies, and application logs feed normalized event data into the SIEM pipeline.
Normalization: Raw logs in different formats (syslog, CEF, LEEF, JSON) are parsed and mapped to a common schema, typically the Common Event Format or an internal taxonomy.
Correlation Engine: Rules and ML models cross-reference events from multiple sources. Example: "User from HR subnet performing RDP to 50 hosts in 60 seconds" triggers a lateral movement alert.
Alert Triage: SOC analysts review alerts with contextual enrichment (threat intel feeds, asset value, user role) and classify events as true positive, false positive, or investigation needed.
Incident Response: Confirmed true positives are escalated to the RESPOND workflow, containment, forensic preservation, and notification procedures begin.
:::

:::image src="images/27_siem_architecture.png" alt="SIEM architecture diagram with five vertical columns: Column 1 labeled 'Log Sources' contains icons for firewall, endpoint, Active Directory, cloud platform, DNS; arrows feed right into Column 2 labeled 'Collection & Normalization' with a log aggregator box and schema mapping diagram; arrows feed right into Column 3 labeled 'Correlation Engine' with overlapping rule icons and ML model icon; Column 3 generates alerts flowing into Column 4 labeled 'Alert Triage Queue' showing a queue of prioritized alerts with severity labels; Column 5 shows a SOC analyst icon reviewing alerts and two outcome paths: True Positive leading to 'Incident Response' and False Positive leading to 'Rule Tuning'; the entire diagram sits on a footer bar labeled 'Threat Intelligence Feed enriching all stages'" caption="SIEM architecture: log data flows left-to-right from diverse sources through normalization, correlation, and triage into incident response. Threat intelligence enrichment at every stage reduces false positives and accelerates analyst decisions." width=full
:::

:::notes
A Security Information and Event Management platform, universally abbreviated SIEM (pronounced "sim"), is the foundational detection technology in modern Security Operations Centers. Understanding how SIEM works architecturally is essential for both security practitioners and security architects, because the effectiveness of a SIEM deployment depends almost entirely on how it is integrated with the organization's other systems, how its correlation rules are designed, and how its alerts are operationalized into response procedures.

The fundamental problem a SIEM solves is signal-to-noise. A modern enterprise generates millions of log events per day across hundreds of systems. Individually, most of these events are benign and unremarkable. A user logs into Active Directory, normal. A firewall blocks an inbound connection attempt, normal. A web server returns a 404 error, normal. But a user logs in from an unusual geographic location at 3 AM, then immediately begins querying a database they have never accessed before, while a firewall simultaneously blocks an unusual outbound connection to an IP in an Eastern European ASN, individually normal, collectively a strong indicator of credential theft and data exfiltration. The SIEM's correlation engine is specifically designed to detect these multi-event patterns that no single log source would reveal.

The architecture of a SIEM deployment begins with log source integration. The value of a SIEM is directly proportional to the breadth and quality of its log sources. At minimum, a functional SIEM should ingest: Active Directory / identity provider authentication logs (who is authenticating, from where, to what); firewall and network flow logs (what is connecting to what, with what volume and frequency); endpoint EDR agent logs (what processes are running, what files are being accessed, what network connections are being made); DNS query logs (a surprisingly rich source of threat intelligence, since many malware families use DNS for C2 communication); web proxy logs (what URLs are being accessed from corporate endpoints); and cloud platform API logs (AWS CloudTrail, Azure Activity Log, GCP Audit Logs).

Once collected, raw log data must be normalized, parsed from vendor-specific formats and mapped to a common schema. Without normalization, correlation rules cannot work across sources, because a firewall's log entry for a blocked connection uses completely different field names and formats than an Active Directory logon failure. Common normalization frameworks include the Common Event Format (CEF), the LEEF format used by IBM QRadar, and the Common Information Model (CIM) used by Splunk. Many SIEMs now also support the OCSF (Open Cybersecurity Schema Framework), an open standard launched in 2022 by AWS, Splunk, and other major vendors.

The correlation engine is the intelligence core of the SIEM. It applies rules and models to normalized events to identify patterns indicative of specific attack techniques. Rule-based correlations are explicit logical conditions: "Generate a HIGH alert if a single source IP attempts to authenticate to more than 10 different accounts within 5 minutes (password spray detection)" or "Generate a CRITICAL alert if an endpoint initiates a connection to an IP listed in the threat intelligence feed while the user account associated with that endpoint has not authenticated in the past 30 days (possible zombie endpoint)." These rules implement MITRE ATT&CK techniques, the SIEM vendor and SOC team map correlation rules to specific ATT&CK tactic and technique IDs, ensuring comprehensive coverage.

Modern SIEMs augment rule-based detection with ML-based User and Entity Behavior Analytics (UEBA). UEBA establishes behavioral baselines for individual users and devices over time, what systems does this user typically access, at what times, from what locations, using what protocols, and flags deviations from baseline as anomalous. This is particularly valuable for detecting insider threats and credential theft where the attacker is using a legitimate account, because their behavior (accessing unusual systems, downloading large data volumes, connecting at unusual hours) deviates from the account owner's baseline even if the credentials are valid.

Alert triage is the operational process where SIEM value is most commonly lost. A poorly tuned SIEM may generate thousands of alerts per day, overwhelming the SOC team and resulting in alert fatigue, where analysts begin dismissing alerts without careful review, potentially missing true positives among the noise. NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide) provides guidance on triage processes, establishing four triage categories: Not an Incident, False Positive, True Positive with Low Priority, and True Positive requiring Immediate Response. SOAR platforms (covered in a later slide) automate portions of the triage process to reduce analyst burden.

SIEM platforms commonly evaluated by enterprises include Splunk Enterprise Security, Microsoft Sentinel (cloud-native), IBM QRadar, Elastic SIEM, and Securonix. NIST SP 800-92 (Guide to Computer Security Log Management) provides foundational guidance on log source identification, log retention policies, and SIEM architecture design principles.

A SIEM that does not ingest Active Directory logs is blind to most credential-theft, privilege-escalation and lateral-movement detection, because those use cases depend on AD events. SIEM effectiveness is therefore as much about comprehensive, high-quality log-source coverage as about the platform itself.
:::

%%%
---
unit: Deep Dive
code: ZTA2
title: Microsegmentation, Zero Trust Network Design
---
:::callout style=soft
**Microsegmentation** is the network implementation of Zero Trust, dividing the internal network into isolated security zones enforced at the workload level rather than at the perimeter. It contains breaches and prevents lateral movement.
:::

::::columns ratio=1:1
::col::
::::card heading="Traditional Flat Network"
:::list style=tight
- Single VLAN or broad subnets span entire buildings or business units
- East-west traffic between hosts unrestricted
- One compromised host can reach every other host on the segment
- Lateral movement is rapid, minutes to scan entire subnet
:::
::::
::col::
::::card heading="Microsegmented Network"
:::list style=tight
- Each workload or application tier is isolated in a dedicated segment
- East-west traffic requires explicit policy authorization
- Compromised host can only reach explicitly permitted destinations
- Lateral movement is blocked or severely constrained
:::
::::
::::

:::table
| Microsegmentation Approach | Granularity | Implementation | Use Case |
|---|---|---|---|
| VLAN-based | Subnet level | Network switches | Legacy datacenter segmentation |
| Firewall Zones | Zone level | Perimeter/internal firewalls | DMZ and major tier separation |
| Software-Defined Networking (SDN) | Workload level | Overlay network (VMware NSX, Cisco ACI) | Cloud and virtualized datacenter |
| Host-Based Firewall | Process level | OS firewall (iptables, Windows Firewall) | Container and microservice environments |
:::

:::image src="images/27_microsegmentation_design.png" alt="Side-by-side network diagram: left side shows a flat network with all workstations, servers, and database in one large box labeled 'Corporate LAN VLAN 10' with double-headed arrows between all nodes labeled 'Unrestricted east-west traffic'; a red attacker figure on one workstation has arrow paths reaching all other nodes; right side shows microsegmented network with separate boxes for 'User Workstations Segment', 'Web Tier Segment', 'App Tier Segment', 'DB Tier Segment', each separated by firewall icons; arrows between segments are labeled 'Explicit policy required'; the attacker figure on one workstation is blocked from reaching App Tier and DB Tier by red X marks on the firewall barriers" caption="Microsegmentation eliminates the flat-network attacker advantage. In a flat network (left), one compromised workstation can reach all resources. In a microsegmented network (right), the same compromise is contained to the workstation's segment, and lateral movement requires defeating additional independent policy controls." width=full
:::

:::notes
Microsegmentation is the operational heart of Zero Trust network implementation, and it is the most direct architectural response to the lateral movement problem that enabled breaches like Target and SolarWinds. To understand why microsegmentation is so impactful, we need to understand what it replaces: the flat network.

In a flat network architecture, which remains common in enterprise environments today, particularly in older datacenters and mid-market organizations, hosts within a subnet or VLAN can communicate with each other freely using any protocol and any port. A Windows workstation can establish a TCP connection to a database server on the same VLAN without any intervening control checking whether that connection is authorized. If an attacker compromises that workstation through phishing, drive-by download, or physical access, they immediately inherit that same ability: they can connect to any host on the subnet, run port scans to discover what is reachable, and attempt to exploit vulnerabilities on every discovered host. This "east-west" movement within the network, as distinct from "north-south" movement between internal and external zones, is the mechanism attackers use to move from a low-value initial foothold to high-value targets like domain controllers, database servers, and backup systems.

The attacker's advantage in a flat network is speed and coverage. Automated tools like Mimikatz (for credential extraction), BloodHound (for Active Directory relationship mapping), and Metasploit (for exploit delivery) allow attackers to move from initial workstation compromise to domain controller compromise in minutes. NIST SP 800-53 SC-7(21) explicitly requires separation of user functionality from system management functionality, and SC-4 (Information in Shared Resources) requires preventing unauthorized sharing of information between processes. These controls translate architecturally into network segmentation requirements.

Microsegmentation solves this problem by enforcing access policy at the workload level, ideally at the host-based firewall or at a software-defined networking layer, such that east-west communication between workloads requires explicit policy authorization. In a microsegmented architecture, even if two workloads exist in the same physical datacenter and on the same physical switching infrastructure, they cannot communicate unless there is an explicitly defined policy rule permitting that communication. A workstation cannot reach a database server unless there is a rule stating "workstations in the Finance VLAN may connect to TCP port 5432 on database server DB-FINANCE-01." Any other connection attempt is blocked by default (fail-safe defaults principle applied at the network layer).

The implementation technology varies by environment. In legacy datacenter environments, VLAN segmentation using managed switches provides basic zone-level separation. Internal firewalls between zones (as in the DMZ architecture discussed earlier) enforce inter-zone policy. These approaches provide useful segmentation at a coarse granularity, separating major tiers like web, application, and database, but cannot enforce workload-level policies within a tier.

For more granular control, Software-Defined Networking (SDN) platforms like VMware NSX provide microsegmentation capabilities at the virtual machine level. NSX implements distributed firewalling at the virtual network interface card (vNIC) of each virtual machine, meaning that every connection between VMs is evaluated against policy regardless of whether those VMs are on the same physical host or different hosts. This enables policy enforcement at the individual workload level without requiring physical network changes.

In container and microservice environments, Kubernetes Network Policies, service meshes (Istio, Linkerd), and eBPF-based tools (Cilium) provide process-level and service-level microsegmentation. Each microservice can be assigned a policy that permits it to communicate only with the specific other services it legitimately depends on, implementing true zero-trust communication between components of a distributed application.

The operational challenge of microsegmentation is policy management. In a large enterprise with hundreds or thousands of workloads, maintaining explicit allow-list policies for every legitimate communication path is a significant engineering effort. Organizations typically begin by mapping existing traffic flows using network flow analysis tools (NetFlow, IPFIX), then progressively tightening policies as they gain confidence in their traffic maps. Starting with the most sensitive assets (databases, domain controllers, backup systems) and working outward is the recommended approach.

NIST SP 800-125B (Secure Virtual Network Configuration for Virtual Machine (VM) Protection) provides guidance specifically applicable to SDN-based microsegmentation in virtualized environments, and is a recommended reference for students interested in cloud and datacenter security architecture.
:::

%%%
---
unit: Deep Dive
code: IAM
title: Identity & Access Management Architecture
---
:::callout style=soft
**Identity is the new perimeter.** As traditional network boundaries dissolve, the identity of the user or service making a request becomes the primary control point for access decisions in Zero Trust environments.
:::

:::steps
**Identity Governance:** Establish authoritative identity sources (Active Directory, Okta, Azure AD), define role taxonomies aligned to business functions, and implement lifecycle management processes for user provisioning, modification, and de-provisioning.
**Authentication Strength:** Deploy phishing-resistant MFA across all user and administrative accounts. Prioritize FIDO2/WebAuthn hardware tokens or passkeys for privileged users. Enforce contextual step-up authentication for sensitive resources.
**Authorization:** Implement Role-Based Access Control (RBAC) for broad entitlement assignment and Attribute-Based Access Control (ABAC) for fine-grained, context-dependent authorization. Regularly conduct access reviews (entitlement recertification) to prune unused or excessive rights.
**Privileged Access Management (PAM):** Vault all privileged credentials in a PAM solution (CyberArk, BeyondTrust, Delinea). Issue just-in-time, time-limited administrative sessions with session recording. No standing privileged accounts.
**Federation & Single Sign-On:** Implement SAML 2.0 or OIDC-based SSO to centralize authentication across SaaS applications, reducing credential sprawl while enabling central visibility and control over all authentication events.
:::

:::image src="images/27_iam_architecture.png" alt="IAM architecture diagram with four horizontal tiers: Tier 1 at top labeled 'Identity Sources' shows Active Directory, HR System, and Cloud Directory icons feeding into a central Identity Provider box; Tier 2 labeled 'Authentication' shows MFA policy engine with FIDO2 token, mobile push, and SMS icons with a policy decision diamond; Tier 3 labeled 'Authorization' shows RBAC roles mapping to resource access permissions and an ABAC policy evaluation box checking user attributes vs resource sensitivity; Tier 4 at bottom labeled 'Protected Resources' shows icons for SaaS apps, on-premises servers, cloud workloads, and APIs; a separate box on the right labeled 'PAM Vault' connects to privileged access paths with a session recording icon" caption="IAM architecture: identity sources feed an Identity Provider that enforces MFA at authentication and RBAC/ABAC at authorization. PAM vaults privileged credentials separately. All authentication events are logged to SIEM for behavioral analysis." width=full
:::

:::notes
In the perimeter-centric security model, network location was the primary access control mechanism: being on the corporate network was taken as evidence of legitimacy. As the network perimeter has dissolved through cloud computing, remote work, SaaS adoption, and mobile devices, identity has emerged as the primary, and in many architectures, the only, control point that is consistently present regardless of where users and resources are located. This is why security professionals say "identity is the new perimeter."

Identity and Access Management (IAM) architecture is the systematic design of systems and processes that manage who can access what, under what conditions, and how those decisions are enforced and audited. Poor IAM architecture is implicated in a substantial majority of significant breaches: the Verizon Data Breach Investigations Report (DBIR) consistently reports that compromised credentials are involved in approximately 80% of confirmed breaches. This statistic reflects the fact that stealing a credential is often much easier than exploiting a technical vulnerability, and once credentials are stolen, the attacker impersonates a legitimate user and may evade detection indefinitely.

A complete IAM architecture addresses five components. Identity governance begins with having authoritative sources of truth for identity: typically an on-premises directory service like Microsoft Active Directory, combined with a cloud identity provider like Okta, Azure Active Directory (now Entra ID), or Google Workspace. Organizations that operate without authoritative identity sources, allowing individual application administrators to create local accounts, or relying on manual processes for provisioning and de-provisioning, inevitably accumulate orphaned accounts (accounts of former employees that were never disabled), over-privileged accounts, and shadow IT identities that exist outside any governance process.

Authentication strength is the quality of the mechanism used to verify identity claims. Passwords alone are the weakest acceptable authentication factor, and they should not be used without MFA for any account with access to sensitive systems. NIST SP 800-63B (Digital Identity Guidelines) defines authentication assurance levels: AAL1 permits single-factor authentication for low-sensitivity applications; AAL2 requires multi-factor authentication; AAL3 requires hardware-based cryptographic authenticators for the highest-sensitivity applications. FIDO2/WebAuthn hardware security keys, like YubiKey, are the gold standard for phishing-resistant MFA at AAL3, because they bind the authentication credential to the legitimate origin URL, making them immune to credential-phishing attacks. NIST specifically recommends phishing-resistant authenticators in OMB Memorandum M-22-09, which drove the U.S. federal government's Zero Trust implementation mandates.

Authorization, the question of what an authenticated user is permitted to do, is implemented through two primary models. Role-Based Access Control (RBAC) assigns users to roles (Finance Analyst, Network Administrator, HR Manager), and roles are granted specific permissions. RBAC is manageable at scale and aligns well with organizational structure, but it can produce over-privileged access when a user's role grants more permissions than their specific job requires. Attribute-Based Access Control (ABAC) evaluates dynamic policies that consider multiple attributes simultaneously: the user's role, their current device's security posture, the sensitivity classification of the requested resource, the time of day, and the geographic location of the request. ABAC enables the dynamic, context-aware access decisions that Zero Trust requires but is more complex to implement and manage than RBAC. Most mature IAM architectures use both: RBAC for broad entitlement assignment and ABAC for fine-grained policy enforcement at sensitive resources.

Privileged Access Management is the specialized discipline of securing administrative credentials, the accounts with elevated privileges that, if compromised, give attackers the ability to modify systems, create accounts, disable logging, and exfiltrate data at scale. PAM solutions vault privileged credentials in an encrypted password safe, issue time-limited just-in-time sessions to administrators, and record all privileged sessions for forensic review. The principle is that no administrator should have a permanent standing privilege to log into production systems, they should request access, receive a time-limited credential, complete their task, and have the credential automatically rotated after the session ends. NIST SP 800-53 AC-17 (Remote Access), AC-2 (Account Management), and IA-5 (Authenticator Management) all directly address PAM requirements.

Single Sign-On using SAML 2.0 or OpenID Connect (OIDC) federated identity protocols reduces credential sprawl by centralizing authentication through the identity provider. Instead of each SaaS application maintaining its own user database and password store, every application delegates authentication to the central IdP. This provides three benefits: administrators can de-provision access to all applications simultaneously by disabling the central account; all authentication events are visible in a single log source for SIEM analysis; and users experience fewer friction points, which reduces password reuse and shadow IT workarounds.

In the 2022 Okta breach, attackers compromised a support engineer's workstation and used it to reach Okta's support tools, affecting customers including Cloudflare, Twilio and DoorDash. Even an identity provider must apply Zero Trust to its own internal access, with no implicit trust for privileged support staff.
:::

%%%
---
unit: Deep Dive
code: PAM
title: Privileged Access Management (PAM) Deep Dive
---
:::callout style=soft
**Privileged accounts** are the crown jewels of enterprise security. Administrative credentials can bypass most security controls, PAM architecture treats privileged access as a time-limited exception, not a standing entitlement.
:::

::::columns ratio=1:1
::col::
::::card heading="The Privileged Account Risk"
:::list style=tight
- **Blast Radius:** A compromised domain admin can create accounts, disable logging, and move to any system
- **Credential Theft Targets:** Mimikatz, Pass-the-Hash, and DCSync attacks specifically harvest privileged credentials
- **Standing Access:** Most orgs have hundreds of service accounts with permanent admin rights that never expire
- **Shared Passwords:** Teams sharing generic "admin" passwords create unattributable forensic gaps
:::
::::
::col::
::::card heading="PAM Architecture Controls"
:::list style=tight
- **Password Vaulting:** All privileged credentials stored encrypted in a PAM vault (CyberArk, BeyondTrust, Delinea)
- **Just-in-Time (JIT) Access:** Admin credentials issued for specific tasks with automatic expiration and rotation
- **Session Recording:** All privileged sessions video-recorded and keystroke-logged for forensic and audit use
- **Privileged Session Management:** Proxy-based access so admins never see the actual credential
:::
::::
::::

:::image src="images/27_pam_architecture.png" alt="PAM architecture flow diagram: a user labeled 'Administrator' submits an access request to a 'PAM Vault' box; the PAM vault checks an 'Approval Workflow' box (which may require manager approval for sensitive systems); upon approval, the PAM vault issues a time-limited session credential and establishes a 'Privileged Session Manager' proxy connection to the target server; a 'Session Recording' box captures all activity; an automatic 'Credential Rotation' process runs after session termination, changing the server password so the credential the admin received is now invalid; all events flow to a 'SIEM / Audit Log' box; a clock icon shows the session expiration timer" caption="PAM workflow: administrators request access through the vault, which enforces approval workflows, issues time-limited credentials, proxies the session for recording, and automatically rotates credentials after session termination, ensuring no standing privileges exist." width=full
:::

:::notes
Privileged accounts represent the highest-risk identity class in any enterprise environment. A Domain Administrator in an Active Directory environment can create user accounts, modify group memberships, disable audit logging, dump the NTDS.dit credential database, and push group policy changes to every Windows system in the organization. A cloud IAM administrator with sufficient permissions can create new API keys, modify S3 bucket permissions, and exfiltrate data from any cloud resource. A database administrator can read, modify, or delete any data in the database, create new accounts, and disable database-level auditing. These accounts are, by design, extremely powerful, and that power makes them the primary target of sophisticated attackers.

The threat model for privileged credentials is well-documented. Mimikatz, an open-source credential extraction tool originally published by Benjamin Delpy in 2011, can extract plaintext credentials and Kerberos ticket data from Windows memory (specifically the LSASS process) on any machine where the operator has local administrator access. Pass-the-Hash and Pass-the-Ticket attacks use these extracted credentials to authenticate as other users without knowing their plaintext passwords. DCSync attacks allow a machine with certain Active Directory replication rights to pull password hashes for all domain accounts from a domain controller, effectively enabling offline cracking of all enterprise credentials. These techniques are widely available, well-documented in the MITRE ATT&CK framework under Credential Access (TA0006), and used routinely in real-world attacks.

The foundational problem that PAM architecture addresses is standing privilege: the configuration where service accounts, shared administrator accounts, or individual named administrator accounts have permanent, persistent privilege that is continuously active regardless of whether it is being used. A service account with permanent Domain Admin rights that runs a scheduled task every night at 2 AM has 23 hours and 55 minutes each day during which its credentials could be stolen and used without the legitimate task running. A network administrator who has permanent privileged access to production switches is a target whenever they are connected to the network, even when they are not performing administrative tasks.

Just-in-Time (JIT) access is the PAM mitigation. Instead of granting standing privilege, JIT access requires administrators to explicitly request elevated access for a specific task, with a defined justification and a time limit. The PAM vault approves the request (optionally requiring manager approval for sensitive systems), issues a temporary credential or session, and automatically revokes and rotates the credential when the time limit expires. At no point does the administrator know the actual privileged credential, they access the target system through a PAM session proxy that injects the credential transparently. This means that even if the administrator's workstation is compromised, the attacker cannot steal a credential they have never seen.

Session recording provides forensic accountability for all privileged activity. Every privileged session is recorded as a video-like session replay and keystroke log, stored in a tamper-evident audit repository. If an incident occurs that involved privileged account activity, forensic investigators can replay exactly what was done, when, and by whom. This serves both accountability and legal admissibility purposes. NIST SP 800-53 AU-2 (Audit Events) and AU-12 (Audit Record Generation) require audit logging of privileged account activity, and the NIST CSF IDENTIFY function ID.GV-3 (Legal and regulatory requirements regarding cybersecurity, including privacy and civil liberties obligations, are understood and managed) connects PAM audit requirements to regulatory compliance.

Service account management is a particularly neglected area of PAM that deserves specific attention. Service accounts, accounts used by applications, services, and scheduled tasks, often accumulate excessive privileges over time because developers request Domain Admin access "to avoid access errors" rather than identifying the minimum permissions required. They also rarely have password rotation policies, meaning a service account password set five years ago during a developer's tenure may still be valid after that developer left the organization. Group Managed Service Accounts (gMSAs) in Windows environments provide an architecture that automatically manages and rotates service account credentials, eliminating standing service account credentials as an attack vector.

In the 2021 Colonial Pipeline attack, the attackers used a compromised VPN password for an account that had been unused for months but was never de-provisioned. Just-in-time access and account lifecycle management would have removed or flagged that account before it could be used.
:::

%%%
---
unit: Deep Dive
code: CLOUD
title: Cloud Security Architecture, Shared Responsibility
---
:::callout style=soft
Cloud computing does not eliminate security responsibility, it **divides** it. Understanding the Shared Responsibility Model is essential for ensuring that no security gap exists between what the cloud provider secures and what the customer must secure.
:::

:::table
| Responsibility | On-Premises | IaaS (AWS/Azure/GCP) | PaaS | SaaS |
|---|---|---|---|---|
| Physical Security | Customer | **Provider** | **Provider** | **Provider** |
| Hypervisor / Network | Customer | **Provider** | **Provider** | **Provider** |
| Operating System | Customer | **Customer** | Provider | Provider |
| Runtime / Middleware | Customer | Customer | Provider | Provider |
| Application Code | Customer | Customer | **Customer** | Provider |
| Data Classification | Customer | Customer | Customer | **Customer** |
| Identity & Access | Customer | Customer | Customer | **Customer** |
| Network Config (VPC) | Customer | **Customer** | Customer | Provider |
:::

:::callout style=warn
**The Shared Responsibility Gap:** Misunderstandings about this model are the root cause of most cloud breaches. Customers who assume the provider secures everything leave identity, data classification, and network configurations unprotected. Providers secure the cloud infrastructure, customers must secure everything **in** the cloud.
:::

:::image src="images/27_cloud_shared_responsibility.png" alt="Stacked bar chart comparing On-Premises, IaaS, PaaS, and SaaS across a vertical stack of responsibility layers from Physical at bottom to Data/Identity at top; in On-Premises all layers are customer-colored (blue); in IaaS the bottom 3 layers are provider-colored (green) and top 5 are customer-colored; in PaaS bottom 5 layers are provider-colored and top 3 customer-colored; in SaaS all layers except Data and Identity are provider-colored; a red dashed line at the Data and Identity rows spans all four columns labeled 'Always the customer's responsibility'; annotations point to common misconfigurations at the VPC network configuration, IAM permissions, and data encryption layers" caption="The Shared Responsibility Model: provider responsibilities expand from IaaS to SaaS, but data classification and identity management remain the customer's responsibility in all models. The red line marks the layers most commonly misconfigured in cloud breaches." width=full
:::

:::notes
Cloud computing has fundamentally changed the security architecture problem space by introducing a division of security responsibility between the cloud provider and the cloud customer. This division, formalized by each major provider as the Shared Responsibility Model, is well-documented but poorly understood in practice, and misunderstanding it is one of the most consistent root causes of cloud security incidents.

The model works as follows: the cloud provider is always responsible for the security of the cloud, the physical datacenters, the hypervisor layer, the global network infrastructure, and the managed services themselves. The customer is always responsible for security in the cloud, the data they store, the identity and access management policies they configure, the network architecture of their cloud environment (VPC design, security groups, access control lists), and the configurations of cloud services they use.

In Infrastructure as a Service (IaaS) deployments, AWS EC2, Azure Virtual Machines, GCP Compute Engine, the customer is responsible for the operating system (patching, hardening, configuration), any software installed on the OS, application code, and data. The provider is responsible for the physical host, the hypervisor, and the global network fabric. This is the most traditional model, closest to running your own datacenter, but with physical security and hardware maintenance outsourced.

In Platform as a Service (PaaS) deployments, AWS RDS, Azure App Service, GCP App Engine, the provider also manages the OS and runtime environment, leaving the customer responsible only for their application code, data, and access configuration. The customer cannot patch the OS or configure the runtime; the provider handles these automatically. This removes significant operational burden but also removes visibility, the customer cannot install EDR agents on the underlying OS or inspect hypervisor-level logs.

In Software as a Service (SaaS) deployments, Microsoft 365, Salesforce, Google Workspace, the provider manages the application, runtime, OS, and infrastructure. The customer is responsible almost exclusively for data and identity: what data they put into the service, how it is classified and governed, which users have access, and what permissions those users have. Despite how little the customer controls in SaaS environments, misconfigured SaaS access is an enormous source of data breaches, exposed SharePoint sites, misconfigured Google Drive sharing, and over-privileged Salesforce profiles are routine findings in security assessments.

The critical architectural principle is that certain responsibilities never transfer to the cloud provider regardless of the service model: data classification and protection, identity and access management, and compliance obligations. An organization subject to HIPAA does not become HIPAA-compliant by moving to a HIPAA-eligible AWS service, they must still configure access controls correctly, encrypt PHI, enable appropriate audit logging, and sign a Business Associate Agreement (BAA) with AWS. The provider's HIPAA eligibility means their infrastructure meets certain requirements; it does not mean the customer's configuration is compliant.

NIST SP 800-144 (Guidelines on Security and Privacy in Public Cloud Computing) and the Cloud Security Alliance (CSA) Cloud Controls Matrix (CCM) provide frameworks for systematically addressing cloud security requirements across the shared responsibility boundary. The CSA CCM maps controls to specific cloud service models (IaaS/PaaS/SaaS) and identifies which entity (provider or customer) is responsible for each control, a practical tool for cloud security architecture design.

Common misconfigurations that exploit the shared responsibility gap include: S3 buckets configured with public access (customer network configuration responsibility, provider tools like AWS S3 Block Public Access exist but must be explicitly enabled); overly permissive IAM policies using wildcards (customer identity management responsibility); unencrypted databases (customer data protection responsibility); and disabled CloudTrail logging (customer audit configuration responsibility). The 2019 Capital One breach, where a misconfigured AWS Web Application Firewall allowed a server-side request forgery attack to retrieve IAM credentials, which were then used to access millions of customer records in S3, is a canonical example of the shared responsibility gap in practice.

Cloud providers publish their shared-responsibility documentation, AWS its Shared Responsibility Model and Microsoft its Azure Security Benchmark, which set out exactly which controls the provider handles and which remain the customer's, and the boundary differs sharply between SaaS and IaaS.
:::

%%%
---
unit: Framework Detail
code: 80053
title: NIST SP 800-53 Control Families, Deep Dive
---
:::callout style=soft
NIST SP 800-53 Rev. 5 organizes its 1,000+ controls into **20 control families**. Each family addresses a specific domain of security practice and maps to one or more NIST CSF functions, enabling traceability from framework functions to specific technical requirements.
:::

:::table
| Control Family (ID) | Focus Area | Key Controls | CSF Function |
|---|---|---|---|
| Access Control (AC) | Who can access what | AC-2 Account Mgmt, AC-6 Least Privilege, AC-17 Remote Access | PROTECT |
| Audit & Accountability (AU) | Logging & forensics | AU-2 Events, AU-9 Log Protection, AU-12 Generation | DETECT |
| Configuration Mgmt (CM) | Baseline & hardening | CM-2 Baseline Config, CM-6 Settings, CM-7 Functionality | PROTECT |
| Identification & Auth (IA) | Authentication | IA-2 MFA, IA-5 Authenticators, IA-8 Non-Org Users | PROTECT |
| Incident Response (IR) | IR planning & execution | IR-4 Handling, IR-6 Reporting, IR-8 Plan | RESPOND |
| Risk Assessment (RA) | Threat & vuln analysis | RA-3 Risk Assessment, RA-5 Vulnerability Monitoring | IDENTIFY |
| System & Comm Protect (SC) | Network architecture | SC-7 Boundary, SC-28 Data at Rest, SC-8 Transmission | PROTECT |
| System & Info Integrity (SI) | Monitoring & patching | SI-2 Flaw Remediation, SI-3 Malware, SI-4 Monitoring | DETECT |
:::

:::image src="images/27_nist_80053_control_families.png" alt="Circular diagram with 20 segments, each labeled with a NIST SP 800-53 control family abbreviation and name arranged around the perimeter; segments are color-coded by the CSF function they primarily support (blue for PROTECT, yellow for DETECT, green for IDENTIFY, orange for RESPOND, red for RECOVER, dark blue for GOVERN); the center of the circle contains the text 'NIST SP 800-53 Rev. 5' with '1,000+ controls' below; small icons on each segment hint at the domain (lock for AC, camera for AU, gear for CM, person-check for IA, alarm for IR, microscope for RA, network for SC, shield for SI)" caption="NIST SP 800-53 Rev. 5 organizes security controls into 20 families mapped to CSF functions. Understanding which family governs which domain allows architects to identify control gaps and build requirement traceability from business risk to specific technical implementation." width=full
:::

:::notes
NIST Special Publication 800-53 Revision 5, titled "Security and Privacy Controls for Information Systems and Organizations," is the most comprehensive and authoritative catalog of security controls published for U.S. federal information systems, and is widely adopted as a de facto standard across critical infrastructure sectors and large private enterprises. Rev. 5, published in September 2020, introduced significant updates including deeper integration with privacy controls, an increased emphasis on supply chain risk management, and the addition of controls addressing modern threat vectors like cloud computing and mobile devices.

Understanding the structure of SP 800-53 is essential for any security practitioner who designs architectures, conducts risk assessments, or prepares for audits against federal standards like FedRAMP or FISMA. The publication organizes its controls into 20 families, each designated by a two-letter abbreviation and covering a specific security domain. Controls are designated by their family ID and a sequential number, for example, AC-2 is the second control in the Access Control family, which addresses Account Management.

Each control has a base statement, the core requirement, and may have control enhancements that extend the requirement for higher-baseline systems. For example, IA-2 (Identification and Authentication for Organizational Users) at the base level requires that information systems uniquely identify and authenticate users. IA-2(1) enhances this to require multi-factor authentication for privileged accounts, and IA-2(6) further enhances it to require phishing-resistant authenticators for PIV-ineligible environments. Organizations operating at the High baseline under FIPS 199 must implement the base control and most enhancements; Low-baseline systems may implement only the base control.

The Access Control (AC) family is arguably the most foundational, addressing the questions of who is allowed to access what resources under what conditions. AC-2 (Account Management) requires organizations to maintain inventories of authorized accounts, disable accounts for inactive users, and review account privileges regularly. AC-6 (Least Privilege) requires that users and processes operate with the minimum access necessary, directly implementing Saltzer and Schroeder's least privilege principle. AC-17 (Remote Access) governs VPN and remote access configurations, requiring MFA and encrypted transport.

The Audit and Accountability (AU) family governs logging, the foundational input to SIEM and forensic investigation. AU-2 requires identifying the events that must be logged (authentication events, privilege escalation, account creation and deletion, object access for sensitive resources). AU-9 (Protection of Audit Information) requires that log integrity be protected, logs should be shipped to an immutable log storage system as close to real-time as possible, preventing an attacker who gains system access from deleting or modifying local logs to cover their tracks. AU-12 (Audit Record Generation) requires that audit records be generated in a format and with the content fields necessary to establish who did what, when, from where, to what, the who, what, when, where of forensic completeness.

The System and Communications Protection (SC) family governs network architecture. SC-7 (Boundary Protection) is the primary network segmentation control, requiring that managed interfaces control communications at external network boundaries and internal network boundaries, directly implementing the DMZ and microsegmentation architectures we have discussed. SC-28 (Protection of Information at Rest) requires that sensitive information stored on systems be protected through encryption or other cryptographic mechanisms. SC-8 (Transmission Confidentiality and Integrity) requires that information transmitted over networks be protected using TLS or other cryptographic protocols.

NIST SP 800-53B (Control Baselines for Information Systems and Organizations) provides the specific set of controls required at each baseline level (Low, Moderate, High) as defined by the system's security categorization under FIPS 199. FedRAMP, the federal authorization program for cloud service providers, uses the Moderate baseline as its standard authorization requirement, adding cloud-specific control enhancements. Organizations pursuing FedRAMP authorization must implement all Moderate baseline controls and document them in a System Security Plan (SSP).

NIST publishes a mapping between SP 800-53 control families and MITRE ATT&CK techniques: SI-3 (Malicious Code Protection) defends against Initial Access and Execution, AC-6 (Least Privilege) and AC-17 (Remote Access) against Privilege Escalation and Lateral Movement, and AU-2 (Audit Events) enables detection across tactics. The mapping is a practical reference for building control architectures.
:::

%%%
---
unit: Misconceptions
code: MYTH
title: Common Misconceptions, Zero Trust
---
:::callout style=soft
Zero Trust is one of the most misunderstood concepts in enterprise security. Vendor marketing has attached the label to products that do not implement ZTA principles. Understanding what Zero Trust is, and is not, prevents costly misimplementation.
:::

:::table
| Myth | Reality |
|---|---|
| "Zero Trust means zero trust in employees" | ZTA is a network and access architecture principle, not a cultural policy. It means no implicit trust based on network location, employees still need sufficient access to do their jobs. |
| "We're Zero Trust because we bought a ZTNA product" | Zero Trust Network Access (ZTNA) replaces VPN but is only one component. Full ZTA requires identity governance, device health verification, microsegmentation, and continuous monitoring. |
| "Zero Trust eliminates the need for perimeter security" | ZTA reduces reliance on a single perimeter but does not replace all network controls. DMZ architectures and network filtering remain valuable layers in a ZTA environment. |
| "Zero Trust is a product you can buy" | ZTA is an architectural philosophy and design approach. It is implemented through a combination of products, processes, and policies, not a single vendor solution. |
| "Zero Trust is only for large enterprises" | NIST SP 800-207 explicitly states ZTA principles apply to organizations of any size. Cloud-native identity providers and ZTNA solutions make ZTA economically accessible to SMBs. |
| "Once Zero Trust is deployed, we are fully protected" | ZTA reduces attack surface and limits lateral movement; it does not eliminate the risk of breach. Detection and response capabilities remain essential. |
:::

:::image src="images/27_zero_trust_myths.png" alt="Six myth-busting cards arranged in a 2x3 grid; each card has a red 'MYTH' banner at the top with an X icon, the myth statement in italic gray text, a green 'REALITY' banner in the middle, and the corrected explanation in black text below; icons for each card reinforce the concepts: a handshake icon for the employee trust myth, a shopping cart icon for the product myth, a brick wall icon for the perimeter myth, a price tag icon for the purchase myth, a building icon for the size myth, and a shield-with-crack icon for the full-protection myth" caption="Zero Trust myths vs reality: ZTA is an architectural approach, not a product, a culture policy, or a complete solution. Understanding these distinctions prevents organizations from deploying 'Zero Trust' security theater that provides a false sense of protection." width=full
:::

:::notes
Zero Trust has become one of the most heavily marketed terms in cybersecurity, and with that marketing saturation has come significant confusion, misrepresentation, and misimplementation. Organizations are making multi-million dollar purchasing decisions based on vendor claims that their products "deliver Zero Trust," without a clear understanding of what Zero Trust architecture actually requires. This slide addresses the six most common and consequential misconceptions about Zero Trust.

The first and perhaps most culturally charged misconception is that "Zero Trust means zero trust in employees." This misunderstanding can create organizational resistance to ZTA initiatives if employees and managers interpret it as an expression of distrust toward the workforce. Zero Trust is an architectural principle about network access design, not a cultural or management philosophy. It means that the architecture does not grant access based on network location alone, being connected to the corporate WiFi does not automatically grant access to sensitive resources. It has no implication about whether the organization trusts its employees as people; it is about the design of access controls. NIST SP 800-207 defines Zero Trust solely in terms of network architecture and access policy, no reference to organizational culture.

The second misconception is perhaps the most commercially motivated: "We are Zero Trust because we bought a ZTNA product." Zero Trust Network Access (ZTNA) is a class of product that replaces traditional VPN with an application-specific access proxy that requires authentication and device health verification before granting access to each specific application. ZTNA products are a valuable component of ZTA, but they address only the remote access use case. They do not provide microsegmentation of the internal network, device health management for on-premises systems, UEBA monitoring for behavioral anomaly detection, or privileged access management. An organization that deploys a ZTNA product but retains a flat internal network, standing privileged accounts, and no behavioral monitoring has implemented one component of ZTA, not ZTA itself.

The third misconception, that Zero Trust eliminates the need for perimeter security, reflects a common overcorrection. ZTA's "assume breach" tenet does mean that the architecture should not rely on the perimeter as the sole line of defense. But it does not mean that perimeter controls are useless. DDoS mitigation, boundary filtering, and DMZ architectures all retain value in a ZTA environment: they reduce attack surface, absorb volumetric attacks that would otherwise overwhelm internal systems, and provide an additional detection layer. The correct framing is that ZTA eliminates implicit trust based on perimeter position, not that the perimeter is removed entirely.

The fourth misconception, "Zero Trust is a product you can buy", is the core commercial confusion. No single product implements ZTA. ZTA is implemented through a combination of identity governance (IdP, MFA, PAM), device health verification (MDM, EDR), network controls (microsegmentation, ZTNA), and continuous monitoring (SIEM, UEBA). These capabilities may come from multiple vendors or a single platform, but the architecture, how these components interoperate, what policies govern access decisions, and how the PDP/PEP model is implemented, is designed by the organization's security architects, not delivered by a vendor out of the box.

The fifth misconception is that Zero Trust is only accessible to large enterprises. NIST SP 800-207 explicitly notes that ZTA principles are applicable to organizations of any size. Cloud-native identity providers like Okta, Azure Active Directory, and Google Workspace provide sophisticated MFA, conditional access policies, and ZTNA capabilities at price points accessible to SMBs. Cloud-based SIEM platforms with usage-based pricing, cloud-native microsegmentation via security groups and VPC network ACLs, and cloud provider-native PAM services have made ZTA architectures achievable without the on-premises infrastructure investment that was previously required.

The sixth misconception, that ZTA provides complete protection, is the most dangerous because it can lead to reduced investment in detection and response capabilities. Zero Trust dramatically reduces attack surface and limits lateral movement, which reduces the probability and impact of breaches. However, no architecture is impenetrable. Insider threats, zero-day vulnerabilities, and attacks that bypass MFA through SIM swapping or adversary-in-the-middle phishing (as seen in the 2022 Uber breach) can defeat ZTA controls. Detection and response capabilities, SIEM, UEBA, IR planning, remain essential complements to ZTA's preventive controls.

Evaluating a vendor's "Zero Trust" marketing against the NIST SP 800-207 model, identifying which components it addresses, which it does not and what else an organization would need to integrate, exposes how much of a complete ZTA any single product actually provides.
:::

%%%
---
unit: Checkpoint
code: CHK1
title: Mid-Lecture Checkpoint, Architecture Concepts
---
:::callout style=soft
Pause and consolidate. These questions verify that the foundational architecture concepts from the first half of this lecture are clear before we move into advanced topics and case studies.
:::

:::list style=numbered
**Question 1:** A company deploys a next-generation firewall, endpoint MFA, and full-disk encryption on all laptops. Which cell(s) in the NIST control taxonomy are most represented? Which cells are most likely underinvested?
**Question 2:** An attacker gains access to a web server in the DMZ. In a properly implemented Defense in Depth architecture, what prevents them from directly accessing the database server?
**Question 3:** What is the difference between a Policy Decision Point (PDP) and a Policy Enforcement Point (PEP) in NIST SP 800-207's Zero Trust model? Which one evaluates the policy and which one enforces it?
**Question 4:** An organization's NIST CSF Implementation Tier assessment shows they are Tier 2 (Risk-Informed) in their DETECT function but Tier 3 (Repeatable) in PROTECT. What does this imply about their security posture, and what should they prioritize?
**Question 5:** What is the "assume breach" principle of Zero Trust? How does it differ from the underlying assumption of a perimeter-centric security model?
**Question 6:** Name two secure design principles from Saltzer and Schroeder (1975) and give one concrete modern example of each principle applied to cloud architecture.
:::

:::image src="images/27_checkpoint_review.png" alt="Classroom-style quiz card graphic with a pencil and notepad icon at the top; six numbered question boxes arranged in two columns of three; each question box has a light blue background with a small category tag in the upper-left corner (CTRL, DID, ZTA, CSF, ZTA, DSGN respectively); at the bottom, a timer icon with '5 minutes' label and a speech bubble icon labeled 'Discuss with a partner'" caption="Mid-lecture checkpoint: take 5 minutes to answer or discuss these questions before the break. These concepts are foundational to the case studies and advanced topics in the second half of the lecture." width=full
:::

:::notes
This checkpoint is designed for use at approximately the midpoint of the lecture, after covering control taxonomy, Defense in Depth, Zero Trust, and the NIST CSF. It is intended as a five-minute individual or paired reflection activity, not a formal assessment. The goal is to surface conceptual misunderstandings before building on these foundations with the more advanced material in the second half.

Question 1 targets the control taxonomy from the CTRL slide. The correct answer is that the three listed controls, NGFW, endpoint MFA, and full-disk encryption, are all Technical Preventive controls, concentrated in the upper-left cell of the 3x3 matrix. The most likely underinvested cells are Administrative Corrective (no incident response plan mentioned), Technical Corrective (no backups or automated patch management mentioned), and Administrative Preventive (no security awareness training or formal policies mentioned). This question reinforces the insight that organizations systematically over-invest in Technical Preventive controls.

Question 2 tests understanding of Defense in Depth network architecture. The correct answer involves the internal firewall between the DMZ and the internal network segment, which should be configured to permit only specific database protocol traffic (e.g., TCP 3306/5432) from the authorized application server IP address to the database server, and nothing else. A web server in the DMZ has no rule permitting it to connect to the database server; therefore, even if the web server is compromised, the attacker cannot establish a direct database connection. If students mention EDR on the database server or database-level authentication as additional layers, that is an excellent answer demonstrating understanding of multiple independent controls.

Question 3 targets the ZTA architecture from the ZTA slide. The Policy Decision Point (PDP) is the component that evaluates the access policy, it receives the access request context (user identity, device posture, resource sensitivity, time of day) and determines whether to grant or deny access. The Policy Enforcement Point (PEP) is the component that enforces the PDP's decision, it sits inline on the access path and either permits or blocks the actual connection based on the PDP's authorization response. The PDP decides; the PEP enforces.

Question 4 tests CSF implementation tier interpretation. Being Tier 3 in PROTECT means the organization has consistent, formalized preventive controls in place. Being Tier 2 in DETECT means the organization has some detection capability but it is inconsistently applied, monitoring may not cover all systems, alert escalation processes may be informal, and threat intelligence integration may be ad-hoc. The implication is that the organization has invested in prevention but will be slow to detect when preventive controls fail. The priority should be maturing DETECT capabilities: comprehensive log source coverage in SIEM, formal alert triage procedures, UEBA deployment, and documented escalation processes. This directly maps to reducing Mean Time to Detect (MTTD).

Question 5 tests Zero Trust core principles. "Assume breach" means designing the architecture as if attackers are already present inside the network, focusing on limiting lateral movement, detecting adversarial behavior, and protecting high-value assets even from apparently legitimate internal sources. The perimeter-centric model assumes that the perimeter will be successfully defended and that interior traffic is therefore legitimate. Assume breach rejects this assumption as empirically false given the frequency of perimeter breaches.

Question 6 is open-ended and invites examples. Good modern cloud examples include: Least Privilege, an AWS Lambda function should have an IAM role with permissions only to the specific S3 bucket and DynamoDB table it needs, not an AmazonS3FullAccess or AdministratorAccess policy. Fail-Safe Defaults, AWS Security Groups are deny-all by default; no inbound traffic is permitted unless explicitly allowed by a rule, directly implementing fail-safe defaults at the cloud network layer.

:::

%%%
---
unit: Deep Dive
code: THREAT
title: Threat Modeling with STRIDE
---
:::callout style=soft
**Threat modeling** is the structured process of identifying potential threats to a system before building or deploying it. STRIDE provides a mnemonic taxonomy for categorizing threats by type, enabling systematic identification of control requirements.
:::

:::table
| STRIDE Threat | Description | Example | Mitigating Control |
|---|---|---|---|
| **S**poofing | Impersonating a legitimate user or system | Attacker uses stolen credentials to log in as a valid user | MFA, Certificate-based authentication |
| **T**ampering | Unauthorized modification of data or code | SQL injection modifying database records | Input validation, Database integrity checks, Audit logging |
| **R**epudiation | Denying having performed an action | User claims they did not initiate a wire transfer | Non-repudiation logging (AU-9), Digital signatures |
| **I**nformation Disclosure | Exposing data to unauthorized parties | TLS misconfiguration exposes session tokens | TLS 1.3 enforcement, Data classification, Encryption at rest |
| **D**enial of Service | Disrupting availability of a system | Volumetric DDoS attack on web infrastructure | DDoS mitigation, Rate limiting, Auto-scaling |
| **E**levation of Privilege | Gaining higher permissions than authorized | Exploiting a buffer overflow to gain root access | OS hardening, Least privilege, EDR monitoring |
:::

:::image src="images/27_stride_threat_model.png" alt="Central hexagon labeled 'Application / System Under Analysis' surrounded by six satellite boxes arranged in a ring, each representing one STRIDE threat category; the Spoofing box is blue with an impersonator mask icon; Tampering is orange with a wrench-on-data icon; Repudiation is gray with an eraser icon; Information Disclosure is yellow with an open envelope icon; Denial of Service is red with a crossed-out server icon; Elevation of Privilege is purple with an upward-arrow-crown icon; each satellite box has a small arrow pointing toward the central hexagon representing the threat vector, and a second arrow pointing away labeled with the primary mitigating control category" caption="STRIDE threat model: each of the six threat categories targets a different security property (authentication, integrity, non-repudiation, confidentiality, availability, authorization). Systematically applying STRIDE to each component of a system ensures no threat category is overlooked in the control design." width=full
:::

:::notes
Threat modeling is one of the most valuable, and most underutilized, practices in security architecture. It is the process of systematically identifying potential threats to a system, application, or architecture before it is built or deployed, so that controls can be incorporated into the design rather than being retrofitted after a vulnerability is discovered or exploited. The Security Development Lifecycle (SDL) developed by Microsoft in the early 2000s made threat modeling a mandatory phase of software development, and it has since become an industry best practice formalized in NIST SP 800-154 (Guide to Data-Centric System Threat Modeling).

STRIDE is the most widely used threat categorization taxonomy in threat modeling. Developed by Loren Kohnfelder and Praerit Garg at Microsoft in 1999 and published more widely in the SDL, STRIDE provides a mnemonic that ensures threat modelers systematically consider six distinct categories of threat, corresponding to six distinct security properties that a system must protect.

Spoofing attacks target authentication, the ability to verify the identity of a user or system. An attacker who spoofs a legitimate user's identity gains access to resources and can take actions attributed to the victim. Spoofing threats are mitigated by strong authentication mechanisms: multi-factor authentication, certificate-based mutual authentication between services, and binding authentication tokens to the authenticated device to prevent token theft.

Tampering attacks target integrity, the assurance that data and code have not been modified without authorization. SQL injection is a classic tampering attack: the attacker modifies the SQL query being executed against the database by injecting malicious SQL through an input field. Tampering threats are mitigated by input validation, parameterized queries, cryptographic integrity checks (digital signatures, checksums), and audit logging that records data modification events.

Repudiation attacks target non-repudiation, the ability to prove that a specific entity performed a specific action. An attacker or malicious insider may delete or modify logs to deny having performed a harmful action. Non-repudiation is achieved through write-once audit logging (NIST SP 800-53 AU-9 requires log integrity protection), digital signatures that cryptographically bind actions to identities, and multi-party approval workflows that create documented authorization chains.

Information Disclosure attacks target confidentiality, the assurance that data is accessible only to authorized parties. TLS misconfiguration, exposed debug endpoints, overly verbose error messages, and insufficient access controls all create information disclosure vulnerabilities. Encryption in transit (TLS 1.3 minimum), encryption at rest (AES-256), data classification and handling procedures, and least-privilege access controls are the primary mitigations.

Denial of Service attacks target availability, the ability of authorized users to access system resources when needed. Volumetric DDoS attacks, resource exhaustion through algorithmic complexity attacks, and application-layer DoS (e.g., Slowloris) all threaten availability. DDoS mitigation services, rate limiting, connection throttling, auto-scaling infrastructure, and redundant architecture mitigate these threats.

Elevation of Privilege attacks target authorization, the assurance that authenticated users can only perform actions they are explicitly permitted to perform. Buffer overflow exploits, directory traversal vulnerabilities, and misconfigured RBAC policies can all allow an attacker to perform actions at a privilege level above what they are authorized for. OS hardening (removing unnecessary SUID/SGID binaries, applying kernel security features like ASLR and NX), least privilege configuration, input validation, and EDR monitoring for privilege escalation behavior mitigate these threats.

The practical process of threat modeling using STRIDE involves four steps: First, decompose the system into its components (web server, database, authentication service, file storage, APIs, external integrations). Second, identify trust boundaries, the places where data crosses from one trust zone to another. Third, for each trust boundary and each component, enumerate potential STRIDE threats. Fourth, for each identified threat, design or select a mitigating control and verify that the control is included in the system's implementation plan.

Applying STRIDE to each element of an enterprise PII database architecture, the web server, the internal firewall, the database server and the SIEM, and proposing mitigations for the identified threats is the core of a security architecture assessment.
:::

%%%
---
unit: Tool Spotlight
code: SOAR
title: Tool Spotlight, Security Orchestration, Automation & Response (SOAR)
---
:::callout style=soft
**SOAR** platforms extend SIEM capabilities by automating alert triage and response actions. They reduce Mean Time to Respond (MTTR) from hours to minutes by executing predefined playbooks automatically when specific threat patterns are detected.
:::

::::columns ratio=1:1
::col::
::::card heading="SIEM Without SOAR"
:::list style=tight
- Alert fires → analyst receives notification
- Analyst manually queries multiple systems for context
- Analyst manually applies containment (block IP, disable account)
- Documentation created manually post-incident
- Hours per alert, analyst fatigue at high volumes
:::
::::
::col::
::::card heading="SIEM + SOAR"
:::list style=tight
- Alert fires → SOAR playbook executes automatically
- SOAR queries threat intel, asset DB, and user directory for context
- SOAR automatically isolates endpoint, blocks IP, and disables account
- Full investigation timeline auto-documented
- Minutes per alert, analyst reviews outcome, not each step
:::
::::
::::

:::steps
**Trigger:** SIEM correlation rule fires (e.g., "Ransomware behavior detected on endpoint, mass file encryption observed").
**Enrichment:** SOAR queries asset inventory for device owner, business criticality, and network location; queries threat intelligence for known ransomware family IOCs; checks whether device has an active EDR agent.
**Containment:** SOAR automatically isolates the endpoint at the network level (quarantine via EDR API); disables the associated user account in Active Directory; blocks observed malicious IPs at the firewall.
**Notification:** SOAR sends automated notifications to the IR team Slack channel, the device owner's manager, and the IT help desk with full incident context.
**Documentation:** SOAR creates a timestamped incident ticket with all actions taken, enrichment data, and timeline, providing complete audit trail for forensic and compliance purposes.
**Human Review:** SOC analyst reviews the automated response, confirms or reverses containment actions, and proceeds with deeper forensic investigation if warranted.
:::

:::image src="images/27_soar_playbook_flow.png" alt="SOAR playbook flowchart for ransomware response: starting node labeled 'SIEM Alert: Mass File Encryption on EP-HR-042'; first decision diamond labeled 'EDR agent active?' with Yes/No branches; Yes branch leads to action boxes 'Isolate endpoint via EDR API', 'Query asset DB for device criticality', 'Query threat intel for malware family'; No branch leads to 'Dispatch field tech for physical isolation'; after enrichment, a parallel action group shows 'Disable AD account', 'Block C2 IPs at firewall', 'Notify IR team via Slack'; all paths converge to 'Create incident ticket with timeline'; final node is 'Analyst review and confirm'" caption="SOAR ransomware response playbook: from SIEM alert to contained, documented incident in under 5 minutes. Actions that previously required manual analyst effort across multiple consoles execute automatically and in parallel, while the analyst reviews outcomes rather than performing each step." width=full
:::

:::notes
Security Orchestration, Automation, and Response platforms address one of the most critical operational bottlenecks in security programs: the gap between what SIEM systems detect and how quickly human analysts can act on those detections. The Ponemon Institute and IBM's Cost of a Data Breach Report consistently find that Mean Time to Detect (MTTD) and Mean Time to Respond (MTTR) are among the strongest predictors of breach cost, and that the vast majority of the time in both metrics is spent on manual activities that could be automated.

A SOAR platform integrates with the security tool ecosystem, SIEM, EDR, threat intelligence platforms, asset management databases, Active Directory, firewall management interfaces, ticketing systems, and communication platforms, through APIs, and provides a playbook engine that executes predefined response workflows automatically when specific trigger conditions are met. A well-implemented SOAR deployment can reduce MTTR for common incident types from hours to minutes.

The key SOAR capability that most directly reduces analyst burden is automated enrichment. When a SIEM alert fires, say, an account lockout from multiple failed authentication attempts, a SOAR playbook can automatically query the user directory to retrieve the account owner's name and manager, query the asset database to determine what systems the account has access to, query threat intelligence feeds to check whether the source IP has known malicious history, query the VPN logs to determine whether the account is currently connected remotely, and compile all of this context into a single enriched alert card. This enrichment process, which previously took an analyst 15-30 minutes of manual querying across multiple consoles, is completed in seconds. The analyst receives not a raw alert but a fully contextualized incident summary.

Automated containment playbooks provide the most dramatic MTTR reduction for high-confidence threat scenarios. A ransomware detection playbook can automatically isolate an infected endpoint through the EDR API (quarantining it from all network communication except the management channel) in seconds, long before a human analyst has even read the alert. This is particularly valuable for fast-moving threats like ransomware and worm propagation, where every minute of uncontained spread dramatically expands the scope of the incident.

SOAR playbooks are built around the concept of conditional logic and API integrations. The playbook designer defines the sequence of automated actions, decision branches based on enrichment results, and conditions under which the automation should pause for human review. For example, a playbook for blocking an IP address might automatically block the IP at the perimeter firewall for any IP with a threat intelligence confidence score above 90, but require analyst approval for IPs with confidence scores between 50 and 90, preventing false positives from disrupting legitimate traffic.

Commercial SOAR platforms include Splunk SOAR (formerly Phantom), Palo Alto Cortex XSOAR, Microsoft Sentinel (which includes native playbook orchestration through Azure Logic Apps), and IBM Security QRadar SOAR. The NIST CSF RESPOND function (specifically RS.AN, Incident Analysis and RS.MI, Incident Mitigation) directly maps to SOAR capabilities, as does NIST SP 800-61 Rev. 2's requirement for timely incident containment and documented incident handling.

Playbook library standardization is an important operational consideration. Organizations should maintain a library of tested, version-controlled playbooks for the most common incident types they expect to encounter, credential compromise, ransomware detection, data exfiltration alerts, malicious email reporting, and privileged account anomalies. Each playbook should be reviewed and updated periodically as the threat landscape and tool ecosystem evolve, and after each real-world incident where the playbook was used.

SOAR playbooks exist in both commercial platforms and open resources, including Splunk's open-source playbook library and the MITRE CACAO standard for machine-readable, vendor-neutral playbooks. Familiarity with both is useful for SOC engineering roles.
:::

%%%
---
unit: Deep Dive
code: DLP
title: Data Loss Prevention (DLP) Architecture
---
:::callout style=soft
**Data Loss Prevention (DLP)** controls prevent sensitive data from leaving the organization's control through unauthorized channels, email, USB, cloud upload, or web. DLP is the technical implementation of data classification policy.
:::

::::columns ratio=1:1
::col::
::::card heading="DLP Inspection Points"
:::list style=tight
- **Network DLP:** Inspects data at the proxy or firewall as it leaves the network perimeter (email relay, web proxy, API gateways)
- **Endpoint DLP:** Agent installed on endpoints controls USB, clipboard, print, and application-level data transfers
- **Cloud DLP:** CASB or native cloud APIs monitor and control data stored and shared in SaaS platforms (OneDrive, Salesforce, Slack)
- **Email DLP:** Scans outbound email attachments and body for sensitive content patterns
:::
::::
::col::
::::card heading="DLP Detection Methods"
:::list style=tight
- **Regular Expressions:** Pattern matching for structured data (SSN: \d{3}-\d{2}-\d{4}, credit card: 16-digit Luhn-valid)
- **Document Fingerprinting:** Hash-based comparison against known sensitive document templates
- **Machine Learning Classification:** ML models classify document content by sensitivity based on training data
- **Exact Data Matching (EDM):** Match against a database of known sensitive records (actual PII database entries)
:::
::::
::::

:::image src="images/27_dlp_architecture.png" alt="Enterprise DLP deployment diagram showing three inspection layers: Layer 1 labeled 'Endpoint DLP' with agent icons on laptops blocking USB transfer and clipboard paste to non-business apps; Layer 2 labeled 'Network / Email DLP' at the internet boundary showing outbound email scanning and web proxy inspection with a policy violation alert blocking an upload attempt; Layer 3 labeled 'Cloud DLP / CASB' showing a Cloud Access Security Broker sitting between corporate users and SaaS platforms (Microsoft 365, Salesforce, Box), scanning file shares and external collaboration invitations; a central 'DLP Policy Engine' box connects all three layers with bidirectional arrows labeled 'Unified Policy'; a 'Data Classification Taxonomy' document feeds the Policy Engine" caption="Three-tier DLP architecture: endpoint, network, and cloud DLP layers work under a unified policy engine driven by the organization's data classification taxonomy. Coverage across all three layers is required because sensitive data can leave through any of these channels." width=full
:::

:::notes
Data Loss Prevention architecture addresses one of the most consequential but technically challenging security problems: preventing sensitive data from leaving organizational control through unauthorized or unintended channels. Data exfiltration is the final phase of most sophisticated attacks, all the lateral movement, privilege escalation, and credential theft that precede it are in service of eventually extracting valuable data. DLP is the technical control layer specifically designed to detect and block that extraction.

Understanding DLP requires understanding its relationship with data classification. DLP controls can only protect data they can identify as sensitive. Without a data classification framework, a taxonomy that defines what data types are sensitive, how they are labeled, and what handling requirements apply at each sensitivity level, DLP systems default to pattern-matching heuristics that generate significant false positive rates. The NIST CSF IDENTIFY function ID.AM-5 (Resources are prioritized based on their classification, criticality, and business value) directly addresses the prerequisite data classification work that must precede DLP deployment.

Data classification taxonomies typically define three to five sensitivity levels. A common enterprise taxonomy includes: Public (data approved for external distribution), Internal (data for internal use only, not regulated, but not intended for public release), Confidential (sensitive business data requiring protection, trade secrets, financial projections, personnel data), Restricted (regulated data requiring the highest protection, PII, PHI, PCI cardholder data, CUI). Each classification level has associated handling requirements: how the data must be stored, transmitted, accessed, and disposed of.

Endpoint DLP agents are installed on managed devices and monitor and control data movement at the device level: USB port usage, clipboard operations, printing, screen capture, and data pasting between applications. When a user attempts to copy a file containing credit card numbers to a USB drive, the endpoint DLP agent evaluates the operation against policy, if the file contains data matching the credit card pattern and the user is not in the authorized data export role, the operation is blocked and an alert is generated. Endpoint DLP is the strongest control for preventing exfiltration by insiders using physical media or personal cloud storage from managed devices, but requires agent deployment on all managed endpoints and does not protect data on unmanaged (BYOD) devices.

Network DLP operates at the perimeter, typically integrated with the web proxy or email security gateway, and inspects outbound traffic for sensitive content. Email DLP scans outbound email attachments and body text for sensitive data patterns before the email leaves the organization's email relay. Web proxy DLP inspects HTTP POST requests (file uploads) to cloud storage sites, personal webmail, and other web destinations. Network DLP provides coverage for unmanaged devices connecting through the corporate proxy, but cannot inspect encrypted traffic without TLS inspection, which introduces its own privacy and legal considerations.

Cloud DLP, typically implemented through a Cloud Access Security Broker (CASB) or through native cloud provider APIs (Microsoft Purview DLP, Google Cloud DLP), monitors and controls sensitive data within and across SaaS platforms. This is increasingly important as more business data lives natively in cloud applications rather than on managed endpoints. CASB solutions provide visibility into which SaaS applications employees are using (sanctioned and unsanctioned), what sensitive data is stored in those applications, and whether that data is being shared externally, for example, a SharePoint site inadvertently configured with external sharing enabled exposing confidential documents.

Detection methods range in sophistication and accuracy. Regular expressions are the most basic, they match patterns like Social Security Number formats, credit card number formats, or bank routing number formats. They produce false positives (strings that match the pattern but are not actually sensitive data) and miss sensitive data that does not conform to regular formats. Document fingerprinting creates a hash-based signature of known sensitive document templates (an employee's confidential performance review template) and blocks transfers of documents matching those signatures. Exact Data Matching (EDM) creates a database of specific sensitive records, actual SSNs, specific customer account numbers, and matches content against the exact values rather than patterns, dramatically reducing false positives. Machine learning classification models trained on labeled sensitive and non-sensitive documents can classify new documents by content context rather than just pattern matching, providing the most adaptive detection but requiring careful training data management.

NIST SP 800-53 MP-5 (Media Transport) governs physical media controls, SC-28 (Protection of Information at Rest) addresses encryption requirements, and AC-3 (Access Enforcement) governs the access controls that DLP complements. GDPR Article 32 and HIPAA Security Rule §164.312(a)(2)(iv) both require technical safeguards for protecting regulated data, which DLP helps satisfy.
:::

%%%
---
unit: Comparison
code: COMP1
title: Comparison, WAF vs IPS vs NGFW
---
:::callout style=soft
Three critical network security tools are commonly confused. Understanding their distinct roles, inspection capabilities, and deployment positions is essential for designing the correct layered defense at each architectural tier.
:::

:::table
| Attribute | WAF (Web Application Firewall) | IPS (Intrusion Prevention System) | NGFW (Next-Gen Firewall) |
|---|---|---|---|
| **OSI Layer** | Layer 7 (Application) | Layer 3–7 (Network to Application) | Layer 3–7 (Stateful + Application) |
| **Primary Target** | HTTP/HTTPS application attacks | Known exploit signatures, anomalies | Network traffic policy enforcement |
| **Deployment Position** | In front of web applications | Inline on network path | Network perimeter or inter-zone |
| **Signature Focus** | OWASP Top 10 (SQLi, XSS, CSRF) | CVE-based exploit signatures, protocol anomalies | Port/protocol policy, app identification |
| **SSL/TLS Inspection** | Yes (required for HTTPS) | Optional (resource intensive) | Optional (with performance penalty) |
| **Example Products** | AWS WAF, Cloudflare, F5 ASM | Snort, Suricata, Palo Alto IPS | Palo Alto NGFW, Fortinet FortiGate, Check Point |
| **NIST SP 800-53 Control** | SI-3, SC-7(21) | SI-4, SC-7 | SC-7 (Boundary Protection) |
:::

:::image src="images/27_waf_ips_ngfw_comparison.png" alt="Three-column comparison card layout: left card labeled 'WAF' with an application-layer funnel icon showing HTTP traffic being filtered for SQL injection and XSS patterns; center card labeled 'IPS' with a signature-matching icon showing network packets checked against a CVE signature database with malicious ones dropped; right card labeled 'NGFW' with a stateful inspection diagram showing connection state table and application identification layer; below each card, a deployment position diagram shows WAF placed between internet and web server, IPS placed inline on the internal network segment, and NGFW placed at the network perimeter; color coding distinguishes the three by function (WAF=blue, IPS=orange, NGFW=green)" caption="WAF, IPS, and NGFW operate at different OSI layers and address different threat categories. All three may be present in a mature architecture, each positioned at the layer and location where it provides the highest value." width=full
:::

:::notes
Web Application Firewalls, Intrusion Prevention Systems, and Next-Generation Firewalls are three of the most commonly deployed network security tools, and they are consistently misunderstood, both individually and in relation to each other. Students and practitioners frequently conflate their capabilities, deploy them in inappropriate positions, or assume that having one eliminates the need for the others. This comparison slide establishes the precise technical distinction between all three.

A Next-Generation Firewall is a network-layer security control that enforces access policy between network segments. It performs stateful packet inspection, tracking the state of TCP connections and evaluating whether each packet belongs to a legitimately established session, combined with application identification using deep packet inspection (DPI). A traditional firewall enforces policy based only on source IP, destination IP, port, and protocol. An NGFW adds application identification: it can recognize specific applications by their traffic patterns (Dropbox, BitTorrent, Salesforce, Zoom) regardless of the port they use, and apply access policy at the application identity level rather than just the port level. NGFWs are deployed at network perimeter positions and between major network zones, they enforce the "which network zones can communicate with which other zones" policy and enforce basic access control policy on what applications are permitted.

An Intrusion Prevention System adds signature-based and behavioral threat detection to the network inspection capability. Where an NGFW says "permit HTTPS traffic from the DMZ to the internet," an IPS inspects that HTTPS traffic and says "this HTTPS traffic contains a pattern matching CVE-2023-44487 (HTTP/2 Rapid Reset DoS attack), block this specific connection." The IPS maintains a continuously updated signature database of known attack patterns, protocol anomalies, and malicious payloads, and blocks or alerts on connections matching those signatures. IPS may be deployed as a standalone appliance inline on network paths, or integrated as a feature module within an NGFW platform (most modern NGFW products include integrated IPS capabilities). The NIST MITRE ATT&CK framework maps IPS signatures to specific ATT&CK technique IDs, enabling organizations to track their signature coverage against the attack techniques most relevant to their threat environment.

A Web Application Firewall is specifically designed for Layer 7 HTTP/HTTPS application security, addressing the attack categories defined in the OWASP Top 10. Unlike an NGFW or IPS, a WAF understands HTTP semantics, request methods, URL paths, headers, cookies, form parameters, and response codes, and can evaluate the content and structure of HTTP requests for application-layer attack patterns. SQL injection attacks embed malicious SQL syntax in URL parameters or form fields. A WAF examines the content of those parameters and blocks requests containing SQL syntax like `' OR 1=1 --` or `UNION SELECT`. An NGFW or IPS at the network layer cannot detect SQL injection reliably because the malicious content is embedded within a legitimately formatted HTTP request, the packet looks like normal web traffic from a network perspective.

WAFs operate in two primary modes. In allowlist mode (also called positive security model), the WAF only permits HTTP requests matching a defined profile of expected behavior, known URL paths, known parameter names, expected data types. Any request deviating from the known-good profile is blocked. This is highly effective but requires significant upfront configuration and ongoing maintenance to keep the allowlist current with application changes. In blocklist mode (negative security model), the WAF applies signature rules blocking known malicious patterns, using signatures from sources like OWASP ModSecurity Core Rule Set (CRS) or vendor-maintained signature libraries. This requires less configuration but misses novel attacks not yet in the signature database.

The correct architecture deploys all three of these tools in their appropriate positions: the NGFW enforces zone-to-zone access policy and application identity control at network boundaries; IPS signatures inspect traffic for known exploit patterns in all traffic flows; and the WAF specifically protects web application endpoints from application-layer attacks. They are complementary, not redundant. Removing any one of them creates a detection or enforcement gap at the OSI layer that tool was covering.

TLS/SSL inspection deserves mention as a shared challenge. All three tools struggle with encrypted traffic: they cannot inspect the payload of an HTTPS connection without terminating and re-encrypting the TLS session (sometimes called TLS inspection or SSL bumping). This creates both performance and privacy considerations. Organizations typically implement TLS inspection selectively, inspecting outbound enterprise user traffic (web proxy TLS inspection) but not inspecting all encrypted flows, to balance security visibility with performance and privacy requirements. NIST SP 800-81 (Secure Domain Name System) and NIST SP 800-177 (Trustworthy Email) provide guidance on specific protocol security that complements these network inspection tools.
:::

%%%
---
unit: Framework Detail
code: ISO
title: "ISO/IEC 27001:2022 & NIST Alignment"
---
:::callout style=soft
**ISO/IEC 27001:2022** is the international standard for Information Security Management Systems (ISMS). Organizations pursuing international customers, EU regulatory compliance, or supply-chain certification requirements need to understand how 27001 aligns with and complements NIST frameworks.
:::

:::table
| Dimension | ISO/IEC 27001:2022 | NIST CSF 2.0 | NIST SP 800-53 Rev. 5 |
|---|---|---|---|
| **Type** | Certifiable management system standard | Voluntary framework | Mandatory control catalog (federal) |
| **Audience** | International / commercial enterprises | U.S. enterprises, critical infrastructure | U.S. federal agencies, contractors |
| **Structure** | 10 clauses + 93 Annex A controls | 6 Functions, 22 Categories, 106 Subcategories | 20 families, 1000+ controls with baselines |
| **Certification** | Third-party certification (annual surveillance + 3-yr recertification) | No certification, self-assessment or voluntary disclosure | FedRAMP/FISMA authorization (not ISO cert) |
| **Risk Approach** | Risk treatment plan drives control selection | Risk-based prioritization via Profiles | Baseline (Low/Moderate/High) controls required |
| **GDPR Alignment** | Strong, 27001 is frequently cited as a GDPR technical measure | Partial | Partial (SP 800-53 Rev. 5 adds privacy controls) |
:::

:::callout style=soft
ISO/IEC 27001:2022 Annex A maps directly to NIST SP 800-53 Rev. 5. Organizations implementing both frameworks share approximately 80% of their control work. The ISO Statement of Applicability (SoA) document is the equivalent of the NIST System Security Plan (SSP).
:::

:::image src="images/27_iso27001_nist_alignment.png" alt="Venn diagram with three overlapping circles: left circle labeled 'ISO/IEC 27001:2022' in blue with key attributes listed (certifiable, international, 93 Annex A controls, ISMS clause structure); right circle labeled 'NIST SP 800-53 Rev. 5' in green with key attributes (U.S. federal mandatory, 1000+ controls, Low/Mod/High baselines, FedRAMP); bottom circle labeled 'NIST CSF 2.0' in orange with key attributes (voluntary, business-aligned, 6 functions, Profile-based); overlapping regions between all three circles contain shared elements: risk assessment methodology (ISO/NIST overlap), control families mapping (all three overlap), and incident response requirements (all three overlap); center of all three circles labeled 'Core Risk Management Practices'" caption="ISO 27001, NIST SP 800-53, and NIST CSF overlap significantly in risk assessment methodology and control content. Organizations implementing one framework have completed the majority of work required for the others, enabling dual compliance at manageable cost." width=full
:::

:::notes
ISO/IEC 27001 is the internationally recognized standard for Information Security Management Systems (ISMS), published by the International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC). The 2022 revision, the current version, substantially updated the control structure of Annex A, reorganizing the previous 114 controls across 14 domains into 93 controls across four themes: Organizational Controls (37 controls), People Controls (8 controls), Physical Controls (14 controls), and Technological Controls (34 controls). The reorganization better reflects contemporary security architectures, explicitly adding controls for cloud security, threat intelligence, and information security in DevSecOps environments.

For security architects operating in international business environments, ISO 27001 certification is frequently required as a condition of supply chain partnership, customer contract award, or regulatory compliance in European markets. GDPR Article 32 requires that organizations implement "appropriate technical and organizational measures" to protect personal data, while not mandating specific controls, ISO 27001 certification is widely accepted by data protection authorities across EU member states as evidence that appropriate measures are in place. UK, EU, and Asia-Pacific government procurement processes frequently specify ISO 27001 certification as a vendor qualification requirement.

The relationship between ISO 27001 Annex A and NIST SP 800-53 Rev. 5 is one of substantial overlap. Both are control catalogs grounded in the same fundamental risk management principles, addressing the same security domains (access control, cryptography, incident management, physical security, network security, supplier relationships). NIST has published a mapping between SP 800-53 Rev. 5 and ISO 27001:2022 Annex A controls, which shows that for most organizations implementing both frameworks, approximately 80% of the control work is shared. The primary differences are in breadth (SP 800-53 has more controls at higher technical specificity) and in the management system structure (ISO 27001's clause 4-10 requirements for ISMS governance, internal audit, and management review have no direct NIST SP 800-53 equivalent, though they map well to NIST CSF's GOVERN function).

The ISO 27001 certification process involves three stages. Stage 1 (Documentation Review): the certification body (an accredited third-party audit firm) reviews the organization's ISMS documentation, the scope statement, information security policy, risk assessment, risk treatment plan, and Statement of Applicability (SoA). The SoA documents all 93 Annex A controls and for each control states: whether it is applicable to the organization's scope, whether it is implemented, and if not implemented, the justification for exclusion. Stage 2 (On-Site Audit): the certification body conducts an on-site assessment verifying that the documented ISMS is actually implemented and effective. Auditors interview staff, review evidence (configuration screenshots, audit logs, training records), and test process execution. Stage 3 (Surveillance Audits): after certification is granted, annual surveillance audits verify continued conformance, with a full recertification audit every three years.

The NIST System Security Plan (SSP) required for FedRAMP and FISMA compliance is the functional equivalent of the ISO 27001 SoA and ISMS documentation package, both are comprehensive descriptions of an organization's security controls, their implementation status, and associated risk treatment decisions. Organizations pursuing both ISO 27001 and FedRAMP authorizations can structure their documentation program to satisfy both requirements from a single master document set, provided the document structure and evidence are organized appropriately.

NIST Interagency Report 8011 (Automation Support for Security Control Assessments) provides guidance on automating the evidence collection process for SP 800-53 control assessments, similar automation tools exist for ISO 27001 internal audits through GRC platforms like ServiceNow GRC, Archer, or LogicGate. These platforms allow organizations to maintain a continuous compliance posture rather than scrambling to collect evidence immediately before audit cycles.

For governance, risk and compliance careers, ISO 27001 Lead Auditor and Lead Implementer certifications from accredited bodies (IRCA, PECB, BSI) are a pathway into compliance program management, internal audit and third-party vendor risk assessment.
:::

%%%
---
unit: Deep Dive
code: SUPPLY
title: Supply Chain Security & Third-Party Risk
---
:::callout style=soft
Modern organizations are only as secure as their weakest vendor. **Third-party and supply chain risk** represents one of the fastest-growing attack surfaces, adversaries compromise high-value targets by first compromising their more vulnerable suppliers.
:::

:::steps
**Inventory Third Parties:** Catalog every vendor, contractor, SaaS provider, and open-source dependency that has access to organizational systems, data, or code. NIST SP 800-161 Rev. 1 calls this the C-SCRM (Cyber Supply Chain Risk Management) baseline.
**Classify by Risk Tier:** Assess each third party by data access level, system connectivity, software integration type, and criticality to business operations, assigning high, medium, or low risk tiers that determine assessment rigor.
**Contractual Requirements:** Include specific security requirements in vendor contracts: right-to-audit clauses, breach notification timelines, minimum security standards (e.g., ISO 27001 certification or SOC 2 Type II report), and data handling requirements.
**Security Assessment:** For high-risk vendors: conduct questionnaire-based assessments (SIG, CAIQ), review SOC 2 / ISO 27001 reports, and perform on-site or technical assessments of critical integrations.
**Software Bill of Materials (SBOM):** For software vendors, require an SBOM, a machine-readable inventory of all open-source and commercial components in the delivered software. SBOM enables rapid identification of exposure when new CVEs are published in component libraries.
**Continuous Monitoring:** Use attack surface management and third-party risk monitoring services (BitSight, SecurityScorecard, RiskRecon) to track vendor security posture changes between formal assessments.
:::

:::image src="images/27_supply_chain_risk.png" alt="Concentric circle supply chain diagram: innermost circle labeled 'Target Organization' with a building icon; surrounding ring labeled 'Direct Vendors (Tier 1)' with icons for HVAC contractor, software vendor, SaaS provider, IT managed service provider; outer ring labeled 'Vendor Suppliers (Tier 2)' with icons showing the suppliers of Tier 1 vendors; outermost ring labeled 'Open Source Components (Tier 3)' showing npm, PyPI, Maven dependency packages; red arrows from outer rings pointing inward labeled with attack vectors: 'Credential theft (Target)', 'Malicious update (SolarWinds)', 'Log4Shell in dependency (Log4j)'; a risk tier heat map legend shows Tier 1 in orange (High Risk), Tier 2 in yellow (Medium Risk), Tier 3 in blue (Monitor)" caption="The supply chain attack surface extends through multiple tiers: direct vendors (Tier 1), vendor suppliers (Tier 2), and open-source software components (Tier 3). Adversaries choose the weakest link, often a less-secured vendor, as their initial access vector into well-defended primary targets." width=full
:::

:::notes
Supply chain security has emerged as one of the most consequential security architecture challenges of the past decade, driven by a series of high-profile incidents that demonstrated how adversaries can compromise well-defended primary targets by first compromising their less-well-defended suppliers. The SolarWinds attack (2020), the Log4Shell vulnerability in the Apache Log4j library (CVE-2021-44228, 2021), and the XZ Utils backdoor discovered in March 2024 (CVE-2024-3094) all illustrate different vectors in the supply chain attack surface.

The supply chain attack surface has three tiers. Tier 1 is direct vendor relationships: companies and contractors that have direct system access, data access, or software delivery relationships with the organization. HVAC vendors with remote access credentials, managed service providers with administrative access to corporate systems, SaaS providers hosting organizational data, and software vendors delivering products used in production all represent Tier 1 supply chain risk. The Target breach was a Tier 1 supply chain attack.

Tier 2 is the supply chain of your supply chain: the vendors and subcontractors that your Tier 1 vendors rely on. If your organization uses a payroll processing service, and that payroll service uses a subcontracted background check vendor, that background check vendor is a Tier 2 supplier. Organizations rarely have direct contractual relationships or security assessment capability over Tier 2 suppliers, which is why NIST SP 800-161 Rev. 1 emphasizes "flow-down" requirements, contractually requiring your Tier 1 suppliers to impose minimum security requirements on their own suppliers.

Tier 3 is open-source software dependencies: the npm packages, Python libraries, Maven components, and other open-source software libraries embedded in applications your organization develops or uses. Log4Shell (CVE-2021-44228) demonstrated the catastrophic potential of this tier: a single critical vulnerability in the Apache Log4j logging library, embedded as a dependency in hundreds of thousands of applications across virtually every industry, created an attack surface requiring emergency remediation for organizations worldwide within days of public disclosure. The challenge is that organizations frequently do not know which open-source libraries are embedded in their software, they may know the top-level libraries explicitly added to their application's dependency manifest, but not the transitive dependencies (libraries depended upon by their direct dependencies).

Software Bill of Materials (SBOM) is the emerging technical mechanism for addressing Tier 3 supply chain risk. An SBOM is a machine-readable inventory of all software components, commercial and open-source, included in a software product, including their version numbers and provenance. When a new CVE is published in a component library (e.g., Log4j), an organization with SBOMs for all its software products can immediately identify which products contain the vulnerable component and prioritize remediation. Without SBOMs, organizations must manually audit their codebase, a process that takes weeks and is frequently incomplete.

Executive Order 14028 (May 2021) mandated SBOM requirements for all software sold to the U.S. federal government, establishing SBOM as a contractual requirement across the federal procurement supply chain. The NTIA (National Telecommunications and Information Administration) published minimum SBOM element specifications, and NIST published guidance on SBOM integration into software development processes through NIST IR 8060.

NIST SP 800-53 Rev. 5 SA-9 (External Information System Services) governs third-party access requirements, SA-12 (Supply Chain Protection) governs supply chain risk management, and SR-1 through SR-12 (the Supply Chain Risk Management family introduced in Rev. 5) provide comprehensive guidance on the organizational and technical controls required for supply chain security. For organizations in the U.S. defense industrial base, DFARS clause 252.204-7012 (Safeguarding Covered Defense Information) requires compliance with NIST SP 800-171, which includes supply chain risk management requirements, and flow-down to subcontractors handling Covered Defense Information.

The practical organizational response to supply chain risk begins with vendor inventory, most organizations discover they have far more third-party relationships than they were aware of. Risk tiering using data access, system connectivity, and business criticality factors allows organizations to concentrate limited assessment resources on the highest-risk relationships. Contractual security requirements, breach notification timelines, minimum security standard certifications (SOC 2 Type II, ISO 27001), right-to-audit clauses, and data destruction requirements at contract termination, establish baseline expectations that shift some risk back to the vendor. Continuous monitoring services that track vendor attack surface scores provide early warning of vendor security deterioration between formal assessment cycles.

Log4Shell illustrates third-party supply chain risk: Log4j was embedded in nearly every Java application, including enterprise products from Cisco, VMware and Oracle, so identifying all affected systems was slow and manual. A Software Bill of Materials would have made that inventory immediate.
:::

%%%
---
unit: Deep Dive
code: NETARCH
title: Network Segmentation Patterns
---
:::callout style=soft
Network segmentation is implemented using several distinct patterns, each suited to different architectural contexts. Choosing the right pattern, or combination of patterns, determines the effectiveness of east-west traffic control and lateral movement containment.
:::

:::table
| Pattern | Architecture | Typical Use Case | Limitation |
|---|---|---|---|
| **DMZ (Three-Leg)** | External FW → DMZ → Internal FW → Internal Net | Web servers, email relays, VPN concentrators | Coarse-grained: entire tier in one zone |
| **VLAN Segmentation** | Switch-level VLAN assignment with inter-VLAN ACLs | Separating user workstations from server VLANs | VLAN hopping attacks; limited to L2 boundary |
| **Firewall Zones** | Dedicated firewall between each major network zone | Datacenter tier separation (web/app/db tiers) | Firewall bottleneck; complex rule management at scale |
| **Software-Defined Networking (SDN)** | Overlay network with centralized controller (NSX, ACI) | Large-scale datacenter and cloud microsegmentation | Controller availability; initial complexity |
| **Host-Based Firewall** | OS-level firewall rules on each host (iptables, nftables) | Container environments, East-West micro-policy | Agent management at scale; OS-level bypass risk |
| **Service Mesh** | Mutual TLS + policy sidecar per microservice (Istio) | Kubernetes and microservice architectures | Significant latency overhead if not optimized |
:::

:::image src="images/27_network_segmentation_patterns.png" alt="Six small network diagrams arranged in a 2x3 grid, each illustrating one segmentation pattern: DMZ shows three-zone layout with external internet, DMZ box, and internal network with two firewall barriers; VLAN diagram shows a managed switch with four VLAN color bands and an inter-VLAN router; Firewall Zones shows four boxes (user/server/management/backup) each separated by firewall icons; SDN diagram shows a central controller with policy flows distributed to virtual switches on each host; Host-Based Firewall shows individual servers each with a shield icon representing OS-level rules; Service Mesh shows four microservice boxes each with a sidecar proxy icon connected by mTLS lines labeled with policy labels" caption="Six network segmentation patterns from most traditional (DMZ, VLAN) to most granular (Service Mesh). Mature environments layer multiple patterns, DMZ at the perimeter, VLAN or firewall zones for datacenter tier separation, and SDN or host-based controls for workload-level microsegmentation." width=full
:::

:::notes
Network segmentation is one of the most important architectural controls for limiting lateral movement, but it is not a single technology or approach. Different segmentation patterns are appropriate for different parts of the enterprise architecture, and mature environments use multiple patterns at different layers. Understanding the strengths and limitations of each pattern enables architects to design a segmentation strategy that provides defense in depth at the network layer.

The DMZ (Demilitarized Zone) is the most fundamental and widely deployed segmentation pattern. A three-legged DMZ places internet-facing systems, web servers, email relays, VPN concentrators, in a segment between two firewalls. The external firewall controls what traffic reaches the DMZ from the internet; the internal firewall controls what traffic can flow from the DMZ into the internal network. Systems in the DMZ are intentionally designed to be exposed to the internet, so they are hardened appropriately, and their compromised state must not provide direct access to internal systems. The DMZ pattern is well-understood, widely supported by firewall vendor architectures, and remains the correct approach for internet-facing service deployment regardless of what other segmentation patterns are used deeper in the network.

VLAN segmentation uses the VLAN feature of managed network switches to divide a physical network into logically separate broadcast domains. Users in different VLANs cannot communicate directly, their traffic must be routed through a router or Layer 3 switch that can apply access control lists (ACLs) between VLANs. VLAN segmentation is the most common form of basic segmentation in enterprise networks and provides useful separation between major user populations (e.g., corporate users vs. guest WiFi vs. IoT devices). However, VLAN segmentation operates at Layer 2, and VLAN hopping attacks, where an attacker sends packets with manipulated 802.1Q VLAN tags to cross VLAN boundaries, can bypass VLAN controls in misconfigured switch environments. VLAN segmentation also provides only coarse-grained control: all devices in the same VLAN can communicate freely.

Firewall zones extend the DMZ concept to internal network segments, placing dedicated firewall instances between each major network tier. A datacenter might have separate firewall zones for the web tier, application tier, database tier, and management network, with explicit firewall rules controlling what traffic is permitted between zones. This is the pattern illustrated in our enterprise DMZ case study earlier in this lecture. Firewall zones provide strong policy enforcement and detailed logging of inter-zone traffic, but can create performance bottlenecks (all inter-zone traffic must traverse the firewall) and require careful rule management as the number of zones and services grows.

Software-Defined Networking (SDN) platforms provide workload-level microsegmentation by implementing a centralized network controller that distributes policy to distributed virtual switches deployed on each hypervisor host. VMware NSX and Cisco ACI are the dominant enterprise SDN platforms. SDN enables policy enforcement at the virtual NIC level, each VM can have a distinct policy specifying exactly which other VMs it may communicate with and on which ports, without requiring physical network changes or dedicated firewall appliances between each pair of VMs. This enables truly granular microsegmentation at datacenter scale, though it requires expertise to design and operate the centralized controller and policy model.

Host-based firewalls (iptables/nftables on Linux, Windows Defender Firewall on Windows) implement microsegmentation at the OS level. Policy rules on each host specify which remote hosts and ports are permitted to make inbound connections. This approach is particularly well-suited to container environments, where containers on the same host need distinct network policies, and to edge cases where network-level segmentation cannot be extended. Kubernetes Network Policies implement host-based microsegmentation natively in container orchestration environments.

Service meshes like Istio, Linkerd, and Consul Connect provide microsegmentation for microservice architectures by deploying a sidecar proxy alongside each service instance. The sidecar handles all incoming and outgoing network communication for its service, enforcing mutual TLS authentication (both ends of every connection authenticate cryptographically), and applying fine-grained policy about which services may communicate with which other services. Service meshes provide the highest level of granularity, enforcing authenticated, encrypted, policy-controlled communication between individual microservices, but introduce latency overhead from the sidecar proxy and require expertise to configure and operate.

NIST SP 800-53 SC-7 (Boundary Protection) provides the foundational requirement for all these segmentation patterns, requiring that managed interfaces be defined at external boundaries and key internal boundaries. NIST SP 800-125B (Secure Virtual Network Configuration for Virtual Machine Protection) addresses SDN-specific security requirements.
:::

%%%
---
unit: Case Study
code: EQUIFAX
title: Case Study, The 2017 Equifax Breach
---
:::callout style=soft
The Equifax breach exposed **147 million Americans'** personal data. The root cause was a known vulnerability left unpatched for 76 days, a foundational **vulnerability management architecture** failure, not a novel or sophisticated attack.
:::

::::columns ratio=1:1
::col::
::::card heading="Attack Timeline"
:::list style=tight
- **March 8, 2017:** Apache Struts CVE-2017-5638 patch released (CVSS 10.0, critical)
- **March 9, 2017:** US-CERT advisory issued; exploitation observed within 24 hours
- **March 15, 2017:** Equifax's IT team sent an internal alert about the vulnerability, but the scanning tool used had a misconfigured certificate and was not actually scanning the vulnerable system
- **May 13, 2017:** Attackers exploited CVE-2017-5638 against Equifax's ACIS consumer portal and gained initial access
- **July 29, 2017:** Equifax analysts noticed suspicious traffic during a routine certificate renewal and terminated the attack
- **September 7, 2017:** Public disclosure, 76 days after compromise, 153 days after patch release
:::
::::
::col::
::::card heading="Root Cause Architecture Failures"
:::list style=tight
- No patching SLA for critical/CVSS 10.0 vulnerabilities, no defined response timeline
- Vulnerability scanning tool failure undetected for months (misconfigured certificate)
- Flat internal network enabled extensive lateral movement after initial access
- Unencrypted PII in the exploited database
- SSL inspection disabled on internal traffic, attack traffic went undetected for 76 days
- No data classification program to identify which systems held the most sensitive data
:::
::::
::::

:::image src="images/27_equifax_breach_timeline.png" alt="Vertical timeline with key events marked: March 8 at top with CVE-2017-5638 patch release and red patch icon; March 9 with US-CERT advisory and exploitation-in-wild warning icons; March 15 with misconfigured scanner icon and yellow warning triangle; May 13 with attacker entry icon and 'Day 0' label; a thick red bar spanning from May 13 to July 29 labeled '76-day attacker dwell time'; July 29 with SSL inspection notice icon; September 7 at bottom with public disclosure icon; annotations on the right side at each event label the architectural failure category (patch management, vulnerability scanning, network monitoring, data protection)" caption="Equifax attack timeline: 153 days elapsed between patch availability and breach discovery. Every phase reflects a distinct architectural failure, not a single point of failure, but systematic gaps across vulnerability management, network monitoring, and data protection architecture." width=full
:::

:::notes
The 2017 Equifax breach is the most consequential example of a vulnerability management architecture failure in documented history. Unlike the Target breach (which involved sophisticated lateral movement and detection suppression) or the SolarWinds attack (which involved a novel and technically impressive supply chain compromise), the Equifax breach involved a known, publicly disclosed vulnerability with a publicly available patch, exploited 76 days after the patch was released, a timeframe that reflected pure organizational and process failure.

CVE-2017-5638 is a remote code execution vulnerability in Apache Struts 2, a widely used Java web application framework. The vulnerability exists in the Jakarta Multipart parser, which processes file upload requests. A specially crafted Content-Type header in an HTTP request could cause the parser to execute arbitrary Operating System commands, giving an unauthenticated attacker the ability to run any command on the web server without any form of authentication. The CVSS (Common Vulnerability Scoring System) score was 10.0, the maximum possible severity. The Apache Software Foundation published a patch on March 8, 2017. The U.S. Computer Emergency Readiness Team (US-CERT) issued an advisory on March 9. Exploitation in the wild was observed within 24 hours of public disclosure.

Equifax's IT security team issued an internal advisory on March 15 directing that systems be patched within 48 hours. This policy action would have been sufficient, if it had been executed. However, Equifax's vulnerability scanning program had a critical flaw: the certificate used by the scanning tool to inspect encrypted traffic had expired. As a result, the scanning tool was not actually scanning the traffic flows containing the ACIS (Automated Consumer Interview System) web portal, the application that ran on Apache Struts and contained the exploitable endpoint. The scanner reported no vulnerabilities not because there were none, but because it was not actually scanning the relevant traffic. This misconfiguration went undetected for months.

On May 13, 2017, 76 days after the patch was available, attackers exploited CVE-2017-5638 against the ACIS portal. They gained remote code execution on the web server and used that access as their initial foothold. What followed was extensive lateral movement that lasted for 76 days, during which attackers accessed 51 separate database tables across multiple systems. The subsequent investigation identified that the internal network had limited segmentation, the initial web server compromise allowed the attackers to reach database systems that were not directly related to the ACIS application, suggesting insufficient microsegmentation between application zones.

The Equifax breach also revealed a data encryption failure. NIST SP 800-53 SC-28 (Protection of Information at Rest) requires encryption of sensitive data at rest. The personal information (Social Security numbers, birth dates, addresses, driver's license numbers) stored in the breached databases was not encrypted at rest, meaning that once the attackers reached the database servers, the data was immediately readable. Had the data been encrypted at rest with per-customer-record keys, the attackers' database access would have yielded only ciphertext, still a serious incident, but one with dramatically reduced impact.

SSL inspection on internal traffic was also disabled, an apparent legacy configuration decision. As a result, the command-and-control traffic the attackers used to exfiltrate data during the 76-day dwell period traveled over the internal network in encrypted form that the security monitoring systems could not inspect. This is a specific architectural gap: disabling TLS inspection on internal east-west traffic creates a blind spot that sophisticated attackers can exploit for sustained covert communication. NIST SP 800-53 SI-4 (System Monitoring) requires monitoring of information systems including outbound communications, but monitoring encrypted traffic requires either TLS inspection or behavioral analytics that detect anomalies in traffic volume and destination even without payload visibility.

The Congressional investigation into the Equifax breach identified that Equifax had an IT organizational structure that separated the teams responsible for IT and security decisions, creating accountability gaps. The security team was not informed of the expired scanning certificate by the team that managed the scanner. The patch compliance tracking system showed false compliance, because the scanner reported no vulnerability, the compliance database showed the vulnerability as remediated. No independent verification process existed to cross-check scanner results against the actual patch deployment status.

Post-breach remediation cost Equifax approximately $1.38 billion in settlements, regulatory fines, and remediation costs. The FTC settlement included a $575 million consumer redress fund, the largest ever data breach settlement at the time. The class-action settlements, regulatory fines from the UK ICO (£500,000, the maximum under the pre-GDPR Data Protection Act 1998), and cybersecurity remediation program costs brought the total closer to $2 billion over several years.

The Equifax case offers clear, specific, and actionable architecture lessons. First, vulnerability management requires a defined patching SLA for each severity level, at minimum, a documented and enforced requirement that CVSS 9.0+ vulnerabilities be patched within 72-96 hours of patch availability. Second, scanning tool failures must be detected through independent verification, cross-checking scanner coverage against the asset inventory to confirm that every known system is actually being scanned. Third, flat internal networks must be replaced with microsegmentation so that initial web server compromises cannot provide access to unrelated database systems. Fourth, data at rest must be encrypted with key management processes that limit the impact of database-level access. Fifth, SSL inspection or behavioral analytics must provide monitoring visibility into internal encrypted traffic flows to detect exfiltration activity.

NIST SP 800-40 Rev. 4 covers enterprise patch-management planning, including service-level frameworks by vulnerability severity. The Equifax breach, roughly $2 billion of cost against a 76-day patch delay, quantifies the per-day financial cost of gaps in the patch process.
:::

%%%
---
unit: Comparison
code: MTTR
title: Architecture Metrics, MTTD, MTTR, and Breach Cost
---
:::callout style=soft
Security architecture effectiveness is measurable. **Mean Time to Detect (MTTD)** and **Mean Time to Respond (MTTR)** are the two most important operational metrics, both are directly predictive of total breach cost.
:::

:::table
| Metric | Definition | Industry Average (2024) | Best-in-Class | Primary Architecture Driver |
|---|---|---|---|---|
| **MTTD** | Time from initial breach to detection | 194 days | < 30 days | DETECT function: SIEM, UEBA, EDR coverage |
| **MTTR** | Time from detection to containment | 64 days | < 7 days | RESPOND function: IR plan, SOAR, playbooks |
| **Total Dwell Time** | MTTD + MTTR | 258 days | < 37 days | Combined DETECT + RESPOND maturity |
| **Average Breach Cost** | Total cost including detection, notification, legal, remediation | $4.88M (IBM 2024) | $2.2M (ZTA deployed) | Full CSF lifecycle + ZTA architecture |
| **ZTA Cost Reduction** | Breach cost differential for organizations with ZTA | -$1.76M vs. non-ZTA | — | Zero Trust Architecture deployment |
| **AI/Automation Saving** | Breach cost reduction for SOAR/AI-enabled DETECT + RESPOND | -$2.22M vs. no automation | — | SOAR, ML-based detection, automated response |
:::

:::callout style=soft
Every 10-day reduction in dwell time is associated with approximately $300,000 in reduced breach cost (IBM Cost of a Data Breach Report 2024). Architecture investments in DETECT and RESPOND functions have directly calculable ROI.
:::

:::image src="images/27_mttd_mttr_breach_cost.png" alt="Two-chart layout: left chart is a horizontal bar chart comparing MTTD + MTTR for four organization profiles: 'No SIEM/EDR' (MTTD 290 days + MTTR 100 days = 390 total), 'SIEM Only' (MTTD 220 days + MTTR 80 days), 'SIEM + EDR + SOAR' (MTTD 80 days + MTTR 30 days), 'ZTA + AI/SOAR' (MTTD 28 days + MTTR 9 days); each bar is segmented with MTTD in blue and MTTR in orange; right chart is a column chart showing average breach cost for the same four profiles, declining from $6.1M (No SIEM/EDR) to $2.2M (ZTA + AI/SOAR); a green dollar savings label on each column shows cumulative cost reduction" caption="MTTD and MTTR correlate directly with breach cost: organizations with mature DETECT and RESPOND architectures (ZTA + AI/SOAR) experience both the shortest dwell times and the lowest breach costs. The cost differential provides clear ROI justification for architecture investment in these functions." width=full
:::

:::notes
Security architecture investment decisions must ultimately be justified in business terms, in risk reduction measured in financial impact, regulatory exposure, and business continuity cost. The metrics presented in this slide provide the quantitative framework for making those justifications. They are drawn primarily from IBM Security's annual Cost of a Data Breach Report, which surveys hundreds of organizations that experienced data breaches, and from the Ponemon Institute's research. These are the most widely cited empirical benchmarks in the security industry.

Mean Time to Detect (MTTD) measures how long an attacker can operate within an organization's environment before being discovered. The industry average of 194 days in 2024 means that the typical organization takes over six months to discover that it has been breached. During those 194 days, an attacker is free to move laterally, escalate privileges, identify the most valuable data, and exfiltrate it systematically. The relationship between MTTD and breach cost is direct and well-established: every day of additional dwell time allows more data to be exfiltrated, more systems to be compromised, and more forensic evidence to be destroyed. IBM's research indicates approximately $300,000 in reduced breach cost for every 10-day reduction in dwell time.

MTTD is primarily driven by DETECT function architecture: the breadth and quality of log source coverage in the SIEM, the sophistication of correlation rules and UEBA behavioral models, and the coverage of EDR agents across the endpoint fleet. Organizations without SIEM or EDR, typically small and mid-sized organizations, experience the longest MTTD values because they have no automated mechanism for detecting adversarial behavior. Breaches in these organizations are typically discovered by external parties (payment processors noticing fraudulent transaction patterns, law enforcement notifying the victim after finding their data in criminal marketplaces, or customers reporting unauthorized account access) rather than internal detection.

Mean Time to Respond (MTTR) measures how long it takes from the moment a breach is detected to effective containment, isolating compromised systems, removing attacker access, and stopping further data loss. The industry average of 64 days reflects the organizational challenges of incident response: legal review before action, difficulty isolating interdependent production systems without causing business outages, forensic investigation requirements before containment to preserve evidence, and notification obligations that must be satisfied before remediation actions that might alter the evidence state. A mature RESPOND function, with documented incident response plans, pre-authorized response playbooks, SOAR automation for initial containment steps, and a tested incident response team, can bring MTTR below 7 days for many incident types.

The business case for Zero Trust Architecture receives strong empirical support from IBM's 2024 data. Organizations with fully deployed Zero Trust Architecture experienced average breach costs of approximately $2.2 million, compared to approximately $4 million for organizations without ZTA in place, a difference of $1.8 million per breach on average. The cost reduction reflects both lower breach impact (microsegmentation containing lateral movement, reducing the scope of data access) and faster detection (ZTA's continuous monitoring and behavioral analytics reducing MTTD).

AI and automation capabilities, specifically SOAR platforms and ML-based detection, contributed an additional average cost reduction of $2.22 million compared to organizations without these capabilities. The IBM research categorizes organizations by AI/automation deployment maturity: organizations with fully deployed AI/automation in security operations experienced average breach costs of $2.77 million versus $5.72 million for organizations with no AI/automation deployment, a difference of nearly $3 million per breach. This magnitude of ROI makes AI/automation investment highly justifiable even for mid-market organizations.

The practical implication for security architects and CISOs is that MTTD and MTTR should be tracked as primary security program KPIs, not vanity metrics like number of patches applied or number of phishing simulations run, but the metrics that directly predict financial exposure. Monthly or quarterly MTTD and MTTR tracking against organizational targets provides board-level reporting that demonstrates security program effectiveness in language that business leadership can evaluate and respond to.

NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide) provides the process framework for measuring and improving MTTR through structured incident response lifecycle management. The NIST CSF RESPOND function subcategory RS.AN-4 (Incidents are categorized consistent with response plans) and RS.MI-1 (Incidents are contained) directly map to the MTTR measurement and improvement process.

Security architecture is a risk-management function with measurable return, not a cost center. If SOAR reduces average breach cost by $2.22M and costs $500K a year to run, it pays for itself in less than one contained breach, a calculation that models how security architects communicate investment value to financial leadership.
:::

%%%
---
unit: Summary
code: ARCH2
title: Architecture Maturity Roadmap
---
:::callout style=soft
Building a mature security architecture is a multi-year program, not a one-time project. This roadmap maps capability investments to NIST CSF functions and implementation tiers, providing a structured path from reactive to adaptive security posture.
:::

:::table
| Phase | Timeline | Key Investments | Target CSF Tier | Expected MTTD Reduction |
|---|---|---|---|---|
| **Foundation** | Year 1 | Asset inventory, basic SIEM, MFA rollout, IR plan documentation | Tier 1 → Tier 2 | 290 → 220 days |
| **Visibility** | Year 1-2 | SIEM with full log source coverage, EDR on all endpoints, vulnerability management SLAs | Tier 2 → Tier 2.5 | 220 → 130 days |
| **Control** | Year 2-3 | Microsegmentation, PAM deployment, DLP, Zero Trust identity (ZTNA + conditional access) | Tier 2.5 → Tier 3 | 130 → 70 days |
| **Detection** | Year 3-4 | UEBA, threat intelligence integration, SOAR playbooks, purple team exercises | Tier 3 | 70 → 30 days |
| **Adaptive** | Year 4+ | AI-driven analytics, continuous compliance monitoring, supply chain risk program, SBOM integration | Tier 3 → Tier 4 | 30 → < 15 days |
:::

:::image src="images/27_architecture_maturity_roadmap.png" alt="Horizontal roadmap with five labeled phases from left to right: Foundation, Visibility, Control, Detection, Adaptive; each phase sits on a rising staircase step with a year label; above each step, three to four key investment items are listed in small text; below the staircase, a gradient bar from red (left, high breach cost) to green (right, low breach cost) is labeled 'Breach Cost Exposure' with dollar values declining across the gradient; a secondary y-axis shows MTTD values declining from 290 days at Foundation to 15 days at Adaptive; small NIST CSF tier badges (Tier 1 through Tier 4) appear above each step transition; the overall image title reads 'Journey to Security Architecture Maturity'" caption="Security architecture maturity roadmap: five phases over four+ years, each building on the previous. The roadmap correlates capability investments to MTTD reduction and breach cost exposure, providing measurable business justification for each phase of investment." width=full
:::

:::notes
Security architecture maturity does not arrive in a single budget cycle. Responsible architecture planning requires a multi-year roadmap that sequences investments in a logical dependency order, building the foundation capabilities that more advanced capabilities depend on, rather than attempting to deploy everything simultaneously or being driven by vendor marketing cycles. This slide presents a five-phase maturity roadmap that maps investments to NIST CSF implementation tier progression and to measurable MTTD improvements.

The Foundation phase is the prerequisite for everything that follows. Without an accurate asset inventory, the SIEM cannot have comprehensive log source coverage. Without basic incident response plan documentation, even a well-staffed SOC will respond chaotically to the first significant incident it faces. MFA rollout, particularly for remote access and privileged accounts, is one of the highest-ROI individual investments an organization can make, preventing the credential-based attack paths that account for the majority of breach initial access vectors. Organizations beginning this phase typically have informal, reactive security practices (Tier 1) and should expect to reach Tier 2 (Risk-Informed) by the end of Year 1.

The Visibility phase builds on the foundation to achieve comprehensive monitoring coverage. A SIEM without complete log source coverage has blind spots, attack paths that generate no telemetry and therefore cannot trigger detections. This phase focuses on ensuring all critical systems generate logs in SIEM-parseable formats and that all those logs are being collected. EDR deployment across all managed endpoints is the other critical investment in this phase, providing host-level telemetry that the network-only SIEM visibility cannot see. Vulnerability management SLAs, defined timelines for patching CVSS 9.0+ (24 hours), 7.0+ (7 days), and lower severity vulnerabilities (30 days), address the Equifax-class vulnerability management failure mode. Organizations completing this phase should expect MTTD reduction from approximately 220 days to 130 days.

The Control phase implements the proactive architectural controls that reduce attack surface and limit the blast radius of successful breaches: microsegmentation of the internal network, PAM deployment to eliminate standing privileged credentials, DLP for sensitive data protection, and Zero Trust identity controls (ZTNA replacing VPN, conditional access policies integrating device health into authentication decisions). These investments are more complex and operationally impactful than the earlier phases, microsegmentation in particular requires careful traffic analysis and staged rollout to avoid breaking legitimate application dependencies. Organizations completing this phase should be solidly at Tier 3 (Repeatable) across most CSF functions.

The Detection phase matures the DETECT function from threshold-based alerting to behavioral analytics, adding UEBA models that establish behavioral baselines and detect anomalies from legitimate accounts and devices that would not match traditional signature-based rules. Threat intelligence integration feeds current indicator of compromise (IOC) data into SIEM correlation, enabling detection of known threat infrastructure before signatures are widely distributed. SOAR playbook deployment automates initial triage and containment for high-confidence alerts. Purple team exercises empirically validate that detection and response capabilities work as designed. By the end of this phase, MTTD should be below 30 days for most incident types.

The Adaptive phase represents the frontier of mature security programs: continuous compliance monitoring using GRC platform automation, supply chain risk management programs with SBOM integration, AI-driven analytics for predictive threat detection, and threat hunting programs where analysts proactively search for adversary presence using hypothesis-driven investigation. Tier 4 (Adaptive) organizations at this phase use lessons learned from each incident and exercise to continuously refine their detection rules, response playbooks, and architectural controls, creating a virtuous improvement cycle rather than a static compliance posture.

The roadmap correlates each phase with expected MTTD improvements, providing measurable targets that allow organizations to track progress and validate that investments are producing the expected improvements. These improvements in MTTD and MTTR translate directly to breach cost reduction, using the IBM benchmark data presented in the previous slide to calculate approximate financial ROI for each phase.

One important planning consideration: the phases in this roadmap are not strictly sequential. Organizations facing specific regulatory deadlines (e.g., a CMMC Level 2 certification requirement within 12 months) may need to accelerate specific controls out of sequence. The Control phase investments (specifically microsegmentation and PAM) are often the highest-priority for organizations facing active threat campaigns targeting their industry. The roadmap should be adapted to each organization's specific risk environment, regulatory obligations, and available resources, it is a framework for thinking, not a rigid prescription.

This roadmap, applied in conjunction with the NIST CSF Profile and Gap Analysis process presented earlier in this lecture, provides a complete toolset for security architects to design, communicate, and execute a multi-year security program. In Class 29's risk assessment project, you will apply these tools to analyze a real-world organization scenario, identify architectural gaps, and propose a prioritized investment roadmap, exactly as a professional security architect would do for a client or employer.
:::
