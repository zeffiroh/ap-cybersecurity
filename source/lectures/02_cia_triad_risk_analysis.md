---
deck:
  title: CIA Triad & Risk Analysis
  kicker: Class 2
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 2
  description: Formal CIA definitions, how risk is calculated from likelihood and impact, and the NIST RMF lifecycle.
  topics: [Confidentiality, Integrity, Availability, Risk, Likelihood, Impact, RMF]
---

---
title: CIA Triad & Risk Analysis
cover: true
---
:::text class=sub
Foundational security principles and structured risk assessment methodologies
:::
::::columns
::col::
:::list heading="Core Security Goals" style=plain
- Confidentiality
- Integrity
- Availability
:::
::col::
:::list heading="Key Frameworks" style=chips
- NIST SP 800-30 Rev. 1
- NIST SP 800-37 Rev. 2
- ISO/IEC 27001
:::
::col::
:::list heading="Risk Components" style=plain
- Threat
- Vulnerability
- Impact
:::
::::
:::callout style=soft
The CIA Triad forms the cornerstone of information security, defining the three primary goals that drive the development of security policies, controls, and risk management strategies.
:::

:::image src="images/02_cia_triad_risk_overview.png" alt="Overview diagram linking the CIA Triad (Confidentiality, Integrity, Availability) to risk management frameworks NIST SP 800-30 and ISO 27001, with risk equation Risk = Likelihood × Impact" caption="Class 2 conceptual map: the CIA Triad defines what we protect; risk analysis (Likelihood × Impact) determines prioritization; the NIST RMF operationalizes the continuous protection lifecycle" width=full
:::

:::notes
The CIA Triad, comprising Confidentiality, Integrity, and Availability, represents the foundational model guiding information security practices globally. These three properties were not invented by any single organization but emerged organically through decades of computer security research and were formally codified in standards such as NIST Special Publication 800-33 (Underlying Technical Models for Information Technology Security) and later centralized within FIPS 199 (Standards for Security Categorization of Federal Information and Information Systems). Today, the CIA triad appears in virtually every major security standard, regulation, and framework worldwide, from ISO/IEC 27001 and PCI DSS to HIPAA, GDPR, and the SOC 2 Trust Services Criteria.

Confidentiality ensures that information is accessible only to those authorized to access it. In technical implementations, this is enforced through encryption (AES-256 at rest, TLS 1.3 in transit), access control models (RBAC, ABAC, mandatory access control), and identity verification mechanisms (MFA, PKI certificates). A confidentiality breach can range from accidental disclosure of internal documents to large-scale exposure of personal data, as in the 2018 Marriott breach, where the personal data of approximately 500 million guests was compromised after attackers maintained persistent access to the Starwood guest reservation database for four years (CVE-2018-3983).

Integrity guarantees that data remains accurate and unaltered unless modified by an authorized entity through authorized processes. Integrity mechanisms include cryptographic hashing (SHA-256, SHA-3), digital signatures (RSA, ECDSA), message authentication codes (HMAC), and audit trails. Integrity failures can be subtle or catastrophic: the 2017 NotPetya attack destroyed the Master Boot Records of thousands of systems in Ukraine and global corporations, making data permanently inaccessible, a devastating integrity attack at infrastructure scale.

Availability ensures that information and resources are accessible to authorized users when needed. Redundancy, failover systems, DDoS mitigation, and disaster recovery plans are the primary availability controls. Availability failures have direct operational and financial consequences: in 2021, a ransomware attack on JBS Foods (the world's largest meat processor) forced the shutdown of U.S. beef processing facilities, demonstrating how availability attacks on critical infrastructure translate into real-world supply chain disruptions.

These principles are operationalized through structured risk analysis processes defined in NIST Special Publication 800-30 Rev. 1, which outlines a repeatable, quantifiable methodology for conducting risk assessments, and NIST SP 800-37 Rev. 2, the Risk Management Framework, which integrates risk management into the system development lifecycle. ISO/IEC 27001 complements these efforts by providing a governance framework for establishing, implementing, maintaining, and continually improving an ISMS, with risk treatment at its center. Risk analysis connects the CIA triad to operational decision-making by quantifying the consequences of CIA violations: Risk = Threat × Vulnerability × Impact, where each term can be expressed qualitatively or quantitatively. This equation enables organizations to prioritize protective investments based on where CIA violations are most likely and most damaging, transforming abstract security principles into defensible budget allocations and control selections.
:::

%%%

---
unit: Recap
code: CIA
title: The CIA Triad, Revisited
---
:::callout style=soft
In our previous session, we introduced the foundational principles of information security: **confidentiality**, **integrity**, and **availability**. These principles, colloquially known as the **CIA Triad**, form the cornerstone of most security frameworks and are formally defined by institutions such as the **National Institute of Standards and Technology (NIST)**. Each principle corresponds to a core security objective that informs the design and implementation of protective controls.
:::

:::table
| Principle       | Formal Security Objective                            | Compromised When…                                      |
|----------------|------------------------------------------------------|--------------------------------------------------------|
| Confidentiality | Authorized restriction of information access         | Information is disclosed to unauthorized entities      |
| Integrity       | Safeguarding accuracy and completeness of information | Data is altered, destroyed, or corrupted improperly    |
| Availability    | Ensuring timely and reliable access to information   | Systems or data are inaccessible when needed           |
:::

::::columns
::col::
:::list heading="Confidentiality Mechanisms" style=plain
- Encryption (e.g., AES, TLS)
- Access control lists (ACLs)
- Role-Based Access Control (RBAC)
- Multi-factor authentication (MFA)
:::
::col::
:::list heading="Integrity Mechanisms" style=plain
- Cryptographic hashing (e.g., SHA-256)
- Digital signatures
- Checksums
- Version control systems
:::
::col::
:::list heading="Availability Mechanisms" style=plain
- Redundant systems (e.g., RAID, failover clusters)
- Load balancing
- DDoS mitigation
- Backup and disaster recovery plans
:::
::::

:::image src="images/02_cia_mechanisms_comparison.png" alt="Three-column diagram showing the CIA Triad with specific technical mechanisms listed under each pillar, Confidentiality (encryption, ACLs, MFA), Integrity (hashing, signatures, audit logs), Availability (redundancy, load balancing, backups)" caption="CIA Triad mechanisms: each pillar is supported by a distinct set of technical and administrative controls that collectively address the full spectrum of information security requirements" width=full
:::

:::notes
The CIA Triad is more than just a mnemonic, it is a structured model for understanding and categorizing information security requirements. Each of the three principles is formally recognized in standards such as NIST Special Publication 800-53, which defines security and privacy controls for federal information systems, and FIPS 199, which establishes security categorization based on the potential impact of CIA violations across three levels: Low, Moderate, and High. These impact levels directly determine the baseline security controls that must be implemented, creating a direct regulatory link between CIA principles and operational security practices.

**Confidentiality** ensures that information is accessible only to those who are authorized. This is enforced through a layered approach. At the data layer, encryption converts plaintext to ciphertext using mathematical algorithms, AES-256 is the current NIST-approved standard (FIPS 197) for protecting sensitive unclassified information, while TLS 1.3 (RFC 8446) provides encrypted communication channels between networked systems. At the access control layer, Role-Based Access Control (RBAC) assigns permissions based on organizational roles rather than individual identities, simplifying administration while enforcing least privilege. Attribute-Based Access Control (ABAC) provides more granular control by evaluating multiple attributes of users, resources, and environments simultaneously. Multi-Factor Authentication (MFA) adds verification layers beyond passwords, typically combining something you know (PIN/password), something you have (TOTP token, hardware security key), and/or something you are (biometric). NIST SP 800-63B formally defines authentication assurance levels (AAL1, AAL2, AAL3) and requires MFA at AAL2 and above for high-value systems.

**Integrity** refers to the trustworthiness and accuracy of data over its entire lifecycle. Cryptographic hashing functions like SHA-256 and SHA-3 produce deterministic, fixed-size digests that change dramatically if even a single bit of input changes, a property called the avalanche effect. This makes hashes ideal for detecting unauthorized modifications. Digital signatures combine asymmetric cryptography (RSA, ECDSA, Ed25519) with hashing to provide both integrity verification and non-repudiation: the private key holder signs the message hash, and any recipient with the corresponding public key can verify both that the message is unaltered and that it originated from the key holder. Audit logs and chain-of-custody records provide forensic integrity evidence that is essential for incident investigations and regulatory compliance. The NIST National Software Reference Library (NSRL) uses SHA-256 to maintain reference hashes for known legitimate software files, enabling forensic analysts to quickly distinguish known-good files from potential malware.

**Availability** guarantees that information and systems are accessible to authorized users when needed. The primary threat to availability is denial of service (DoS), which can originate from malicious attacks (volumetric DDoS flooding, application-layer attacks) or unintentional events (hardware failure, natural disasters, software bugs). RAID (Redundant Array of Independent Disks) protects against drive failure through data redundancy; RAID-1 mirrors data across two drives, while RAID-6 adds double parity for tolerance of two simultaneous drive failures. Geographically distributed failover clusters ensure service continuity even during regional outages or datacenter failures. The 3-2-1 backup rule (3 copies, 2 different media types, 1 offsite) protects against data loss from localized disasters. Cloud providers like AWS, Azure, and GCP achieve availability SLAs of 99.9% to 99.999% ("five nines") by distributing workloads across multiple availability zones and regions with automatic failover.

Together, these principles form the foundation for risk assessment, threat modeling, and control selection in cybersecurity frameworks. Every protective measure, from firewalls to intrusion detection systems, is ultimately designed to uphold one or more of these objectives. Understanding the CIA Triad in depth enables security professionals to systematically identify vulnerabilities, assess threats, and implement controls that are proportional to the actual risk of CIA property violations in their specific organizational context.
:::

%%%

---
unit: Goals
code: CIA
title: Confidentiality, Integrity, Availability, In Practice
---
::::columns ratio=1:1:1
::col::
::::card heading="Confidentiality"
:::list style=tight
- Encryption at rest (AES-256, TPMs)
- Encryption in transit (TLS 1.3, IPsec)
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)
- Multi-factor authentication (MFA)
- Data loss prevention (DLP) systems
:::
::::
::col::
::::card heading="Integrity"
:::list style=tight
- Cryptographic hashing (SHA-256, SHA-3)
- Digital signatures (RSA, ECDSA)
- Message authentication codes (HMAC)
- Audit logs and chain of custody
- Version control systems (Git with signed commits)
- Secure boot and firmware validation
:::
::::
::col::
::::card heading="Availability"
:::list style=tight
- Redundant hardware (RAID, failover clusters)
- Geographic replication
- Load balancing (DNS-based, application-level)
- Regular backups (3-2-1 rule)
- Incident response plans
- DDoS mitigation (rate limiting, CDNs, scrubbing centers)
:::
::::
::::

:::image src="images/02_cia_in_practice_examples.png" alt="Real-world CIA implementation examples: encrypted storage and TLS channels for Confidentiality, hash verification chains for Integrity, and multi-datacenter failover for Availability, with example CVEs showing violations of each property" caption="CIA Triad in practice: technical implementations and real-world violation examples demonstrate how each pillar is both implemented and attacked in modern enterprise environments" width=full
:::

:::notes
In practice, the CIA Triad translates into a structured set of security controls that align with both organizational policy and international standards such as NIST SP 800-53 and ISO/IEC 27001. Each pillar is supported by specific technologies and methodologies that defend against real-world threats, and each has been violated in landmark security incidents that illustrate the concrete consequences of security failures.

**Confidentiality in practice** is enforced through encryption mechanisms, AES-256 for data at rest and TLS 1.3 for data in transit, as well as sophisticated access control architectures. TPMs (Trusted Platform Modules), specified in ISO/IEC 11889, provide hardware-rooted key storage for disk encryption (BitLocker, FileVault), ensuring that encryption keys are bound to a specific hardware configuration and cannot be extracted even if storage media is physically stolen. Data Loss Prevention (DLP) systems monitor data flows to detect and block unauthorized transmission of sensitive content, detecting credit card numbers, Social Security numbers, or proprietary code being emailed, uploaded to cloud storage, or copied to removable media. A foundational confidentiality breach is illustrated by CVE-2021-26855 (Microsoft Exchange ProxyLogon), where attackers bypassed authentication to access mailboxes of thousands of organizations, reading confidential emails without decryption because they obtained direct access to the plaintext data.

**Integrity in practice** begins at the firmware level with Secure Boot (UEFI), which verifies cryptographic signatures on each component of the boot chain, firmware, bootloader, kernel, before allowing execution, preventing boot-time malware (bootkits) from establishing persistence below the operating system. SHA-256 hashing provides file integrity verification: when software packages are distributed, publishers include SHA-256 checksums that recipients verify before installation. HMAC (Hash-based Message Authentication Code) combines a shared secret key with hashing to provide both integrity and message authentication in protocols like TLS record authentication and API request signing. Git's object model uses SHA-1 (migrating to SHA-256) to create a tamper-evident chain of commits, where altering any historical commit changes all subsequent commit hashes, making history tampering immediately apparent. A critical integrity violation is CVE-2020-10148, where the SolarWinds Orion update mechanism was compromised to distribute maliciously modified software that appeared to have valid code signatures.

**Availability in practice** is achieved through redundancy at every layer of the infrastructure stack. At the storage layer, RAID arrays protect against disk failure; at the compute layer, clustering and auto-scaling groups provide workload failover; at the network layer, Anycast routing and multiple ISP connections provide path redundancy; at the application layer, CDNs (Content Delivery Networks) distribute content geographically to reduce latency and absorb traffic spikes. DDoS mitigation leverages rate limiting (dropping traffic above threshold), CAPTCHAs to distinguish humans from bots, and specialized scrubbing centers that filter attack traffic before it reaches the origin server. The 3-2-1 backup rule (3 copies of data, on 2 different media types, with 1 copy offsite) protects against localized disasters and ransomware attacks that may encrypt primary backup repositories. A landmark availability violation is the 2016 Mirai botnet DDoS attack against DNS provider Dyn, which disrupted major internet services including Twitter, Netflix, Reddit, and Amazon for hours by flooding Dyn's DNS infrastructure with 1.2 Tbps of traffic from compromised IoT devices.

These controls are foundational to risk management frameworks. Understanding how CIA mechanisms interplay is essential for conducting effective risk analysis: a compensating control for one CIA property may inadvertently weaken another. For example, aggressive logging for availability monitoring may create confidentiality risks if log data contains sensitive information without proper access controls, illustrating why CIA properties must be balanced holistically rather than optimized in isolation.
:::

%%%

---
unit: Risk
code: RSK
title: What Is Risk, Formally?
---

:::callout style=soft
NIST defines **risk** as a measure of the extent to which an entity is threatened by a potential circumstance or event, and is typically expressed as a combination of the **likelihood** that a particular threat will occur and the **impact** it would have if it did occur.
:::

:::flow
Threat → Exploits → Vulnerability → Leads to → Impact  
Likelihood × Impact = Risk
:::

:::pullquote
Risk = Likelihood × Impact
:::

:::text
This foundational equation underpins most formal risk assessment methodologies, including those outlined in **NIST SP 800-30 Rev. 1**, *Guide for Conducting Risk Assessments*, and aligns with **ISO/IEC 27005** for information security risk management.
:::

::::columns
::col::
:::list heading="Core Components of Risk"
- Threat
- Vulnerability
- Likelihood
- Impact
:::
::col::
:::list heading="Risk Outcomes"
- Confidentiality Breach
- Integrity Corruption
- Availability Loss
:::
::::

:::image src="images/02_risk_equation_diagram.png" alt="Diagram showing the risk equation: a Threat Source (with Motivation and Capability) exploiting a Vulnerability (weakness in a system) to produce an Impact against CIA properties, with Likelihood as the probability arrow and Risk as the combined result" caption="Formal risk decomposition: risk is the product of Likelihood (the probability that a threat source with sufficient motivation and capability will exploit a vulnerability) and Impact (the magnitude of CIA property violation that results)" width=full
:::

:::notes
In cybersecurity, **risk** is not merely a buzzword, it is a quantifiable and analyzable construct rooted in formal definitions provided by standards bodies like NIST and ISO. According to **NIST Special Publication 800-30 Rev. 1** (*Guide for Conducting Risk Assessments*, 2012), risk is defined as "a measure of the extent to which an entity is threatened by a potential circumstance or event, and is typically a function of: (1) the **adverse impact** that would arise if the circumstance or event occurs, and (2) the **likelihood** of occurrence." This definition is operationally precise: it specifies that risk is not merely the existence of a threat or vulnerability, but the probabilistic product of both a threatening event occurring and the damage that event would cause.

The formal risk definition emphasizes two critical dimensions. First, risk requires a **potential** for harm, a threat that could materialize under the right conditions. Second, risk is inherently **uncertain**, it is a probabilistic estimate rather than a certainty. This probabilistic nature is why risk management is a continuous, iterative process rather than a one-time determination: as threat landscapes evolve, new vulnerabilities are discovered, and organizational environments change, risk levels change accordingly and must be reassessed.

To operationalize the risk definition, we decompose risk into four core components:

**Threat**: A potential cause of an unwanted incident that may result in harm to a system or organization. Threats can be intentional (an attacker actively seeking to exploit a vulnerability), unintentional (a user accidentally deleting critical files), or environmental (a flood damaging server infrastructure). NIST categorizes threat sources as Adversarial (malicious actors), Accidental (human errors), Structural (equipment failures), and Environmental (natural disasters). Characterizing the threat source, including its capability, intent, and targeting, is the first step in risk assessment.

**Vulnerability**: A weakness or gap in security practices, procedures, or technologies that can be exploited by a threat. Vulnerabilities exist at every layer of the technology stack: software vulnerabilities (unpatched CVEs, coding errors), configuration weaknesses (default credentials, excessive permissions), process gaps (inadequate incident response procedures), and human factors (untrained users, susceptibility to social engineering). The vulnerability must be both present and exploitable by the identified threat source for risk to exist, a zero-day exploit is irrelevant to an organization if no systems running the affected software are deployed.

**Likelihood**: The probability that a given threat source will successfully exploit a specific vulnerability within a defined time period. Likelihood assessment integrates threat source characteristics (capability, motivation, access) with vulnerability characteristics (exploitability, exposure, existing controls). NIST SP 800-30 provides a five-level qualitative likelihood scale (Very Low, Low, Moderate, High, Very High) that organizations map to quantitative probabilities in their specific context.

**Impact**: The magnitude of harm resulting from a threat successfully exploiting a vulnerability. Impact is assessed across CIA dimensions and expressed in operational terms (system downtime, data loss) or financial terms (recovery costs, regulatory fines, reputational damage). The fundamental risk equation, **Risk = Likelihood × Impact**, enables organizations to prioritize risks: a low-likelihood event with catastrophic impact may warrant more investment than a high-likelihood event with minimal impact. This equation is central to NIST SP 800-30, ISO/IEC 27005, FAIR (Factor Analysis of Information Risk), and virtually every other formal risk analysis framework used in cybersecurity today.

Understanding this formal definition is the prerequisite for every subsequent risk analysis activity in this course, likelihood assessment, impact analysis, risk matrix construction, and risk treatment selection all flow directly from this foundational framework.
:::

%%%

---
unit: Risk
code: RSK
title: Likelihood, How Probable Is It?
---
:::table
| Rating   | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| Low      | Threat source lacks motivation or capability; existing controls are effective |
| Moderate | Threat source is motivated and capable; some controls may fail               |
| High     | Threat source is highly motivated and capable; controls are insufficient     |
:::

:::callout style=line
Likelihood integrates two core components: the **threat source** (its intent and ability) and the **vulnerability** (the ease of exploitation). It reflects not just the possibility of an attack, but how realistically it could occur given current conditions.
:::

:::image src="images/02_likelihood_assessment_matrix.png" alt="Likelihood assessment matrix with Threat Source Capability on one axis and Vulnerability Exploitability on the other, producing Low/Moderate/High likelihood ratings in each cell, with example CVE scenarios annotated" caption="Likelihood assessment matrix: combining threat source capability and motivation with vulnerability exploitability produces a structured likelihood rating that feeds the overall risk equation" width=half
:::

:::notes
Likelihood is a foundational element of risk assessment, representing the probability that a given threat will exploit a specific vulnerability within a defined operational context and timeframe. In cybersecurity risk management frameworks such as NIST SP 800-30 Rev. 1, likelihood is not simply an intuitive guess but a structured analytical judgment that integrates two distinct domains of analysis: the **threat source characteristics** and the **vulnerability characteristics**.

The **threat source** analysis evaluates the adversary's **motivation** (the reason they would target this asset), **capability** (the technical skills, tools, and resources they possess), and **access** (whether they can reach the vulnerable system). A threat source with high motivation, sophisticated capability, and direct access to the vulnerable system produces maximum likelihood, while a threat source lacking any of these three factors produces minimal likelihood. For example, a nation-state APT group (extremely high capability) targeting a defense contractor's intellectual property (high motivation) through an internet-exposed application (direct access) creates a High likelihood scenario even if controls exist, because APT groups are known to use zero-day exploits and custom tooling that bypasses standard defenses.

