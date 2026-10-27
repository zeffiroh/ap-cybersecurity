---
deck:
  title: Access Control
  kicker: Class 18
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 18
  description: Authentication proves who you are, access control decides what you're allowed to actually do.
  topics: [Authentication, Authorization, Least Privilege, RBAC, DAC, MAC]
---

%%%
---
title: Access Control
cover: true
---
:::text class=sub
Authentication vs. Authorization, Enterprise Access Models, and Security Policy Enforcement
:::
:::list style=chips
- Authentication vs. Authorization (NIST SP 800-53)
- Least Privilege (AC-6) & Separation of Duties (AC-5)
- RBAC, DAC, and MAC Architecture
- Mathematical Security Models (Bell-LaPadula & Biba)
:::

:::image src="images/18_access_control_overview.png" alt="Three-stage security gateway illustration: a user presents credentials at the Authentication gate (labeled 'Who are you?'), passes through to the Authorization gate (labeled 'What can you do?'), then reaches the protected resource, with rejected access attempts showing red X marks at each stage and approved access showing green checkmarks" caption="The access control pipeline, authentication proves identity, authorization enforces permissions, together they protect resources from unauthorized access" width=full:::
:::

:::notes
Welcome to Class 18, "Access Control." In our previous lectures, we explored authentication systems that prove a user's identity, and host hardening practices that secure system configurations. Today, we will examine the logical policies that govern what an authenticated user or system process can do with the access they have been granted. Authentication and authorization are the two essential pillars of access control, and understanding how they work together, and where they differ, is fundamental to designing secure systems.

Access control is a foundational pillar of cybersecurity, directly supporting the Confidentiality and Integrity components of the CIA triad. Without effective access control, a successfully authenticated user could read any file on the system, modify any database record, or install any software. This would mean that stealing a single set of credentials, which attackers routinely accomplish through phishing, credential stuffing, or password spraying, would provide unlimited access to all organizational resources. Access control limits this blast radius by ensuring that each identity can only interact with the specific resources they need for their legitimate work.

We will analyze access control through the lens of international standards, including NIST Special Publication 800-53 (Security and Privacy Controls, Access Control family AC-1 through AC-25) and the foundational ANSI/INCITS 359-2004 standard for Role-Based Access Control. We will compare the four primary access control models that organizations deploy today: Discretionary Access Control (DAC), which is the default model in most operating systems; Mandatory Access Control (MAC), used in high-security government and military environments; Role-Based Access Control (RBAC), the most common enterprise model; and Attribute-Based Access Control (ABAC), the most flexible and sophisticated modern model.

We will also study the mathematical formal security models that underlie MAC implementations: the Bell-LaPadula Confidentiality Model, which enforces the "no read up, no write down" rule to prevent information leakage across classification levels, and the Biba Integrity Model, which enforces complementary rules to protect data integrity. These mathematical models provide a rigorous, provable basis for access control policy, allowing security architects to formally verify that an access control system cannot be configured to allow prohibited information flows.

By the end of this lecture, you will understand how to select, design, and implement authorization policies appropriate for different organizational contexts, from the open sharing environment of a collaborative business to the strict compartmentalization of a classified government system.

ISO/IEC 27001:2022 reorganizes its access control requirements under Annex A.9 (Access Control), which maps directly to NIST SP 800-53's AC control family. A.9.1 requires a documented access control policy, A.9.2 addresses user access management including provisioning and deprovisioning, A.9.4 covers system and application access control, and A.9.4.4 specifically addresses the use of privileged utility programs. GDPR Article 25 (Data Protection by Design and Default) requires that organizations implement access control as a technical measure to ensure that personal data is not accessed beyond what is necessary for the specified purpose, making access control not merely a security concern but a legal compliance obligation for organizations processing EU personal data. The 2013 Target breach, in which attackers accessed Target's payment processing network through compromised HVAC vendor credentials, demonstrated that insufficient access control between network segments and overly permissive third-party access rights can enable catastrophic breaches even when authentication is present.
:::

%%%
---
unit: Foundations
code: ATH
title: Authentication vs. Authorization
---
:::callout style=soft
Access control requires a two-step process: **Authentication (AuthN)** verifies the identity of a subject, while **Authorization (AuthZ)** determines the rights and permissions granted to that authenticated identity.
:::

::::columns ratio=1:1
::col::
::::card heading="Authentication (AuthN)"
:::list style=plain
- **Objective:** Proves identity ("Who are you?").
- **Verification Factors:** Passwords, biometrics, hardware tokens, cryptographic certificates.
- **NIST Standard:** NIST SP 800-63 (Digital Identity Guidelines).
:::
::::
::col::
::::card heading="Authorization (AuthZ)"
:::list style=plain
- **Objective:** Restricts operations ("What can you do?").
- **Verification Factors:** Roles, group memberships, file permissions, security clearance labels.
- **NIST Standard:** NIST SP 800-53 Access Control (AC) Family.
:::
::::
::::

:::flow
Subject presents credentials
Authentication engine verifies identity claim
Identity confirmed, session token issued
Authorization engine evaluates access policy
Policy evaluation: permissions granted for this identity
Access decision: permit or deny resource request
Audit log records the access decision (accounting)
:::

:::image src="images/18_authn_authz_flow.png" alt="Sequential flow diagram showing the AAA model: Authentication step with credential symbols, Authorization step with permission matrix, and Accounting step with log file icon, with a subject (person icon) on the left and a protected database resource on the right, connected by the three-step pipeline" caption="The AAA model: Authentication, Authorization, and Accounting, three distinct phases required for comprehensive access control" width=half:::
:::

:::notes
Although "authentication" and "authorization" are frequently used interchangeably in casual conversation, they represent fundamentally distinct security phases that must both be implemented correctly for an access control system to provide meaningful security. A failure in either phase can result in unauthorized access: a weak authentication system allows attackers to impersonate legitimate users, while a weak authorization system allows legitimately authenticated users to access resources outside their permitted scope.

Authentication occurs at the boundary of the system, verifying that a user, device, or process is the entity it claims to be. Authentication relies on one or more factors: something the subject knows (passwords, PINs, security questions), something the subject has (hardware tokens, smart cards, mobile authenticator apps), something the subject is (biometric characteristics such as fingerprints, facial geometry, or retinal patterns), or, in advanced implementations, somewhere the subject is (geolocation-based authentication) or something the subject does (behavioral biometrics such as typing cadence). NIST SP 800-63 provides detailed guidance on identity assurance levels (IAL) and authentication assurance levels (AAL), specifying which combinations of factors are appropriate for systems requiring different levels of assurance.

Once identity is verified, the system enters the authorization phase. Authorization is the process of enforcing access control policies to determine which specific operations an authenticated subject is permitted to perform on which specific objects. The subject (a user account, service account, or process) presents a request to access an object (a file, database record, API endpoint, or network resource). The authorization engine evaluates the request against a policy that defines the permitted relationships between subjects and objects, and produces a permit or deny decision. This decision is then logged for accountability purposes.

The accounting component, the third element of the classic AAA (Authentication, Authorization, and Accounting) security framework, is equally critical. Accounting creates an immutable audit trail of all authorization decisions, recording who accessed what, when, from where, and with what outcome. This audit trail is essential for forensic investigation, regulatory compliance (such as SOX, HIPAA, and GDPR requirements for audit logging), and detecting anomalous access patterns that may indicate credential compromise.

A common failure mode in access control design is conflating authentication strength with authorization sufficiency. An organization might implement strong multi-factor authentication while using an overly permissive authorization model that grants all authenticated users broad access to sensitive resources. Strong authentication without granular authorization provides limited protection against insider threats or compromised credentials. The two controls must be designed and implemented together as a unified access control architecture.

Privilege creep is a particularly common access control failure in dynamic organizations. When employees change roles, take on temporary project responsibilities, or receive access rights to expedite urgent business needs, those rights are frequently never revoked. Over time, individual users accumulate far more access than their current role requires, creating a situation where a single compromised account can access systems across multiple business functions. Access reviews, periodic audits of user rights against current role requirements, are the primary control against privilege creep (NIST SP 800-53 AC-2 Account Management).

NIST SP 800-207 (Zero Trust Architecture) elevates authentication and authorization from static perimeter controls to continuous, dynamic evaluations. In a Zero Trust model, authentication does not produce a permanent trusted session, instead, every new access request triggers a fresh authorization evaluation that considers the requester's current device health, behavioral risk score, and the sensitivity of the specific resource being requested. This "continuous verification" model directly addresses the limitation of traditional AAA where a valid session token, once issued, may remain trusted for hours or days even if the underlying session is later compromised. The concept of "just-in-time" (JIT) authorization, implemented in products like Microsoft Privileged Identity Management (PIM), extends this principle to privileged access, requiring users to request and receive time-limited privilege grants rather than holding elevated permissions continuously, dramatically reducing the window of exposure if credentials are stolen.
:::

%%%
---
unit: Principles
code: LPV
title: Least Privilege & Implicit Deny
---
:::callout style=soft
The **Principle of Least Privilege** (NIST SP 800-53 AC-6) states that subjects must be granted only the minimum permissions necessary to complete their assigned tasks.
:::

:::steps
1. **Implicit Deny:** By default, all access is blocked. If no explicit rule permits access, it is denied.
2. **Needs Analysis:** Evaluating the operational requirements of a job role to determine necessary resources.
3. **Explicit Authorization:** Creating access rules that permit only the verified operational requirements.
4. **Separation of Duties (AC-5):** Splitting critical tasks among multiple users to prevent fraud or administrative abuse.
5. **Privilege Review:** Auditing access rights regularly to revoke permissions that are no longer necessary.
:::

:::image src="images/18_least_privilege_model.png" alt="Layered permission diagram showing three user types: a standard user with minimal file-system access (small green zone), a power user with expanded but limited access (medium zone), and an administrator with full access (large zone), with 'need-to-know' labels and arrows showing how each scope is minimized to the operational requirement, plus a 'blast radius' indicator showing how a compromised account's access scope limits damage" caption="Least Privilege access scoping, each identity class is restricted to the minimum resource set required, limiting the blast radius if that identity is compromised" width=full:::
:::

:::notes
The Principle of Least Privilege is one of the most powerful and widely applicable security design principles in cybersecurity. First articulated by Jerome Saltzer and Michael Schroeder in their foundational 1975 paper "The Protection of Information in Computer Systems," the principle holds that every subject, whether a user, a process, or a program, should operate with only the minimum set of privileges necessary to accomplish its defined task, and no more.

The security benefit of least privilege is the limitation of blast radius. If an attacker compromises a standard user account that has been properly restricted to its minimum required access, the attacker inherits only those restricted permissions. They can access the files the compromised user can access, run the applications the user can run, and interact with the network services the user is permitted to reach. This limits lateral movement, prevents privilege escalation via the compromised account, and restricts data exfiltration to only the data the account could legitimately access. Contrast this with an environment where users routinely operate with local administrator or domain administrator rights, in that environment, a single phishing attack that compromises one user account can give the attacker complete control over the entire organization's infrastructure.

The foundation of least privilege is the default policy of Implicit Deny. In a properly designed access control system, the rule for any access request that does not match an explicit "permit" rule is automatic denial. This is the opposite of the dangerous "allow by default" model, where everything is permitted unless explicitly blocked. Implicit deny creates a closed system: to gain access to any resource, the request must match a specific, explicitly written permission rule. This ensures that forgotten, legacy, or unreviewed permissions cannot silently provide access.

Building a least privilege authorization system requires a structured role analysis process. First, security and business analysts work together to document every job role in the organization and the specific resources each role requires to perform its functions. This analysis must be granular, not just "the HR department needs access to the HR system," but "HR Generalists need read/write access to employee personal records and read-only access to payroll reports, but not access to payroll calculation functions or executive compensation data." These requirements are then translated into specific access control rules.

Separation of Duties (NIST SP 800-53 AC-5) is a complementary principle that divides critical business processes among multiple users, requiring collaboration, and therefore collusion, for fraud to occur. The classic example is financial controls: the employee who can create a vendor payment record must be different from the employee who approves payment, and both must be different from the employee who reconciles bank statements. No single individual should be able to complete a financially significant transaction unilaterally. In IT, separation of duties prevents administrators from both writing code and deploying it to production, requiring a second actor to review and approve deployment, making sabotage significantly more difficult and detectable.

Regular access reviews are the operational mechanism for maintaining least privilege over time. NIST SP 800-53 AC-2 requires organizations to review user account access rights at defined intervals, typically quarterly for privileged accounts and annually for standard users. These reviews compare current access rights against current job requirements, identifying and revoking access that is no longer needed.

The principle's importance is illustrated starkly by the 2013 Target data breach: attackers compromised credentials belonging to Fazio Mechanical, an HVAC vendor with network access. Because Target's access control architecture granted that vendor access to payment processing network segments beyond what was operationally necessary, the attackers were able to pivot from the HVAC management system to the point-of-sale network and ultimately exfiltrate 40 million credit card numbers. A properly enforced least privilege architecture would have restricted the vendor's network access to only the HVAC management systems, containing the breach. CIS Control 5 (Account Management) in CIS Controls v8 requires organizations to establish and maintain an inventory of all accounts, implement least privilege access for all accounts, and disable accounts that are inactive for more than 45 days, providing specific, measurable implementation requirements that operationalize NIST AC-6.
:::

%%%
---
unit: Models
code: RBA
title: Role-Based Access Control (RBAC)
---
:::callout style=soft
**Role-Based Access Control (RBAC)** assigns permissions to specific organizational roles rather than to individual users. Users inherit the permissions of the roles to which they are assigned.
:::

:::flow
User Account Created
Job Role Identified (e.g., HR Generalist, Database Administrator)
User Assigned to Role
Role Permissions Applied to User Session
User Requests Resource Access
Authorization Engine Checks Role Membership
Access Permitted or Denied Based on Role Permissions
Role Membership Reviewed and Updated During Access Review Cycle
:::

:::image src="images/18_rbac_hierarchy.png" alt="Three-tier hierarchical diagram showing RBAC structure: Users tier at the bottom with individual user icons, Roles tier in the middle with role boxes (HR Generalist, DBA, Network Admin, Developer), and Permissions tier at the top with resource icons (files, databases, network devices, source repos), arrows from users point to roles, arrows from roles point to permitted resources" caption="RBAC three-tier architecture, permissions are assigned to roles rather than users, with users inheriting access through role assignment" width=full:::
:::

:::notes
Role-Based Access Control (RBAC), formally standardized under ANSI/INCITS 359-2004, is the most widely deployed authorization model in modern enterprise networks and applications. It was introduced to address a fundamental scalability problem in direct user-to-resource permission management: as organizations grow, maintaining individual permission assignments for each user against each resource becomes administratively unmanageable and audit-unfriendly.

Consider the access control challenge for an organization with 500 employees and 200 distinct systems and applications. Direct user-permission management would theoretically require 500 × 200 = 100,000 individual permission relationships to be created, documented, and maintained. When an employee joins, an administrator must manually grant access to every system they need. When an employee leaves, an administrator must manually revoke access from every system they had. When a system is retired, administrators must manually remove it from every user's permission set. When a regulatory audit occurs, auditors must review all 100,000 permission relationships to verify compliance. This is operationally impractical and audit-nightmarish.

RBAC solves this by introducing roles as an abstraction layer between users and permissions. Instead of mapping users directly to resources, administrators define roles that correspond to organizational job functions, "HR Generalist," "Finance Manager," "Database Administrator," "Network Engineer," "Sales Representative." Each role is granted the specific set of resource permissions required for that function. Users are then assigned to the appropriate roles. Access rights follow automatically from role assignment. The number of permission relationships to manage drops dramatically: instead of user × resource relationships, organizations manage role × resource relationships (typically dozens of roles instead of hundreds of users) plus user × role relationships (one role assignment per user instead of dozens of resource grants).

The RBAC standard defines four models of increasing sophistication. Flat RBAC (RBAC0) provides the basic three-tier user-role-permission structure. Hierarchical RBAC (RBAC1) allows role inheritance, where a senior role automatically inherits the permissions of junior roles, for example, a "Senior Database Administrator" role might inherit all permissions of the "Database Administrator" role plus additional rights. Constrained RBAC (RBAC2) adds separation of duty constraints, preventing a single user from holding two roles that would together grant excessive privilege. Symmetric RBAC (RBAC3) combines hierarchy and constraints.

In enterprise implementations, RBAC is typically implemented through directory services such as Microsoft Active Directory or LDAP. Users are added to security groups that correspond to roles, and those groups are granted access to specific resources. This architecture integrates with virtually every modern application, enabling centralized role management that cascades across the entire application portfolio. When an employee changes departments, administrators update their group membership, and access rights adjust automatically across all integrated systems.

The primary operational risk in RBAC deployments is "role explosion", the tendency for organizations to create increasingly specific roles to handle permission variations, ultimately creating hundreds or thousands of roles that are as difficult to manage as individual user permissions. Role rationalization, periodically reviewing and consolidating roles, is a necessary operational discipline.

In Microsoft Active Directory environments, RBAC is implemented through security groups: users are added to AD security groups that correspond to organizational roles, and those groups are granted access to file shares, SharePoint sites, Exchange mailboxes, and application resources. Microsoft's Tier Administration Model extends RBAC with zone-based isolation, preventing administrator accounts that manage workstations from also managing servers or domain controllers, limiting the blast radius of a credential compromise in a privileged account. NIST SP 800-53 AC-2 (Account Management) requires organizations to define and document the roles with access to the system, approve access based on valid role assignment, and review accounts regularly, establishing RBAC as a compliance control as well as an operational security architecture. The 2021 Colonial Pipeline ransomware attack, which disrupted fuel supply to the US East Coast, was enabled in part by a compromised VPN account belonging to a former employee that had not been properly deprovisioned, illustrating how RBAC lifecycle management (timely deprovisioning) is as critical as the initial access grant.
:::

