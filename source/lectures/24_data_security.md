---
deck:
  title: Data Security
  kicker: Class 24
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 24
  description: Data classification models, the three states of data, backup architectures, DLP, and media sanitization standards.
  topics: [Data Classification, States of Data, Backups, Data Loss Prevention, Media Sanitization]
---

%%%
---
title: Data Security
cover: true
---
:::text class=sub
Information Lifecycle Protection: Classification, State Controls, Backup Redundancy, DLP, and Sanitization
:::
:::list style=chips
- Government vs. Corporate Classification
- Data Rest/Transit/Use States
- 3-2-1 Backup Strategy
- NIST SP 800-88 Media Sanitization
:::

%%%
---
unit: Classification
code: CLS
title: Data Classification Frameworks
---
:::callout style=soft
**Data classification** is the systematic categorization of data based on its sensitivity and the potential impact of its unauthorized disclosure. It forms the basis for implementing proportional security controls.
:::

::::columns ratio=1:1
::col::
::::card heading="Corporate Data Classification Model"
:::list style=tight
- **Restricted (Critical)**: High impact if compromised (e.g., trade secrets, SSNs, credit card numbers, intellectual property).
- **Confidential**: Moderate-to-high impact (e.g., customer records, employee salaries, legal contracts).
- **Internal**: Low-to-moderate impact (e.g., internal wikis, organizational charts, company policies).
- **Public**: No negative impact (e.g., marketing brochures, press releases, public websites).
:::
::::
::col::
::::card heading="Government & Military Classification"
:::list style=tight
- **Top Secret**: Exceptionally grave damage to national security if disclosed.
- **Secret**: Serious damage to national security.
- **Confidential**: Identifiable damage to national security.
- **Unclassified**: General data, though may be marked as *Controlled Unclassified Information (CUI)*.
:::
::::
::::

:::image src="images/24_classificationframeworks.png" alt="Side-by-side comparison of corporate and government data classification tiers" caption="Corporate vs. Government data classification models" width=full
:::

:::notes
Data security operates on the fundamental principle that not all data is created equal. Applying maximum security controls to all information within an organization is economically and operationally infeasible. Therefore, we must establish a data classification framework. Data classification, as defined by standards like ISO/IEC 27001 and NIST SP 800-53, is the process of sorting data into categories based on the risk of exposure.

In the corporate world, classification models typically use four tiers. Restricted data is the most sensitive; a breach of this data could cause catastrophic financial loss or regulatory penalties under frameworks like GDPR or HIPAA. Public data is at the opposite end, requiring no confidentiality controls. 

In the government and military sectors, classification is governed by executive orders and focuses on national security. The tiers, Top Secret, Secret, Confidential, and Unclassified, are legally defined, and access requires specific security clearances and a verified "need to know." Regardless of the framework, classification is the critical first step. You cannot protect your data until you know what data you have, where it is stored, and how sensitive it actually is.

A hospital patient record can fall into different categories under corporate and government classification models, which shows that classification labels vary between frameworks even for the same underlying data.
:::

%%%
---
unit: Data States
code: STA
title: The Three States of Data and Technical Controls
---
:::callout style=soft
Data exists in three distinct states within an information system. Each state exposes data to unique threats and requires specific cryptographic and architectural controls.
:::

::::columns ratio=1:3
::col::
::::card heading="Data at Rest"
:::list style=tight
- **Definition**: Data stored persistently on physical media.
- **Threats**: Device theft, unauthorized access, database cloning.
- **Controls**: Full Disk Encryption (FDE), Transparent Data Encryption (TDE), File-level encryption.
:::
::::
::col::
::::card heading="Data in Transit"
:::list style=tight
- **Definition**: Data traversing a local or wide area network.
- **Threats**: Eavesdropping, man-in-the-middle (MitM) attacks, packet capture.
- **Controls**: Transport Layer Security (TLS), IPsec VPNs, Secure Shell (SSH).
:::
::::
::col::
::::card heading="Data in Use"
:::list style=tight
- **Definition**: Data actively residing in volatile memory (RAM) or CPU cache during processing.
- **Threats**: Memory scraping malware, side-channel attacks, core dumps.
- **Controls**: Secure Enclaves (e.g., Intel SGX), Homomorphic Encryption, secure coding.
:::
::::
::::

:::image src="images/24_threestatesofdata.png" alt="Diagram of data flowing between rest, transit, and use states with associated controls" caption="The three states of data and their respective technical controls" width=full
:::

:::notes
Data is dynamic, and its protection must adapt to its state. We identify three distinct states: data at rest, data in transit, and data in use.

Data at rest refers to files and records sitting on a storage medium, such as a solid-state drive, backup tape, or cloud storage bucket. The primary threat here is unauthorized access via physical theft or logical intrusion. To protect data at rest, we implement encryption. This can be done at the physical layer using Full Disk Encryption (FDE), such as BitLocker, or at the application layer using database Transparent Data Encryption (TDE).

Data in transit, or data in motion, is actively moving across network lines. If an attacker can intercept this traffic, they can read or modify it. We defend data in transit using cryptographic protocols. TLS (RFC 5246) is the standard for web traffic, while IPsec is used to secure network-to-network connections in VPNs.

The most challenging state is data in use. Traditionally, to process data (like calculating a credit card transaction), the CPU had to decrypt the data into volatile memory (RAM), exposing it to memory-scraping attacks. Modern mitigations include Secure Enclaves, which isolate data in a hardware-protected CPU enclave, and Homomorphic Encryption, a mathematical technique that allows computations on encrypted data without ever decrypting it.

The 2013 Target breach is a classic data-in-use compromise: RAM-scraping malware on point-of-sale terminals captured card numbers in the fraction of a second they existed unencrypted in memory. Data in use is the hardest of the three states to protect because it must be in cleartext to be processed.
:::

%%%
---
unit: Data Redundancy
code: BAK
title: Backup Architectures and the 3-2-1 Rule
---
:::callout style=soft
A **backup** is a redundant copy of data maintained to recover from data loss due to system failure, human error, disaster, or ransomware. The industry-standard architecture for backups is the **3-2-1 Rule**.
:::

::::columns ratio=1:1
::col::
::::card heading="The 3-2-1 Backup Rule"
:::steps
1. **Three (3) Copies**: Maintain one primary production copy and at least two backup copies.
2. **Two (2) Media Types**: Store backups on two distinct types of physical media (e.g., SSD, NAS, Cloud, or LTO Tape) to prevent common-mode hardware failures.
3. **One (1) Offsite Location**: Keep at least one backup copy offsite, logically isolated (immutable/offline) to defend against ransomware propagation.
:::
::::
::col::
:::table
| Backup Type | Description | Backup Speed | Recovery Speed | Storage Space |
|---|---|---|---|---|
| **Full** | Copies all selected data blocks. | Slowest | Fastest | Highest |
| **Incremental** | Copies only blocks changed since the *last backup* (of any type). | Fastest | Slowest | Lowest |
| **Differential** | Copies all blocks changed since the *last full backup*. | Moderate | Moderate | Moderate |
:::
::::

:::image src="images/24_backuparchitecture.png" alt="Diagram showing the 3-2-1 backup rule with three copies on two media types and one offsite" caption="The 3-2-1 backup rule ensures resilience against hardware failure and ransomware" width=full
:::

:::notes
Backups represent the ultimate fallback. When preventative security controls fail, such as when ransomware bypasses host defenses and encrypts corporate files, the ability to recover data depends entirely on the backup architecture. 

To ensure resilience, organizations implement the 3-2-1 backup rule. This rule dictates that we keep three copies of data: the active copy and two separate backups. We store them on two different types of media, such as a local network-attached storage device and a cloud storage repository. This prevents a single hardware defect from destroying both backups. Crucially, at least one copy must be kept offsite or offline. In modern networks, ransomware actively searches for backup servers to encrypt them before locking the rest of the network. Having an offline or immutable (read-only) offsite backup ensures that there is always a clean copy out of the attacker's reach.

Organizations must also select a backup type. A full backup copies everything but takes the longest time and uses the most storage. An incremental backup only copies data that has changed since the last backup, making it fast but requiring a complex recovery chain. A differential backup copies everything that has changed since the last full backup, offering a middle ground in terms of backup speed and recovery complexity.

A common backup strategy combines a weekly full backup with daily incrementals: recovery needs the full plus every incremental since, which saves storage but lengthens and endangers recovery, a single corrupted incremental breaks the chain, whereas differential backups (each relative to the last full) would not.
:::

%%%
---
unit: Data Loss Prevention
code: DLP
title: Data Loss Prevention (DLP) Architecture
---
:::callout style=soft
**Data Loss Prevention (DLP)** systems detect, monitor, and block unauthorized movement or exfiltration of sensitive data. They operate at multiple points in the enterprise architecture.
:::

::::columns ratio=1:1
::col::
::::card heading="DLP Deployment Domains"
:::list style=tight
- **Endpoint DLP**: Runs as an agent on workstations and servers; monitors local activities such as copying data to USB drives, printing, or pasting into web browsers.
- **Network DLP**: Deployed at the network gateway; inspects outbound traffic (email, web, FTP) for sensitive data patterns.
- **Discovery DLP**: Scans corporate filesystems, databases, and cloud storage to locate and classify unstructured sensitive data at rest.
:::
::::
::col::
::::card heading="Data Inspection Techniques"
:::list style=tight
- **Pattern Matching**: Using regular expressions (Regex) to detect structured data like credit card numbers (e.g., Luhn algorithm checks) or Social Security Numbers.
- **Document Fingerprinting**: Generating cryptographic hashes of sensitive templates; the system blocks any file matching the hash or fragment.
- **Metadata Tagging**: Inspecting file properties for classification labels (e.g., "Confidential") added by users or classification tools.
:::
::::
::::

:::image src="images/24_dlparchitecture.png" alt="Diagram showing endpoint, network, and discovery DLP deployment points within an enterprise" caption="DLP systems monitor data at the endpoint, network boundary, and within storage" width=full
:::

:::notes
While firewalls prevent unauthorized inbound connections, Data Loss Prevention, or DLP, focuses on outbound data. DLP is designed to prevent data exfiltration, the unauthorized removal of sensitive data from the corporate boundary, which is a key phase in the cyber attack lifecycle (MITRE ATT&CK TA0010).

We deploy DLP across three domains. Endpoint DLP runs on employee laptops, monitoring interactions with local hardware. It can block an employee from dragging a file to a personal USB drive or uploading it to a personal webmail account. Network DLP sits at the egress points of the network, performing deep packet inspection to block outgoing emails or uploads that contain sensitive data. Discovery DLP performs search-and-index operations across corporate storage to find where sensitive data is stored, helping security teams verify that customer records are not sitting in unprotected folders.

To identify sensitive data, DLP uses sophisticated inspection techniques. Simple pattern matching looks for strings matching known formats, like credit card numbers. Fingerprinting goes further, taking a seed document (like a tax form template) and creating a signature of its structure, allowing the DLP system to detect if parts of that template are copied into another file.

DLP systems generate high alert volumes and so cause alert fatigue; policies must be tuned to reduce false positives. A nurse legitimately emailing patient data with authorization must not be blocked, which makes policy exceptions and workflows as important as the detection engine.
:::

%%%
---
unit: Media Sanitization
code: SAN
title: Media Sanitization Standards (NIST SP 800-88)
---
:::callout style=soft
**Media Sanitization** is the process of making data recovery from storage media impossible. The definitive standard is **NIST SP 800-88 Rev 1 (Guidelines for Media Sanitization)**, which outlines three sanitization categories.
:::

:::table
| Category | Definition | Application | Mechanism Examples |
|---|---|---|---|
| **Clear** | Logic techniques that sanitize data in user-addressable storage locations; protects against simple undelete tools. | Reusing media within the same security boundary. | Overwriting sectors with all zeros or random patterns; factory reset commands. |
| **Purge** | Physical or logical techniques that render data recovery infeasible using state-of-the-art laboratory techniques. | Reusing media outside the security boundary, or decommissioning. | **Degaussing** (demagnetizing magnetic disks); **Cryptographic Erase** (destroying the encryption key for self-encrypting drives). |
| **Destroy** | Physical destruction of the media rendering it completely unusable and unable to store data. | Decommissioning high-security drives; media cannot be reused. | **Disintegration**, **incineration**, **pulverization**, or **shredding** of the physical drive components. |
:::

:::image src="images/24_mediasanitization.png" alt="Table and diagram comparing Clear, Purge, and Destroy sanitization methods per NIST SP 800-88" caption="NIST SP 800-88 Rev 1 defines three tiers of media sanitization" width=full
:::