The **vulnerability characteristics** analysis evaluates how easily the vulnerability can be exploited given current defensive conditions. The CVSS Attack Complexity (AC) metric is a standardized proxy for this: AC:L (Low complexity) indicates exploitation is straightforward and repeatable, while AC:H (High complexity) indicates exploitation requires special conditions or significant preparation. The presence of exploit code in the wild (captured in the CVSS Exploit Code Maturity temporal metric and in threat intelligence from sources like the CISA Known Exploited Vulnerabilities catalog) dramatically increases practical exploitability beyond what the theoretical CVSS Base Score suggests.

A **Low** likelihood rating indicates that either the attacker lacks interest or the necessary means, or that existing security controls (firewalls, IDS, access controls, patch deployment) are robust enough to deter or prevent exploitation. For instance, a vulnerability requiring physical hardware access (CVSS AV:P) in an organization with strict physical security controls and no external threat actors with physical access would receive a Low likelihood rating.

A **Moderate** rating suggests that motivated attackers with adequate capability exist, but current controls provide meaningful resistance. A production web server running outdated middleware with known CVEs, protected by a WAF but without active monitoring, might receive Moderate likelihood, the controls exist but may not provide complete protection against a determined, sophisticated attacker.

A **High** likelihood rating implies a capable and determined threat actor facing minimal effective resistance: either controls are absent, misconfigured, or known to be ineffective against the threat actor's TTPs. The exploitation of CVE-2017-0144 (EternalBlue) by the WannaCry ransomware campaign in May 2017 exemplifies a High likelihood scenario at global scale: the vulnerability was internet-exploitable with no authentication required, over 200,000 organizations had not applied the available Microsoft patch (MS17-010) in the two months since its release, and the exploit code was publicly available through the NSA's Shadow Brokers leak. The result was over $4 billion in global damages within days.

Understanding likelihood assessment enables organizations to prioritize defensive investments not merely based on vulnerability severity (CVSS scores) but on the realistic probability of exploitation given the specific threat environment they face, a more operationally actionable risk metric.
:::

%%%

---
unit: Risk
code: RSK
title: Impact, How Bad Would It Be?
---

::::columns
::col::
:::table
| Rating   | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| Low      | Limited adverse effect on operations, assets, or individuals                |
| Moderate | Serious adverse effect, significant damage, financial loss, or harm        |
| High     | Severe or catastrophic adverse effect, loss of life, mission failure, etc. |
:::

::col::
:::callout style=line
Impact is evaluated in the context of the **CIA Triad**:  
**Confidentiality**, **Integrity**, or **Availability**, and **how severely** each is compromised.
:::
::::

:::list heading="Impact Analysis Factors" style=plain
- Nature of the asset affected (e.g., public data vs. PII, mission-critical systems)
- Scope of compromise (single user vs. enterprise-wide outage)
- Duration of impact (temporary vs. permanent damage)
- Regulatory and compliance consequences (e.g., GDPR, HIPAA violations)
- Reputational and financial implications
:::

:::image src="images/02_impact_analysis_dimensions.png" alt="Impact analysis radar chart showing five impact dimensions, operational, financial, regulatory, reputational, and safety, with Low/Moderate/High ratings plotted for an example ransomware attack on a hospital system" caption="Multi-dimensional impact analysis: a single security incident can simultaneously affect operational continuity, financial performance, regulatory compliance, organizational reputation, and (in critical systems) human safety" width=half
:::

:::notes
In cybersecurity risk analysis, **impact** refers to the **severity of consequences** that would result from a successful threat exploitation of a specific vulnerability. While likelihood addresses the probability of an event occurring, impact addresses the **magnitude of damage** if it does occur. This distinction is fundamental to risk prioritization: a highly likely but low-impact event may warrant less investment than a rare but catastrophic one. The asymmetry between likelihood and impact is particularly pronounced in cybersecurity, where rare events like nation-state attacks or zero-day exploits can cause unprecedented harm.

Impact is formally assessed using a standardized scale, Low, Moderate, and High, as defined in frameworks like NIST SP 800-30 Rev. 1 and FIPS 199, which provide specific criteria for each level based on operational consequences. NIST SP 800-60 further provides a comprehensive mapping of specific information types (tax records, healthcare data, financial data, national security information) to impact levels, enabling consistent classification across organizations and sectors.

Critically, impact must be **evaluated against all three CIA dimensions simultaneously**, as a single incident may violate multiple properties:

**Confidentiality impact**: Unauthorized disclosure of information. The severity depends on the sensitivity of the information type. Disclosure of public press releases has negligible impact; disclosure of trade secrets may cost hundreds of millions in competitive advantage; disclosure of personally identifiable information (PII) triggers regulatory reporting obligations (72-hour GDPR notification, HIPAA breach notification) and may result in fines, class action lawsuits, and long-term reputational damage. The EternalBlue-related CVE-2017-0144 exploitation in WannaCry primarily targeted availability, but related campaigns such as NotPetya also exfiltrated credentials, combining confidentiality and availability impact.

**Integrity impact**: Unauthorized modification or destruction of data. Integrity impacts are often the most underestimated, as they may be difficult to detect and may require complete data restoration or recreation. Ransomware attacks that encrypt files violate integrity (files are modified to encrypted forms) before violating availability (files are inaccessible). Silent data corruption, where data is altered without obvious indicators, may go undetected for months or years, propagating incorrect information throughout dependent systems. The 2016 Bangladesh Bank heist demonstrated integrity impact: attackers modified SWIFT financial transfer instructions (CVE-2016-4330 related infrastructure), redirecting $81 million before the fraud was detected.

**Availability impact**: Disruption of access to systems or data. The severity depends on the criticality of the affected system and the duration of disruption. A temporary unavailability of a public-facing marketing website has Low impact; a one-hour outage of an online banking system during peak hours has Moderate impact (customer frustration, SLA penalties, quantifiable transaction losses); a multi-day ransomware-induced outage of a hospital's electronic health records system has potentially High or even life-threatening impact, as clinicians lose access to medication histories, allergy records, and diagnostic information.

Five key dimensions frame impact analysis beyond the CIA triad: **Operational** impact measures the degree to which business processes are disrupted; **Financial** impact encompasses direct costs (incident response, legal fees, regulatory fines) and indirect costs (lost business, remediation); **Regulatory** impact reflects penalties and compliance violations under applicable laws; **Reputational** impact captures brand damage and customer trust erosion (often persisting years beyond the incident itself); and **Safety** impact applies specifically to operational technology (OT) and industrial control systems where cyber incidents can directly threaten physical safety, as demonstrated by the 2021 Oldsmar, Florida water treatment plant attack, where an attacker remotely adjusted sodium hydroxide levels to potentially dangerous concentrations.

Understanding impact in these multi-dimensional terms transforms risk assessment from a purely technical exercise into a business risk management discipline, enabling CISOs and executives to make informed decisions about security investments using the same risk language as financial, legal, and operational leadership.
:::

%%%

---
unit: Risk
code: RSK
title: The Risk Matrix
---

::::columns
::col::
:::table
| | **Impact: Low** | **Impact: Moderate** | **Impact: High** |
|---|---|---|---|
| **Likelihood: Low** | Low | Low | Moderate |
| **Likelihood: Moderate** | Low | Moderate | High |
| **Likelihood: High** | Moderate | High | High |
:::
::col::
:::callout
The risk matrix is a qualitative risk assessment tool that maps the intersection of likelihood and impact to produce an overall risk rating. It enables decision-makers to prioritize risks based on their potential effect on organizational objectives and available resources.
:::
::::

:::text
The risk matrix serves as a foundational mechanism in information security risk management, widely referenced in standards such as **NIST SP 800-30 Rev. 1** ("Guide for Conducting Risk Assessments") and **ISO/IEC 27005** ("Information Security Risk Management"). These frameworks emphasize that risk is a function of likelihood and impact:

$$ \text{Risk} = \text{Likelihood} \times \text{Impact} $$

While quantitative analysis uses precise metrics, many organizations adopt qualitative matrices for practicality and communication clarity.
:::

:::list heading="Key Interpretations of Risk Levels:"
- **Low Risk**: Events that are unlikely and would cause minimal damage. Often accepted without further action.
- **Moderate Risk**: Events with either moderate likelihood or impact, or both. Requires monitoring and possible mitigation.
- **High Risk**: Events that are highly likely and/or would cause severe damage. Demands immediate management attention and mitigation.
:::

:::image src="images/02_risk_matrix_annotated.png" alt="Color-coded 3x3 risk matrix with Likelihood on the y-axis (Low/Moderate/High) and Impact on the x-axis (Low/Moderate/High), with each cell color-coded green/yellow/red and annotated with real-world cybersecurity scenario examples" caption="Annotated risk matrix: the intersection of Likelihood and Impact produces Low (green), Moderate (yellow), or High (red) risk ratings, each cell is annotated with a representative cybersecurity scenario to calibrate practical judgment" width=full
:::

:::notes
The risk matrix is a qualitative tool used to assess and prioritize risks by evaluating two core dimensions: **likelihood** (how probable a threat event is to occur) and **impact** (the severity of consequences if it does occur). Developed to provide a standardized, visually intuitive risk communication mechanism, the risk matrix appears in virtually every major security risk framework: NIST SP 800-30 Rev. 1, ISO/IEC 27005, NIST CSF, FAIR (Factor Analysis of Information Risk), OCTAVE (Operationally Critical Threat, Asset, and Vulnerability Evaluation), and the U.K. National Cyber Security Centre (NCSC) risk management guidance. Its enduring utility lies in its ability to translate complex, multi-variable risk assessments into a format accessible to non-technical executive audiences who must make resource allocation decisions.

The 3×3 matrix structure presented here, mapping Low/Moderate/High Likelihood against Low/Moderate/High Impact, produces nine cells that collapse into three risk rating zones. This structure, while simple, captures the essential non-linearity of risk: Low-Likelihood × High-Impact events (the upper-right cell) receive a Moderate rather than High rating, acknowledging that probability matters even when potential consequences are severe. This calibration prevents organizations from devoting excessive resources to extremely unlikely catastrophic scenarios at the expense of more probable moderate-impact events.

Real-world calibration of the matrix cells with concrete cybersecurity scenarios enhances its analytical utility. The High×High cell (maximum risk rating) maps to scenarios like a known, actively exploited vulnerability on an internet-facing server containing production customer PII, high probability of exploitation, catastrophic regulatory and financial impact. The High×Low cell (Moderate risk) maps to high-frequency, low-sophistication attacks like automated brute-force attempts against a public-facing SSH server with MFA enabled, very high likelihood of attempts, but minimal impact because the control renders each attempt ineffective. The Low×High cell (Moderate risk) maps to sophisticated nation-state APT targeting, extremely high impact if successful, but low likelihood for most organizations that are not high-value intelligence targets.

In practice, a **high-impact, low-likelihood** event (such as a zero-day exploit like CVE-2021-44228, Log4Shell before its public disclosure) may still justify preventive investment in vulnerability scanning and network traffic monitoring, even if the probability of being specifically targeted is low. The **high-likelihood, low-impact** events (like frequent automated phishing attempts against a well-trained workforce) may justify maintaining existing email filtering controls without additional investment, accepting the residual risk. Only when both dimensions are high, such as a widespread ransomware campaign targeting unpatched systems in a known-vulnerable industry, does the matrix yield a definitive High risk rating requiring urgent executive escalation and emergency response.

Larger organizations often employ 5×5 matrices with five likelihood and five impact levels, providing more granular differentiation across the risk spectrum. Some frameworks also use log-scale matrices where the axes represent order-of-magnitude differences in probability or financial impact, better capturing the vast range of risk scenarios in complex environments. Regardless of matrix size, the fundamental principle remains: **Risk = Likelihood × Impact**, and the matrix's value lies in transforming subjective assessments into a shared organizational understanding of risk that enables consistent, defensible decision-making.
:::

%%%

---
unit: Risk
code: RSK
title: Risk Evaluation, Responding to Risk
---
::::columns
::col::
:::table
| Response  | Definition                                 | Example                                      |
|-----------|--------------------------------------------|----------------------------------------------|
| Accept    | Acknowledge risk without further action    | Cost of mitigation exceeds expected loss     |
| Avoid     | Eliminate the source of the risk           | Discontinue use of an insecure legacy system |
| Mitigate  | Apply controls to reduce likelihood/impact | Deploy MFA, apply security patches           |
| Transfer  | Shift risk liability to another party      | Purchase cyber insurance, outsource services |
:::
::col::
:::callout
Risk response strategies are not mutually exclusive and may be used in combination depending on organizational context, regulatory requirements, and risk appetite.
:::
::::

:::flow
Identify and Assess Risks (SP 800-30 Methodology)
Evaluate Against Organizational Risk Tolerance
Select Risk Response Strategy (Accept/Avoid/Mitigate/Transfer)
Implement Selected Controls and Risk Transfer Mechanisms
Monitor Residual Risk and Control Effectiveness
Reassess Periodically and After Significant Changes
:::

:::image src="images/02_risk_response_strategies.png" alt="Four-quadrant diagram of risk response strategies, Accept (low risk, low cost), Avoid (risk elimination), Mitigate (control implementation), Transfer (insurance/outsourcing), with decision criteria for selecting each strategy" caption="Risk response selection framework: the choice between Accept, Avoid, Mitigate, and Transfer depends on risk rating, cost-benefit analysis, regulatory requirements, and organizational risk appetite" width=half
:::

:::notes
After identifying and analyzing risks, organizations must determine how to respond to each risk based on its level, the cost of available responses, regulatory requirements, and organizational risk appetite. The National Institute of Standards and Technology (NIST) Special Publication 800-30 and ISO/IEC 27005 both define four primary risk response strategies: **Accept**, **Avoid**, **Mitigate**, and **Transfer**. These are not merely academic categories but operational decision frameworks that directly determine how security budgets are allocated and what controls are deployed.

**Accepting** a risk represents a deliberate, documented organizational decision to acknowledge the existence of a risk without implementing additional controls. Risk acceptance is not ignorance or negligence, it is a formal governance decision made when the cost or operational impact of mitigation exceeds the expected loss from the risk materializing, or when the risk falls within the organization's formally defined risk tolerance. For example, a small business might formally accept the risk of a low-sophistication phishing attack on a non-critical shared email account if deploying an enterprise email security gateway costs $50,000 annually but the expected financial impact of a successful attack is less than $5,000. Risk acceptance must be documented, reviewed periodically, and approved by the appropriate risk acceptance authority, typically the system owner or a risk management committee, to remain a valid governance posture rather than passive negligence.

**Avoiding** risk involves eliminating the activity, system, or configuration that creates the risk in the first place. Risk avoidance is conceptually simple but often operationally challenging: it may require discontinuing business activities, decommissioning legacy systems, or fundamentally changing business processes. For instance, an organization running an end-of-life database system (no longer receiving security patches) might avoid the associated risk by migrating to a supported version. However, avoidance is not always feasible when the risky activity is integral to business operations. A healthcare organization cannot avoid the risk of patient data breaches simply by not storing patient records, their regulatory and operational mandate requires it. In such cases, avoidance of the specific risk must give way to mitigation or transfer.

**Mitigation** is the most commonly applied strategy and involves implementing safeguards that reduce either the likelihood of exploitation or the magnitude of impact. Technical mitigations include patching (reducing exploitability of known CVEs), deploying MFA (reducing credential-based attack success rates), implementing network segmentation (reducing lateral movement capability), and deploying endpoint detection and response (EDR) tools (reducing mean time to detect and respond to breaches). Administrative mitigations include security awareness training (reducing social engineering success rates), implementing change management processes (reducing misconfiguration risk), and establishing incident response procedures (reducing impact by enabling rapid containment). Effective mitigation operates on both likelihood and impact dimensions simultaneously, a well-implemented MFA deployment reduces the likelihood that stolen credentials will be usable while also reducing the impact of phishing campaigns by limiting their ultimate effectiveness. NIST SP 800-53 provides the comprehensive catalog of technical and administrative mitigations aligned to specific risk scenarios.

**Transferring** risk does not eliminate the underlying vulnerability or threat, it shifts the financial liability of adverse outcomes to a third party. Cyber insurance policies have become a standard risk transfer mechanism, covering incident response costs, business interruption losses, regulatory fines, legal fees, and data breach notification costs. The cyber insurance market has grown significantly as organizations recognize the financial exposure from cyber incidents: the average cost of a data breach reached $4.45 million in 2023 (IBM Cost of a Data Breach Report). However, insurance providers have become increasingly sophisticated in their requirements, often demanding evidence of specific security controls (MFA, EDR, backup procedures) as conditions of coverage. Outsourcing security operations to managed security service providers (MSSPs) or managed detection and response (MDR) providers is another form of risk transfer, the provider assumes operational responsibility for detection and response. Importantly, regulatory liability generally cannot be transferred: even if an MSSP fails to detect an incident, the regulated organization remains responsible for GDPR, HIPAA, or PCI DSS compliance penalties.

Each risk response strategy must be evaluated within the organization's formally defined **risk appetite** (the amount of risk the organization is willing to pursue) and **risk tolerance** (the acceptable variance around risk appetite). These governance parameters, defined in frameworks such as ISO 31000 (Risk Management Principles and Guidelines), prevent ad hoc risk decisions and ensure that risk responses are coherent with overall business strategy.
:::

%%%

---
unit: RMF
code: RMF
title: The NIST Risk Management Framework
---
:::callout style=soft
The **NIST Risk Management Framework (RMF)** provides a structured, lifecycle-based approach for integrating information security and risk management into system development and operations. Originally defined in NIST Special Publication 800-37, RMF aligns with broader federal security mandates such as FISMA and supports both federal and non-federal organizations in managing cybersecurity risk throughout the system lifecycle, from initiation to disposal.
:::

:::steps
**Prepare**, Establish the organization's risk management strategy, roles, and context.
**Categorize**, Determine the system's impact level based on the potential harm from a security breach (aligned with FIPS 199 and NIST SP 800-60).
**Select**, Choose appropriate security controls from NIST SP 800-53 based on system categorization and organizational priorities.
**Implement**, Integrate the selected controls into system and organizational processes.
**Assess**, Evaluate control effectiveness through testing, monitoring, and evaluation (aligned with NIST SP 800-115).
**Authorize**, Senior officials make risk-based decisions to authorize system operation (known as "Authorization to Operate" or ATO).
**Monitor**, Continuously assess and update the system's security posture in response to environmental and threat changes.
:::

::::columns
::col::
:::callout style=line
**Key Standards & Documents**
- NIST SP 800-37 Rev. 2: RMF for Systems and Organizations
- NIST SP 800-53: Security and Privacy Controls
- NIST SP 800-60: Guide for Mapping Types of Information and Systems to Security Categories
- FIPS 199: Standards for Security Categorization
:::
::col::
:::callout style=line
**RMF in Practice**
Used across U.S. federal agencies and adopted by private sector organizations for:
- Compliance with regulatory frameworks
- Structured risk-based decision-making
- Continuous authorization and real-time risk awareness
:::
::::

:::image src="images/02_nist_rmf_lifecycle.png" alt="NIST Risk Management Framework seven-step lifecycle diagram showing Prepare, Categorize, Select, Implement, Assess, Authorize, and Monitor in a circular flow with supporting NIST publication references at each step" caption="NIST RMF lifecycle: seven iterative steps convert organizational risk management strategy into implemented, continuously monitored security controls, the framework is used by all U.S. federal agencies under FISMA" width=full
:::

:::notes
The **NIST Risk Management Framework (RMF)** is a comprehensive, iterative process for managing risk throughout the system development lifecycle (SDLC). It is defined in NIST Special Publication 800-37 Revision 2 (*Risk Management Framework for Information Systems and Organizations: A System Life Cycle Approach for Security and Privacy*, 2018) and serves as the cornerstone for federal information systems' security management under the Federal Information Security Modernization Act (FISMA). The RMF is not just a compliance checklist but a strategic approach that integrates technical, operational, and management components to ensure that cybersecurity is embedded into every phase of a system's existence, from initial design decisions through operational deployment to eventual decommissioning.

Revision 2 of SP 800-37 introduced significant enhancements over the original framework, most notably adding the **Prepare** step at the beginning of the lifecycle, emphasizing organizational-level preparation before any individual system is categorized or assessed. This addition reflects a mature understanding that successful risk management requires institutional readiness, defined roles, executive commitment, risk management processes, and organizational risk tolerance statements, before system-specific controls can be meaningfully selected and implemented.

The seven RMF steps form an integrated lifecycle:

**Step 1: Prepare** establishes the organizational and system-level context for risk management. At the organizational level, this includes defining risk management roles (Risk Executive, Authorizing Official, System Owner, Information System Security Officer/ISSO, Information System Security Manager/ISSM), documenting organizational risk tolerance, and selecting common controls that can be inherited by multiple systems. At the system level, this includes identifying and registering the system, conducting a preliminary risk assessment, defining the system boundary, and identifying stakeholders.

**Step 2: Categorize** determines the information system's impact level, Low, Moderate, or High, based on the potential adverse impact on the organization if confidentiality, integrity, or availability are compromised. This categorization follows FIPS 199 (Standards for Security Categorization) and is guided by NIST SP 800-60 (Guide for Mapping Types of Information and Information Systems to Security Categories), which provides detailed mapping tables for hundreds of information types across executive branch agencies. The impact level drives all subsequent control selection decisions.