%%%
---
unit: Models
code: DAC
title: Discretionary Access Control (DAC)
---
:::callout style=soft
**Discretionary Access Control (DAC)** permits the owner of a resource to determine access permissions for other subjects. Access is managed at the discretion of the resource owner.
:::

::::columns ratio=1:1
::col::
::::card heading="Mechanics of DAC"
:::list style=plain
- **Access Control Lists (ACLs):** Metadata tables attached to files or folders listing users and their read, write, or execute permissions.
- **Access Control Entries (ACEs):** Individual entries within an ACL defining the permissions of a specific user or group.
- **Discretionary Sharing:** Users can pass their permissions on to other users without administrative oversight.
:::
::::
::col::
::::card heading="Security Implications"
:::list style=plain
- **High Flexibility:** Allows quick sharing and decentralized management, suitable for collaborative business environments.
- **Low Security Control:** Vulnerable to user error, Trojan horses, and lateral movement, as permissions can be modified by compromised accounts.
:::
::::
::::

:::steps
1. **Resource Creation:** A user creates a file or directory; the OS assigns that user as the resource owner with full discretionary control over the Access Control List.
2. **ACL Configuration:** The owner configures the ACL, specifying which users or groups receive Read, Write, Execute, Modify, or Full Control rights via ACE entries.
3. **Access Request Evaluation:** When a subject attempts to access the resource, the OS kernel reads the Security Descriptor and evaluates the requesting principal against each ACE in order.
4. **ACE Matching:** The system identifies the first ACE matching the requesting principal (or a group the principal belongs to) and evaluates whether it is an Allow or Deny entry, explicit Deny takes precedence.
5. **Access Decision:** If a matching Allow ACE is found and no Deny ACE takes precedence, access is granted at the permitted level; otherwise the request is denied.
6. **Audit Logging:** The access decision (permit or deny) is recorded in the OS security event log if object access auditing has been configured (NIST SP 800-53 AU-2).
:::

:::image src="images/18_dac_acl_structure.png" alt="File system diagram showing a document file with its attached Access Control List (ACL) expanded: entries for Owner (Alice, Full Control), Bob (Read/Write), Marketing Group (Read Only), and Everyone (Deny), with arrows showing how a Trojan running as Alice can modify the ACL to grant itself access to other files, illustrating DAC's primary security weakness" caption="DAC Access Control List structure, the owner controls all permissions, which provides flexibility but creates risk when accounts are compromised" width=full:::
:::

:::notes
Discretionary Access Control (DAC) is the default access model for consumer operating systems (Windows, macOS, Linux) and most cloud collaboration platforms (Google Drive, OneDrive, Dropbox). It is called "discretionary" because access decisions are left to the discretion of the resource owner, the individual user or process that created or owns a resource controls who else can access it.

In a DAC model, every resource has an associated owner, typically the user account that created it. This owner holds full control over the resource's Access Control List (ACL), a metadata structure maintained by the operating system kernel that defines which other users or groups can access the resource and with what permissions. In Windows, file and directory permissions are managed through NTFS ACLs, implemented in the Windows Security Descriptor. A Security Descriptor contains a Discretionary ACL (DACL) listing Access Control Entries (ACEs), each specifying a security principal (user or group), an access right (Read, Write, Execute, Modify, Full Control), and whether the ACE allows or denies that right. Linux implements a simpler but analogous model through POSIX permission bits and POSIX Access Control Lists (POSIX ACLs).

The primary strength of DAC is its flexibility and user-friendliness. Users can share files with specific colleagues by modifying their ACLs without requiring administrator intervention, enabling rapid collaboration in business environments. This decentralized permission management model aligns with how most people naturally expect file sharing to work.

The fundamental security weakness of DAC is that it places trust in users to manage security correctly, and it provides no protection against compromised user accounts. When a user's account is compromised by a Trojan or through credential theft, the attacker inherits all of that user's DAC permissions, including the ability to modify ACLs on resources the user owns. An attacker with access to a user's account can silently grant themselves access to all of that user's files, share sensitive documents with external accounts, or modify ACLs to persist access even after the original account is recovered.

The "confused deputy problem" arises in DAC: if a program running with elevated user privileges is exploited, it can use those privileges to read or modify files the user owns but the program should not access. Trojan horses specifically exploit this: they run with the user's DAC permissions, silently accessing and exfiltrating files the user can read. DAC provides no mechanism to prevent a process running as the user from accessing any resource the user owns. This is why DAC systems require complementary controls, application whitelisting, behavioral endpoint detection, and data loss prevention, to detect and prevent unauthorized access by malicious processes operating within a user's permission scope.

The Confused Deputy Problem, first described by Norm Hardy in 1988, arises directly from DAC's model: a program that has been granted elevated privileges to perform a specific task can be manipulated, "confused", into using those privileges to access resources outside the intended scope. Early ransomware families exploited DAC extensively: once executed with the user's privileges, they could access and encrypt every file the user had permission to read, including mapped network drives and shared folders, because DAC provides no mechanism to distinguish between the legitimate user and a malicious process operating in their security context. CVE-2022-30190 (Follina) demonstrated this dynamic in a modern context: a Word document exploit that executed MSDT.exe (Microsoft Support Diagnostic Tool) under the user's DAC permissions, allowing arbitrary code execution without requiring Administrator rights. The fact that these exploits operate entirely within the user's legitimate DAC permission boundary is precisely why behavioral EDR (not DAC itself) must be the primary control against malicious process activity in DAC environments.
:::

%%%
---
unit: Models
code: MAC
title: Mandatory Access Control (MAC)
---
:::callout style=soft
**Mandatory Access Control (MAC)** restricts access based on security labels assigned to both subjects (users) and objects (files). These access policies are enforced centrally by the operating system kernel.
:::

:::code language=mermaid caption="Bell-LaPadula Confidentiality Model, formal security model defining permitted information flows across classification levels to prevent unauthorized disclosure"
graph TD
    subgraph Secret Level
    %% A user with Secret clearance CAN read files at their own level (Simple Security Property)
    S_User[User Clearance: Secret] -->|Simple Property: Read Allowed, same level read is permitted| S_File[File Classification: Secret]
    %% A user with Secret clearance CANNOT write DOWN to Confidential (Star Property prevents downgrade)
    S_File -->|Star Property: Write Down Denied, prevents classified data leaking to lower level| C_File[File Classification: Confidential]
    end
    subgraph Confidential Level
    %% A user with Confidential clearance CAN read at their level
    C_File -->|Simple Property: Read Allowed, same level read is permitted| C_User[User Clearance: Confidential]
    %% A Confidential user CAN write UP to Secret level (they can contribute information upward)
    C_User -->|Star Property: Write Up Allowed, information can flow upward to higher classification| S_File
    end
:::

:::steps
1. **Clearance Assignment:** A system security administrator evaluates the user's need-to-know and assigns a subject clearance label (e.g., Unclassified, Confidential, Secret, Top Secret).
2. **Object Classification:** Data owners or administrators assign a classification label to each object (file, directory, database record) based on the sensitivity of its content.
3. **Access Request Interception:** A subject attempts to read or write an object, the access request is intercepted by the MAC enforcement engine in the operating system kernel before any data is transferred.
4. **Simple Security Check (Read):** The kernel checks whether the subject's clearance level is greater than or equal to the object's classification level, if not, reading is denied (no read up).
5. **Star Property Check (Write):** The kernel checks whether the subject's clearance level is less than or equal to the object's classification level, if not, writing is denied (no write down).
6. **Access Decision Enforcement:** Both checks must pass for the request to be granted, if either the Simple Security or Star Property rule is violated, the request is denied regardless of owner preferences or user intent.
:::

:::image src="images/18_mac_bell_lapadula.png" alt="Two-column diagram comparing Bell-LaPadula (Confidentiality) and Biba (Integrity) models side by side: Bell-LaPadula shows Top Secret, Secret, Confidential, and Unclassified levels with 'no read up' and 'no write down' arrows; Biba shows High, Medium, Low integrity levels with 'no read down' and 'no write up' arrows, a combined legend explains each rule prevents a specific type of unauthorized information flow" caption="Bell-LaPadula and Biba formal security models, mathematical frameworks that define provably secure information flow policies for confidentiality and integrity respectively" width=full:::
:::

:::notes
Mandatory Access Control (MAC) is a strict, non-discretionary access model used in high-security environments including government intelligence agencies, military command and control systems, classified databases, and financial systems with strong data compartmentalization requirements. It is called "mandatory" because access policies are enforced by the operating system kernel regardless of what the resource owner desires, neither users nor resource owners have discretion over access decisions. All access policy is centrally defined by a system security administrator and enforced uniformly.

MAC implements access control through security labels. Every subject (user, process, or program) is assigned a clearance label that represents their authorization level. Every object (file, directory, database record, network socket) is assigned a classification label that represents the sensitivity of the data it contains. The access control engine evaluates any access request by comparing the subject's clearance label against the object's classification label, according to rules defined by a formal security model.

The Bell-LaPadula Model (BLP), developed by David Bell and Leonard LaPadula for the US Air Force in 1973, is the most widely studied formal MAC security model. BLP focuses exclusively on confidentiality protection. It defines two fundamental properties:

The **Simple Security Property** ("no read up") states that a subject at clearance level X cannot read an object at classification level Y if Y is higher than X. A user with "Confidential" clearance cannot read "Secret" documents. This prevents unauthorized disclosure of classified information to users without the appropriate clearance.

The **Star Property** (written as *-property, "no write down") states that a subject at clearance level X cannot write data to an object at classification level Y if Y is lower than X. A user with "Secret" clearance cannot write to a "Confidential" document. This prevents a cleared user from intentionally or accidentally leaking classified information into lower-classification documents that less-cleared users can access.

The BLP model guarantees confidentiality but makes no guarantees about data integrity, it prevents information from flowing downward but would allow a low-clearance user to write corrupt data upward. The **Biba Integrity Model**, developed by Kenneth Biba in 1977, provides the complementary integrity protections. Biba defines its own two properties:

The **Simple Integrity Property** ("no read down") prevents a subject at integrity level X from reading an object at a lower integrity level Y. This prevents contamination of high-integrity processes by potentially corrupt low-integrity data.

The **Star Integrity Property** ("no write up") prevents a subject at integrity level X from writing to an object at higher integrity level Y. This prevents a low-integrity process from corrupting high-integrity data.

Real-world MAC implementations include the SELinux (Security-Enhanced Linux) security framework, which implements MAC for Linux systems using Type Enforcement policies, and the mandatory integrity controls in modern Windows (Medium, High, and System integrity levels for processes). The principle is also visible in iOS's sandboxing model, where applications cannot access resources outside their designated container regardless of user permissions.

SELinux, originally developed by the NSA and released as open-source in 2000, provides a practical MAC implementation for Linux systems through Type Enforcement (TE) policies. Every process and file in an SELinux-enabled system is assigned a security context (user:role:type:level), and policy rules define which process types may access which file types. If a web server process is compromised through a CVE exploit, SELinux confines the attacker to only the file types that the web server type is permitted to access, preventing lateral movement to system configuration files, user home directories, or SSH keys, even if the attacker achieves code execution within the web server process. This directly addresses the Confused Deputy Problem that DAC cannot prevent. The Common Criteria Evaluation Assurance Level (EAL) framework, an international standard (ISO/IEC 15408), provides formal certification of MAC-capable operating systems: systems targeting EAL4+ and above must implement formal security models (such as Bell-LaPadula) to achieve certification, which is required for many government procurement contracts.
:::

%%%
---
unit: Models
code: ABA
title: Attribute-Based Access Control (ABAC)
---
:::callout style=soft
**Attribute-Based Access Control (ABAC)** determines access rights by evaluating policies against the attributes of the subject, the object, the requested action, and environmental conditions.
:::

::::columns ratio=1:1
::col::
::::card heading="ABAC Attribute Categories"
:::list style=plain
- **Subject Attributes:** Properties of the user (e.g., job department, security clearance, training records).
- **Object Attributes:** Properties of the resource (e.g., file owner, classification label, creation date).
- **Environmental Attributes:** Contextual variables (e.g., current time, source IP address, device health status).
:::
::::
::col::
::::card heading="Access Policy Example"
:::code language=text caption="ABAC policy rule, evaluates four attribute categories simultaneously to produce an access decision"
Allow Subject to Read Object IF:
  Subject.Department == "Engineering" AND
  Object.Type == "SourceCode" AND
  Environment.SourceNetwork == "CorporateVPN" AND
  Environment.TimeOfAccess >= 08:00 AND
  Environment.TimeOfAccess <= 18:00
  %% This rule: only Engineering staff, only source code files,
  %% only from the corporate VPN, only during business hours
  %%, four conditions must ALL be true simultaneously
:::
::::
::::

:::flow
Subject sends an access request to a protected resource endpoint
Policy Enforcement Point (PEP) intercepts the request before it reaches the resource
PEP packages the request metadata and forwards it to the Policy Decision Point (PDP)
PDP retrieves subject attributes from the identity store (department, role, clearance, device compliance)
PDP retrieves object attributes from resource metadata (classification label, data type, sensitivity tier)
PDP retrieves environmental attributes in real time (current time, source network, source IP geolocation)
PDP evaluates all attribute sets simultaneously against applicable policy rules in the Policy Store
PDP issues a Permit or Deny decision, deny overrides permit if multiple rules produce conflicting decisions
PEP enforces the decision: grants access or returns a 403 Forbidden response to the requesting subject
All evaluated attributes and the access decision are written to the audit log for compliance and forensic purposes
:::

:::image src="images/18_abac_policy_engine.png" alt="ABAC policy evaluation engine diagram: input arrows from Subject Attributes (user profile), Object Attributes (resource metadata), and Environmental Attributes (time, location, device) all feeding into a central Policy Decision Point (PDP) which evaluates rules from a Policy Store, the PDP outputs permit or deny to a Policy Enforcement Point (PEP) that controls access to the resource" caption="ABAC policy evaluation architecture, the Policy Decision Point evaluates multi-dimensional attribute sets against stored policies to produce dynamic, context-aware access decisions" width=full:::
:::

:::notes
As organizations modernize their infrastructures through cloud adoption, remote work, and zero-trust architectures, traditional access control models like RBAC begin to show scalability and flexibility limitations. RBAC's role-based abstraction works well when job functions are relatively stable and resource access requirements align cleanly with roles. However, in dynamic environments where access decisions must account for contextual factors, the requester's physical location, the health status of their device, the time of day, the sensitivity of specific data fields within a document, RBAC requires the creation of increasingly specific roles to capture each distinct access scenario. This "role explosion" can result in organizations managing thousands of roles that are nearly as difficult to audit as direct user-to-resource permissions.

Attribute-Based Access Control (ABAC), defined in NIST SP 800-162, addresses these limitations by shifting from a static role membership model to a dynamic, policy-based decision model. In ABAC, access decisions are made by evaluating a policy rule that considers attributes from multiple categories simultaneously. NIST SP 800-162 identifies four primary attribute categories: subject attributes (properties of the requesting user or process), object attributes (properties of the resource being accessed), action attributes (the specific operation being requested, read, write, delete, execute), and environmental attributes (contextual properties of the access request, time, location, device compliance status, network connection type).

This multi-dimensional evaluation enables access policies of remarkable precision. Consider a healthcare example: "Allow a physician (subject.role == 'Physician') to read a patient record (object.type == 'PatientRecord') during a scheduled appointment (object.appointmentStatus == 'Active') from a hospital-issued device (environment.deviceManaged == true) located within the hospital network (environment.network == 'HospitalNetwork'), but not after the appointment ends, not from personal devices, and not from external networks." This single ABAC rule captures an access scenario that would require dozens of RBAC roles to approximate.

ABAC is the access control model underlying cloud-native identity and access management (IAM) systems. AWS IAM policies, Azure RBAC condition expressions, and Google Cloud IAM conditions are all implementations of ABAC principles, allowing administrators to write fine-grained policies that evaluate resource tags, request conditions, and environmental context. ABAC is also a fundamental component of zero-trust network access (ZTNA) architectures, where every access request is evaluated in full context rather than relying on network location (such as "inside the VPN") as a trust proxy.

The primary operational cost of ABAC is its complexity. Writing, testing, and auditing ABAC policies requires a more sophisticated policy management infrastructure and greater security engineering expertise than RBAC role assignment. Policy conflicts, where two rules would produce contradictory permit and deny decisions for the same request, require a conflict resolution mechanism (typically "deny overrides permit" for security purposes). Despite these complexities, ABAC is increasingly the preferred model for organizations operating in cloud environments, as it provides the flexibility to implement zero-trust principles without the scalability limitations of role-based models.

AWS IAM policy language is one of the most widely deployed ABAC implementations. An IAM policy that permits an EC2 instance to read from only S3 buckets tagged with `Environment=Production` and `DataClassification=Internal`, evaluated only when the request originates from a specific VPC, implements four-dimensional ABAC: subject attributes (instance role), object attributes (S3 bucket tags), environmental attributes (source VPC), and action attributes (GetObject). NIST SP 800-162 (Guide to Attribute Based Access Control Definition and Considerations) provides the federal standard for ABAC implementation, defining the Policy Decision Point (PDP), Policy Enforcement Point (PEP), Policy Administration Point (PAP), and Policy Information Point (PIP) as the architectural components of an ABAC system. ABAC is foundational to the Zero Trust principle of "never trust, always verify" because it enables the granular, context-sensitive policies necessary to evaluate each request individually rather than granting broad session-level access based on a single authentication event.
:::

%%%
---
unit: Comparison
code: CMP
title: Access Control Models Comparison
---
:::table
| Access Model | Access Decided By | Granularity | Implementation Complexity | Primary Use Case | Standard Reference |
|---|---|---|---|---|---|
| **DAC** | Resource Owner | Low | Low | General-purpose filesystems & document sharing | TCSEC Orange Book |
| **MAC** | System Administrator | High | High | Military & Government systems; classified databases | Bell-LaPadula / Biba |
| **RBAC** | Organizational Roles | Medium | Medium | Business enterprise networks & enterprise applications | ANSI/INCITS 359-2004 |
| **ABAC** | Multi-attribute Rules | Very High | High | Cloud infrastructure (AWS IAM), zero-trust networks | NIST SP 800-162 |
:::