:::notes
Data security does not end when data is no longer actively used. Decommissioned computers, server hard drives, and mobile devices still contain fragments of data that can be recovered by an adversary if the storage media is not properly sanitized. This risk is addressed in detail by NIST Special Publication 800-88 Revision 1.

NIST SP 800-88 establishes three categories of media sanitization: Clear, Purge, and Destroy.

Clear is the most basic level, typically involving logical overwriting of data sectors. This is suitable when a computer is being transferred to another user within the same department. However, clearing does not guarantee defense against advanced laboratory data recovery.

Purging goes deeper, utilizing physical or logical actions that make recovery impossible even under a microscope. An example is degaussing, which uses a powerful magnetic field to erase magnetic disks. Another highly efficient purge method is Cryptographic Erase (CE). If a drive utilizes hardware-based encryption (a Self-Encrypting Drive), we can purge it instantly by securely destroying the master decryption key, rendering the remaining ciphertext permanently unrecoverable.

Destroy is the final tier. When media is obsolete, we physically shred, incinerate, or crush the drives, ensuring that no data recovery is physically possible.

NIST SP 800-88 is the media-sanitization standard referenced by many federal procurement contracts and required of federal agencies under FISMA. A company that sells old laptops without wiping them can incur liability under state breach-notification laws.
:::

%%%
---
unit: Classification
code: CLS
title: Data Ownership, Stewardship, and Custodianship
---
:::callout style=soft
Effective data governance requires clearly defined **roles** for managing data throughout its lifecycle. Three primary roles distribute accountability across the organization.
:::

::::columns ratio=1:1:1
::col::
::::card heading="Data Owner"
:::list style=tight
- A senior executive or business unit leader.
- Responsible for **deciding** the classification level and acceptable use.
- Authorizes access policies and bears ultimate accountability.
- Example: The Chief Marketing Officer for customer mailing lists.
:::
::::
::col::
::::card heading="Data Steward"
:::list style=tight
- A domain expert or manager within the business unit.
- Responsible for **implementing** classification decisions and maintaining data quality.
- Enforces access rules day-to-day and handles data requests.
- Example: The Marketing Manager who approves list exports.
:::
::::
::col::
::::card heading="Data Custodian"
:::list style=tight
- A technical role, typically in IT or Security Operations.
- Responsible for **safeguarding** data through technical controls (encryption, backups, access logs).
- Does not decide policy but implements it.
- Example: The DBA who encrypts the customer database.
:::
::::
::::

:::image src="images/24_dataownership.png" alt="Diagram showing the relationship between data owner, steward, and custodian roles" caption="Data governance roles distribute accountability from business decisions to technical implementation" width=full
:::

:::notes
One of the most common failures in data security programs is the absence of clear accountability. When no one "owns" a dataset, no one is responsible for protecting it. To solve this, modern data governance frameworks, including those aligned to ISO/IEC 38505 and NIST SP 800-53 Control PM-5, define explicit roles.

The Data Owner is a business-side executive who understands the strategic value and risk of the data. They make the call on what classification label a dataset receives and who should be allowed to access it. They are ultimately accountable if a breach occurs due to a flawed policy decision. Importantly, the Data Owner does not usually touch the data technically, they set policy.

The Data Steward is the operational implementer of the owner's policies. They manage access request queues, perform periodic access reviews, and ensure the data remains accurate and properly labeled. If an employee changes departments and should lose access to a sensitive database, the steward is responsible for initiating that change.

The Data Custodian is the IT or security professional who implements the technical controls: setting up database encryption, configuring access control lists, running backup jobs, and monitoring access logs. The custodian follows the owner's policy but has no authority to change it.

This three-way separation of duties is critical. Without it, a single IT administrator could both set policy and implement it, creating an unchecked opportunity for insider misuse or negligence. NIST SP 800-53 Rev 5 Control AC-5 (Separation of Duties) directly addresses this risk.

Data roles map to a bank vault: the owner (bank president) decides who may access it and under what conditions, the steward (branch manager) checks identities and approves requests, and the custodian (security guard) operates the door and logs every entry. All three are required and none replaces another.
:::

%%%
---
unit: Classification
code: CLS
title: Building a Data Inventory and Asset Register
---
:::callout style=soft
You cannot classify or protect data you do not know exists. A **data inventory**, also called a data asset register, is the foundational record of what data an organization holds, where it lives, and who is responsible for it.
:::

:::steps
1. **Discovery**: Use automated scanning tools (e.g., DLP discovery mode, cloud security posture management tools) to locate data across all systems, servers, endpoints, SaaS apps, and shadow IT.
2. **Classification**: Apply classification labels to each discovered dataset based on sensitivity and regulatory category (PII, PHI, PCI, IP).
3. **Mapping**: Record the data flow, where does data originate, where does it move, and where does it rest? Produce a Data Flow Diagram (DFD).
4. **Ownership Assignment**: Assign a Data Owner, Steward, and Custodian to each dataset.
5. **Review**: Schedule periodic reviews (at minimum annually) to identify new data types, moved data, or changed risk levels.
:::

:::image src="images/24_datainventory.png" alt="Flowchart showing the five steps of building a data inventory from discovery to review" caption="A data inventory lifecycle: discover, classify, map, assign, and review" width=full
:::

:::notes
The GDPR Article 30 requirement for Records of Processing Activities (RoPA) and the NIST Cybersecurity Framework (CSF) Identify function (ID.AM) both mandate that organizations know what data they hold. This sounds obvious, but in practice most large organizations have significant "dark data", data stores that IT and security teams do not know about, often created by business units using shadow IT tools like personal cloud storage or unauthorized SaaS applications.

The first step is discovery. Automated tools scan network shares, cloud storage buckets, email archives, and endpoint file systems, looking for patterns that indicate sensitive data, Social Security Numbers, credit card numbers, health record identifiers. This is exactly the Discovery DLP function we discussed earlier, used here in an inventorying context rather than a blocking context.

Once data is discovered, it must be classified and tagged. Modern data governance platforms like Microsoft Purview or AWS Macie use machine learning models to auto-classify data with high accuracy, reducing the manual burden significantly.

Data flow mapping is often neglected but critically important. Under GDPR, organizations must document not just where data sits, but how it moves, from collection at a web form, through processing in a CRM, to archiving in cloud storage. Each step in that flow is a potential exposure point.

Finally, ownership must be assigned so that when a policy question or a breach occurs, there is a named person accountable. Data inventories are living documents; they degrade quickly without scheduled reviews. NIST SP 800-53 Rev 5 Control CM-8 (System Component Inventory) and PM-5 (System Inventory) provide the formal control references for this process.

Few organizations have truly mapped their data landscape even when regulation requires it: asking where student data lives and who its owner is usually reveals that no one can name the owner.
:::

%%%
---
unit: Data States
code: STA
title: Encryption at Rest, Deep Dive
---
:::callout style=soft
Encrypting data at rest is the primary defense against physical theft and unauthorized logical access to storage systems. Multiple layers of encryption can be applied depending on the risk profile.
:::

:::table
| Encryption Layer | Where Applied | Example Technology | Protects Against |
|---|---|---|---|
| **Full Disk Encryption (FDE)** | Physical drive / volume | BitLocker (Windows), FileVault (macOS), dm-crypt (Linux) | Stolen laptop / drive |
| **Database Transparent Data Encryption (TDE)** | Database engine level | SQL Server TDE, Oracle TDE, PostgreSQL pgcrypto | Database file theft, unauthorized DBA |
| **File / Object Level Encryption** | Individual files or objects | AWS S3 SSE-KMS, Azure Blob Encryption, PGP | Per-file access control, cloud breach |
| **Application-Level Encryption** | Application code | AES-256 in application logic before DB write | Even DBAs cannot read plaintext |
:::

:::image src="images/24_encryptionatrest.png" alt="Layered diagram showing full disk, database, file, and application-level encryption stacked on a storage system" caption="Multiple layers of at-rest encryption address different threat vectors" width=full
:::

:::notes
When we say "encrypt data at rest," we are not describing a single solution, we are describing a strategy that can be implemented at multiple layers of the storage stack, each defending against a different adversary profile.

Full Disk Encryption (FDE) operates at the lowest layer. Tools like Microsoft BitLocker use the Trusted Platform Module (TPM) chip to tie the encryption key to the hardware. If a drive is physically removed from a stolen laptop and connected to another machine, the data remains encrypted and unreadable, the TPM will not release the key to a different host. NIST SP 800-111 provides guidance specifically on FDE for laptops and mobile devices.

Database Transparent Data Encryption (TDE) operates at the database engine layer. The database files on disk are encrypted, so an attacker who obtains a raw copy of the database files (e.g., by cloning an S3 bucket containing a database backup) cannot open them without the encryption key. Importantly, authorized database applications can still read and write data seamlessly, hence the word "transparent."

File or object-level encryption, common in cloud environments, applies encryption to each individual object or file. AWS S3 with SSE-KMS encrypts each object with a unique key managed by the AWS Key Management Service, and access to that key can be audited and revoked independently.

Application-level encryption is the strongest form, the application itself encrypts data before writing it to the database. This means even a database administrator with full DB privileges sees only ciphertext. This is the approach used by end-to-end encrypted messaging services.

The follow-up to any encryption decision is where the keys are stored. Storing the key with the encrypted data, like putting the safe key inside the safe, defeats the purpose. Key Management Systems and Hardware Security Modules separate key storage from data storage; NIST SP 800-57 Part 1 covers the key-management lifecycle.
:::

%%%
---
unit: Data States
code: STA
title: Encryption in Transit, TLS Deep Dive
---
:::callout style=soft
**Transport Layer Security (TLS)** is the cryptographic protocol that secures data in transit across the internet and private networks. Understanding its handshake process is essential for diagnosing security failures and misconfigurations.
:::

:::flow
TLS Handshake
Client Hello (supported cipher suites, TLS version)
Server Hello (chosen cipher suite, certificate)
Certificate Validation (CA chain verification)
Key Exchange (ECDHE generates shared session key)
Finished (encrypted application data begins)

:::

::::columns ratio=1:1
::col::
::::card heading="TLS Versions and Security"
:::list style=tight
- **TLS 1.3** (RFC 8446, 2018): Current standard. Eliminates weak ciphers; 1-RTT handshake; mandatory Perfect Forward Secrecy.
- **TLS 1.2** (RFC 5246, 2008): Still widely used; secure when properly configured (disable RC4, 3DES, export ciphers).
- **TLS 1.0 / 1.1**: Deprecated by RFC 8996 (2021). Vulnerable to BEAST and POODLE attacks. Must be disabled.
- **SSL 2.0 / 3.0**: Obsolete and critically vulnerable (DROWN, POODLE). Never use.
:::
::::
::col::
::::card heading="Common TLS Misconfigurations"
:::list style=tight
- Allowing deprecated protocol versions (TLS 1.0/1.1).
- Using weak cipher suites (RC4, 3DES, NULL).
- Expired or self-signed certificates accepted without warning.
- Missing certificate revocation checking (OCSP/CRL).
- Failing to enforce HSTS (HTTP Strict Transport Security).
:::
::::
::::

:::image src="images/24_tlshandshake.png" alt="Diagram of the TLS 1.3 handshake sequence showing client hello, server certificate, and session key exchange" caption="The TLS 1.3 handshake establishes an encrypted channel in a single round trip" width=full
:::

:::notes
Every time you visit an HTTPS website, open a banking app, or send an email through a corporate mail server, TLS is the technology protecting your data in transit. It is the most widely deployed data security control in existence, yet misconfigurations are one of the most common findings in security assessments.

The TLS handshake is the negotiation phase before any application data is exchanged. In TLS 1.3, this was streamlined to a single round trip (1-RTT), compared to the two round trips required by TLS 1.2. The client announces what cipher suites and TLS versions it supports. The server selects the best mutual option and presents its digital certificate, which the client validates against a trusted Certificate Authority (CA) chain. A shared session key is derived using Elliptic Curve Diffie-Hellman Ephemeral (ECDHE) key exchange, which provides Perfect Forward Secrecy, meaning that even if the server's private key is later compromised, past sessions cannot be decrypted.

TLS 1.0 and 1.1 were formally deprecated by RFC 8996 in March 2021. They are vulnerable to the BEAST attack (CVE-2011-3389) and the POODLE attack (CVE-2014-3566). PCI DSS 3.2 mandated the disabling of TLS 1.0 for cardholder data environments. SSL 3.0 and earlier are completely broken and must never be used.

Common misconfigurations include allowing legacy protocol fallback, which an attacker can exploit using a downgrade attack, forcing the connection to use a weaker protocol. Another frequent issue is accepting self-signed certificates, browsers warn about these, but applications and automated scripts often suppress these warnings, creating man-in-the-middle vulnerabilities.

