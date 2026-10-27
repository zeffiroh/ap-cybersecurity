---
deck:
  title: Cybersecurity Foundations
  kicker: Class 1
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 1
  description: Goals, assets, threats, vulnerabilities, risk management, attack surface, roles, and the security mindset.
  topics: [Goals, Assets, Threats, Vulnerabilities, Risk, Attack Surface, Roles, Mindset]
---

---
unit: Class 01
title: Cybersecurity Foundations
cover: true
---
:::text class=sub
Academic Reading Handout · Information Assurance Foundations
:::
::::columns
::col::
:::list heading="Core Concept Areas" style=chips
- Theoretical Security Models
- Foundational Frameworks (NIST, ISO, MITRE)
- Risk Management & Controls
- Professional Practice & Ethics
:::
::col::
:::callout style=soft
Cybersecurity is a multidisciplinary field rooted in computer science, systems theory, risk analysis, and behavioral psychology. This course establishes the conceptual and operational foundations necessary for advanced study and practice.
:::
::::

:::image src="images/01_cybersecurity_overview_diagram.png" alt="Cybersecurity discipline overview showing the intersection of people, process, and technology with governance frameworks" caption="Cybersecurity as a multidisciplinary field: People, Process, and Technology converge under governance frameworks such as NIST CSF, ISO 27001, and MITRE ATT&CK" width=full
:::

:::notes
Welcome to the foundational lecture of our cybersecurity curriculum. Before engaging with tools, technologies, or attack simulations, it is essential to establish a rigorous academic and conceptual understanding of what cybersecurity is, why it matters, and how it is structured as a discipline.

At its core, cybersecurity is the practice of protecting information systems and data from unauthorized access, use, disclosure, disruption, modification, or destruction. This protection is framed around the CIA triad, Confidentiality, Integrity, and Availability, which serves as the foundational security model. Confidentiality ensures that information is accessible only to those authorized to view it. Integrity ensures that data remains accurate and trustworthy throughout its lifecycle. Availability ensures that systems and data are accessible when needed by authorized users.

Beyond the CIA triad, modern cybersecurity frameworks extend these principles. The Parkerian Hexad, introduced by Donn B. Parker in the 1990s, adds Possession (control over data), Authenticity (verified origin), and Utility (usefulness of information) to the traditional triad, providing a more comprehensive model for evaluating information security requirements. Meanwhile, architectural frameworks such as the Gartner Adaptive Security Architecture emphasize continuous monitoring, prediction, and adaptive response as the pillars of modern security operations.

Cybersecurity is also deeply standardized. The National Institute of Standards and Technology (NIST) provides comprehensive frameworks such as the NIST Cybersecurity Framework (CSF), updated to version 2.0 in February 2024, and Special Publications including SP 800-53 (Security Controls for Federal Systems) and SP 800-30 (Risk Assessment Guide). The SP 800 series represents over two decades of applied security research and is legally mandated for U.S. federal agencies under the Federal Information Security Modernization Act (FISMA). Internationally, ISO/IEC 27001 offers a globally recognized model for Information Security Management Systems (ISMS), focusing on risk-based thinking, continuous improvement, and organizational accountability.

The historical context of cybersecurity is equally instructive. The discipline emerged from concerns about computer fraud in the 1970s, was formalized through early U.S. government initiatives such as the Trusted Computer System Evaluation Criteria (TCSEC, or "Orange Book") in 1983, and has evolved through landmark incidents such as the Morris Worm of 1988 (one of the first recognized computer worms), the publication of the Computer Fraud and Abuse Act (CFAA) in 1986, and more recent watershed events such as the 2017 WannaCry ransomware attack (CVE-2017-0144), the 2020 SolarWinds supply chain breach (CVE-2020-10148), and the 2021 Log4Shell vulnerability (CVE-2021-44228).

This lecture introduces foundational models, frameworks, and professional roles that will be expanded upon in subsequent classes. It is critical to understand that cybersecurity is not just about tools, it is about structured thinking, risk prioritization, and aligning technical decisions with organizational objectives. A security professional who understands frameworks and threat models will always outperform one who merely knows how to operate tools, because tools change, but adversary logic and organizational risk principles remain consistent.
:::

%%%

---
unit: Foundations
code: DEF
title: What Is Cybersecurity?
---
::::columns ratio=1:1
::col::
:::callout style=soft
**Cybersecurity** is a multidimensional discipline focused on safeguarding information systems, networks, and data from threats, both internal and external. It integrates governance, risk management, and compliance through a structured model of *People, Process, and Technology*. This triad ensures that security is not only technical but also organizational and procedural.
:::
:::list heading="NIST CSF 2.0 Core Functions" style=plain smartart=RadialCluster
- **Govern (GV):** Develops the organizational context for managing cybersecurity risk, including policies, risk tolerance, and strategic alignment.
- **Identify (ID):** Establishes the business context, resource dependencies, and associated risks to systems and assets.
- **Protect (PR):** Deploys safeguards to ensure delivery of critical services and limit the impact of potential incidents.
- **Detect (DE):** Implements continuous monitoring to identify cybersecurity events and anomalies.
- **Respond (RS):** Executes response plans to mitigate the impact of incidents and maintain stakeholder communication.
- **Recover (RC):** Restores capabilities and implements improvements to prevent recurrence.
:::
::col::
:::image src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/NIST_Version_2.0.png/640px-NIST_Version_2.0.png" alt="NIST Cybersecurity Framework 2.0 Core Functions" caption="NIST CSF 2.0 Core Functions: Govern, Identify, Protect, Detect, Respond, Recover" width=full
:::
::::

:::image src="images/01_nist_csf_cycle_diagram.png" alt="NIST CSF 2.0 lifecycle cycle showing the six functions in a continuous loop around a central governance layer" caption="The NIST CSF 2.0 cycle: Govern anchors the five operational functions (Identify, Protect, Detect, Respond, Recover) in an iterative, risk-driven loop" width=half
:::

:::notes
Cybersecurity, at its core, is the practice of defending digital environments, including hardware, software, data, and services, from malicious actors and unintended harm. It is not merely about deploying firewalls or antivirus tools; rather, it is a strategic discipline that must be embedded into the organizational fabric through governance, risk assessment, and continuous operational vigilance.

The **NIST Cybersecurity Framework (CSF) 2.0**, released in February 2024, represents a mature evolution of the original framework, now emphasizing governance as a foundational element. The addition of the **Govern (GV)** function underscores that cybersecurity must be aligned with business objectives, regulatory requirements, and enterprise risk management strategies. Without governance, organizations risk implementing disjointed or misaligned security controls that fail to protect critical assets effectively.

Each of the six functions operates in a continuous cycle:
- **Identify** requires organizations to maintain an accurate inventory of assets, understand their interdependencies, and assess vulnerabilities using standards like **NIST SP 800-53** or **ISO/IEC 27001**.
- **Protect** involves implementing safeguards such as access control mechanisms (e.g., RBAC, MFA), encryption, and employee awareness training.
- **Detect** leverages tools like SIEMs (Security Information and Event Management) and intrusion detection systems to identify anomalies or indicators of compromise (IoCs), such as those cataloged in **MITRE ATT&CK** or **CVE databases**.
- **Respond** includes incident triage, containment, eradication, and communication with internal and external stakeholders, often guided by playbooks aligned with **NIST SP 800-61**.
- **Recover** focuses on restoring systems and services while incorporating lessons learned to improve resilience, often referencing frameworks like **ISO 22301** for business continuity.

A real-world analogy helps contextualize this framework: consider a bank's vault security. The bank *identifies* its most valuable assets (cash, customer records), *protects* them (vault doors, cameras, guards), *detects* intrusions (alarm sensors, teller alerts), *responds* to incidents (lockdown procedures, law enforcement notification), and *recovers* (insurance claims, system audits). Cybersecurity applies the same logic to digital environments, but at a far greater scale and velocity.

The "People, Process, Technology" model further reinforces that no single dimension is sufficient. A perfect technical control (firewalls, encryption) is undermined if people are not trained to use it correctly, or if processes do not mandate its use. Conversely, a well-trained workforce cannot compensate for absent technical controls. This interdependence is why governance, the Govern function in CSF 2.0, is now formally elevated as the foundation of the entire framework.

This cyclical model reflects the reality that cybersecurity is not a one-time project but a persistent, adaptive process essential for organizational resilience in an increasingly threat-laden digital ecosystem.
:::

%%%

---
unit: Goals
code: CIA
title: The Cybersecurity Goals, CIA Triad & Beyond
---
::::columns ratio=1:1:1
::col::
::::card heading="Confidentiality"
:::list style=tight
- **Core Definition:** Restricting access to authorized entities only.
- **Mechanisms:** Advanced Encryption Standard (AES), Role-Based Access Control (RBAC), multi-factor authentication (MFA).
- **Academic Context:** Ensuring privacy under data protection laws like GDPR.
:::
::::
::col::
::::card heading="Integrity"
:::list style=tight
- **Core Definition:** Maintaining data trustworthiness and accuracy.
- **Mechanisms:** Cryptographic hash algorithms (SHA-256), digital signatures, database transaction constraints.
- **Academic Context:** Protecting against tampering and spoofing.
:::
::::
::col::
::::card heading="Availability"
:::list style=tight
- **Core Definition:** Assuring timely access to systems and services.
- **Mechanisms:** Redundant arrays (RAID), load balancing, failover clustering, DDoS mitigations.
- **Academic Context:** Maintaining service level agreements (SLAs).
:::
::::
::::

:::callout style=line
**Expanding the Triad:** Modern frameworks also demand **Authenticity** (verifying identity) and **Non-repudiation** (proving action occurrence, e.g., via asymmetric key cryptography).
:::

:::image src="images/cia_triad.jpg" alt="The CIA Triad of Information Security" caption="The CIA Triad of Information Security" width=half
:::

:::image src="images/01_parkerian_hexad_diagram.png" alt="The Parkerian Hexad extending the CIA Triad with Possession, Authenticity, and Utility as additional security dimensions" caption="The Parkerian Hexad: an extension of the CIA Triad that adds Possession, Authenticity, and Utility, providing a more complete model for information security requirements" width=half
:::

:::image src="images/01_cia_integrated_principles.png" alt="Venn diagram of confidentiality, integrity and availability and the qualities each pair produces" caption="Venn diagram of confidentiality, integrity and availability and the qualities each pair produces" width=half
:::

:::notes
The foundational principles of cybersecurity are encapsulated in the CIA triad, Confidentiality, Integrity, and Availability, which collectively define the core objectives of any secure information system. These principles form the cornerstone of numerous international standards including NIST SP 800-53, ISO/IEC 27001, and the Common Criteria for Information Technology Security Evaluation (ISO/IEC 15408). The triad was not invented by a single body but rather emerged organically through decades of security research and standardization, and it remains the most universally recognized model in the field.

Confidentiality ensures that sensitive information is accessible only to those who are authorized to view it. This is typically enforced through encryption mechanisms such as the Advanced Encryption Standard (AES-256), which is NIST-approved under FIPS 197 for protecting sensitive government information. Access control models like Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC) determine who may access what resources based on organizational roles or contextual attributes. Multi-factor authentication (MFA) further strengthens confidentiality by requiring multiple forms of verification before granting access. From a regulatory perspective, maintaining confidentiality aligns with legal frameworks such as the General Data Protection Regulation (GDPR), HIPAA, and the California Consumer Privacy Act (CCPA). A famous real-world breach of confidentiality is the 2013 Yahoo breach, which exposed credentials of approximately 3 billion user accounts, one of the largest in history.

Integrity refers to the assurance that data remains accurate and unaltered during storage or transmission unless intentionally modified by an authorized entity. Cryptographic techniques such as SHA-256 hashing and digital signatures play a critical role in detecting unauthorized modifications. The SHA-2 family (including SHA-256 and SHA-512) is standardized in FIPS PUB 180-4 and is widely deployed in TLS, code signing, and blockchain systems. In databases, integrity can be enforced using constraints and triggers to maintain consistency. A man-in-the-middle attack that alters financial transaction details (as in the BGP hijacking incident of 2010, where traffic was rerouted through routers in China) violates data integrity, which can have severe consequences in both business and personal contexts.

Availability guarantees that systems and data remain accessible to legitimate users when needed. This is supported by redundancy mechanisms such as RAID configurations (particularly RAID-1 mirroring or RAID-6 with dual parity), failover clustering, and load balancing. Network-level protections like DDoS mitigation strategies, including rate limiting, anycast routing, and scrubbing centers, are essential to ensure continuous service delivery. The failure of availability can lead to significant operational disruptions, as seen in the 2017 WannaCry ransomware attack (CVE-2017-0144), which rendered critical NHS hospital systems inaccessible for days, directly impacting patient care. The 2021 Colonial Pipeline ransomware attack similarly illustrated how availability failures in operational technology can cascade into real-world physical consequences.

Beyond the traditional triad, modern security frameworks recognize two additional properties. Authenticity confirms the verified identity of a user, system, or data origin, often achieved through cryptographic certificates (X.509) and challenge-response protocols. Non-repudiation prevents an individual from later denying their involvement in a transaction, typically implemented using asymmetric cryptography such as RSA or ECDSA digital signatures, a property critical for legal enforceability of digital contracts and audit trails. Together, these five properties, Confidentiality, Integrity, Availability, Authenticity, and Non-repudiation, constitute a comprehensive model for information security assurance. The Parkerian Hexad further adds Possession (physical control over data media), expanding the model to six dimensions for particularly sensitive environments.
:::

%%%

---
unit: Goals
code: INT
title: Cryptographic Enforcement of Integrity
---
:::text
Cryptographic hashing is a foundational mechanism for enforcing data integrity in cybersecurity. A cryptographic hash function is a deterministic, one-way mathematical transformation that maps input data of arbitrary size to a fixed-size output, commonly referred to as a **message digest** or **hash value**. The output is typically represented as a hexadecimal string. The function must satisfy several critical security properties:
:::

:::list heading="Core Properties of Cryptographic Hash Functions" style=plain smartart=HexagonCluster
- **Deterministic**: The same input always produces the same hash.
- **Pre-image Resistance**: Given a hash value, it is computationally infeasible to determine the original input.
- **Second Pre-image Resistance**: Given an input, it is computationally infeasible to find another input that produces the same hash.
- **Collision Resistance**: It is computationally infeasible to find two different inputs that produce the same hash.
:::

:::callout style=soft
The **avalanche effect** is a key property ensuring that even a single-bit change in the input results in approximately 50% of the output bits changing. This makes hash functions highly sensitive to input variations, enabling reliable integrity checks.
:::

:::code language=python caption="Demonstrating SHA-256 and the Avalanche Effect in Python"
import hashlib  # Python's built-in cryptographic library; implements SHA-2 per FIPS PUB 180-4

def calculate_sha256(data: str) -> str:
    """Calculates the SHA-256 hash of a given string.

    SHA-256 produces a 256-bit (32-byte) fixed-size digest regardless of input length.
    It is a one-way function: the original input cannot be recovered from the output.
    """
    # encode('utf-8') converts the Python str to bytes, hashlib requires a bytes-like object
    # sha256() initializes the SHA-256 hash context using the NIST-approved algorithm
    # hexdigest() returns the 256-bit digest as a 64-character lowercase hex string
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Baseline message representing authentic, unaltered financial transaction data
msg_original = "Authorize transfer of $10,000.00 to Account A."

# Tampered message representing an unauthorized modification, only destination account changed
# This simulates a man-in-the-middle integrity attack on a financial transaction
msg_tampered = "Authorize transfer of $10,000.00 to Account B."

hash_orig = calculate_sha256(msg_original)  # Compute digest of the legitimate message
hash_tamp = calculate_sha256(msg_tampered)  # Compute digest of the tampered message

print(f"Original Msg: '{msg_original}'")
print(f"Original Hash: {hash_orig}")        # 64 hex chars represent 256 bits
print(f"Tampered Msg: '{msg_tampered}'")
print(f"Tampered Hash: {hash_tamp}")        # Avalanche effect: ~50% of bits will differ

# Hash comparison detects integrity violation
# NOTE: In production, use hmac.compare_digest() instead of != to prevent
# timing side-channel attacks (constant-time comparison guards against timing analysis)
if hash_orig != hash_tamp:
    print("\n[ALERT] Data integrity breach detected! Hashes do not match.")
:::

:::image src="images/01_sha256_avalanche_effect.png" alt="Visual demonstration of the avalanche effect: two nearly identical inputs producing completely different SHA-256 hashes, with bit difference highlighted" caption="The SHA-256 avalanche effect: a single character change in input ('A' to 'B') results in approximately 50% of output bits changing, making unauthorized modifications immediately detectable" width=full
:::

:::notes
Cryptographic enforcement of data integrity is a cornerstone of secure communication and data storage. At its core, it relies on **cryptographic hash functions**, which are standardized mathematical algorithms designed to take an input (or message) and produce a fixed-size string of bytes. The output, known as a **hash value** or **message digest**, is unique to the input data. Even a minor change in the input, such as altering a single character, results in a drastically different hash output. This behavior is known as the **avalanche effect**, and it is a critical security property ensuring that tampering is easily detectable.

The Secure Hash Algorithm 2 (SHA-2) family, defined by NIST in FIPS PUB 180-4, includes SHA-256, which is widely used in security protocols such as TLS, IPsec, S/MIME, and blockchain systems including Bitcoin. SHA-256 generates a 256-bit (32-byte) hash value, typically rendered as a 64-character hexadecimal string. The algorithm processes input in 512-bit blocks through 64 rounds of bitwise operations, including additions modulo 2^32, bitwise ANDs, XORs, and rotations. The algorithm is designed to be **collision-resistant**, meaning it is computationally infeasible, requiring approximately 2^128 operations per the birthday bound, to find two distinct inputs that hash to the same output. This property is essential for ensuring that attackers cannot forge data that matches the hash of an authentic message.

An important historical note: SHA-1 (the predecessor to SHA-2) was found to be collision-vulnerable in 2017 when Google's Project Zero team demonstrated a practical collision attack (known as "SHAttered"), producing two different PDF files with identical SHA-1 hashes. This incident accelerated the global migration to SHA-256 and above, illustrating that cryptographic standards must be continuously evaluated against evolving computational capabilities. NIST formally deprecated SHA-1 for most uses in 2011 and prohibited its use in digital signatures by 2014.

In the provided Python example, two nearly identical messages are hashed using SHA-256. The first message authorizes a transfer to Account A, while the second alters the destination to Account B. Despite the minimal change (a single character), the resulting hashes are entirely different, illustrating the avalanche effect in practice. In real-world systems, message hashes are stored or transmitted alongside the message itself, in signed software distributions, secure boot manifests, or TLS certificate chains. Upon receipt, the recipient recalculates the hash and compares it to the stored reference. A mismatch indicates a potential integrity breach. A notable real-world application is the Git version control system, which uses SHA-1 (and is migrating to SHA-256) to uniquely identify every commit, file, and tree object in a repository, ensuring that any modification to history is immediately detectable.

This mechanism is foundational in numerous security frameworks and standards. ISO/IEC 27001 emphasizes the importance of data integrity controls as part of an ISMS, and NIST SP 800-57 (Recommendation for Key Management) outlines the use of cryptographic mechanisms for protecting information at rest and in transit. Hash-based integrity checks are central to digital signatures (where the document hash is signed rather than the full document), certificate validation (X.509 certificates include signed hashes of public keys), and secure software distribution (package managers verify SHA-256 checksums before installation).

The code also demonstrates an important security engineering consideration: the comment about `hmac.compare_digest()`. Using a standard inequality operator (`!=`) to compare hash strings in Python creates a potential timing side-channel vulnerability, the comparison terminates early upon finding the first differing character, leaking information about where the strings diverge. The `hmac.compare_digest()` function performs a constant-time comparison regardless of where strings differ, eliminating this vulnerability. This subtle detail illustrates how cryptographic correctness extends beyond algorithm choice to implementation details.
:::

%%%

---
unit: Assets
code: AST
title: Asset Inventory & Taxonomy (ISO 27001)
---
:::table
| Asset Category | Description | Key Protection Mechanism |
|---|---|---|
| **Information / Data** | Intellectual property, customer databases, system configurations, source code. | Encryption-at-rest, access control lists (ACLs). |
| **Software Assets** | Operating systems, application suites, APIs, custom proprietary code. | Code signing, static application security testing (SAST). |
| **Physical Assets** | Servers, endpoints, network equipment, physical facility infrastructure. | Access logs, biometric checkpoints, hardware security modules (HSM). |
| **Human Assets** | Employees, contractors, users, and their digital credentials. | Security awareness training, identity & access management (IAM). |
| **Services** | Core computing resources, DNS, cloud service providers, network bandwidth. | Redundancy, service-level monitoring, API gateways. |
:::

:::callout style=line
**ISO/IEC 27001 Annex A.8:** Mandates that all assets must be identified and an inventory of assets must be drawn up and maintained to ensure consistent security controls.
:::

:::flow smartart=CircleProcess
Define Asset Scope and Organizational Boundaries
Enumerate All Information and Technology Assets
Classify Each Asset by Sensitivity and Criticality
Assign Asset Ownership (Individual Accountability)
Implement Controls Proportionate to Classification
Review and Update Inventory Continuously
:::

:::code language=mermaid caption="ISO/IEC 27001 Asset Inventory & Taxonomy"
mindmap
  root((Asset inventory))
    Information
      Databases, contracts, records
    Software
      Applications, operating systems
    Physical
      Servers, laptops, network gear
    Services
      Cloud, power, connectivity
    People
      Skills, knowledge
    Intangibles
      Reputation, brand
:::

:::image src="images/01_asset_classification_workflow.png" alt="Asset classification workflow showing asset discovery, enumeration, classification by sensitivity, owner assignment, and control mapping" caption="ISO 27001-aligned asset classification workflow: assets are discovered, enumerated, classified by business impact, assigned to owners, and mapped to proportionate security controls" width=half
:::

:::notes
Before you can build a defense, you must know what you are defending. In cybersecurity, this fundamental principle is operationalized through the practice of asset inventory and classification. According to the international standard ISO/IEC 27001:2022, Clause 8.1 and Annex A Control 5.9 (Information and other associated assets), maintaining a complete and current asset inventory is an absolute requirement for establishing an effective Information Security Management System (ISMS). The standard defines an information asset as anything that has value to the organization and must therefore be identified, classified, and protected proportionally.

We categorize assets into five main taxonomies, each with distinct protection requirements. **Information and Data** assets represent the crown jewels of most organizations, customer records, intellectual property, source code, cryptographic keys, and configuration files. These are protected using encryption at rest (e.g., AES-256 on disk via BitLocker or dm-crypt) and in transit (TLS 1.3), combined with granular access control lists and data loss prevention (DLP) tools. A classic example of inadequate information asset protection is the 2017 Equifax breach, where unencrypted personally identifiable information (PII) of 147 million individuals was exposed due to an unpatched web application vulnerability (CVE-2017-9805, Apache Struts).

**Software Assets** encompass all programs, operating systems, firmware, and APIs that process or manage data. Protecting software assets involves code signing (ensuring software originates from a trusted publisher and has not been modified), static application security testing (SAST) during development, and software composition analysis (SCA) to identify vulnerable third-party dependencies. The 2020 SolarWinds attack (CVE-2020-10148) demonstrated how compromised software assets, specifically a tampered build pipeline, can become a vector for widespread supply chain attacks.