:::image src="images/18_access_control_comparison.png" alt="Four-quadrant diagram comparing access control models on two axes: Security Rigidity (low to high on Y-axis) and Management Flexibility (low to high on X-axis), DAC in lower-right (high flexibility, low rigidity), RBAC in center (balanced), MAC in upper-left (high rigidity, low flexibility), and ABAC in upper-right (high rigidity and flexibility with policy-based dynamic rules)" caption="Access control model selection framework, choosing the right model requires balancing security requirements, management overhead, and operational flexibility" width=full:::
:::

:::notes
This comparative table summarizes the four primary access control models, providing a framework for selecting the appropriate model given an organization's specific security requirements, operational environment, and administrative capabilities. The choice of access control model is not merely a technical decision, it reflects the organization's fundamental security philosophy and risk tolerance.

Discretionary Access Control represents the "usability-first" end of the spectrum. Its decentralized, owner-controlled model minimizes administrative overhead and maximizes user flexibility, making it well-suited for collaborative business environments where users need to share documents and resources quickly. However, DAC's security guarantees are entirely dependent on users making correct access decisions, a premise that consistently fails in practice due to user error, social engineering, and malware that runs with user privileges. For environments handling sensitive regulated data (healthcare records, financial data, legal documents), DAC alone provides insufficient security and must be supplemented with additional controls.

Mandatory Access Control represents the "security-first" end of the spectrum. Its centrally enforced, label-based model provides mathematically provable confidentiality (through Bell-LaPadula) and integrity (through Biba) guarantees. No user, regardless of their privileges, can configure the system to violate the defined information flow rules. This rigidity, while highly secure, creates operational friction in environments that require frequent collaboration across classification levels. MAC is appropriate for environments where the consequences of confidentiality failure are catastrophic, intelligence systems, military command networks, and classified databases, but its operational overhead makes it unsuitable for general enterprise use.

Role-Based Access Control occupies the practical middle ground that makes it the dominant enterprise choice. It provides significantly stronger security than DAC by removing per-resource user discretion, while remaining administratively manageable through the role abstraction layer. The key operational challenge with RBAC is maintaining role hygiene, ensuring roles remain well-defined and that users are not assigned to roles beyond their operational requirements. When RBAC implementations develop "role explosion" or allow excessive role accumulation by individual users, their security benefits erode.

Attribute-Based Access Control provides the most sophisticated access control model available, enabling context-aware, dynamic policies that adapt to changing environmental conditions. It is particularly powerful in cloud and zero-trust environments where traditional network perimeters do not exist and access must be evaluated based on the totality of request context rather than network location or simple role membership. The operational cost is policy management complexity, which requires mature security engineering practices and robust policy testing frameworks.

Most large organizations implement hybrid models. A typical architecture might use RBAC to manage baseline access to enterprise applications, ABAC conditions to add context-sensitive restrictions (such as requiring device compliance or specific network connections for accessing sensitive resources), and MAC classification labels for the most sensitive data repositories. Understanding these models and their tradeoffs is essential for designing access architectures that balance security effectiveness with operational sustainability.

The TCSEC (Trusted Computer System Evaluation Criteria, the "Orange Book"), published by the US Department of Defense in 1983, first formalized the distinction between DAC and MAC in an evaluation framework. TCSEC Level C2 requires DAC with audit capabilities; Levels B1 and above require MAC with security labels. The Common Criteria framework superseded TCSEC internationally but preserves the same fundamental hierarchy, with Protection Profile requirements mapping to DAC (lower assurance levels) and MAC (higher assurance levels). Organizations subject to HIPAA's Security Rule must implement access controls (45 CFR §164.312(a)) that ensure only authorized persons or software programs access protected health information, a requirement satisfied through RBAC role assignment with ABAC conditions enforcing context-based access, demonstrating that access control model selection is frequently driven by regulatory compliance requirements as much as by security architecture preferences.
:::

%%%
---
unit: Principles
code: NTK
title: The Need-to-Know Principle
---
:::callout style=soft
**Need-to-Know** is a MAC-derived access control principle stating that a subject may access sensitive information only if that access is necessary to perform a specific, authorized task, even if the subject holds sufficient clearance to read it.
:::

::::columns ratio=1:1
::col::
::::card heading="Clearance vs. Need-to-Know"
:::list style=plain
- **Clearance:** The maximum classification level a subject is authorized to access.
- **Need-to-Know:** The specific compartment or project the subject is currently working on.
- **Both Required:** Clearance is necessary but insufficient. The subject must also demonstrate operational need.
- **Compartmentalization:** Data is divided into isolated compartments, each requiring separate need-to-know justification.
:::
::::
::col::
::::card heading="Enterprise Applications"
:::list style=plain
- **Project-Based Access:** Developers receive repository access only for their active sprint assignments.
- **HR Data:** Payroll staff access salary data; HR generalists see only role and department information.
- **Legal Hold:** Attorneys with matter access can read documents; other legal staff cannot.
- **Medical Records:** Physicians can view active patients; not historical patients they never treated.
:::
::::
::::

:::image src="images/18_needtoknow_compartments.png" alt="Grid diagram showing four classified compartments (Alpha, Bravo, Charlie, Delta) as separate boxes, User A (Secret clearance) is shown with access only to compartment Alpha and Bravo (highlighted), but not Charlie or Delta, even though their clearance level technically covers all four compartments, illustrating that clearance is a ceiling, not a blanket access grant" caption="Need-to-Know compartmentalization, clearance establishes a ceiling but not a blanket grant; each compartment requires a separate, justified need-to-know determination" width=full:::
:::

:::notes
The Need-to-Know principle is a crucial refinement to clearance-based MAC models and has important application in commercial access control as well. In government and military systems, the principle resolves a critical problem: if clearance level alone determined access, a Secret-cleared analyst working on signals intelligence would be able to read every Secret-classified document in the entire organization, including human intelligence reports, procurement plans, operational orders, and diplomatic cables that have absolutely no bearing on their job function. This would create enormous risks: an analyst who turns dissident, gets coerced, or has their account compromised would be a single point of failure for the entire collection of Secret-level information.

The Need-to-Know principle addresses this by adding a second dimension to access control: beyond clearance level, a subject must also be working on the specific project, program, or mission that the data relates to. The data is divided into compartments that are logically independent of one another. Access to a compartment requires both the appropriate clearance level AND a separate determination that the subject has an operational need to access that specific compartment. This is the architectural foundation of the Sensitive Compartmented Information (SCI) classification system used by the US intelligence community, having a Top Secret clearance does not grant access to SCI compartments; those require additional Special Access Program (SAP) authorizations.

In commercial enterprise environments, need-to-know manifests as project-based access controls layered on top of role-based permissions. A developer who holds the "Software Engineer" role gets access to the software development tools, build systems, and staging environments. But within that role, access to individual source code repositories is controlled at the project level: the developer receives access to repositories for their currently assigned projects, not all repositories across the engineering organization. This is precisely the model used by GitHub Organizations and GitLab Groups: role-based access (Member, Developer, Maintainer) is combined with project-level membership to enforce need-to-know at the repository level.

The principle becomes critical in data privacy contexts. GDPR Article 5(1)(b) states that personal data shall be "collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes", a data minimization requirement. Applying need-to-know at the data access layer, ensuring that each employee can only access the personal data records relevant to their current business purpose, is a technical implementation of this legal principle. An HR platform that allows all HR staff to see all employee salary data (rather than restricting compensation specialists to compensation records and HR generalists to non-compensation data) violates need-to-know and potentially GDPR's data minimization principle.

The Edward Snowden case (2013) is the most prominent real-world illustration of the consequences of inadequate need-to-know implementation at scale. Snowden, working as an NSA contractor, had a Top Secret/SCI clearance that, in combination with administrative access privileges and weaknesses in the NSA's access control architecture, allowed him to access and exfiltrate intelligence reports far beyond the scope of his assigned mission. Post-Snowden reviews of NSA access controls led to significant reforms, including privileged access management for administrator accounts, enhanced monitoring and user behavior analytics, and stricter compartmentalization enforcement, changes that demonstrate the very access control principles we cover in this lecture.

Need-to-know restricts access to what a role actually requires, and it is commonly violated: staff who can view all customer records rather than their assigned accounts, HR staff who can see executive compensation irrelevant to their work, or database administrators with read access to all tables. NIST SP 800-53 AC-3(3) enforces need-to-know alongside clearance level, requiring access based on both authorization and operational necessity.
:::

%%%
---
unit: Deep Dive
code: PAM
title: Privileged Access Management (PAM)
---
:::callout style=soft
**Privileged Access Management (PAM)** is a security discipline and toolset that governs, monitors, and records the activity of privileged accounts, the accounts that can bypass or reconfigure access controls on other accounts.
:::

:::list style=plain
- **Privileged Accounts:** Root, Administrator, Service Accounts, Database Owners, Network Device Admin accounts, any credential that can modify system configurations, access control policies, or other accounts.
- **Vaulting:** PAM stores privileged credentials in an encrypted vault, never exposing the actual password to the human operator, they check out a session rather than learning the password.
- **Session Recording:** Every privileged session is recorded (keystrokes, commands, screen capture) and archived for forensic review and compliance.
- **Just-in-Time (JIT) Access:** Privileged rights are granted only for the duration of an approved work order, then automatically revoked, accounts do not carry persistent elevated rights.
- **Dual Control / Four-Eyes:** Critical operations (production database changes, firewall rule modifications) require approval from a second administrator before execution.
:::

:::table
| PAM Capability | Security Benefit | NIST Control |
|---|---|---|
| Credential Vaulting | Humans never see privileged passwords | AC-2, IA-5 |
| Session Recording | Full forensic audit of all privileged activity | AU-2, AU-12 |
| Just-in-Time Access | Eliminates persistent privileged accounts | AC-6(2) |
| Dual Control | Prevents single-admin sabotage or error | AC-5 |
| Privileged Account Discovery | Finds unknown or orphaned privileged accounts | AC-2(1) |
:::

:::image src="images/18_pam_architecture.png" alt="PAM architecture diagram: an administrator requests a privileged session through the PAM portal, the PAM system checks an approval workflow, retrieves credentials from the encrypted vault, establishes a proxied session to the target server, and records all keystrokes and screen activity to a tamper-evident audit archive, the administrator never sees the actual credential" caption="PAM architecture, privileged sessions are proxied, recorded, and time-limited, with credentials stored in an encrypted vault and never exposed directly to operators" width=full:::
:::

:::notes
Privileged accounts are the most dangerous class of credentials in any organization. Unlike standard user accounts, privileged accounts can modify access control configurations, create new accounts with elevated rights, disable security controls, access encrypted data at rest, and erase audit logs. If a privileged account is compromised, through phishing, insider threat, or credential theft, the attacker essentially has the same capabilities as the organization's system administrators. This is why adversaries aggressively target privileged credentials during attack campaigns: the MITRE ATT&CK framework lists "Valid Accounts: Domain Accounts" (T1078.002) as one of the most commonly observed techniques for privilege escalation and persistence, with the 2022 Verizon DBIR noting that privilege abuse was a factor in 74% of breaches involving insiders.

Privileged Access Management (PAM) emerged as a security discipline specifically to control, monitor, and audit the activity of privileged accounts. The core design principle of PAM is that privileged credentials should be stored, managed, and used in a way that protects them from exposure, even to the administrators who use them. This is accomplished through credential vaulting: privileged passwords are stored in an encrypted vault (such as CyberArk Enterprise Password Vault, HashiCorp Vault, or BeyondTrust Password Safe). When an administrator needs to perform a privileged task, they authenticate to the PAM system, request access to a specific target system for a specific purpose, receive approval (either automated based on policy or manual from a change management system), and are then connected to the target system through a session proxy. The actual password to the target system is retrieved by the PAM system from the vault and injected into the session automatically, the human administrator never sees or knows the password. After the session ends, the password is automatically rotated, ensuring that even if the administrator noted the password during the session (which they cannot, as it was never displayed), the credential is no longer valid.

Session recording extends accountability far beyond traditional access logs. While NIST SP 800-53 AU-2 requires audit logging of security-relevant events, logs only capture what the system was told to record. PAM session recording captures everything that happens during a privileged session, every command typed, every file browsed, every configuration changed, every piece of data viewed. These recordings are stored in a tamper-evident archive and can be played back exactly like a video recording for forensic investigation. This capability is essential for insider threat investigations and provides a level of accountability that dramatically changes the risk calculus for administrators considering abuse of their privileges.

Just-in-time (JIT) access is the most powerful PAM control for eliminating persistent privilege. In traditional environments, privileged accounts exist continuously, the "root" account on a Linux server or the "Administrator" account on a Windows server is always present and always holds its full privileges. If these credentials are stolen, an attacker has permanent access. JIT access eliminates this window: instead of persistent privileged accounts, the PAM system creates time-limited privilege grants when a legitimate need is approved. An administrator requesting access to a production database server for a specific change ticket receives a time-limited account (valid for, say, two hours) with the minimum permissions needed for that specific task. After the time window expires, the account is automatically disabled or deleted. This dramatically reduces the attack surface by eliminating the class of credential that attackers most want to steal.

Leading PAM products include CyberArk Privileged Access Security (the enterprise market leader), BeyondTrust Privileged Remote Access, Delinea (formerly Centrify and Thycotic), and HashiCorp Vault (particularly strong in DevOps and cloud-native environments). Microsoft's Privileged Identity Management (PIM), included in Azure AD Premium P2, provides JIT access for Azure and Microsoft 365 administrative roles without requiring a dedicated PAM product, making it accessible to organizations already invested in the Microsoft ecosystem.

In the 2020 SolarWinds attack, weak privileged-account controls let attackers escalate and persist for months. They specifically targeted identity infrastructure, Active Directory, Azure AD and federation services, because compromising it let them forge authentication tokens and bypass access controls. NIST SP 800-53 AC-6(2) requires administrators to use standard accounts for non-administrative work, the just-in-time principle whose violation this attack illustrates.
:::

%%%
---
unit: Deep Dive
code: IAM
title: Identity & Access Management (IAM) Lifecycle
---
:::callout style=soft
**Identity and Access Management (IAM)** is the set of processes, policies, and technologies that manage digital identities and their associated access rights across an organization's entire lifecycle from account creation to deprovisioning.
:::

:::steps
1. **Provisioning (Joiner):** A new employee's identity is created in the authoritative identity store (Active Directory, Okta, Azure AD). Role assignments are made based on job function, granting initial access to required systems.
2. **Access Certification:** Within 30 days, a manager reviews and certifies the access rights assigned to the new employee to confirm they are appropriate for the role.
3. **Movers (Role Change):** When the employee changes roles, a lifecycle event triggers: old role access is revoked and new role access is provisioned, preventing privilege accumulation.
4. **Periodic Access Review:** Quarterly (privileged accounts) or annually (standard accounts), managers recertify each direct report's access rights against their current job requirements.
5. **Termination (Leaver):** When the employee leaves, an HR system event triggers immediate account suspension across all integrated systems within minutes, not days.
6. **Orphan Account Remediation:** Automated discovery tools scan for accounts with no corresponding active HR record, these orphaned accounts are flagged and disabled.
:::

:::image src="images/18_iam_lifecycle.png" alt="Circular lifecycle diagram with five phases: Provisioning (new account creation with role assignment), Access Review (periodic manager certification), Role Change (mover process with access adjustment), Offboarding (automatic deprovisioning), and Orphan Discovery (automated scan for stale accounts), arrows connect phases in a cycle with NIST SP 800-53 AC-2 label in the center" caption="IAM joiner-mover-leaver lifecycle, identity governance ensures access rights stay aligned with current job requirements throughout an employee's tenure" width=full:::
:::

:::notes
Identity and Access Management (IAM) is often treated as a technical system configuration task, but it is more accurately understood as a governance discipline that uses technology to enforce organizational policies about who should have access to what. The technology components, identity providers, directory services, provisioning systems, access governance platforms, are merely the mechanisms that enforce policies defined by HR, legal, security, and business units. When IAM fails, it typically fails because the technology is present but the governance processes are absent: no one is responsible for reviewing access after initial provisioning, no automated process triggers access revocation when an employee leaves, and no one audits whether existing access rights still match current job requirements.

The Joiner-Mover-Leaver (JML) framework provides the process model for IAM lifecycle governance. The Joiner process covers everything that happens when a new employee, contractor, or service account is created: HR records the new hire in the authoritative HR system, an automatic integration pushes the identity to the identity store (Active Directory, Okta, Azure AD), role assignments are made based on the job title or department, and the new account is provisioned across all integrated application systems. Critically, this provisioning should be based on a predefined role profile, a set of access rights that have been pre-approved as appropriate for a given job function, rather than ad-hoc assignments decided by the hiring manager at the time of onboarding.

The Mover process is the most frequently neglected aspect of IAM lifecycle management. When an employee transfers departments, changes roles, or takes on a new project, their access rights should be updated to reflect their new responsibilities, both adding new access and removing old access that is no longer needed. In practice, organizations routinely add new access for the new role while failing to remove old access from the previous role. Over time, employees who have changed roles multiple times accumulate a patchwork of access rights spanning every system they ever touched. This "privilege creep" or "permission sprawl" is one of the most common access control findings in security audits and penetration tests.

The Leaver process, deprovisioning when an employee leaves, is where IAM failures have the most immediate and dramatic security consequences. The 2021 Colonial Pipeline attack was enabled by an unused VPN account belonging to a former employee; the 2020 Shopify breach involved two rogue employees who had access to customer data because of inadequate access controls for their job roles; countless other breaches have begun with credentials belonging to former employees, vendors, or contractors who retained active accounts after their relationship with the organization ended. NIST SP 800-53 AC-2 requires that organizations "disable accounts when no longer required", deprovisioning is a compliance requirement, not just an operational best practice.