Public TLS scanners grade a server's configuration in seconds, and major websites occasionally receive grades of C or below for poor TLS hygiene, which shows that correct TLS configuration is not automatic even at large organizations.
:::

%%%
---
unit: Data States
code: STA
title: Data in Use, Secure Enclaves and Confidential Computing
---
:::callout style=soft
**Confidential Computing** is an emerging paradigm that protects data while it is actively being processed, the historically unprotected "data in use" state. It uses hardware-enforced **Trusted Execution Environments (TEEs)**.
:::

::::columns ratio=1:1
::col::
::::card heading="How Secure Enclaves Work"
:::steps
1. Application requests a secure enclave from the CPU (e.g., Intel SGX ECREATE instruction).
2. CPU allocates a protected region of memory (Enclave Page Cache) that even the OS kernel and hypervisor cannot read.
3. Sensitive code and data are loaded into the enclave and verified via a cryptographic measurement (attestation).
4. Processing occurs inside the enclave. Output is returned encrypted.
5. Remote attestation allows a third party to verify the enclave's integrity before sending sensitive data.
:::
::::
::col::
::::card heading="Confidential Computing Technologies"
:::list style=tight
- **Intel SGX** (Software Guard Extensions): CPU-level enclaves; 128MB–1TB protected memory.
- **AMD SEV** (Secure Encrypted Virtualization): Encrypts entire VMs; useful for confidential cloud VMs.
- **ARM TrustZone**: Mobile/embedded secure world; used in mobile banking apps and DRM.
- **Homomorphic Encryption**: Mathematical approach; compute on ciphertext without decryption. Still computationally expensive.
:::
::::
::::

:::image src="images/24_secureenclaves.png" alt="Diagram of a CPU with a secure enclave region isolated from OS and hypervisor, with encrypted data flowing in and out" caption="Secure enclaves create CPU-enforced memory regions that even the operating system cannot access" width=full
:::

:::notes
The third state of data, data in use, has historically been the weakest link in the security chain. To process data, a CPU must have access to plaintext values. If an attacker can access the system's RAM (through memory scraping malware, a hypervisor vulnerability, or physical cold-boot attacks), they can read that plaintext data, regardless of how well it was encrypted at rest or in transit.

Confidential Computing addresses this gap using hardware-enforced Trusted Execution Environments, or TEEs. These are regions of the CPU that are cryptographically isolated from the rest of the system. The key insight is that the isolation is enforced at the silicon level, even a fully compromised operating system or cloud hypervisor cannot read the contents of an active enclave.

Intel's Software Guard Extensions (SGX) is the most widely known implementation. An application creates an enclave, loads sensitive code and data into it, and then performs a cryptographic attestation, a process where the CPU signs a measurement of the enclave's contents, proving to a remote verifier that the correct, unmodified code is running in a genuine Intel SGX environment. Cloud providers like Microsoft Azure (via Azure Confidential Computing) and AWS (via AWS Nitro Enclaves) now offer TEE-based instances.

AMD's Secure Encrypted Virtualization (SEV) takes a different approach, encrypting entire virtual machine memory regions with keys that are unique to each VM and stored only in the CPU, the cloud provider's hypervisor literally cannot read tenant VM memory. This is increasingly important for regulated industries that need to process sensitive data in multi-tenant cloud environments.

Homomorphic Encryption represents the theoretical ideal: performing mathematical operations directly on ciphertext, with results that decrypt to the same answer you would have gotten processing plaintext. Practical fully homomorphic encryption (FHE) schemes exist today (e.g., Microsoft SEAL, IBM HElayers) but remain computationally expensive, thousands of times slower than plaintext processing, limiting their current use to specific high-value use cases.

Heartbleed (CVE-2014-0160, 2014) was a data-in-use attack needing no enclave: a buffer over-read in OpenSSL let an attacker read 64KB chunks of active server memory, potentially capturing private keys, session tokens and plaintext passwords. Secure enclaves would have limited the blast radius.
:::

%%%
---
unit: Classification
code: CLS
title: Case Study, Capital One Data Breach (2019)
---
:::callout style=soft
**Real-World Breach**: In July 2019, Capital One disclosed a breach affecting approximately **106 million customers** in the United States and Canada. The attacker exfiltrated credit card application data stored in Amazon S3 cloud buckets.
:::

::::columns ratio=1:1
::col::
::::card heading="Attack Chain"
:::steps
1. **SSRF Vulnerability**: Attacker exploited a Server-Side Request Forgery (SSRF) flaw in a misconfigured AWS Web Application Firewall (WAF).
2. **Credential Theft**: SSRF was used to query the AWS EC2 Instance Metadata Service (IMDS), stealing temporary IAM role credentials.
3. **Privilege Abuse**: The stolen IAM credentials had excessive S3 ListBuckets and GetObject permissions.
4. **Data Exfiltration**: Attacker listed and downloaded 30+ S3 buckets containing sensitive PII and credit data.
:::
::::
::col::
::::card heading="Data Security Failures"
:::list style=tight
- **Excessive Permissions**: IAM role had far broader S3 access than the application required (violated least privilege).
- **No DLP on S3 Exfiltration**: Bulk download of 30 buckets was not detected in real time.
- **Insufficient Network Egress Controls**: The WAF was internet-facing with no egress filtering for outbound metadata requests.
- **Delayed Detection**: Breach occurred in March 2019; Capital One was not notified until July 2019 via a responsible disclosure report.
:::
::::
::::

:::image src="images/24_capitalonebreachdiagram.png" alt="Attack chain diagram for the Capital One 2019 breach showing SSRF to IMDS credential theft to S3 exfiltration" caption="The Capital One breach followed a three-step chain: SSRF → credential theft → cloud data exfiltration" width=full
:::

:::notes
The Capital One breach of 2019 is one of the most instructive cloud data security incidents on record. It illustrates how multiple individually manageable security gaps can chain together to produce a catastrophic data exposure, even in a major financial institution with a mature security program.

The attacker, Paige Thompson, had previously worked as a cloud engineer and possessed sophisticated knowledge of AWS architecture. She identified a misconfigured AWS WAF running on an EC2 instance. The WAF was vulnerable to Server-Side Request Forgery (SSRF), a class of vulnerability where an attacker tricks a server into making HTTP requests to internal resources on the attacker's behalf. SSRF is catalogued as CWE-918 and features prominently in the OWASP Top 10.

Thompson used the SSRF flaw to send a request to the EC2 Instance Metadata Service (IMDS), a special IP address (169.254.169.254) that provides AWS configuration details, including temporary IAM security credentials, to applications running on EC2. This is a well-known attack vector; AWS has since released IMDSv2, which requires session-oriented authentication and blocks simple SSRF-based metadata requests.

The retrieved IAM role credentials had been granted excessive permissions, violating the principle of least privilege. A WAF application should have no need to list or read S3 buckets containing customer credit applications. With those credentials, Thompson was able to enumerate and download the contents of more than 30 S3 buckets over several months.

From a data security control perspective, multiple layers failed simultaneously: no DLP was monitoring for bulk S3 GetObject activity, IAM permissions were overly broad, and the SSRF vulnerability was not caught in a WAF security review. The breach cost Capital One over $190 million in settlements and fines, and served as a catalyst for AWS releasing new security services like Amazon Macie for S3 data classification.

In the Capital One case, the attacker posted about the breach publicly on GitHub and Slack, which is how it was found and reported. This motivates monitoring public code repositories for leaked credentials and sensitive references, now automated by tools such as GitHub secret scanning.
:::

%%%
---
unit: Data Redundancy
code: BAK
title: Recovery Point Objective and Recovery Time Objective
---
:::callout style=soft
Two metrics define an organization's acceptable tolerance for data loss and system downtime during a recovery event. These metrics directly determine backup frequency and recovery architecture requirements.
:::

::::columns ratio=1:1
::col::
::::card heading="Recovery Point Objective (RPO)"
:::list style=tight
- **Definition**: The maximum acceptable amount of **data loss** measured in time. How old can recovered data be?
- **Example**: An RPO of 4 hours means backups must be taken at least every 4 hours; any data created in the last 4 hours may be lost in a recovery scenario.
- **Determines**: Backup frequency and replication requirements.
- **Low RPO** (minutes/seconds): Requires real-time replication or journaling; high cost.
:::
::::
::col::
::::card heading="Recovery Time Objective (RTO)"
:::list style=tight
- **Definition**: The maximum acceptable **downtime**, how long a system can be offline before recovery must be complete.
- **Example**: An RTO of 2 hours means the recovery process (restore, validate, bring online) must complete within 2 hours.
- **Determines**: Recovery infrastructure investment, hot/warm/cold standby architecture.
- **Low RTO** (minutes): Requires hot standby systems; high cost.
:::
::::
::::

:::table
| Tier | RPO | RTO | Architecture | Cost |
|---|---|---|---|---|
| Tier 1, Mission Critical | < 1 min | < 15 min | Active-active replication, hot standby | Very High |
| Tier 2, Business Critical | < 4 hours | < 4 hours | Warm standby, frequent incremental backups | High |
| Tier 3, Important | < 24 hours | < 24 hours | Daily full backups, cold standby | Moderate |
| Tier 4, Non-Critical | < 72 hours | < 72 hours | Weekly backups, no standby | Low |
:::

:::image src="images/24_rporto.png" alt="Timeline diagram showing RPO as the gap between last backup and failure, and RTO as the gap between failure and recovery" caption="RPO measures acceptable data loss; RTO measures acceptable downtime" width=full
:::

:::notes
Every organization has a different risk tolerance for data loss and system downtime. A hospital's electronic health records system and a marketing department's newsletter archive have vastly different business requirements. RPO and RTO provide the quantitative framework for translating business risk tolerance into concrete backup and recovery architecture decisions.

Recovery Point Objective, or RPO, answers the question: "How much data can we afford to lose?" It is measured in time, not in volume. An RPO of four hours means the organization is willing to lose up to four hours of transactions or changes. This directly sets the maximum interval between backup operations. If the backup runs at midnight and a system fails at 3:30 AM, four hours of data will be lost in recovery, which is exactly at the RPO boundary.

Recovery Time Objective, or RTO, answers the question: "How long can we afford to be offline?" For a financial trading platform, an RTO measured in hours could cost tens of millions of dollars in lost transactions and regulatory penalties. For an internal HR documentation system, an RTO of 24 hours might be perfectly acceptable. RTO drives decisions about standby infrastructure: a hot standby system (an identical, live replica that can take over in seconds) is required for low RTO, while a cold standby (a system that must be provisioned and restored before use) is appropriate for high RTO tolerances.

Together, RPO and RTO define the Tier of service required. Mission-critical systems (Tier 1) like payment processing engines typically demand sub-minute RPO and sub-15-minute RTO, requiring active-active replication across geographically distributed data centers. NIST SP 800-34 Rev 1 (Contingency Planning Guide for Federal Information Systems) provides detailed guidance on establishing RPO and RTO targets through Business Impact Analysis (BIA).

Lower RPO and RTO are not always better: a one-minute RPO for a petabyte-scale database requires continuous replication costing hundreds of thousands of dollars a year. The business impact analysis exists to decide whether the impact of downtime or data loss justifies that cost, which for many organizations it does not.
:::

%%%
---
unit: Data Redundancy
code: BAK
title: Backup Validation and the Untested Backup Problem
---
:::callout style=soft
**An untested backup is not a backup, it is a hope.** Organizations that have never validated their backup recovery process frequently discover failures only during an actual crisis, when time and resources are critically constrained.
:::

::::columns ratio=1:1
::col::
::::card heading="Why Backups Fail Silently"
:::list style=tight
- **Bit rot**: Storage media degrades over time; individual sectors become unreadable without warning.
- **Backup job errors**: Backup software may report "success" while silently skipping locked files (e.g., open databases).
- **Version incompatibility**: Backup software versions change; older backup archives may not be restorable with newer software.
- **Dependency drift**: A restored database backup may reference application configuration files that have since been deleted or changed.
- **Encryption key loss**: Encrypted backups become permanently unrecoverable if the key is lost.
:::
::::
::col::
::::card heading="Backup Validation Program"
:::steps
1. **Automated integrity checks**: Run scheduled hash verification of backup archives to detect bit rot or corruption.
2. **Tabletop exercises**: Periodically simulate a data loss event and walk through recovery procedures without executing them.
3. **Partial restore tests**: Monthly restoration of a random subset of files to verify archive readability.
4. **Full disaster recovery drills**: Quarterly or annual complete recovery of a system from backups in an isolated environment.
5. **Documentation**: Record recovery time achieved during tests vs. RTO target. Report gaps to management.
:::
::::
::::