**Step 3: Select** identifies the baseline set of security controls from NIST SP 800-53 appropriate to the categorization level. Low-impact systems use the Low baseline (approximately 35 controls), Moderate-impact systems use the Moderate baseline (approximately 180 controls), and High-impact systems use the High baseline (approximately 230 controls). These baselines are tailored to the organization's environment, controls may be scoped, parameterized, or supplemented based on specific threats, regulatory requirements, or mission needs.

**Step 4: Implement** deploys the selected controls into the system architecture and operational processes. This includes configuring hardware and software, establishing procedures, deploying monitoring tools, and documenting the implementation in a System Security Plan (SSP). Implementation requires close collaboration between security professionals and system developers, operations personnel, and business stakeholders.

**Step 5: Assess** evaluates the effectiveness of implemented controls through a combination of interviews, document reviews, observation, and technical testing (aligned with NIST SP 800-115, Technical Guide to Information Security Testing and Assessment). The assessment produces a Security Assessment Report (SAR) documenting control effectiveness, deficiencies, and recommendations. Independent assessors (distinct from the implementation team) provide objective evaluation.

**Step 6: Authorize** involves a senior organizational official (the Authorizing Official or AO) making a risk-based decision to authorize the system for operation. The AO reviews the SSP, SAR, and Plan of Action and Milestones (POA&M) documenting remediation plans for identified deficiencies, and makes a formal Authorization to Operate (ATO) decision, acknowledging and accepting residual risk. ATOs are time-limited (typically one to three years) and must be renewed, ensuring periodic reassessment.

**Step 7: Monitor** continuously tracks the security posture of authorized systems through ongoing assessment of controls, monitoring of threat environment changes, and management of configuration changes. This step implements the guidance in NIST SP 800-137 (Information Security Continuous Monitoring) and supports transition from periodic authorization to a continuous authorization model where risk decisions are updated in near-real-time. The Log4Shell vulnerability (CVE-2021-44228) highlighted the critical importance of robust Monitor-phase capabilities: organizations with strong continuous monitoring programs detected and began remediating the vulnerability within hours of its disclosure, while those without adequate monitoring took weeks or months, creating dramatically different risk exposure windows.
:::

%%%

---
unit: RMF
code: RMF
title: RMF in Practice
---
:::callout style=line
The Risk Management Framework (RMF) is a dynamic, iterative process, not a static checklist. It emphasizes continuous risk assessment and adaptive security management throughout the system lifecycle.
:::

::::columns
::col::
:::flow
Prepare
Categorize
Select
Implement
Assess
Authorize
Monitor
:::
::col::
:::list heading="Key Attributes of RMF in Practice" style=plain
- Iterative and adaptive
- Risk-driven decision-making
- Continuous authorization
- Feedback loops between phases
:::
::::

:::pullquote
A system is never "done" being secured, it's continuously managed.
:::

:::image src="images/02_rmf_continuous_monitoring.png" alt="Diagram showing the RMF lifecycle with feedback arrows from Monitor back to all earlier steps, and a continuous monitoring timeline below showing ongoing control assessments, vulnerability scans, and threat updates between formal authorization cycles" caption="RMF as a continuous lifecycle: the Monitor phase feeds back into all upstream steps as threats evolve, vulnerabilities are discovered, and systems change, continuous authorization replaces periodic compliance checkpoints" width=full
:::

:::notes
The NIST Risk Management Framework (RMF), defined in NIST Special Publication 800-37, is not a linear, one-time compliance process. Rather, it is a cyclical and adaptive methodology designed to integrate security and risk management into the system development lifecycle (SDLC) continuously. Each of the seven steps, Prepare, Categorize, Select, Implement, Assess, Authorize, and Monitor, informs and influences the others, creating feedback loops essential for maintaining security posture over time. This iterative nature distinguishes RMF from simpler compliance frameworks that treat security as a periodic checklist rather than an ongoing operational discipline.

In practice, the iterative nature of RMF manifests in several ways. When a significant vulnerability is discovered in a system component, as with Log4Shell (CVE-2021-44228) in 2021 or EternalBlue (CVE-2017-0144) in 2017, the Monitor step detects the vulnerability, triggers a return to the Assess step to evaluate control effectiveness against the new threat, potentially drives updates in the Select step if new controls are needed, leads to Implement activity to deploy patches or compensating controls, and may require a reassessment at the Authorize step if the residual risk exceeds the AO's risk acceptance threshold. This complete loop can happen within days or weeks for critical vulnerabilities, far faster than a traditional annual assessment cycle.

The concept of **continuous authorization** represents the evolution of the traditional ATO model. Rather than conducting comprehensive assessments every one to three years and operating on the assumption that the security posture is static between assessments, continuous authorization maintains a near-real-time risk picture by continuously collecting and analyzing security metrics. NIST SP 800-137 (Information Security Continuous Monitoring) provides detailed guidance on implementing information security continuous monitoring (ISCM) programs, including the selection and monitoring of security metrics, ongoing assessment frequencies, and automated security reporting. Tools such as SIEM platforms, vulnerability scanners, configuration management databases (CMDBs), and security orchestration platforms provide the automation backbone for continuous monitoring at scale.

The organizational implications of RMF in practice extend beyond technical implementation. Effective RMF requires clear governance structures: Authorizing Officials must have sufficient seniority and risk management authority to make meaningful risk acceptance decisions; Information System Security Officers (ISSOs) must maintain current knowledge of the systems they oversee; and organizational risk executives must coordinate risk management activities across the entire system portfolio to prevent fragmented, siloed risk decisions. The Prepare step's emphasis on organizational-level readiness, establishing these governance structures before system-specific activities begin, reflects hard-won lessons from organizations that deployed RMF technically but without adequate governance support.

Security professionals entering the field should understand that RMF is not merely a government compliance exercise. Its fundamental principles, continuous monitoring, risk-based control selection, authorized risk acceptance, and iterative improvement, represent best practices applicable to any organization managing information systems in a dynamic threat environment. Private-sector organizations that adopt RMF's continuous improvement philosophy alongside their industry-specific compliance frameworks (PCI DSS, HIPAA, SOC 2, ISO 27001) achieve more resilient security programs than those that treat compliance as the ceiling rather than the floor of their security investment.
:::

%%%

---
unit: Summary
code: SUM
title: Putting Risk Analysis to Work
---
::::columns
::col::
:::callout style=soft
Confidentiality, integrity, and availability define what we protect. Likelihood and impact turn threats and vulnerabilities into a measurable risk. The RMF makes managing that risk a continuous, repeatable process, not a one-time fix.
:::
::col::
:::list style=chips
- Confidentiality
- Integrity
- Availability
- Likelihood
- Impact
- Risk Matrix
- RMF
:::
::::
::::card
:::table
| Risk Level     | Likelihood × Impact | Example Scenario                        |
|----------------|---------------------|-----------------------------------------|
| High           | High × High         | Data breach exposing customer PII       |
| Medium         | Medium × Medium     | Temporary service degradation           |
| Low            | Low × Low           | Minor configuration error, no exposure  |
:::
::::
:::steps
1. Identify risks using asset, threat, and vulnerability assessments.
2. Analyze likelihood and impact to quantify risk exposure.
3. Evaluate risk against organizational risk tolerance (NIST SP 800-30).
4. Select risk response: Accept, Avoid, Mitigate, or Transfer.
5. Implement controls aligned with selected response.
6. Monitor and review risk posture continuously.
7. Improve risk analysis and response mechanisms iteratively.
:::

:::image src="images/02_risk_analysis_workflow_summary.png" alt="End-to-end risk analysis workflow diagram showing seven steps from asset identification through continuous improvement, with CIA Triad, NIST SP 800-30 risk equation, and RMF lifecycle icons annotated at each relevant step" caption="Risk analysis synthesis: the complete workflow from CIA property identification through asset inventory, threat and vulnerability assessment, risk quantification, response selection, and continuous monitoring under the NIST RMF" width=full
:::

:::notes
At the heart of information security lies the CIA triad, confidentiality, integrity, and availability, which collectively define the core attributes of information that we seek to protect. However, understanding *what* to protect is only the first step in a rigorous security program. To operationalize security, we must assess *how likely* it is that a threat will exploit a vulnerability, and what the *impact* would be if it did. This transformation of qualitative threat data into quantifiable, prioritized risk is the essence of risk analysis, and it is what separates reactive security from proactive, risk-informed security management.

Risk is expressed as a function: **Risk = Likelihood × Impact**. This deceptively simple equation embeds enormous analytical depth. Likelihood requires assessing threat source characteristics (capability, motivation, access) and vulnerability exploitability (CVSS scores, exploit availability, existing controls). Impact requires assessing consequences across CIA dimensions (confidentiality breach severity, integrity corruption extent, availability disruption duration) and translating technical impacts into business terms (financial loss, regulatory exposure, reputational damage). The equation's multiplicative structure means that either dimension independently drives risk level: a near-certain minor incident and a rare catastrophic incident may warrant equal attention depending on organizational risk tolerance.

The **risk matrix** provides a visual prioritization mechanism that makes risk assessments accessible to executive leadership. By mapping likelihood against impact in a structured grid, security teams can communicate complex risk landscapes in a format that enables rapid prioritization and resource allocation decisions. The matrix's simplicity is a feature rather than a limitation, it forces clarity and consensus about relative risk ratings that might otherwise remain ambiguous in purely numerical analyses.

The **Risk Management Framework (RMF)**, defined in NIST SP 800-37, operationalizes risk analysis into a continuous organizational discipline. Its seven steps, Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor, ensure that risk management is not a one-time compliance activity but an embedded, iterative operational practice. The Monitor step's continuous feedback into earlier phases creates the adaptive capability needed to respond to the rapidly evolving threat landscape: new vulnerabilities, emerging threat actors, changing business processes, and shifting regulatory requirements all demand ongoing risk reassessment.

Risk responses, Accept, Avoid, Mitigate, Transfer, translate risk analysis into operational decisions. Each response has appropriate use cases, cost implications, and governance requirements. Effective risk response selection requires not just technical judgment but organizational context: the same risk rating might lead to different responses in a defense contractor (strong regulatory pressure to mitigate) versus a startup (financial constraints may favor acceptance for non-critical systems). The risk response decision must be documented, approved, and periodically reviewed as part of a mature risk governance process.

In the next lecture, we will shift focus to the adversaries themselves, examining specific threat actor categories, their motivations, capabilities, and the MITRE ATT&CK framework that catalogs their observable behaviors. Understanding who is attacking (threat actors) and why (motivations) provides the qualitative threat intelligence that feeds the likelihood dimension of our risk equation, transforming it from an abstract formula into a grounded assessment of real-world adversarial capability and intent.
:::

%%%

---
unit: CIA
code: CIA
title: Data Classification, The Foundation of Confidentiality
---
:::callout style=soft
Data classification assigns a sensitivity level to information assets, enabling organizations to apply proportional protection. Without classification, it is impossible to determine *which* data needs encryption, *who* needs access, or *what* the impact of a breach would be.
:::

:::table
| Classification Level | Description                                          | Example                              | Controls Required                          |
|----------------------|------------------------------------------------------|--------------------------------------|--------------------------------------------|
| Public               | Approved for unrestricted release                    | Press releases, marketing materials  | Basic integrity controls (no special access) |
| Internal             | For employee use; not for public release             | Internal policies, org charts        | Access control, basic encryption           |
| Confidential         | Sensitive business data; restricted distribution     | Financial forecasts, contracts       | Encryption at rest + in transit, RBAC      |
| Restricted / Secret  | Highly sensitive; unauthorized disclosure causes severe harm | PII, PHI, trade secrets, national security | MFA, DLP, audit logging, need-to-know access |
:::

:::list heading="Classification Principles" style=plain
- Classification is based on **sensitivity** and **impact of unauthorized disclosure**
- Data should be classified at the **highest level** of any component it contains
- NIST SP 800-60 maps federal information types to FIPS 199 impact levels (Low / Moderate / High)
- Classifications must be reviewed periodically, data can be **reclassified downward** as sensitivity decreases
:::

:::code language=mermaid caption="Data classification pyramid: sensitivity and required controls increase toward the apex, classification drives encryption requirements, access control granularity, and breach impact ratings used in risk assessment"
flowchart TB
  R["Restricted / Secret<br/>trade secrets, encryption keys<br/>strongest encryption, need-to-know, full audit"]
  C["Confidential<br/>PII, health and payroll records<br/>encryption, role-based access"]
  I["Internal<br/>policies, org charts<br/>authentication required"]
  P["Public<br/>press releases, marketing<br/>integrity checks only"]
  R --> C --> I --> P
:::

:::notes
Data classification is the foundational process that makes the Confidentiality pillar of the CIA Triad operationally meaningful. Without a systematic classification scheme, organizations cannot consistently determine which data requires encryption, which personnel should have access, what monitoring is necessary, or how to calculate the impact of a confidentiality breach. Classification bridges the abstract goal of "protecting sensitive information" and the concrete implementation of specific controls for specific data types.

Most enterprise classification schemes adopt a four-tier model loosely aligned with government classification systems, though private sector organizations define their own tier names and definitions. The **Public** tier covers information approved for unrestricted release, marketing materials, published financial reports, product documentation. The primary security concern for Public data is integrity (ensuring the published information is accurate and unmodified) rather than confidentiality. The **Internal** tier covers operational information that employees need but that should not be released externally, internal policies, organizational charts, project plans, meeting minutes. Loss of Internal data may cause reputational harm or competitive disadvantage but generally does not trigger regulatory reporting obligations. The **Confidential** tier covers sensitive business data where unauthorized disclosure could harm the organization significantly, financial forecasts, merger and acquisition plans, customer lists, unpublished research. Confidential data requires encryption at rest (AES-256) and in transit (TLS 1.3), strict role-based access controls, and audit logging of access events. The **Restricted** tier (sometimes called Secret, Highly Confidential, or Top Secret depending on the organization or sector) covers data where unauthorized disclosure causes severe harm, personally identifiable information (PII), protected health information (PHI), payment card data (PCI), trade secrets, and national security information. Restricted data demands the full suite of controls: end-to-end encryption, MFA for all access, data loss prevention (DLP) monitoring, privileged access management (PAM), and regular access reviews.

The NIST SP 800-60 guidance formally maps federal information types to FIPS 199 security categories. For example, "Individual Health Information" maps to a High confidentiality impact because unauthorized disclosure "could be expected to have a severe or catastrophic adverse effect" on individuals' privacy and wellbeing. This government mapping methodology provides a disciplined template that private-sector organizations can adapt to their own information asset inventories.

A critical classification principle is that composite data sets should be classified at the highest sensitivity level of any component. A database containing both public product descriptions and confidential customer PII must be classified and protected as Confidential, the presence of PII determines the classification even if most fields are non-sensitive. This principle has significant practical implications: it drives database design decisions (separating sensitive fields into purpose-limited tables), schema decisions (minimizing PII stored in application databases), and access control decisions (restricting access to composite data even when component data might have lower sensitivity in isolation).

Classification must follow regulatory requirements, not intuition. A spreadsheet of 50,000 customers' names, emails and purchase histories is personal data under GDPR Article 6; a five-year strategic plan is commercially confidential; a list of employee salaries is both personal and sensitive. Salary data and purchase histories are often underestimated as "just numbers". ISO/IEC 27001 Annex A control 5.12 requires classification schemes to be reviewed at least annually to account for new regulations, new data types and changes in the competitive environment.
:::

%%%

---
unit: CIA
code: CIA
title: Cryptographic Integrity, Hash Functions and Digital Signatures
---
:::callout style=soft
Integrity mechanisms provide mathematical proof that data has not been altered. Two fundamental tools, **cryptographic hash functions** and **digital signatures**, underpin integrity verification in modern systems from software distribution to financial transactions.
:::

::::columns
::col::
:::list heading="Hash Functions (SHA-256)" style=plain
- Deterministic: same input always produces same output
- One-way: computationally infeasible to reverse
- Avalanche effect: 1-bit change completely alters digest
- Fixed output size: 256 bits regardless of input length
- Collision resistant: infeasible to find two inputs with same hash
:::
::col::
:::list heading="Digital Signatures (RSA / ECDSA)" style=plain
- Combine asymmetric cryptography with hashing
- Sign with private key → verify with public key
- Provide integrity AND non-repudiation
- Used in: code signing, TLS certificates, S/MIME email, SSH
- ECDSA preferred over RSA for smaller key sizes at equivalent strength
:::
::::

:::table
| Algorithm | Output Size | Status           | Use Case                              |
|-----------|-------------|------------------|---------------------------------------|
| MD5       | 128 bits    | Deprecated (broken) | Legacy systems only, do NOT use    |
| SHA-1     | 160 bits    | Deprecated       | Being phased out (collision found 2017) |
| SHA-256   | 256 bits    | Current standard | File integrity, TLS, code signing     |
| SHA-3-256 | 256 bits    | Current (NIST approved) | High-assurance applications      |
:::

:::code language=mermaid caption="Integrity verification mechanisms: SHA-256 hashing detects unauthorized modifications; digital signatures add authentication and non-repudiation by binding the hash to a specific private key holder"
flowchart TB
  subgraph H["Hash verification (integrity)"]
    direction LR
    F1[File] --> S1["Sender computes SHA-256"] --> T1["File + hash sent"]
    T1 --> R1["Receiver recomputes SHA-256"] --> Q1{"Hashes match?"}
  end
  subgraph S["Digital signature (integrity + authenticity)"]
    direction LR
    F2[File] --> S2["Hash signed with<br/>sender's private key"] --> T2["File + signature sent"]
    T2 --> R2["Receiver verifies with<br/>sender's public key"] --> Q2{"Valid signature?"}
  end
  H ~~~ S
:::

:::notes
Cryptographic integrity mechanisms translate the abstract goal of "ensuring data remains unaltered" into mathematical constructs that provide formal, verifiable guarantees. Understanding how these mechanisms work, and where they can be undermined, is essential for applying them correctly in security architectures.

A **cryptographic hash function** takes an arbitrary-length input and produces a fixed-length output called a digest, hash, or checksum. Several properties make hash functions useful for integrity verification. **Determinism** means the same input always produces exactly the same output, verifying that a downloaded file matches the publisher's SHA-256 hash requires computing the hash independently and comparing. **Collision resistance** means it is computationally infeasible to find two different inputs that produce the same hash output, an attacker cannot craft a malicious file that produces an identical hash to the legitimate file. **Pre-image resistance** (one-wayness) means it is computationally infeasible to reconstruct the original input from the hash output, hashes cannot be "reversed." The **avalanche effect** means that a single-bit change in the input causes approximately half of the output bits to change, making it immediately obvious that a modification occurred when comparing hashes, even for very small changes.

SHA-256 (Secure Hash Algorithm 256-bit), standardized in FIPS 180-4, is the current NIST-approved standard for general-purpose integrity verification. It produces a 256-bit (32-byte) digest, typically expressed as a 64-character hexadecimal string. The entire SHA-2 family (SHA-224, SHA-256, SHA-384, SHA-512) remains cryptographically sound as of 2025. SHA-3 (Keccak), standardized in FIPS 202, is an alternative with a fundamentally different internal structure (sponge construction vs. Merkle-Damgård) that provides defense-in-depth if SHA-2 were ever found vulnerable.