Automated deprovisioning, triggered by HR system events, is the technical solution. When HR marks an employee as terminated, an integration platform (such as Okta Lifecycle Management, Microsoft Identity Governance, or SailPoint) automatically suspends or deletes the corresponding accounts across all integrated systems, Active Directory, email, VPN, cloud applications, badge access, within a defined time window, typically within one hour of the HR event. This eliminates the manual, error-prone process of asking IT to "disable John's account" when John leaves.

Access reviews, periodic recertification of existing access rights, are the control that catches privilege creep and ensures long-term alignment between access rights and job requirements. Modern identity governance platforms (SailPoint IdentityNow, Saviynt, One Identity) automate access review campaigns: they generate a list of each manager's direct reports and their current access rights, send the manager a certification task in their email or manager portal, track which accesses have been certified as appropriate and which have been flagged for revocation, and automatically submit revocation requests for flagged access. Certification completion rates and revocation statistics feed directly into compliance reporting for SOX, HIPAA, ISO 27001, and other regulatory frameworks that require periodic access reviews. NIST SP 800-53 AC-2(7) requires privileged accounts to be reviewed more frequently than standard accounts, reflecting the higher risk associated with privileged credential compromise.

Access certification, in which managers periodically confirm that their reports still need particular access, is a core governance control, but it is often treated as a checkbox exercise where managers certify all access without examining it. Genuine review prevents the privilege creep that attackers exploit.
:::

%%%
---
unit: Principles
code: SOD
title: Separation of Duties, Worked Examples
---
:::callout style=soft
**Separation of Duties (SoD)** divides high-risk tasks between multiple individuals so that no single person can complete a sensitive transaction alone. It is the technical implementation of the "two-person rule" in security and financial control.
:::

::::columns ratio=1:1
::col::
::::card heading="Financial SoD Example"
:::list style=plain
- **Step 1, Create Payment:** Accounts Payable clerk creates vendor payment record in ERP system.
- **Step 2, Approve Payment:** Finance Manager approves payment in workflow system (separate account required).
- **Step 3, Release Payment:** Treasury officer releases the wire transfer from the banking system.
- **Step 4, Reconcile:** Internal Auditor reconciles bank statement against payment records.
- **Result:** Four distinct roles, four distinct system permissions. Fraud requires collusion across all four.
:::
::::
::col::
::::card heading="IT Operations SoD Example"
:::list style=plain
- **Step 1, Develop:** Developer writes code in development environment, no production access.
- **Step 2, Review:** Peer reviewer approves the pull request, cannot also be the submitter.
- **Step 3, Test:** QA engineer validates in staging, separate credentials from development.
- **Step 4, Deploy:** Release Manager deploys to production, cannot also be the developer who wrote the code.
- **Result:** Code sabotage requires compromise of at least two separate roles in a controlled pipeline.
:::
::::
::::

:::table
| Risk Scenario | SoD Control | Accounts Involved |
|---|---|---|
| Rogue financial transaction | Require separate Create and Approve roles | Accounts Payable + Finance Manager |
| Insider code sabotage | Enforce 4-eyes code review before deployment | Developer + Peer Reviewer + Release Manager |
| Unauthorized account creation | Separate AD provisioner from approval workflow | IT Help Desk + IT Manager |
| Database record tampering | No DBA can both write and audit their own queries | DBA + Database Auditor (read-only) |
| Data exfiltration via backup | Separate backup operator from backup media owner | Backup Admin + Tape Librarian |
:::

:::image src="images/18_separation_of_duties.png" alt="Two parallel flowcharts side-by-side: left shows financial transaction flow through four distinct role boxes (Clerk, Manager, Treasury, Auditor) with separate user icons at each step and a 'No single person can complete transaction alone' label; right shows DevOps pipeline flow through Developer, Reviewer, QA, and Release Manager with separate permission zones at each stage, both diagrams show a 'Fraud requires collusion' annotation" caption="Separation of Duties in financial and IT operations, critical transactions are split across multiple roles with distinct system permissions, requiring collusion for abuse to succeed" width=full:::
:::

:::notes
Separation of Duties (SoD) is one of the oldest internal control mechanisms in existence, it predates computing and originates in financial auditing practices dating back to medieval banking guilds. The principle is elegantly simple: if committing fraud or sabotage requires the cooperation of multiple independent individuals, it becomes exponentially more difficult because each additional person represents an additional opportunity for detection and refusal. A single dishonest employee can act alone; two dishonest employees must trust each other completely, both accept the risk, and coordinate their actions without being caught, a dramatically higher bar.

In financial systems, the classic SoD controls are well-established. The COSO Internal Control Framework (Committee of Sponsoring Organizations of the Treadway Commission), the authoritative standard for internal controls referenced in SOX compliance, identifies the separation of authorization, record-keeping, and custody as the three fundamental SoD divisions. No person who can authorize a transaction should also be able to execute it, record it in the ledger, or reconcile it against the bank statement. Each of these four functions, authorization, execution, recording, reconciliation, should be performed by a different individual with distinct system access. This four-way separation makes undetected fraud extremely difficult, as each step produces records visible to the next step's actor.

In IT operations, SoD takes the form of change control: a developer who writes code should not also be the person who deploys that code to production. This separation exists for two reasons. First, it prevents deliberate sabotage: a developer with production deployment rights could introduce malicious code directly into the production environment without review. Second, it provides quality control: a peer reviewer is more likely to catch logical errors, security vulnerabilities (such as SQL injection or hardcoded credentials), or business logic mistakes that the original developer, who is close to the code, might miss. NIST SP 800-53 AC-5 (Separation of Duties) requires organizations to "define duties of individuals requiring separation" and "implement separation of duties through assigned information system access authorizations." NIST SP 800-53 CM-4 (Security Impact Analysis) additionally requires that a separate review be conducted for configuration changes, implementing SoD in the change management process.

The database administrator role presents a persistent SoD challenge. DBAs typically need broad access to maintain database health, tune performance, resolve incidents, and manage schema changes. However, this same access enables them to view, modify, or delete any record in the database, including records they should not have access to for legitimate reasons (such as their own compensation records, executive data, or competitor pricing information). Effective SoD for DBA roles includes read-only audit accounts that DBAs cannot use to modify data (allowing auditors to verify what DBAs have accessed), privileged access management solutions that require approval before DBAs can run queries against sensitive tables, and database activity monitoring (DAM) tools that log all DBA query activity independent of the database's own logs (which a DBA could potentially alter).

The PCIDSS (Payment Card Industry Data Security Standard) Section 6.4.2 specifically requires SoD between development and production environments: "All customizations must be tested in a separate environment... and must be reviewed by individuals other than the developer..." This is a codification of the SoD principle in a payment security context, recognizing that without it, developers could introduce payment card data skimming code directly into production systems. The 2014 Home Depot breach, in which attackers compromised point-of-sale systems and exfiltrated 56 million payment card numbers over a five-month period, was partly enabled by inadequate SoD between IT operations teams with broad access, illustrating that when SoD controls are absent, the blast radius of a single insider threat or credential compromise can encompass the entire payment environment.

When a team is too small to separate all duties, compliance frameworks such as PCI DSS and ISO 27001 allow compensating controls, increased monitoring, more frequent access reviews, management sign-off on deployments, or automated security testing, in place of a full separation of duties. The risk of inadequate separation must be mitigated, not simply accepted.
:::

%%%
---
unit: Framework
code: NST
title: NIST SP 800-53 Access Control Family
---
:::callout style=soft
**NIST SP 800-53 Revision 5** defines the AC (Access Control) control family, 25 controls governing how federal systems and their contractors must implement, manage, and audit access control. These controls are widely adopted as the benchmark for enterprise access control programs.
:::

:::table
| Control | Name | Key Requirement |
|---|---|---|
| AC-1 | Policy and Procedures | Document access control policy; assign roles and responsibilities |
| AC-2 | Account Management | Create, modify, disable, and remove accounts; conduct access reviews |
| AC-3 | Access Enforcement | Enforce approved authorizations for logical access to the system |
| AC-5 | Separation of Duties | Define and enforce SoD for roles that, if combined, would create excessive risk |
| AC-6 | Least Privilege | Grant only the minimum permissions required; review periodically |
| AC-7 | Unsuccessful Logon Attempts | Lock accounts after a defined number of failed login attempts |
| AC-11 | Device Lock | Enable automatic device lock after inactivity |
| AC-17 | Remote Access | Authorize, document, and enforce restrictions on remote access |
| AC-19 | Access Control for Mobile Devices | Establish usage restrictions and guidance for mobile device access |
| AC-20 | Use of External Information Systems | Restrict connections to external systems not owned by the organization |
:::

:::image src="images/18_nist_ac_family.png" alt="Hierarchical diagram of NIST SP 800-53 AC family: AC-1 Policy at the top, branching to AC-2 Accounts and AC-3 Enforcement, then further branching to AC-5 SoD, AC-6 Least Privilege, AC-17 Remote Access, and AC-20 External Systems, each control node has a brief one-line description and its NIST SP 800-53 Rev 5 control identifier" caption="NIST SP 800-53 AC control family hierarchy, AC-1 policy governs all downstream controls, with AC-2 account management and AC-3 access enforcement as the foundational operational controls" width=full:::
:::

:::notes
NIST Special Publication 800-53 Revision 5, "Security and Privacy Controls for Information Systems and Organizations," is the most comprehensive and authoritative access control standard published by any government body. Originally developed for federal information systems under the Federal Information Security Management Act (FISMA), SP 800-53 has been broadly adopted as a security control framework by private-sector organizations across finance, healthcare, defense contracting, and critical infrastructure. The Access Control (AC) family, consisting of controls AC-1 through AC-25, provides a complete specification of access control policy, implementation, and operational management requirements.

AC-1, Policy and Procedures, is the foundational control that requires every organization to document its access control philosophy in a written policy and assign specific roles and responsibilities for access control administration. This control reflects the principle that technology controls without governance are insufficient, someone must be accountable for setting access policy, reviewing access decisions, and responding when access control fails. The policy must specify the types of access permitted, the procedures for granting and revoking access, and the frequency of access reviews.

AC-2, Account Management, is arguably the most operationally impactful control in the family. It requires organizations to maintain an inventory of all accounts (standard, privileged, service, shared, and guest accounts), define account types and their associated permissions, implement a formal process for account creation and modification that requires managerial approval, conduct periodic account reviews to identify and disable unnecessary accounts, and automatically disable or remove accounts when users separate from the organization. AC-2 directly addresses the privilege creep and orphaned account problems that enable so many real-world breaches.

AC-3, Access Enforcement, requires that the system technically enforces the access decisions made by administrators, ensuring that the implemented access controls actually reflect the defined policies, rather than policies existing on paper while the system enforces something different or nothing at all. This control is satisfied by the technical implementation of DAC, MAC, RBAC, or ABAC, the choice of model determines how AC-3 is implemented.

AC-6, Least Privilege, builds on AC-3 by requiring that the access decisions enforced by AC-3 adhere to the minimum necessary principle. AC-6 includes important enhancements: AC-6(1) requires authorizing access to security functions only to explicitly authorized personnel; AC-6(2) requires that users use non-privileged accounts for non-administrative activities (JIT privilege); AC-6(5) requires privileged accounts to be separate from standard user accounts (no dual-use accounts); and AC-6(9) requires logging of the use of privileged functions, ensuring that elevated access is fully auditable.

The NIST Cybersecurity Framework (CSF) 2.0, released in February 2024, reorganizes and references SP 800-53 controls within its six core functions: Govern, Identify, Protect, Detect, Respond, and Recover. The access control controls fall primarily within the Protect function, specifically the Identity Management, Authentication and Access Control (PR.AA) category. CSF 2.0 PR.AA-05 (Access permissions and authorizations are managed) maps directly to SP 800-53 AC-2, AC-3, AC-5, and AC-6, making the AC family controls the technical implementation of the CSF's identity protection requirements. Organizations that align to the CSF will find SP 800-53's AC family to be the control catalog they most directly implement.

FedRAMP (Federal Risk and Authorization Management Program), which provides cloud security authorization for federal agencies, mandates SP 800-53 AC controls as baseline requirements for all FedRAMP-authorized cloud service providers. A cloud service provider offering SaaS to federal agencies must implement all AC controls at the appropriate impact level (Low, Moderate, or High), have their implementation assessed by a FedRAMP-authorized third-party assessment organization (3PAO), and maintain continuous monitoring evidence of AC control effectiveness. This makes SP 800-53 AC controls effectively mandatory for any organization seeking to do business with the US federal government, extending their reach far beyond strictly government systems.

The NIST SP 800-53 Access Control family is directly referenced by Security+, CISSP and CISA exam objectives. The full SP 800-53 Rev. 5 document, freely available from csrc.nist.gov, gives the complete control text, parameters and supplemental guidance.
:::

%%%
---
unit: Case Study
code: TGT
title: Case Study, 2013 Target Data Breach
---
:::callout style=soft
The 2013 Target breach compromised 40 million payment card records and 70 million customer records, enabled by a third-party vendor's stolen credentials and inadequate network segmentation access controls.
:::

:::steps
1. **Initial Compromise (Nov 2013):** Attackers phish credentials from Fazio Mechanical, an HVAC contractor with remote access to Target's network for energy monitoring systems.
2. **Lateral Movement:** Fazio's remote access was not restricted to the HVAC management systems, it connected to the same network segments as Target's point-of-sale (POS) systems.
3. **POS Infection:** Attackers deploy BlackPOS malware ("Kaptoxa") to Target's point-of-sale terminals, capturing card data from magnetic stripe reads in RAM before encryption.
4. **Exfiltration:** Stolen card data is staged on a Target internal server, then exfiltrated to external servers in Eastern Europe over several weeks.
5. **Detection:** The US DOJ notifies Target in mid-December; the breach had been running undetected for three weeks.
6. **Impact:** 40 million credit/debit card numbers exposed; 70 million customer records (names, addresses, emails, phone numbers) stolen; $202 million total estimated cost to Target.
:::

:::list style=plain
- **Access Control Failures:** Vendor network access was not restricted to HVAC systems, violated least privilege and need-to-know.
- **Segmentation Failure:** POS network was not isolated from vendor-accessible network segments.
- **Monitoring Gap:** FireEye alerted the Target Security Operations Center to the POS malware, alerts were reportedly ignored or deprioritized.
:::

:::image src="images/18_target_breach_timeline.png" alt="Attack chain diagram for the 2013 Target breach: Phase 1 shows Fazio Mechanical credentials phished; Phase 2 shows attacker entering Target network via Fazio's remote access; Phase 3 shows lateral movement to POS network (with a dotted red line crossing what should have been a firewall boundary, labeled 'Access Control Failure'); Phase 4 shows BlackPOS malware deployed to POS terminals; Phase 5 shows data exfiltration to external C2 servers" caption="Target breach attack chain, the critical access control failure was granting a third-party HVAC vendor network connectivity that extended beyond the HVAC management environment into payment-processing network segments" width=full:::
:::

:::notes
The 2013 Target breach is one of the most thoroughly documented and analyzed retail security incidents in history, and it remains a canonical teaching example of how access control failures cascade into catastrophic data breaches. The breach is particularly instructive because it did not involve sophisticated zero-day exploits or novel attack techniques, it exploited straightforward access control weaknesses that NIST SP 800-53 controls explicitly address and that many organizations could have prevented with basic security hygiene.

The attack began not with Target's own systems but with a third-party contractor. Fazio Mechanical Services, a refrigeration and HVAC contractor based in Sharpsburg, Pennsylvania, had a remote access connection to Target's corporate network. This connection was established for legitimate business purposes: Fazio used it to remotely monitor and manage the climate control systems in Target stores. However, the key access control failure was that Fazio's remote access was not scoped to only the HVAC management systems. The network access was provisioned in a way that allowed Fazio's remote connection to reach other network segments within Target's environment, segments that had nothing to do with HVAC management and should have been inaccessible to a refrigeration vendor.

When attackers successfully phished credentials from Fazio Mechanical (likely through a spear-phishing email targeting Fazio employees), they gained access to a network account with connectivity into Target's network. From this initial foothold, they were able to conduct reconnaissance within Target's network and discover the point-of-sale system infrastructure. The access control failure that made lateral movement possible was the absence of proper network micro-segmentation: the POS network and the vendor-accessible network were not adequately isolated from one another, violating the principle of network access least privilege.

The NIST SP 800-53 controls that would have prevented or contained this breach are straightforward. AC-17(3) requires organizations to "employ automated mechanisms to monitor and control remote access methods", properly configured remote access would have restricted Fazio's VPN session to only the IP ranges serving HVAC management systems. AC-20 (Use of External Information Systems) requires policies defining restrictions on external system connections, which would have required Fazio's access to be reviewed and scoped. SC-7 (Boundary Protection) and network segmentation controls would have isolated the POS network from vendor-accessible segments. The fact that FireEye security software reportedly generated alerts about the malware before the breach's public disclosure, and that those alerts were not acted upon by Target's security operations center, illustrates that technical controls without operational processes and human response are insufficient, a point that underscores the importance of the full AAA triad (and SIEM/SOC monitoring) as complements to access control.

The financial consequences of the breach illustrate the business case for access control investment. Target paid $18.5 million in a multi-state settlement, faced at least $90 million in payment card fraud liability, spent millions on remediation, and suffered long-term brand and customer trust damage that affected revenue for years. The CEO and CIO both resigned in the aftermath of the breach. These costs vastly exceed what proper network segmentation, third-party access controls, and vendor access reviews would have cost to implement, making the Target breach a compelling return-on-investment argument for access control spending.