:::image src="images/24_backupvalidation.png" alt="Checklist diagram showing backup validation steps from integrity checks to full disaster recovery drills" caption="A backup validation program ensures backups will function when they are actually needed" width=full
:::

:::notes
The cybersecurity industry has a well-worn saying: "You don't have a backup; you have a backup process. Whether you have a recovery is something you only find out when you need it." This captures a critically important concept that organizations routinely overlook.

Backup jobs report success at the job level, meaning the backup software successfully initiated and completed its process. This does not mean the resulting archive is usable. Locked files (such as open database files during a hot backup without proper database-aware backup agents) may be silently skipped. The backup log shows "success," but the database files are not actually in the archive.

Bit rot is another insidious failure mode. Storage media, even enterprise-grade tape and spinning disk, degrades at the individual bit level over years. A backup tape written in 2019 may be partially unreadable in 2024. Without periodic verification reads (also called integrity scrubbing), the organization does not know this until a recovery attempt fails.

NIST SP 800-34 Rev 1 formally requires that contingency plans be tested through structured exercises. The testing hierarchy moves from tabletop exercises (discussion-based, low risk) through functional exercises (simulating the process without actually failing over systems) to full-scale tests (complete failover to backup systems in a real environment). The key metric is comparing actual recovery time achieved during testing against the documented RTO.

One of the most catastrophic failure modes is encrypted backup key loss. If backups are encrypted (as they should be) but the encryption key is not separately backed up and controlled through a Key Management System, losing that key means losing all backups permanently, regardless of how many copies exist. NIST SP 800-57 Part 1 Rev 5 addresses key lifecycle management, including backup and escrow of cryptographic keys.

In the 2017 GitLab incident, an administrator accidentally deleted the primary production database during a DDoS response, and recovery revealed that all five backup systems had failed silently, for reasons including a wrong directory, a full disk, misconfigured replication and a process that was not running. It is a famous case study in backup validation failure: a backup is only real if its restoration has been tested.
:::

%%%
---
unit: Data Redundancy
code: BAK
title: Ransomware-Resistant Backup Architecture
---
:::callout style=soft
Modern ransomware variants specifically target backup systems before encrypting production data. A ransomware-resistant backup architecture requires **immutability**, **air-gapping**, and **offline isolation**.
:::

::::columns ratio=1:1
::col::
::::card heading="Ransomware Backup Attack Tactics"
:::list style=tight
- **VSS Deletion**: Ransomware deletes Windows Volume Shadow Copies (VSS) before encrypting, removing local recovery points.
- **Backup Server Targeting**: Malware scans the network for backup servers and encrypts them first.
- **Credential Harvesting**: Attackers steal backup service account credentials to authenticate to backup consoles and delete jobs.
- **Cloud Sync Propagation**: Infected/encrypted files replicate to connected cloud storage via sync clients, overwriting clean backups.
:::
::::
::col::
::::card heading="Ransomware-Resistant Architecture"
:::list style=tight
- **Immutable Backups**: Write-once storage where even the backup administrator cannot delete or modify archives (e.g., AWS S3 Object Lock in WORM mode, Veeam Hardened Repository).
- **Air-Gapped Backups**: Offline tape or disconnected storage media with no persistent network connection to production environment.
- **3-2-1-1-0 Rule**: Extends 3-2-1, adds **1** offline copy and **0** errors verified by automated testing.
- **Privileged Access Workstations (PAW)**: Manage backup systems only from hardened, isolated management hosts.
:::
::::
::::

:::image src="images/24_ransomwarebackup.png" alt="Diagram contrasting a traditional backup architecture vulnerable to ransomware with an immutable air-gapped architecture" caption="Ransomware-resistant backup architecture uses immutability and air-gapping to prevent attacker backup destruction" width=full
:::

:::notes
Ransomware is the primary threat driver behind modern backup architecture decisions. The criminal economics of ransomware depend on victims being unable to recover their data without paying, which means attackers have strong incentives to destroy backups before triggering the encryption payload. Modern ransomware families including LockBit, BlackCat (ALPHV), and Cl0p have all demonstrated sophisticated backup destruction capabilities.

The most common first step is VSS deletion. Windows Volume Shadow Copy Service maintains point-in-time snapshots of local volumes, which have historically been used for quick local recovery. Ransomware routinely executes commands like `vssadmin delete shadows /all /quiet` and `wmic shadowcopy delete` before encrypting. Defenders can partially mitigate this by restricting which accounts can execute VSS deletion and enabling VSS protection via Windows Defender.

Cloud sync services create a particularly dangerous backup failure mode. If a user stores "backups" in a folder synchronized to OneDrive or Dropbox, and ransomware encrypts those files, the sync client dutifully propagates the encrypted versions to the cloud, overwriting clean copies, often within minutes. This is why synchronized cloud storage does not constitute a proper backup unless the cloud service provides versioning with a retention window beyond the attacker's dwell time.

Immutable storage is the most effective architectural defense. AWS S3 Object Lock in WORM (Write Once, Read Many) mode prevents any user or application from deleting or modifying objects for a defined retention period, even an administrator with full AWS account credentials cannot override this during the lock period. Veeam's Hardened Repository for Linux achieves similar immutability using Linux immutable file attributes.

The 3-2-1-1-0 rule extends the classic 3-2-1 by adding an explicit requirement for one offline copy (protecting against networked ransomware propagation) and zero recovery errors (enforcing backup validation). CISA and the Multi-State Information Sharing and Analysis Center (MS-ISAC) both recommend this framework in their ransomware guidance documents.

In the 2021 Colonial Pipeline attack, the decision to shut down operational technology was driven partly by uncertainty about the integrity of data and systems. Confidence in backup and recovery, or the lack of it, directly shapes operational decisions at the highest levels of critical infrastructure.
:::

%%%
---
unit: Data Loss Prevention
code: DLP
title: DLP Policy Design and Tuning
---
:::callout style=soft
A DLP system is only as effective as its policy configuration. Poorly tuned DLP generates excessive false positives (alert fatigue) or false negatives (missed exfiltration), both of which undermine the security program.
:::

:::steps
1. **Define Scope**: Identify which data types require DLP monitoring (PII, PHI, PCI data, intellectual property). Reference the data classification inventory.
2. **Establish Baselines**: Audit normal data movement patterns for 30–60 days in monitor-only mode before enabling blocking rules.
3. **Author Detection Rules**: Combine pattern matching (regex), fingerprinting, and classification labels. Use AND/OR logic to reduce false positives.
4. **Set Response Actions**: Map sensitivity tiers to actions, log only (Internal data), alert + quarantine (Confidential), block + alert CISO (Restricted).
5. **Tune Iteratively**: Review false positive reports weekly for the first 90 days. Refine rules to reduce noise while maintaining coverage.
6. **Manage Exceptions**: Build an approved workflow for legitimate high-sensitivity data movements (e.g., legal counsel emailing contracts to external parties).
:::

:::image src="images/24_dlppolicydesign.png" alt="Flowchart showing the DLP policy lifecycle from scope definition through iterative tuning and exception management" caption="Effective DLP policy design is an iterative process requiring business context and regular refinement" width=full
:::

:::notes
One of the most common DLP deployment failures is enabling a DLP solution without adequate policy tuning, resulting in so many alerts that the security team stops reviewing them, a condition known as alert fatigue. Equally problematic is an overly permissive DLP configuration that allows genuine data exfiltration to pass undetected.

The key insight is that DLP is a process, not a product. The technology provides detection and enforcement mechanisms, but the policies that drive those mechanisms must be informed by deep knowledge of how the business legitimately uses sensitive data.

Beginning in monitor-only mode (sometimes called "learn" or "audit" mode) is critical. Before any blocking is enabled, the DLP system watches traffic and logs what it would have blocked. Security teams review these logs to identify legitimate business processes that would be falsely blocked, for example, a customer service team that regularly sends masked account numbers in support emails, or a payroll service that exports salary data to an external HR platform every Friday. These workflows must be accounted for in exception policies before blocking is activated.

Detection rule design requires combining multiple signals. A single credit card number pattern match in an email might be a false positive (someone discussing a transaction number in conversation). But 50 credit card numbers in a single email attachment, combined with a recipient outside the corporate domain and an absence of a classification label, is a much stronger signal. DLP systems that support compound rules using AND/OR logic significantly improve signal quality.

Response actions must be proportional. For data classified as Internal, logging the event for later audit review is typically sufficient. For Confidential data leaving the organization, automated quarantine and manager notification is appropriate. For Restricted data, immediate blocking and escalation to the CISO is warranted. NIST SP 800-53 Rev 5 Controls SI-12 (Information Management and Retention) and AC-4 (Information Flow Enforcement) provide the control framework underlying DLP policy design.

DLP in healthcare cannot be binary. A nurse emailing a patient's medication list to a specialist at another hospital is a legally required transfer, and a DLP system that blindly blocked all PHI from leaving the network would violate HIPAA's treatment, payment and operations exceptions and impair care. Policies must model legitimate business workflows.
:::

%%%
---
unit: Data Loss Prevention
code: DLP
title: "Case Study, DLP in Healthcare: HIPAA and Data Exfiltration"
---
:::callout style=soft
Healthcare organizations face unique DLP challenges. Protected Health Information (PHI) must flow freely among authorized care providers while being strictly controlled against unauthorized disclosure. Regulatory penalties under HIPAA can reach **$1.9 million per violation category per year**.
:::

::::columns ratio=1:1
::col::
::::card heading="HIPAA Security Rule DLP Requirements"
:::list style=tight
- **45 CFR §164.312(a)(1)**: Technical access controls must prevent unauthorized PHI access.
- **45 CFR §164.312(e)(1)**: Technical security measures must guard against unauthorized access to ePHI transmitted over electronic communications networks.
- **45 CFR §164.312(e)(2)(ii)**: Encryption of ePHI in transit is an addressable implementation specification (i.e., required unless an equivalent alternative is documented).
- **Breach Notification Rule**: Any impermissible disclosure of unsecured PHI triggers mandatory notification, to patients (60 days), to HHS, and for breaches over 500 individuals, to major media outlets.
:::
::::
::col::
::::card heading="Common Healthcare DLP Scenarios"
:::list style=tight
- **Email PHI to wrong patient**: Autocomplete sends lab results to the wrong John Smith. DLP with recipient domain and content policies can quarantine for review.
- **Bulk record access by a departing employee**: Privileged insider downloads 10,000 records before resigning. UEBA + DLP analytics detects anomalous volume access.
- **Medical device data exfiltration**: Connected medical devices log patient data to cloud services without IT knowledge. Discovery DLP identifies the unauthorized data store.
- **Ransomware targeting EHR systems**: Encrypted patient records disrupt care. Immutable backup and documented RTO/RPO prevent permanent data loss.
:::
::::
::::

:::image src="images/24_hippadlp.png" alt="Healthcare network diagram showing DLP controls for email, endpoint, and network protecting ePHI flows" caption="Healthcare DLP must balance patient care data sharing requirements with strict HIPAA confidentiality obligations" width=full
:::

:::notes
Healthcare is among the most heavily regulated sectors for data security, and it presents a fascinating tension: PHI must flow rapidly and freely among authorized care providers to support patient outcomes, while simultaneously being protected against any unauthorized disclosure. A DLP system calibrated too aggressively can impair life-critical care workflows; one calibrated too permissively creates massive regulatory liability.

HIPAA's Security Rule, codified in 45 CFR Part 164, establishes the minimum-security requirements for electronic Protected Health Information (ePHI). The technical safeguards section requires access controls, audit controls, integrity controls, and transmission security. DLP is a key technical control addressing transmission security.

The HIPAA Breach Notification Rule dramatically raises the stakes. Any impermissible use or disclosure of unsecured PHI, even an accidental misdirected email containing a single patient's record, is a reportable breach. For breaches affecting fewer than 500 individuals, the covered entity must notify HHS annually. For breaches over 500, individual patient notification within 60 days and prominent local media notice are required. The Office for Civil Rights (OCR) at HHS maintains a public "Wall of Shame" listing all breaches affecting 500 or more individuals, as of 2024, this list contains thousands of entries.

The Office for Civil Rights has levied significant financial penalties. In 2020, CHSPSC LLC (Community Health Systems) settled for $5 million following a breach affecting 6.1 million records caused by an APT group exploiting an Adobe Flash vulnerability (CVE-2014-0515). The failure to implement adequate technical safeguards, specifically, insufficient network monitoring and outdated software, was central to the settlement.