MD5 and SHA-1 are **broken** for security purposes and must not be used for integrity verification in new systems. Researchers demonstrated practical MD5 collision attacks in 2004 (Wang and Yu) and SHA-1 collisions in 2017 (Google's SHAttered attack). CVE-2008-0166 illustrates the real-world consequences of cryptographic weakness: the Debian OpenSSL random number generator flaw created predictable SSL keys across Debian-based systems, any system relying on those certificates for integrity had fundamentally compromised assurance, even though the hash function itself was not broken.

**Digital signatures** extend hashing to provide both integrity verification and **non-repudiation**, proof that a specific entity (the private key holder) created and signed the data. The signing process: the signer computes a hash of the message, then encrypts that hash with their private key using RSA or ECDSA. The result (the signature) is transmitted alongside the message. The verification process: any recipient computes the hash of the received message, decrypts the signature using the signer's public key, and compares the two hash values. If they match, the message is verified as unaltered and originating from the private key holder. Code signing uses digital signatures to ensure software packages are authentic and unmodified, Windows Authenticode and macOS Gatekeeper verify code signatures before execution. The SolarWinds compromise (CVE-2020-10148) is a landmark case where attackers compromised the build pipeline to inject malicious code that was then signed with SolarWinds' legitimate code signing certificate, producing a valid signature on malicious software, demonstrating that code signing security is only as strong as the protection of the private signing key.

A hash and a digital signature are different. A hash provides integrity that anyone can check but says nothing about who produced it; a digital signature provides both integrity and authentication. A SHA-256 checksum published on the same server as the download therefore gives little protection: an attacker who compromises the server replaces both the file and the checksum. The checksum must travel through a separate trusted channel, such as a different server, a PKI-signed manifest or an out-of-band message. This is why code signing rooted in PKI is stronger than self-published hashes.
:::

%%%

---
unit: CIA
code: CIA
title: Availability Deep-Dive, RTO, RPO, and Disaster Recovery
---
:::callout style=soft
Availability planning quantifies **how much downtime is acceptable** (RTO) and **how much data loss is acceptable** (RPO). These two metrics drive the selection and cost of disaster recovery technologies, the tighter the targets, the more expensive the solution.
:::

::::columns
::col::
:::callout style=line
**Recovery Time Objective (RTO)**
Maximum acceptable time between a disruption and restoration of service. If your RTO is 4 hours, systems must be restored within 4 hours of an outage.
:::
::col::
:::callout style=line
**Recovery Point Objective (RPO)**
Maximum acceptable data loss measured in time. If your RPO is 1 hour, you must be able to recover data from at most 1 hour before the disruption.
:::
::::

:::table
| DR Strategy         | Typical RTO     | Typical RPO     | Relative Cost | Description                                         |
|---------------------|-----------------|-----------------|---------------|-----------------------------------------------------|
| Tape/Cold Backup    | Hours to days   | 24 hours+       | Low           | Restore from offline backups; full rebuild required |
| Warm Standby        | Minutes to hours | Hours           | Medium        | Pre-configured standby systems, data synced periodically |
| Hot Standby         | Seconds to minutes | Minutes       | High          | Fully operational duplicate; near-real-time sync    |
| Active-Active       | Near-zero       | Near-zero       | Very High     | Multiple live sites; load-balanced; immediate failover |
:::

:::list heading="3-2-1 Backup Rule" style=plain
- **3** copies of data total
- **2** different storage media types (e.g., disk + cloud)
- **1** copy stored offsite or air-gapped
:::

:::image src="images/02_rto_rpo_timeline.png" alt="Timeline diagram showing a disruption event, the RPO window extending backward in time to the last recoverable backup point, and the RTO window extending forward in time to service restoration, with DR strategy options mapped against their typical RTO/RPO positions" caption="RTO and RPO define the availability SLA: RPO determines backup frequency; RTO determines standby infrastructure investment, tighter targets require more expensive redundancy architectures" width=full
:::

:::notes
Availability planning moves the CIA Triad's availability pillar from abstract principle to engineering specification. The two key metrics, Recovery Time Objective (RTO) and Recovery Point Objective (RPO), transform the business requirement of "systems must be available" into quantified engineering targets that drive specific technology investments. Without these metrics, DR planning becomes guesswork; with them, it becomes a solvable engineering and cost optimization problem.

**Recovery Time Objective (RTO)** is the maximum acceptable duration of service disruption, the time from the moment a disruption occurs until service is fully restored. If a hospital's electronic health records system has an RTO of 4 hours, the DR plan must ensure that systems can be fully operational within 4 hours of any declared disaster. RTO drives decisions about infrastructure: an RTO of 72 hours might be achievable by restoring from tape backups; an RTO of 15 minutes requires hot standby infrastructure with automated failover. NIST SP 800-34 (Contingency Planning Guide for Federal Information Systems) requires organizations to determine RTOs for all systems as part of Business Impact Analysis (BIA), the BIA identifies which systems are mission-critical and what the operational, financial, and regulatory consequences of downtime are.

**Recovery Point Objective (RPO)** is the maximum acceptable data loss measured in time, specifically, the age of the most recent backup that will be accepted as a recovery point. An RPO of 1 hour means the organization can tolerate losing at most the last 1 hour of transactions or updates. RPO drives backup frequency: if your RPO is 4 hours, backups must occur at least every 4 hours. RPO also drives replication technology choices: an RPO of near-zero requires synchronous database replication (every transaction committed at primary is also committed at secondary before the transaction is acknowledged), while an RPO of 15 minutes might be achievable with asynchronous replication with 15-minute flush intervals.

The four DR tiers represent an RTO/RPO vs. cost trade-off. **Cold backups** (tape or offline disk) achieve RPOs of 24 hours or more and RTOs measured in hours or days, but cost only the media and offsite storage fees. They are acceptable for non-critical systems where occasional data loss and extended downtime have limited business impact. **Warm standby** maintains pre-configured infrastructure that is restored from periodic backups, servers are provisioned but not running, requiring boot time and data restoration before service can be restored, typically achieving RTOs of 1-4 hours and RPOs of 1-4 hours. **Hot standby** runs a fully operational duplicate environment with near-real-time data synchronization, typically achieving RTOs of minutes and RPOs of minutes, acceptable for critical business applications where downtime causes significant financial or operational harm. **Active-active** configurations run multiple live environments simultaneously, load-balancing traffic across all sites with zero failover time and near-zero data loss, appropriate for the most critical systems where any disruption is unacceptable (financial trading platforms, emergency services dispatch systems, healthcare monitoring systems).

The **3-2-1 backup rule** is the foundational availability best practice: maintain three copies of data (the primary copy plus two backups), store them on two different media types (protecting against media-specific failures, e.g., disk drive failure doesn't affect tape backups), and keep one copy offsite (protecting against site-wide disasters like fires, floods, and ransomware that encrypts all locally accessible storage). Ransomware attacks like the 2021 Kaseya VSA attack (CVE-2021-30116) demonstrated why the offsite/air-gapped requirement is critical: ransomware variants specifically target and encrypt connected backup repositories, leaving organizations without recovery options if backups are network-accessible from compromised systems. The Colonial Pipeline ransomware attack (2021), which caused six days of fuel supply disruption across the U.S. East Coast, underscores the operational and national security consequences of inadequate availability planning for critical infrastructure.

Availability investments can be justified in financial terms. An e-commerce site that takes $100,000 an hour loses $400,000 in a four-hour outage, so a $50,000-a-year hot standby pays for itself after one avoided incident. Cost-benefit language of this kind is how availability controls are argued to non-technical leadership.
:::

%%%

---
unit: CaseStudy
code: CS
title: Case Study, 2017 Equifax Breach (Confidentiality Failure)
---
:::callout style=soft
The 2017 Equifax breach, affecting 147 million individuals, is one of the largest confidentiality failures in history. A single unpatched Apache Struts vulnerability (CVE-2017-5638) gave attackers access to the most sensitive personal financial data of nearly half the U.S. adult population.
:::

:::list heading="Incident Timeline" style=plain
- **March 7, 2017**: Apache Struts CVE-2017-5638 publicly disclosed (CVSS 10.0 Critical)
- **March 9, 2017**: Equifax security team receives patch notification; fails to apply it
- **May 13, 2017**: Attackers exploit unpatched vulnerability; breach begins
- **July 29, 2017**: Equifax detects suspicious traffic; incident investigation begins
- **September 7, 2017**: Equifax publicly discloses the breach, 76 days after detection
- **2020**: Four Chinese PLA members indicted by U.S. DOJ for the attack
:::

:::table
| CIA Property    | Violation                                                          | Impact                                                  |
|-----------------|--------------------------------------------------------------------|---------------------------------------------------------|
| Confidentiality | 147M SSNs, DOBs, addresses, driver's license and credit card data exfiltrated | Massive PII exposure; identity theft risk for nearly half U.S. adult population |
| Integrity       | No data modification detected                                      | N/A                                                     |
| Availability    | Limited service disruption                                         | Minimal operational impact; primary harm was data disclosure |
:::

:::list heading="Root Causes" style=plain
- Failure to apply critical patch within 76 days of public disclosure
- Inadequate network segmentation allowed lateral movement post-exploitation
- Missing TLS inspection inside internal network masked exfiltration traffic
- No data minimization, massive historical PII retained without business justification
:::

:::code language=mermaid caption="Equifax breach timeline: a 76-day window between patch availability and exploitation, followed by a 76-day dwell time before detection, illustrates the compounding cost of delayed patching and inadequate monitoring"
flowchart TB
  A["March 7, 2017<br/>Apache Struts CVE-2017-5638 disclosed and patched"] --> B["March 15<br/>Internal scan misses the vulnerable dispute portal"]
  B --> C["May 13<br/>Attackers exploit the unpatched portal"]
  C --> D["May to July<br/>About 76 days of undetected data theft"]
  D --> E["July 29<br/>Traffic finally inspected after an expired certificate is renewed"]
  E --> F["September 7<br/>Public disclosure, about 147 million people affected"]
:::

:::notes
The 2017 Equifax breach is the defining confidentiality failure case study for information security curricula because it combines nearly every category of control failure into a single incident: a known, patchable vulnerability exploited because of process failure, combined with inadequate network controls that permitted extensive lateral movement and exfiltration, compounded by data retention practices that accumulated far more sensitive data than necessary for business operations.

The root cause was CVE-2017-5638, a remote code execution vulnerability in Apache Struts 2 (a widely used Java web framework) that exploited improper input validation in the Content-Type HTTP header. The vulnerability received a CVSS Base Score of 10.0, the maximum possible score, indicating that it was remotely exploitable, required no authentication, had no complexity constraints, and could result in complete system compromise. The Apache Software Foundation released a patch within hours of disclosure on March 7, 2017. The U.S. Computer Emergency Readiness Team (US-CERT) issued a public advisory the same day urging immediate patching. Despite this, Equifax's security team failed to apply the patch due to a combination of inadequate asset inventory (they did not know all systems running Struts), an expired SSL certificate on their internal scanning tool that prevented inspection of the vulnerable traffic, and an organizational process that did not enforce emergency patching for critical CVEs.

Attackers exploited the unpatched vulnerability on May 13, 2017, 67 days after the patch was publicly available. Once inside, they conducted a textbook attack progression: initial access via the Struts exploit, reconnaissance of internal systems and data repositories, credential harvesting to enable lateral movement to additional servers, and systematic exfiltration of PII through encrypted HTTPS connections that Equifax's monitoring tools could not inspect because the necessary SSL inspection certificates had also expired. Over 76 days of dwell time, attackers accessed approximately 50 databases and exfiltrated data in 9,000 queries, an activity profile that should have been detectable with basic anomaly detection on database query volumes.

The breach exposed the full spectrum of PII: Social Security Numbers, dates of birth, home addresses, driver's license numbers, and approximately 209,000 credit card numbers. For 147 million Americans, this constitutes essentially all the information needed for identity theft, tax fraud, fraudulent credit applications, and synthetic identity creation. The breach also exposed 15.2 million U.K. citizens and approximately 19,000 Canadian citizens, triggering regulatory investigations in multiple jurisdictions.

The regulatory and financial consequences were substantial. Equifax reached a settlement with the FTC, CFPB, and 50 U.S. states for approximately $700 million in 2019, at the time, the largest data breach settlement in history. The settlement required Equifax to implement a comprehensive information security program, including annual independent security assessments, executive-level security leadership, and specific technical controls including patch management, network monitoring, and data minimization. The UK Information Commissioner's Office (ICO) fined Equifax £500,000, the maximum under the then-applicable Data Protection Act 1998 (note that under GDPR, which took effect in 2018, the fine could have been up to 4% of global annual turnover, potentially $675 million based on Equifax's 2016 revenue).

Key lessons for risk management: (1) CVSS 10.0 vulnerabilities require emergency patching measured in hours or days, not weeks; (2) asset inventory is a prerequisite for effective vulnerability management, you cannot patch systems you don't know exist; (3) network segmentation limits lateral movement; (4) data minimization reduces breach impact, Equifax retained historical data far beyond its business utility; (5) internal network traffic inspection is as important as perimeter monitoring. The Equifax breach is a direct lesson in how a single moderate-effort likelihood event (known critical CVE, unpatched for 67 days) combined with high impact (147M individuals' complete financial identity) produces a catastrophic risk realization that could have been prevented by basic patch management discipline.

Responsibility for the Equifax breach was shared: by the security team that did not patch, by the executives who did not fund adequate staffing, and by the board that did not require regular security reporting. This is why the NIST RMF requires authorization at the senior executive level: security is a governance issue as well as a technical one.
:::

%%%

---
unit: CaseStudy
code: CS
title: Case Study, 2020 SolarWinds Supply Chain Attack (Integrity Failure)
---
:::callout style=soft
The SolarWinds SUNBURST attack, attributed to Russia's SVR (Cozy Bear / APT29), compromised the software build pipeline of SolarWinds Orion, injecting malicious code into signed software updates distributed to approximately 18,000 organizations worldwide, including U.S. federal agencies.
:::

:::list heading="Attack Chain" style=plain
- **October 2019**: Attackers gain access to SolarWinds build environment
- **October 2019 – February 2020**: Attackers test and refine SUNBURST malware injection
- **March 2020**: Malicious Orion update (2019.4.5200.9083) distributed to customers
- **December 8, 2020**: FireEye announces its own breach caused by the attack
- **December 13, 2020**: CISA issues Emergency Directive 21-01, disconnect SolarWinds immediately
- **December 2020**: Affected agencies include Treasury, Commerce, Homeland Security, and others
:::

:::table
| CIA Property    | Violation                                                          |
|-----------------|-------------------------------------------------------------------|
| Integrity       | Legitimate software update modified to contain backdoor (SUNBURST); digitally signed with SolarWinds' valid certificate |
| Confidentiality | Attackers accessed email, classified network files, and sensitive communications at U.S. agencies |
| Availability    | No immediate disruption, attack prioritized stealth over disruption |
:::

:::list heading="Why This Was a Supply Chain Attack" style=plain
- Attackers targeted the **software build process**, not production systems directly
- The malicious code was **signed with a legitimate code signing certificate**
- Recipients had no way to distinguish the trojanized update from a legitimate one
- Affected all downstream customers of a trusted, widely-deployed network monitoring tool
:::

:::code language=mermaid caption="SolarWinds SUNBURST attack chain: by compromising the software supply chain at the build stage, attackers distributed legitimately-signed malware to 18,000 organizations, defeating code signing integrity controls by compromising the signing key itself"
flowchart LR
  A["Build pipeline<br/>compromised at the source"] --> B["Malicious code injected<br/>into Orion update"]
  B --> C["Package signed with<br/>legitimate certificate"]
  C --> D["Shipped through the official<br/>update mechanism"]
  D --> E["Customers install it<br/>because they trust it"]
:::

:::notes
The SolarWinds SUNBURST attack, publicly disclosed in December 2020 and attributed by the U.S. intelligence community to Russia's Foreign Intelligence Service (SVR), represented a fundamental integrity attack at unprecedented scale and sophistication. Rather than attacking individual target organizations directly, the threat actors compromised the software development and build infrastructure of SolarWinds, a company whose Orion network management platform was installed in approximately 33,000 organizations worldwide, including the majority of Fortune 500 companies and numerous U.S. federal agencies.

The attack technique was a **software supply chain compromise**, a category of attack that defeats perimeter and endpoint defenses by delivering malicious code through a trusted software update mechanism that organizations are expected to trust and install. The attackers accessed SolarWinds' development environment in October 2019, more than a year before the breach was discovered, and spent months testing a SUNBURST malware injection technique that modified the Orion source code in a way that avoided detection by SolarWinds' internal testing and code review processes. The injected code was designed to be dormant for approximately two weeks after installation, evading detection by sandbox analysis tools that typically observe malware behavior for shorter periods, and to mimic legitimate SolarWinds network traffic patterns to avoid triggering anomaly detection.

The integrity violation was fundamental: the compiled software binary that was distributed as a legitimate Orion update (version 2019.4.5200.9083, released March 2020) contained malicious code, the SUNBURST backdoor, that had been injected into the build process. The resulting update package was signed with SolarWinds' legitimate Authenticode code signing certificate, meaning all standard code integrity verification mechanisms (Windows signature verification, enterprise software deployment tools' signature checking) would indicate the package was authentic and unmodified. This illustrates a critical boundary of code signing: it proves the software was signed by the private key holder, but does not prove that the private key holder's build environment produced only legitimate code. If the build pipeline is compromised before signing, the signature is valid but the code is malicious.

Approximately 18,000 organizations installed the trojanized update. Of these, the attackers selected fewer than 100 high-value targets for active follow-on operations, installing the TEARDROP second-stage payload to enable persistent access, lateral movement, and data exfiltration. Confirmed victims included the U.S. Department of the Treasury, Department of Commerce (including NTIA), Department of Homeland Security (including CISA itself), Department of State, Department of Defense, and cybersecurity firm FireEye (whose discovery of the attack initiated public disclosure). The attackers accessed email systems, sensitive files, and in some cases classified network segments, with the full scope of data exfiltration remaining classified.

CISA issued Emergency Directive 21-01 on December 13, 2020, requiring all federal agencies to immediately disconnect or power down SolarWinds Orion products, an extraordinary step demonstrating the severity of the compromise. The directive noted that the malicious code "poses an unacceptable risk to the security of federal networks." CISA and the FBI subsequently issued multiple advisories detailing SUNBURST indicators of compromise (IoCs), TEARDROP behavior, and recommended detection and remediation steps.

Supply chain attacks are particularly challenging from a risk management perspective because they weaponize trust, the same trust relationships that make software distribution efficient (automatic updates, signed packages) become attack vectors when the upstream supplier is compromised. NIST SP 800-161 (Supply Chain Risk Management Practices for Federal Information and Communications Technology) and the 2021 Executive Order on Improving the Nation's Cybersecurity (EO 14028) respond to this reality by requiring software bills of materials (SBOMs), enhanced software supply chain security requirements for federal suppliers, and multi-party validation of software build integrity. These responses acknowledge that perimeter and endpoint defenses are insufficient against sophisticated supply chain attacks, defense requires extending trust verification into the software production process itself.

SolarWinds shows the limits of traditional controls. A vulnerability assessment of a system running SUNBURST would almost certainly have found nothing, because the malware arrived as a legitimately signed update with no known signature. Behavioral detection, network traffic analysis and zero-trust architecture are needed alongside signature-based detection. The attack also illustrates the trust chain: an organization's security is bounded by the security of every supplier in its software supply chain.
:::

%%%

---
unit: CaseStudy
code: CS
title: Case Study, 2021 Colonial Pipeline Ransomware (Availability Failure)
---
:::callout style=soft
In May 2021, the DarkSide ransomware group attacked Colonial Pipeline, operator of the largest refined fuel pipeline in the United States, forcing a six-day operational shutdown that triggered fuel shortages across the U.S. East Coast and a national emergency declaration. The initial access vector: a single compromised VPN password with no MFA.
:::

:::list heading="Incident Timeline" style=plain
- **April 29, 2021**: Attackers gain initial access using a compromised VPN account password (no MFA)
- **May 7, 2021**: DarkSide deploys ransomware; Colonial shuts down pipeline operations
- **May 8, 2021**: Colonial pays $4.4M ransom in Bitcoin (75 BTC) to DarkSide
- **May 8, 2021**: President Biden declares a State of Emergency; fuel supply restrictions activated
- **May 12, 2021**: Colonial restores full pipeline operations
- **June 2021**: DOJ recovers approximately $2.3M of the ransom payment
:::

:::table
| CIA Property    | Impact                                                                                  | Severity |
|-----------------|-----------------------------------------------------------------------------------------|----------|
| Availability    | 5,500-mile pipeline carrying 45% of East Coast fuel supply shut down for 6 days         | Critical |
| Confidentiality | DarkSide exfiltrated approximately 100GB of data before deploying ransomware (double extortion) | High |
| Integrity       | Ransomware encrypted IT systems; OT systems isolated as precaution                     | Moderate |
:::

:::list heading="Root Causes and Lessons" style=plain
- Single compromised legacy VPN account with **no MFA** was the initial access vector
- The compromised password was found in a **dark web credential dump** from a prior breach
- Colonial lacked **network segmentation** between IT and OT environments
- **No tested incident response plan**, leadership made ad hoc decisions under crisis conditions
- **Ransom payment** illustrates that availability failures have direct financial consequences regardless of recovery
:::

:::code language=mermaid caption="Colonial Pipeline attack: a single compromised VPN password without MFA led to a 6-day shutdown of 45% of East Coast fuel supply, illustrating how availability failures in critical infrastructure translate directly into national security consequences"
flowchart TB
  A["April 29, 2021<br/>Login to a legacy VPN account: leaked password, no MFA"] --> B["May 6<br/>About 100 GB of data stolen"]
  B --> C["May 7<br/>DarkSide ransomware hits IT systems, pipeline shut down, ransom paid"]
  C --> D["May 12<br/>Pipeline restarts after fuel shortages across the Southeast"]
  D --> E["June 7<br/>DOJ recovers 63.7 bitcoin of the ransom"]
:::

:::notes
The Colonial Pipeline ransomware attack is the most consequential availability incident in U.S. critical infrastructure history, demonstrating with stark clarity how a single credential security failure can cascade into national-level supply disruption, economic harm, and geopolitical consequences. The attack was executed by DarkSide, a Russian-speaking ransomware-as-a-service (RaaS) group that provides ransomware tooling and infrastructure to affiliate attackers in exchange for a percentage of ransom payments.

The initial access was startlingly simple given the consequences it produced. Investigators found that attackers obtained a valid username and password for Colonial Pipeline's legacy VPN service from a dark web credential dump, a collection of usernames and passwords stolen from other previously breached services where Colonial employees had reused the same password. The VPN account had no multi-factor authentication enabled, meaning possession of the username and password was sufficient to gain network access. This is precisely the scenario that NIST SP 800-63B AAL2 authentication requirements are designed to prevent: requiring MFA for access to sensitive systems ensures that credential theft alone is insufficient for unauthorized access.

Once inside Colonial's network, DarkSide operators conducted reconnaissance, moved laterally through IT systems, and exfiltrated approximately 100GB of data before deploying the ransomware payload, a technique known as "double extortion" where victims face both the ransom demand for decryption keys and a threat to publicly release exfiltrated data if they do not pay. The ransomware encrypted Colonial's billing and business IT systems. Colonial proactively shut down pipeline operations as a precautionary measure, not because the OT (operational technology) systems were directly compromised, but because operators lacked confidence in the integrity of systems that interface with pipeline operations and feared the attack might spread to operational control systems. This decision, while understandable, highlights a critical gap: the absence of tested IT-OT network segmentation and separation meant that an IT compromise created doubt about OT safety, necessitating operational shutdown as a risk management measure.