The breach also prompted regulatory and industry responses that changed access control standards for retail organizations. The Payment Card Industry Data Security Standard (PCIDSS) Requirement 1.3 requires that firewalls restrict inbound and outbound traffic to only that which is necessary for the cardholder data environment, a direct network-level access control requirement. PCIDSS Requirement 8.6 requires that accounts used by systems or software include controls to restrict their use, addressing the vendor account management failure in the Target case. The aftermath of the Target breach directly drove adoption of EMV chip-and-PIN payment cards in the United States, which addresses the specific attack vector (magnetic stripe data skimming in RAM) used in the breach, illustrating how access control failures at one layer drive compensating controls at other layers of the security architecture.

Target's security team received alerts about the malware that were reportedly seen but not escalated, which shows the relationship between access control and detection. Access controls reduce the blast radius and slow attackers, giving detection time to respond; when access control and detection both fail, a breach can run for weeks undetected.
:::

%%%
---
unit: Deep Dive
code: PRV
title: Privilege Escalation, Attack Patterns
---
:::callout style=soft
**Privilege Escalation** is the technique of exploiting a vulnerability, misconfiguration, or design weakness to gain more access rights than were originally granted. It is a critical attack phase between initial access and lateral movement.
:::

::::columns ratio=1:1
::col::
::::card heading="Vertical Privilege Escalation"
:::list style=plain
- **Definition:** Gaining higher-privilege access than granted, e.g., a standard user becomes local Administrator or root.
- **CVE-2021-34527 (PrintNightmare):** Windows Print Spooler vulnerability allowed standard users to execute code as SYSTEM.
- **Unquoted Service Paths:** Windows service paths with spaces and no quotes allow a lower-privileged user to place a malicious executable in the path.
- **SUID/SGID Abuse (Linux):** Executables with SUID bit run as the file owner (often root), allowing privilege escalation if the binary is exploitable.
:::
::::
::col::
::::card heading="Horizontal Privilege Escalation"
:::list style=plain
- **Definition:** Accessing resources of another user at the same privilege level, e.g., User A reads User B's files.
- **IDOR (Insecure Direct Object Reference):** CVE-style web vulnerability where changing a user ID parameter in a URL allows access to another user's records.
- **Session Hijacking:** Stealing an active session token to impersonate another user without knowing their credentials.
- **Credential Reuse:** A user uses the same password across systems, compromising one reveals access to another user's account on a different system.
:::
::::
::::

:::table
| Escalation Technique | Access Control Mitigation | NIST Control |
|---|---|---|
| Local Admin via vulnerability | Remove local admin rights from standard users | AC-6(2) |
| SUID/SGID abuse | Audit and restrict SUID binaries; use AppArmor/SELinux | AC-3, CM-7 |
| Kerberoasting (AD) | Use strong service account passwords; gMSA accounts | IA-5, AC-2 |
| Token impersonation | Restrict SeImpersonatePrivilege; use PAM | AC-6(5) |
| IDOR | Enforce server-side authorization on every object access | AC-3 |
:::

:::image src="images/18_privilege_escalation.png" alt="Two-path diagram showing vertical and horizontal privilege escalation: vertical path shows an attacker starting as a low-privilege user (bottom of pyramid) and exploiting a vulnerability to reach Administrator/root at the top; horizontal path shows an attacker at the same privilege level crossing to access another user's resources by exploiting IDOR or session hijacking, both paths are labeled with example CVEs and mitigations" caption="Privilege escalation patterns, vertical escalation gains higher privilege than granted; horizontal escalation accesses resources of peers at the same privilege level" width=full:::
:::

:::notes
Privilege escalation is the phase in an attack campaign that occurs after initial access and before the attacker can achieve their primary objective, whether that is data exfiltration, ransomware deployment, financial fraud, or sabotage. Almost all attack campaigns require some form of privilege escalation: initial access is frequently achieved through a standard user's compromised credentials or a vulnerability that provides limited execution context, while the final objective typically requires administrative or system-level access. Understanding privilege escalation techniques helps defenders design access control architectures that deny attackers the escalation paths they need.

Vertical privilege escalation, moving from a lower privilege level to a higher one, is the form most familiar from public vulnerability disclosures. CVE-2021-34527 (PrintNightmare) is a recent and widely exploited example: a vulnerability in the Windows Print Spooler service allowed an attacker who had a standard user account (or even network access without credentials) to install a malicious printer driver that executed code in the SYSTEM security context, the highest privilege level on a Windows machine. The vulnerability was particularly severe because Print Spooler runs as SYSTEM by default on all Windows machines, including domain controllers, meaning a standard domain user could potentially execute code as SYSTEM on a domain controller, effectively achieving domain compromise. NIST SP 800-53 AC-6(2) directly addresses this risk by requiring that "non-privileged accounts or roles" be used for "non-security functions," meaning that the Print Spooler service itself should not run as SYSTEM but rather as a limited service account with only the specific privileges needed for print management.

Kerberoasting is a Windows Active Directory-specific privilege escalation technique that abuses the Kerberos authentication protocol. Service accounts in Active Directory are identified by Service Principal Names (SPNs). Any domain user can request a Kerberos service ticket for any SPN, and these tickets are encrypted with the service account's password hash. An attacker with a standard domain user account can request service tickets for all service accounts in the domain, take those encrypted tickets offline, and crack them with GPU-accelerated password cracking tools. If the service account has a weak password, the attacker learns the service account's credentials, and many service accounts run with high privileges or even Domain Admin rights. The NIST control for Kerberoasting is IA-5(1), which requires that passwords meet minimum complexity requirements, but more specifically, the use of Group Managed Service Accounts (gMSA), which have 120-character randomly generated passwords that are automatically rotated and are computationally infeasible to crack offline, is the architectural mitigation.

Horizontal privilege escalation, accessing the resources of a peer at the same privilege level, is particularly prevalent in web application contexts through Insecure Direct Object Reference (IDOR) vulnerabilities. IDOR occurs when a web application uses a predictable, user-controlled identifier (such as a database record ID or username) to retrieve objects, and fails to verify that the authenticated user is authorized to access the specific object they are requesting. For example, if a web application retrieves account details via the URL `GET /api/account?id=12345` and simply returns the account with that ID without verifying that the logged-in user owns account 12345, an attacker who has account 12346 can modify the ID to 12345 and read another user's account details. IDOR vulnerabilities are consistently among the most common findings in web application penetration tests and are listed in the OWASP Top 10 under "Broken Access Control" (A01:2021). The NIST control is AC-3 (Access Enforcement), which requires that authorization checks be applied on every access to every object, a server-side check that verifies the requesting user's authorization to access the specific object, not merely whether they are logged in.