User and Entity Behavior Analytics (UEBA) plays a critical complementary role to traditional DLP in healthcare. While DLP monitors content patterns, UEBA monitors behavioral patterns, detecting, for example, a nurse who normally accesses 20 patient records per day suddenly downloading 5,000 records over a weekend. UEBA flagging triggers a DLP investigation that might confirm impermissible disclosure. The Anthem breach of 2015, which compromised 78.8 million records, was partially attributed to inadequate monitoring of privileged account access behavior.

HIPAA's public breach portal lists reported healthcare breaches by state, an unusual level of public disclosure most industries do not require. Whether such disclosure creates positive security incentives or mainly embarrasses organizations after the fact is a genuine policy question.
:::

%%%
---
unit: Media Sanitization
code: SAN
title: Degaussing, Deep Dive
---
:::callout style=soft
**Degaussing** is a Purge-level media sanitization technique that uses a powerful external magnetic field to randomize the magnetic domains on spinning hard disk drives (HDDs) and magnetic tape, rendering stored data permanently unrecoverable.
:::

::::columns ratio=1:1
::col::
::::card heading="How Degaussing Works"
:::list style=tight
- Magnetic storage (HDD, tape) stores data as polarized magnetic domains on a ferromagnetic coating.
- A degausser generates a rapidly alternating high-intensity magnetic field (measured in Oersteds, typically 10,000–20,000 Oe for modern hard drives).
- This field exceeds the coercivity (resistance to demagnetization) of the storage medium, randomizing all magnetic domains.
- Result: no data pattern remains; the drive returns to a near-virgin magnetic state.
:::
::::
::col::
::::card heading="Degaussing Limitations"
:::list style=tight
- **Does NOT work on SSDs or Flash Storage**: SSDs store data in electronic charge states, not magnetic domains. Degaussing has no effect on NAND flash memory, the data remains intact.
- **Renders HDDs permanently unusable**: Post-degaussing, the drive's firmware stored on the magnetic platters is also destroyed, making the drive unbootable and unrecognizable by the OS.
- **Must be verified**: NSA/CSS EPL (Evaluated Products List) requires verification testing to confirm field strength meets requirements for the media's coercivity rating.
:::
::::
::::

:::image src="images/24_degaussing.png" alt="Diagram showing magnetic domains on an HDD platter before and after degaussing, organized patterns versus randomized chaos" caption="Degaussing randomizes magnetic domains, permanently erasing all data and rendering the drive unusable" width=full
:::

:::notes
Degaussing is one of the most misunderstood sanitization techniques in practice, primarily because security professionals sometimes incorrectly assume it works on all types of storage media. Understanding when degaussing is appropriate, and critically, when it is not, is essential for any data security practitioner managing end-of-life media.

Spinning hard disk drives store data by magnetizing tiny regions of a ferromagnetic coating on rotating platters. The direction of magnetization (north or south pole orientation) represents binary 1s and 0s. A degausser generates an intense alternating magnetic field, typically produced by passing the drive through an electromagnetic coil. The field strength must exceed the coercivity rating of the specific media type being degaussed. Modern high-density HDDs have higher coercivity than older drives, requiring correspondingly more powerful degaussers.

The NSA maintains an Evaluated Products List (EPL) for degaussers, categorizing them for use with specific media types. Organizations handling classified information are required to use only NSA-listed degaussers for appropriate media. This ensures field strength is verified to meet NSA standards, not just claimed by the vendor.

The critical limitation is that degaussing is entirely ineffective against solid-state storage. SSDs, USB flash drives, SD cards, and eMMC storage all use NAND flash memory, which stores data as electrical charge in floating gate transistors. A magnetic field has no effect on electrical charge states. An organization that degausses a mixed batch of HDDs and SSDs assuming all media is now sanitized has a serious problem, the SSDs emerge from the degausser with all data intact.

For SSDs, NIST SP 800-88 Rev 1 recommends Cryptographic Erase (if the drive is a self-encrypting drive) or physical Destroy (disintegration to particles smaller than 2mm per NSA/CSS PM 9-12). Overwrite-based clearing is less effective on SSDs due to wear leveling algorithms that may preserve older data blocks in over-provisioned space.

Degaussing renders a magnetic drive permanently unusable by erasing its servo tracks, which is why a degaussed drive cannot simply be reformatted and reused. It applies only to magnetic media, not to flash-based SSDs, which require cryptographic erase or physical destruction instead.
:::

%%%
---
unit: Media Sanitization
code: SAN
title: Cryptographic Erase and Self-Encrypting Drives
---
:::callout style=soft
**Cryptographic Erase (CE)** is a Purge-level sanitization technique applicable to **Self-Encrypting Drives (SEDs)**. It works by permanently destroying the Media Encryption Key (MEK), rendering all data on the drive mathematically unrecoverable, instantly.
:::

:::flow
SED Write Path
Data enters drive
Hardware encryption engine applies MEK (AES
256)
Ciphertext written to NAND/platters
MEK stored in secure hardware register

:::

:::flow
Cryptographic Erase
Secure erase command issued
Drive firmware generates new random MEK
Old MEK overwritten and destroyed
All stored ciphertext is now permanently undecipherable

:::

::::columns ratio=1:1
::col::
::::card heading="Advantages of Cryptographic Erase"
:::list style=tight
- **Speed**: Near-instantaneous, no need to overwrite terabytes of data.
- **Completeness**: Eliminates concerns about wear-leveling hidden sectors on SSDs retaining data.
- **Drive reuse**: Unlike degaussing, the drive remains fully functional and reusable after CE.
- **NIST approval**: Recognized as Purge-level sanitization in NIST SP 800-88 Rev 1.
:::
::::
::col::
::::card heading="Requirements and Limitations"
:::list style=tight
- Drive must be a hardware-based Self-Encrypting Drive (SED) compliant with TCG Opal or FIPS 140-2/3.
- MEK must have been active at the time data was written (data written before encryption was enabled is NOT covered).
- Key management documentation must prove the old MEK is irretrievable.
- Not applicable to non-encrypting drives, software FDE (BitLocker) alone does not enable CE.
:::
::::
::::

:::image src="images/24_cryptographicerase.png" alt="Diagram contrasting the SED write path with encryption and the cryptographic erase key destruction process" caption="Cryptographic Erase destroys the encryption key, making stored ciphertext permanently unrecoverable without touching the data itself" width=full
:::

:::notes
Cryptographic Erase represents a fundamentally different approach to data sanitization. Rather than removing or overwriting the data itself, CE removes the ability to interpret the data by destroying the key that makes it meaningful. This is conceptually elegant and practically powerful, instead of a multi-hour overwrite operation against a 10-terabyte drive, cryptographic erase completes in milliseconds.

A Self-Encrypting Drive contains dedicated encryption hardware built into the drive controller. Every byte written to the drive is transparently encrypted using a 256-bit AES key called the Media Encryption Key (MEK), and every byte read is decrypted. This happens below the operating system level, the OS sees plaintext data as if it were stored unencrypted. The MEK is stored in a protected register within the drive's controller firmware, inaccessible to external software.

The Trusted Computing Group (TCG) Opal 2.0 specification and the IEEE 1667 standard define the interfaces and behaviors for SEDs in enterprise environments. FIPS 140-2 and FIPS 140-3 validated drives provide additional assurance that the cryptographic implementation has been independently tested.

When a secure erase command is issued to an SED, the drive firmware generates a new random MEK and overwrites the old one. At this point, the data stored on the platters or NAND cells still exists physically, but it is AES-256 ciphertext for which the key no longer exists anywhere in the universe. The expected time to brute-force a 256-bit AES key (approximately 2^256 operations) exceeds the age of the observable universe by an enormous margin. NIST classifies this as computationally infeasible recovery.

An important pre-condition is that the MEK must have been enabled before the data was written. Some organizations purchase SEDs but never configure a pre-boot authentication password, leaving the drive in an unlocked/passthrough state where data is not actually encrypted, making CE ineffective. Verify SED configuration during procurement and deployment.

Self-encrypting drives provide no protection if pre-boot authentication and encryption are never configured: in passthrough mode the data was never encrypted, so cryptographic erase is not valid remediation after theft. The "self-encrypting" label is meaningless without correct configuration, a common real-world failure.
:::

%%%
---
unit: Media Sanitization
code: SAN
title: Chain of Custody for Media Disposal
---
:::callout style=soft
Media sanitization is only trustworthy when combined with a documented **chain of custody**, a recorded sequence of control and accountability from the time a device is decommissioned until its final sanitization is verified and documented.
:::

:::steps
1. **Asset Identification**: Record the asset tag, serial number, model, and data classification level of media to be decommissioned. Cross-reference with the asset inventory.
2. **Sanitization Assignment**: Assign the appropriate NIST SP 800-88 sanitization category (Clear, Purge, Destroy) based on classification level and media type.
3. **Sanitization Execution**: Perform the sanitization operation using approved tools and methods. Record date, operator, tool/version, and method used.
4. **Verification**: Attempt post-sanitization data recovery using forensic tools to verify effectiveness. Document the result.
5. **Certificate of Destruction**: Issue a formal certificate documenting the sanitization details, verified by two parties (four-eyes principle).
6. **Disposal**: Transfer to approved recycler (R2 or e-Stewards certified) or physically destroy in-house. Retain disposal receipts.
:::

:::image src="images/24_chainofcustody.png" alt="Flowchart showing the six steps of media disposal chain of custody from decommission to verified disposal" caption="A documented chain of custody ensures media sanitization is auditable and legally defensible" width=full
:::

:::notes
Media sanitization without documentation is legally and operationally insufficient. If a regulatory audit or a legal discovery process requires an organization to prove that customer data was properly destroyed when a storage device was retired, verbal assurances are not acceptable. A documented chain of custody creates the evidentiary record that controls were applied correctly.

NIST SP 800-88 Rev 1 Section 4 explicitly recommends documenting the sanitization process with records that include the date sanitization was performed, the type of sanitization technique, the tool or equipment used, the serial number of the media, and the name of the individual performing the process. This documentation supports compliance with regulations such as GDPR Article 5(1)(e) (storage limitation and data integrity), HIPAA 45 CFR §164.310(d)(1) (device and media controls), and PCI DSS Requirement 9.8.

A Certificate of Destruction (CoD) is the formal artifact produced at the end of the chain. For third-party disposal vendors, requesting a CoD should be standard practice, it transfers documentation responsibility and creates a contractual record. Ensure that any third-party recycler holds either R2 (Responsible Recycling) or e-Stewards certification, which require documented data sanitization processes and auditable chain of custody.

The four-eyes principle, requiring two independent parties to witness and verify sanitization, is a critical control against fraud or negligence. A single employee could falsify a sanitization log; it is far harder for two independent parties to collude. This mirrors the dual-control principles used in financial transaction authorization and nuclear weapons safety systems.

High-security environments may require even more rigorous procedures: continuous video surveillance of the destruction area, third-party auditor presence during batch sanitization events, and weight measurement of shredded material to verify no drives were removed before destruction.

Without a chain-of-custody process, an organization retiring hundreds of workstations a year cannot prove that every drive was sanitized. A single drive with patient records surfacing for resale brings regulatory and reputational consequences, and the difficulty of proving it was isolated rather than systemic is exactly why documentation matters as much as the technical sanitization.
:::

%%%
---
unit: Regulatory Context
code: REG
title: GDPR Data Security Requirements
---
:::callout style=soft
The **EU General Data Protection Regulation (GDPR)** (Regulation 2016/679) establishes binding data security obligations for any organization processing personal data of EU residents, regardless of where the organization is located.
:::

::::columns ratio=1:1
::col::
::::card heading="Key GDPR Security Articles"
:::list style=tight
- **Article 5(1)(f), Integrity and Confidentiality**: Personal data shall be processed in a manner that ensures appropriate security, including protection against unauthorized access, disclosure, loss, or destruction (the "security principle").
- **Article 25, Data Protection by Design and by Default**: Security and privacy must be embedded into systems during design, not added afterward. Default settings must protect the maximum amount of privacy.
- **Article 32, Security of Processing**: Controllers must implement appropriate technical and organizational measures including pseudonymization, encryption, and regular testing of security measures.
- **Article 33/34, Breach Notification**: Breaches affecting personal data must be reported to supervisory authorities within 72 hours; individuals notified without undue delay when risk is high.
:::
::::
::col::
::::card heading="GDPR Security Measures (Article 32)"
:::list style=tight
- Pseudonymization and encryption of personal data.
- Ensuring ongoing confidentiality, integrity, availability, and resilience of processing systems.
- Ability to restore availability and access to personal data in the event of an incident.
- A process for regularly testing, assessing, and evaluating the effectiveness of technical and organizational security measures.
:::
::::
::::