**Physical Assets** include the hardware layer: servers, workstations, routers, switches, and the physical facilities that house them. Physical security forms the foundation of logical security, an attacker with physical access to a server can bypass most software protections through techniques like cold boot attacks (extracting encryption keys from RAM) or direct memory access (DMA) via Thunderbolt ports. Access controls such as biometric locks, mantrap entry systems, hardware security modules (HSMs), and CCTV surveillance are essential physical safeguards.

**Human Assets**, employees, contractors, and users, are simultaneously the most valuable and most exploitable asset category. Social engineering, phishing, and insider threats all target the human element. ISO/IEC 27001 mandates ongoing security awareness training (Annex A Control 6.3), background verification (A.6.1), and disciplinary processes for policy violations. Organizations invest in identity and access management (IAM) platforms, privileged access workstations (PAWs), and user behavior analytics (UBA) to monitor and control human asset risk.

**Services** represent operational dependencies: DNS, authentication services, cloud platforms (AWS, Azure, GCP), and network bandwidth. Service disruptions, even of seemingly minor components, can cascade into complete operational failures. For example, the October 2021 Facebook outage, caused by a BGP configuration error, rendered Facebook, Instagram, and WhatsApp inaccessible to billions of users for approximately six hours, illustrating how critical service dependencies must be inventoried and protected.

By mapping assets to this taxonomy, organizations can apply the principle of proportionality: resources invested in protecting an asset should be commensurate with the value of that asset and the risk of its compromise. This aligns with the ISO 27001 risk treatment process and NIST SP 800-53's asset management control family (PM-5, CM-8), ensuring that security investments are both efficient and defensible.
:::

%%%

---
unit: Assets
code: GOV
title: Classifying Data Sensitivity & Governance
---

::::columns
::col::
:::table
| Sensitivity Level | Description | Impact of Exposure | Regulatory Framework |
|---|---|---|---|
| **Public** | Low sensitivity; intended for general release. | Negligible; no reputational or financial harm. | N/A (Marketing/Public PR) |
| **Internal** | Non-public organizational operational details. | Low to moderate; minor competitive disadvantage. | NDA / Internal Policy |
| **Confidential** | Proprietary strategic data, customer records. | High; financial loss, brand damage, litigation. | GDPR, CCPA, ISO 27001 |
| **Restricted** | Highly sensitive; protected under strict laws. | Catastrophic; severe legal fines, complete loss of trust. | HIPAA (PHI), PCI-DSS (Cardholder) |
| **Secret (Govt)** | Classified national security information. | Threatens national security, defense, or infrastructure. | Executive Order 13526 |
:::

::col::
:::callout style=soft
**Classification-based controls** dictate how data is handled: from encryption requirements (e.g., AES-256 for Restricted data) to disposal policies (e.g., cryptographic erasure or physical degaussing).
:::

:::list heading="Key Governance Standards" style=plain
- **NIST SP 800-60 Vol. 2**: Guide for Mapping Types of Information and Information Systems to Security Categories
- **ISO/IEC 27001**: Information security management systems (ISMS)
- **GDPR Article 30**: Records of processing activities
- **HIPAA Security Rule**: Administrative, physical, and technical safeguards
:::
::::

:::image src="images/01_data_classification_pyramid.png" alt="Data classification pyramid showing five tiers from Public at the base to Secret Government at the apex, with regulatory frameworks and control requirements at each level" caption="Data sensitivity classification pyramid: each ascending tier represents greater sensitivity, stricter controls, and more severe consequences for unauthorized disclosure" width=half
:::

:::notes
Data classification is a foundational element of information governance and risk management. It enables organizations to apply proportionate security controls based on the value, sensitivity, and criticality of information assets. Without proper classification, resources may be misallocated, resulting in either under-protection of sensitive data or over-investment in securing low-value information. The data classification framework is sometimes described as the "Rosetta Stone" of security policy: once a classification label is assigned, it triggers an entire cascade of handling requirements, access controls, retention policies, and disposal procedures.

The five-tier classification model presented in this slide reflects industry best practices and aligns with standards such as **NIST Special Publication 800-60 Volume 2**, which provides guidance on categorizing information types and mapping them to security impact levels (Low, Moderate, High) as defined by FIPS 199. Each level defines not only the nature of the data but also the potential consequences of its unauthorized disclosure, modification, or destruction, consequences evaluated across the CIA triad dimensions.

**Public** data requires minimal protection because exposure poses no harm. Examples include press releases, marketing materials, job postings, and publicly filed financial reports. In contrast, **Internal** data, such as employee handbooks, internal project plans, or system architecture diagrams, should remain within the organization but does not typically trigger regulatory penalties if disclosed accidentally. However, internal data may still enable competitive intelligence gathering by adversaries.

**Confidential** data includes intellectual property, financial records, strategic business plans, and customer records. Its exposure can lead to significant business harm including loss of competitive advantage, stock price impact, and breach of contract liability. This tier is commonly subject to contractual obligations under non-disclosure agreements and compliance frameworks like **ISO/IEC 27001** and regional privacy laws such as the **General Data Protection Regulation (GDPR)**, which imposes breach notification requirements within 72 hours of discovery under Article 33.

**Restricted** data is legally protected and includes personally identifiable information (PII), protected health information (PHI) governed by **HIPAA** (which mandates administrative, physical, and technical safeguards under 45 CFR Parts 164), and payment card data regulated by the **PCI DSS** (Payment Card Industry Data Security Standard). Mishandling such data can result in severe penalties, including fines up to €20 million or 4% of annual global turnover under GDPR, or per-incident fines and card processing privilege revocation under PCI DSS. The 2014 Home Depot breach, which exposed 56 million payment card records, resulted in over $179 million in settlements, a stark illustration of Restricted data exposure consequences.

Finally, **Secret** data applies primarily to government and military contexts. In the U.S., this classification is defined under **Executive Order 13526** (Classified National Security Information), which establishes the classification system with levels: Confidential, Secret, and Top Secret, based on the degree of damage to national security that unauthorized disclosure could cause. Handling such data requires personnel with active security clearances issued by the U.S. government and stored on systems approved by the Defense Information Systems Agency (DISA) under the Risk Management Framework (RMF).

Effective data governance mandates the implementation of **classification-based controls** throughout the data lifecycle: collection, processing, storage, transmission, and disposal. Encryption requirements scale with classification level (AES-256 minimum for Restricted), and data disposal must be verifiably irreversible, using cryptographic erasure (overwriting encryption keys) for storage media or physical degaussing and shredding for hardware that cannot be sanitized through software. Organizations deploying cloud infrastructure must also ensure classification labels are enforced across hybrid environments, an increasingly complex challenge as data traverses multiple jurisdictions.
:::

%%%

---
unit: Threats
code: THR
title: Threat Modeling Frameworks, STRIDE & PASTA
---
::::columns ratio=1:1
::col::
::::card heading="STRIDE (Microsoft)"
:::list style=tight smartart=vList5
- **S**poofing (targets Authenticity)
- **T**ampering (targets Integrity)
- **R**epudiation (targets Non-repudiation)
- **I**nformation Disclosure (targets Confidentiality)
- **D**enial of Service (targets Availability)
- **E**levation of Privilege (targets Authorization)
:::
::::
::col::
::::card heading="PASTA (Risk-Centric)"
:::steps
Define objectives & business impact
Define technical scope & assets
Deconstruct application & data flows
Analyze threats & adversary behavior
Detect vulnerability & weaknesses
Model attack paths & simulate exploits
Conduct risk & impact analysis
:::
::::
::::

:::callout style=soft
**Threat modeling** is a proactive engineering process: we identify potential threats before code is deployed, ensuring security by design.
:::

:::image src="images/01_stride_pasta_comparison.png" alt="Side-by-side comparison of the STRIDE and PASTA threat modeling frameworks, showing how STRIDE maps threats to security properties while PASTA provides a seven-stage risk-centric analysis process" caption="STRIDE vs. PASTA: STRIDE provides a developer-friendly threat classification system mapped to security properties, while PASTA offers a risk-centric, business-aligned seven-stage methodology" width=full
:::

:::image src="images/01_pasta_stages_illustrated.png" alt="Illustrated threat-modeling stages: prepare, attack, scan, test, address" caption="Illustrated threat-modeling stages: prepare, attack, scan, test, address" width=half
:::

:::notes
Threat modeling is a structured approach to identifying, quantifying, and addressing potential security threats within a system before they can be exploited. It is a foundational practice in secure software development that aligns with standards such as NIST SP 800-30 (Risk Management Guide) and ISO/IEC 27005 (Information Security Risk Management), as well as the OWASP Threat Modeling Cheat Sheet. The goal is to anticipate and mitigate threats early in the system development lifecycle (SDLC), adhering to the principle that the cost of remediating a vulnerability decreases dramatically the earlier in development it is discovered, a concept quantified in IBM's Systems Sciences Institute research showing that fixing a defect in production can cost 100 times more than fixing it during design.

Microsoft's **STRIDE** framework was developed at Microsoft in 1999 by Loren Kohnfelder and Praerit Garg as a threat classification model that maps threat categories to violated security properties. Each letter in STRIDE corresponds to a specific threat type and the security principle it undermines. STRIDE is particularly effective for development teams conducting design reviews because it provides a systematic checklist that can be applied to each component in a data flow diagram.

- **Spoofing** involves an attacker impersonating another user or system, violating **authenticity**. Real-world example: CVE-2021-40438, an Apache HTTP Server vulnerability allowing server-side request forgery (SSRF) where the server could be made to forward requests to arbitrary backend servers, effectively spoofing the origin.
- **Tampering** refers to unauthorized modification of data or code, violating **integrity**. This includes memory corruption attacks, SQL injection, and man-in-the-middle attacks altering network traffic.
- **Repudiation** occurs when a system cannot prove that a user performed an action, undermining **non-repudiation**. Inadequate audit logging creates repudiation vulnerabilities, users can deny actions that lack an auditable trail.
- **Information Disclosure** breaches **confidentiality**, such as through insecure APIs exposing internal data, side-channel attacks (e.g., Spectre/Meltdown, CVE-2017-5753/5754), or improper error messages revealing system internals.
- **Denial of Service (DoS)** targets **availability**, rendering systems or services unusable. The 2016 Mirai botnet attack overwhelmed DNS provider Dyn with 1.2 Tbps of traffic, taking down major internet services including Twitter, Netflix, and Amazon.
- **Elevation of Privilege** violates **authorization**, allowing attackers to gain higher access rights. CVE-2021-34527 ("PrintNightmare") enabled remote code execution under SYSTEM privileges by exploiting the Windows Print Spooler service.

In contrast, **PASTA** (Process for Attack Simulation and Threat Analysis), developed by VerSprite in 2012, is a more holistic, risk-centric methodology that aligns technical threat analysis with business context and regulatory requirements. The seven-stage process begins with understanding business objectives (what are we protecting and why?), then moves through technical scoping (what systems are in scope?), data flow analysis (how does data move?), threat and adversary modeling (who attacks and how?), vulnerability detection (what weaknesses exist?), attack simulation (how would exploitation actually occur?), and concludes with risk impact analysis (what is the business cost?). PASTA ensures that threat models are not only technically sound but also strategically aligned with organizational risk tolerance and compliance frameworks such as NIST RMF or ISO 27001.

Both frameworks are complementary rather than competing. STRIDE is ideal for early-stage design reviews and developer training, providing a quick, systematic checklist. PASTA is better suited for enterprise-level risk assessments, security architecture reviews, and red-team simulations where business context and regulatory implications must be formally documented. Many mature organizations use STRIDE for component-level threat enumeration and PASTA for system-level risk governance.
:::

%%%

---
unit: Threats
code: ATK
title: The Adversary Landscape & MITRE ATT&CK
---

::::columns
::col::
:::table
| Threat Actor | Motivation | Capability / Resources | MITRE ATT&CK Mapping |
|---|---|---|---|
| **Script Kiddies** | Egos, reputation, curiosity. | Low; relies on automated pre-built scripts. | T1110 (Brute Force) |
| **Hacktivists** | Ideology, political, social. | Low to medium; defacement, DDoS. | T1499 (Endpoint DoS) |
| **Cybercriminals** | Financial gain, extortion. | High; professional malware, ransomware. | T1486 (Data Encrypted for Impact) |
| **Insiders (Malicious)** | Revenge, sabotage, profit. | High; has legitimate credentials and access. | T1078 (Valid Accounts) |
| **Nation-States / APTs** | Espionage, geopolitical power. | Extremely high; zero-day exploits, persistence. | T1071 (Application Layer Protocol) |
:::

::col::
:::callout style=line
**MITRE ATT&CK** is a globally-accessible knowledge base of adversary tactics, techniques, and procedures (TTPs) based on real-world observations. It enables defenders to understand attacker behavior, assess detection coverage, and improve incident response.
:::

:::text
The MITRE ATT&CK framework organizes adversarial behavior into **tactics** (the *why* of an attack) and **techniques** (the *how*). Tactics include Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, and Impact.
:::

:::list heading="Key ATT&CK Use Cases" style=plain
- Mapping red team exercises to known adversary behaviors
- Evaluating security tool coverage against real-world techniques
- Enriching threat intelligence with structured TTP data
- Supporting incident response with behavioral context
:::
::::

:::image src="images/01_mitre_attack_matrix.png" alt="MITRE ATT&CK Enterprise Matrix showing the 14 tactic columns and selected techniques beneath each, color-coded by threat actor type" caption="MITRE ATT&CK Enterprise Matrix: 14 tactic columns (from Reconnaissance through Impact) with hundreds of techniques and sub-techniques cataloged from real-world adversary behavior" width=full
:::

:::image src="images/01_mitre_attack_logo.png" alt="MITRE ATT&CK logo" caption="MITRE ATT&CK logo" width=half
:::

:::notes
Understanding the modern adversary landscape is foundational to cybersecurity defense. Threat actors today range from unskilled individuals to highly resourced nation-state groups, each with distinct motivations, operational methods, and levels of sophistication. This diversity necessitates a structured approach to threat modeling and defense planning that goes beyond simply patching known vulnerabilities.

MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) is a globally recognized framework that catalogs and standardizes the behaviors of cyber adversaries. First published by MITRE Corporation in 2013 based on analysis of APT threat groups targeting Windows enterprise environments, ATT&CK has since expanded to cover Linux, macOS, Mobile (Android/iOS), Cloud, Containers, and Industrial Control Systems (ICS). Unlike signature-based detection methods that rely on known indicators such as IP addresses or file hashes, ATT&CK focuses on *behavioral analysis*. This shift enables defenders to detect previously unknown threats by identifying malicious actions rather than static artifacts, a capability critical for countering sophisticated adversaries who routinely change their infrastructure and tooling.

Each entry in ATT&CK is structured around **tactics**, which represent the tactical goals of an adversary (e.g., Initial Access, Execution, Persistence), and **techniques**, which describe the specific methods used to achieve those goals. The Enterprise ATT&CK matrix currently contains 14 tactics and over 200 techniques with more than 400 sub-techniques, each backed by real-world incident data and often accompanied by mitigations, detection guidance, and known threat group associations. For example, T1078 (Valid Accounts) is used by actors ranging from cybercriminals (who purchase stolen credentials on dark web markets) to nation-state APTs (who obtain domain admin credentials through credential harvesting). The same technique demands different defensive responses depending on the actor and context, illustrating why ATT&CK's richness is essential for nuanced defense.

Techniques are further broken down into **procedures**, which are real-world examples of how a specific technique has been implemented by documented threat groups. For instance, APT29 (Cozy Bear, linked to Russian intelligence) used T1021.001 (Remote Desktop Protocol) for lateral movement during the 2020 SolarWinds campaign, while also employing T1553.002 (Code Signing) to bypass security controls by signing their SUNBURST backdoor with a legitimate SolarWinds certificate.

For defenders, ATT&CK enables several critical activities. Security operations centers (SOCs) map their detection rules to ATT&CK techniques to identify coverage gaps. Red teams use ATT&CK to plan adversary emulation exercises that simulate realistic threat scenarios. Threat intelligence teams use ATT&CK's threat group profiles to track adversary campaigns and anticipate future behavior. Security vendors map their product capabilities to ATT&CK techniques to enable comparative evaluation. This shared language and structured knowledge base transforms fragmented, siloed security intelligence into a collaborative, industry-wide defense ecosystem aligned with NIST SP 800-53 control families and ISO/IEC 27001 risk management requirements.
:::

%%%

---
unit: Vulnerabilities
code: VUL
title: Vulnerability Assessment & CVSS Metrics
---
:::text
In cybersecurity, a **vulnerability** is a weakness in a system, design, implementation, or operation that could be exploited to violate system security policies. Vulnerabilities are distinct from threats, which are potential causes of harm. Identifying and quantifying vulnerabilities is a core function of vulnerability management, and standardized frameworks like the **Common Vulnerabilities and Exposures (CVE)** program and the **Common Vulnerability Scoring System (CVSS)** are essential tools in this process.
:::

:::callout style=line
The **CVE Program**, maintained by MITRE Corporation, assigns unique identifiers to publicly disclosed cybersecurity vulnerabilities. Each CVE identifier provides a standardized reference point for discussing a specific vulnerability across organizations, tools, and databases.
:::

:::text
The **Common Vulnerability Scoring System (CVSS)**, developed by the Forum of Incident Response and Security Teams (FIRST), provides a standardized methodology for rating the severity of software vulnerabilities. CVSS enables security professionals to prioritize vulnerability remediation efforts based on objective, quantifiable metrics. The system is widely adopted and referenced in standards such as **NIST SP 800-53** and **ISO/IEC 27001**.
:::

:::code language=python caption="CVSS v3.1 Severity Classification Function"
def classify_cvss(score: float) -> str:
    """Determines the severity tier based on CVSS v3.1 scoring guidelines.

    CVSS v3.1 is the current standard maintained by FIRST.org.
    Severity thresholds are defined in the CVSS v3.1 Specification Document, Section 5.
    Scores range from 0.0 (no severity) to 10.0 (maximum severity).
    """
    # Input validation: reject any score outside the valid CVSS range [0.0, 10.0]
    if not (0.0 <= score <= 10.0):
        raise ValueError("CVSS score must be between 0.0 and 10.0")

    # Severity bands per CVSS v3.1 specification:
    if score == 0.0:
        return "None"       # No exploitability; no security impact
    elif score < 4.0:
        return "Low"        # Limited access; minimal impact on CIA
    elif score < 7.0:
        return "Medium"     # Partial unauthorized access; some impact possible
    elif score < 9.0:
        return "High"       # Significant unauthorized access; high CIA impact
    else:
        return "Critical"   # Complete system compromise; maximum CIA impact, patch immediately