The Token Impersonation technique, exploiting the Windows SeImpersonatePrivilege or SeAssignPrimaryTokenPrivilege, allows an attacker who has compromised a service account (such as a web server or database service account) to impersonate higher-privileged tokens present on the system. Tools like Juicy Potato and PrintSpoofer automate this technique, allowing attackers to escalate from a limited service account to SYSTEM. Defending against token impersonation requires PAM controls that ensure service accounts are granted only the minimum Windows privileges needed (specifically, removing SeImpersonatePrivilege from accounts that don't absolutely require it) and SELinux/AppArmor policies that confine what actions compromised service processes can take even with their granted tokens. This illustrates the complementary relationship between DAC/access controls and MAC-style confinement: DAC controls limit what the service account can access directly, while MAC confinement prevents the service account from being used as a launch pad for privilege escalation techniques that exploit Windows token architecture.

MITRE ATT&CK tactic TA0004 (Privilege Escalation) documents real-world escalation techniques with incident examples, each mapped to mitigations that correspond to NIST SP 800-53 controls. Cross-referencing attacker techniques with defender controls is a core competency for SOC, red-team and architecture roles.
:::

%%%
---
unit: Framework
code: ZTA
title: Zero Trust Architecture (NIST SP 800-207)
---
:::callout style=soft
**Zero Trust Architecture (ZTA)** eliminates implicit trust based on network location and requires continuous verification of every access request regardless of source. The core principle: "Never trust, always verify."
:::

::::columns ratio=1:1
::col::
::::card heading="Traditional Perimeter Model"
:::list style=plain
- Trust is granted based on network location (inside = trusted).
- VPN provides broad network access once connected.
- Lateral movement is relatively unconstrained inside the perimeter.
- A single breached perimeter exposes the entire internal network.
- Authentication is one-time at network entry.
:::
::::
::col::
::::card heading="Zero Trust Model"
:::list style=plain
- No implicit trust from network location, inside is not trusted.
- Access is granted per-resource, per-session based on current context.
- Every lateral connection requires a separate authorization decision.
- A breached endpoint cannot freely access other internal resources.
- Authentication and authorization are continuous throughout the session.
:::
::::
::::

:::flow
User/device requests access to a specific resource
Identity Provider verifies the user's identity (MFA required)
Device compliance check: is the endpoint managed and patch-compliant?
Behavioral analytics check: is this request anomalous for this user?
Policy Engine evaluates all signals against ABAC/RBAC policy
Policy Administrator issues a time-limited, scoped access token
Policy Enforcement Point grants access to the specific resource only
Session continuously re-evaluated; anomalous behavior revokes access immediately
:::

:::image src="images/18_zero_trust_model.png" alt="Side-by-side comparison: left shows traditional castle-and-moat perimeter model with a hard perimeter boundary, trusted internal network, and attacker moving freely after crossing the perimeter; right shows Zero Trust model with no perimeter, every resource protected by its own Policy Enforcement Point, and continuous verification gates on every connection, NIST SP 800-207 label at top" caption="Zero Trust vs. perimeter security, Zero Trust eliminates the trusted interior by requiring continuous verification of every connection to every resource, regardless of network origin" width=full:::
:::

:::notes
Zero Trust Architecture represents the most significant shift in network security thinking in the past two decades. The term was coined by John Kindervag at Forrester Research in 2010, and the concept was formalized as a federal government standard by NIST in SP 800-207 (Zero Trust Architecture), published in August 2020. Zero Trust's core insight is that the traditional "castle and moat" perimeter security model, in which the network boundary is the primary security control and everything inside is trusted, has been fundamentally broken by three concurrent trends: the migration of applications to cloud environments outside the corporate perimeter, the growth of remote work that takes employees outside the physical perimeter, and the demonstrated ability of attackers to cross perimeters through phishing, supply chain attacks, and insider threats.

When an attacker breaches a traditional perimeter (by compromising VPN credentials, exploiting a perimeter firewall vulnerability, or obtaining access through a supply chain attack), they typically land inside a "trusted" network segment where they can move laterally with relatively little resistance. Most internal network traffic is assumed to be legitimate and is not subject to the same rigorous access controls as traffic crossing the perimeter boundary. This creates enormous advantages for attackers during the post-breach phase: once inside, they can conduct reconnaissance, establish persistence, escalate privileges, and move toward their objectives without triggering the perimeter-based controls that are the primary security investment in traditional architectures.

Zero Trust eliminates this trusted interior by treating every network location, inside or outside the traditional perimeter, as untrusted. Every access request to every resource must be fully evaluated against the requester's current identity, the health status of their device, behavioral analytics signals, and the sensitivity of the specific resource being accessed. This evaluation happens for every request, not just at the initial network connection point. The key architectural components, as defined by NIST SP 800-207, are:

The **Policy Engine (PE)** is the decision-making core of ZTA. It receives all attributes of an access request, identity claims, device posture, behavioral signals, environmental context, and evaluates them against ABAC/RBAC policies to produce a trust score and an access decision (permit or deny). The Policy Engine is the most sensitive component of ZTA, as compromising it would allow an attacker to manipulate access decisions.

The **Policy Administrator (PA)** acts on the Policy Engine's decisions by communicating with enforcement infrastructure, configuring firewall rules, issuing access tokens, or establishing encrypted tunnels to the requested resource. The Policy Administrator is the control plane of ZTA.

The **Policy Enforcement Point (PEP)** is the component that actually gates access to resources, enforcing the decisions made by the PE and communicated by the PA. PEPs can be implemented as API gateways, network access control devices, software-defined perimeter proxies (like Cloudflare Access or Zscaler Private Access), or integrated enforcement within applications themselves.

CISA's Zero Trust Maturity Model (ZTMM), published in 2023, defines five pillars for Zero Trust implementation: Identity, Devices, Networks, Applications and Workloads, and Data. The model defines three maturity levels (Traditional, Advanced, Optimal) for each pillar, providing a roadmap for organizations transitioning from perimeter-based security to Zero Trust. The Identity pillar maps directly to the access control models discussed in this lecture: at the Optimal level, all access is ABAC-based with continuous re-evaluation of every session, and no implicit trust is granted based on prior authentication. The Data pillar requires data-level access controls (MAC-style classification and labeling) that restrict access to data based on classification labels and subject attributes, not merely network location.

Executive Order 14028 (Improving the Nation's Cybersecurity), signed by President Biden in May 2021, mandates that all federal agencies develop and implement Zero Trust Architecture plans within 60 days. The Office of Management and Budget (OMB) Memorandum M-22-09 (Moving the US Government Toward Zero Trust Cybersecurity Principles), issued in January 2022, established specific ZTA targets for federal agencies by fiscal year 2024, including requiring MFA for all access, implementing device compliance checks, and transitioning to cloud-based access controls that enforce zero trust principles. This federal mandate has significantly accelerated commercial adoption of Zero Trust principles and products.

Zero Trust is visible in the shift from VPNs to Zero Trust Network Access. A traditional VPN gave a remote user broad access to the internal network; ZTNA replaces it with per-application access, so a user reaches only the specific applications they are authorized for, not the whole network. The move accelerated with the shift to remote work and cloud.
:::

%%%
---
unit: Misconceptions
code: FAQ
title: Common Misconceptions About Access Control
---
:::callout style=soft
Access control is frequently misunderstood in ways that lead to dangerous architectural decisions. Clarifying these misconceptions is essential for designing security programs that actually work.
:::

:::list style=plain
- **Misconception 1, "Strong authentication is sufficient."** Authentication proves identity but grants no access by itself. Without properly scoped authorization policies, a strong-password, MFA-protected account can still access everything in the system once authenticated. Both layers are required.
- **Misconception 2, "Encryption replaces access control."** Encryption protects data in transit and at rest from a third-party attacker, but it does not prevent an authorized-but-unauthorized user from accessing data they should not see. If the wrong people have access, they can decrypt it.
- **Misconception 3, "Network location determines trust."** The perimeter model assumption. Being inside the corporate network does not make a connection trusted, insider threats and lateral movement by external attackers demonstrate that internal network position is not a reliable trust signal.
- **Misconception 4, "Admin accounts are needed for daily work."** A frequent cause of privilege escalation success. Standard users running as local administrators dramatically expands the attack surface. Daily work should use standard accounts; elevated access should be JIT, scoped, and time-limited.
- **Misconception 5, "Once permissions are set, access control is done."** Access rights decay in alignment with organizational relevance. Employees change roles, systems change, regulatory requirements evolve. Access control is an ongoing operational discipline, not a one-time configuration task.
- **Misconception 6, "Deny-all firewall rules = MAC."** Network filtering is not mandatory access control. MAC is a formal information flow model based on clearance labels and classification labels, enforced by the operating system kernel, not a network appliance rule. Firewall rules implement network-level access restrictions, which are a complementary control, not MAC.
:::

:::image src="images/18_access_control_misconceptions.png" alt="Six-panel infographic titled 'Access Control Myths vs. Reality': each panel shows a common misconception on the left (in red with an X icon) paired with the correct understanding on the right (in green with a checkmark), panels cover authentication vs. authorization, encryption vs. access control, network location vs. zero trust, admin account abuse, access review necessity, and firewall rules vs. MAC" caption="Access control misconceptions, six frequent misunderstandings that lead to security architecture gaps when left uncorrected" width=full:::
:::

:::notes
Misconceptions about access control are pervasive in organizations of all sizes and maturity levels, and they lead directly to the architectural gaps that attackers exploit. Addressing these misconceptions in security awareness programs, architecture reviews, and executive briefings is as important as implementing the technical controls themselves.

The "strong authentication is sufficient" misconception is arguably the most dangerous because it creates a false sense of security at the highest visibility control point. Organizations that invest heavily in multi-factor authentication, rolling out hardware tokens, implementing phishing-resistant FIDO2 authentication, deploying passwordless authentication, sometimes treat this investment as their primary access control achievement. But authentication is only the first gate. An employee who has cleared strong authentication can still access far more resources than they need for their job function if authorization policies are not granular and properly maintained. An attacker who compromises that employee's MFA token or SIM-swaps their phone number can impersonate them through the strong authentication gate and then have free run of every resource the employee was authorized to access, which, in organizations that don't maintain least privilege, may be enormous. Strong authentication reduces the risk of credential theft, but granular authorization limits the damage when authentication is defeated.

The "encryption replaces access control" misconception often emerges from compliance conversations: a system containing sensitive data encrypts it at rest, and the compliance team marks the encryption control as satisfied. But encryption at rest protects against an attacker who physically steals a storage device or extracts raw files from a backup. It does nothing to protect against an authorized user who has the legitimate decryption key but should not be accessing that specific data. A cloud storage bucket that is encrypted but accessible to all IAM principals in the AWS account is not meaningfully protected, any compromised account in the organization can decrypt and exfiltrate the data using the IAM permissions to call the KMS decrypt operation. Access control governs who can request decryption; encryption protects against those who cannot. They are complementary layers, not substitutes.

The misconception that "network location determines trust", the castle-and-moat assumption, has been thoroughly disproven by decades of attacks that exploit lateral movement after perimeter breach. The 2013 Target breach, the 2020 SolarWinds attack, the 2021 Colonial Pipeline attack, and countless other high-profile incidents followed the same pattern: a perimeter was crossed (through credential theft, supply chain compromise, or social engineering), and the attacker then moved laterally within a trusted internal network with minimal additional obstacles. The Zero Trust principle that "internal = trusted" is a fundamentally broken assumption is now broadly accepted in the security community, but many operational network architectures still reflect the old model.

The "admin accounts are needed for daily work" misconception creates the single largest privilege escalation attack surface in Windows environments. When standard users are local administrators on their workstations, every phishing attack, drive-by download, or malicious email attachment that executes code runs with local administrator rights. This dramatically expands what the attacker can do: they can install persistence mechanisms, disable security software, extract credential hashes from memory using tools like Mimikatz, and modify the local system security configuration. Microsoft's guidance for many years has been to implement the "standard user" default on all workstations, users who need occasional elevated rights should use UAC prompts that require separate administrator credentials, not the same user account running with dual standard/admin privileges.

The misconception that "access control is done after initial setup" manifests operationally as the failure to conduct access reviews, the failure to deprovision departed employees, the failure to revoke temporary access grants, and the failure to adjust access rights when roles change. Organizations often invest significantly in access control at the time of a system deployment or compliance audit, then allow those controls to decay as the organization evolves around them. Quarterly access reviews, automated deprovisioning tied to HR systems, and role-change triggered access adjustments are the operational mechanisms that maintain access control alignment over time.

Common access-control misconceptions include running everyday accounts as local administrator, treating VPN access as equivalent to physical presence, and relying on encryption alone without controlling who can decrypt.
:::

%%%
---
unit: Tool Spotlight
code: SEL
title: Tool Spotlight, SELinux & AppArmor
---
:::callout style=soft
**SELinux** (Security-Enhanced Linux) and **AppArmor** are Linux kernel-level MAC frameworks that confine processes to only the resources their policy explicitly permits, providing mandatory access control enforcement independent of DAC permissions.
:::

::::columns ratio=1:1
::col::
::::card heading="SELinux"
:::list style=plain
- **Developed by:** NSA; integrated into Linux kernel 2.6 (2003).
- **Policy Model:** Type Enforcement (TE), every process and file has a security context (user:role:type:level).
- **Policy Enforcement:** Process types may only access file types explicitly permitted in the TE policy.
- **Modes:** Enforcing (deny + log violations), Permissive (log only, no deny), Disabled.
- **Default In:** RHEL, CentOS, Fedora, Amazon Linux.
:::
::::
::col::
::::card heading="AppArmor"
:::list style=plain
- **Developed by:** Novell; integrated into Linux kernel 2.6.36 (2010).
- **Policy Model:** Path-based profiles, policies reference file paths rather than type labels.
- **Policy Enforcement:** Per-application profiles define allowed files, capabilities, and network access.
- **Modes:** Enforce (active blocking), Complain (logging only, for profile development).
- **Default In:** Ubuntu, Debian, openSUSE.
:::
::::
::::

:::code language=bash caption="SELinux security context inspection, the 'Z' flag displays the SELinux context (user:role:type:level) for files and processes"
# View the SELinux security context of files
ls -lZ /var/www/html/
# -rw-r--r--. root root system_u:object_r:httpd_sys_content_t:s0 index.html
#                       |      |          |                     |
#                     SELinux SELinux  File Type             MLS Level
#                      User   Role   (httpd_sys_content_t)

# View the SELinux context of the running Apache process
ps -eZ | grep httpd
# system_u:system_r:httpd_t:s0    apache   1234  0:00  httpd
# Process type: httpd_t, allowed to access httpd_sys_content_t files
# Process type: httpd_t, NOT allowed to access user_home_t files

# Check current SELinux enforcement mode
getenforce
# Enforcing
:::

:::image src="images/18_selinux_confinement.png" alt="Split diagram showing Apache web server process compromise scenario: left side (without SELinux) shows attacker code executing in Apache's security context with red arrows accessing /etc/passwd, SSH keys, and other sensitive files; right side (with SELinux) shows the same compromise confined to httpd_t type, with red X marks on attempts to access files outside the httpd policy, and green checkmarks only on permitted file types like httpd_sys_content_t" caption="SELinux process confinement, a compromised Apache process operating as httpd_t can only access file types explicitly permitted in the SELinux policy, preventing access to SSH keys, /etc/passwd, and other sensitive resources" width=full:::
:::

:::notes
SELinux and AppArmor are two Linux Mandatory Access Control frameworks that implement kernel-level process confinement, providing a critical second layer of defense beyond standard DAC permissions. Their importance stems from a fundamental limitation of DAC: when a process is compromised through a software vulnerability (such as a buffer overflow in a web server or a remote code execution vulnerability in a PDF parser), the attacker's code executes with the full DAC permissions of the process that was exploited. If Apache is running as the www-data user and www-data has read access to sensitive files (or if the vulnerability allows privilege escalation to root), the attacker can access those files. DAC cannot distinguish between the legitimate Apache process reading a configuration file and an attacker who has injected code into the Apache process reading SSH private keys.

SELinux, originally developed by the NSA's Information Assurance Directorate and integrated into the Linux kernel in 2003, addresses this limitation through Type Enforcement (TE) policies. In SELinux, every process and every file is assigned a security context composed of a user, role, type, and sensitivity level (in MLS implementations). The kernel intercepts every file access, network connection, and inter-process communication and checks whether the accessing process's type is permitted to access the target object's type according to the TE policy. If the policy does not contain an explicit "allow httpd_t httpd_sys_content_t : file { read getattr }" rule, then an httpd_t process cannot read that file type, regardless of what DAC permissions say.

Consider a concrete example: an attacker exploits CVE-2021-41773 (Apache path traversal vulnerability) to gain remote code execution in the context of the Apache process, which runs as type httpd_t. On a system without SELinux, the attacker can use this code execution to read /etc/shadow (the password hash file), read SSH private keys in /root/.ssh/, modify web server configurations, or install backdoors. On a system with SELinux enforcing an httpd_t policy, none of these actions are permitted: the httpd_t type is defined to have access only to web content file types (httpd_sys_content_t, httpd_sys_script_t), not to system password files (shadow_t), SSH key files (ssh_home_t), or user home directories (user_home_t). The attacker has code execution in the Apache process but finds they are confined to exactly the file types the web server legitimately needs, making the exploitation largely useless for further lateral movement.

The practical challenge with SELinux is policy management. Default SELinux policies for common software packages (Apache, Nginx, MySQL, OpenSSH, Docker) are included in distributions like RHEL and are well-maintained by the distribution vendors. These default policies represent years of experience with what each application legitimately needs to access, and they provide meaningful confinement out of the box. The challenge arises with custom applications and non-standard configurations: administrators frequently disable SELinux ("setenforce 0" or setting SELINUX=disabled in /etc/selinux/config) when they encounter denials rather than investigating and correcting the policy violation. This "disable instead of fix" behavior is a significant operational security problem, a system with SELinux disabled has lost its MAC confinement layer entirely.

AppArmor takes a different, more approachable approach by using file path-based profiles instead of type labels. An AppArmor profile for Nginx might specify: "allow read /var/www/html/**, allow read /etc/nginx/**, deny read /etc/shadow, deny read /home/**." This path-based model is easier for administrators to write and understand than SELinux TE policies, at the cost of being easier to bypass (since path-based controls can be circumvented by symlinks or hardlinks in some configurations). AppArmor is the default MAC system in Ubuntu and Debian, including Ubuntu Server LTS which is widely deployed in cloud environments.

Docker and Kubernetes leverage both SELinux and AppArmor as container security controls. Docker's default AppArmor profile (docker-default) restricts container processes from accessing the host filesystem, kernel module loading, raw socket creation, and other potentially dangerous capabilities. Kubernetes SecurityContextConstraints and PodSecurityPolicies (replaced by Pod Security Standards in newer Kubernetes versions) allow administrators to mandate that container workloads run with SELinux labels or AppArmor profiles, implementing MAC at the container orchestration level. These controls are critical in multi-tenant Kubernetes clusters where container escapes are a significant threat.

Mandatory access control confines a process to a defined type regardless of file ownership. Under SELinux in enforcing mode, a web server exploited through a web application still cannot read a protected file such as the shadow password file, because policy forbids that process type from that file type, and the denial is logged with the exact process type, target and the rule that would be needed to permit it, making the model auditable.
:::

%%%
---
unit: Deep Dive
code: CLO
title: Access Control in Cloud Environments
---
:::callout style=soft
Cloud IAM implements fine-grained ABAC and RBAC through policy documents that control which identities can perform which actions on which resources under which conditions, replacing traditional network perimeter controls with identity-centric access enforcement.
:::

::::columns ratio=1:1
::col::
::::card heading="AWS IAM Core Concepts"
:::list style=plain
- **Principals:** IAM users, IAM roles, service accounts, federated identities.
- **Resources:** S3 buckets, EC2 instances, RDS databases, Lambda functions.
- **Actions:** API operations (s3:GetObject, ec2:StartInstances, rds:DescribeDBInstances).
- **Conditions:** Time-of-day, MFA required, source IP range, resource tags.
- **Effect:** Allow or Deny (explicit Deny always overrides Allow).
:::
::::
::col::
::::card heading="AWS IAM Policy Example"
:::code language=json caption="IAM policy granting S3 read access only for objects with specific tag, only via MFA, and only from the corporate VPC endpoint"
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::company-data/*",
  "Condition": {
    "StringEquals": {
      "s3:ExistingObjectTag/Classification": "Internal",
      "aws:sourceVpce": "vpce-0abc123"
    },
    "Bool": {"aws:MultiFactorAuthPresent": "true"}
  }
}
:::
::::
::::

:::image src="images/18_cloud_iam_abac.png" alt="AWS IAM ABAC diagram: an EC2 instance (subject) attempts s3:GetObject on an S3 bucket (resource), the IAM Policy Evaluation Engine checks the policy document conditions (MFA present, source VPC endpoint, object classification tag), all conditions must evaluate true for Allow to be applied, the Policy Enforcement Point (S3 service) returns the object or a 403 Forbidden" caption="Cloud IAM ABAC evaluation, AWS IAM policies implement ABAC by evaluating action, resource, and multi-dimensional condition attributes before producing an Allow or Deny decision" width=full:::
:::

:::notes
Cloud Identity and Access Management (IAM) systems represent the most widely deployed implementation of ABAC principles in the world. AWS IAM, Azure RBAC with conditions, and Google Cloud IAM are collectively managing access control for hundreds of millions of cloud resources across thousands of organizations, and they do so through policy documents that implement the same ABAC attribute evaluation model we discussed earlier in this lecture, subject attributes, resource attributes, action attributes, and environmental condition attributes are all evaluated simultaneously to produce every access decision.

Understanding cloud IAM is increasingly essential for security practitioners because cloud environments have fundamentally shifted the access control challenge. In traditional on-premises environments, network location (which physical network segment a server or workstation was connected to) served as a coarse-grained first layer of access control: resources on the database network were not reachable from the internet, resources on the HR network were not reachable from the engineering network. Cloud environments eliminate this physical segmentation, all cloud resources are logically adjacent from a network perspective, separated only by IAM policies. A misconfigured IAM policy in AWS can expose an S3 bucket containing sensitive data directly to the internet; a misconfigured Azure AD role assignment can grant a contractor global administrator rights to an entire Microsoft 365 tenant.

AWS IAM policies are JSON documents that specify Effect (Allow or Deny), Principal (who), Action (what API operation), Resource (which resource ARN), and Condition (under what circumstances). The Condition block is where ABAC becomes visible: conditions can check dozens of context variables including the presence of MFA authentication (aws:MultiFactorAuthPresent), the source VPC endpoint (aws:sourceVpce), the source IP address (aws:SourceIp), the time of access (aws:CurrentTime), the ARN of the requesting role (aws:PrincipalArn), and resource tags (s3:ExistingObjectTag/TagKey). A policy that requires all five of these conditions to be true simultaneously for an Allow decision is implementing five-dimensional ABAC, and the granularity far exceeds what was achievable in traditional RBAC implementations.

The "confused deputy" problem appears in cloud environments as the "cross-account access" challenge. AWS services (such as Lambda functions, EC2 instances, or ECS tasks) often need permissions to access other AWS resources. These permissions are granted through IAM roles attached to the service. If these roles are misconfigured with overly broad permissions, for example, an EC2 instance role that has "s3:*" (all S3 actions) on all S3 buckets, then a compromise of that EC2 instance gives the attacker full S3 access across the account. Least privilege in IAM requires that every service role be granted only the specific API actions on specific resource ARNs that the service legitimately needs. AWS Access Analyzer is a tool that helps enforce this by analyzing CloudTrail activity logs to determine what API calls a role has actually made, allowing administrators to generate least-privilege policies based on actual observed usage rather than guessing what permissions might be needed.

The shared responsibility model in cloud computing directly defines where access control responsibility falls. Cloud providers (AWS, Azure, GCP) are responsible for implementing access controls to protect the cloud infrastructure itself, the physical datacenters, the hypervisors, the cloud management control plane. Customers are responsible for implementing access controls within their own cloud accounts, IAM policies, S3 bucket policies, security groups, and network ACLs. Misunderstandings about this division create security gaps: organizations that assume the cloud provider is protecting their S3 bucket data against unauthorized access (when in fact the bucket policy may allow public access) are making a fundamental shared responsibility model error. The Capital One breach in 2019 (CVE-esque in its nature: a Server-Side Request Forgery attack on a misconfigured WAF allowed access to an EC2 instance metadata service that returned IAM role credentials) exposed over 100 million customer records stored in S3, a direct consequence of IAM misconfiguration that violated least privilege principles.

Cloud security posture management (CSPM) tools, including AWS Security Hub, Microsoft Defender for Cloud, Google Security Command Center, and third-party tools like Wiz, Orca Security, and Prisma Cloud, continuously analyze cloud IAM configurations for access control violations: publicly accessible storage buckets, overly permissive IAM policies, unused privileged accounts, cross-account access patterns that violate least privilege, and service roles with excessive permissions. These tools operationalize the access control principles from this lecture in cloud-native environments, providing continuous compliance monitoring against CIS Benchmarks, NIST CSF, and other frameworks.

Attribute-based access control decides access from attributes of the user, resource and context. A cloud policy can, for example, allow only engineers to read a specific storage bucket, only during business hours, and only from a specific network, and a policy simulator shows which combinations are permitted and which are denied, and why.
:::

%%%
---
unit: Deep Dive
code: DBX
title: Access Control in Databases
---
:::callout style=soft
Database access control governs which users or applications can read, insert, update, or delete specific tables, views, columns, or rows. Weak database authorization is a leading cause of data breach impact severity.
:::

:::list style=plain
- **Object-Level Privileges:** GRANT/REVOKE control access at the table or view level (SELECT, INSERT, UPDATE, DELETE, REFERENCES).
- **Column-Level Privileges:** Restrict access to specific columns, e.g., HR staff can SELECT name, department but NOT salary, SSN.
- **Row-Level Security (RLS):** Filters rows based on the querying user's identity, a sales rep can only SELECT rows where region = their assigned region.
- **Views as Access Control:** Non-privileged users are granted access to a VIEW that exposes only approved columns/rows, rather than the underlying table.
- **Stored Procedure Access:** Applications authenticate to the database using a service account that has EXECUTE permission on stored procedures only, no direct table access.
- **Database Roles:** Privilege groups analogous to RBAC roles, db_reader, db_writer, db_owner roles assigned to user accounts.
:::

:::code language=sql caption="PostgreSQL Row-Level Security example, sales representatives can only see their own region's customer records"
-- Enable Row-Level Security on the customers table
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

-- Create policy: users can only SELECT rows where their assigned region matches
CREATE POLICY region_isolation ON customers
    FOR SELECT
    USING (region = current_setting('app.current_user_region'));

-- Grant SELECT on the table (RLS policy further restricts which rows are returned)
GRANT SELECT ON customers TO sales_rep_role;

-- Users in sales_rep_role now see ONLY rows matching their region attribute
-- A Chicago rep cannot see New York customer records even with SELECT privilege
:::

:::image src="images/18_database_rls.png" alt="Database access control layers diagram: Layer 1 shows Network Access (only app servers reach the database port); Layer 2 shows Database Authentication (service account credentials); Layer 3 shows Object Privileges (GRANT SELECT on specific tables); Layer 4 shows Column Privileges (salary and SSN columns excluded from HR role); Layer 5 shows Row-Level Security (each sales rep sees only their region's rows), each layer is labeled with its SQL command or NIST control reference" width=full:::
:::

:::notes
Database access control is a critical and frequently under-implemented layer of the overall access control architecture. Many organizations invest in network-level access controls and application-layer authentication, but treat the database as an implicitly trusted resource, using a single shared application service account with broad database permissions for all application operations. This architecture means that a SQL injection vulnerability in the application, a compromised application server, or a rogue developer with access to the application's database connection string can access all data in all tables with all permissions granted to that service account.

The least privilege principle applies to database access just as it applies to operating system permissions and network access. Applications should authenticate to databases using service accounts that have only the minimum permissions required for the application's intended function. A web application that only displays customer records needs only SELECT privilege on the specific tables containing customer data, it does not need INSERT, UPDATE, DELETE, or any administrative privileges. A reporting application that only reads data for dashboards should use a read-only account. A data loading job that imports records needs INSERT on specific tables but not SELECT on tables containing sensitive business data irrelevant to its function. This service-account least privilege model ensures that even if an SQL injection attack succeeds, the attacker can only perform the database operations the service account is authorized for.

Column-level privileges extend least privilege below the table level to individual data fields. Most relational databases (including Oracle, SQL Server, and PostgreSQL) support GRANT ... ON specific_table (column1, column2) TO role, restricting access to a subset of table columns. This is particularly valuable for tables that mix operational data (which many roles need) with sensitive data (which few roles should access). An employee table might contain name, department, and manager_id (needed by many application functions) alongside salary, SSN, and bank account number (needed only by payroll processing systems). Column-level privileges allow the non-sensitive columns to be granted to a broad role while restricting the sensitive columns to a payroll_processor role.

Row-Level Security (RLS), supported in PostgreSQL, Oracle (Virtual Private Database), SQL Server, and MySQL 8.0+, takes column-level restrictions further by filtering which rows a querying user can see based on their identity or attributes. The SQL example in the slide demonstrates PostgreSQL's ENABLE ROW LEVEL SECURITY and CREATE POLICY syntax, which creates a filter applied automatically to every query against the table for users subject to the policy. A sales representative in the Chicago region who runs SELECT * FROM customers sees only the rows where region = 'Chicago', the database engine adds the filter automatically, invisibly, so the application does not need to implement the filtering logic explicitly. RLS is particularly valuable for multi-tenant SaaS applications where a single database table contains data belonging to multiple customers: an RLS policy based on the authenticated user's tenant_id attribute ensures each tenant can only access their own data.

Database views are a simpler but less dynamic mechanism for access control: a view is a stored SELECT query that presents a filtered or transformed version of one or more tables. Granting a role access to a view (rather than the underlying table) restricts what data they can access to exactly what the view definition returns, specific columns, filtered rows, or derived calculations. Views provide an abstraction layer that insulates application logic from raw table structure while enforcing consistent access control logic that cannot be bypassed by constructing clever WHERE clauses.

The Oracle Database Vault product extends these principles to the database administration layer, implementing MAC-style controls that prevent even the DBA from reading sensitive application data. This addresses the DBA trust problem: traditional database security models grant DBAs god-like access to all data, creating an insider threat risk. Database Vault creates "realms" around sensitive data (such as payment card data, HR compensation data, or healthcare records) that DBAs cannot access without a separate authorization that requires additional approval, implementing SoD for database administrators and providing the database equivalent of PAM privileged access controls.

HIPAA's Security Rule (45 CFR §164.312(a)(1)) requires covered entities to implement technical security measures to guard against unauthorized access to ePHI transmitted over or stored in electronic information systems, a requirement directly satisfied by database access controls including user authentication, column-level privileges, and audit logging of all access to PHI records. The HITECH Act strengthens these requirements and significantly increases penalties for PHI exposure due to inadequate access controls, making database security a legal compliance requirement with multi-million-dollar fine exposure for healthcare organizations that fail to implement it properly.

SQL injection (OWASP A03:2021) most directly exploits weak database access control, running arbitrary SQL under the application's service account. A read-only, single-purpose service account sharply limits the damage: an injection in a product-catalog query cannot reach the users, payment or credentials tables, which makes database least privilege one of the highest-value mitigations for injection risk.
:::

%%%
---
unit: Case Study
code: COL
title: Case Study, Colonial Pipeline Ransomware Attack
---
:::callout style=soft
The May 2021 Colonial Pipeline ransomware attack shut down the largest fuel pipeline in the United States for six days, causing fuel shortages across the Southeast, triggered by a single compromised VPN account with no MFA.
:::

:::steps
1. **Credential Discovery:** Attackers (DarkSide ransomware group) obtained the password for a legacy VPN account, likely through a dark web credential dump from a prior breach at another organization.
2. **VPN Authentication:** The stolen password worked because the VPN account had no multi-factor authentication and had not been disabled despite being for an account that was not in active use.
3. **Network Access:** The compromised VPN account provided access to Colonial Pipeline's IT network. No network micro-segmentation limited the account's lateral movement capability.
4. **Ransomware Deployment:** DarkSide deployed ransomware across Colonial Pipeline's IT systems. Out of caution about potential OT network impact, Colonial proactively shut down the operational technology (OT) pipeline control systems.
5. **Impact:** The 5,500-mile pipeline, carrying 45% of the US East Coast's fuel, was shut down for six days. Gas shortages, panic buying, and regional fuel price spikes followed. Colonial paid a $4.4 million ransom in Bitcoin.
6. **Access Control Failures:** No MFA on VPN; orphaned/unused account not deprovisioned; no network segmentation limiting VPN account lateral movement; no privileged access monitoring.
:::

:::list style=plain
- **NIST Controls Violated:** AC-2 (Account Management, orphaned account), IA-2 (MFA, no MFA on VPN), AC-17 (Remote Access, inadequate VPN access controls), SC-7 (Boundary Protection, insufficient network segmentation).
:::

:::image src="images/18_colonial_pipeline_attack.png" alt="Attack chain diagram for Colonial Pipeline: Step 1 shows dark web credential marketplace with Colonial VPN credentials; Step 2 shows attacker authenticating to VPN without MFA (green checkmark on single-factor auth, red warning); Step 3 shows attacker inside IT network with broad lateral movement; Step 4 shows DarkSide ransomware deployment across file servers, domain controllers, and workstations; Step 5 shows Colonial proactively shutting down OT/pipeline systems; Step 6 shows six-day shutdown timeline and fuel shortage map" caption="Colonial Pipeline attack chain, a single dormant VPN account without MFA provided the initial access that led to a six-day shutdown of critical fuel infrastructure" width=full:::
:::

:::notes
The Colonial Pipeline ransomware attack of May 7, 2021 is one of the most consequential cyber attacks on US critical infrastructure in history, and it is a masterclass in how multiple access control failures compound into catastrophic real-world consequences. The attack was not technically sophisticated, it did not require zero-day exploits, advanced persistent threat tooling, or complex attack infrastructure. It required a single valid credential for a VPN account with no multi-factor authentication and no deprovisioning of dormant accounts.

The Cybersecurity and Infrastructure Security Agency (CISA) and Federal Bureau of Investigation (FBI) released a joint advisory following the attack identifying the key access control failures. The compromised VPN account was not an active, in-use account at the time of the attack, it was a dormant account that should have been deprovisioned. Colonial Pipeline's account management processes (NIST SP 800-53 AC-2) had not identified and disabled this orphaned account before attackers used it. This is the "leaver" failure from the IAM lifecycle: accounts that are no longer needed for active users must be disabled promptly, not left dormant where they can be exploited by anyone who obtains the credentials.

The absence of multi-factor authentication on the VPN account (NIST SP 800-53 IA-2, Identification and Authentication) was the second critical failure. With MFA, a stolen password is insufficient to authenticate to the VPN, the attacker also needs the second factor (a hardware token, authenticator app OTP, or push notification). If Colonial had enforced MFA for all VPN access, the compromised credential would have been unusable by the attacker regardless of how it was obtained. FBI Director Christopher Wray testified before Congress that the Colonial attack "serves as a clarion call about the real threat posed by ransomware" and specifically cited the absence of MFA as a fundamental gap.

The network architecture allowed the compromised VPN account to reach internal systems beyond what was operationally necessary for its legitimate purpose (NIST SP 800-53 AC-17, Remote Access, and SC-7, Boundary Protection). In a properly segmented network architecture implementing least privilege at the network layer, the VPN session would have been restricted to only the network segments and systems the account was authorized to reach for its legitimate function. Instead, the account's network access enabled broad lateral movement within Colonial's IT environment.

The decision to shut down the OT pipeline control systems, which were not directly compromised, highlights an important architectural point: when IT and OT networks are insufficiently segmented, an IT network compromise creates immediate credible threat to OT operations, forcing operational shutdowns even when OT systems themselves are not yet affected. This is the network segmentation access control failure in its most consequential real-world form. Had Colonial's IT and OT networks been properly air-gapped or segregated with strict access controls at the IT/OT boundary, the ransomware spreading through IT systems would not have created plausible threat to pipeline operations, potentially allowing Colonial to continue operations while remediating the IT network.

Colonial Pipeline reportedly paid $4.4 million in Bitcoin to the DarkSide ransomware group to receive a decryption key, though the US Department of Justice subsequently recovered approximately $2.3 million of that ransom by identifying and seizing the Bitcoin wallet. The total incident cost to Colonial, including ransom payment, incident response, remediation, regulatory attention, and business disruption, far exceeds the cost of implementing MFA on VPN access, conducting regular account reviews to identify orphaned accounts, and implementing network micro-segmentation, all standard access control practices that would have prevented or dramatically limited the attack.

The attack prompted multiple federal government actions. President Biden signed Executive Order 14028 (Improving the Nation's Cybersecurity) two weeks after the Colonial attack, which includes specific directives for MFA adoption and Zero Trust Architecture implementation. The Transportation Security Administration (TSA), which has regulatory jurisdiction over pipeline security, issued emergency security directives requiring pipeline companies to implement MFA on all remote access systems, directly addressing the specific access control failure that enabled the Colonial attack. CISA's "Known Exploited Vulnerabilities" catalog and Binding Operational Directives were expanded, and CISA released a specific advisory (AA21-131A) on DarkSide ransomware that includes detailed access control recommendations that map directly to the NIST SP 800-53 controls we studied in this lecture.

The Colonial Pipeline attack contrasts defense in depth with defense by perimeter. A single VPN was the only meaningful access control boundary: there was no MFA to strengthen it, no cleanup of orphaned accounts, no segmentation to limit a compromised session's reach and no privileged-access monitoring. Any one additional layer would have changed the outcome, which is the operational lesson of defense in depth.
:::

%%%
---
unit: Comparison
code: PHY
title: Physical vs. Logical Access Control
---
:::callout style=soft
Physical access control and logical access control implement the same fundamental principles, authentication, authorization, and accounting, using different mechanisms to protect physical spaces versus digital resources.
:::

:::table
| Principle | Physical Access Control | Logical Access Control |
|---|---|---|
| **Authentication** | Keycard, PIN, biometric reader, security guard | Password, MFA, smart card, biometric login |
| **Authorization** | Facility policy defining which badge grants which door access | IAM policy defining which account grants which resource access |
| **Implicit Deny** | Locked door, entry requires valid credential match | Default deny ACL/policy, access requires explicit Allow rule |
| **Least Privilege** | Warehouse staff cannot access executive floor | HR staff cannot read financial system data |
| **Audit Logging** | Badge reader logs: who entered which door, when | SIEM logs: who accessed which resource, when |
| **Separation of Duties** | Two-person rule for vault access | Dual approval for production deployments |
| **Privileged Access** | Security administrator controls badge permissions | IAM administrator controls access policies |
| **Access Review** | Quarterly review of which badges can access which zones | Quarterly access certification of user account rights |
:::

:::image src="images/18_physical_logical_comparison.png" alt="Parallel diagram showing physical access control (left) and logical access control (right) implementing the same security principles: Physical shows a keycard reader, badge management system, door log, and security office; Logical shows a login screen, IAM policy engine, SIEM audit log, and security operations center, connecting arrows between each pair are labeled with the shared principle (Authentication, Authorization, Audit) showing structural equivalence" caption="Physical and logical access control implement identical security principles through different technical mechanisms, both enforce authentication, authorization, least privilege, and audit accounting" width=full:::
:::

:::notes
Understanding the structural equivalence between physical access control and logical (digital) access control is valuable for security practitioners because it highlights that access control is a universal architectural principle, not a technology-specific implementation. The same design patterns, authentication, authorization based on policy, implicit deny, least privilege, audit logging, separation of duties, regular access reviews, appear identically in both domains, using different technologies to achieve the same security objectives.

Physical access control systems manage access to physical spaces: office buildings, server rooms, data centers, manufacturing floors, medical records storage areas, and other locations where physical presence enables harmful actions. A badge access system functions as an authentication and authorization system: the badge is a credential (something you have), which may be supplemented by a PIN (something you know) or biometric (something you are) for sensitive areas. The access control panel that evaluates whether a specific badge should be permitted to open a specific door is functionally equivalent to an IAM policy engine evaluating whether a specific user should be permitted to read a specific file. The badge management database that defines which badge IDs are authorized to access which door groups is functionally equivalent to an RBAC role assignment database. The physical access logs showing badge presentation events are functionally equivalent to SIEM audit logs showing authentication and resource access events.

The convergence of physical and logical access control, often called Physical and Logical Access Convergence (PLAC), is an important security architecture trend. Traditional organizations manage physical access (badges) and logical access (IT accounts) in entirely separate systems with separate lifecycles. An employee who is terminated might have their IT account disabled within hours but retain a functional badge for days or weeks because the physical security team was not notified. Or an employee might be badge-revoked due to HR misconduct but retain IT access because the systems are not integrated. PLAC addresses this by integrating the physical access management system with the HR system and IT identity management system, when an employee is terminated in HR, both the badge and the IT account are disabled simultaneously through a single workflow, eliminating the gap between physical and logical deprovisioning.

The two-person rule in physical security, requiring two authorized individuals to be present for access to high-security areas such as nuclear weapons storage, secure communications vaults, or drug storage, is the physical equivalent of dual control and separation of duties in logical access control. Just as no single system administrator should be able to unilaterally make production changes without a second approver, no single person should be able to access a nuclear material storage area without a second cleared person present. The principle prevents insider threats and provides a detection mechanism: if someone tries to access a high-security area alone, the physical control (requiring two badges or two biometrics) prevents it, just as the software control (requiring dual approval in the change management system) prevents unilateral production changes.

Server room and data center physical security is the boundary layer where physical and logical access control intersect most critically. An attacker with physical access to a server can bypass logical access controls through methods that are impossible remotely: booting from external media to reset administrator passwords, connecting a hardware keylogger to capture credentials, installing a malicious network device for remote access, or simply stealing physical storage media. NIST SP 800-53 PE (Physical and Environmental Protection) controls, including PE-2 (Physical Access Authorizations), PE-3 (Physical Access Control), and PE-6 (Monitoring Physical Access), recognize this by treating physical access control as a primary control for protecting information systems. The principle is that logical access controls on a system are meaningless if an attacker can walk up to the physical hardware, physical security is the ultimate backstop for logical access control.

Cloud computing has created an interesting inversion of the traditional physical-logical relationship. For cloud-hosted systems, the customer has no physical access to the hardware, all access is logical, through APIs and management consoles. The cloud provider manages all physical access controls (CCTV, biometric entry controls, mantraps, two-person rules for data center access). Customers receive SOC 2 Type II reports and third-party audit reports (such as ISO 27001 certification) that attest to the effectiveness of the provider's physical controls, rather than directly managing or auditing them. This represents a major shift in the shared responsibility model: for on-premises systems, the organization manages both physical and logical access control; for cloud systems, physical control is fully delegated to the provider, and the customer's access control responsibility focuses entirely on the logical layer, IAM policies, network ACLs, and encryption key management.

Tailgating, following an authorized person through a secure door without presenting a credential, is the physical equivalent of session hijacking: the attacker rides a legitimate authentication without holding credentials. Mantraps, challenging guards and anti-tailgating turnstiles are the physical analogues of session controls that detect and end sessions from unexpected addresses, devices or locations.
:::

%%%
---
unit: Mid-Lecture Checkpoint
code: CHK
title: Checkpoint, Access Control Models Quiz
---
:::callout style=soft
Test your understanding of the four access control models before we proceed to advanced topics.
:::

:::list style=plain
- **Question 1:** An intelligence analyst with "Top Secret" clearance attempts to read a "Secret" document. Under the Bell-LaPadula Simple Security Property, is this permitted? *(Answer: Yes, the analyst's clearance is equal to or higher than the document's classification. "No read up" prevents reading higher-classification documents; reading equal or lower classification is permitted.)*
- **Question 2:** A "Secret"-cleared analyst wants to copy classified notes into an "Unclassified" document to share with a colleague. Under Bell-LaPadula's Star Property, is this permitted? *(Answer: No, the Star Property ("no write down") prevents writing to a lower classification level. This would leak Secret information into Unclassified data.)*
- **Question 3:** A company assigns file-share permissions to "HR_Generalist" group rather than to individual users. Which access control model does this implement? *(Answer: RBAC, permissions are assigned to a role (group) and users inherit access through role membership.)*
- **Question 4:** An AWS IAM policy allows S3 access only if the requester has MFA enabled, the request comes from the corporate VPC, and the S3 object is tagged "Internal." Which access control model does this implement? *(Answer: ABAC, the decision evaluates subject attributes (MFA status), environmental attributes (source VPC), and resource attributes (object tag) simultaneously.)*
- **Question 5:** A file owner grants a colleague Read permission on their personal document. Which access control model does this demonstrate? *(Answer: DAC, the resource owner exercises discretionary control to grant permissions to other users.)*
:::

:::image src="images/18_checkpoint_models.png" alt="Five-question quiz card layout: each question is displayed in a blue card with the question text and a 'Think before reading...' prompt, with answer text revealed below in green, questions cover Bell-LaPadula read-up, Bell-LaPadula write-down, RBAC group assignment, ABAC multi-attribute policy, and DAC owner permission grant" caption="Mid-lecture checkpoint, five scenario questions to verify comprehension of the four access control models and formal security model rules before proceeding to advanced topics" width=full:::
:::

:::notes
These questions check comprehension of the four access control models before the advanced implementation topics that follow.

Question 1 (Bell-LaPadula Simple Security Property) tests the "no read up" rule. The key insight is that the rule prevents reading higher-classification documents, not lower-classification or same-classification ones. A Top Secret-cleared analyst can read Top Secret, Secret, Confidential, and Unclassified documents, their clearance level establishes a ceiling, not a floor. The restriction flows upward only: they cannot read documents classified above their clearance level. This is the "no read up" formulation: subjects cannot read objects at a higher classification level than their clearance. Reading at or below clearance level is permitted by the Simple Security Property.

Question 2 (Bell-LaPadula Star Property) tests the "no write down" rule. The scenario describes exactly the information leakage that the Star Property is designed to prevent: a cleared user copying Secret information into an Unclassified document would allow that Secret information to flow downward to users with only Unclassified access, a confidentiality violation. The Star Property (also called the *-property or confinement property) prevents subjects from writing to objects at a lower classification level than their clearance. Writing up is permitted (a Secret-cleared user can add to Top Secret documents, contributing information upward), but writing down is prohibited. The mathematical elegance of BLP is that the two rules together guarantee that information can only flow upward in the classification hierarchy, from lower to higher classification, ensuring that no classified information can ever reach a lower-classification container accessible to less-cleared users.

Question 3 (RBAC) is a straightforward identification question. The defining characteristic of RBAC is that permissions are assigned to roles (implemented as groups in most directory services), not to individual users. Users receive access by being assigned to roles. The "HR_Generalist" group represents the role abstraction, all users in that group share the same permissions, and permissions are managed at the role level rather than the individual level.

Question 4 (ABAC) should be recognizable by the multi-dimensional condition evaluation. The policy evaluates three independent attributes simultaneously, MFA status (subject attribute), source VPC (environmental attribute), and object tag (resource/object attribute), and requires all three to be true. This is the hallmark of ABAC: access decisions based on policies that evaluate attribute sets from multiple categories in combination. Any system that uses conditions based on time, location, device state, resource properties, or user attributes beyond simple role membership is implementing ABAC principles.

Question 5 (DAC) returns to the fundamental characteristic of DAC: owner discretion. The defining feature is that the resource owner (a regular user, not an administrator) is making the access grant decision. In DAC, the owner has full discretion over who else can access their resources and what permissions those users receive. This contrasts with RBAC (where administrators define roles and their permissions), MAC (where system administrators define clearance and classification labels), and ABAC (where administrators define the policy rules evaluated by the policy engine).

A common confusion in the Bell-LaPadula model is the direction of the Star Property: a subject may write up to higher classification but never down to lower, which is the opposite of the read rule (read down, never up). The write-down restriction prevents leaking classified information into a lower-classification document.
:::

%%%
---
unit: Framework
code: GDR
title: Access Control & Regulatory Compliance
---
:::callout style=soft
Access control requirements are mandated by every major data protection regulation and industry security standard. Compliance obligations provide a minimum floor for access control design, security best practice often requires exceeding these minimums.
:::

:::table
| Regulation / Standard | Access Control Requirements | Key Access Control Controls |
|---|---|---|
| **GDPR (EU)** | Art. 25 (Privacy by Design), Art. 32 (Security of processing) | Least privilege, access logging, need-to-know for personal data |
| **HIPAA Security Rule** | 45 CFR §164.312(a), Access Control standard | Unique user IDs, automatic logoff, encryption/decryption, emergency access |
| **PCI DSS v4.0** | Req. 7 (Restrict access), Req. 8 (User identification) | RBAC for cardholder data, MFA for all administrative access, account reviews |
| **SOX (Sarbanes-Oxley)** | Section 302/404, Internal controls over financial reporting | SoD for financial transactions, privileged access logging, access reviews |
| **ISO/IEC 27001:2022** | Annex A.8 (Access control) | Access policy, user provisioning, privileged access management, access reviews |
| **NIST CSF 2.0** | PR.AA (Identity Management, Authentication, Access Control) | Identity governance, least privilege, access enforcement, continuous monitoring |
| **FedRAMP** | Baseline: NIST SP 800-53 AC family (all controls) | Full AC-1 through AC-25 implementation with third-party assessment |
:::

:::image src="images/18_compliance_mapping.png" alt="Compliance mapping diagram with a central 'Access Control Core Practices' hub showing six key practices (Least Privilege, MFA, Access Reviews, SoD, Audit Logging, Deprovisioning) connected by spokes to surrounding regulatory circles (GDPR, HIPAA, PCI DSS, SOX, ISO 27001, NIST CSF, FedRAMP), each regulatory circle is labeled with its specific access control requirement that maps to the core practices" caption="Access control compliance mapping, the same core access control practices satisfy requirements across GDPR, HIPAA, PCI DSS, SOX, ISO 27001, and NIST frameworks simultaneously" width=full:::
:::

:::notes
One of the most strategically valuable insights for security practitioners is that a strong access control foundation simultaneously satisfies access control requirements across most major compliance frameworks. Organizations that invest in implementing access control correctly, least privilege, proper account lifecycle management with timely deprovisioning, MFA on all access, regular access reviews, separation of duties for high-risk transactions, and comprehensive audit logging, find that the same implementations satisfy GDPR, HIPAA, PCI DSS, SOX, and ISO 27001 access control requirements simultaneously. Compliance is a byproduct of good security, not a separate track.

GDPR Article 25 (Data Protection by Design and by Default) requires controllers to "implement appropriate technical and organisational measures" to ensure that "by default, only personal data which is necessary for each specific purpose of the processing are processed." This is a legal mandate for need-to-know and data minimization at the access control layer: each system function should only access the personal data fields necessary for that function, each user role should only access the personal data records necessary for their responsibilities, and each processing operation should have access controls scoped to its specific purpose. Violations of Article 32 (which requires "appropriate technical measures" including "ensuring ongoing confidentiality, integrity, availability and resilience of processing systems") that involve inadequate access controls have resulted in multi-million euro fines: in 2019, British Airways was fined £183 million (later reduced to £20 million) following a breach in which inadequate access controls were cited as a contributing factor.

HIPAA's Security Rule (45 CFR Part 164, Subpart C) defines an "Access Control" standard (§164.312(a)(1)) that requires covered entities and their business associates to implement technical policies and procedures to allow only authorized persons or software programs to access electronic Protected Health Information (ePHI). The required implementation specifications under this standard include unique user identification (no shared accounts, each user must have a unique ID for audit trail attribution), emergency access procedure (a mechanism to access ePHI in emergencies when normal access paths are unavailable), automatic logoff (idle session termination to prevent unauthorized access to unattended workstations), and encryption/decryption procedures. These HIPAA requirements map directly to NIST SP 800-53 AC-2 (Account Management, unique IDs), AC-11 (Device Lock, automatic logoff), and IA-5 (Authenticator Management, credential policies).

PCI DSS Version 4.0, effective April 2024, significantly strengthened access control requirements. Requirement 7 (Restrict Access to System Components and Cardholder Data by Business Need to Know) requires organizations to grant access based on documented business need (need-to-know) and to establish and maintain access control systems with at least one technical control to prevent unauthorized access. Requirement 8 (Identify Users and Authenticate Access to System Components) now requires MFA for all access into the cardholder data environment (CDE), including for all administrator access and all remote access. The explicit MFA requirement in PCI DSS 4.0 directly addresses the Colonial Pipeline-style attack vector, requiring a second factor that makes stolen credentials insufficient for access to payment systems.

The Sarbanes-Oxley Act (SOX), while primarily a financial reporting law, has strong access control implications through its internal controls requirements. Section 404 requires management and external auditors to assess the effectiveness of internal controls over financial reporting (ICFR). Access controls, specifically, who has access to financial systems and the separation of duties in financial transaction processing, are a core component of ICFR. SOX compliance typically requires formal documentation of access rights to all financially significant systems, evidence of periodic access reviews (access recertification campaigns), evidence of SoD controls preventing the same individual from both creating and approving financial transactions, and audit trails of all changes to financial data. The PCAOB (Public Company Accounting Oversight Board) standards that govern SOX audits specifically reference access controls as a critical element of IT general controls (ITGC) that external auditors must test.

ISO/IEC 27001:2022's Annex A.8 (Technological Controls) consolidates access control requirements that were previously spread across Annex A.9 in the 2013 version. A.8.2 (Privileged access rights) requires that privileged access rights be restricted, controlled, and reviewed, mapping to NIST AC-6 and PAM principles. A.8.5 (Secure authentication) requires strong authentication including MFA for administrative accounts. A.8.18 (Use of privileged utility programs) addresses the PAM concern about tools that can bypass normal system controls.

Compliance requirements set a floor, not a ceiling. HIPAA requires unique IDs and automatic logoff but treats MFA only as addressable; PCI DSS requires MFA for cardholder-data access but does not mandate ABAC or Zero Trust. Treating compliance as the objective produces access control that meets the minimum bar but not current best practice, so the practitioner must understand both the floor and the security-optimal target.
:::

%%%
---
unit: Tool Spotlight
code: CYA
title: Tool Spotlight, CyberArk & PAM Products
---
:::callout style=soft
**CyberArk Privileged Access Security** is the market-leading Privileged Access Management (PAM) platform, providing credential vaulting, session recording, just-in-time access, and privileged session analytics for enterprise environments.
:::

::::columns ratio=1:1
::col::
::::card heading="CyberArk Core Architecture"
:::list style=plain
- **Digital Vault:** AES-256 encrypted, FIPS 140-2 certified credential store with tamper-evident audit logging.
- **Central Policy Manager:** Defines access workflows, approval processes, and session recording policies.
- **Privileged Session Manager (PSM):** Proxy that establishes sessions to target systems, operators never see the credential.
- **Password Vault Web Access (PVWA):** Web UI for requesting access, submitting approvals, and reviewing session recordings.
- **Privileged Threat Analytics (PTA):** Behavioral analytics that alert on anomalous privileged session activity.
:::
::::
::col::
::::card heading="Competing PAM Products"
:::list style=plain
- **BeyondTrust Privileged Remote Access:** Strong in vendor/remote access scenarios; excellent session recording.
- **Delinea Secret Server:** Originally Thycotic; good for mid-market; strong DevOps integrations.
- **HashiCorp Vault:** Open-source/enterprise; cloud-native; strong for dynamic secrets and DevOps pipelines.
- **Microsoft PIM (Azure AD):** Included in Azure AD P2; JIT access for Azure and M365 administrative roles.
- **AWS IAM Identity Center:** Centralized SSO and permission set management for multi-account AWS environments.
:::
::::
::::

:::image src="images/18_cyberark_architecture.png" alt="CyberArk architecture diagram: administrator requests access through PVWA portal, request routes to Central Policy Manager for approval workflow evaluation, approved request triggers PSM to retrieve credentials from Digital Vault, PSM establishes proxied RDP/SSH session to target server, session is recorded to Session Recording Storage, PTA analyzes session activity for anomalies, all components connected to a central Audit Database for compliance reporting" caption="CyberArk PAM architecture, every privileged session is proxied, recorded, and analyzed, with credentials stored in a certified encrypted vault and never exposed to operators" width=full:::
:::

:::notes
CyberArk Privileged Access Security (PAS) has been the consistent leader in the Gartner Magic Quadrant for Privileged Access Management since the category was established, and understanding its architecture and capabilities provides a practical reference point for understanding what enterprise-grade PAM looks like in production. CyberArk protects privileged accounts at over half of the Fortune 500, and its core architecture implements the PAM principles we discussed in the PAM slide with specific technical implementations designed for large enterprise scale and high-security environments.

The CyberArk Digital Vault is the security core of the platform. It is a hardened server appliance (or virtual appliance) that stores privileged credentials in an AES-256 encrypted database. The vault is FIPS 140-2 validated, meeting the US federal government cryptographic module standard for high-security applications. All access to the vault is logged in a tamper-evident audit trail, even vault administrators cannot access credentials without generating an audit record. Vault hardening includes network isolation (only specific CyberArk components can communicate with the vault), OS hardening, and hardware security module (HSM) integration for key management.

The Privileged Session Manager (PSM) is the component that eliminates credential exposure to human operators. When an administrator requests access to a target system (a Linux server via SSH, a Windows server via RDP, a database via JDBC), the PSM receives approval from the Central Policy Manager, retrieves the credential from the Digital Vault, establishes a connection to the target system using those credentials, and then presents the administrator with a proxied session. The administrator types commands and sees screen output through the PSM proxy, they are never in direct contact with the target system and never see or know the actual password. When the session ends, the PSM terminates the connection and triggers automatic password rotation in the vault, making the previously used credential invalid even if the administrator somehow recorded it.

Session recording stores a full record of every privileged session, keystrokes, commands, screen content captured as a video-like recording, in a searchable, tamper-evident archive. This capability is invaluable for forensic investigation: if a privileged account is suspected of misuse, security teams can review the full session recording to see exactly what commands were run, what data was accessed, and what changes were made. Session recordings also support insider threat programs: behavioral analytics (CyberArk's Privileged Threat Analytics component) can analyze session patterns to detect anomalies that suggest account compromise or malicious insider activity, such as unusual commands, access to systems outside the user's normal scope, or sessions occurring outside normal working hours.

HashiCorp Vault represents the leading cloud-native and DevOps-oriented PAM solution. Where CyberArk excels in protecting human administrator access to traditional IT infrastructure, HashiCorp Vault is optimized for the challenge of secrets management in automated, cloud-native environments. Modern applications running in Kubernetes containers, CI/CD pipelines, and serverless functions need credentials, database connection strings, API keys, cloud provider credentials, but these applications are ephemeral and automated, making traditional credential vaulting approaches impractical. HashiCorp Vault's "dynamic secrets" capability allows applications to request short-lived, application-specific credentials at runtime. For example, an application container can request a PostgreSQL credential from Vault; Vault creates a new database account with the minimum required privileges, provides the credentials to the application, and automatically revokes that account when the credential's TTL expires (typically minutes or hours). This eliminates long-lived database credentials from application configuration entirely.

Microsoft Privileged Identity Management (PIM), included in Azure Active Directory Premium P2, provides JIT access for Microsoft's ecosystem, specifically for Azure resource management roles and Microsoft 365 administrative roles. A Global Administrator in M365 who uses PIM does not hold Global Admin rights continuously; instead, they request activation (specifying a business justification and duration), receive temporary Global Admin rights for the approved duration (typically 1-8 hours), and the elevation expires automatically. All activation events are logged in Azure AD audit logs for compliance review. PIM also supports approval workflows, requiring a second Global Admin to approve requests for particularly sensitive role activations, implementing dual control for the most powerful administrative roles. PIM represents a pragmatic PAM capability for organizations already invested in the Microsoft ecosystem that may not require a full third-party PAM solution.

Consumer password managers help individuals manage personal credentials, while enterprise privileged access management controls, audits and enforces policy around shared privileged credentials, adding session proxying, behavioral analytics and approval workflows. The 2022 LastPass breach, in which encrypted customer vaults were stolen after a developer endpoint was compromised, shows that a credential vault is itself a high-value target requiring extraordinary protection.
:::

%%%
---
unit: Summary
code: SUM
title: Class 18 Review & Policy Enforcement
---
:::pullquote
"Authentication gets you through the door. Least privilege, RBAC, DAC, MAC, and ABAC decide which rooms you are allowed to enter, what you can touch, and how long you are permitted to stay."
:::

:::list style=chips
- Authentication (Identity) vs. Authorization (Rights)
- Principle of Least Privilege (NIST SP 800-53 AC-6)
- Role-Based Access Control (RBAC) Abstraction
- Discretionary Access Control (DAC) & Access Control Lists
- Mandatory Access Control (MAC) Security Labels
- Attribute-Based Access Control (ABAC) Policies
:::

:::image src="images/18_zero_trust_access.png" alt="Zero Trust access control architecture diagram: user on the left attempting to access a resource on the right, the request passes through Identity Verification (AuthN), then Device Health Check, then Risk-Based Policy Evaluation (ABAC/RBAC), then Least Privilege Scoping, all before reaching the resource, with 'never trust, always verify' label and each evaluation gate showing its decision criteria" caption="Zero Trust access control, every access request is fully evaluated against identity, device, policy, and environmental context, regardless of network location" width=full:::
:::

:::notes
To wrap up Class 18, remember that access control is the mechanism that translates security policy into operational system enforcement. Authentication verifies identity, but it is authorization that determines what that verified identity is permitted to do within the system, and the design of that authorization architecture fundamentally determines an organization's resistance to insider threats, credential compromise, and lateral movement.

The four access control models we studied today represent a spectrum from user-controlled to administrator-controlled, from flexible to rigid, and from simple to sophisticated. Organizations rarely implement a single model in isolation. Instead, they compose these models into layered architectures appropriate to their environment and risk profile. A healthcare organization might use RBAC as the baseline, ABAC to enforce context-sensitive access based on patient-physician appointment relationships, and MAC-style classification labels to separate data sensitivity tiers. A financial institution might use MAC-inspired integrity controls for financial transaction systems, RBAC for application-layer access, and DAC for collaboration documents.

The Zero Trust security model, articulated in NIST SP 800-207, represents the maturation of access control thinking. Zero Trust eliminates the concept of a trusted network perimeter, no request is trusted by virtue of its network origin. Instead, every access request, regardless of whether it originates inside or outside the network, must be fully evaluated against the requester's authenticated identity, device health status, behavioral risk signals, and the sensitivity of the requested resource. This evaluation is performed by an access control engine that combines RBAC roles, ABAC attribute policies, and continuous authentication signals. The Principle of Least Privilege is enforced dynamically, with access grants being time-limited and scoped to the minimum required to complete the specific task.

The practical implementations of the Principle of Least Privilege that are most impactful in real-world security include: eliminating local administrator rights from standard user accounts (dramatically reducing malware persistence capabilities), implementing just-in-time (JIT) privileged access that grants elevated rights only for the duration of a specific approved task, enforcing application-level least privilege to prevent applications from requesting unnecessary OS permissions, and conducting quarterly access reviews to revoke accumulated privilege creep.

In our next session, Class 19, we will explore detection systems. We will learn how to monitor systems to identify when an authorized account begins behaving anomalously, suggesting the credential may have been compromised by an attacker who is now operating within the access boundaries that our authorization policies define.

NIST SP 800-207 (Zero Trust Architecture) defines the logical components of a ZTA, the Policy Engine (PE), Policy Administrator (PA), and Policy Enforcement Point (PEP), which collectively implement the access control vision described in this lecture at the network and application layer. In practice, enterprise ZTA deployments combine Okta or Azure AD (identity and AuthN), CrowdStrike Falcon (device health attestation), Palo Alto Prisma Access (PEP/network enforcement), and a Policy Decision Point that integrates all inputs, producing exactly the multi-factor access control evaluation we described. The practical impact of mature access control on breach outcomes is supported by the Verizon DBIR: in 2023, credentials (either stolen or default) were the primary attack vector in 49% of breaches, access control architectures that enforce least privilege, implement MFA, and conduct regular access reviews directly address this dominant threat category, making access control arguably the highest-ROI security investment available to most organizations.
:::