:::image src="images/24_gdprsecurity.png" alt="Diagram mapping GDPR Articles 5, 25, 32, 33, and 34 to corresponding technical and organizational data security controls" caption="GDPR security obligations span data protection by design, encryption, incident response, and breach notification" width=full
:::

:::notes
GDPR is arguably the most influential data protection regulation in history. Since its enforcement began in May 2018, it has resulted in fines exceeding €4.5 billion in total, with individual fines reaching €1.2 billion (Meta, 2023, for unlawful EU-US data transfers). Any organization processing the personal data of European Union residents, regardless of whether the organization is based in the EU, is subject to GDPR's security requirements.

Article 5 establishes the foundational data protection principles, with 5(1)(f) specifically addressing security. It requires processing to ensure "appropriate security of personal data, including protection against unauthorized or unlawful processing and against accidental loss, destruction or damage." Critically, GDPR does not prescribe specific technologies, it requires that security be "appropriate" to the risk, leaving organizations to determine which controls satisfy this standard.

Article 25 introduces the concept of "Data Protection by Design and by Default." From a technical standpoint, this means security controls (encryption, access logging, pseudonymization) must be considered during the requirements and design phase of every system that handles personal data, not bolted on after deployment. Many breach investigations reveal that systems were built without security consideration and then failed to be adequately secured before go-live.

Article 32 is the primary technical security obligation. It explicitly lists pseudonymization and encryption as measures to consider, along with the CIA triad extended to resilience. The "regular testing" requirement directly motivates penetration testing programs, vulnerability management programs, and the backup validation exercises we discussed earlier.

The 72-hour breach notification requirement under Article 33 is operationally demanding. Organizations must have incident response plans and data breach notification workflows in place before a breach occurs, improvising a notification process while simultaneously managing the technical response and stakeholder communications in under 72 hours is extremely difficult.

After a 2018 Magecart attack injected malicious JavaScript into the British Airways booking site and exfiltrated customer payment data for two months, the ICO fined BA under GDPR Article 32 (originally £183 million, reduced to £20 million) for inadequate security, including insufficient monitoring of website code integrity.
:::

%%%
---
unit: Regulatory Context
code: REG
title: PCI DSS Data Security Requirements
---
:::callout style=soft
**PCI DSS** (Payment Card Industry Data Security Standard) is a contractual standard mandated by card brands (Visa, Mastercard, Amex, Discover) for any organization that stores, processes, or transmits **cardholder data**. Version 4.0 took effect in March 2024.
:::

:::table
| PCI DSS Requirement | Data Security Control | Key Technical Obligation |
|---|---|---|
| **Req 3, Protect Stored Account Data** | Encryption at rest | Primary Account Numbers (PAN) must be encrypted (AES-256) or tokenized; full card numbers must not be stored post-authorization. |
| **Req 4, Protect Cardholder Data in Transit** | Encryption in transit | Strong cryptography (TLS 1.2+) required for all PAN transmission over open, public networks. |
| **Req 7, Restrict Access** | Access control | Need-to-know access to cardholder data; principle of least privilege enforced. |
| **Req 9, Restrict Physical Access** | Physical security + media controls | Physical access to cardholder data systems controlled; media containing PAN sanitized per approved standards before disposal. |
| **Req 10, Log and Monitor** | Audit logging + DLP | All access to cardholder data logged; logs retained for 12 months with 3 months immediately available. |
| **Req 12, Security Policies** | Data classification | Cardholder data must be inventoried and classified; data flow diagrams required. |
:::

:::image src="images/24_pcidss.png" alt="Diagram of the PCI DSS Cardholder Data Environment with labeled control zones for encryption, access control, logging, and physical security" caption="PCI DSS v4.0 maps twelve requirements across the cardholder data environment to protect stored, transmitted, and accessed payment card data" width=full
:::

:::notes
PCI DSS exists because payment card fraud is a multi-billion dollar global problem, and the card brands established a contractual standard to elevate baseline security across all merchants and service providers that touch payment card data. Unlike GDPR, PCI DSS is not a law, it is a contractual obligation embedded in merchant agreements. However, non-compliance can result in card brand fines transmitted through acquiring banks, termination of the ability to process card payments (commercially devastating for most businesses), and mandatory forensic investigations following breaches at the organization's expense.

PCI DSS v4.0, which became mandatory in March 2024, introduced significant changes from version 3.2.1. Notably, it added a requirement for targeted risk analysis (TRA) to justify control timing decisions, expanded authentication requirements (Requirement 8.4 mandates MFA for all CDE access), and introduced new requirements around customized implementation, allowing organizations to satisfy the spirit of a requirement through alternative controls if they can demonstrate equivalent risk reduction. This is a significant conceptual shift from the prescriptive "do exactly this" approach of earlier versions.

Requirement 3 is particularly important for understanding data minimization. PCI DSS prohibits storing the full magnetic stripe data, CVV/CVC codes, and PINs after authorization, even in encrypted form. For stored PANs (the 16-digit card number), encryption or tokenization is required. Tokenization replaces the PAN with a non-sensitive substitute (a token) that has no mathematical relationship to the original PAN and is stored in a secure token vault. Tokens can be presented to the payment processor to retrieve the original PAN, but a breached merchant database containing only tokens yields no usable card data to an attacker.

Requirement 10's logging mandate directly addresses the MITRE ATT&CK technique T1070 (Indicator Removal), where attackers delete logs to cover their tracks. Immutable logging, sending audit logs to a write-protected, centralized SIEM, ensures that even if an attacker compromises a system, they cannot retroactively erase evidence of their access.

A small retailer processing a thousand card transactions a month self-certifies PCI DSS compliance through a Self-Assessment Questionnaire (SAQ-A or SAQ-A-EP, depending on how card data flows), while merchants above six million Visa transactions a year require annual on-site assessment by a Qualified Security Assessor.
:::

%%%
---
unit: Regulatory Context
code: REG
title: Regulatory Comparison, GDPR vs. HIPAA vs. PCI DSS
---
:::callout style=soft
Organizations frequently must comply with multiple data protection regulations simultaneously. Understanding how requirements overlap and differ helps prioritize security investment and avoid compliance gaps.
:::

:::table
| Dimension | GDPR | HIPAA | PCI DSS |
|---|---|---|---|
| **Jurisdiction** | EU residents' personal data (global applicability) | US healthcare providers, payers, and their business associates | Any organization processing Visa/Mastercard/Amex/Discover cards (global) |
| **Data Type** | All personal data (PII, behavioral, biometric, location) | Protected Health Information (PHI / ePHI) | Cardholder data (PAN, CVV, magnetic stripe, PIN) |
| **Legal Basis** | Regulation (EU law); fines enforced by national supervisory authorities | Federal law (US); enforced by HHS Office for Civil Rights | Contractual standard; enforced by card brands through acquirers |
| **Breach Notification** | 72 hours to supervisory authority; individual notification for high-risk breaches | 60 days to affected individuals; HHS annual/media for 500+ | No mandatory public breach notification in the standard; card brands notified |
| **Encryption** | "Appropriate technical measures" (risk-based) | Addressable (required unless documented alternative) | Prescriptive: AES-256 for stored PAN; TLS 1.2+ for transit |
| **Max Penalty** | €20M or 4% of global annual revenue (higher applies) | $1.9M per violation category per year | Card brand fines + forensic costs + potential card acceptance termination |
| **Key Principle** | Data minimization, purpose limitation, privacy by design | Minimum necessary, safeguards, patient rights | Need-to-know, segmentation, least privilege |
:::

:::image src="images/24_regulatorycomparison.png" alt="Venn diagram showing overlap between GDPR, HIPAA, and PCI DSS requirements, with shared controls in the intersection" caption="GDPR, HIPAA, and PCI DSS share many foundational controls but differ in scope, enforcement, and prescription" width=full
:::

:::notes
It is rare for a modern organization to operate under only a single regulatory framework. A US hospital system that processes payment cards and has European patients must comply simultaneously with HIPAA, PCI DSS, and GDPR. Understanding how these frameworks overlap, and where they conflict, is essential for a security architect designing a unified compliance program.

The most important insight is that these frameworks share a common foundation of security controls: access control, encryption, audit logging, incident response, and vendor management. Investing in a strong, principles-based security program, aligned to NIST CSF or ISO/IEC 27001, tends to satisfy the majority of requirements across all three frameworks simultaneously, rather than building separate compliance silos for each.

The key differences lie in specificity, enforcement, and data scope. PCI DSS is the most prescriptive, it specifies exact algorithm requirements (AES-256), protocol versions (TLS 1.2+), and retention periods (12 months of logs). GDPR is the most philosophically flexible but the most financially punishing for violations, the 4% of global annual revenue cap means a company like Alphabet or Meta faces theoretical fines in the tens of billions for a single major violation. HIPAA occupies a middle ground, with detailed technical guidance in the Security Rule but enforcement that historically has focused on systemic failures rather than isolated incidents.

The breach notification timelines differ significantly and create operational challenges for multi-regulated organizations. A healthcare organization that also processes payments and has EU patients must simultaneously manage: a 72-hour GDPR notification, a 60-day HIPAA notification, and card brand notification requirements. Having pre-built, tested notification workflows for each regulatory regime is essential, as is legal counsel that understands all applicable frameworks.

A common controls framework such as HITRUST CSF maps controls to HIPAA, NIST, PCI DSS, GDPR and others at once, letting an organization demonstrate compliance with several standards through one audit. This matters operationally because compliance overhead is one of the largest hidden costs of data security in regulated industries.
:::

%%%
---
unit: Data States
code: STA
title: Database Security Controls
---
:::callout style=soft
Databases are the most common target for data theft, they contain structured repositories of the organization's most sensitive information. A defense-in-depth database security architecture addresses access, activity monitoring, and configuration hardening.
:::

::::columns ratio=1:1
::col::
::::card heading="Database Access Controls"
:::list style=tight
- **Principle of Least Privilege**: Database accounts should have only the permissions required for their function. Application accounts should never have DBA-level access.
- **Separation of Duties**: DBAs who can modify data should not also be able to modify audit logs.
- **Service Account Management**: No shared credentials; rotate service account passwords regularly; disable default accounts (e.g., SA, SYS, SYSTEM).
- **Row-Level Security (RLS)**: Restrict query results to rows the authenticated user is authorized to see, the DB enforces data scope, not the application.
:::
::::
::col::
::::card heading="Database Activity Monitoring (DAM)"
:::list style=tight
- **What it does**: Captures and analyzes all SQL activity, regardless of whether it originates from an application or a direct DBA session.
- **Threat detection**: Identifies SQL injection attempts, anomalous query volumes, privilege escalations, and off-hours bulk exports.
- **Deployment**: Network tap or host-based agent; operates independently of the database so DBAs cannot tamper with logs.
- **Standards**: NIST SP 800-53 AU-2 (Event Logging) and AU-12 (Audit Record Generation) require this monitoring for federal systems.
:::
::::
::::

:::image src="images/24_databasesecurity.png" alt="Diagram of a database security architecture showing network segmentation, access control layers, TDE encryption, and DAM monitoring" caption="Database security requires layered controls spanning access management, encryption, configuration hardening, and independent activity monitoring" width=full
:::

:::notes
Databases are the crown jewels of most organizations' data estates. A single database breach can expose millions of records in a single exfiltration event, dwarfing what is possible through endpoint-by-endpoint data theft. Yet database security is often treated as an afterthought, hardening efforts focus on perimeter firewalls and endpoint protection while the database itself runs with default configurations and overprivileged service accounts.

The principle of least privilege is fundamental to database security. In many organizations, application database accounts are created with DBA-level permissions "for convenience during development" and those permissions are never revoked in production. An attacker who compromises the application layer then inherits full database control, including the ability to dump entire tables, create backdoor accounts, and disable logging.

Row-Level Security (RLS) is a powerful, under-utilized control. Rather than relying on the application to filter query results to only show authorized data, RLS enforces data scope at the database engine level. If a sales representative's database session is constrained by RLS to see only records for their own territory, a SQL injection attack that bypasses application-layer logic still returns only that representative's authorized records. This defense-in-depth approach limits the blast radius of application vulnerabilities.

Database Activity Monitoring (DAM) provides independent oversight of database operations. Because DAM operates either as a network tap or a host-based agent that logs to a separate system, a DBA cannot tamper with the audit trail of their own activities. This satisfies both regulatory requirements (HIPAA, SOX, PCI DSS all require audit logging of data access) and insider threat detection requirements. Modern DAM solutions use behavioral analytics to establish baselines of normal query patterns and alert on anomalies, for example, a developer account that normally executes 50 queries per day suddenly running a SELECT * against the entire customer table at 2 AM.