# Real-world CVE examples for educational reference
vulnerabilities = [
    # CVE-2021-44228: Log4Shell in Apache Log4j 2
    # CVSS 10.0 CRITICAL, AV:N (network reachable) / AC:L (no special conditions)
    # PR:N (no auth required) / UI:N (no user interaction) / S:C (impacts other systems)
    # C:H I:H A:H, full compromise of confidentiality, integrity, and availability
    {"cve": "CVE-2021-44228", "name": "Log4Shell", "cvss": 10.0,
     "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"},

    # CVE-2017-0144: EternalBlue, SMBv1 vulnerability exploited by WannaCry ransomware
    # CVSS 8.1 HIGH, AC:H reduces score (requires specific SMB conditions)
    # Still network-exploitable with no authentication; devastating when combined with DoublePulsar
    {"cve": "CVE-2017-0144", "name": "EternalBlue", "cvss": 8.1,
     "vector": "CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H"},

    # CVE-2023-38606: iOS Kernel exploit used in Operation Triangulation
    # CVSS 5.5 MEDIUM, AV:L (local access required) / PR:L (low privileges needed)
    # Limited vector reduces score despite high integrity and availability impact
    {"cve": "CVE-2023-38606", "name": "iOS Kernel Bug", "cvss": 5.5,
     "vector": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H"}
]

# Iterate and display structured vulnerability assessment output
for vuln in vulnerabilities:
    severity = classify_cvss(vuln["cvss"])  # Translate numeric score to actionable severity tier
    # Formatted output suitable for patch management dashboards and vulnerability reports
    print(f"[{severity}] {vuln['cve']} ({vuln['name']}) - Score: {vuln['cvss']}")
    print(f"  Vector: {vuln['vector']}\n")  # Vector string encodes all CVSS base metrics
:::

:::table
| CVE              | Name            | CVSS Score | Severity  | Attack Vector | Privileges Required | User Interaction |
|------------------|-----------------|------------|-----------|---------------|---------------------|------------------|
| CVE-2021-44228   | Log4Shell       | 10.0       | Critical  | Network       | None                | None             |
| CVE-2017-0144    | EternalBlue     | 8.1        | High      | Network       | None                | None             |
| CVE-2023-38606   | iOS Kernel Bug  | 5.5        | Medium    | Local         | Low                 | None             |
:::

:::image src="images/01_cvss_scoring_breakdown.png" alt="CVSS v3.1 scoring diagram showing the three metric groups (Base, Temporal, Environmental) with their constituent sub-metrics and how they combine to produce a final score" caption="CVSS v3.1 metric hierarchy: Base metrics capture intrinsic vulnerability characteristics; Temporal metrics reflect how exploitability changes over time; Environmental metrics allow organization-specific customization" width=full
:::

:::image src="images/01_cvss_severity_scale.jpg" alt="CVSS severity scale: Low 0.0-3.9, Medium 4.0-6.9, High 7.0-8.9, Critical 9.0-10.0" caption="CVSS severity scale: Low 0.0-3.9, Medium 4.0-6.9, High 7.0-8.9, Critical 9.0-10.0" width=half
:::

:::image src="images/01_cvss_logo.png" alt="Common Vulnerability Scoring System logo" caption="Common Vulnerability Scoring System logo" width=half
:::

:::notes
A vulnerability is a recognized weakness in a system that can be exploited by a threat actor to gain unauthorized access or cause harm. The discipline of vulnerability management, systematically discovering, classifying, prioritizing, and remediating vulnerabilities, is a cornerstone of organizational security programs and is formally addressed in NIST SP 800-40 (Guide to Enterprise Patch Management Planning) and ISO/IEC 27001 Annex A Control 8.8 (Management of Technical Vulnerabilities).

The **Common Vulnerabilities and Exposures (CVE)** program, managed by MITRE Corporation and funded by the U.S. Cybersecurity and Infrastructure Security Agency (CISA), assigns unique identifiers to publicly disclosed vulnerabilities, enabling consistent communication and tracking across vendors, researchers, and security teams. As of 2024, the CVE database contains over 220,000 entries spanning three decades of vulnerability disclosures. CVE identifiers follow the format CVE-[Year]-[Number] (e.g., CVE-2021-44228), where the year indicates when the CVE was reserved or published. The National Vulnerability Database (NVD), maintained by NIST, enriches CVE data with CVSS scores, vulnerable product enumerations (CPE), and remediation guidance.

The **Common Vulnerability Scoring System (CVSS)**, currently at version 3.1 with version 4.0 released in 2023, provides a numerical score from 0.0 to 10.0 reflecting vulnerability severity based on exploitability and impact. The scoring system is structured around three metric groups:

- **Base Metrics** capture intrinsic characteristics constant across environments: Attack Vector (AV: Network, Adjacent, Local, Physical), Attack Complexity (AC: Low, High), Privileges Required (PR: None, Low, High), User Interaction (UI: None, Required), Scope (S: Unchanged, Changed), and impacts on Confidentiality (C), Integrity (I), and Availability (A), each rated None, Low, or High. These metrics combine through a formula specified in the CVSS SIG specification document to produce the Base Score.
- **Temporal Metrics** reflect how exploitability changes over time: Exploit Code Maturity (whether working exploit code exists), Remediation Level (whether patches are available), and Report Confidence (reliability of the vulnerability report).
- **Environmental Metrics** allow organizations to customize the base score for their specific environment, adjusting impact ratings based on the criticality of affected systems.

The Log4Shell vulnerability (CVE-2021-44228) achieved a CVSS 10.0 score because it is exploitable over the network (AV:N) with no prerequisites (AC:L, PR:N, UI:N), affects other systems beyond the vulnerable component (S:C), and fully compromises all three CIA properties (C:H, I:H, A:H). When disclosed in December 2021, Log4Shell affected millions of systems running Apache Log4j, from enterprise servers to IoT devices, requiring organizations to implement emergency patch procedures across their entire infrastructure. In contrast, CVE-2023-38606 (a zero-click iOS kernel vulnerability used in Operation Triangulation, a sophisticated APT campaign targeting journalists and researchers) scores only 5.5 due to its local access requirement (AV:L) and need for low privileges (PR:L), reflecting that despite its real-world impact in a targeted espionage campaign, it is harder to exploit at scale than network-reachable vulnerabilities.

Understanding CVSS scores and their constituent metrics is critical for prioritizing patch management in organizations that face thousands of open vulnerabilities at any time. Security teams typically use CVSS scores in combination with environmental context (is the vulnerable system internet-facing?) and threat intelligence (is there active exploitation in the wild?) to make informed, risk-based remediation decisions aligned with NIST SP 800-30 risk assessment methodology.
:::

%%%

---
unit: Risk
code: RSK
title: Risk Assessment Methodology (NIST SP 800-30)
---
:::flow
Identify Threat Sources and Events
Identify Vulnerabilities and Predisposing Conditions
Determine Likelihood of Exploitation
Determine Magnitude of Impact
Calculate and Prioritize Risk (ALE)
:::

::::columns ratio=1:1
::col::
::::card heading="Quantitative Risk Formula"
:::list style=tight
- **Single Loss Expectancy (SLE):** The cost of a single exploit event.
    *Formula: SLE = Asset Value (AV) × Exposure Factor (EF)*
- **Annualized Rate of Occurrence (ARO):** The estimated frequency of the event per year.
- **Annualized Loss Expectancy (ALE):** The total yearly cost of the risk.
    *Formula: ALE = SLE × ARO*
:::
::::
::col::
::::card heading="Risk Treatment Options"
:::list style=tight smartart=VerticalCurvedList
- **Mitigate:** Apply controls (e.g., install patches).
- **Transfer:** Shift risk (e.g., cyber insurance, outsourcing).
- **Avoid:** Eliminate risk cause (e.g., disable service).
- **Accept:** Absorb risk if remediation cost exceeds asset value.
:::
::::
::::

:::code language=mermaid caption="Threat, Vulnerability, and Risk Interconnection"
flowchart LR
  T["Threat<br/>who or what could cause harm"] -->|exploits| V["Vulnerability<br/>a weakness"]
  V -->|exposes| A["Asset<br/>what has value"]
  A --> R["Risk = likelihood x impact"]
  C["Controls"] -.->|reduce| V
:::

:::image src="images/01_ale_risk_calculation_diagram.png" alt="Quantitative risk calculation diagram showing AV times EF equals SLE, and SLE times ARO equals ALE, with example values for a data breach scenario" caption="Quantitative risk calculation: Asset Value (AV) × Exposure Factor (EF) = Single Loss Expectancy (SLE); SLE × Annualized Rate of Occurrence (ARO) = Annualized Loss Expectancy (ALE)" width=half
:::

:::image src="images/01_nist_risk_assessment_tiers.png" alt="NIST risk assessment at the organization, process and IT-system tiers, and its five steps" caption="NIST risk assessment at the organization, process and IT-system tiers, and its five steps" width=half
:::

:::notes
Risk assessment is a foundational process in cybersecurity risk management, and NIST Special Publication 800-30 Revision 1, titled *Guide for Conducting Risk Assessments*, provides the most widely adopted structured methodology for performing this critical task. First published in 2002 and revised in 2012, SP 800-30 is a cornerstone of the broader NIST Risk Management Framework (RMF) defined in SP 800-37, and it is legally required for U.S. federal agencies under FISMA. Its clear, repeatable five-step process has also been widely adopted by private-sector organizations seeking a rigorous, defensible approach to risk quantification.

The NIST SP 800-30 methodology follows a five-step process:

**Step 1: Identify Threat Sources and Events.** This involves cataloging potential adversaries (e.g., nation-state actors, insiders, hacktivists) and the specific events they might initiate (e.g., phishing campaigns, DDoS attacks, zero-day exploits). Threat source characterization includes assessing the actor's capability, intent, and access to target systems. For example, a financially motivated cybercriminal group with known ransomware capability targeting healthcare providers represents a specific, documentable threat source. This step often draws on threat intelligence feeds, CVE data, and frameworks like MITRE ATT&CK to enumerate plausible threat scenarios.

**Step 2: Identify Vulnerabilities and Predisposing Conditions.** Vulnerabilities are weaknesses in systems, processes, or controls that can be exploited by a threat source. Predisposing conditions include environmental or organizational factors, such as lack of security training, aging infrastructure, or absence of network segmentation, that increase the likelihood of successful exploitation. Vulnerability identification relies on automated scanning tools (Nessus, Qualys), penetration testing, and security architecture reviews, producing a prioritized list of weaknesses mapped against the threat landscape from Step 1.

**Step 3: Determine Likelihood of Exploitation.** This step estimates the probability that a specific threat source will successfully exploit a specific vulnerability within a defined timeframe. NIST SP 800-30 provides qualitative ratings (Very Low, Low, Moderate, High, Very High) that combine threat source characteristics (motivation, capability, access) with vulnerability exploitability (CVSS Access Vector and Complexity metrics). For instance, a public-facing web server with an unpatched CVE (CVSS 9.8, Critical, network-exploitable, no authentication required) facing an active, capable threat actor would receive a High likelihood rating.

**Step 4: Determine Magnitude of Impact.** Impact is assessed across the CIA triad dimensions and expressed in qualitative (Low, Moderate, High) or quantitative terms. NIST SP 800-60 provides detailed guidance on mapping information types to impact levels. Quantitative impact assessment yields the **Exposure Factor (EF)**, the percentage of asset value lost in a single incident, which feeds the risk calculation formulas. For example, a ransomware attack on a $1 million database server might have an EF of 0.4 (40% of asset value lost due to recovery costs, downtime, and data restoration).

**Step 5: Calculate and Prioritize Risk using ALE.** The **Single Loss Expectancy (SLE)** represents the expected monetary loss from a single incident: SLE = Asset Value × Exposure Factor. The **Annualized Rate of Occurrence (ARO)** estimates how many times the incident might occur per year. The **Annualized Loss Expectancy (ALE)** combines these: ALE = SLE × ARO. For example, if SLE = $400,000 and ARO = 0.5 (once every two years), then ALE = $200,000 per year, meaning investing up to $200,000 annually in controls to prevent this risk is economically justified.

Once risks are quantified, the four treatment options (Mitigate, Transfer, Avoid, Accept) can be evaluated against their cost-benefit profiles, ensuring that risk decisions are consistent, defensible, and aligned with organizational risk appetite and regulatory compliance requirements including FISMA, HIPAA, and ISO/IEC 27001.
:::

%%%

---
unit: Attack Surface
code: SRF
title: The Attack Surface & Attack Path
---
:::callout style=soft
The **attack surface** encompasses all potential entry points and vulnerabilities that an attacker can exploit to compromise a system or network. It includes network interfaces, software applications, physical access points, and human interactions. Effective cybersecurity requires continuous identification, assessment, and reduction of the attack surface through practices such as port minimization, privilege restriction, and patch management.
:::

::::columns
::col::
:::list heading="Key Components of the Attack Surface" style=plain
- Network-based vectors (e.g., open ports, exposed services)
- Software-based vectors (e.g., unpatched applications, APIs)
- Physical vectors (e.g., unprotected hardware, USB ports)
- Human vectors (e.g., phishing susceptibility, insider threats)
:::

::col::
:::table
| Vector Type     | Examples                          | Mitigation Strategy               |
|-----------------|-----------------------------------|------------------------------------|
| Network         | Open SSH, SMB, RDP ports          | Port filtering, network segmentation |
| Software        | Vulnerable web apps (e.g., CVEs)  | Patching, WAFs, input sanitization |
| Physical        | Unsecured server rooms            | Access controls, surveillance      |
| Human           | Social engineering, credential reuse | Security awareness training       |
:::
::::

:::flow caption="Adversary Attack Path Lifecycle (MITRE ATT&CK Alignment)"
graph TD
    A[Initial Access: Phishing Email] --> B[Execution: Malicious Macro]
    B --> C[Persistence: Registry Key Modification]
    C --> D[Privilege Escalation: LSASS Memory Dump]
    D --> E[Credential Access: Domain Admin Hash]
    E --> F[Lateral Movement: RDP to Database Server]
    F --> G[Exfiltration: Encrypted Stolen Data to Cloud]
:::

:::image src="images/01_attack_surface_vectors.png" alt="Diagram of the four attack surface vector types, network, software, physical, and human, arranged around a central organization icon with attack arrows from external and internal threats" caption="The four attack surface vector categories: every exposed port, unpatched application, unlocked door, and untrained employee represents a potential entry point that must be continuously inventoried and reduced" width=full
:::

:::image src="images/01_attack_surface_asset_types.png" alt="Asset types that make up an attack surface, from cloud environments to supply-chain assets" caption="Asset types that make up an attack surface, from cloud environments to supply-chain assets" width=full
:::

:::notes
The concept of the **attack surface** is foundational to risk assessment and threat modeling in cybersecurity. Defined by NIST SP 800-53 as the set of points on the boundary of a system where an attacker can attempt to enter, cause an effect, or extract data, the attack surface is dynamic, it expands with every new system, service, user, or API added to the environment. Modern cloud-first, hybrid-work organizations face dramatically expanded attack surfaces compared to traditional perimeter-defended networks, making continuous attack surface management (ASM) an essential security practice.

An **attack path**, in contrast, represents the sequence of steps an adversary takes to achieve their objective once they have identified vulnerable entry points. Each step in the path corresponds to a technique in the MITRE ATT&CK framework, and the path as a whole follows the adversarial kill chain from Initial Access through Impact. Understanding attack paths enables defenders to apply the **principle of attack chain disruption**, recognizing that breaking even one link in the chain can invalidate the entire attack strategy.

The illustrated attack path demonstrates a canonical enterprise compromise scenario mapped to MITRE ATT&CK:

- **Initial Access** (T1566, Phishing): The attacker sends a targeted phishing email containing a malicious document. When opened, it exploits a zero-click or user-triggered vulnerability to establish a foothold on the victim's endpoint.
- **Execution** (T1059, Command and Scripting Interpreter, T1221, Template Injection): A malicious macro or embedded script executes on the victim's machine, downloading additional payloads or establishing a reverse shell to the attacker's command-and-control (C2) server.
- **Persistence** (T1547.001, Registry Run Keys / Startup Folder): The malware modifies Windows registry run keys to ensure it restarts after system reboots, maintaining access regardless of normal user behavior or unintentional reboots.
- **Privilege Escalation** (T1003.001, LSASS Memory Dump): The attacker dumps credentials from the Local Security Authority Subsystem Service (LSASS) process using tools like Mimikatz, extracting NTLM hashes or Kerberos tickets for high-privileged accounts.
- **Credential Access** (T1003): A domain administrator credential hash is harvested, enabling the attacker to authenticate as a privileged user across the enterprise network without knowing the plaintext password (Pass-the-Hash technique, T1550.002).
- **Lateral Movement** (T1021.001, Remote Desktop Protocol): Using the stolen domain admin credential, the attacker connects via RDP to a database server, effectively "pivoting" through the network to reach higher-value targets.
- **Exfiltration** (T1567, Exfiltration Over Web Service): Sensitive data is compressed, encrypted, and transferred to an external cloud storage service (e.g., a legitimate service like Google Drive or Dropbox) to blend with normal traffic and evade network monitoring tools.

Defenders can apply multiple disruption strategies to this path. Disabling macros in Microsoft Office applications (T1221 mitigation) prevents Execution. Deploying Credential Guard (a Windows virtualization-based security feature) prevents LSASS memory dumping. Requiring privileged access workstations (PAWs) and network-level RDP restrictions limits Lateral Movement. Implementing DNS filtering and CASB (Cloud Access Security Broker) solutions can detect anomalous data exfiltration to cloud services. As NIST SP 800-207 (Zero Trust Architecture) emphasizes, treating every request as potentially untrusted, regardless of its network origin, provides continuous verification that individual attack path steps cannot succeed silently.
:::

%%%

---
unit: Mindset
code: MND
title: The Security Mindset & Control Categories
---
::::columns ratio=1:1
::col::
::::card heading="Core Security Principles"
:::list style=tight
- **Defense in Depth:** Multi-layered security controls so no single point of failure exists.
- **Least Privilege:** Users/systems receive the absolute minimum access required.
- **Zero Trust Architecture:** "Never trust, always verify" every request, regardless of origin.
- **Assume Breach:** Design systems under the premise that the network is already compromised.
:::
::::
::col::
::::card heading="Control Taxonomy (by Function)"
:::list style=tight
- **Administrative (Managerial):** Security policies, compliance audits, hiring procedures.
- **Technical (Logical):** Firewalls, intrusion detection, encryption, access controls.
- **Physical:** Perimeter fences, locks, badges, CCTV, biometric gates.
:::
:::list heading="Control Taxonomy (by Action)" style=tight
- **Preventive:** Block attacks (e.g., firewalls).
- **Detective:** Alert anomalies (e.g., SIEM).
- **Corrective:** Rebuild systems (e.g., backups).
- **Deterrent:** Discourage threats (e.g., warning banners).
- **Compensating:** Alternative controls when primary ones are not feasible.
:::
::::
::::
::::columns ratio=1:2
::col::
::::card heading="NIST Control Families (SP 800-53)"
:::list style=plain
- Access Control (AC)
- Audit and Accountability (AU)
- Configuration Management (CM)
- Identification and Authentication (IA)
- Incident Response (IR)
- Risk Assessment (RA)
- System and Communications Protection (SC)
:::
::::
::col::
::::card heading="ISO/IEC 27001 Control Categories"
:::table
| Category | Examples |
|----------|----------|
| A.5 - Information Security Policies | Policy approval, review cycles |
| A.6 - Organization of Information Security | Roles, segregation of duties |
| A.7 - Human Resource Security | Background checks, exit procedures |
| A.8 - Asset Management | Asset inventory, classification |
| A.9 - Access Control | User access rights, MFA |
| A.10 - Cryptography | Key management, TLS |
| A.11 - Physical and Environmental Security | Secure areas, equipment protection |
| A.12 - Operations Security | Malware protection, backup |
| A.13 - Communications Security | Network controls, secure transfer |
| A.14 - System Acquisition, Development, Maintenance | Secure engineering, supply chain |
| A.15 - Supplier Relationships | Supplier agreements, audits |
| A.16 - Information Security Incident Management | Reporting, response plan |
| A.17 - Business Continuity | BCM, redundancy |
| A.18 - Compliance | Legal, regulatory compliance |
:::
::::
::::

:::image src="images/01_defense_in_depth_layers.png" alt="Defense in depth diagram showing concentric security layers: physical, network, perimeter, endpoint, application, and data, with threat actors stopped at successive layers" caption="Defense in depth: layered security controls ensure that the failure of any single layer does not result in complete compromise, threats must defeat multiple independent controls to reach critical assets" width=full
:::

:::image src="images/01_security_control_types.gif" alt="Security control functional types: preventive, detective, corrective, physical, deterrent, compensating" caption="Security control functional types: preventive, detective, corrective, physical, deterrent, compensating" width=half
:::

:::notes
Adopting a security mindset is foundational to building resilient systems. This mindset is anchored in four core principles that shape how we approach threat modeling, system design, and incident response. These principles are not merely technical, they represent a philosophical orientation toward security that must permeate organizational culture from the C-suite to individual contributors.

**Defense in Depth** (also known as layered security) ensures that if one control fails, others will still provide protection. This principle, rooted in medieval castle architecture, moats, drawbridges, walls, inner keeps, applies equally to digital systems: networks are segmented, endpoints are hardened, applications are sandboxed, and data is encrypted. Each layer operates independently, so a firewall bypass does not automatically grant database access. This principle aligns with NIST SP 800-160 (Systems Security Engineering) and is essential in mitigating advanced persistent threats (APTs). The 2013 Target breach illustrates what happens when defense in depth fails: attackers gained initial access via a HVAC vendor's network connection, then pivoted through inadequately segmented point-of-sale networks to exfiltrate 40 million payment card records, a lateral movement path that robust segmentation could have blocked.

**Least Privilege** restricts user and system access to only the minimum permissions required to perform their legitimate functions. This principle is codified in NIST SP 800-53 control AC-6 and ISO/IEC 27001 Annex A.9 (Access Control). It directly reduces the blast radius of any compromise: if a low-privilege account is stolen, the attacker inherits only that account's limited permissions rather than administrative access. The 2017 Equifax breach demonstrated least privilege failure at scale, database service accounts had excessive read permissions across the entire cardholder database, enabling mass exfiltration once the application layer (CVE-2017-5638, Apache Struts) was exploited.

**Zero Trust Architecture**, formally defined in NIST SP 800-207, replaces the obsolete "castle-and-moat" security model with the principle "never trust, always verify." Every transaction, regardless of whether it originates inside or outside the traditional network perimeter, must be authenticated, authorized, and continuously validated. ZTA is particularly critical in cloud and hybrid environments where there is no longer a meaningful network perimeter. Microsoft's post-breach adoption of Zero Trust following the 2020 SolarWinds attack is a high-profile example of ZTA deployment in a mature enterprise environment.

**Assume Breach** is a proactive posture that accepts the premise that determined adversaries will eventually achieve some level of access, and focuses organizational investment on rapid detection and containment rather than solely on prevention. This philosophy is operationalized through red team exercises, purple team collaboration, threat hunting programs, and incident response rehearsals. It aligns with the NIST CSF's Detect and Respond functions and is the philosophical foundation of modern managed detection and response (MDR) services.

Security controls are organized along two axes. By **function**: Administrative controls (policies, training, hiring procedures), Technical controls (firewalls, encryption, SIEM), and Physical controls (biometrics, locks, CCTV). By **action**: Preventive controls block attacks before they occur; Detective controls identify attacks in progress; Corrective controls restore systems after an incident; Deterrent controls discourage adversaries through risk perception; Compensating controls provide alternative protection when primary controls cannot be implemented due to operational or technical constraints. This two-dimensional taxonomy enables security architects to ensure holistic coverage, identifying gaps where, for example, all controls are detective but none are preventive, creating an unacceptable residual risk profile.

NIST SP 800-53 organizes controls into 20 families (from AC through SR), providing over 1,000 individual control statements that collectively cover the full scope of information system security. ISO/IEC 27001:2022 provides 93 controls organized into four themes (Organizational, People, Physical, Technological), offering a complementary international standard. Mature organizations map their control implementations against both frameworks to demonstrate compliance across multiple regulatory and contractual requirements simultaneously.
:::

%%%

---
unit: Roles
code: ROL
title: Cybersecurity Roles & Professional Careers
---
:::table
| Role / Function | Operational Focus | Key Framework / Tool |
|---|---|---|
| **SOC Analyst (L1-L3)** | Continuous monitoring, alert triage, incident detection. | SIEM (Splunk, Elastic), SOAR |
| **Penetration Tester** | Offensive testing, vulnerability exploitation, finding weak spots. | Kali Linux, Metasploit, OWASP Top 10 |
| **Security Engineer** | Security architecture design, firewall rules, IAM systems. | NIST SP 800-53, Terraform, Cloud IAM |
| **Incident Responder** | Immediate containment, forensics, root-cause analysis. | NIST SP 800-61 (Incident Handling) |
| **GRC / Compliance Analyst** | Aligning security with legal regulations and standards. | ISO 27001, SOC 2, HIPAA, GDPR |
| **CISO (Executive)** | Risk management, budget allocation, security strategy. | NIST CSF, ISO 31000 |
| **Threat Intelligence Analyst** | Adversary tracking, IOC analysis, threat hunting. | STIX/TAXII, MITRE ATT&CK |
:::

:::image src="images/cyber_careers.jpg" alt="Cybersecurity Roles & Career Paths" caption="Cybersecurity Roles & Career Paths" width=half
:::

:::image src="images/01_red_blue_purple_team_model.png" alt="Red team, Blue team, and Purple team model diagram showing offensive (red), defensive (blue), and collaborative (purple) roles in a circular adversarial-defensive feedback loop" caption="Red, Blue, and Purple team model: Red teams simulate adversaries using offensive techniques; Blue teams defend and detect; Purple teams facilitate knowledge transfer between red and blue to continuously improve defenses" width=half
:::

:::notes
Everything we have discussed today maps onto distinct professional roles within the cybersecurity career ecosystem. Cybersecurity is not a monolithic profession but a highly specialized field with roles categorized broadly into offensive (Red Team), defensive (Blue Team), and governance/management tracks, with collaborative Purple Team functions bridging offensive and defensive operations. Understanding these roles helps students identify career pathways and appreciate how each specialization contributes to an organization's overall security posture.

**SOC (Security Operations Center) Analysts** form the frontline defensive operation. Operating in three tiers (L1: alert triage and escalation; L2: incident investigation and correlation; L3: advanced threat hunting and forensics), SOC analysts monitor network logs, endpoint telemetry, and cloud audit trails in real time using Security Information and Event Management (SIEM) platforms such as Splunk, Microsoft Sentinel, or IBM QRadar. They use Security Orchestration, Automation, and Response (SOAR) tools to automate repetitive tasks like IOC enrichment, ticket creation, and initial containment actions. SOC analysts typically hold certifications such as CompTIA Security+, EC-Council's Certified Incident Handler (ECIH), or GIAC Security Operations Certified (GSOC).

**Penetration Testers** (ethical hackers) probe systems for exploitable weaknesses, mimicking real adversaries to help organizations identify and remediate flaws before malicious actors discover them. They follow structured methodologies such as the OWASP Testing Guide (for web applications), NIST SP 800-115 (Technical Guide to Security Testing), and the PTES (Penetration Testing Execution Standard). Tools include Kali Linux (a specialized penetration testing Linux distribution), Metasploit Framework, Burp Suite, and Nmap. Industry certifications include OSCP (Offensive Security Certified Professional), CEH (Certified Ethical Hacker), and GPEN (GIAC Penetration Tester).

**Security Engineers** design and build the security infrastructure that protects an organization's systems and data. They configure firewall rule sets, implement Identity and Access Management (IAM) systems using frameworks like RBAC and PAM, design network segmentation architectures, and automate security controls through Infrastructure as Code (IaC) tools like Terraform and Ansible. Cloud Security Engineers specialize in securing AWS, Azure, and GCP environments using cloud-native security services. Key frameworks include NIST SP 800-53 and the CIS Controls.

**Incident Responders** engage when a security event occurs, functioning as the organization's emergency response team. Following the NIST SP 800-61 (Computer Security Incident Handling Guide) lifecycle of Preparation, Detection and Analysis, Containment, Eradication, Recovery, and Post-Incident Activity, they triage alerts, contain threats, conduct forensic investigations, and coordinate communications. Incident responders use tools like FTK, Volatility (memory forensics), and Wireshark (network forensics). The GIAC Certified Incident Handler (GCIH) and SANS FOR508 certifications are standard in this role.

**GRC (Governance, Risk, and Compliance) Analysts** ensure that the organization's security program aligns with applicable laws, regulations, and standards. They conduct risk assessments, manage audit programs, maintain policy libraries, and interface with legal, finance, and executive leadership to translate technical risks into business language. Key frameworks include ISO/IEC 27001, NIST CSF, SOC 2, HIPAA, PCI DSS, and GDPR. The CISM (Certified Information Security Manager) and CRISC (Certified in Risk and Information Systems Control) certifications are foundational.

**CISOs (Chief Information Security Officers)** own the organization's entire security strategy, aligning all security investments and programs with business objectives and risk tolerance. They report to the Board of Directors and C-suite, manage multi-million dollar budgets, and make final risk acceptance decisions. Effective CISOs combine deep technical literacy with executive communication, financial acumen, and regulatory expertise, a challenging combination that commands top-tier compensation in both public and private sectors.

**Threat Intelligence Analysts** study adversary groups themselves, tracking indicators of compromise (IOCs), analyzing malware campaigns, and mapping observed TTPs to MITRE ATT&CK to anticipate future attacks. They consume and produce threat intelligence in structured formats (STIX 2.1, TAXII 2.1) and share findings through ISACs (Information Sharing and Analysis Centers) relevant to their industry sector.

Regardless of your ultimate specialization, understanding how these roles cooperate, through shared platforms, common frameworks, and cross-functional processes, is essential for building and contributing to a unified, resilient security program.
:::

%%%

---
unit: Goals
code: PKH
title: The Parkerian Hexad, Extending the CIA Triad
---
::::columns ratio=1:1
::col::
:::callout style=soft
The **Parkerian Hexad**, introduced by security consultant Donn B. Parker in 1998, extends the CIA triad by adding three additional properties that address security dimensions not fully captured by Confidentiality, Integrity, and Availability alone.
:::
:::table
| Property | Definition | Example Violation |
|---|---|---|
| **Confidentiality** | Information accessible only to authorized entities. | Data breach exposing customer PII. |
| **Integrity** | Data is accurate and unaltered. | SQL injection modifying financial records. |
| **Availability** | Systems are accessible when needed. | DDoS attack blocking online banking. |
| **Possession / Control** | Authorized party physically controls the data. | Encrypted laptop stolen, data not decrypted yet but possession is lost. |
| **Authenticity** | Origin and identity of data can be verified. | Forged digital certificate used in MITM attack. |
| **Utility** | Data is in a usable format for its intended purpose. | Encryption key is lost, data is intact but inaccessible (utility violation, not availability). |
:::
::col::
:::list heading="Why Extend Beyond CIA?" style=plain
- **Possession** addresses situations where data remains encrypted (no confidentiality breach) but physical control is lost, a meaningful security event.
- **Authenticity** is critical in environments where data provenance matters, such as legal evidence, financial transactions, and software supply chains.
- **Utility** captures scenarios where data becomes useless without being technically unavailable, e.g., a backup stored in an obsolete format that can no longer be read.
:::
:::callout style=line
**ISO/IEC 27001:2022** now includes authenticity as an explicit security property alongside CIA, reflecting industry-wide recognition that the triad alone is insufficient for modern threat environments.
:::
::::

:::code language=mermaid caption="The Parkerian Hexad: six information security properties that together provide a more complete security assurance model than the classic CIA Triad alone"
mindmap
  root((Parkerian Hexad))
    Confidentiality
      Medical records read by an outsider
    Integrity
      Payroll figures altered
    Availability
      Website down under DDoS
    Possession
      Backup tape stolen, still encrypted
    Authenticity
      Email forged in the CEO's name
    Utility
      Data encrypted and the key lost
:::

:::notes
The CIA triad is the most widely taught and referenced model in cybersecurity education, and for good reason, it is simple, memorable, and covers the core security concerns for the vast majority of practical scenarios. However, as security practice matured through the 1990s and 2000s, practitioners began encountering situations that the triad could not adequately describe. Donn B. Parker, a security researcher at SRI International, formalized these gaps in his 1998 book "Fighting Computer Crime," introducing the Parkerian Hexad as a more complete model with six properties.

Understanding the three extended properties requires careful distinction from the original triad:

**Possession** (also called Control) addresses the physical or logical custody of data independently of its content. Consider the classic scenario of an encrypted laptop stolen from a consultant's bag at an airport. If the encryption is strong and the key is not known to the thief, confidentiality has not been breached, the data remains unreadable. However, the organization has lost possession of that data. This matters practically: the laptop might be sold to a nation-state actor with sufficient cryptographic resources, or a vulnerability in the encryption software might be discovered later. From a regulatory and risk perspective, the loss of possession is itself a security event worthy of documentation, notification (many data protection regulations require reporting lost devices even if they are encrypted), and remediation. Possession also extends to logical data: if a disgruntled employee copies confidential data to personal cloud storage before being terminated, possession is violated even if confidentiality is technically maintained through access controls on the original system.

**Authenticity** ensures that data, messages, or system identities are genuine and verifiable. While integrity confirms that data has not been modified, authenticity confirms that it came from who it claims to come from. This distinction matters in scenarios such as digital signatures on legal documents (where the question is not just "was the document altered?" but "did this specific person actually sign it?"), email communication (DKIM and SPF verify that email originated from the claimed domain), and software distribution (code signing certificates verify publisher identity). The 2011 DigiNotar CA compromise illustrates an authenticity failure: attackers forged SSL certificates for Google, Mozilla, and other major domains, allowing them to conduct man-in-the-middle attacks on Iranian internet users, the data was not modified (no integrity violation), but its authenticity was fraudulently established. MITRE ATT&CK technique T1553.002 (Code Signing) specifically addresses adversaries who abuse code signing certificates to bypass authenticity controls.

**Utility** addresses the usability of data for its intended purpose. This is perhaps the most subtle of the six properties. Consider a scenario where an organization stores critical backups encrypted with a key managed by a third-party key management service (KMS). If the KMS provider goes out of business and the keys are lost, the backup data is physically present, its integrity is intact, and it is technically "available" in the sense that no denial-of-service attack has occurred, yet the data is completely useless because it cannot be decrypted. This is a utility violation. Similarly, data stored in a proprietary format from discontinued software suffers a utility failure when the software cannot run on modern operating systems. Organizations must maintain not only the data itself but also the tools, keys, and formats necessary to make that data useful. NIST SP 800-57 Part 1 (Key Management) addresses cryptographic key lifecycle management as a critical operational security function that directly impacts data utility.

Utility is not a subset of availability. Availability describes whether systems and data can be accessed at all; utility describes whether the data can serve its intended function. A database that is available but corrupted or unusably formatted is an availability success and a utility failure. The hexad names this distinction, which matters when designing recovery plans, backup validation procedures and key escrow strategies.

For modern practitioners, the Parkerian Hexad provides more expressive vocabulary for describing security requirements in contracts, risk assessments, and incident reports. However, it has not displaced the CIA triad as the primary educational framework because its three additional properties, while real, arise less frequently in day-to-day security operations. The recommended approach is to default to CIA for standard risk communication and invoke the Hexad's extensions when specific scenarios demand the additional precision.
:::

%%%

---
unit: Cryptography
code: CRY
title: Symmetric vs. Asymmetric Cryptography
---
::::columns ratio=1:1
::col::
::::card heading="Symmetric Cryptography"
:::list style=tight
- **Single shared key** for both encryption and decryption.
- **Algorithm examples:** AES-128/256 (FIPS 197), ChaCha20, 3DES (deprecated).
- **Speed:** Very fast; suitable for bulk data encryption.
- **Key challenge:** Secure key distribution, how do two parties share a secret key without a secure channel?
- **Use cases:** Disk encryption (BitLocker, dm-crypt), TLS record layer, database encryption.
:::
::::
::col::
::::card heading="Asymmetric Cryptography"
:::list style=tight
- **Key pair:** Public key (shared freely) + Private key (secret).
- **Algorithm examples:** RSA-2048/4096, ECDSA (P-256, P-384), Ed25519.
- **Speed:** Much slower than symmetric; used for small data or key exchange only.
- **Key advantage:** Solves the key distribution problem, anyone can encrypt with a public key; only the private key holder can decrypt.
- **Use cases:** TLS handshake, digital signatures (code signing, S/MIME), SSH authentication.
:::
::::
::::

:::callout style=soft
**Hybrid encryption**, used in TLS, PGP, and Signal, combines both: asymmetric cryptography securely exchanges a symmetric session key, then symmetric cryptography encrypts the actual data at speed.
:::

:::table
| Property | Symmetric (AES-256) | Asymmetric (RSA-4096) |
|---|---|---|
| Key size | 256 bits | 4096 bits |
| Relative speed | ~10 Gbps (hardware) | ~1000x slower |
| Key distribution | Manual / pre-shared | Public key freely shareable |
| Typical key lifetime | Session / short-term | Months to years (with revocation) |
| NIST standard | FIPS 197 | SP 800-56A / FIPS 186-5 |
:::

:::code language=mermaid caption="Symmetric vs. asymmetric cryptography: symmetric is fast but requires secure key exchange; asymmetric solves key exchange but is slow; TLS uses both in a hybrid model"
flowchart TB
  subgraph S["Symmetric: one shared key"]
    direction LR
    A1[Sender] -->|"encrypt with key K"| C1[Ciphertext] -->|"decrypt with same key K"| B1[Receiver]
  end
  subgraph AS["Asymmetric: key pair"]
    direction LR
    A2[Sender] -->|"encrypt with receiver's public key"| C2[Ciphertext] -->|"decrypt with receiver's private key"| B2[Receiver]
  end
  subgraph H["Hybrid: TLS handshake"]
    direction LR
    H1["Asymmetric key exchange<br/>(ECDHE, certificate)"] --> H2[Shared session key] --> H3["Bulk data encrypted<br/>symmetrically (AES-GCM)"]
  end
  S ~~~ AS ~~~ H
:::

:::notes
Cryptography is the mathematical foundation of information security. At its core, encryption transforms readable plaintext into unreadable ciphertext using a mathematical algorithm and a key, and decryption reverses the process using the same or a related key. The choice between symmetric and asymmetric cryptography represents one of the most fundamental design decisions in any secure system, and understanding the trade-offs is essential for every security practitioner.

**Symmetric cryptography** uses a single key for both encryption and decryption. The algorithm most widely deployed today is the **Advanced Encryption Standard (AES)**, standardized by NIST in FIPS 197 following a public competition in 2001 that selected the Rijndael algorithm. AES operates on 128-bit blocks with key sizes of 128, 192, or 256 bits. AES-256 is the current gold standard for protecting sensitive data at rest and in transit, providing a security margin of 256-bit key space that is computationally infeasible to brute-force even with quantum computing (Grover's algorithm reduces symmetric key security by half, making AES-256 effectively equivalent to 128 bits of post-quantum security, still considered sufficient per NIST's post-quantum recommendations). AES hardware acceleration (AES-NI instructions) is built into virtually all modern CPUs, enabling throughput of 10+ Gbps with negligible CPU overhead, making it practical for encrypting large data volumes such as full-disk encryption (BitLocker on Windows, dm-crypt on Linux) or database tablespace encryption.

The fundamental challenge of symmetric cryptography is **key distribution**: both parties must possess the same secret key before they can communicate securely. In a small, closed environment (e.g., two parties who can meet in person), this is manageable. But in open systems like the internet, where millions of parties need to establish secure channels with strangers, pre-sharing keys is impractical. This "key distribution problem" motivated the development of asymmetric cryptography.

**Asymmetric (public-key) cryptography**, pioneered by Diffie, Hellman, Rivest, Shamir, and Adleman in the 1970s, uses mathematically related key pairs. The **public key** can be shared with anyone; the **private key** is kept secret by its owner. Data encrypted with the public key can only be decrypted with the corresponding private key, solving the key distribution problem entirely, since public keys require no secure channel to distribute. The most widely deployed asymmetric algorithm is **RSA** (Rivest-Shamir-Adleman), whose security rests on the computational difficulty of factoring large composite integers. NIST SP 800-131A specifies that RSA key sizes below 2048 bits are no longer acceptable, and 3072 or 4096 bits are recommended for systems requiring long-term security. **Elliptic Curve Cryptography (ECC)** provides equivalent security to RSA with dramatically smaller key sizes, ECDSA with a P-256 curve (256-bit key) provides roughly the same security as RSA-3072, enabling faster operations and smaller certificates. Ed25519, used in modern SSH and TLS implementations, offers excellent performance and resistance to certain implementation attacks that plague RSA.

The critical limitation of asymmetric cryptography is speed: RSA operations are typically 1000x slower than AES operations due to their mathematical complexity. This makes asymmetric cryptography unsuitable for encrypting bulk data. The solution, universally applied in protocols like TLS, PGP, and Signal, is **hybrid encryption**: asymmetric cryptography is used only to securely exchange a randomly generated symmetric session key, then all actual data is encrypted with that session key using AES. This combines the key distribution advantages of asymmetric cryptography with the performance of symmetric cryptography.

Sharing a public key does not weaken a system. The public key is designed to encrypt and verify, not to decrypt or sign, so publishing it is intentional and safe. Security rests entirely on the secrecy of the private key and on the computational difficulty of deriving it from the public key.
:::

%%%

---
unit: Controls
code: ACM
title: Access Control Models, MAC, DAC, RBAC, ABAC
---
::::columns ratio=1:1
::col::
::::card heading="Mandatory Access Control (MAC)"
:::list style=tight
- **Enforcer:** The operating system or security kernel, not the resource owner.
- **Basis:** Security labels (classification levels) assigned to subjects (users) and objects (files).
- **Example:** SELinux, government classified systems (DoD MLS).
- **NIST:** AC-3(3), Mandatory Access Control.
:::
::::
::::card heading="Discretionary Access Control (DAC)"
:::list style=tight
- **Enforcer:** The resource owner sets permissions for their own objects.
- **Basis:** Owner-defined ACLs (e.g., Windows NTFS permissions, Linux chmod).
- **Weakness:** Susceptible to Trojan horse attacks, malicious programs inherit owner's permissions.
- **NIST:** AC-3, Access Enforcement.
:::
::::
::col::
::::card heading="Role-Based Access Control (RBAC)"
:::list style=tight
- **Enforcer:** Administrators define roles; users are assigned to roles.
- **Basis:** Job function determines access (e.g., HR role, Finance role, Admin role).
- **Standard:** ANSI/INCITS 359-2004 RBAC Standard.
- **Advantage:** Simplifies permission management at enterprise scale.
:::
::::
::::card heading="Attribute-Based Access Control (ABAC)"
:::list style=tight
- **Enforcer:** Policy engine evaluates multiple attributes dynamically.
- **Basis:** Subject attributes (department, clearance), object attributes (classification), environment (time, location, device).
- **Standard:** NIST SP 800-162.
- **Advantage:** Fine-grained, context-aware decisions, the foundation of Zero Trust.
:::
::::
::::

:::callout style=line
**Modern IAM** typically combines RBAC for coarse-grained role assignment with ABAC policies for fine-grained contextual enforcement, a model sometimes called **ReBAC** (Relationship-Based Access Control) or **PBAC** (Policy-Based Access Control).
:::

:::code language=mermaid caption="Access control model comparison: MAC enforces mandatory labels; DAC gives owners control; RBAC maps roles to permissions; ABAC uses dynamic attribute policies for fine-grained Zero Trust decisions"
flowchart TB
  subgraph MAC["MAC: Mandatory"]
    M1["Who controls: central authority"]
    M2["Basis: labels and clearances"]
    M3["Example: SELinux, military systems"]
  end
  subgraph DAC["DAC: Discretionary"]
    D1["Who controls: resource owner"]
    D2["Basis: owner's choice"]
    D3["Example: file permissions, shared folders"]
  end
  subgraph RBAC["RBAC: Role-Based"]
    R1["Who controls: administrators"]
    R2["Basis: job role"]
    R3["Example: Active Directory groups"]
  end
  subgraph ABAC["ABAC: Attribute-Based"]
    A1["Who controls: policy engine"]
    A2["Basis: user, resource, context attributes"]
    A3["Example: cloud IAM conditions"]
  end
  MAC ~~~ DAC
  RBAC ~~~ ABAC
:::

:::notes
Access control is the set of mechanisms that determine who or what can view, use, or modify a resource. It is one of the most foundational security controls in any system and is formally addressed in NIST SP 800-53 control family AC (Access Control), ISO/IEC 27001 Annex A.9, and the Common Criteria Protection Profiles for operating systems and databases. The choice of access control model significantly shapes an organization's security posture, administrative overhead, and ability to enforce least privilege at scale.

**Mandatory Access Control (MAC)** is the most restrictive model, where access decisions are made by the operating system or security kernel based on security labels, not by the resource owner. Every subject (user or process) and object (file, process, network port) is assigned a label that encodes its security classification (e.g., Unclassified, Confidential, Secret, Top Secret) and security categories (compartments). The security policy mandates that subjects can only access objects at or below their clearance level, a rule known as the Bell-LaPadula model's "no read up, no write down" principle. MAC is primarily used in government and military environments where strict information flow enforcement is legally required. Linux implementations include SELinux (Security-Enhanced Linux), developed by the NSA and integrated into the mainline Linux kernel in 2003, and AppArmor, used in Ubuntu and SUSE. The key advantage of MAC is that even a resource owner cannot grant access beyond what the security policy allows, eliminating the insider threat risk present in DAC.

**Discretionary Access Control (DAC)** is the model most familiar to desktop users. The resource owner controls permissions on their own objects through access control lists (ACLs). Linux file system permissions (read/write/execute for owner/group/others, managed via chmod and chown) and Windows NTFS permissions are classic DAC implementations. DAC is flexible and easy to use but has a critical security weakness: it is vulnerable to **Trojan horse attacks**. If a malicious program runs with the same identity as a legitimate user, it inherits that user's access rights and can read or modify any file the user owns. For this reason, pure DAC is rarely sufficient in high-security environments.

**Role-Based Access Control (RBAC)**, standardized in ANSI/INCITS 359-2004, assigns permissions to roles rather than to individual users. Users are then assigned to roles based on their job functions. This indirection simplifies administration enormously at enterprise scale: changing the permissions of a "Finance Analyst" role automatically affects all users in that role, rather than requiring individual permission updates for each user. RBAC is the dominant model in enterprise identity management systems (Active Directory, Okta, Azure AD) and cloud platforms (AWS IAM roles, GCP IAM). The NIST RBAC model defines four components: core RBAC (users, roles, permissions, sessions), hierarchical RBAC (role inheritance for organizational hierarchy), constrained RBAC (separation of duty, a user cannot hold conflicting roles), and symmetric constrained RBAC. Separation of duty prevents fraud by ensuring that no single individual can complete a sensitive transaction alone, for example, a user who creates a payment cannot also approve it.

**Attribute-Based Access Control (ABAC)**, defined in NIST SP 800-162, makes access decisions based on the evaluation of policies against the attributes of subjects, objects, and the environment at the time of the access request. This enables highly granular, context-sensitive decisions: "Allow access to the patient record only if the requesting user is a licensed physician (subject attribute), the record is in the same hospital as the physician (object attribute), and the request is made during business hours from a hospital-issued device (environment attributes)." ABAC is computationally more expensive than RBAC because policies are evaluated dynamically, but it provides the fine-grained control necessary for Zero Trust Architecture, where every access request must be evaluated against its full context rather than simply checking role membership. ABAC is increasingly deployed in cloud environments (AWS IAM condition keys, OPA/Rego policy engines) and is the theoretical foundation of modern identity governance platforms.

The access control models differ in who controls access. In MAC, the system decides from labels, regardless of the owner's preference. In RBAC, administrators decide by assigning roles. In DAC, the owner decides. This hierarchy of control is the clearest way to tell the three apart.
:::

%%%

---
unit: Threats
code: MAL
title: Malware Taxonomy & Classification
---
:::callout style=soft
**Malware** (malicious software) is any program or code designed to harm, exploit, or otherwise compromise a computer system without the informed consent of the user. Malware is the primary weapon of cybercriminals, nation-state actors, and hacktivists, and its taxonomy reflects decades of adversarial evolution.
:::

:::table
| Malware Type | Primary Behavior | Persistence Method | Notable Example |
|---|---|---|---|
| **Virus** | Attaches to legitimate programs; spreads on execution. | Infects executable files. | CIH/Chernobyl (1998), overwrote BIOS firmware. |
| **Worm** | Self-replicates across networks without user action. | Exploits network vulnerabilities. | Morris Worm (1988), WannaCry (2017). |
| **Trojan Horse** | Disguises as legitimate software; enables backdoor. | Persists via legitimate installation. | Zeus banking trojan (credential theft). |
| **Ransomware** | Encrypts victim files; demands ransom payment. | Scheduled tasks, registry run keys. | LockBit, Conti, REvil (CVE-2017-0144). |
| **Rootkit** | Hides attacker presence by modifying OS internals. | Kernel modules, bootloader infection. | Sony BMG DRM rootkit (2005). |
| **Spyware** | Silently collects user data and transmits to attacker. | Browser extensions, registry persistence. | FinFisher, Pegasus (NSO Group). |
| **Botnet / Bot** | Joins a network of compromised machines (C2-controlled). | Cron jobs, scheduled tasks, WMI. | Mirai botnet (IoT DDoS, 2016). |
| **Keylogger** | Records keystrokes to harvest credentials. | Kernel drivers, hook injection. | DarkComet RAT keylogger. |
| **Fileless Malware** | Operates entirely in memory; no disk artifacts. | WMI subscriptions, PowerShell. | Kovter, PowerSploit-based attacks. |
:::

:::list heading="MITRE ATT&CK Malware Techniques" style=plain
- **T1059**, Command and Scripting Interpreter (PowerShell, cmd.exe): used by most modern malware for execution.
- **T1547**, Boot or Logon Autostart Execution: persistence via registry, scheduled tasks, startup folders.
- **T1055**, Process Injection: injecting malicious code into legitimate processes to evade detection.
- **T1486**, Data Encrypted for Impact: ransomware encryption of victim files.
:::

:::code language=mermaid caption="Malware taxonomy: the eight primary categories of malicious software, their propagation mechanisms, persistence methods, and representative real-world specimens"
mindmap
  root((Malware))
    Virus
      Attaches to host files
      ILOVEYOU
    Worm
      Self-propagates over networks
      WannaCry
    Trojan
      Disguised as legitimate software
      Emotet
    Ransomware
      Encrypts data for payment
      Ryuk
    Spyware
      Covert data collection
      Pegasus
    Rootkit
      Hides deep in the OS or firmware
      LoJax
    Botnet
      Remotely controlled fleets
      Mirai
    Fileless
      Lives in memory and scripts
      PowerShell loaders
:::

:::notes
Malware represents the operational toolset of the vast majority of cyberattacks. Understanding malware taxonomy is essential not just for defensive purposes, recognizing behavioral indicators, but also for effective incident response, where rapid classification of discovered malware determines the appropriate containment and eradication strategy. NIST SP 800-83 (Guide to Malware Incident Prevention and Handling) and CISA's Malware Analysis Reports (MARs) provide authoritative references for malware classification and response guidance.

**Viruses** are the oldest category of malware, dating to the early 1980s. Unlike worms, viruses require a host program and human action (running the infected program) to spread. The defining characteristic is self-replication by attaching code to legitimate executables, documents (macro viruses in Microsoft Office), or boot sectors. The CIH virus (also called Chernobyl), discovered in 1998, was particularly destructive because it overwrote the victim system's BIOS firmware, rendering machines unbootable, a level of destruction rarely achieved by more modern malware. Modern antivirus (AV) engines use signature-based detection (hash matching of known malware), heuristic analysis (behavioral patterns), and machine learning models to detect both known and novel viruses, though signature evasion through polymorphism and metamorphism remains a persistent challenge.

**Worms** are self-propagating malware that spread across networks by exploiting vulnerabilities, without requiring user interaction. The Morris Worm of 1988, the first recognized computer worm, exploited Unix sendmail, fingerd, and rsh/rexec vulnerabilities to spread across ARPANET, infecting approximately 6,000 machines (roughly 10% of the internet at the time). The author, Robert Morris, was the first person convicted under the Computer Fraud and Abuse Act. Modern worms such as WannaCry (2017) exploit unpatched network vulnerabilities (CVE-2017-0144, EternalBlue in SMBv1) to spread autonomously at machine speed across enterprise networks, making them capable of infecting hundreds of thousands of systems within hours. Network segmentation, host-based firewalls, and rapid patch deployment are the primary countermeasures.

**Ransomware** has become the dominant financially-motivated malware category of the past decade. Modern ransomware operations are organized as **Ransomware-as-a-Service (RaaS)** businesses, where developers create and maintain the malware and leak sites while "affiliates" conduct the actual intrusions and receive 70-80% of ransom payments. The attack lifecycle typically follows a pattern called "double extortion": first, data is exfiltrated; second, files are encrypted. If the victim refuses to pay, the attacker threatens to publish stolen data on leak sites. Major RaaS groups include LockBit (responsible for thousands of incidents globally), ALPHV/BlackCat (using Rust-based ransomware for cross-platform attacks), and the now-defunct Conti (notorious for attacking healthcare organizations including the Irish Health Service Executive in 2021, causing weeks of operational disruption). CISA, FBI, and NCSC provide joint advisories on ransomware prevention, including the 3-2-1 backup rule (three copies, two different media, one offsite) as the primary recovery strategy.

**Rootkits** operate at the deepest levels of a system, kernel space, hypervisor level, or firmware, to hide attacker presence from standard detection tools. By hooking system calls or modifying kernel data structures, rootkits can make malicious processes, files, and network connections invisible to the operating system's own reporting mechanisms. The Sony BMG DRM rootkit scandal of 2005 demonstrated that rootkit technology could be deployed commercially (and illegally) by major corporations, Sony's XCP copy protection software installed a kernel rootkit on Windows systems when music CDs were inserted, exposing millions of systems to exploitation by third-party malware.

**Fileless malware** represents the most sophisticated evasion category, operating entirely within legitimate system processes and memory without writing files to disk. By abusing Windows Management Instrumentation (WMI), PowerShell, Microsoft Office macros, and the Windows registry, fileless malware evades file-based detection (AV signatures, file integrity monitoring). Detection requires memory forensics, behavioral monitoring (Endpoint Detection and Response tools like CrowdStrike Falcon or SentinelOne), and SIEM correlation of PowerShell transcript logs and WMI activity.

Malware types map onto the CIA triad. Ransomware attacks availability, and confidentiality as well when data is exfiltrated before encryption. Spyware attacks confidentiality. Worms can affect all three properties.
:::

%%%

---
unit: Threats
code: SOC
title: Social Engineering & Human-Factor Attacks
---
:::callout style=line
**Social engineering** exploits human psychology rather than technical vulnerabilities. It is frequently the initial vector in sophisticated attacks because it is often easier to manipulate a person into providing access than to break through properly configured technical controls. MITRE ATT&CK Tactic TA0001 (Initial Access) includes multiple social engineering techniques.
:::

::::columns ratio=1:1
::col::
:::list heading="Primary Social Engineering Attack Types" style=plain
- **Phishing (T1566.001):** Mass-distributed fraudulent emails mimicking legitimate entities to steal credentials or deliver malware. Example: IRS-themed phishing during tax season.
- **Spear Phishing (T1566.001):** Highly targeted phishing using personal information about the victim to increase credibility. Used by APT28 in election interference campaigns.
- **Vishing:** Voice phishing, phone calls impersonating bank fraud departments, IT helpdesks, or government agencies.
- **Smishing:** SMS-based phishing; increasingly common with mobile banking adoption.
- **Pretexting:** Creating a fabricated scenario (pretext) to extract information. Example: impersonating an auditor requesting system access credentials.
- **Baiting:** Leaving infected USB drives in parking lots; curiosity causes victims to plug them in (tested by organizations as red team exercises).
- **Tailgating / Piggybacking:** Physically following an authorized employee through a secured door.
- **Business Email Compromise (BEC):** Impersonating executives to authorize fraudulent wire transfers; caused $50B+ in losses per FBI IC3 2023 report.
:::
::col::
:::table
| Psychological Principle | How Attackers Exploit It |
|---|---|
| **Authority** | Impersonating executives, law enforcement, IT administrators. |
| **Urgency** | "Your account will be suspended in 24 hours!" |
| **Scarcity** | "Only 3 slots remaining, sign up now." |
| **Social Proof** | "All your colleagues have already updated their passwords." |
| **Reciprocity** | Offering small favors before requesting sensitive information. |
| **Liking / Trust** | Impersonating known contacts, spoofing email addresses. |
:::
:::callout style=soft
The 2020 Twitter hack, in which attackers social engineered Twitter IT employees via phone calls to obtain internal admin tool access, then hijacked accounts of Barack Obama, Elon Musk, and others to run a Bitcoin scam, illustrates that even the most technically sophisticated companies can be defeated by human-factor attacks.
:::
::::

:::code language=mermaid caption="Social engineering attack taxonomy: all variants exploit cognitive biases and psychological principles rather than technical vulnerabilities, making human awareness training the primary countermeasure"
mindmap
  root((Human Vector))
    Phishing
      Urgency, authority
    Vishing
      Trust in a live voice
    Pretexting
      A believable story
    Baiting
      Curiosity, greed
    Tailgating
      Politeness
    BEC
      Authority, routine payments
:::

:::notes
Social engineering is often described as "hacking the human operating system." While technical vulnerabilities require specific conditions (an unpatched system, an exposed service, a misconfigured firewall), social engineering targets universal human psychological tendencies that exist in every organization regardless of technical security maturity. This is why security awareness training is mandated by virtually every major security framework, including ISO/IEC 27001 Annex A Control 6.3, NIST SP 800-53 AT (Awareness and Training) control family, PCI DSS Requirement 12.6, and HIPAA Security Rule §164.308(a)(5).

The psychological principles exploited by social engineers were systematically documented by psychologist Robert Cialdini in his 1984 book "Influence: The Psychology of Persuasion." The six principles, Reciprocity, Commitment, Social Proof, Authority, Liking, and Scarcity, form the theoretical foundation of most social engineering attack scripts. Modern security awareness training programs, such as those provided by KnowBe4, Proofpoint Security Awareness Training, and Cofense, use simulated phishing campaigns that deliberately invoke these principles to test and train employees.

**Phishing** remains the most commonly used initial access vector across all threat actor categories. According to the Verizon Data Breach Investigations Report (DBIR), phishing is involved in over 35% of data breaches annually. A typical phishing email contains urgency ("Your account has been suspended"), impersonation (forged sender address using lookalike domains or display name spoofing), and a call to action (link to a credential-harvesting page or malicious attachment). Email authentication standards including SPF (Sender Policy Framework), DKIM (DomainKeys Identified Mail), and DMARC (Domain-based Message Authentication, Reporting, and Conformance) are technical controls that reduce spoofing, but they are only effective when implemented correctly by both sending and receiving organizations, a deployment gap that attackers continue to exploit.

**Spear phishing** elevates the attack by incorporating specific personal details about the target: their name, role, recent activities, colleagues' names, and business context gathered from LinkedIn, corporate websites, and social media. APT28 (Fancy Bear, linked to Russian military intelligence GRU) conducted spear phishing campaigns against Democratic National Committee staff in 2016, using personalized emails that appeared to be security alerts from Google, directing victims to attacker-controlled credential harvesting pages. The 2020 SolarWinds attack chain began with a spear phishing email against a SolarWinds reseller, demonstrating how initial human compromise can cascade into catastrophic supply chain attacks.

**Business Email Compromise (BEC)** deserves special attention because it causes the greatest financial losses of any cybercrime category, surpassing ransomware, phishing, and all other categories combined. The FBI's Internet Crime Complaint Center (IC3) 2023 report documented over $2.9 billion in BEC losses in the United States alone in 2022. Unlike other phishing attacks that deliver malware, BEC relies entirely on deception: attackers compromise or impersonate an executive's email account and send fraudulent payment authorization instructions to the finance department. No malware is involved, making BEC invisible to most technical security controls. Countermeasures include out-of-band verification procedures (phone callbacks to verify wire transfer requests), mandatory dual-approval for transactions above thresholds, and DMARC enforcement to prevent executive email address spoofing.

The defense against social engineering is primarily behavioral, not technical. Security awareness training programs should be frequent (quarterly at minimum), personalized (role-specific scenarios for finance, HR, IT), simulated (phishing simulations measure actual click rates), and reinforcing (immediate training for employees who fail simulations). Organizations should also implement technical controls that reduce the impact of successful social engineering: phishing-resistant MFA (hardware security keys like YubiKey are immune to credential phishing because they use cryptographic challenge-response rather than passwords), email filtering, and privileged access management that limits what a compromised account can do.

The 2011 RSA SecurID breach began with a spear-phishing email sent to a small group of RSA employees under the subject "2011 Recruitment Plan". The attached Excel file exploited a zero-day in Adobe Flash to install a backdoor. That single human compromise led to the theft of SecurID seed data, which was later used against defense contractors including Lockheed Martin. One opened email produced losses of hundreds of millions of dollars and weakened the security of millions of customers.
:::

%%%

---
unit: Response
code: IRL
title: Incident Response Lifecycle, NIST SP 800-61
---
:::callout style=soft
**Incident response (IR)** is the organized approach to addressing and managing the aftermath of a security breach or cyberattack. A well-defined IR process minimizes damage, reduces recovery time and costs, and informs improvements to prevent recurrence. **NIST SP 800-61 Rev. 2** (Computer Security Incident Handling Guide) defines the standard four-phase IR lifecycle used by organizations worldwide.
:::

:::steps
Phase 1, Preparation: Establish IR team, policies, playbooks, tools, and training before incidents occur.
Phase 2, Detection & Analysis: Identify and confirm incidents through log analysis, SIEM alerts, and threat hunting; assess severity and scope.
Phase 3, Containment, Eradication & Recovery: Isolate affected systems; remove malware and attacker persistence; restore from clean backups; harden controls.
Phase 4, Post-Incident Activity: Conduct lessons-learned review; update detection rules, playbooks, and controls; report to stakeholders and regulators.
:::

::::columns ratio=1:1
::col::
:::list heading="Detection Sources & Indicators of Compromise (IoCs)" style=plain
- SIEM alerts (Splunk, Microsoft Sentinel, IBM QRadar)
- Endpoint Detection & Response (EDR) telemetry
- Network anomaly detection (NetFlow, IDS/IPS)
- User reports and helpdesk tickets
- Threat intelligence feeds (STIX/TAXII, ISACs)
- External notifications (CISA, FBI, vendor disclosures)
:::
::col::
:::list heading="Containment Strategies by Incident Type" style=plain
- **Ransomware:** Immediately isolate affected hosts; disconnect from network; preserve forensic images; contact FBI (do not pay without guidance).
- **Phishing / Credential Compromise:** Reset compromised passwords; revoke active sessions and tokens; enable MFA; review audit logs for lateral movement.
- **Data Breach:** Identify exfiltration scope; notify legal/privacy team; assess regulatory notification obligations (GDPR 72-hour rule, HIPAA 60-day rule).
- **DDoS:** Activate upstream scrubbing; engage CDN/DDoS mitigation provider; rate-limit or null-route attack traffic.
:::
::::

:::code language=mermaid caption="NIST SP 800-61 Incident Response Lifecycle: four phases form a continuous improvement cycle, each incident's lessons-learned output feeds back into improved preparation for the next"
flowchart LR
  P[Preparation] --> D[Detection and Analysis]
  D --> C["Containment, Eradication<br/>and Recovery"]
  C --> D
  C --> PI[Post-Incident Activity]
  PI -->|lessons learned| P
:::

:::notes
Incident response is the structured practice of preparing for, detecting, containing, and recovering from cybersecurity incidents. Without a defined incident response capability, organizations facing a breach often improvise under pressure, making decisions that inadvertently destroy forensic evidence, extend the breach duration, or violate legal obligations. NIST Special Publication 800-61 Revision 2, "Computer Security Incident Handling Guide," published in 2012, is the foundational reference document for IR programs and is required for U.S. federal agencies under FISMA. Its four-phase lifecycle model is also widely adopted in private-sector organizations, forming the basis of IR programs aligned with ISO/IEC 27035 (Information Security Incident Management) and SANS Institute's PICERL model (Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned).

**Phase 1: Preparation** is the most impactful phase, investments made here determine how effectively every subsequent phase can be executed. Preparation includes establishing and training an incident response team (IRT) with clearly defined roles (IR Manager, Forensic Analyst, Communications Lead, Legal Liaison), creating playbooks for common incident types (ransomware, phishing, insider threat, DDoS), deploying and tuning detection tools (SIEM, EDR, NDR), establishing out-of-band communication channels (incident-specific email addresses, encrypted messaging apps for IR team coordination), and maintaining legal and regulatory contacts. Organizations should conduct tabletop exercises at least annually, simulated incident scenarios discussed without technical execution, and full red team/blue team exercises to test actual response capabilities. A Cyber Incident Response Retainer with a specialist firm (Mandiant, CrowdStrike, Secureworks) provides pre-negotiated access to expert IR resources when an incident exceeds internal capabilities.

**Phase 2: Detection and Analysis** begins when a potential incident is flagged. The majority of detections originate from SIEM alerts correlating log data from network devices, endpoints, identity providers, and cloud services. The initial analysis must determine whether the alert represents a true positive security incident or a false positive. This requires analysts to investigate supporting evidence: timeline reconstruction from logs, process execution histories from EDR telemetry, network connection records from firewall and proxy logs, and authentication events from identity providers (Active Directory, Azure AD). Severity classification is critical for escalation decisions, a CVSS-style severity framework (Critical, High, Medium, Low) allows consistent prioritization across incidents. Key metrics tracked in this phase include Mean Time to Detect (MTTD) and Mean Time to Respond (MTTR), which are leading indicators of SOC effectiveness. Industry benchmarks from IBM's Cost of a Data Breach Report show that organizations with mature IR programs (low MTTD/MTTR) save an average of $1.49 million per breach compared to organizations without such capabilities.

**Phase 3: Containment, Eradication, and Recovery** is the active response phase. Containment strategies are incident-type specific: ransomware requires immediate network isolation of affected hosts to prevent further encryption spread, while a compromised cloud identity may require token revocation and MFA enforcement without system isolation. All containment actions should preserve forensic evidence, capturing memory dumps, disk images, and log archives before remediation. Eradication removes the attacker's foothold: deleting malware, removing persistence mechanisms (registry keys, scheduled tasks, rogue user accounts), and patching the exploited vulnerability. Recovery restores normal operations from known-good backups, validates system integrity, and gradually reconnects isolated systems under enhanced monitoring to detect attacker re-entry attempts. The 3-2-1-1-0 backup rule, three copies, two different media, one offsite, one air-gapped, zero untested backups, is the gold standard for ransomware recovery preparedness.

**Phase 4: Post-Incident Activity** transforms the painful experience of an incident into organizational improvement. The lessons-learned review, conducted within two weeks of incident closure, answers key questions: What happened? When? How was it detected? What went well? What should be improved? The output, updated playbooks, new detection rules, remediated vulnerabilities, improved training, feeds directly back into Phase 1, completing the improvement cycle. Regulatory notification obligations must also be addressed in this phase: GDPR requires notification to the supervisory authority within 72 hours of discovery; HIPAA requires notification to affected individuals within 60 days; SEC rules (adopted in 2023) require material cybersecurity incident disclosure to investors within four business days.
:::

%%%

---
unit: Case Studies
code: CS1
title: Case Study, WannaCry Ransomware (CVE-2017-0144)
---
:::callout style=line
**WannaCry** (May 2017) was a global ransomware cyberattack that infected over 200,000 systems across 150 countries in under 24 hours, causing estimated damages between $4 billion and $8 billion. It exploited **CVE-2017-0144** (EternalBlue), a critical SMBv1 vulnerability in Windows that was developed by the NSA and leaked by the Shadow Brokers hacking group in April 2017.
:::

::::columns ratio=1:1
::col::
:::list heading="Attack Timeline" style=plain
- **April 14, 2017:** Shadow Brokers leak NSA exploit toolkit including EternalBlue (CVE-2017-0144) and DoublePulsar backdoor implant.
- **March 14, 2017:** Microsoft releases MS17-010 patch for supported Windows versions (but not XP/2003).
- **May 12, 2017:** WannaCry ransomware campaign begins; spreads globally within hours.
- **May 12, 2017 (afternoon):** Security researcher Marcus Hutchins discovers and activates a kill switch domain, slowing propagation.
- **June 2017:** U.S., UK, and Australia officially attribute WannaCry to North Korea's Lazarus Group.
:::
::col::
:::list heading="Technical Analysis" style=plain
- **Vulnerability:** CVE-2017-0144, Windows SMBv1 buffer overflow allowing remote code execution as SYSTEM (CVSS 8.1).
- **Propagation:** Worm component scanned TCP port 445; infected all reachable unpatched Windows systems autonomously.
- **Payload:** AES-128 encrypted victim files with .WCRY extension; demanded $300-600 in Bitcoin.
- **Kill switch:** WannaCry checked if a specific unregistered domain resolved, if it did, execution halted. Hutchins registered it for $10.69.
- **Impact on NHS:** 80 UK NHS trusts affected; surgeries cancelled; patient records inaccessible for days.
:::
::::

:::table
| Impact Dimension | Details |
|---|---|
| Systems Infected | 200,000+ across 150 countries |
| Financial Damage | $4B–$8B estimated global damages |
| Sectors Hit | Healthcare (NHS), Telecom (Telefónica), Logistics (FedEx/TNT), Manufacturing (Renault, Nissan) |
| Root Cause | Unpatched SMBv1 on legacy Windows XP/7 systems; no network segmentation |
| Attributtion | North Korea's Lazarus Group (U.S. DoJ indictment, 2018) |
| Key Lessons | Patch management discipline; legacy OS elimination; network segmentation; offline backups |
:::

:::code language=mermaid caption="WannaCry attack chain: EternalBlue exploits SMBv1 (CVE-2017-0144) for remote code execution; DoublePulsar installs a kernel-level backdoor; WannaCry ransomware encrypts victim files and demands Bitcoin payment"
flowchart LR
  A["Scan for exposed<br/>SMBv1 (TCP 445)"] --> B["EternalBlue exploit<br/>(MS17-010)"]
  B --> C["DoublePulsar<br/>kernel backdoor"]
  C --> D["WannaCry payload<br/>runs"]
  D --> E["Files encrypted"]
  E --> F["Bitcoin ransom<br/>demand"]
  D -->|worm spreads to next host| A
:::

:::notes
WannaCry is arguably the most significant ransomware event in cybersecurity history, not because of its technical sophistication, it was relatively straightforward by APT standards, but because of the scale and speed of its impact, the critical infrastructure it disrupted, and the systemic lessons it exposed about enterprise patch management and legacy system risk. Examining WannaCry in detail provides a comprehensive case study that touches on vulnerability management (CVE-2017-0144, CVSS scoring), threat actors (Lazarus Group, nation-state attribution), incident response (NHS response), and risk governance (failure of patch management programs).

The story of WannaCry begins with an NSA cyberweapon. EternalBlue was developed by the NSA's Tailored Access Operations (TAO) group as an exploit for a critical buffer overflow vulnerability in Microsoft's implementation of the SMBv1 (Server Message Block version 1) protocol. SMBv1, introduced in 1992, was already two decades old and had been superseded by SMBv2 and SMBv3, but remained enabled by default on Windows XP, Windows 7, Windows Server 2003, and Windows Server 2008 systems that millions of organizations continued to run due to legacy application dependencies and upgrade costs. Microsoft had already patched the vulnerability in MS17-010 (released March 14, 2017, almost two months before WannaCry), but the patch had not been applied to an enormous number of systems, particularly in organizations running unmanaged or out-of-support Windows XP (for which Microsoft had ended extended support in 2014).

The attack chain was elegant in its brutality. WannaCry's worm component scanned the internet for systems with TCP port 445 (SMB) open. Upon finding a reachable target, it deployed EternalBlue to exploit the SMBv1 vulnerability, achieving SYSTEM-level code execution without any user interaction, no phishing email, no malicious attachment, no social engineering. Once on the system, it dropped DoublePulsar, an NSA-developed kernel-level backdoor implant that also leaked by Shadow Brokers, to establish persistent access. WannaCry's ransomware component then began AES-128 encrypting user files, appending the .WCRY extension, and displaying a ransom demand of $300-600 in Bitcoin with a countdown timer. The worm then simultaneously began scanning for additional victims both on the local network and randomly across the internet, enabling exponential propagation.

The NHS impact deserves particular attention as a case study in healthcare security governance. Approximately 80 NHS trusts in England and Scotland were affected, with an estimated 19,000 appointments cancelled, including surgeries. Some hospitals reverted to paper-based operations. The critical issue was not merely the unpatched vulnerability but the hospital environment itself: NHS trusts ran large fleets of Windows XP workstations connected to medical devices (MRI scanners, CT scanners, infusion pumps) that could not be updated or replaced because device manufacturers had not certified their products on newer operating systems. This created a dilemma that persists across healthcare and industrial environments globally: patch management is necessary for security but potentially disruptive to device availability and patient safety. The solution, isolated network segments for legacy medical devices, with no external connectivity, was technically available but not widely deployed before WannaCry.

Marcus Hutchins' kill switch discovery was a pivotal moment. While analyzing WannaCry samples, Hutchins noticed the malware queried a specific nonsensical domain (iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com) and halted execution if the domain resolved. This was likely intended as a sandbox detection mechanism (malware sandboxes often resolve all domains to detect evasion checks). By registering the domain for $10.69 and pointing it to a sinkhole, Hutchins caused all active WannaCry instances globally to halt propagation, an accidental kill switch that is credited with saving tens of thousands of additional infections. However, it did not help systems already encrypted.

From a NIST SP 800-30 risk assessment perspective, WannaCry represented a failure across multiple risk treatment dimensions: the vulnerability was known and patched (mitigate option was available but not taken); network segmentation would have prevented lateral movement (an additional mitigate measure); offline backups would have enabled recovery without paying ransom (a recovery control absent in many affected organizations). The Annualized Loss Expectancy for an organization with unpatched SMBv1 exposed to the internet, assessed against a ransomware threat actor with known RCE exploit tooling, would have been catastrophically high, yet many organizations had not performed or acted on such an assessment.
:::

%%%

---
unit: Case Studies
code: CS2
title: Case Study, SolarWinds Supply Chain Attack (2020)
---
:::callout style=soft
The **SolarWinds attack** (discovered December 2020) was a sophisticated supply chain compromise attributed to Russian intelligence (SVR, APT29 / Cozy Bear). Attackers compromised SolarWinds' build pipeline to insert a backdoor (SUNBURST) into the Orion IT monitoring platform, which was then digitally signed and distributed to approximately 18,000 customers, including U.S. federal agencies, Fortune 500 companies, and critical infrastructure operators.
:::

::::columns ratio=1:1
::col::
:::steps
Attackers compromise SolarWinds build environment (mid-2019)
SUNBURST backdoor inserted into Orion software build process
Tampered Orion update (2019.4.5200.9083) signed with legitimate SolarWinds certificate
18,000 organizations install the poisoned update via normal software update process
SUNBURST lies dormant for 12-14 days; checks for security tools before activating
Backdoor establishes C2 over HTTPS using legitimate Orion API traffic patterns
Attacker deploys TEARDROP/RAINDROP second-stage payloads to high-value targets
FireEye discovers its own tools stolen; reports to Microsoft and CISA (December 8, 2020)
:::
::col::
:::list heading="Why This Attack Was Unprecedented" style=plain
- **Trust exploitation:** The malware was delivered through a legitimate, digitally signed update from a trusted vendor, standard security checks (hash verification, signature validation) provided no protection.
- **Patient adversary:** The SUNBURST backdoor was dormant for 12-14 days and used legitimate Orion traffic patterns to blend in with normal monitoring tool communications, making network-based detection extremely difficult.
- **Blast radius:** Orion was used to monitor critical networks; SUNBURST gave attackers visibility into the very security monitoring infrastructure of their victims.
- **Supply chain vector:** Demonstrated that defending one's own perimeter is insufficient, the integrity of every software vendor in the supply chain must be verified.
:::
::::

:::table
| Attribute | Details |
|---|---|
| CVE Reference | CVE-2020-10148 (SolarWinds Orion API authentication bypass) |
| Threat Actor | APT29 / Cozy Bear (Russian SVR) |
| Duration (undetected) | ~9 months (March–December 2020) |
| Victims | 18,000 organizations received poisoned update; ~100 organizations deeply compromised |
| U.S. Government Impact | DHS, Treasury, Commerce, State Department, parts of NSC compromised |
| Detection | FireEye red team tools stolen; FireEye initiated investigation leading to disclosure |
| Key MITRE ATT&CK TTPs | T1553.002 (Code Signing), T1195.002 (Compromise Software Supply Chain), T1071.001 (Web Protocols for C2) |
:::

:::code language=mermaid caption="SolarWinds supply chain attack: by compromising the build pipeline of a trusted IT monitoring vendor, attackers delivered a signed backdoor to 18,000 organizations, bypassing all perimeter defenses and vendor trust controls"
flowchart LR
  A["Attackers breach<br/>SolarWinds build system"] --> B["SUNBURST inserted<br/>into Orion code"]
  B --> C["Update signed with<br/>SolarWinds certificate"]
  C --> D["Distributed to about<br/>18,000 organizations"]
  D --> E["Dormant backdoor<br/>checks in"]
  E --> F["Second stage only on<br/>high-value targets"]
:::

:::notes
The SolarWinds attack fundamentally changed how the cybersecurity community thinks about software supply chain risk. Before SolarWinds, supply chain attacks were theoretical concerns discussed in academic research and occasional APT reports. After SolarWinds, every organization that relied on third-party software, which is every organization in the modern world, was forced to confront the reality that their trust in a vendor's digitally signed software was insufficient protection against a sophisticated adversary who had compromised that vendor's own build process.

The attack began with the compromise of SolarWinds' internal development environment, likely via a combination of credential theft and vulnerability exploitation, sometime in mid-2019. The attackers, identified with high confidence as APT29 (Cozy Bear), the cyber operations unit of Russia's Foreign Intelligence Service (SVR), spent months studying SolarWinds' software build pipeline, understanding the code structure, and identifying how to insert a backdoor without triggering code review processes or automated testing. This level of patience and operational security is characteristic of nation-state APT groups, which prioritize long-term access over quick gains.

The SUNBURST backdoor was inserted into a source code file of the SolarWinds Orion platform (solarwinds.orion.core.businesslayer.dll) in a way designed to look like legitimate code. When SolarWinds compiled and packaged the Orion update, SUNBURST was compiled into the binary, then cryptographically signed with SolarWinds' legitimate code signing certificate. The signing process, which is explicitly designed to verify that software comes from a trusted publisher and has not been modified, provided no protection because the modification occurred before signing, within the trusted build environment. This is a fundamental limitation of code signing: it verifies the publisher's identity and post-signing integrity, but cannot detect malicious code inserted by the publisher (or an attacker controlling the publisher's systems) before signing.

SUNBURST's operational security was extraordinary. Upon installation, the backdoor lay dormant for 12-14 days, performing no suspicious activity, a deliberate measure to evade sandbox analysis (most automated malware sandboxes run samples for only a few minutes) and to ensure the installation completed and the security team's attention had moved on before activation. When it activated, SUNBURST communicated with its C2 infrastructure using HTTP requests that were specifically crafted to mimic legitimate Orion platform API calls, hiding its traffic within the noise of the monitoring tool's own normal operation. The C2 domain (avsvmcloud.com) was hosted on legitimate cloud infrastructure and used a domain generation algorithm that required victim-specific data to resolve, making detection via blocklist extremely difficult.

The consequences for U.S. federal government security were severe. The Cybersecurity and Infrastructure Security Agency (CISA), which is responsible for defending federal civilian networks, was itself a victim. The Treasury Department and the Commerce Department's National Telecommunications and Information Administration (NTIA) were compromised. The scope of data accessed at these agencies, emails, documents, internal communications, remains partially classified. The incident led directly to Executive Order 14028 (May 2021, "Improving the Nation's Cybersecurity"), which mandated Zero Trust adoption across federal agencies, software supply chain security standards (including SBOM, Software Bill of Materials requirements), and enhanced logging and incident response capabilities.

From a defensive perspective, SolarWinds demonstrated the necessity of several controls that were absent or insufficient: (1) **Build pipeline integrity monitoring**, monitoring the build environment itself for unauthorized changes to source code or build scripts; (2) **Software Bill of Materials (SBOM)**, maintaining a complete inventory of software components and their origins to enable rapid impact assessment when compromised components are discovered; (3) **Behavioral detection**, SUNBURST was ultimately detectable through anomalous DNS patterns and unusual network connections from Orion processes, but required sophisticated behavioral analytics that most organizations lacked; (4) **Zero Trust segmentation**, organizations with strict network segmentation and microsegmentation would have limited SUNBURST's lateral movement even after the backdoor activated; (5) **Third-party risk management**, conducting security assessments of critical software vendors, including review of their build pipeline security and code signing practices, aligned with NIST SP 800-161 (Cybersecurity Supply Chain Risk Management Practices).
:::

%%%

---
unit: Mindset
code: ZTA
title: Zero Trust Architecture, Deep Dive (NIST SP 800-207)
---
:::callout style=soft
**Zero Trust Architecture (ZTA)** is a security paradigm that eliminates the concept of implicit trust based on network location. Every access request, regardless of whether it originates inside or outside the traditional network perimeter, must be explicitly authenticated, authorized, and continuously validated before granting access to resources. ZTA is formally defined in **NIST SP 800-207** (August 2020).
:::

::::columns ratio=1:1
::col::
:::list heading="Seven Core Tenets of Zero Trust (NIST SP 800-207)" style=plain
- **1.** All data sources and computing services are considered resources.
- **2.** All communication is secured regardless of network location.
- **3.** Access to individual resources is granted on a per-session basis.
- **4.** Access is determined by dynamic policy (identity, device health, behavioral analytics).
- **5.** All owned and associated devices are monitored for security posture.
- **6.** All resource authentication and authorization is dynamic and strictly enforced before access is allowed.
- **7.** The enterprise collects as much information as possible about the current state of assets, network traffic, and communications to improve security posture.
:::
::col::
:::list heading="ZTA vs. Traditional Perimeter Security" style=plain
- **Traditional model ("castle and moat"):** Trust is granted based on network location, devices inside the firewall are trusted; devices outside are not. Once inside, lateral movement is largely unrestricted.
- **ZTA model ("never trust, always verify"):** Network location is irrelevant. Every user, device, and application must prove their identity and authorization for each resource access, every time.
- **Why the old model fails:** Remote work, cloud services, BYOD, and supply chain attacks (SolarWinds) mean the perimeter no longer meaningfully separates trusted from untrusted entities.
:::
:::callout style=line
**Microsoft** adopted ZTA after the 2020 SolarWinds attack. **Google** pioneered BeyondCorp, their ZTA implementation, in 2014, allowing all employees to work from untrusted networks with the same access experience as the corporate network.
:::
::::

:::flow
Verify identity explicitly (MFA, certificate-based auth, passwordless)
Validate device health (patch status, EDR agent, OS version, disk encryption)
Evaluate request context (location, time, behavior analytics, risk score)
Apply least-privilege access (RBAC + ABAC policy, just-in-time access)
Monitor session continuously (behavioral analytics, anomaly detection)
Re-verify on context change (location change, privilege escalation request)
:::

:::code language=mermaid caption="NIST SP 800-207 Zero Trust Architecture: the Policy Engine evaluates all access requests against identity, device, and context signals; the Policy Enforcement Point grants or denies access to resources based on dynamic, least-privilege authorization"
flowchart LR
  subgraph Subjects
    U[User]
    DV[Device]
  end
  subgraph CP["Control plane"]
    PE["Policy Engine<br/>(decides)"] --- PA["Policy Administrator<br/>(issues session)"]
  end
  Subjects -->|access request| PEP["Policy Enforcement Point"]
  PEP <--> PA
  SIG["Signals: identity, device health,<br/>threat intelligence, logs"] --> PE
  PEP -->|allowed session only| R["Enterprise resource"]
:::

:::notes
Zero Trust Architecture represents the most significant paradigm shift in network security since the introduction of the firewall. The traditional perimeter security model, variously called "castle and moat," "network perimeter defense," or "hard shell, soft center", assumed that threats came primarily from outside the corporate network and that devices and users inside the network could be trusted implicitly. This assumption held reasonably well in the era of centralized computing, fixed workstations, and on-premise data centers with well-defined network boundaries. It became progressively less valid with each of the following trends: remote work and VPN proliferation, cloud service adoption (where data and applications live outside the traditional perimeter), personal device (BYOD) policies, and supply chain attacks that compromise trusted internal systems. The SolarWinds attack made the final, unanswerable case: if an internal monitoring tool running with elevated network privileges can be backdoored through a legitimate update process, then no device inside the network can be implicitly trusted.

NIST Special Publication 800-207, "Zero Trust Architecture," published in August 2020, provides the authoritative U.S. government definition and implementation guidance for ZTA. The document defines three core architectural components: the **Policy Engine (PE)**, which makes access decisions by evaluating all available signals against policy; the **Policy Administrator (PA)**, which communicates the PE's decisions by establishing or terminating sessions; and the **Policy Enforcement Point (PEP)**, which acts as the actual gatekeeper, allowing or blocking access to enterprise resources based on PA instructions.

The seven tenets of NIST ZTA reflect a fundamental shift in how trust is conceptualized:

Tenets 1-2 establish that the network itself is untrusted: all communication must be secured (TLS 1.3 minimum), and every device and service must be considered a resource that requires authentication regardless of its network location. This means internal API calls between microservices, internal database connections, and administrator console access all require the same cryptographic authentication as external user access.

Tenets 3-4 implement least privilege at a temporal granularity: access is granted per-session, not permanently. A user authenticated to their email should not automatically have access to the HR database, each resource access requires separate authorization evaluated against the current policy. Dynamic policy incorporates risk signals that were irrelevant in static access control models: the user's current geographic location (anomalous if they authenticated from New York but are now requesting access from Eastern Europe), device health posture (is the EDR agent active? are patches current? is disk encryption enabled?), time of day, behavioral analytics (does this access pattern match the user's historical behavior?), and threat intelligence signals.

Tenet 5 mandates continuous device monitoring through MDM (Mobile Device Management) and EDR platforms. ZTA does not trust devices permanently, if a device's security posture degrades (EDR agent disabled, OS patch missed, jailbreak detected), its access should be automatically revoked or restricted pending remediation.

Tenets 6-7 operationalize continuous verification and improvement. Rather than authenticating once per day (or once per VPN session), ZTA requires re-verification on context changes, privilege escalation requests, location changes, or behavioral anomalies trigger additional authentication challenges or automatic session termination.

Google's BeyondCorp initiative, begun in 2011 and publicly described in a 2014 paper, was the pioneering enterprise ZTA implementation. Google eliminated the distinction between "trusted corporate network" and "untrusted internet" for all employee access, requiring device certificates and identity authentication for every application access regardless of network location. This allowed Google employees to work from coffee shops with the same access experience as the corporate campus, and eliminated VPN as a corporate dependency entirely. Microsoft's post-SolarWinds ZTA adoption similarly restructured their internal access model, requiring hardware-attested device health checks and user identity verification for all resource access.

The practical implementation of ZTA for most organizations is incremental. CISA's Zero Trust Maturity Model defines five pillars (Identity, Devices, Networks, Applications and Workloads, Data) and three maturity levels (Traditional, Advanced, Optimal) that allow organizations to assess current posture and plan progressive ZTA adoption. Organizations typically begin with strong identity controls (phishing-resistant MFA, privileged access management), then add device health verification, micro-segmentation of critical assets, and eventually behavioral analytics and continuous authorization.
:::

%%%

---
unit: Resilience
code: BCP
title: Business Continuity & Disaster Recovery Planning
---
:::callout style=soft
**Business Continuity Planning (BCP)** ensures that critical business functions can continue during and after a disruption. **Disaster Recovery (DR)** focuses specifically on restoring IT systems and data after a failure event. Together, BCP/DR form the resilience layer of an organization's security and operational program, governed by **ISO 22301** (Business Continuity Management Systems) and NIST SP 800-34 (Contingency Planning Guide).
:::

::::columns ratio=1:1
::col::
:::list heading="Key Recovery Metrics" style=plain
- **Recovery Time Objective (RTO):** Maximum acceptable time to restore a system or function after a disruption. Example: "The payment processing system must be restored within 4 hours."
- **Recovery Point Objective (RPO):** Maximum acceptable amount of data loss measured in time. Example: "We can tolerate losing no more than 1 hour of transaction data."
- **Maximum Tolerable Downtime (MTD):** The absolute maximum time the organization can survive without a critical function before irreversible harm occurs.
- **Work Recovery Time (WRT):** Time needed to verify system integrity and resume normal operations after technical restoration is complete.
:::
::col::
:::list heading="Backup Strategy, The 3-2-1-1-0 Rule" style=plain
- **3** copies of data (production + 2 backups)
- **2** different storage media types (disk + tape, or disk + cloud)
- **1** copy offsite (geographically separated data center or cloud region)
- **1** copy offline / air-gapped (disconnected from all networks, ransomware-proof)
- **0** untested backups, every backup must be regularly verified with restoration tests
:::
::::

:::table
| DR Strategy | RTO | RPO | Cost | Best For |
|---|---|---|---|---|
| Cold Site | Days–Weeks | Last backup | Low | Non-critical systems |
| Warm Site | Hours–Days | Hours | Medium | Important business functions |
| Hot Site | Minutes–Hours | Minutes | High | Business-critical systems |
| Cloud DR (AWS/Azure) | Minutes | Near-zero | Variable/pay-per-use | Modern cloud workloads |
| Active-Active | Seconds | Near-zero | Very High | Mission-critical (banking, hospitals) |
:::

:::image src="images/01_bcp_dr_rto_rpo_diagram.png" alt="Business continuity diagram showing the relationship between disaster event, RTO, RPO, MTD, and recovery timeline, with the three backup copies illustrated at different recovery tiers" caption="BCP/DR key metrics: RPO defines acceptable data loss (measured backward from the disaster); RTO defines the restoration deadline; MTD defines the absolute survival limit, all three must be defined per critical business function through a Business Impact Analysis" width=full
:::

:::notes
Business continuity and disaster recovery planning is the practice of ensuring organizational resilience against disruptive events, whether cyberattacks, natural disasters, hardware failures, power outages, or pandemic-level business disruptions. While often treated as a separate discipline from cybersecurity, BCP/DR is deeply integrated with the information security program: ransomware attacks are fundamentally availability attacks that require robust BCP/DR capabilities to survive without paying ransom; the NIST CSF Recover function explicitly addresses business continuity; and ISO/IEC 27001 Annex A Control A.17 mandates information security continuity planning.

The foundation of any BCP/DR program is the **Business Impact Analysis (BIA)**, a structured assessment that identifies critical business functions, determines their dependencies (people, systems, data, facilities), and establishes recovery objectives. The BIA produces three key metrics for each critical function: the Recovery Time Objective (RTO), Recovery Point Objective (RPO), and Maximum Tolerable Downtime (MTD). These metrics are not aspirational targets set by IT, they are business requirements set by process owners, representing the operational reality of how long a business function can be unavailable before customer harm, regulatory penalties, or financial losses become unacceptable. A hospital's electronic health record system might have an RTO of 4 hours and an RPO of 1 hour because longer outages risk patient safety. An internal reporting system might have an RTO of 5 days because that function is less time-sensitive.

The **3-2-1-1-0 backup rule** is the industry standard guidance for resilient backup architectures. The original 3-2-1 rule was coined by photography backup advocate Peter Krogh and adopted by the cybersecurity community. The "-1-0" extensions were added by Veeam Software in the ransomware era. The critical addition is the offline/air-gapped copy: ransomware specifically targets and encrypts backup repositories if they are network-connected. The 2021 Colonial Pipeline ransomware attack, the 2021 Kaseya VSA attack (where MSP backup tools were specifically targeted), and numerous healthcare ransomware incidents have demonstrated that backup systems connected to the same network as production are often encrypted along with production data. An air-gapped backup, physically disconnected from all networks, accessible only for scheduled backup operations through a controlled process, provides a recovery option that ransomware cannot reach. The "0 untested backups" requirement addresses a common organizational failure: backups are taken but never tested for restoration, leading to the discovery of corrupted or incomplete backups only at the moment of crisis. NIST SP 800-34 Section 3.4 mandates regular backup testing as part of the contingency plan maintenance cycle.

Recovery site strategies span a spectrum of cost versus recovery speed. A **cold site** is a facility with power, cooling, and network connectivity but no pre-installed hardware or data, the organization ships equipment and restores from backups on demand. This results in RTO measured in days to weeks but minimal ongoing cost. A **warm site** has pre-installed hardware (often on standby) with data synchronized periodically via backups or replication, RTO of hours to days with moderate cost. A **hot site** (or "hot standby") maintains fully operational mirrored systems with near-real-time data replication, RTO of minutes with high cost. Cloud-based disaster recovery (using services like AWS Elastic Disaster Recovery, Azure Site Recovery, or Zerto) provides flexible, pay-per-use hot/warm site capabilities with RTOs of minutes, making enterprise-grade DR accessible to smaller organizations. **Active-active** architectures run workloads simultaneously across two or more sites, the failure of one site results in automatic traffic rerouting to the surviving site with near-zero downtime, but at the highest cost.

The Colonial Pipeline ransomware attack (May 2021) is a powerful BCP/DR teaching example. The pipeline's operational technology (OT) systems were not directly compromised, the ransomware hit business IT systems only. However, Colonial Pipeline shut down the pipeline proactively due to uncertainty about whether OT systems were affected and concern about billing systems being offline. This decision, based on OT/IT network architecture uncertainty and BCP gaps, caused fuel shortages across the U.S. East Coast for six days. The incident demonstrates that BCP/DR planning must extend beyond IT systems to operational dependencies, and that the failure to understand IT/OT boundaries can cause crisis-level decisions based on incomplete information.
:::

%%%

---
unit: Roles
code: RBP
title: Red Team, Blue Team & Purple Team Operations
---
::::columns ratio=1:1:1
::col::
::::card heading="Red Team (Offense)"
:::list style=tight
- **Goal:** Simulate real-world adversaries to find security gaps before attackers do.
- **Methods:** Phishing campaigns, network exploitation, physical intrusion, social engineering.
- **Frameworks:** MITRE ATT&CK, TIBER-EU, CBEST, PTES.
- **Output:** Report of exploited vulnerabilities, attack paths, and ATT&CK technique coverage gaps.
- **Certifications:** OSCP, CRTO, GXPN.
:::
::::
::col::
::::card heading="Blue Team (Defense)"
:::list style=tight
- **Goal:** Detect, contain, and respond to attacks; harden the environment continuously.
- **Methods:** SIEM tuning, threat hunting, EDR management, log analysis, vulnerability patching.
- **Frameworks:** NIST CSF, D3FEND, CIS Controls.
- **Output:** Detection rule improvements, hardening recommendations, incident reports.
- **Certifications:** GCIH, GCIA, GCFA, Security+.
:::
::::
::col::
::::card heading="Purple Team (Collaboration)"
:::list style=tight
- **Goal:** Maximize the value of red and blue interactions through structured knowledge transfer.
- **Methods:** Real-time exercise observation; immediate blue team feedback on red techniques; rapid detection rule creation.
- **Frameworks:** MITRE ATT&CK for Purple Teaming, VECTR platform.
- **Output:** Improved detection coverage mapped to ATT&CK; shared lessons across both teams.
- **Value:** Without purple teaming, red team findings often go unactioned; blue team improvements are untested.
:::
::::
::::

:::table
| Dimension | Red Team | Blue Team | Purple Team |
|---|---|---|---|
| Perspective | Attacker | Defender | Bridge |
| Primary tool | Offensive tradecraft (Cobalt Strike, Metasploit) | SIEM, EDR, Firewall | Both + collaboration facilitation |
| Success metric | Objectives achieved (flags captured) | Mean time to detect/respond | ATT&CK technique detection coverage % |
| Frequency | Annual or semi-annual engagements | Continuous operations | Quarterly exercises |
| Regulatory alignment | TIBER-EU (banking), CBEST (UK finance) | NIST CSF Detect/Respond | Continuous improvement cycle |
:::

:::code language=mermaid caption="Purple team operations: rather than red and blue working in isolation, purple team exercises create a structured collaboration where attack techniques are immediately analyzed for detection opportunities, accelerating security improvement cycles"
flowchart LR
  R["Red team<br/>runs an attack technique"] --> P["Purple facilitator<br/>shares what was done, live"]
  B["Blue team<br/>watches and detects"] --> P
  P --> O["Detection rules tuned,<br/>gaps closed"]
  O --> R
:::

:::notes
The adversarial testing model, pitting offensive teams against defensive teams to evaluate and improve security posture, is a foundational practice in mature security organizations. Understanding the distinct roles, objectives, and outputs of red, blue, and purple teams is essential for security practitioners because these functions collectively form the empirical testing layer of an organization's security program, converting abstract risk assessments into measured, observable security capabilities.

**Red team operations** originate from military war-gaming practices where a designated "red force" simulates an enemy to test the readiness of the defending "blue force." In cybersecurity, red teams conduct adversary emulation, not just penetration testing (which finds vulnerabilities) but full-scenario simulations of realistic threat actors from initial access through achievement of defined objectives (flag capture, data exfiltration, system compromise). Red teams use the same tools and techniques as real adversaries: Cobalt Strike (a commercial C2 framework widely used by both legitimate red teams and criminal actors, which is why Cobalt Strike Beacon detections are a critical blue team capability), Metasploit Framework, custom implants, and living-off-the-land techniques (using built-in OS tools like PowerShell, WMI, and certutil to avoid signature detection). Red team engagements are typically scoped under a Rules of Engagement (ROE) document signed by executive leadership, defining what is in scope, what techniques are prohibited (e.g., destructive actions on production systems), and notification procedures if critical systems are compromised. TIBER-EU (Threat Intelligence-Based Ethical Red Teaming), developed by the European Central Bank, provides the most rigorous framework for red team exercises in the financial services sector.

**Blue team operations** are continuous, unlike red team engagements which occur periodically, the blue team defends 24/7/365 through the Security Operations Center (SOC). Blue teams are responsible for deploying and tuning detection technologies (SIEM, EDR, NDR, DLP), developing and maintaining detection rules (SIGMA rules, YARA signatures, Suricata/Snort IDS rules), conducting threat hunting (proactively searching for signs of compromise without waiting for alerts), managing vulnerability remediation programs, and executing incident response when threats are confirmed. MITRE D3FEND, released in 2021, is the defensive complement to ATT&CK, a knowledge graph of defensive techniques mapped to the offensive techniques in ATT&CK, enabling blue teams to systematically identify and deploy countermeasures against known adversary behaviors. The CIS Controls (v8) provide a prioritized, evidence-based framework of 18 control families that blue teams use to structure their defensive program, with IG1 (Implementation Group 1) representing the minimum baseline that all organizations should achieve.

**Purple team operations** emerged from the recognition that red and blue teams often operate in silos, red teams submit reports that blue teams receive weeks after an exercise, limiting the opportunity for real-time learning. Purple teaming restructures the interaction: a purple team facilitator (who may be a third-party contractor or an internal team member) observes red team technique execution in real time, immediately checks whether blue team detection tools triggered, and works with blue team analysts to improve detection rules on the spot. The VECTR platform (Visual, Execution, Collect, Track, Report) is purpose-built for documenting and tracking purple team exercises, mapping each tested ATT&CK technique to its detection outcome and creating a historical record of ATT&CK coverage improvement over time. Purple teaming is particularly valuable when organizations have invested in ATT&CK-aligned threat intelligence but have not systematically validated whether their detection stack actually detects the techniques attributed to their primary threat actors.

The measurement of red/blue/purple team effectiveness is increasingly formalized through metrics. **Detection coverage** (what percentage of ATT&CK techniques relevant to the organization's threat model are detectable by current tools) is the primary purple team output metric. **Mean Time to Detect (MTTD)** measures SOC responsiveness. **Mean Time to Contain (MTTC)** and **Mean Time to Respond (MTTR)** measure IR effectiveness. Organizations track these metrics over time to demonstrate security program maturity to boards, regulators, and cyber insurers, increasingly required for cyber insurance underwriting and premium calculation.
:::

%%%

---
unit: Mindset
code: FAQ
title: Common Misconceptions in Cybersecurity
---
:::callout style=soft
Misconceptions about cybersecurity are widespread among both the general public and new practitioners. Addressing these directly helps establish accurate mental models that will prevent poor decision-making in professional practice. Each misconception below is grounded in real-world consequences.
:::

::::columns ratio=1:1
::col::
:::list heading="Misconception 1: Antivirus Is Sufficient Protection" style=plain
- **Reality:** Signature-based AV detects only known malware via hash matching, zero-day, fileless, and polymorphic malware evade it entirely.
- Modern endpoints require behavioral EDR, application allowlisting, and memory protection.
- DBIR: signature-based AV alone detects fewer than 50% of breach-related malware samples.
:::

:::list heading="Misconception 2: Strong Passwords Are Enough" style=plain
- **Reality:** Complex passwords are still vulnerable to credential stuffing, phishing, keylogging, and MITM attacks.
- MFA reduces account compromise by over 99% (Microsoft data); phishing-resistant MFA (FIDO2/passkeys) eliminates credential phishing entirely.
- Password complexity alone does not defeat attacks that bypass the password entirely.
:::

:::list heading="Misconception 3: We Are Too Small to Be a Target" style=plain
- **Reality:** Automated tools scan and attack all internet-exposed systems indiscriminately, no human chooses whether you are "worth it."
- Small vendors are specifically targeted in supply chain attacks (e.g., Kaseya VSA, 2021) to reach larger downstream victims.
- CISA and DBIR data confirm organizations of all sizes are victimized at similar rates.
:::
::col::
:::list heading="Misconception 4: Compliance Equals Security" style=plain
- **Reality:** Compliance frameworks define minimum baselines, not comprehensive security coverage.
- Target was PCI-DSS compliant during the 2013 breach that exposed 40 million payment cards.
- True security requires risk-based thinking that goes beyond the compliance checklist.
:::

:::list heading="Misconception 5: Cyber Threats Are Always External" style=plain
- **Reality:** Insider threats account for approximately 34% of data breaches (Ponemon Institute 2023).
- Negligent insiders, misconfigured systems, phishing clicks, improper data handling, cause more incidents than malicious ones.
- Zero Trust Architecture removes implicit internal trust, treating all requests as potentially adversarial.
:::

:::list heading="Misconception 6: Encryption Makes Data Completely Safe" style=plain
- **Reality:** Encryption does not protect against key management failures, decrypted data in active use, or implementation flaws.
- Heartbleed (CVE-2014-0160) leaked memory containing encryption keys from running TLS servers.
- Ransomware uses the victim's own system to encrypt files, encryption is one layer, not a complete defense.
:::
::::

:::notes
Correcting misconceptions is one of the most impactful educational interventions in cybersecurity. Inaccurate mental models lead to poor security decisions at every level of an organization, from individual employees who believe their strong password protects them from phishing, to executives who believe that passing a compliance audit means their organization is secure, to security engineers who deploy antivirus as their primary endpoint protection. Addressing these misconceptions directly accelerates the development of accurate, risk-based thinking that is the hallmark of effective security practitioners.

**Misconception 1: Antivirus is sufficient.** This misconception has its roots in the early history of personal computing, when viruses spread primarily through floppy disks and signature-based detection was genuinely effective at catching the limited population of known malware. Today, the threat landscape has changed beyond recognition. Security researchers at AV-TEST register approximately 450,000 new malware samples every day. Sophisticated actors specifically design their tools to evade common antivirus signatures through polymorphism (changing code structure while maintaining function), metamorphism (completely rewriting code between infections), and packing/encryption (encrypting the payload and decrypting it only at runtime in memory). Fileless malware never writes anything to disk, making file-scanning irrelevant. The practical consequence: organizations that invest only in AV have a deeply false sense of security. Endpoint Detection and Response (EDR) platforms, which monitor process behavior, memory patterns, and system call sequences rather than file signatures, represent the modern minimum for endpoint protection.

**Misconception 2: Strong passwords are enough.** The password security paradigm is fundamentally broken not because strong passwords are easy to guess, but because most accounts are not compromised through guessing at all. Credential stuffing attacks use the billions of username/password combinations leaked in historical breaches (Have I Been Pwned catalogs over 12 billion leaked accounts) to automatically test those credentials against other services, exploiting the reality that many people reuse passwords. Phishing attacks trick users into entering their correct, strong passwords on fake websites. Keyloggers capture passwords as they are typed. Man-in-the-middle attacks intercept credentials in transit. None of these attacks are defeated by password complexity. MFA, specifically phishing-resistant MFA using hardware security keys (FIDO2/WebAuthn) or device-bound passkeys, is the only control that provides meaningful protection against all of these vectors simultaneously, because the authentication secret is device-bound and never transmitted to a potentially attacker-controlled server.

**Misconception 3: Small organizations are not targets.** This misconception is psychologically understandable, it feels reasonable that a nation-state attacker or sophisticated criminal group would focus on large, high-value targets. And for some attacks, this is true: APTs targeting specific industries or organizations do prioritize high-value victims. However, the vast majority of cybercrime is automated and indiscriminate. Shodan, Censys, and similar internet scanning tools allow attackers to enumerate every internet-connected device with a given open port or service version. A criminal group deploying ransomware does not choose targets based on revenue, they attack every system their automated tools find vulnerable. Additionally, supply chain attacks specifically target small vendors (MSPs, software developers, logistics providers) as pathways to their larger clients. The 2021 Kaseya VSA attack used a zero-day in a small IT management software provider to deploy REvil ransomware across 1,500 downstream managed service provider customers, none of whom were the original attacker's primary target.

**Misconception 4: Compliance equals security.** Compliance frameworks define regulatory minimum standards based on best practices at the time of their development, they are necessarily backward-looking. By the time a compliance requirement is codified, adversaries have often already developed techniques that exploit gaps the framework doesn't address. The 2013 Target breach, mentioned earlier, is the classic example: Target was PCI DSS compliant at the time of the breach but was still compromised through a third-party vendor connection (network segmentation gap) and insufficient monitoring of point-of-sale network traffic (detection gap). The distinction between compliance and security is that compliance asks "do we meet the minimum requirements?" while security asks "have we reduced risk to an acceptable level for our specific threat environment?" CISO leadership must communicate this distinction clearly to boards who may view compliance certification as evidence of adequate security.

**Misconceptions 5 and 6** address insider threats and encryption limitations respectively. The insider threat misconception leads organizations to focus all security investment on perimeter defenses while neglecting internal user monitoring, data access logging, and data loss prevention tools. The encryption misconception leads to over-reliance on encryption as a universal solution, particularly dangerous when combined with poor key management practices, since encryption is only as secure as the protection of its keys. These misconceptions collectively illustrate why defense-in-depth thinking, where no single control is treated as sufficient, is the only defensible security posture.

:::

%%%

---
unit: Roles
code: CRT
title: Cybersecurity Certifications & Learning Pathways
---
:::callout style=soft
Professional certifications provide structured, vendor-recognized evidence of cybersecurity competency. They signal proficiency to employers, validate knowledge against industry standards, and provide structured learning pathways. The certification landscape spans foundational, intermediate, advanced, and specialist tracks aligned with different career roles.
:::

:::table
| Certification | Issuing Body | Level | Focus Area | Prerequisite |
|---|---|---|---|---|
| **CompTIA Security+** | CompTIA | Foundational | Broad security fundamentals; DoD 8570 approved | None required (SY0-701) |
| **CompTIA CySA+** | CompTIA | Intermediate | Threat detection, behavioral analytics, SIEM | Security+ recommended |
| **CompTIA CASP+** | CompTIA | Advanced | Enterprise security architecture, risk management | 10 years experience |
| **CEH (Certified Ethical Hacker)** | EC-Council | Intermediate | Ethical hacking methodology, tools | None (but training required) |
| **OSCP (Offensive Security Certified Professional)** | Offensive Security | Advanced | Hands-on penetration testing; 24-hour practical exam | PWK course; strong Linux/scripting |
| **CISSP** | (ISC)² | Expert | Security management, architecture, governance | 5 years experience across 8 domains |
| **CISM** | ISACA | Expert | Information security management, GRC | 5 years management experience |
| **CRISC** | ISACA | Expert | IT risk identification, assessment, control | 3 years risk management experience |
| **GCIH / GCIA / GCFA** | GIAC/SANS | Advanced | Incident handling, network forensics, advanced forensics | Domain-specific experience |
| **AWS Security Specialty** | Amazon Web Services | Advanced | Cloud security architecture and operations on AWS | AWS Solutions Architect level |
| **CCSP** | (ISC)² + CSA | Expert | Cloud security architecture and governance | CISSP or 5 years experience |
:::

::::columns ratio=1:1
::col::
:::list heading="Recommended Learning Pathway by Role" style=plain
- **SOC Analyst / Blue Team:** CompTIA Security+ → CySA+ → GCIH → GCIA → GCFA
- **Penetration Tester / Red Team:** CompTIA Security+ → CEH → OSCP → GXPN / CRTO
- **Security Engineer / Architect:** CompTIA Security+ → CASP+ → CISSP → Cloud Specialty
- **GRC / Compliance:** CompTIA Security+ → CISM → CRISC → CISSP
- **Cloud Security:** AWS/Azure Fundamentals → Security Specialty → CCSP
:::
::col::
:::list heading="Free & Open-Source Learning Resources" style=plain
- **TryHackMe / HackTheBox:** Gamified, hands-on labs (beginner to advanced)
- **SANS Cyber Aces:** Free foundational training
- **MITRE ATT&CK Navigator:** Interactive framework exploration
- **NIST SP 800 Series:** Free authoritative reference library
- **OWASP Top 10:** Web application security reference
- **Cybrary / Professor Messer:** Free Security+ preparation
- **PortSwigger Web Security Academy:** Free web hacking labs (Burp Suite)
:::
::::

:::code language=mermaid caption="Cybersecurity certification roadmap: CompTIA Security+ serves as the universal foundation; career tracks branch toward offensive (OSCP), defensive (GCIH/GCFA), architectural (CISSP), and governance (CISM/CRISC) specializations"
flowchart TB
  F["Foundation: Security+"]
  F --> SOC["SOC / Blue Team"]
  F --> PT["Penetration Testing / Red Team"]
  F --> SE["Security Engineering"]
  F --> GRC["GRC / Compliance"]
  SOC --> SOC1["CySA+"] --> SOC2["GCIH, GCIA"]
  PT --> PT1["PenTest+, eJPT"] --> PT2["OSCP"]
  SE --> SE1["CCSP, cloud vendor certs"] --> SE2["CISSP"]
  GRC --> G1["CISA, CRISC"] --> G2["CISM, CISSP"]
:::

:::notes
Cybersecurity certifications serve multiple purposes in the professional ecosystem. For individuals, they provide structured learning frameworks that ensure comprehensive coverage of a domain, validate knowledge through standardized examinations, and communicate competency to employers in a labor market where skills can be difficult to assess from resume descriptions alone. For employers, certifications provide a baseline quality signal for candidate screening, particularly important in a field where self-described expertise varies enormously. For regulatory compliance, certain certifications are specifically required: U.S. Department of Defense Directive 8570 mandates that personnel performing information assurance functions hold specific certifications (Security+ for IA Technical Level 1 baseline, CISSP for IA Management Level 3), and similar requirements exist across federal contracting.

**CompTIA Security+** (currently SY0-701, updated in November 2023) is the most widely held entry-level cybersecurity certification globally, with over 700,000 certifications awarded. It covers six domains: General Security Concepts, Threats, Vulnerabilities, and Mitigations; Security Architecture; Security Operations; Security Program Management and Oversight. Security+ is approved under DoD 8570/8140 for multiple IA roles and is accepted by employers across government, defense, commercial, and non-profit sectors as evidence of foundational security literacy. Unlike experience-based certifications, Security+ has no formal prerequisite, making it accessible to career changers and students completing their first cybersecurity course.

**OSCP (Offensive Security Certified Professional)** deserves special discussion because it is uniquely practical among industry certifications. Unlike multiple-choice exams, the OSCP assessment requires candidates to compromise five target machines in a private lab environment within 24 continuous hours, then write and submit a professional penetration test report within an additional 24 hours. This format, explicitly designed to be anti-memorization, ensures that certified professionals have demonstrated actual exploitation skills, not just knowledge of security concepts. Offensive Security's Proving Grounds and HackTheBox provide practice environments, and the community-maintained OSCP preparation resources are extensive. OSCP is widely considered the most respected entry-level offensive certification in the industry.

**CISSP (Certified Information Systems Security Professional)** is the gold standard for senior security management and architecture positions. Maintained by (ISC)², CISSP covers eight domains (Security and Risk Management; Asset Security; Security Architecture and Engineering; Communication and Network Security; Identity and Access Management; Security Assessment and Testing; Security Operations; Software Development Security) with a four-hour, 100-150 adaptive question examination that is widely regarded as one of the most challenging cybersecurity assessments available. The mandatory five-year professional experience requirement (across at least two of the eight domains) ensures that CISSP holders have substantial real-world context for the knowledge tested. CISSP is often required for CISO, security director, and senior architect positions.

**GIAC (Global Information Assurance Certification)**, the certification arm of the SANS Institute, offers the most technically specific and respected certifications for operational security roles. GCIH (Certified Incident Handler), GCIA (Certified Intrusion Analyst), GCFA (Certified Forensic Analyst), and GNFA (Network Forensic Analyst) collectively represent the blue team specialist track. SANS courses are expensive (typically $4,000-8,000 per course) but are universally recognized as the highest-quality technical security training available, with SANS authors including some of the most cited researchers in the field.

For students in this course, the recommended first step is CompTIA Security+, which directly aligns with the topics covered in this curriculum and provides a recognized credential that opens doors to entry-level SOC analyst and security support positions. The hands-on lab platforms TryHackMe and HackTheBox both offer free tiers that allow students to practice the technical skills (network scanning, enumeration, exploitation, and defense) that complement the theoretical foundations covered in this lecture. SANS Cyber Aces provides a completely free, SANS-quality foundational curriculum covering operating systems, networking, and security fundamentals.

Certifications supplement hands-on experience and continuous learning; they do not replace them. Effective practitioners combine certification knowledge with lab practice, Capture the Flag competitions and engagement with the security community through conferences (DEF CON, Black Hat, BSides), blogs (Krebs on Security, Troy Hunt) and open-source work.
:::

%%%

---
unit: Compliance
code: LEG
title: "Legal & Regulatory Compliance Landscape"
---
::::columns ratio=1:1
::col::
:::table
| Regulation | Scope | Key Requirement | Max Penalty |
|---|---|---|---|
| **GDPR** | EU personal data globally | Breach notification within 72 hours (Art. 33); data minimization | €20M or 4% global revenue |
| **HIPAA** | U.S. protected health info | Administrative, physical, and technical safeguards (45 CFR §164) | Up to $1.9M per category/year |
| **PCI-DSS** | Cardholder payment data | 12 requirements including encryption, access control, pen testing | Card processing revocation + fines |
| **CFAA** | U.S. unauthorized computer access | Criminalizes unauthorized access to protected computers | Up to 10 years imprisonment |
| **FISMA** | U.S. federal information systems | RMF compliance, annual assessments, NIST SP 800-53 controls | Funding sanctions, congressional scrutiny |
:::
::col::
:::callout style=soft
**Breach Notification Timelines** vary by regulation: GDPR mandates **72 hours** to the supervisory authority; HIPAA requires **60 days** to HHS and affected individuals; U.S. state laws (e.g., California AB 375) may require **30 days** or less.
:::
:::list heading="Compliance vs. Security" style=plain
- Compliance defines a **minimum floor**, not a security ceiling, a compliant organization can still be breached.
- **NIST RMF** integrates compliance and security through a continuous authorization and monitoring lifecycle.
- **ISO/IEC 27001 certification** is the international signal of a mature ISMS, accepted across sectors and borders.
- Regulatory requirements drive security budgets, align control justifications to applicable frameworks.
:::
::::

:::code language=mermaid caption="Global regulatory compliance landscape: organizations operating across borders must navigate overlapping data protection laws, each with distinct scope, requirements, and enforcement mechanisms"
mindmap
  root((Data protection laws))
    Europe
      GDPR
    United States
      HIPAA
      CCPA
      CFAA
    Canada
      PIPEDA
    Brazil
      LGPD
    Southeast Asia
      PDPA Singapore and Thailand
:::

:::notes
Legal and regulatory compliance is a foundational driver of organizational cybersecurity investment. While security professionals focus on risk reduction, legal frameworks create binding obligations with defined consequences for non-compliance, transforming security from a voluntary best practice into a mandatory operational requirement. Understanding the major regulatory frameworks is essential for every cybersecurity practitioner, as they shape security program scope, budget allocation, control selection, and incident response procedures.

The **General Data Protection Regulation (GDPR)**, effective May 2018, is the most globally impactful data protection law. It applies to any organization that processes personal data of EU residents, regardless of where the organization is based, making it effectively a global standard. GDPR's key principles include data minimization (collecting only what is necessary), purpose limitation (using data only for stated purposes), storage limitation (retaining data only as long as needed), and privacy by design (embedding privacy into systems from the start). Article 32 requires "appropriate technical and organizational measures" to protect data, which regulators interpret to include encryption, access controls, and regular security testing. Enforcement has been substantial: Amazon was fined €746 million (2021), WhatsApp €225 million (2021), and Meta €1.2 billion (2023), illustrating that GDPR enforcement is active and impactful.

**HIPAA (Health Insurance Portability and Accountability Act, 1996)** governs Protected Health Information (PHI) in the United States, affecting all healthcare providers, health plans, and their business associates. The Security Rule (45 CFR Part 164) mandates administrative safeguards (risk analysis, security training, access management), physical safeguards (facility access controls, device controls), and technical safeguards (access control, audit controls, integrity, transmission security). The 2023 HHS Office for Civil Rights (OCR) Wall of Shame lists thousands of breaches affecting 500+ individuals, a public accountability mechanism that has become a compliance incentive in itself. Notable fines include Anthem ($16M, 2018) for the 2015 breach affecting 79 million records.

**PCI-DSS (Payment Card Industry Data Security Standard)**, maintained by the PCI Security Standards Council (Visa, Mastercard, American Express, Discover, JCB), applies to all organizations that store, process, or transmit cardholder data. Version 4.0 (released 2022) added requirements for targeted risk analysis, multi-factor authentication for all accounts accessing cardholder data environment, and enhanced phishing awareness. Non-compliance consequences include card processing privilege revocation, per-transaction fines, and mandatory forensic investigations.

**FISMA (Federal Information Security Modernization Act, 2014)** requires all U.S. federal agencies to implement comprehensive information security programs based on NIST standards, including the Risk Management Framework (SP 800-37), security controls (SP 800-53), and continuous monitoring (SP 800-137). FISMA compliance is audited annually by agency Inspectors General and reported to Congress, creating accountability at the highest levels of government. The framework has been adopted by contractors and private-sector organizations seeking to align with federal security standards.

The critical insight for security professionals: **compliance creates a floor, not a ceiling**. An organization can be fully HIPAA-compliant and still suffer a catastrophic breach if it meets only minimum requirements without addressing the full threat landscape. Mature security programs use compliance frameworks as one input into a comprehensive risk management program, satisfying legal obligations while applying additional controls based on threat intelligence, business risk, and industry best practices. The integration of multiple frameworks (NIST CSF + ISO 27001 + applicable regulations) provides the most robust governance foundation.
:::

%%%

---
unit: Operations
code: MET
title: Security Metrics & KPIs, Measuring Program Effectiveness
---
:::callout style=line
Security programs must be measurable to be governable. **Key Performance Indicators (KPIs)** and **Key Risk Indicators (KRIs)** enable CISOs and security teams to demonstrate value, identify trends, and make data-driven decisions aligned with business objectives and NIST CSF functions.
:::

::::columns ratio=1:1
::col::
:::table
| Metric | Definition | Target Benchmark |
|---|---|---|
| **MTTD** (Mean Time to Detect) | Average time from breach start to detection | < 24 hours (industry: ~207 days) |
| **MTTR** (Mean Time to Respond) | Average time from detection to containment | < 4 hours for critical severity |
| **Patch Coverage %** | % of systems patched within SLA after CVE disclosure | > 95% within 30 days (critical: 72 hrs) |
| **Phishing Click Rate** | % of employees who clicked simulated phishing links | < 5% after awareness training |
| **Vulnerability Remediation SLA** | % of Critical/High CVEs resolved within SLA | > 90% Critical within 15 days |
| **MFA Enrollment Rate** | % of user accounts with MFA enabled | 100% for privileged; > 95% overall |
| **Security Awareness Completion** | % of staff completing mandatory training | > 98% annually |
:::
::col::
:::list heading="NIST CSF Function Alignment" style=plain
- **Identify (ID):** Asset inventory completeness %, open vulnerabilities by age
- **Protect (PR):** Patch coverage %, MFA enrollment rate, training completion
- **Detect (DE):** MTTD, alert false-positive rate, SIEM rule coverage %
- **Respond (RS):** MTTR, incident closure rate, playbook adherence %
- **Recover (RC):** RTO achievement rate, backup success rate, post-incident review completion
:::
:::callout style=soft
**IBM Cost of a Data Breach Report 2023:** Organizations with mature security AI and automation detected and contained breaches **108 days faster** and saved **$1.76M** compared to organizations without these capabilities. Metrics drive maturity.
:::
::::

:::notes
Measuring security program effectiveness is as critical as implementing security controls. Without metrics, security teams cannot demonstrate value to executives, identify program gaps, justify budget requests, or track improvement over time. The discipline of security measurement is addressed by NIST SP 800-55 (Performance Measurement Guide for Information Security), which provides a framework for developing, selecting, and implementing measures that reflect the organization's security objectives.

**Mean Time to Detect (MTTD)** is one of the most impactful security metrics because it directly quantifies how long attackers operate undetected in an environment. IBM's 2023 Cost of a Data Breach Report found that the global average time to identify a breach was 204 days, giving attackers over six months to conduct reconnaissance, escalate privileges, establish persistence, and exfiltrate data. Organizations using AI-powered security operations platforms reduced MTTD to an average of 28 days. Each day of dwell time (the period between initial compromise and detection) increases the scope and cost of the breach. MTTD improvements are typically driven by investments in SIEM (Security Information and Event Management), EDR (Endpoint Detection and Response), and threat hunting capabilities.

**Mean Time to Respond (MTTR)** measures the efficiency of the incident response process once an event is detected. MTTR encompasses triage, containment, eradication, and recovery phases. Organizations with documented and rehearsed incident response playbooks consistently achieve lower MTTR than those that handle incidents ad-hoc. The 2021 Colonial Pipeline ransomware incident illustrates the consequence of poor MTTR, the pipeline remained offline for six days, causing fuel shortages across the Eastern United States and a $4.4 million ransom payment, because response procedures were insufficient for the scale of the incident.

**Patch Coverage %** measures how effectively the organization manages the vulnerability lifecycle. CISA's Known Exploited Vulnerabilities (KEV) catalog mandates that U.S. federal agencies remediate listed vulnerabilities within 15 days for critical severity, driving the industry benchmark toward 72 hours for critical CVEs. Patch coverage below 95% typically indicates systemic asset inventory gaps (unmapped systems that miss patch cycles) or approval process friction (change management processes that delay emergency patching). Automated patch management platforms integrated with vulnerability scanners can achieve 99%+ coverage rates.

**Phishing Click Rate** is a leading indicator of human-factor security posture. Proofpoint's 2023 State of the Phish report found that 44% of employees clicked on phishing links in organizations without formal security awareness programs, compared to 5-7% in organizations with monthly simulated phishing campaigns and just-in-time training delivery. The click rate is a lagging indicator of training effectiveness; security awareness programs should additionally measure reporting rates (employees who report suspicious emails) as a positive behavior metric.

Security metrics serve different audiences: operational metrics (MTTD, MTTR, alert volume) are relevant to SOC teams; risk metrics (open critical vulnerabilities, compliance status, third-party risk scores) are relevant to risk committees; program metrics (budget utilization, headcount, training completion) are relevant to executive leadership. A mature security metrics program addresses all three audiences with role-appropriate dashboards, enabling informed decision-making at every level of the organization.
:::

%%%

---
unit: Culture
code: CUL
title: Building a Security-Aware Organization
---
::::columns ratio=1:1
::col::
:::list heading="Security Awareness Program Elements" style=plain
- **Phishing Simulations:** Monthly simulated phishing campaigns with immediate, personalized feedback for users who click. Track click rates, reporting rates, and repeat offenders.
- **Mandatory Training:** Annual baseline training plus role-specific modules (e.g., developers: OWASP; HR: social engineering; executives: business email compromise).
- **Tabletop Exercises:** Quarterly scenario-based exercises where leadership teams walk through realistic incident scenarios without affecting production systems.
- **Security Champions:** Embedded advocates in each business unit who receive advanced training and serve as the first line of security awareness within their teams.
- **Incident Reporting Culture:** Low-friction, blame-free reporting channels encourage early disclosure of suspected incidents before they escalate.
- **Onboarding Integration:** Security training woven into the first week of employment, establishing expectations before bad habits form.
:::
::col::
:::table
| SANS Awareness Maturity Level | Description |
|---|---|
| **Level 1, Non-Existent** | No formal awareness program; ad-hoc training at most. |
| **Level 2, Compliance Focused** | Annual training checkbox; no behavioral change measurement. |
| **Level 3, Promoting Awareness** | Regular communications, phishing simulations, metrics tracked. |
| **Level 4, Long-Term Sustainment** | Multi-module program with role-specific content and continuous measurement. |
| **Level 5, Metrics Framework** | Fully data-driven program; awareness KPIs reported to executive leadership. |
:::
:::callout style=soft
**Verizon DBIR 2023:** 74% of all breaches involved the human element, through error, privilege misuse, social engineering, or stolen credentials. Technology alone cannot close this gap.
:::
::::

:::code language=mermaid caption="SANS Security Awareness Maturity Model: organizations progress from ad-hoc awareness through compliance-driven training to a sustainable, metrics-driven culture where security is embedded in daily employee behavior"
flowchart BT
  L1["1. Non-Existent<br/>no program"] --> L2["2. Compliance-Focused<br/>annual checkbox training"]
  L2 --> L3["3. Promoting Awareness and Behavior Change<br/>targeted, ongoing content"]
  L3 --> L4["4. Long-Term Sustainment and Culture Change<br/>security part of daily work"]
  L4 --> L5["5. Metrics Framework<br/>measured, data-driven"]
:::

:::notes
Technology controls, firewalls, endpoint detection, encryption, multi-factor authentication, are necessary but insufficient. The 2023 Verizon Data Breach Investigations Report found that **74% of all breaches involved the human element**, whether through direct employee error, social engineering manipulation, misuse of privileged access, or use of stolen credentials. Building a security-aware organizational culture is therefore not a soft, supplementary activity, it is a core security control with measurable impact on breach frequency, dwell time, and incident cost.

The foundation of a security awareness program is the recognition that human behavior is a skill that can be trained and measured, not a fixed vulnerability to be resigned to. The SANS Security Awareness Maturity Model provides a structured framework for assessing and advancing an organization's human security posture across five levels. Most organizations without dedicated security awareness programs operate at Level 1 or 2, either doing nothing or checking the annual compliance training box without measuring behavioral change. Research consistently shows that organizations operating at Level 3 and above (with regular phishing simulations, targeted training, and behavioral metrics) achieve click rates below 5% and significantly higher incident reporting rates.

**Phishing simulations** are the most widely adopted awareness measurement tool. Platforms such as KnowBe4, Proofpoint Security Awareness Training, and Cofense deliver realistic phishing scenarios tailored to current threat intelligence (e.g., simulating DocuSign credential harvesting campaigns or Microsoft 365 login page spoofing). The most effective programs integrate immediate, just-in-time training at the moment of failure, when a user clicks a simulated phishing link, they immediately receive a brief, contextual lesson about the specific technique used. This timing leverages the teachable moment effect: learning delivered immediately after an error is significantly more retained than learning delivered in advance. Organizations should track both click rates (declining over time indicates success) and reporting rates (users who report suspicious emails, a positive security behavior that should increase over time).

**Tabletop exercises** (TTX) are scenario-based discussions in which key stakeholders, executives, IT leadership, legal, communications, HR, walk through the steps they would take in response to a simulated incident. Unlike live-fire exercises (penetration tests, red team engagements) that test technical controls, TTX tests organizational decision-making, communication protocols, and inter-team coordination. NIST SP 800-84 provides guidance on IT exercise design. Common TTX scenarios include ransomware attacks requiring business continuity decisions, data breach scenarios requiring regulatory notification decisions, and insider threat scenarios requiring HR and legal coordination. Organizations that conduct TTX at least quarterly reduce average incident response time by an average of 35% compared to those that do not.

**Security Champions programs** embed security advocates within product development, operations, finance, HR, and other business units. Champions receive additional security training (e.g., SANS Cyber Aces, OWASP for developers), participate in security team meetings, and serve as the first point of contact for security questions within their units. Champions programs address a fundamental challenge in large organizations: the security team cannot be physically present in every team conversation where security-relevant decisions are made. Champions extend the security team's reach exponentially, and organizations with mature Champions programs report that a higher percentage of security issues are identified and resolved before they reach the security team for escalation.

The cultural dimension of security awareness extends to leadership behavior. Research in organizational psychology consistently shows that employees model their behavior on that of senior leadership, if executives bypass security controls, override MFA requirements, or dismiss security team recommendations, employees infer that security is not genuinely valued. Security leaders (CISOs) must cultivate executive-level security advocacy, ensuring that leaders visibly comply with the same security requirements as all other staff and publicly endorse the security awareness program as a business priority, not just a compliance obligation.
:::

%%%

---
unit: Summary
code: CHK
title: Checkpoint, Foundations Knowledge Review
---
:::callout style=soft
This checkpoint reviews the key concepts from the Cybersecurity Foundations module. Use this as a self-assessment tool before the formative assessment. Each question maps to a specific framework or standard discussed in this class.
:::

::::columns ratio=1:1
::col::
:::list heading="Concept Check Questions" style=plain
- **Q1 (CIA Triad):** A hospital's ransomware attack encrypted patient records, making them inaccessible for 3 days. Which CIA property was primarily violated? How would you classify this using the Parkerian Hexad?
- **Q2 (NIST CSF):** Which NIST CSF 2.0 function was added in the February 2024 update? Why is it positioned as the foundation of all other functions?
- **Q3 (STRIDE):** A developer discovers that their application does not log user actions. Which STRIDE threat category does this gap primarily enable?
- **Q4 (CVSS):** A vulnerability scored CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H, what is the severity classification? What does AV:N tell you about remediation priority?
- **Q5 (Risk):** An asset worth $500,000 has an Exposure Factor of 0.6, and the threat occurs once every 5 years. Calculate SLE and ALE. What is the maximum justified annual spend on controls?
- **Q6 (ATT&CK):** Map the following action to its MITRE ATT&CK technique ID: "An attacker modifies a Windows Registry key to ensure their malware restarts after every reboot."
- **Q7 (Access Control):** Which access control model would you recommend for a healthcare system that needs to allow physician access to patient records only during scheduled appointments and from hospital-approved devices?
:::
::col::
:::list heading="Answers" style=plain
- **A1:** Availability was primarily violated. Parkerian Hexad analysis: Availability (system inaccessible) + Utility (data present but unusable while encrypted). If data was also exfiltrated before encryption, Confidentiality is also violated.
- **A2:** The Govern (GV) function. It is foundational because all other functions (Identify, Protect, Detect, Respond, Recover) must be aligned with organizational policies, risk tolerance, roles, and strategic objectives, which governance defines.
- **A3:** Repudiation, users can deny performing actions because no audit trail exists to prove they did. Lack of logging is a non-repudiation failure.
- **A4:** CVSS 10.0, Critical. AV:N (Attack Vector: Network) means the vulnerability is remotely exploitable over the internet without physical or local access, making it the highest remediation priority.
- **A5:** SLE = $500,000 × 0.6 = $300,000. ARO = 1/5 = 0.2. ALE = $300,000 × 0.2 = $60,000/year. Maximum justified annual spend is $60,000.
- **A6:** T1547.001, Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder.
- **A7:** ABAC (Attribute-Based Access Control), requires dynamic evaluation of subject attributes (physician role), object attributes (patient record), time attribute (scheduled appointment), and device attribute (hospital-approved device). RBAC alone cannot enforce time and device constraints.
:::
::::

:::code language=mermaid caption="Foundations checkpoint: seven key concepts mapped to their frameworks, each question tests the ability to apply a framework to a realistic scenario, not merely recall a definition"
mindmap
  root((Foundations))
    CIA Triad
    NIST CSF
    STRIDE
    CVSS
    Risk = Likelihood x Impact
    MITRE ATT&CK
    Access control models
:::

:::notes
This checkpoint slide serves as both a formative assessment tool and a synthesis exercise that connects the discrete topics covered throughout this lecture into an integrated analytical framework. The questions are deliberately scenario-based rather than definition-recall because real professional practice always requires the application of knowledge to specific contexts, practitioners who can recite the CIA triad but cannot identify which property a specific attack violated are not yet thinking like security professionals.

Working through each question in detail:

**Question 1 (CIA + Parkerian Hexad integration):** Ransomware is primarily an availability attack because the core impact is making data and systems inaccessible. However, modern ransomware operations almost always include a data exfiltration component (double extortion), making confidentiality the secondary violated property. The Parkerian Hexad adds nuance: encrypted files still exist on disk (availability in the strict technical sense is not violated, the system is running), but the data is practically unusable, a utility violation. If the ransomware operator also exfiltrated data before encryption, possession is also violated (the organization has lost exclusive control of their data). This multi-property analysis is more useful for insurance claims, legal proceedings, and post-incident reporting than the simple "availability attack" characterization.

**Question 2 (NIST CSF 2.0):** The Govern function's positioning as foundational reflects a maturity insight: organizations that implemented CSF 1.1 often found that individual functions operated in isolation, the IR team responding without alignment to business priorities, the protect function deploying controls without executive risk tolerance guidance. By making governance the anchor, CSF 2.0 ensures that every security activity is contextualized within organizational strategy, regulatory requirements, and risk appetite.

**Question 3 (STRIDE Repudiation):** This question tests the ability to map a specific technical gap (missing audit logs) to a STRIDE threat category. Many students initially answer "Information Disclosure" (thinking that logs could leak information), but the correct analysis focuses on what the gap enables: without logs, users can deny performing actions, repudiation. This is why comprehensive, tamper-evident audit logging (enforced by NIST SP 800-53 AU-3 and ISO 27001 A.12.4) is a security control, not just an operational practice.

**Question 4 (CVSS vector string interpretation):** Reading CVSS vector strings is a practical skill for vulnerability analysts and patch management teams. AV:N is particularly significant because it determines whether a vulnerability requires physical proximity, local access, or can be exploited from anywhere on the internet. Network-exploitable vulnerabilities with no authentication requirement (PR:N) and no user interaction requirement (UI:N), the "no-click, no-auth, internet-exposed" pattern, are the highest-priority class of vulnerabilities for emergency patching, exemplified by Log4Shell, Heartbleed, and EternalBlue.

**Question 5 (ALE calculation):** The ALE calculation exercise develops quantitative risk intuition. The key insight is that ALE defines the economic ceiling for control investment, spending more than ALE on a control means the cure costs more than the disease. This does not mean organizations should spend exactly ALE; other factors (regulatory penalties that exceed direct damage costs, reputational harm not captured in direct loss estimates, cascading effects) can justify higher investment. But ALE provides the anchoring point for cost-benefit analysis.

**Questions 6 and 7** test framework application at the operational level, mapping observations to specific ATT&CK technique IDs (a skill used daily by threat analysts and detection engineers) and selecting appropriate access control models for complex scenarios (a skill required for security architects). Students who find these questions challenging should revisit the MITRE ATT&CK Navigator web application (attack.mitre.org) and practice identifying techniques from technique descriptions.

As you complete this module, remember that cybersecurity foundations are not merely introductory concepts to be left behind as you advance, they are the analytical vocabulary and framework lens you will apply throughout every subsequent topic in this curriculum, from network security and cryptography to cloud security and incident response. Every vulnerability you encounter will have a CVSS score and a CVE identifier. Every threat actor you analyze will have ATT&CK technique mappings. Every risk you assess will involve SLE and ALE calculations. Every control you design will serve one or more CIA properties. Return to these foundations often.
:::

%%%

---
unit: Summary
code: SUM
title: Summary & Foundations Checklist
---
:::pullquote
Cybersecurity is a continuous process of risk management. By protecting assets using the CIA triad, threat modeling with STRIDE, evaluating vulnerabilities via CVSS, and implementing Defense-in-Depth, security professionals build resilient systems that support the business objectives.
:::

::::columns
::col::
:::list heading="Foundational Milestones for This Course" style=chips
- 1. Understand Security Goals (CIA + Parkerian Hexad)
- 2. Map Assets & Classify Sensitivity (ISO 27001)
- 3. Identify Threats & Actors (STRIDE + MITRE ATT&CK)
- 4. Analyze Vulnerabilities & Risk (CVSS + NIST SP 800-30)
- 5. Define Control Strategies (Defense-in-Depth & Zero Trust)
:::
::col::
:::table
| Milestone | Framework/Standard | Purpose |
|-----------|--------------------|---------|
| Security Goals | CIA Triad, Parkerian Hexad | Define what needs protection and why |
| Asset Mapping | ISO 27001, NIST SP 800-53 | Identify and classify organizational resources |
| Threat Modeling | STRIDE, MITRE ATT&CK | Understand attacker perspectives and tactics |
| Vulnerability & Risk Analysis | CVSS, NIST SP 800-30 | Quantify risk and prioritize remediation |
| Control Implementation | NIST CSF, Zero Trust | Apply layered and adaptive defenses |
:::
:::
::::

:::image src="images/01_security_foundations_mindmap.png" alt="Mind map of cybersecurity foundations showing the CIA triad at center, branching to assets, threats, vulnerabilities, risk, controls, and professional roles" caption="Cybersecurity foundations mind map: the CIA triad anchors all downstream security concepts, from asset taxonomy and threat modeling to CVSS-based risk assessment and control implementation" width=full
:::

:::notes
In this foundational module, we have established the core principles that underpin all cybersecurity practices. These principles are not merely theoretical, they constitute the operational vocabulary and analytical framework that security professionals use daily to make risk-based decisions, justify security investments, and communicate with business leaders, regulators, and technical teams.

At the heart of cybersecurity lies the CIA triad, Confidentiality, Integrity, and Availability, which serves as the baseline for defining security goals. Every security control, policy, and investment ultimately traces back to protecting one or more of these properties. The Parkerian Hexad extends this model by introducing Possession (physical control over information), Authenticity (verified origin and identity), and Utility (usability of information), offering a more granular framework for evaluating security requirements in contexts where the traditional triad is insufficient, such as preventing unauthorized copying of encrypted data (a possession violation even without decryption) or detecting data corruption that does not affect availability (a utility violation).

Asset identification and classification are critical first steps in any risk management program. Standards like ISO/IEC 27001 provide structured methodologies for cataloging information assets, data, software, hardware, people, and services, and classifying them by sensitivity (Public, Internal, Confidential, Restricted, Secret). This classification drives every downstream security decision: encryption requirements, access control policies, audit log retention periods, and disposal procedures are all determined by an asset's classification. Without a current and accurate asset inventory, organizations are effectively defending an unknown perimeter against unknown adversaries, a fundamentally untenable position.

Threat modeling frameworks such as STRIDE systematically identify potential threats organized around violated security properties, while MITRE ATT&CK provides a comprehensive, empirically grounded knowledge base of real-world adversary tactics, techniques, and procedures. Together, these frameworks transform abstract risk concepts into specific, actionable intelligence about where and how attacks are likely to occur. The CVSS scoring system then enables organizations to quantify vulnerability severity in a standardized, comparable format, bridging the gap between technical vulnerability disclosure and business risk prioritization. NIST SP 800-30's quantitative risk methodology (SLE, ARO, ALE) further enables economic analysis of risk treatment options, ensuring that security spending is proportional to documented, quantified risk.

Defensive strategies such as Defense-in-Depth and Zero Trust Architecture ensure that security is resilient against sophisticated, multi-stage attacks. These models emphasize redundancy, segmentation, continuous validation, and least-privilege access, principles that are essential in modern threat landscapes where perimeter defenses alone are insufficient against supply chain attacks, insider threats, and cloud-native attack surfaces. The BCP/DR framework completes the resilience picture by ensuring that when controls fail, as they inevitably will, the organization can restore operations within defined RTO and RPO objectives, maintaining business continuity while the incident response team eradicates the threat.

The case studies of WannaCry and SolarWinds demonstrate that these foundational principles are not academic abstractions but directly predictive of real-world security outcomes. WannaCry devastated organizations that failed to apply basic patch management (a Protect function failure) and lacked network segmentation (a defense-in-depth failure). SolarWinds compromised organizations that trusted vendor-signed software without continuous behavioral monitoring (a Detect function failure) and lacked Zero Trust segmentation that would have limited post-compromise lateral movement.

Finally, the professional roles discussed in this class, SOC Analysts, Penetration Testers, Security Engineers, Incident Responders, GRC Analysts, Threat Intelligence Analysts, and CISOs, represent the human dimension of cybersecurity: the practitioners who apply these frameworks, operate these tools, and make these decisions every day. Understanding how these roles interact within a mature security program provides the organizational context needed to appreciate why technical skills alone are insufficient, collaboration, communication, and a shared security culture are equally essential.

This integrated approach, goals, assets, threats, vulnerabilities, risk, controls, and people, forms the architecture of all subsequent topics in the course, including network security, cryptography, access control, incident response, and security operations. As complexity and specificity increase in later modules, students should continually return to these foundational concepts as the interpretive lens through which every technical and organizational security decision is made.
:::