The six-day shutdown of the 5,500-mile pipeline that carries approximately 45% of diesel, gasoline, and jet fuel to the U.S. East Coast triggered widespread fuel shortages. The Biden administration declared a State of Emergency (18 U.S.C. § 521) to waive hours-of-service restrictions for fuel transport drivers, and the Department of Transportation relaxed fuel transport regulations to accelerate alternative supply routes. Panic buying exacerbated shortages, with lines stretching hours at gas stations across the Southeast and Mid-Atlantic. Multiple airports faced potential disruptions to aviation fuel supplies.

Colonial paid a $4.4 million (75 BTC) ransom within hours of the attack, a decision that received significant criticism from cybersecurity professionals who argue that ransom payments fund future attacks and incentivize ransomware campaigns targeting critical infrastructure. Colonial CEO Joseph Blount testified to Congress that the payment decision was made without adequate consultation because no tested incident response plan existed with clear decision authority for such scenarios. Remarkably, the FBI and DOJ subsequently seized approximately $2.3 million (63.7 BTC) of the ransom payment by obtaining the private key associated with the DarkSide wallet, demonstrating that cryptocurrency ransom payments are not as untraceable as attackers assume, particularly when law enforcement has the operational capability to trace blockchain transactions and seize keys.

From a risk analysis perspective, the Colonial Pipeline attack illustrates several critical principles. The likelihood of VPN credential compromise and ransomware deployment was High, ransomware attacks on critical infrastructure were well-documented and increasing, and the absence of MFA on an internet-accessible VPN was a known, exploitable gap. The impact of a pipeline shutdown was unambiguously High, CISA's Critical Infrastructure Protection framework classifies Energy as one of 16 critical infrastructure sectors where disruption could "have a debilitating effect on national security, national economic security, national public health or safety, or any combination thereof." A proper risk matrix analysis would have placed this risk in the High × High cell, warranting immediate investment in MFA deployment, network segmentation, and incident response planning. Post-incident, the Biden administration's 2021 Executive Order on Cybersecurity (EO 14028) cited Colonial Pipeline as a motivating case for new requirements including mandatory incident reporting for critical infrastructure operators and enhanced cybersecurity standards for pipeline operators.
:::

%%%

---
unit: CIA
code: CIA
title: When CIA Properties Conflict, Trade-offs and Tensions
---
:::callout style=soft
The CIA Triad properties do not always point in the same direction. Real-world security architecture requires **deliberate trade-offs**, strengthening one property can weaken another, and optimizing all three simultaneously often requires accepting constraints on each.
:::

:::table
| Tension                          | Confidentiality Impact          | Availability Impact              | Integrity Impact              |
|----------------------------------|---------------------------------|-----------------------------------|-------------------------------|
| Aggressive encryption            | Strengthens                     | Can impair (key management overhead) | Neutral                    |
| Heavy audit logging              | May expose sensitive data in logs | Slight overhead on system performance | Strengthens (forensic trail) |
| Redundant data copies (backups)  | More copies = more exposure surface | Strengthens                    | Each copy must be verified    |
| Zero-trust network architecture  | Strengthens                     | Can add latency if poorly tuned   | Neutral                       |
| Rapid patching                   | Neutral                         | Brief outage during patch cycles  | Strengthens (reduces CVE risk)|
:::

::::columns
::col::
:::list heading="Classic Conflicts" style=plain
- **Encryption vs. Availability**: full-disk encryption requires decryption for every read, adds I/O overhead
- **Logging vs. Confidentiality**: detailed logs capturing user activity may expose PII or sensitive operations
- **Redundancy vs. Confidentiality**: every backup copy is an additional target for unauthorized access
:::
::col::
:::callout style=line
**Design Principle**: The goal is not to maximize each CIA property in isolation, but to find the **optimal balance** given the organization's risk profile, regulatory requirements, and operational constraints.
:::
::::

:::image src="images/02_cia_tradeoffs_venn.png" alt="Venn diagram with three overlapping circles labeled Confidentiality, Integrity, and Availability, with tension zones in the overlaps annotated with real-world examples: encryption overhead in the C-A overlap, log exposure risk in the C-I overlap, and backup verification burden in the I-A overlap; the center shows the design goal of balanced optimization" caption="CIA Triad trade-off diagram: the overlapping regions between CIA properties represent real engineering tensions that security architects must resolve through deliberate design choices rather than attempting to maximize each property independently" width=full
:::

:::notes
One of the most important, and often overlooked, aspects of the CIA Triad is that its three properties are not independent. Security architects who attempt to maximize each property in isolation often discover that controls that strengthen one property create weaknesses or operational burdens in another. Recognizing these tensions is essential for designing security architectures that are both effective and operationally sustainable.

The **confidentiality-availability tension** is perhaps the most practically significant. Encryption is the primary confidentiality control for data at rest and in transit, but encryption imposes computational overhead. For most modern systems, AES-256-GCM hardware acceleration (available in Intel AES-NI and ARM Cryptography Extensions) makes encryption overhead negligible. However, key management, the processes for generating, distributing, storing, rotating, and revoking encryption keys, creates significant availability risk. If encryption keys are lost, the data they protect becomes permanently inaccessible regardless of the data's integrity. The 2019 QuadrigaCX cryptocurrency exchange collapse, where approximately $190 million CAD in customer funds became permanently inaccessible after the sole holder of the cold wallet private keys died, illustrates an extreme but real availability failure caused by inadequate key management. NIST SP 800-57 (Recommendation for Key Management) provides comprehensive guidance for managing encryption keys in a way that maintains both confidentiality (keys inaccessible to unauthorized parties) and availability (keys recoverable by authorized parties through documented procedures).

The **confidentiality-integrity tension** manifests most commonly in audit logging. Comprehensive audit trails are essential for integrity assurance, they record who accessed what data, what changes were made, and when, enabling detection of unauthorized modifications and forensic reconstruction of security incidents. However, detailed audit logs may themselves contain sensitive information: logs of database queries may capture the content of those queries (including sensitive data); logs of network connections may reveal patterns of communication that are themselves sensitive; logs of user authentication events may capture usernames in a way that enables enumeration attacks. Organizations must therefore apply confidentiality controls to audit logs themselves, restricting access, encrypting log storage, and implementing log integrity protection (tamper-evident logging using cryptographic chaining), or risk creating a confidentiality vulnerability in the very system designed to protect integrity.

The **integrity-availability tension** is most visible in backup and recovery architectures. Maintaining multiple copies of data (the 3-2-1 rule) strengthens availability by ensuring that data can be recovered even if primary copies are lost or corrupted. However, each backup copy is an additional surface for unauthorized access, if backup media is unencrypted, improperly secured, or stored in cloud repositories with insufficient access controls, the backup copies may be easier targets for confidentiality attacks than the primary systems. Additionally, backup integrity must be actively verified: storing backup copies without verifying that they are complete, uncorrupted, and actually restorable means that backup availability is assumed rather than tested. The Ransomware task force has documented numerous cases where organizations discovered during a ransomware recovery attempt that their backup systems had silently failed months earlier, leaving no viable recovery option despite the apparent existence of backups.

The **confidentiality-zero-trust tension** is increasingly relevant as organizations adopt zero-trust network architectures. Zero-trust requires continuous verification of every access request, every user, device, and network connection must be authenticated and authorized regardless of network location. This continuous verification process requires monitoring network traffic, user behavior, device state, and access patterns to make authorization decisions, creating a surveillance infrastructure that, if not carefully controlled, itself becomes a confidentiality risk (particularly in jurisdictions with employee privacy regulations like the EU). Organizations implementing zero-trust must establish clear data governance policies defining what monitoring data is collected, how long it is retained, who can access it, and what it may be used for.

The practical design principle is that the goal of security architecture is not to maximize each CIA property in isolation but to find the optimal balance given the specific risk environment, regulatory constraints, and operational requirements of the organization. This balance is achieved through risk-based trade-off analysis: identify the specific CIA tensions present in the architecture, assess the risk implications of each resolution option, and select the option that achieves acceptable CIA properties across all three dimensions simultaneously. Documenting these trade-off decisions as part of security architecture artifacts ensures that future changes to the system consider their CIA implications and maintain the intended balance.

Controls can pull CIA properties against each other. In a healthcare organization that adopts full-disk encryption on every server, logs every database query and keeps redundant backups on local and cloud storage, each choice creates a new obligation: key management for the disk encryption, access control and encryption for the query logs, and encryption and access control for both backup copies. The controls achieve the intended balance only if these secondary protections are in place.
:::

%%%

---
unit: CIA
code: CIA
title: Common Misconceptions About the CIA Triad
---
:::callout style=soft
Despite its apparent simplicity, the CIA Triad is frequently misunderstood in practice. Clearing up these misconceptions is essential for applying the framework correctly in risk assessments, control selection, and incident classification.
:::

::::columns
::col::
:::list heading="Misconception 1: CIA = Just Encryption" style=plain
**Wrong**: Encryption addresses confidentiality in transit and at rest, but does nothing for availability (a DDoS attack bypasses encryption entirely) or integrity (an attacker with a valid encryption key can modify and re-encrypt data).

**Correct**: Each CIA property requires its own control family. Encryption is one of many confidentiality controls.
:::
::col::
:::list heading="Misconception 2: Availability = Just Uptime" style=plain
**Wrong**: Availability is often reduced to "99.9% uptime SLA." But availability also includes ensuring data is accessible in a usable, accurate form, a system that is "up" but returning corrupted data violates availability.

**Correct**: Availability means timely and reliable access to accurate information and resources.
:::
::::

::::columns
::col::
:::list heading="Misconception 3: CIA Is Equally Weighted" style=plain
**Wrong**: Many assume all three properties are equally important for all systems. In reality, priority varies by context, a public website prioritizes availability; a classified system prioritizes confidentiality.

**Correct**: CIA property prioritization depends on the system's mission, data sensitivity, and regulatory environment (FIPS 199).
:::
::col::
:::list heading="Misconception 4: Integrity = Backups" style=plain
**Wrong**: Backups protect availability, not integrity. A backup of corrupted data is a backup of corrupted data. If data has been silently modified, the backup preserves the modification.

**Correct**: Integrity requires cryptographic verification (hashing, signing) to detect modifications, not just preserving copies.
:::
::::

:::notes
The CIA Triad is taught in virtually every introductory security curriculum, but its apparent simplicity breeds a set of persistent misconceptions that cause real errors in security architecture, risk assessment, and incident classification. Addressing these misconceptions explicitly helps students apply the framework correctly rather than mechanically.

**Misconception 1: CIA is primarily about encryption.** This is the most common misconception among students encountering the triad for the first time. Encryption is a powerful and essential security control, but it addresses only one subset of confidentiality requirements (protecting data from unauthorized disclosure) and does not address integrity or availability at all. A system can be fully encrypted and simultaneously suffer an integrity violation (an authorized user with decryption capability modifies data inappropriately) or an availability violation (the encryption keys are lost, rendering the encrypted data permanently inaccessible). Confidentiality has non-encryption dimensions: access control (ensuring only authorized entities can access data in the first place), data minimization (limiting the amount of sensitive data stored), and classification (knowing which data requires what level of protection) are all confidentiality controls that operate independently of encryption.

**Misconception 2: Availability equals uptime percentage.** SLA-focused thinking reduces availability to a single number (99.9%, 99.99%) that measures whether a system responds to requests. This is necessary but insufficient. True availability requires that systems return accurate, complete, and timely data when accessed, a system that is "up" but returning corrupted data due to a database error violates availability even if its HTTP response code is 200 OK. A system that is "up" but extremely slow due to a partial DDoS may have 100% uptime while failing to meet its availability obligation. NIST SP 800-53 control AU-9 (Protection of Audit Information) requires that audit log availability be maintained even under adversarial conditions, recognizing that availability of specific data types is more nuanced than binary system up/down status.

**Misconception 3: All three CIA properties are equally important.** This misconception leads to control selection errors, applying controls appropriate for high-confidentiality requirements to systems where availability is the dominant concern, and vice versa. FIPS 199 explicitly acknowledges that CIA impact levels vary by system type. A public-facing informational website has Low confidentiality impact (no sensitive data), Low integrity impact (content errors are quickly discoverable), and High availability impact (downtime prevents public access to government information). A classified government information system has High confidentiality impact (disclosure causes serious national security harm), High integrity impact (corruption of intelligence data could cause mission failure), and potentially Moderate availability impact (alternative access methods may exist). Security professionals must conduct impact analysis across all three CIA dimensions independently and calibrate controls to the specific impact level of each property for the specific system under assessment.

**Misconception 4: Backups protect integrity.** This misconception is particularly dangerous because it creates false assurance. Backups protect availability by ensuring that a copy of data exists for recovery after loss, corruption, or ransomware encryption. But if data has been silently modified, through an integrity attack where an attacker altered records gradually over months, the backup faithfully preserves the corrupted data. Detecting integrity violations requires proactive integrity monitoring: baseline hashing of critical files (NIST SP 800-53 SI-7), database activity monitoring that detects unauthorized modifications, and signed audit logs that detect log tampering. The NIST National Checklist Program (NCP) specifies file integrity monitoring requirements for hardened system configurations, recognizing that integrity cannot be assumed, it must be actively verified.

A fifth important misconception worth raising with advanced students: **the CIA Triad is complete.** While CIA covers the foundational security properties, many frameworks extend it. The Parkerian Hexad adds Possession (controlling who holds the data), Authenticity (verifying origin), and Utility (data is in a usable form). Non-repudiation, ensuring a party cannot deny performing an action, is often cited as a fourth fundamental property. The DAD Triad (Disclosure, Alteration, Denial) maps CIA violations from the attacker's perspective. Understanding these extensions helps security professionals recognize scenarios where the classic CIA triad provides incomplete analysis.

Many incidents violate more than one CIA property. Ransomware is an availability attack and also an integrity attack, because it alters files by encrypting them. SQL injection that modifies data is an integrity attack and, if data was also read, a confidentiality attack. Classifying an incident by a single property usually understates its impact.
:::

%%%

---
unit: Framework
code: FWK
title: CVSS, Standardized Vulnerability Scoring
---
:::callout style=soft
The **Common Vulnerability Scoring System (CVSS)** is the industry-standard framework for communicating the severity of software vulnerabilities. A CVSS score provides a numerical summary (0.0–10.0) that security teams use to prioritize patching, assess risk, and communicate with stakeholders.
:::

:::table
| CVSS Metric Group | What It Measures                                          | Example Metrics                                      |
|-------------------|-----------------------------------------------------------|------------------------------------------------------|
| Base Score        | Intrinsic characteristics of the vulnerability            | Attack Vector, Complexity, Privileges Required, Scope, Impact (CIA) |
| Temporal Score    | Time-dependent factors that change over the vulnerability lifecycle | Exploit Code Maturity, Remediation Level, Report Confidence |
| Environmental Score | Organization-specific context that adjusts the score   | Modified Impact Metrics, Security Requirements (CIA importance) |
:::

:::table
| CVSS Score Range | Severity Rating | Example                                      |
|------------------|-----------------|----------------------------------------------|
| 0.0              | None            | No vulnerability                             |
| 0.1 – 3.9        | Low             | Requires local access + user interaction     |
| 4.0 – 6.9        | Medium          | Network exploitable, authentication required |
| 7.0 – 8.9        | High            | Network exploitable, low privileges          |
| 9.0 – 10.0       | Critical        | Remote exploit, no auth, high CIA impact     |
:::

:::list heading="CVSS Limitations to Know" style=plain
- Base Score does not account for exploit availability in the wild
- A CVSS 10.0 vulnerability on an unexposed system is lower risk than a CVSS 5.0 on a public-facing critical server
- CISA's Known Exploited Vulnerabilities (KEV) catalog is a more operationally relevant priority signal than CVSS alone
- CVSS measures severity, not risk, risk requires combining CVSS with asset criticality and threat context
:::

:::code language=mermaid caption="CVSS score decomposition: a Base Score of 10.0 requires network exploitability, no authentication, no user interaction, and High impact across all CIA properties, Temporal and Environmental scores adjust the base for real-world context"
flowchart LR
  subgraph E["Exploitability"]
    AV["Attack Vector: Network"]
    AC["Attack Complexity: Low"]
    PR["Privileges Required: None"]
    UI["User Interaction: None"]
  end
  subgraph S["Scope"]
    SC["Scope: Changed"]
  end
  subgraph I["Impact"]
    C["Confidentiality: High"]
    IN["Integrity: High"]
    A["Availability: High"]
  end
  E --> B["Base score 10.0<br/>Critical"]
  S --> B
  I --> B
:::

:::notes
The Common Vulnerability Scoring System (CVSS) is the de facto standard for communicating vulnerability severity across the cybersecurity industry. Maintained by FIRST (Forum of Incident Response and Security Teams), CVSS v3.1 (released 2019) is the current widely deployed version, with CVSSv4.0 published in 2023 and beginning adoption. Understanding CVSS is essential for vulnerability management, risk communication, and connecting technical vulnerability data to the risk equation (Risk = Likelihood × Impact).

The **CVSS Base Score** captures the intrinsic, time-invariant characteristics of a vulnerability. It comprises two groups of metrics. The **Exploitability metrics** describe how the vulnerability is attacked: Attack Vector (Network, Adjacent, Local, Physical, Network being easiest to exploit), Attack Complexity (Low or High, Low means exploitation is straightforward and reliable), Privileges Required (None, Low, High, None means no account required), and User Interaction (None or Required, None means no victim interaction needed). The **Impact metrics** describe the consequence of successful exploitation: Confidentiality Impact, Integrity Impact, and Availability Impact, each rated None, Low, or High. A Scope metric (Unchanged or Changed) captures whether exploitation of the vulnerable component can impact resources beyond its security scope. CVE-2017-0144 (EternalBlue) receives a Base Score of 9.3 because it is network-exploitable (AV:N), has low complexity (AC:L), requires no privileges (PR:N), requires no user interaction (UI:N), and has High impact on all CIA properties.

The **Temporal Score** adjusts the Base Score for time-dependent factors. Exploit Code Maturity ranges from Unproven (theoretical exploit only) to Functional (usable exploit code exists) to High (reliable exploitation in multiple contexts), a vulnerability with publicly available, weaponized exploit code is substantially more dangerous in practice than a theoretically exploitable vulnerability with no public proof-of-concept. Remediation Level captures whether a vendor patch is available (reducing urgency for patching if a workaround exists). Report Confidence reflects certainty about the vulnerability details (a confirmed, vendor-acknowledged vulnerability warrants higher priority than a single unconfirmed report). The Temporal Score modifies the Base Score downward when mitigating factors exist or upward when exploit availability increases practical risk.

The **Environmental Score** is the most operationally relevant but least consistently applied component. It allows organizations to modify the vulnerability score based on their specific context: Modified Impact metrics adjust CIA weights to reflect how important each property is for the specific system (a system where availability is critical because it controls physical processes should have the Availability metric weighted higher than default). Security Requirements allow organizations to indicate that CIA confidentiality, integrity, or availability have elevated (or reduced) importance for this specific system. The Environmental Score transforms the universal Base Score into an organization-specific risk indicator, a CVSS 7.0 vulnerability on a non-internet-exposed, low-criticality internal system may receive an Environmental Score of 4.0 after adjustment, while the same vulnerability on a public-facing, high-criticality system handling PII may receive an Environmental Score of 9.0.

A critical operational point: CVSS measures intrinsic **severity**, not **risk**. A vulnerability's risk to a specific organization depends on CVSS score, asset criticality (how important is the affected system?), exposure (is the vulnerable service internet-accessible?), and threat context (are there active exploitation campaigns targeting this vulnerability?). CISA's Known Exploited Vulnerabilities (KEV) catalog, which lists CVEs with confirmed exploitation in the wild, is an essential complement to CVSS scoring. CISA's Binding Operational Directive 22-01 requires federal agencies to remediate KEV catalog vulnerabilities on a mandated timeline regardless of CVSS score, acknowledging that exploitation evidence is more operationally urgent than theoretical severity ratings. The EPSS (Exploit Prediction Scoring System) is a newer model that uses machine learning to predict the probability of exploitation within the next 30 days, providing a more operationally focused risk signal than CVSS alone.

The CVSS v3.1 Base Score for Log4Shell (CVE-2021-44228) is 10.0, Critical: AV:N, AC:L, PR:N, UI:N, S:C (the exploit reaches the JVM host), C:H, I:H, A:H. Context changes risk: if the same vulnerability affected only an internal system with no exposure to untrusted networks, adjusting the attack vector to Adjacent or Local in the Environmental metrics would lower the score substantially.
:::

%%%

---
unit: Framework
code: FWK
title: NIST SP 800-53, The Security Controls Catalog
---
:::callout style=soft
NIST Special Publication 800-53 is the most comprehensive catalog of security and privacy controls for information systems. It provides the "menu" from which organizations select controls during the RMF Select step, mapping controls to CIA properties, control families, and baseline impact levels.
:::