NIST SP 800-53 Rev 5 Controls AU-2 through AU-14 form the comprehensive audit and accountability control family that drives DAM requirements for federal systems. These controls are directly mappable to database security requirements in commercial frameworks as well.

SQL injection has appeared in every OWASP Top 10 since the list began. If an application builds a query by concatenating user input, SELECT * FROM users WHERE username = '" + input + "', an attacker who enters ' OR '1'='1 makes the condition always true and the query returns every user. Parameterized queries are the primary prevention, and database activity monitoring is the detective control that catches exploitation when prevention fails.
:::

%%%
---
unit: Classification
code: CLS
title: Tool Spotlight, Microsoft Purview (Data Governance and DLP)
---
:::callout style=soft
**Microsoft Purview** is an integrated data governance, risk, and compliance platform combining capabilities from Microsoft Information Protection (MIP), Microsoft 365 Compliance Center, and Azure Purview into a unified solution.
:::

::::columns ratio=1:1
::col::
::::card heading="Core Purview Capabilities"
:::list style=tight
- **Information Protection (Sensitivity Labels)**: Classify and label Office 365 documents, emails, and Teams messages. Labels persist with the file as metadata, enabling policy enforcement wherever the file travels.
- **Data Loss Prevention**: Enforce DLP policies across Exchange, SharePoint, Teams, and endpoints based on sensitivity labels, patterns, and fingerprints.
- **Data Catalog**: Automated discovery and classification of data assets across Azure, AWS, GCP, on-premises SQL servers, and SaaS applications.
- **eDiscovery and Audit**: Legally defensible search, hold, and export of data for regulatory investigations and litigation support.
- **Insider Risk Management**: Machine learning-based detection of risky user activities, including data exfiltration sequences.
:::
::::
::col::
::::card heading="Sensitivity Label Architecture"
:::steps
1. Admin defines label taxonomy (e.g., Public → Internal → Confidential → Highly Confidential) in Purview admin center.
2. Labels are published to users via label policies, targeting specific users or groups.
3. Users (or auto-labeling policies) apply labels to files and emails.
4. Label metadata travels with the file, even outside Microsoft 365 (PDF, downloaded Office files).
5. DLP and Conditional Access policies evaluate the label and enforce appropriate controls (encrypt, block sharing, require MFA to open).
:::
::::
::::

:::image src="images/24_microsoftpurview.png" alt="Architecture diagram of Microsoft Purview showing sensitivity labeling, DLP policy enforcement, data catalog, and insider risk management components" caption="Microsoft Purview integrates data classification, DLP, governance, and insider risk management into a unified platform" width=full
:::

:::notes
Microsoft Purview represents the current generation of integrated enterprise data governance platforms, illustrating how the individual capabilities we have discussed throughout this lecture, data classification, DLP, data inventory, and insider threat detection, can be operationalized in a unified commercial solution.

The Sensitivity Label system is particularly powerful because it creates a persistent, portable classification marker. Unlike file server permission schemes that exist only within the corporate environment, a sensitivity label embedded in a Word document's metadata travels with that document wherever it goes. If a user emails a "Highly Confidential" labeled document to a personal Gmail account, the DLP policy detects the label and blocks the transmission. If the document is downloaded and stored on a personal laptop, the Azure Information Protection (AIP) client enforces encryption and access controls, requiring the user to re-authenticate to Microsoft identity before the document can be opened.

Auto-labeling is a major advancement over manual classification schemes. Purview's machine learning models can scan documents and automatically apply the appropriate sensitivity label based on content analysis, detecting SSNs, credit card numbers, health record identifiers, and more than 200 other sensitive information types across 40+ languages. This addresses the fundamental human factors problem with manual classification: employees do not consistently label documents, especially under time pressure.

The Insider Risk Management module addresses a gap in traditional DLP. While DLP detects specific policy violations, Insider Risk Management builds behavioral profiles of individual users over time, sequencing activities that individually appear benign but collectively indicate risk, for example, accessing unusually large volumes of files, followed by emailing documents externally, followed by disabling AIP protection, all within 48 hours of a resignation notice. This sequence triggers an alert for HR and Security review.

Microsoft Purview is dominant in Microsoft-heavy environments, but comparable capabilities exist elsewhere, Google Chronicle and Workspace DLP, AWS Macie for storage classification, and products such as Varonis, Forcepoint and Proofpoint. The right platform depends on existing technology investments, not the inherent superiority of any vendor.
:::

%%%
---
unit: Data Redundancy
code: BAK
title: Cloud Backup Architectures and the Shared Responsibility Model
---
:::callout style=soft
Cloud providers do not automatically protect customer data. The **Shared Responsibility Model** defines which security obligations belong to the cloud provider and which remain the customer's responsibility, including backup and data protection.
:::

::::columns ratio=1:1
::col::
::::card heading="AWS Shared Responsibility for Data"
:::list style=tight
- **AWS is responsible for**: Security OF the cloud, physical data centers, hypervisor security, network infrastructure, and the durability/availability of managed services (e.g., S3 provides 99.999999999% object durability).
- **Customer is responsible for**: Security IN the cloud, encrypting data, configuring access controls, enabling versioning and backup, managing IAM permissions, and ensuring multi-region redundancy.
- **S3 is NOT a backup by itself**: S3 replicates data within and across AZs but deletion and overwrites (including ransomware encryption) are replicated immediately.
:::
::::
::col::
::::card heading="Cloud Backup Best Practices"
:::list style=tight
- **Enable Versioning**: S3 Object Versioning / Azure Blob Versioning retains previous versions of overwritten or deleted objects for a configurable retention period.
- **Enable Object Lock (WORM)**: Prevents deletion or modification of objects for a defined retention period, even by the account root user.
- **Cross-Region Replication**: Replicate critical data to a secondary region to survive regional outages (satisfies the "offsite" requirement of 3-2-1).
- **AWS Backup / Azure Backup**: Managed backup services that centralize backup policy, monitoring, and restore operations across services.
- **Test Restores**: Cloud restores must be tested just as rigorously as on-premises restores, the restore API must be exercised, not just assumed.
:::
::::
::::

:::image src="images/24_cloudbackup.png" alt="Diagram of the cloud shared responsibility model with data protection responsibilities highlighted on the customer side" caption="Cloud providers protect infrastructure durability; customers must implement versioning, Object Lock, and cross-region replication for true backup resilience" width=full
:::

:::notes
The Cloud Shared Responsibility Model is one of the most misunderstood concepts in cloud security. Organizations migrating to AWS, Azure, or GCP frequently assume that because the cloud provider guarantees high availability and durability for services like S3 or Azure Blob Storage, they no longer need to manage backups. This assumption is incorrect and has led to real data loss events.

AWS S3, for example, provides eleven nines (99.999999999%) of object durability, meaning the expected annual loss of a stored object is extraordinarily low. This means AWS has engineered its infrastructure so that a hardware failure, natural disaster, or datacenter fire will not destroy your objects. However, AWS takes no responsibility for logical data loss, if you or an application deletes a file, if ransomware encrypts and overwrites your objects, or if a misconfigured lifecycle policy expires your data, those objects are gone. AWS maintained its durability guarantee perfectly, and you still lost your data.

S3 Object Versioning is the first line of defense against logical deletion and overwrite. When versioning is enabled, every write to an object creates a new version, and a "delete" operation creates a delete marker rather than removing the underlying version. Previous versions remain accessible for a configurable period. However, if an attacker has IAM permissions to permanently delete all versions (DeleteObject with the versionId parameter), versioning alone is insufficient.

S3 Object Lock in WORM Governance or Compliance mode adds the definitive protection. In Compliance mode, no user, including the AWS account root user, can delete locked objects during the retention period. This is the same technology used to satisfy SEC Rule 17a-4 requirements for financial record immutability.

AWS Backup provides a centralized management plane for backup policies across EC2 instances, RDS databases, DynamoDB tables, EFS file systems, and S3 buckets. It enables policy-as-code backup management, centralized compliance reporting, and cross-account backup copies for additional isolation from a compromised primary account.

Keeping all three copies of a "3-2-1 backup" in the same cloud account does not satisfy the rule, because a compromised account with deletion rights could destroy all three at once. The offsite copy must be logically or physically isolated from the primary environment, which cross-account backups with separate credentials provide.
:::

%%%
---
unit: Classification
code: CLS
title: Common Misconceptions in Data Security
---
:::callout style=soft
**Misconception Check**: Several widely held beliefs about data security are dangerously incorrect. Identifying and correcting these misconceptions prevents real security failures.
:::

:::table
| Misconception | Why It's Wrong | Correct Understanding |
|---|---|---|
| "We're too small to be a target" | Automated attack tools make organization size irrelevant. SMBs are frequently targeted for their data or as a supply chain vector to larger targets. | Every organization is a target. Size affects resources, not risk. |
| "Encryption protects us from breaches" | Encryption protects data confidentiality at rest/transit. It does not prevent unauthorized access by authenticated users, insider threats, or application-layer attacks. | Encryption is one control. Access management, monitoring, and testing are equally essential. |
| "Deleted files are gone" | Standard OS deletion removes directory entries, not data. Forensic tools can recover data until the sectors are overwritten. | Deleted ≠ sanitized. Proper sanitization requires Clear, Purge, or Destroy per NIST SP 800-88. |
| "Our cloud provider backs up our data" | Cloud providers protect infrastructure durability, not logical data integrity. Deleted or overwritten data is not automatically retained. | Customers must enable versioning, Object Lock, and cross-region replication explicitly. |
| "Compliance = security" | Compliance frameworks define minimum requirements. Passing a PCI DSS audit certifies point-in-time compliance, not ongoing security. | Compliance is a floor, not a ceiling. Many breached organizations were "compliant" at the time of breach. |
| "Strong passwords protect database accounts" | Passwords can be stolen via phishing, keyloggers, or credential stuffing. Authentication strength must be supplemented with MFA, session monitoring, and least-privilege access. | MFA, least privilege, and behavioral monitoring are required alongside strong passwords. |
:::

:::image src="images/24_misconceptions.png" alt="Six callout cards each presenting a common data security misconception and its correction" caption="Correcting data security misconceptions prevents false confidence that leads to security program gaps" width=full
:::

:::notes
One of the most valuable services a security professional can provide is correcting misconceptions, both within technical teams and in executive leadership. False confidence in the effectiveness of controls that are improperly understood leads to underinvestment in the controls that are actually needed.

The "too small to be a target" misconception persists despite overwhelming evidence to the contrary. Cybercriminal groups deploy automated scanning tools that enumerate internet-facing systems by vulnerability type, not by victim size. A small accounting firm with misconfigured RDP exposed to the internet is just as likely to be hit by ransomware as a Fortune 500 company. SMBs are increasingly targeted specifically because they serve as supply chain vectors to larger partners, the Target breach of 2013 originated through HVAC contractor Fazio Mechanical, which had network access to Target's systems.

The encryption misconception is subtle but important. Encryption of data at rest protects against physical theft and unauthorized storage access. It does not help if an attacker authenticates with stolen credentials, the database will happily decrypt and serve records to any authenticated session. Encryption is one layer of a defense-in-depth stack, not a silver bullet.

The deletion misconception has driven many breach investigations. When a user "deletes" a file on Windows, the operating system marks those sectors as available for reuse but does not overwrite them. Forensic tools like Autopsy, FTK, or even free tools like Recuva can recover deleted files within seconds, as long as the sectors have not been reused. This is why NIST SP 800-88 Clear (overwriting) is the minimum required sanitization before transferring media.

The compliance-versus-security misconception is particularly relevant for security leaders. The PCI DSS compliance assessments of breached retailers like Target (2013) and Home Depot (2014) found them compliant at or near the time of breach. Compliance frameworks define minimum baseline controls; sophisticated attackers find gaps in those baselines. An active security program, including penetration testing, threat hunting, and red team exercises, goes beyond compliance to test whether controls actually work.

Security theater is a control that creates the appearance of security without meaningful risk reduction, such as password complexity rules that drive password reuse, or awareness training clicked through in two minutes. Effective security requires verifying that a control achieves its intended risk reduction, not merely implementing it.
:::

%%%
---
unit: Classification
code: CLS
title: Data Retention Policies and Legal Hold
---
:::callout style=soft
**Data retention** policies define how long data must be kept and when it must be destroyed. Retaining data beyond its legally required period unnecessarily expands breach impact; destroying data too early can trigger legal sanctions.
:::

::::columns ratio=1:1
::col::
::::card heading="Data Retention Drivers"
:::list style=tight
- **Legal requirements**: Tax records (IRS: 7 years), healthcare records (HIPAA: 6 years from creation or last effective date), financial records (SEC: 7 years for broker-dealers), contracts (varies by jurisdiction).
- **Regulatory requirements**: GDPR storage limitation principle (Article 5(1)(e)), data must not be retained longer than necessary for its purpose.
- **Business requirements**: Customer relationship history, warranty records, engineering documentation.
- **Litigation holds**: When litigation is anticipated, all potentially relevant data must be preserved, normal destruction schedules are suspended.
:::
::::
::col::
::::card heading="Legal Hold Process"
:::steps
1. Legal counsel identifies a litigation or investigation trigger.
2. Litigation hold notice issued to custodians (employees with relevant data).
3. Normal retention schedules suspended for affected data categories.
4. Automated hold applied in eDiscovery systems (e.g., Microsoft Purview eDiscovery, Relativity).
5. Hold maintained until litigation is resolved.
6. Hold released and normal retention policies resume.
:::
::::
::::

:::image src="images/24_dataretention.png" alt="Timeline diagram showing data creation, active retention period, retention expiry, and destruction phases with a legal hold overlay" caption="Data retention policies balance legal minimum retention requirements against the GDPR storage limitation principle" width=full
:::

:::notes
Data retention is the intersection of data security and legal compliance, and it is more complex than many security teams appreciate. The fundamental tension is between two opposing forces: legal and regulatory requirements to keep data for minimum periods, and the GDPR and privacy principle of data minimization, which requires not keeping data longer than necessary.

Retaining data beyond its legally required period creates unnecessary risk. Every piece of data retained is a potential piece of data that could be exposed in a breach. A breach affecting data that was supposed to have been destroyed three years ago is both a data security failure and a data retention compliance failure, two separate liability exposures. Many breach notifications have revealed that the breached data included records that should no longer have existed under the organization's own retention policy.

Failing to meet minimum retention requirements creates different legal risks. Organizations that destroy financial or tax records before the required retention period ends can face IRS penalties. Healthcare organizations that destroy medical records before the HIPAA-required minimum expose themselves to malpractice liability and HIPAA penalties.

Legal hold is a critically important mechanism that most data security programs must support. When a company receives notice of litigation (or has reason to anticipate it), destroying data that might be relevant to that litigation constitutes spoliation, destruction of evidence. Courts can impose severe sanctions for spoliation, including adverse inference instructions (the jury is told to assume the destroyed evidence would have been damaging to the party that destroyed it), monetary fines, and in extreme cases, case-dispositive sanctions. The obligation to preserve evidence is triggered by a reasonable anticipation of litigation, not only when a lawsuit is actually filed.

NIST SP 800-53 Rev 5 Control AU-11 (Audit Record Retention) addresses retention of security audit logs specifically, but the broader data retention challenge spans all enterprise data categories. ISO 15489 (Records Management) provides the international framework for records retention schedules.

A retention policy that destroys emails after 90 days collides with litigation: a litigation hold must suspend destruction before the schedule runs, and the organization must show a good-faith, consistently applied policy that operated before litigation was anticipated. Courts view inconsistently applied schedules that conveniently destroy relevant documents very unfavorably.
:::

%%%
---
unit: Data States
code: STA
title: Data Security Risk Assessment
---
:::callout style=soft
A **Data Security Risk Assessment** identifies threats to sensitive data, estimates the likelihood and impact of those threats materializing, and prioritizes security control investment to reduce risk to acceptable levels.
:::

:::steps
1. **Asset Identification**: Enumerate sensitive data assets using the data inventory. Include data classification level for each asset.
2. **Threat Identification**: For each asset, identify realistic threat actors (external attackers, malicious insiders, accidental disclosure) and threat events (breach, ransomware, misconfiguration).
3. **Vulnerability Assessment**: Identify existing control gaps, missing encryption, excessive permissions, unpatched systems, inadequate DLP coverage.
4. **Likelihood Estimation**: Assess the probability that each threat will exploit each vulnerability given current controls. Use qualitative scales (High/Medium/Low) or quantitative estimates.
5. **Impact Estimation**: Assess the business impact if the threat materializes, financial loss, regulatory penalty, reputational damage, operational disruption.
6. **Risk Scoring**: Combine likelihood × impact to produce a risk score. Prioritize treatment of highest-scoring risks.
7. **Treatment Selection**: For each risk: Accept (within tolerance), Mitigate (add controls), Transfer (insurance/contract), or Avoid (stop the activity).
8. **Residual Risk Documentation**: Document remaining risk after treatment. Obtain management acceptance of residual risk.
:::

:::image src="images/24_riskassessment.png" alt="Risk matrix diagram plotting data security threats by likelihood and impact with color-coded risk zones" caption="A risk matrix maps data security threats by likelihood and impact to prioritize control investment" width=full
:::

:::notes
Risk assessment is the analytical engine that drives proportional security investment. Without a risk assessment, security programs tend toward either under-investment (hoping breaches will not occur) or over-investment in visible controls while neglecting less obvious gaps. NIST SP 800-30 Rev 1 (Guide for Conducting Risk Assessments) and ISO/IEC 27005 (Information Security Risk Management) provide the formal methodologies for data security risk assessment.

The process begins with the data inventory we established earlier. The risk assessment is bounded by what data assets exist and what classification level they carry, a risk assessment for a Restricted dataset (SSNs, credit card numbers) will look very different from one for Internal data.

Threat modeling for data security draws on several sources. MITRE ATT&CK provides a comprehensive library of adversarial tactics and techniques, allowing organizations to assess realistic threat scenarios based on the techniques used by known threat actor groups. For example, if the primary concern is financial cybercrime groups targeting payment card data, ATT&CK can help identify the specific exfiltration techniques (T1041, T1048, T1567) these groups use, allowing targeted control selection.

The likelihood × impact risk matrix is the most common risk scoring approach. Both dimensions are assessed using scales (1-5, or High/Medium/Low) calibrated to the organization's risk appetite. A threat that is highly likely but has low impact (a common spam email campaign) scores differently from a rare but catastrophic threat (a nation-state APT targeting product blueprints). Risk matrices visually communicate the relative priority of risks to executives and board members who may not be technical but need to make resource allocation decisions.

NIST SP 800-30 also addresses the concept of "inherent risk" (risk before controls are applied) versus "residual risk" (risk remaining after controls). Risk acceptance statements, documenting that management acknowledges and accepts a specific residual risk level, are essential for audit and regulatory purposes. Without formal acceptance documentation, unmitigated risks appear as control failures rather than conscious business decisions.

A mini risk assessment ties the concepts together. For a university storing student Social Security numbers in a legacy database: threat, ransomware; likelihood, high (universities are high-value targets with historically weak security); impact, high (FERPA penalties, reputation, disruption); existing controls, basic firewall, no encryption, no database MFA; residual risk, very high; treatment, MFA, transparent database encryption, privileged access management and immutable offsite backups.
:::

%%%
---
unit: Summary
code: CLS
title: Mid-Lecture Checkpoint, Knowledge Check
---
:::callout style=soft
**Pause and Reflect**: Before the summary, test your understanding of the core concepts covered in this lecture.
:::

::::columns ratio=1:1
::col::
::::card heading="Quick Questions"
:::list style=tight
- What is the difference between a Data Owner and a Data Custodian?
- Name the three categories of sanitization defined in NIST SP 800-88.
- Why does degaussing NOT work on solid-state drives?
- What does RPO measure, and what backup design decision does it drive?
- Name two GDPR articles with direct data security implications.
- What is Cryptographic Erase, and what type of drive must support it?
- Why are synchronized cloud folders (OneDrive/Dropbox) not a valid backup against ransomware?
- What is the difference between DLP in "monitor" mode and "block" mode, and why should organizations start in monitor mode?
:::
::::
::col::
::::card heading="Key Formula Reminders"
:::list style=tight
- **3-2-1 Rule**: 3 copies → 2 media types → 1 offsite.
- **3-2-1-1-0 Extension**: Adds 1 offline/immutable copy + 0 errors verified by test.
- **Risk = Likelihood × Impact**
- **RTO** = maximum acceptable downtime.
- **RPO** = maximum acceptable data loss (measured in time).
- **NIST SP 800-88**: Clear (user-addressable) → Purge (lab-proof) → Destroy (physical).
- **TLS 1.3** = current standard; TLS 1.0/1.1 = deprecated (RFC 8996); SSL = never use.
:::
::::
::::

:::image src="images/24_checkpoint.png" alt="Checklist-style knowledge check graphic with eight questions and key formula reminders for data security concepts" caption="Mid-lecture checkpoint: review these questions before moving to the summary" width=full
:::

:::notes
This checkpoint is designed to give students a moment to consolidate the significant volume of material covered in this lecture. Data security is a broad discipline that spans governance, cryptography, backup architecture, regulatory compliance, and operational tooling, it is common for students to absorb individual concepts well but struggle to integrate them into a coherent mental model.

Walk through each question briefly in class, calling on students for answers. This immediate retrieval practice (a technique with strong evidence from cognitive science literature) significantly improves long-term retention compared to passive re-reading.

For the Data Owner vs. Data Custodian question, the key distinction is business accountability versus technical implementation. The owner decides the classification and access policy; the custodian implements the encryption and backup controls.

For the NIST SP 800-88 question, students often confuse the order. Clear is overwriting (simplest). Purge is degaussing/cryptographic erase (lab-proof). Destroy is physical destruction (irreversible). The progression represents increasing security assurance at increasing cost and irreversibility.

The degaussing/SSD question tests a common practical misconception. SSDs use electrical charge states in NAND flash cells, a magnetic field has no effect on electron charge. This is a favorite exam question in certifications like CompTIA Security+ and CISSP.

The RPO question should elicit: RPO measures how much data loss is acceptable in time, which determines backup frequency. A 1-hour RPO means backups must run at least every hour.

The cloud sync/ransomware question reinforces the critical distinction between synchronization (real-time mirroring that propagates changes including encryption) and backup (point-in-time copies with independent retention policies). Students often conflate these because consumer cloud services market sync as "backup."

:::

%%%
---
unit: Summary
code: SUM
title: Data Security Lifecycle Summary
---
:::pullquote
Classification tells us how much protection data deserves. Access control, backups, and DLP are how that protection actually gets delivered.
:::

:::list style=chips
- Corporate vs. Government Classification
- At Rest, In Transit, and In Use States
- 3-2-1 Backup Architecture
- Endpoint and Network DLP
- NIST SP 800-88 Sanitization Standards
:::

:::image src="images/24_summary.png" alt="Mind map connecting data classification at the center to the three states of data, backup architecture, DLP, and media sanitization" caption="Data security is a lifecycle discipline spanning classification, state controls, redundancy, exfiltration prevention, and secure disposal" width=full
:::

:::notes
In today's lecture, we examined the discipline of data security across its full lifecycle, from the moment data is created and classified, through the technical controls applied at each state of its existence, to its ultimate secure disposal.

We established that data classification is the prerequisite for all other controls, ensuring security resources are allocated appropriately. We explored the three states of data and their respective controls, from disk encryption to transport protocols and hardware enclaves. We also reviewed the 3-2-1 backup rule as the primary protection against data loss and ransomware, analyzed how DLP monitors and blocks data exfiltration, and concluded with the NIST SP 800-88 media sanitization guidelines.

We extended these foundational concepts with deep dives into governance roles (data owners, stewards, and custodians), regulatory frameworks (GDPR, HIPAA, PCI DSS), database security controls, cloud backup architecture, and risk assessment methodology. We also examined real-world case studies, the Capital One cloud breach, Target's RAM-scraping attack, and healthcare DLP challenges, that illustrate how these concepts manifest in actual security incidents.

The unifying thread is the data security lifecycle: you cannot protect what you have not classified, you cannot monitor what you have not inventoried, and you cannot recover from what you have not backed up and tested. Data security is not a one-time project but a continuous operational discipline.

Protecting data is the final objective of all cybersecurity frameworks. In our next lecture, we will study the primary technical tool used to enforce confidentiality and integrity across all these states: cryptography. We will dive into the mathematics of encryption, keys, and hashing, laying the groundwork for digital signatures and secure communication.

Data security controls map across all five NIST CSF functions: Identify (data inventory, classification, risk assessment), Protect (encryption, DLP, access controls), Detect (database activity monitoring, DLP alerts, user-behavior analytics), Respond (incident response, breach notification) and Recover (backup, RTO/RPO, recovery drills). The discipline is an integrated whole, not a set of isolated tools.
:::