:::table
| Control Family | Identifier | Example Controls                                              | Primary CIA Focus |
|----------------|------------|---------------------------------------------------------------|-------------------|
| Access Control | AC         | AC-2 (Account Management), AC-3 (Access Enforcement), AC-17 (Remote Access) | Confidentiality |
| Audit and Accountability | AU | AU-2 (Event Logging), AU-9 (Log Protection), AU-12 (Audit Record Generation) | Integrity |
| Incident Response | IR    | IR-4 (Incident Handling), IR-6 (Incident Reporting), IR-8 (Incident Response Plan) | Availability |
| System Integrity | SI      | SI-3 (Malicious Code Protection), SI-7 (Software and Integrity), SI-10 (Input Validation) | Integrity |
| Contingency Planning | CP | CP-2 (Contingency Plan), CP-9 (System Backup), CP-10 (System Recovery) | Availability |
| Identification and Authentication | IA | IA-2 (MFA), IA-5 (Authenticator Management), IA-8 (Non-Org. User Identification) | Confidentiality |
:::

:::list heading="Control Baseline Structure" style=plain
- **Low Baseline**: ~35 controls, minimum protection for low-impact systems
- **Moderate Baseline**: ~180 controls, standard protection for most federal systems
- **High Baseline**: ~230 controls, enhanced protection for high-impact systems
- Controls can be **tailored**: scoped, supplemented, or compensated based on system context
:::

:::code language=mermaid caption="NIST SP 800-53 Rev. 5 control families: 20 families across technical, operational, and management domains provide controls for all CIA properties, each family is tailored to the system's impact level during the RMF Select step"
mindmap
  root((SP 800-53 Rev. 5))
    Confidentiality focus
      AC Access Control
      IA Identification and Authentication
      MP Media Protection
      PE Physical and Environmental
      SC System and Communications
      PT PII Processing and Transparency
    Integrity focus
      AU Audit and Accountability
      CA Assessment and Authorization
      CM Configuration Management
      SA System and Services Acquisition
      SI System and Information Integrity
      SR Supply Chain Risk Management
    Availability focus
      CP Contingency Planning
      IR Incident Response
      MA Maintenance
    Program-wide
      AT Awareness and Training
      PL Planning
      PM Program Management
      PS Personnel Security
      RA Risk Assessment
:::

:::notes
NIST Special Publication 800-53 Revision 5, *Security and Privacy Controls for Information Systems and Organizations* (published September 2020), is the authoritative catalog of security and privacy controls for U.S. federal information systems and serves as the primary reference for control selection across industry sectors. The catalog contains approximately 1,000 individual controls and control enhancements organized into 20 control families, covering technical, operational, and management security domains. It is the primary output of the RMF Select step and the foundation for security plan development, assessment, and authorization decisions.

The 20 control families reflect a comprehensive threat model addressing all dimensions of information security. The **Access Control (AC)** family contains controls for managing user accounts, enforcing access policies, managing remote access, and controlling information flows. AC-2 (Account Management) requires a formal process for creating, modifying, and disabling accounts; AC-3 (Access Enforcement) requires implementation of approved access control policies; AC-17 (Remote Access) requires documented, encrypted, and monitored remote access channels. These controls directly implement confidentiality protections. The **Audit and Accountability (AU)** family requires comprehensive event logging, log protection, and log review to support integrity monitoring and forensic investigations. The **Contingency Planning (CP)** and **Incident Response (IR)** families support availability by requiring tested recovery plans, regular backups, and structured incident handling procedures.

NIST SP 800-53 Rev. 5 introduced several important changes from Rev. 4. It unified security and privacy controls for the first time, adding a **Privacy (PT)** control family and integrating privacy considerations throughout existing families. It introduced the **Supply Chain Risk Management (SR)** family in response to supply chain threats like the SolarWinds SUNBURST attack, requiring organizations to assess and manage the security of their software and hardware supply chains. It also adopted an **outcomes-based** structure that focuses on what controls should achieve rather than how to implement them, providing greater flexibility for innovative implementations while maintaining consistent security outcomes.

Control baselines define the minimum set of controls applicable to systems based on their FIPS 199 impact level. Low-impact systems implement the Low baseline (~35 controls), covering the most fundamental security requirements. Moderate-impact systems implement the Moderate baseline (~180 controls), adding more rigorous account management, more comprehensive logging, stronger authentication requirements, and more detailed contingency planning. High-impact systems implement the High baseline (~230 controls), further adding advanced persistent threat detection capabilities, enhanced supply chain requirements, and more stringent physical security controls. These baselines are starting points, organizations **tailor** them by scoping out controls that are not applicable (a system with no removable media port doesn't need media protection controls for removable media), adjusting parameters (setting password complexity requirements appropriate to their environment), and supplementing with additional controls for specific threats or regulatory requirements.

A key practical skill is mapping specific security scenarios to relevant SP 800-53 controls. When addressing the Colonial Pipeline scenario's MFA gap, the relevant control is IA-2 (Identification and Authentication for Organizational Users), Enhancement 1, which requires MFA for network access to privileged accounts and Enhancement 2 which extends this to non-privileged accounts for high-impact systems. When addressing SolarWinds supply chain integrity, the relevant controls are SR-4 (Provenance), SR-6 (Supplier Assessments and Reviews), and SI-7 (Software, Firmware, and Information Integrity). This mapping capability, translating security incidents and risk scenarios into specific control requirements, is a core skill for security professionals working in NIST-framework environments.

NIST SP 800-53 Rev. 5 is freely available at csrc.nist.gov. Its companion, SP 800-53A Rev. 5, gives the assessment procedure for each control. Together they define what to implement and how to test it, covering the RMF Implement and Assess steps.
:::

%%%

---
unit: Framework
code: FWK
title: FIPS 199, System Categorization in Practice
---
:::callout style=soft
FIPS 199 defines how to categorize federal information and information systems based on the potential impact of a CIA violation. The categorization level (Low / Moderate / High) directly determines the control baseline that must be applied under NIST SP 800-53.
:::

:::steps
**Step 1**: Identify all information types processed, stored, or transmitted by the system (using NIST SP 800-60 as a reference)
**Step 2**: For each information type, determine the potential impact (Low / Moderate / High) of a breach of each CIA property
**Step 3**: The system's overall categorization for each CIA property = the **highest** impact rating across all information types (the "high watermark" principle)
**Step 4**: The overall system categorization = the **highest** of the three CIA categorizations
:::

:::table
| Information Type       | Confidentiality | Integrity | Availability | Overall Type Category |
|------------------------|-----------------|-----------|--------------|------------------------|
| Patient Health Records | High            | High      | Moderate     | High                   |
| Appointment Schedules  | Low             | Moderate  | High         | High                   |
| Billing Information    | High            | High      | Moderate     | High                   |
| **System Overall**     | **High**        | **High**  | **High**     | **High**               |
:::

:::callout style=line
**High Watermark Rule**: A system that processes even a single High-impact information type must be categorized as High for that CIA property, regardless of how many Low or Moderate information types it also processes.
:::

:::code language=mermaid caption="FIPS 199 categorization workflow: the high watermark principle ensures that systems processing any high-sensitivity data receive the highest-baseline controls, preventing under-protection through averaging or majority-rules logic"
flowchart LR
  A["List every information<br/>type in the system"] --> B["Rate C, I, A impact for each<br/>(SP 800-60 guidance)"]
  B --> C["High watermark:<br/>take the highest rating<br/>per property"]
  C --> D["Overall system category<br/>Low, Moderate or High"]
  X["Example: patient records C=High, I=High, A=Moderate<br/>billing C=Moderate, I=High, A=Low<br/>System = High"] -.-> C
:::

:::notes
FIPS 199, *Standards for Security Categorization of Federal Information and Information Systems* (February 2004), is the foundational standard that connects the abstract CIA Triad to concrete control implementation decisions. The categorization process it defines creates a formal, documented link between the sensitivity and criticality of information processed by a system and the security controls that must be implemented to protect it, ensuring that control investment is proportional to the consequences of security failures.

The categorization process begins with an **information type inventory**, a comprehensive enumeration of all categories of data that the system processes, stores, or transmits. NIST SP 800-60 (Guide for Mapping Types of Information and Information Systems to Security Categories) provides a detailed taxonomy of information types for federal systems, organized by mission area (General Government, Defense, Law Enforcement, Healthcare, Financial Management, etc.) and providing recommended CIA impact levels for each. For example, SP 800-60 assigns "Individual Health Information" a recommended impact level of {C: High, I: High, A: Moderate} because unauthorized disclosure causes severe privacy harm (High Confidentiality), incorrect health information causes direct patient safety risk (High Integrity), and while availability is important, clinical operations can often temporarily use backup paper processes (Moderate Availability).

The **high watermark principle** is the critical rule of FIPS 199 categorization. For each CIA property, the system's categorization is the highest impact level assigned to any information type the system handles, not an average, not a majority, not the most common. If a system processes 100 information types at Low impact and one information type at High impact, the system is categorized High for that CIA property. This conservative principle reflects the reality that system-level security controls (encryption, access control, monitoring) cannot selectively apply stronger protection to individual information types while weakening protection for others, the security architecture must protect all information to the standard required by the most sensitive type.

The worked example in this slide illustrates FIPS 199 categorization for a hypothetical hospital EHR system. Patient Health Records require High Confidentiality (patient privacy), High Integrity (clinical decision accuracy), and Moderate Availability (paper fallback procedures available). Appointment Schedules require Low Confidentiality (general scheduling information), Moderate Integrity (incorrect appointments cause operational inefficiency), and High Availability (continuous access required for clinic operations). Billing Information requires High Confidentiality (financial and insurance PII), High Integrity (billing errors cause financial and regulatory harm), and Moderate Availability. Applying the high watermark across all information types for each CIA property: Confidentiality = max(High, Low, High) = High; Integrity = max(High, Moderate, High) = High; Availability = max(Moderate, High, Moderate) = High. The overall system categorization is {C: High, I: High, A: High} = High-impact system, requiring the High control baseline from NIST SP 800-53. This would mandate approximately 230 controls, including advanced authentication requirements, continuous monitoring capabilities, enhanced supply chain security, and comprehensive incident response procedures.

A common error in categorization is attempting to "average" CIA impact levels across information types, leading to a lower-than-appropriate categorization and insufficient control selection. Organizations under regulatory pressure to minimize compliance costs may be tempted to exclude certain information types from categorization scope by arguing they are "temporary" data or "in transit only", but FIPS 199 requires categorization based on all information processed by the system regardless of retention duration or processing mode. Regulators conducting FISMA assessments specifically look for scope manipulation in categorization documentation as an indicator of compliance-focused rather than security-focused categorization.

The practical consequence of categorization is significant: a system categorized as Moderate instead of High (by improperly applying averaging instead of the high watermark) may implement approximately 50 fewer controls, creating significant security gaps in precisely the areas where the misclassified High-impact information type creates the greatest risk. NIST SP 800-37 requires that the Authorizing Official formally review and approve the categorization decision as part of the Prepare step, ensuring that categorization is not made unilaterally by system administrators seeking to reduce compliance burden.
:::

%%%

---
unit: Framework
code: FWK
title: ISO/IEC 27001 vs. NIST RMF, A Comparison
---
:::callout style=soft
Both **ISO/IEC 27001** and the **NIST RMF** provide frameworks for information security management, but they differ in scope, applicability, governance model, and the specificity of their control requirements. Understanding both is essential for security professionals working in multinational or compliance-heavy environments.
:::

:::table
| Dimension                | ISO/IEC 27001                                      | NIST RMF (SP 800-37 + SP 800-53)                          |
|--------------------------|----------------------------------------------------|-----------------------------------------------------------|
| Origin                   | International Standards Organization (ISO)         | U.S. National Institute of Standards and Technology (NIST) |
| Applicability            | Global; any organization type or size              | Mandatory for U.S. federal systems (FISMA); voluntary for others |
| Certification            | Third-party certification by accredited auditors   | Authorization to Operate (ATO) by internal Authorizing Official |
| Scope                    | Entire ISMS (policies, people, processes, technology) | System-specific risk management lifecycle                 |
| Control Catalog          | Annex A: 93 controls across 4 themes (ISO 27002)  | SP 800-53: ~1,000 controls across 20 families             |
| Risk Approach            | Risk treatment plan integrated with ISMS           | Risk-based control selection via FIPS 199 categorization  |
| Update Cycle             | ISO 27001:2022 (current); periodic revision        | SP 800-53 Rev. 5 (2020); NIST updates controls separately |
| Continuous Monitoring    | Recommended via internal audits + management review | Required; SP 800-137 defines formal ISCM program          |
:::

:::list heading="When to Apply Each" style=plain
- **ISO 27001**: Preferred when global operations, international clients, supply chain certification, or non-U.S. regulatory compliance is required (GDPR Article 32 alignment)
- **NIST RMF**: Required for federal agency systems and contractors handling federal information; preferred for DoD, intelligence community, and regulated industries with NIST mandates
- **Both**: Large organizations operating in both federal and international markets often maintain ISO 27001 certification alongside NIST RMF authorization
:::

:::code language=mermaid caption="ISO 27001 vs. NIST RMF: both frameworks address risk-based security management but differ in certification mechanism, control granularity, and regulatory applicability, organizations with both federal and international obligations often implement both simultaneously"
flowchart LR
  subgraph ISO["ISO/IEC 27001 ISMS"]
    direction TB
    P["Plan: scope, risk assessment"] --> D["Do: implement controls"] --> C["Check: monitor, audit"] --> A["Act: management review, improve"] --> P
  end
  subgraph RMF["NIST RMF"]
    direction TB
    R1[Prepare] --> R2[Categorize] --> R3[Select] --> R4[Implement] --> R5[Assess] --> R6[Authorize] --> R7[Monitor]
  end
  P -.- R1
  D -.- R4
  C -.- R5
  A -.- R7
:::

:::notes
ISO/IEC 27001 and the NIST Risk Management Framework represent the two most influential information security governance frameworks worldwide. While they share a common foundation, risk-based management of information security through structured controls, they differ significantly in their governance models, control granularity, certification mechanisms, and regulatory contexts. Security professionals entering the field need a working understanding of both, as most enterprise environments involve some combination of NIST and ISO compliance obligations.

**ISO/IEC 27001** (most recently updated in ISO 27001:2022) defines requirements for establishing, implementing, maintaining, and continually improving an **Information Security Management System (ISMS)**. The ISMS is an organizational system, encompassing policies, procedures, people, processes, and technology, rather than a system-specific security plan. ISO 27001 certification requires an independent audit by an ISO-accredited certification body that verifies the ISMS meets all mandatory requirements. The certification provides external validation recognized by clients, regulators, and trading partners worldwide, making it particularly valuable for organizations selling products or services internationally or participating in global supply chains. ISO 27001 certification is increasingly required as a prerequisite for vendor qualification in healthcare (NHS Digital's DSPT), financial services (Bank of England CBEST), and general supply chain agreements.

ISO 27001's Annex A provides 93 controls organized into four themes: Organizational controls (policies, information security roles), People controls (background checks, security awareness, disciplinary processes), Physical controls (physical security, clear desk), and Technological controls (access management, encryption, network security, vulnerability management). ISO 27002:2022 provides detailed implementation guidance for each Annex A control. While 93 controls may seem far less than NIST SP 800-53's approximately 1,000 controls, ISO controls are higher-level and principle-based, they define outcomes without prescribing implementation specifics. This flexibility makes ISO 27001 adaptable to diverse organizational contexts but requires more interpretive judgment in implementation.

**NIST RMF** is a system lifecycle-focused framework that manages risk through the seven steps from Prepare through Monitor. The authorization mechanism, an internal Authorizing Official making a risk-based ATO decision, provides organizational accountability without requiring external certification. This makes NIST RMF more agile for continuous authorization models where risk decisions must be made in weeks rather than months. NIST SP 800-53's approximately 1,000 controls are highly prescriptive, providing specific technical implementation guidance that reduces interpretive ambiguity but requires significant expertise to apply correctly. The mandatory applicability to U.S. federal systems under FISMA, and the extended requirements for contractors handling federal information (FAR Clause 52.204-21, DFARS 252.204-7012, CMMC), means NIST RMF is non-negotiable for a significant portion of the information security market.

The frameworks are **complementary rather than competing**. NIST SP 800-53 Rev. 5 includes an explicit mapping to ISO/IEC 27001 and 27002 in its appendix, allowing organizations to demonstrate how their SP 800-53 control implementations satisfy ISO 27001 Annex A requirements and vice versa. Organizations operating in both federal and international markets, defense contractors, financial institutions, healthcare organizations, technology companies, typically maintain ISO 27001 certification for their ISMS while pursuing NIST RMF ATOs for specific systems that handle federal information. The ISO 27001 certification demonstrates overall security program maturity; the NIST RMF ATO demonstrates system-specific control implementation.

GDPR Article 32 requires data controllers to implement "appropriate technical and organisational measures" to ensure security appropriate to the risk, a standard that ISO 27001 is widely accepted as demonstrating compliance with. The European Union Agency for Cybersecurity (ENISA) explicitly recognizes ISO 27001 as supporting GDPR Article 32 compliance. NIST has also published a mapping between the NIST Cybersecurity Framework (CSF) and GDPR requirements, enabling organizations using NIST-based frameworks to demonstrate GDPR alignment without requiring ISO certification.

Organizations often need several frameworks at once. A U.S. defense contractor that also sells to European governments and runs a commercial SaaS platform needs the NIST RMF (and likely CMMC Level 2 or 3) for its DoD contracts, ISO 27001 for European government customers and SOC 2 Type II for commercial clients. Each has its own control catalog, assessment method and renewal cycle, which is why framework mapping and integrated compliance programs are a professional specialty.
:::

%%%

---
unit: Framework
code: FWK
title: MITRE ATT&CK, Mapping Adversary Behavior
---
:::callout style=soft
The **MITRE ATT&CK framework** is a globally-accessible knowledge base of adversary tactics, techniques, and procedures (TTPs) based on real-world observations. It translates threat intelligence into actionable knowledge about how attacks progress, enabling both offensive simulation (red team) and defensive detection (blue team).
:::

:::table
| ATT&CK Tactic            | Description                                               | Example Technique                        |
|--------------------------|-----------------------------------------------------------|------------------------------------------|
| Initial Access           | Gaining initial foothold into the network                 | T1190 Exploit Public-Facing Application  |
| Execution                | Running adversary-controlled code                         | T1059 Command and Scripting Interpreter  |
| Persistence              | Maintaining foothold across restarts/credential changes   | T1547 Boot or Logon Autostart Execution  |
| Privilege Escalation     | Gaining higher-level permissions                          | T1068 Exploitation for Privilege Escalation |
| Defense Evasion          | Avoiding detection and analysis tools                     | T1027 Obfuscated Files or Information    |
| Credential Access        | Stealing credentials                                      | T1003 OS Credential Dumping             |
| Discovery                | Mapping the environment post-compromise                   | T1082 System Information Discovery       |
| Lateral Movement         | Moving through the network to additional systems          | T1021 Remote Services                    |
| Collection               | Gathering data of interest                                | T1074 Data Staged                        |
| Exfiltration             | Stealing data out of the network                          | T1041 Exfiltration Over C2 Channel       |
:::

:::list heading="ATT&CK and the CIA Triad" style=plain
- **Credential Access + Lateral Movement** → primary confidentiality attack path
- **Collection + Exfiltration** → confidentiality breach execution
- **Impact: Data Manipulation (T1565)** → integrity attack
- **Impact: Service Stop (T1489), Defacement (T1491)** → availability attack
:::

:::code language=mermaid caption="MITRE ATT&CK Enterprise matrix: 14 tactics and hundreds of techniques document how real adversaries operate, each technique can be mapped to CIA property violations, enabling defenders to prioritize detection and prevention investments"
block-beta
  columns 5
  t1["Reconnaissance"] t2["Resource Development"] t3["Initial Access"] t4["Execution"] t5["Persistence"]
  t6["Privilege Escalation"] t7["Defense Evasion"] t8["Credential Access (C)"] t9["Discovery"] t10["Lateral Movement"]
  t11["Collection (C)"] t12["Command and Control"] t13["Exfiltration (C)"] t14["Impact (I, A)"] space
:::

:::notes
The MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) framework, developed and maintained by MITRE Corporation and first published in 2013, has become the industry standard vocabulary for describing adversary behavior at a level of specificity that enables direct defensive action. Unlike vulnerability frameworks (CVSS) or control frameworks (SP 800-53), ATT&CK describes *what attackers actually do* based on observed intrusions documented in threat intelligence reports, malware analyses, incident response findings, and open-source research. This empirical foundation means ATT&CK techniques describe real attack behaviors rather than theoretical possibilities.

The ATT&CK framework is organized hierarchically. **Tactics** represent the adversary's high-level goals, what they are trying to achieve at each stage of an attack (Initial Access, Execution, Persistence, etc.). **Techniques** describe specific methods for achieving each tactic's goal, there are currently over 400 techniques in the Enterprise ATT&CK matrix. **Sub-techniques** provide more granular detail when a technique encompasses multiple distinct methods (e.g., T1059 Command and Scripting Interpreter has sub-techniques for PowerShell, Python, Windows Command Shell, etc.). **Procedures** document specific instances of technique usage by named threat actors or malware families, providing concrete examples that can be used for threat hunting and detection development.

The **CIA connection** to ATT&CK is direct. Every ATT&CK technique can be mapped to the CIA property it primarily threatens. Confidentiality-targeting techniques include the full spectrum from Credential Access (T1003 OS Credential Dumping, T1555 Credentials from Password Stores) through Collection (T1005 Data from Local System, T1074 Data Staged) to Exfiltration (T1041 Exfiltration Over C2 Channel, T1048 Exfiltration Over Alternative Protocol). Integrity-targeting techniques appear primarily in the Impact tactic: T1565 Data Manipulation targets data integrity directly; T1490 Inhibit System Recovery prevents recovery from integrity attacks; T1072 Software Deployment Tools can be used to modify deployed software at scale. Availability-targeting techniques include T1499 Endpoint Denial of Service, T1489 Service Stop (killing critical services), and T1485 Data Destruction (deleting data rather than encrypting it for ransom).

ATT&CK has three primary enterprise matrices: **Enterprise** (covering Windows, macOS, Linux, cloud, network, and container environments), **Mobile** (iOS and Android), and **ICS** (Industrial Control Systems, critical for critical infrastructure security). The ICS matrix is particularly relevant for understanding attacks like TRITON/TRISIS (2017 Saudi Aramco safety system attack) and CRASHOVERRIDE/Industroyer (2016 Ukraine power grid attack), which specifically targeted operational technology and safety systems to produce physical consequences beyond normal IT security boundaries.

Practitioners use ATT&CK in three primary ways. **Threat intelligence enrichment**: mapping adversary group profiles (e.g., APT29/Cozy Bear, APT41, Lazarus Group) to their documented techniques helps organizations prioritize detection investments against the specific techniques used by threat actors with demonstrated interest in their industry. **Detection development**: each ATT&CK technique has documented data source requirements (the logs and telemetry needed to detect it) and detection logic, enabling security teams to measure and improve their detection coverage against known techniques. **Red team simulation**: penetration testers and red teams use ATT&CK to ensure their exercises test against realistic adversary behaviors rather than theoretical scenarios, enabling organizations to validate their defensive capabilities against techniques actually used in the wild. MITRE's CALDERA platform provides automated adversary emulation based on ATT&CK techniques for continuous testing.

The MITRE ATT&CK Navigator (attack.mitre.org) shows techniques as an interactive matrix that can be colored by detection coverage, actor usage or impact. Mapped onto it, the SolarWinds SUNBURST attack covers T1195.002 Compromise Software Supply Chain (Initial Access), T1027 Obfuscated Files or Information (Defense Evasion, as SUNBURST mimicked legitimate Orion traffic), T1071 Application Layer Protocol (Command and Control), T1119 Automated Collection (Collection) and T1048 Exfiltration Over Alternative Protocol (Exfiltration).
:::

%%%

---
unit: Risk
code: RSK
title: Quantitative vs. Qualitative Risk Assessment
---
:::callout style=soft
Risk assessments can be conducted either **qualitatively** (using descriptive scales like Low/Moderate/High) or **quantitatively** (using numerical values and financial figures). Each approach has strengths and appropriate use cases, most mature risk programs use a combination of both.
:::

:::table
| Dimension               | Qualitative Assessment                              | Quantitative Assessment                                    |
|-------------------------|-----------------------------------------------------|------------------------------------------------------------|
| Likelihood Expression   | Descriptive: Low / Moderate / High                  | Numerical: probability (e.g., 15% annual likelihood)       |
| Impact Expression       | Descriptive: Low / Moderate / High                  | Financial: dollar value of expected loss                   |
| Key Metric              | Risk rating (e.g., High risk)                       | Annual Loss Expectancy (ALE = ARO × SLE)                   |
| Data Requirements       | Expert judgment and industry benchmarks             | Historical incident data, actuarial tables, asset valuations |
| Communication           | Accessible to executives; easy to understand        | Directly comparable to other business risks in financial terms |
| Limitations             | Subjectivity; different raters may assess differently | Data scarcity; difficult to value intangible assets (reputation) |
| Best Framework          | NIST SP 800-30 qualitative scales                   | FAIR (Factor Analysis of Information Risk)                  |
:::

:::list heading="Quantitative Risk Formulas" style=plain
- **SLE (Single Loss Expectancy)** = Asset Value × Exposure Factor, the expected financial loss from a single occurrence
- **ARO (Annualized Rate of Occurrence)** = how many times per year the incident is expected to occur
- **ALE (Annualized Loss Expectancy)** = SLE × ARO, the expected annual loss from a specific risk
- **ROI of Control** = (ALE before control) − (ALE after control) − (Annual Cost of Control)
:::

:::code language=mermaid caption="Qualitative vs. quantitative risk comparison: qualitative matrices provide accessible prioritization; FAIR quantitative analysis translates risk to financial terms that enable direct comparison with other business investment decisions"
flowchart LR
  subgraph QL["Qualitative"]
    direction TB
    L["Likelihood: High"] --> RQ["Risk: High<br/>(red cell in the matrix)"]
    IM["Impact: High"] --> RQ
  end
  subgraph QN["Quantitative (FAIR / ALE)"]
    direction TB
    AV["Asset value $500,000"] --> SLE["SLE = AV x EF<br/>$500,000 x 40% = $200,000"]
    EF["Exposure factor 40%"] --> SLE
    SLE --> ALE["ALE = SLE x ARO<br/>$200,000 x 0.5 = $100,000 per year"]
    ARO["ARO 0.5 per year"] --> ALE
  end
  QL ~~~ QN
:::

:::notes
The debate between qualitative and quantitative risk assessment represents one of the most practically significant methodological choices in risk management. NIST SP 800-30 Rev. 1 explicitly recognizes both approaches and acknowledges that most practical risk assessments blend elements of each. Understanding the strengths, limitations, and appropriate applications of both approaches is essential for security professionals who must communicate risk to diverse audiences, from technical staff to boards of directors to regulators.

**Qualitative risk assessment** uses structured descriptive scales to evaluate likelihood and impact. The NIST SP 800-30 approach defines five likelihood levels (Very Low, Low, Moderate, High, Very High) and three impact levels (Low, Moderate, High), producing risk ratings that can be communicated in a risk matrix. The primary advantages of qualitative assessment are its accessibility (non-technical stakeholders can understand and participate in the assessment), its practicality (it doesn't require precise historical data that may not exist), and its consistency with major frameworks (NIST SP 800-30, ISO/IEC 27005, and OCTAVE all primarily use qualitative scales). The primary limitations are subjectivity (two competent analysts may disagree on whether a threat is "Moderate" or "High" likelihood) and the difficulty of directly comparing security risk ratings with financial metrics used for other business investment decisions.

**Quantitative risk assessment** expresses risk in numerical terms, most commonly financial values. The foundational quantitative risk formulas are: **Asset Value (AV)** is the replacement or market value of the asset at risk; **Exposure Factor (EF)** is the percentage of asset value lost in a successful attack (0.0–1.0); **Single Loss Expectancy (SLE = AV × EF)** is the expected financial loss from a single occurrence of the threat; **Annualized Rate of Occurrence (ARO)** is the estimated frequency of the threat materializing per year; and **Annualized Loss Expectancy (ALE = SLE × ARO)** is the expected financial loss per year from the risk. For example: a company has a customer database worth $5 million in competitive value and recovery costs (AV = $5M). If a successful SQL injection attack would compromise 40% of the database (EF = 0.40), the SLE = $5M × 0.40 = $2M. If SQL injection attacks occur approximately once every 5 years on similar systems (ARO = 0.2), the ALE = $2M × 0.2 = $400,000 per year. This ALE can be directly compared to the $80,000 annual cost of implementing an application security testing program, producing a clear financial ROI for the control.

The **FAIR (Factor Analysis of Information Risk)** framework, developed by Jack Jones and formalized by the Open FAIR Body of Knowledge (OpenFAIR), provides a rigorous quantitative risk methodology that decomposes risk into a probability distribution model. FAIR distinguishes between Risk (the probable frequency and magnitude of future loss) and the underlying factors that drive it: Threat Event Frequency (TEF), Vulnerability (Threat Capability vs. Control Strength), and Loss Magnitude (Primary and Secondary loss components). FAIR enables Monte Carlo simulation to produce probability distributions of ALE rather than point estimates, capturing the inherent uncertainty in risk quantification and providing confidence intervals for risk figures. FAIR is increasingly used in enterprise risk management programs, particularly in financial services and healthcare, where boards require financially expressed risk metrics comparable to other enterprise risk categories (market risk, credit risk, operational risk).

The practical choice between qualitative and quantitative approaches depends on available data, audience, and purpose. For initial risk assessment and control prioritization, qualitative matrices are practical and sufficient. For security investment justification to C-suite and board audiences, quantitative ALE or FAIR-based analysis provides the financial language that executives use for all other capital allocation decisions. For regulatory compliance (FISMA, HIPAA, PCI DSS), qualitative assessments are generally accepted, these frameworks do not require financial quantification. For mature, data-rich programs (large enterprises with years of incident data and sophisticated threat intelligence), quantitative approaches provide more precise prioritization and enable actuarial-style risk transfer decisions (e.g., calculating the optimal cyber insurance deductible and coverage limit based on loss probability distributions).

A worked example of quantitative risk: a university records system holds 50,000 FERPA-protected student records. Asset value is $2M (regulatory fines plus remediation). With an exposure factor of 0.6, SLE = $1.2M. With an ARO of 0.15, based on breach rates at similar institutions, ALE = $180,000 a year. A $30,000-a-year investment in database activity monitoring, MFA for administrators and encrypted backups lowers the ARO to about 0.05, giving a new ALE of $60,000. The net annual benefit is ($180,000 − $60,000) − $30,000 = $90,000.
:::

%%%

---
unit: Risk
code: RSK
title: Worked Example, Hospital EHR System Risk Assessment
---
:::callout style=soft
Applying the full risk assessment methodology to a concrete scenario: a hospital's Electronic Health Records (EHR) system. We walk through asset identification, threat and vulnerability analysis, likelihood and impact assessment, risk matrix placement, and control selection.
:::

:::steps
**Step 1, Asset Identification**: Hospital EHR system processes PHI for 150,000 patients; data includes medical history, medications, diagnoses, insurance, SSNs; system availability critical for clinical operations
**Step 2, Threat Identification**: Ransomware (high probability in healthcare sector); credential theft via phishing; insider threat; third-party vendor access abuse
**Step 3, Vulnerability Assessment**: Legacy EHR software (unpatched CVEs); VPN access without MFA; inadequate network segmentation; overprivileged service accounts
**Step 4, Likelihood Assessment**: Ransomware + unpatched legacy software + VPN without MFA = HIGH likelihood; insider threat with audit logging gaps = MODERATE likelihood
**Step 5, Impact Assessment**: Ransomware: HIPAA breach (HHS fine up to $1.9M/incident), clinical shutdown ($50K/day revenue loss), patient safety risk (HIGH); Insider: PHI disclosure to external party (HIPAA reportable), financial harm (MODERATE-HIGH)
**Step 6, Risk Matrix**: Ransomware: High Likelihood × High Impact = HIGH risk; Insider: Moderate × Moderate-High = HIGH risk
**Step 7, Controls**: MFA for all remote access, EHR vendor patch management SLA, network segmentation, privileged access management, HIPAA-compliant audit logging, tested DR plan with 4-hour RTO
:::

:::table
| Risk Scenario          | Likelihood | Impact | Risk Level | Primary Control                          |
|------------------------|------------|--------|------------|------------------------------------------|
| Ransomware via VPN     | High       | High   | High       | MFA on all VPN access (IA-2)             |
| Phishing → EHR access  | High       | High   | High       | Security awareness training + email filtering (AT-2, SI-8) |
| Insider PHI disclosure | Moderate   | High   | High       | Privileged access management + AU-2 logging |
| Legacy CVE exploitation | Moderate  | High   | High       | Vendor patch management SLA + SI-2       |
| DDoS clinical outage   | Low        | High   | Moderate   | DDoS mitigation + local caching (SC-5)   |
:::

:::code language=mermaid caption="Hospital EHR risk assessment worked example: applying NIST SP 800-30 methodology from asset identification through control selection demonstrates how the risk equation, risk matrix, and SP 800-53 control catalog work together in a realistic healthcare security context"
flowchart TB
  A["Asset inventory<br/>EHR database, clinician workstations, medical devices"] --> T["Threats and vulnerabilities<br/>ransomware, phishing, unpatched servers"]
  T --> LI["Likelihood and impact ratings"] --> M["Risk matrix"]
  M --> CT["SP 800-53 controls<br/>CP-9 backups, AT-2 training, SI-2 patching, AC-2 accounts"]
  CT --> RR["Residual risk accepted or treated"]
:::

:::notes
This worked example applies every concept from today's lecture to a realistic scenario that demonstrates how formal risk assessment methodology translates into specific, defensible security decisions. Healthcare is an ideal sector for this exercise because it combines all three CIA property concerns at high severity: confidentiality of patient health information (legally protected by HIPAA), integrity of clinical data (patient safety implications), and availability of clinical systems (direct patient care consequences).

The scenario is grounded in real-world statistics. Healthcare is the most frequently targeted sector for ransomware attacks: the FBI and HHS reported 210 healthcare ransomware incidents in 2022 alone. The average cost of a healthcare data breach is $10.9 million (IBM Cost of a Data Breach Report 2023), the highest of any sector for 13 consecutive years. The 2020 ransomware attack on Universal Health Services (UHS), one of the largest U.S. hospital chains, forced clinical staff to revert to paper records across hundreds of hospitals for several weeks, delaying test results and forcing patient diversions to other facilities. These statistics calibrate the "High" likelihood and "High" impact ratings in our example, they are not arbitrary; they reflect documented experience in this sector.

The **asset identification** step for the EHR system must be comprehensive: the 150,000 patient records represent regulatory liability (HIPAA covered PHI), competitive sensitivity (patient population data), and clinical necessity (clinicians depend on this data for care decisions). The system's operational criticality for clinical care means availability failures have direct patient safety implications, clinicians who cannot access medication histories may make dosing errors, and clinicians who cannot access allergy records may prescribe contraindicated medications. NIST SP 800-60 maps "Individual Health Information" to a High impact level for all three CIA properties for exactly these reasons.

The **threat analysis** for healthcare is informed by sector-specific threat intelligence. The HHS 405(d) Cybersecurity Task Group maintains a Health Industry Cybersecurity Practices (HICP) guide that identifies the top threats specific to the healthcare sector: phishing attacks leading to ransomware deployment, attacks on connected medical devices, and insider threats related to excessive privileged access. The FBI's Internet Crime Complaint Center (IC3) publishes annual sector-specific threat data that validates both the threat source characteristics (primarily financially motivated criminal groups with significant ransomware capabilities) and the frequency of attacks (making "High" likelihood rating defensible with external data rather than pure expert judgment).

The **control selection** maps directly to NIST SP 800-53 controls. MFA on all VPN access (control IA-2, Enhancement 1) directly addresses the credential theft → remote access path. The HIPAA Security Rule specifically references multi-factor authentication under Access Control standards (45 CFR § 164.312(d)), creating dual regulatory authority for this control investment. Network segmentation limits lateral movement after initial compromise, NIST SP 800-53 SC-7 (Boundary Protection) and SC-32 (Information System Partitioning) define the segmentation requirements. Privileged Access Management (PAM) implements the principle of least privilege through just-in-time access provisioning, reducing the attack surface available to insider threats and external attackers who have compromised service accounts. The tested DR plan with a 4-hour RTO implements the Contingency Planning family requirements (CP-2, CP-9, CP-10) and the HIPAA Contingency Plan standard (45 CFR § 164.308(a)(7)) simultaneously.

The worked example also illustrates risk prioritization in practice: all five risk scenarios in the table produce High or Moderate risk ratings, but they are not equally urgent. The two ransomware-related scenarios (ransomware via VPN and phishing → EHR access) both receive High risk ratings and represent the most probable and most costly threats based on sector data, they warrant immediate emergency investment regardless of budget constraints. The DDoS clinical outage scenario receives only a Moderate rating because while impact is High, likelihood is Low given that the hospital is not a high-profile public target and DDoS attacks on hospital EHR systems are less common than ransomware. This Moderate risk scenario can be addressed in the next budget cycle rather than requiring emergency expenditure, illustrating how risk prioritization prevents wasteful allocation of scarce security resources to lower-probability threats at the expense of higher-probability ones.
:::

%%%

---
unit: Risk
code: RSK
title: Risk Appetite vs. Risk Tolerance, The Governance Boundary
---
:::callout style=soft
Risk management is not the elimination of all risk, it is the management of risk within defined boundaries. **Risk appetite** and **risk tolerance** are the governance parameters that define those boundaries, turning risk management from a technical exercise into a boardroom-level governance discipline.
:::

::::columns
::col::
:::callout style=line
**Risk Appetite**
The *amount and type* of risk an organization is willing to **pursue** in the pursuit of its objectives. It is a strategic, forward-looking statement set by the board or executive leadership.

Example: "We accept moderate cybersecurity risk from digital innovation initiatives but zero tolerance for risks that could result in patient harm."
:::
::col::
:::callout style=line
**Risk Tolerance**
The *acceptable variation* around the risk appetite, the degree to which actual risk exposure may deviate from the stated appetite before action is required.

Example: An organization with a "Moderate" appetite for data breach risk may tolerate exposure to one breach per five years but trigger escalation above that rate.
:::
::::

:::table
| Organization Type        | Typical Cybersecurity Risk Appetite                           | Rationale                                                 |
|--------------------------|---------------------------------------------------------------|-----------------------------------------------------------|
| Financial Institution    | Low, regulatory consequences of breach are severe            | OCC, FFIEC, PCI DSS; customer trust is core business asset |
| Defense Contractor       | Near-zero for classified data                                 | DFARS, CMMC; national security consequences               |
| Healthcare Provider      | Low for PHI; moderate for operational technology             | HIPAA; patient safety implications                        |
| Technology Startup       | Moderate-High for some systems; Low for customer PII          | Speed-to-market priority; limited resources              |
| Critical Infrastructure  | Very Low for OT/control systems                              | Physical safety and national security consequences        |
:::

:::list heading="How Risk Appetite Drives Security Decisions" style=plain
- Systems exceeding risk tolerance trigger automatic escalation to executive leadership
- Risk acceptance decisions must be made by officials with authority commensurate with risk appetite
- NIST RMF Authorize step formalizes risk tolerance through the ATO process
- ISO 31000 (Risk Management Guidelines) defines risk appetite as an ISMS governance requirement
:::

:::image src="images/02_risk_appetite_tolerance.png" alt="Dial diagram with a risk appetite indicator set to Moderate and a risk tolerance band shaded around it showing acceptable deviation; below the dial, a risk inventory heat map shows individual risks plotted as dots, with dots inside the tolerance band labeled Accepted, dots outside labeled Escalated to Board, and arrows showing the governance escalation process" caption="Risk appetite and tolerance governance: the dial represents strategic risk appetite; the band represents acceptable variance; individual risks are accepted within the band or escalated when they exceed tolerance, formalizing risk governance at the board level" width=full
:::

:::notes
Risk appetite and risk tolerance are governance concepts that transform risk management from a purely technical discipline into an organizational governance practice. Without formally defined risk appetite and tolerance statements, risk management decisions are made ad hoc by whoever encounters the risk, often low-level technical staff with insufficient authority, context, or organizational visibility to make sound governance decisions. Formal risk appetite statements ensure that risk decisions are made at the appropriate organizational level with full awareness of business strategy, regulatory requirements, and stakeholder expectations.

**Risk appetite** is defined in ISO 31000:2018 as "the amount and type of risk that an organization is prepared to pursue or retain." It is a strategic governance concept that should be established by the board of directors or equivalent governance body and communicated throughout the organization as a boundary condition for all risk-taking activities. Risk appetite statements are typically qualitative (expressed in descriptive terms) but may be supplemented with quantitative thresholds (e.g., "We will not accept annual expected losses exceeding $5 million from cybersecurity incidents"). Risk appetite is inherently tied to organizational strategy: a healthcare organization's mission of patient care creates a very low appetite for any risk that could compromise patient safety, while the same organization's drive to improve care through digital innovation may create a higher appetite for technology adoption risks.

**Risk tolerance** is the operationalization of risk appetite, the specific, measurable thresholds that define when actual risk exposure has exceeded acceptable limits and requires escalation or treatment. Risk tolerance converts the strategic concept of appetite into operational governance: "Our risk appetite is Low for PHI breach risk. Our risk tolerance is no more than one HIPAA reportable breach per year. If our risk assessment indicates that current exposure would result in greater than one breach per year, the CISO must present a remediation plan to the board within 30 days." This threshold-based structure enables automated risk monitoring (SIEM alerts, vulnerability scanner outputs, incident rates) to trigger governance escalation when thresholds are breached.

The NIST RMF institutionalizes risk tolerance through the Authorize step. The Authorizing Official (AO), a senior executive with sufficient authority and accountability, reviews the residual risk of each system against the organizational risk tolerance and makes a formal ATO decision: accept the residual risk (within tolerance), accept conditionally with a POA&M (risk is currently above tolerance but has a credible remediation plan), or deny authorization (risk is above tolerance with no acceptable path to remediation within a defined timeframe). The ATO decision is explicitly an organizational governance decision, not a technical determination, the AO may accept risks that exceed a system owner's comfort level if they fall within organizational risk tolerance, or may decline risks that technically could be accepted if they conflict with the organization's strategic risk appetite.

The relationship between risk appetite and security budget is direct and underappreciated. Organizations with well-defined, board-approved risk appetite statements can calculate the gap between current risk exposure (from risk assessments) and the organization's maximum acceptable exposure (from risk tolerance thresholds). This gap, the "risk reduction needed", translates directly into the minimum required security investment to bring the organization within its risk appetite. This calculation provides security professionals with a governance-backed, board-level justification for security spending that is far more persuasive than technical arguments alone. The Ponemon Institute and others have documented that organizations with formal risk appetite frameworks achieve higher security investment levels and better security outcomes than those making ad hoc investment decisions.

A formal risk appetite turns a security request into a governance requirement. If the board has set a Low appetite for data-breach risk and the current assessment rates PHI breach risk as Moderate, the gap between exposure and tolerance gives the CISO authority to request funding to close it. Without a formal statement, the same request is only an opinion. Risk appetite is a strategic business tool, not a compliance checkbox.
:::

%%%

---
unit: Defense
code: DEF
title: Defense in Depth, Layered Security Architecture
---
:::callout style=soft
**Defense in Depth** is the security architecture principle of deploying multiple, independent layers of controls so that the failure of any single control does not result in a complete security failure. It is the architectural embodiment of the CIA Triad applied to adversarial reality.
:::

:::flow
Perimeter Layer (Firewall, IDS/IPS, DDoS mitigation)
Network Layer (Segmentation, VLANs, Zero Trust access control)
Endpoint Layer (EDR, host firewall, full-disk encryption, patch management)
Application Layer (WAF, input validation, secure coding, API security)
Data Layer (Encryption at rest, DLP, access control, data classification)
Identity Layer (MFA, PAM, RBAC, identity lifecycle management)
Physical Layer (Access control, surveillance, secure media handling)
:::

:::list heading="Why Layers Work" style=plain
- An attacker who bypasses the perimeter firewall still faces network segmentation
- An attacker who obtains valid credentials still faces MFA and least-privilege access
- An attacker who reaches the data still faces encryption and DLP monitoring
- No single control failure results in a complete CIA property violation
:::

:::table
| Layer            | Primary CIA Focus | Example Controls                           | Example Failure Scenario                    |
|------------------|-------------------|--------------------------------------------|---------------------------------------------|
| Perimeter        | All (first barrier) | Next-gen firewall, WAF, DDoS mitigation  | WAF bypass via zero-day HTTP parsing flaw   |
| Network          | Confidentiality   | VLAN segmentation, micro-segmentation      | Attacker pivots within allowed VLAN         |
| Endpoint         | Integrity, Availability | EDR, patch management, Secure Boot   | EDR detection evaded via living-off-the-land |
| Application      | Integrity, Confidentiality | Input validation, code signing, SAST | SQL injection via unvalidated parameter     |
| Data             | Confidentiality, Integrity | AES-256 encryption, HMAC, DLP     | Encryption key mismanagement                |
| Identity         | Confidentiality   | MFA, PAM, RBAC                            | MFA bypass via SIM swap                     |
:::

:::image src="images/02_defense_in_depth_layers.png" alt="Concentric ring diagram with Data at the center surrounded by successive rings labeled Identity, Application, Endpoint, Network, Perimeter, and Physical, each ring labeled with example controls and color-coded by primary CIA association, with an attack arrow showing multiple layers an attacker must penetrate and the lateral movement challenge when segmentation prevents easy traversal" caption="Defense in depth architecture: concentric security layers ensure that an attacker must defeat multiple independent controls to reach the data at the center, each layer independently limits attack impact even when outer layers are bypassed" width=full
:::

:::notes
Defense in depth is the architectural principle that transforms the CIA Triad from an abstract goal into a resilient, practical security architecture. The principle draws an analogy from medieval castle design: a castle was not defended by a single wall but by multiple concentric barriers, a moat, outer walls, inner walls, the keep, and finally the vaulted strongroom. Each barrier independently delayed and impeded attackers; the overall defense was far stronger than any single layer. Modern information security architecture applies the same principle: no single control is assumed to be impenetrable, but the combination of multiple independent controls creates a defense that is significantly harder to defeat than any individual component.

The layered model presented here applies defense in depth across seven security domains, each addressing CIA property threats from a different architectural vantage point. The **Perimeter Layer** provides initial network-level screening and traffic filtering. Next-generation firewalls (NGFWs) combine traditional packet filtering with deep packet inspection, application awareness, and integrated intrusion prevention. Web Application Firewalls (WAFs) protect internet-facing applications from common web attacks (SQL injection, XSS, CSRF) by analyzing HTTP/HTTPS traffic before it reaches application servers. DDoS mitigation services absorb volumetric attack traffic before it reaches the network perimeter. However, sophisticated attackers regularly bypass perimeter controls through TLS-encrypted channels that evade inspection, legitimate cloud service abuse (exfiltrating data via Google Drive or Dropbox), and social engineering attacks that originate from trusted insiders rather than external network traffic, demonstrating why the perimeter cannot be the only defensive layer.

The **Network Layer** implements micro-segmentation to limit lateral movement after a perimeter breach. Network segmentation using VLANs, subnets, and firewall rules enforces the principle of least-access at the network layer: a compromised workstation in the Sales VLAN should have no network path to the database servers in the Finance VLAN. Zero-trust network architecture (ZTNA) extends this principle by verifying every connection attempt regardless of source, no implicit trust is granted to traffic originating inside the corporate network. The SolarWinds SUNBURST attack's success in reaching sensitive government networks via the Orion monitoring platform (which required broad network access for its legitimate monitoring functions) illustrates the critical importance of network segmentation: monitoring tools should have read-only access to network devices, not broad administrative access that enables lateral movement to sensitive systems.

The **Endpoint Layer** addresses threats that have reached individual systems. Endpoint Detection and Response (EDR) platforms monitor endpoint behavior in real-time for indicators of compromise (IoCs) and suspicious behavioral patterns (credential dumping, process injection, anomalous network connections), enabling rapid detection and automated or analyst-driven response. Patch management ensures that known CVEs are remediated quickly, the CISA KEV catalog provides binding timelines for federal systems but is also a best-practice reference for private sector organizations. Secure Boot (UEFI) prevents boot-time attacks by verifying cryptographic signatures on all boot components. Full-disk encryption protects data on endpoints from physical theft, ensuring that even a stolen device cannot be read without the encryption key.

The **Identity Layer** has emerged as the most critical single security layer in modern architectures due to the "identity is the new perimeter" reality of cloud-first, remote-work environments where traditional network perimeters no longer exist. MFA reduces the risk of credential theft attacks by requiring a second factor even when passwords are compromised. Privileged Access Management (PAM) systems implement just-in-time access provisioning, session recording, and credential rotation for administrative accounts, the highest-value targets for attackers. Role-based access control (RBAC) ensures that each user has only the minimum access required for their specific job functions, limiting the blast radius of any single compromised account.

The multiplicative effect of layered controls explains why defense in depth produces security outcomes significantly better than any single control in isolation. Consider an attacker pursuing a credential-theft-to-data-exfiltration attack chain. Without defense in depth: compromise credential → access any system → access all data → exfiltrate. With defense in depth: compromise credential → stopped by MFA (Identity Layer); or bypass MFA via SIM swap → stopped by network segmentation (Network Layer); or cross segment → stopped by EDR detecting anomalous behavior (Endpoint Layer); or evade EDR → stopped by DLP detecting bulk data access patterns (Data Layer); or evade DLP → stopped by data encryption making exfiltrated data unreadable without key (Data Layer). Each layer independently reduces the probability of complete attack success, even if each individual layer has a 30% bypass probability, five independent layers produce only a 0.3^5 = 0.24% probability of complete success, compared to 30% for a single layer.

Defense in depth means choosing the highest-value control at each layer, not deploying every control. For a 20-person fintech startup that processes payments from the cloud, the physical layer matters little; the budget belongs in identity (MFA, privileged access management) and application security (a WAF, code review), which are the largest attack surfaces for internet-facing financial applications.
:::

%%%

---
unit: Summary
code: SUM
title: Checkpoint, Key Concepts Review
---
:::callout style=soft
Mid-lecture checkpoint: before we continue, let's confirm we have the foundational concepts solidly in place. Each of these concepts feeds into the next, a gap in any one creates confusion in everything that follows.
:::

::::columns
::col::
:::list heading="CIA Triad, Check Your Understanding" style=plain
- Can you define each property in one sentence using NIST language?
- Can you give one technical control and one real-world breach example for each?
- Can you classify a given incident by which CIA property (or properties) it violates?
:::
::col::
:::list heading="Risk Equation, Check Your Understanding" style=plain
- Risk = Likelihood × Impact: can you calculate a risk rating from given L and I values?
- Can you identify what factors increase or decrease likelihood for a given scenario?
- Can you assess impact across all five dimensions (operational, financial, regulatory, reputational, safety)?
:::
::::

::::columns
::col::
:::list heading="Risk Matrix, Check Your Understanding" style=plain
- Can you place a given scenario on a 3×3 risk matrix?
- Can you explain why Low Likelihood × High Impact = Moderate (not High)?
- Can you select an appropriate risk response (Accept/Avoid/Mitigate/Transfer) for a given risk level?
:::
::col::
:::list heading="NIST RMF, Check Your Understanding" style=plain
- Can you name the seven RMF steps in order?
- Can you explain the high watermark principle in FIPS 199?
- Can you identify which NIST SP 800-53 control family addresses a given security gap?
:::
::::

:::table
| Concept         | Key Formula / Standard             | One-Line Takeaway                                                  |
|-----------------|------------------------------------|--------------------------------------------------------------------|
| CIA Triad       | FIPS 199, NIST SP 800-53           | Defines WHAT we protect                                            |
| Risk Equation   | NIST SP 800-30 Rev. 1              | Quantifies HOW MUCH protection is needed                           |
| Risk Matrix     | ISO/IEC 27005                      | Prioritizes WHERE to invest first                                  |
| Risk Response   | ISO 31000                          | Determines HOW to address each risk                                |
| NIST RMF        | NIST SP 800-37 Rev. 2              | Operationalizes WHEN and HOW OFTEN to reassess                     |
| CVSS            | FIRST CVSSv3.1                     | Standardizes vulnerability severity for prioritization             |
| Defense in Depth | NSA / NIST general guidance       | Ensures no single failure produces complete CIA violation           |
:::

:::code language=mermaid caption="Checkpoint concept map: all topics connect, CIA defines what to protect, risk analysis quantifies the threat to it, the risk matrix prioritizes responses, the RMF operationalizes continuous management, and defense in depth architects the controls"
flowchart TB
  CIA["CIA Triad"] --> DC["Data Classification"]
  CIA --> CC["CIA Controls"]
  RE["Risk = Likelihood x Impact"]
  RE --> LK["Likelihood<br/>CVSS, threat actors"]
  RE --> IP["Impact<br/>FIPS 199, business impact"]
  LK --> RM["Risk Matrix"]
  IP --> RM
  RM --> TR["Treatment: mitigate, transfer,<br/>avoid, accept"]
  CC --> TR
  DC --> IP
:::

:::notes
This checkpoint slide serves a dual pedagogical purpose: it consolidates the conceptual connections between topics covered so far, and it surfaces gaps in understanding before students encounter the more application-focused content in the second half of the lecture. The questions in each quadrant are deliberately structured as competency tests rather than knowledge recall prompts, they test whether students can *apply* concepts, not just repeat definitions.

The CIA Triad questions test application-level understanding. The ability to classify a real incident by CIA property violation is a foundational security analyst skill: when a ransomware attack occurs, is it a Confidentiality violation (PII exposed), an Integrity violation (files encrypted = modified), an Availability violation (systems inaccessible), or all three (common in ransomware with double extortion)? Students who can perform this classification confidently have internalized the CIA Triad as an analytical tool rather than a vocabulary list. The ability to name a specific technical control for each property tests whether students understand the *how* of CIA protection, not just the *what*. A student who can name AES-256 as a Confidentiality control but cannot explain *why* it protects Confidentiality (prevents unauthorized reading of encrypted data) has memorized a vocabulary term without understanding the underlying mechanism.

The Risk Equation questions test quantitative reasoning. Students who can correctly place "High Likelihood × Low Impact = Moderate risk" and explain that the Low impact caps the risk rating despite high frequency have understood that the equation's multiplicative structure means both dimensions matter, neither alone determines the risk level. This understanding is essential for avoiding two common prioritization errors: over-investing in mitigating low-impact, high-frequency events (because they generate many "incidents") and under-investing in low-frequency, catastrophic-impact risks (because they "never happen here").

The NIST RMF questions test framework literacy. The seven-step sequence (Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor) should be automatic, these steps appear in security plan documentation, ATO packages, and continuous monitoring reports throughout the career of any security professional working in or with the federal government. The high watermark principle is the single most commonly misapplied element of FIPS 199 categorization: students who understand it will correctly recognize when an organization has attempted to reduce their compliance burden by improperly averaging CIA impact levels rather than applying the maximum. The NIST SP 800-53 control family mapping question tests whether students have developed the ability to connect a vulnerability or gap description to the relevant control family, a skill that turns the 1,000-control catalog from an overwhelming reference into a practical lookup tool.

The summary table crystallizes the "one-line takeaway" for each major framework or concept: CIA defines WHAT to protect, risk analysis defines HOW MUCH protection is needed, the risk matrix determines WHERE to invest first, risk response determines HOW to address each risk, the NIST RMF defines WHEN and HOW OFTEN to reassess, CVSS standardizes vulnerability severity for prioritization, and defense in depth ensures no single failure produces complete CIA violation. These one-liners are intentionally memorable, they provide the conceptual anchors that connect abstract frameworks to practical decision-making. Students who can map each of these "one-liners" to the relevant standard (NIST SP 800-30, FIPS 199, ISO/IEC 27005, NIST SP 800-37) have achieved the framework literacy needed to navigate real-world compliance and security program development contexts.

Two points are commonly weak at this stage: classifying ambiguous incidents that violate several CIA properties at once, and explaining how FIPS 199 categorization drives the selection of SP 800-53 controls.
:::

%%%

---
unit: Summary
code: SUM
title: Putting Risk Analysis to Work
---
::::columns
::col::
:::callout style=soft
Confidentiality, integrity, and availability define what we protect. Likelihood and impact turn threats and vulnerabilities into a measurable risk. The RMF makes managing that risk a continuous, repeatable process, not a one-time fix.
:::
::col::
:::list style=chips
- Confidentiality
- Integrity
- Availability
- Likelihood
- Impact
- Risk Matrix
- RMF
:::
::::
::::card
:::table
| Risk Level     | Likelihood × Impact | Example Scenario                        |
|----------------|---------------------|-----------------------------------------|
| High           | High × High         | Data breach exposing customer PII       |
| Medium         | Medium × Medium     | Temporary service degradation           |
| Low            | Low × Low           | Minor configuration error, no exposure  |
:::
::::
:::steps
1. Identify risks using asset, threat, and vulnerability assessments.
2. Analyze likelihood and impact to quantify risk exposure.
3. Evaluate risk against organizational risk tolerance (NIST SP 800-30).
4. Select risk response: Accept, Avoid, Mitigate, or Transfer.
5. Implement controls aligned with selected response.
6. Monitor and review risk posture continuously.
7. Improve risk analysis and response mechanisms iteratively.
:::

:::image src="images/02_risk_analysis_workflow_summary.png" alt="End-to-end risk analysis workflow diagram showing seven steps from asset identification through continuous improvement, with CIA Triad, NIST SP 800-30 risk equation, and RMF lifecycle icons annotated at each relevant step" caption="Risk analysis synthesis: the complete workflow from CIA property identification through asset inventory, threat and vulnerability assessment, risk quantification, response selection, and continuous monitoring under the NIST RMF" width=full
:::

:::notes
At the heart of information security lies the CIA triad, confidentiality, integrity, and availability, which collectively define the core attributes of information that we seek to protect. However, understanding *what* to protect is only the first step in a rigorous security program. To operationalize security, we must assess *how likely* it is that a threat will exploit a vulnerability, and what the *impact* would be if it did. This transformation of qualitative threat data into quantifiable, prioritized risk is the essence of risk analysis, and it is what separates reactive security from proactive, risk-informed security management.

Risk is expressed as a function: **Risk = Likelihood × Impact**. This deceptively simple equation embeds enormous analytical depth. Likelihood requires assessing threat source characteristics (capability, motivation, access) and vulnerability exploitability (CVSS scores, exploit availability, existing controls). Impact requires assessing consequences across CIA dimensions (confidentiality breach severity, integrity corruption extent, availability disruption duration) and translating technical impacts into business terms (financial loss, regulatory exposure, reputational damage). The equation's multiplicative structure means that either dimension independently drives risk level: a near-certain minor incident and a rare catastrophic incident may warrant equal attention depending on organizational risk tolerance.

The **risk matrix** provides a visual prioritization mechanism that makes risk assessments accessible to executive leadership. By mapping likelihood against impact in a structured grid, security teams can communicate complex risk landscapes in a format that enables rapid prioritization and resource allocation decisions. The matrix's simplicity is a feature rather than a limitation, it forces clarity and consensus about relative risk ratings that might otherwise remain ambiguous in purely numerical analyses.

The **Risk Management Framework (RMF)**, defined in NIST SP 800-37, operationalizes risk analysis into a continuous organizational discipline. Its seven steps, Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor, ensure that risk management is not a one-time compliance activity but an embedded, iterative operational practice. The Monitor step's continuous feedback into earlier phases creates the adaptive capability needed to respond to the rapidly evolving threat landscape: new vulnerabilities, emerging threat actors, changing business processes, and shifting regulatory requirements all demand ongoing risk reassessment.

Risk responses, Accept, Avoid, Mitigate, Transfer, translate risk analysis into operational decisions. Each response has appropriate use cases, cost implications, and governance requirements. Effective risk response selection requires not just technical judgment but organizational context: the same risk rating might lead to different responses in a defense contractor (strong regulatory pressure to mitigate) versus a startup (financial constraints may favor acceptance for non-critical systems). The risk response decision must be documented, approved, and periodically reviewed as part of a mature risk governance process.

In the next lecture, we will shift focus to the adversaries themselves, examining specific threat actor categories, their motivations, capabilities, and the MITRE ATT&CK framework that catalogs their observable behaviors. Understanding who is attacking (threat actors) and why (motivations) provides the qualitative threat intelligence that feeds the likelihood dimension of our risk equation, transforming it from an abstract formula into a grounded assessment of real-world adversarial capability and intent.
:::

%%% 
---
unit: "Risk Assessment"
code: RAS
title: "Quantitative vs. Qualitative Risk Assessment"
---

:::text class=sub
Key differences and applications of quantitative and qualitative risk assessment methodologies.
:::

:::callout style=soft
While both approaches have their place in the risk management lifecycle, they serve different purposes and offer varying levels of precision.
:::

:::list heading="Quantitative vs. Qualitative Risk Assessment" style=plain
- **Quantitative**: Numerical values assigned to risk components (likelihood and impact) using statistical models or expert judgment.
  - Pros: Provides a precise numerical value for risk, allowing for easier comparison and prioritization.
  - Cons: Requires significant data and resources, may not account for all risks.
- **Qualitative**: Risk components are assessed using non-numerical scales or categorical labels.
  - Pros: Less resource-intensive, can be used when data is scarce or uncertain.
  - Cons: Does not provide a precise numerical value, may lead to subjective assessments.
:::

:::table
| Methodology | Data Requirements | Complexity |
|-------------|-------------------|------------|
| Quantitative | Extensive data    | High       |
| Qualitative | Limited data      | Low        |
:::

:::code language=mermaid caption="Quantitative vs. Qualitative Risk Assessment: Choosing the Right Approach"
flowchart LR
  QL["<b>Qualitative</b><br/>Ratings: Low, Medium, High<br/>Fast, relies on expert judgment<br/>Used for: first-pass triage, little data"] -->|"refine the top risks"| QN["<b>Quantitative</b><br/>Dollar values: SLE, ARO, ALE<br/>Needs reliable loss and frequency data<br/>Used for: budgets, insurance, cost-benefit"]
:::

:::notes
Risk assessments can be categorized into two primary types: quantitative and qualitative. Quantitative risk assessment involves assigning numerical values to risk components (likelihood and impact) using statistical models or expert judgment. This approach provides a precise numerical value for risk, allowing for easier comparison and prioritization. However, it requires significant data and resources, which may not always be available.

Qualitative risk assessment, on the other hand, assesses risk components using non-numerical scales or categorical labels. While this approach is less resource-intensive and can be used when data is scarce or uncertain, it does not provide a precise numerical value for risk, leading to potential subjective assessments. The choice between these methodologies depends on the specific needs of the organization and the type of risks being assessed.

In practice, organizations often use a combination of both approaches, starting with qualitative assessments to identify high-risk areas and then applying quantitative methods to refine their understanding of those risks. For instance, in the 2019 Capital One data breach, attackers exploited a web application vulnerability (CVE-2020-10349) that had been previously identified through a qualitative risk assessment. The subsequent investigation highlighted the importance of ongoing monitoring and regular updates to ensure that security controls remain effective.

References:
* NIST SP 800-30 Rev. 1: Guide for Conducting Risk Assessments
* ISO/IEC 27001:2013: Information technology, Security techniques, Information security management systems, Requirements
:::
