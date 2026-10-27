---
deck:
  title: Authentication & Password Security
  kicker: Class 6
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 6
  description: How password attacks work, what makes a password strong, and why MFA shuts most of them down.
  topics: [Password Attacks, Brute Force, Dictionary Attacks, Password Policies, MFA, Authentication Factors]
---

---
title: Authentication & Password Security
cover: true
---
:::text class=sub
Stopping the attack that worked even without a single click
:::
:::list style=chips
- Authentication Factors
- Multi-Factor Authentication
- Password Storage & Hashing
- Credential Management Frameworks
:::

:::image src="images/06_authentication_cover_concept.png" alt="Diagram showing a lock gate with three paths labeled 'something you know,' 'something you have,' and 'something you are' converging at a single access point" caption="Authentication as a multi-layered gate: identity must be proven before access is granted" width=full
:::

:::notes
Authentication is the process of verifying the identity of a user, system, or entity attempting to access a resource. It forms the first line of defense in most cybersecurity architectures and is foundational to the CIA triad, specifically, ensuring that only authorized entities maintain access to information systems. The most common form of authentication relies on knowledge-based factors, such as passwords. However, passwords are inherently vulnerable to a variety of attacks, including credential stuffing (e.g., CVE-2020-17456), phishing, and brute-force attempts.

Authentication mechanisms are typically categorized into three primary factors: something you know (e.g., passwords), something you have (e.g., hardware tokens, smartphones), and something you are (e.g., biometrics). The use of multiple factors, referred to as Multi-Factor Authentication (MFA), is strongly recommended by standards such as NIST SP 800-63B, which outlines digital identity guidelines and emphasizes the importance of phishing-resistant authenticators.

In addition to authentication methods, secure password storage is critical. Systems must never store passwords in plaintext. Instead, they should use cryptographic one-way functions such as bcrypt, scrypt, or Argon2, which are designed to be computationally intensive to resist offline attacks. The National Institute of Standards and Technology (NIST) provides specific guidance on password storage and management within its Cybersecurity Framework and SP 800-118 guidelines.

This lecture explores the theoretical underpinnings and practical implementations of authentication systems, with a focus on password-based vulnerabilities, secure storage mechanisms, and the integration of multi-factor authentication to reduce the risk of unauthorized access.

To appreciate why authentication security matters so deeply, consider the scale of credential-based attacks today. According to the Verizon Data Breach Investigations Report, over 80% of hacking-related breaches involve brute force or the use of stolen or weak passwords. Every organization that has suffered a significant breach in recent memory, from LinkedIn (2012, 117 million accounts), to Adobe (2013, 153 million accounts), to the Yahoo breach (2013–2014, 3 billion accounts), had authentication as either the primary attack surface or the critical failure point that allowed attackers to escalate privileges once inside. Understanding authentication from first principles is therefore not merely academic: it is an operational imperative for every security professional.

The lecture is structured to move from theoretical foundations (what authentication is and what it is meant to accomplish) through the attacker's playbook (how passwords are attacked in practice), through defensive frameworks (modern password policy and MFA), so that by the end students understand not just what to do but why each control exists.
:::

%%%

---
unit: Foundations
code: AUT
title: Authentication, Proving Who You Are
---
:::callout style=soft
**Authentication** is the process of proving that a user is who they claim to be, before granting access to a system.
:::

:::pullquote
Last class's attacker didn't break in, they just logged in, with a stolen password.
:::

::::columns
::col::
:::list heading="Core Authentication Factors" style=plain
- **Something You Know** (e.g., passwords, PINs)
- **Something You Have** (e.g., hardware tokens, smartphones)
- **Something You Are** (e.g., fingerprints, facial recognition)
:::

::col::
:::table
| Factor Type       | Example Mechanism        | NIST SP 800-63 Reference |
|-------------------|--------------------------|--------------------------|
| Single-Factor     | Password-only login      | NIST SP 800-63B          |
| Two-Factor (2FA)  | Password + SMS code      | NIST SP 800-63B          |
| Multi-Factor (MFA)| Password + Token + Biometric | NIST SP 800-63B      |
:::
::::
::::

:::image src="images/06_authentication_factors_triangle.png" alt="Triangle diagram with three vertices labeled Know, Have, and Are; arrows connect them with a shield icon in the center labeled MFA" caption="The three authentication factors: knowledge, possession, and inherence combine to form MFA" width=half
:::

:::flow
User provides identity claim (username)
System challenges for authentication factor(s)
Factor verified against stored credential or live challenge
Access granted if all required factors pass
Session established with appropriate privileges
Audit log records authentication event
:::

:::notes
Authentication is a foundational pillar of information security, defined by NIST in Special Publication 800-63B as the process of establishing confidence in the identity of users or information systems. It answers the question: "Who are you?" This assurance is typically achieved through one or more authentication factors, what the user knows, has, or is.

In practice, many breaches, such as those exploiting credentials stolen via phishing (e.g., CVE-2021-40539 in Zoho ManageEngine, or widespread credential harvesting via malicious OAuth apps), do not involve bypassing authentication but rather obtaining valid credentials through social engineering or exploitation of weak authentication practices. This is why the strength and proper implementation of authentication mechanisms are critical.

NIST outlines three primary authentication factor types:
1. **Something You Know** – Knowledge-based, such as passwords or PINs.
2. **Something You Have** – Possession-based, such as a hardware token or smartphone.
3. **Something You Are** – Inherence-based, such as biometrics.

Single-factor authentication (e.g., password-only) is increasingly insufficient. NIST SP 800-63B emphasizes the importance of multi-factor authentication (MFA) to resist attacks like credential stuffing, password spraying, and session hijacking. The use of out-of-band channels (e.g., SMS or app-based codes) and phishing-resistant authenticators (e.g., FIDO2/WebAuthn) are strongly recommended for high-security environments.

Authentication is distinct from authorization, which determines what an authenticated user is allowed to do. However, weak authentication undermines even the most robust authorization policies. As such, secure authentication design is essential to any defense-in-depth strategy.

It is worth examining the history of authentication to understand the evolutionary pressures that produced today's complex landscape. For decades, password-only authentication was considered adequate because attack tools were slow and credential databases were small and difficult to obtain. The explosion of large-scale data breaches between 2008 and 2016 fundamentally changed this calculus: attackers now maintain databases containing billions of username-password pairs harvested from prior breaches, making automated credential-stuffing attacks trivially cheap to launch.

This backdrop explains why NIST SP 800-63B (2017, updated 2020) made such sweeping changes to long-standing password guidance, and why MFA is no longer considered an optional enhancement but a baseline expectation for any system handling sensitive data. Authentication must now be designed not just against the attacker who tries to guess a password, but against the attacker who already has a high-confidence list of likely passwords obtained from other breaches.

The flow above illustrates the generic authentication sequence that underpins virtually every login interaction, from a simple website to a corporate VPN gateway. Each step is an opportunity for both attack and defense: the identity claim can be spoofed, the challenge can be intercepted, the verification can be bypassed, and the session can be hijacked. Understanding each step deeply is what separates a professional who can design secure systems from one who merely configures them.
:::

%%%

---
unit: Foundations
code: AUT
title: Authentication Factors
---
::::columns
::col::
:::table
| Factor | Description | Examples |
|---|---|---|
| **Something You Know** | A secret only the user should possess | Password, PIN, passphrase, security question |
| **Something You Have** | A physical or digital possession | Hardware token, smartphone app, smart card, cryptographic key |
| **Something You Are** | Unique biological or behavioral traits | Fingerprint, iris scan, voice recognition, facial geometry |
| **Somewhere You Are** | Contextual location or network-based identity | IP address, GPS location, trusted network zone |
:::
::col::
:::callout style=soft
Combining authentication factors from **different categories**, not just repeating the same type, is what provides true multi-factor authentication (MFA) strength.
:::
:::text
The security gain of stacking two passwords or two biometrics is minimal. Real resilience comes from requiring evidence across distinct knowledge, possession, inherence, or location dimensions.
:::
::::

:::image src="images/06_authentication_factor_categories.png" alt="Four-quadrant diagram showing the four factor types with icons: brain for Know, key for Have, fingerprint for Are, map pin for Where; each quadrant lists example mechanisms and typical attack vectors" caption="Four authentication factor categories and their example mechanisms, orthogonality between categories is what makes MFA meaningful" width=full
:::

:::notes
Authentication factors represent distinct categories of evidence used to verify a user's identity. The traditional model, defined by standards such as NIST SP 800-63B, classifies these into three core factors: something you know, something you have, and something you are. Modern frameworks sometimes extend this to include "somewhere you are" as a contextual factor, particularly in adaptive and risk-based authentication systems.

Each factor type has unique security properties. "Something you know" (e.g., passwords) is vulnerable to phishing, brute-force attacks, and social engineering. "Something you have" (e.g., hardware tokens or smartphones with TOTP apps) introduces possession as a barrier to attackers, assuming the device isn't compromised. "Something you are" refers to biometrics, which are difficult to replicate but not infallible, as demonstrated by vulnerabilities like CVE-2022-22848 in certain fingerprint sensors. Lastly, "somewhere you are" adds contextual awareness, such as geolocation or network identity, to detect anomalous login attempts.

Multi-factor authentication (MFA) is most effective when these factors are **independent** and **mutually orthogonal**. For example, using a password (knowledge) and a one-time code from an app (possession) is significantly stronger than using a password and a security question, both of which rely on knowledge and can be socially engineered or guessed. NIST explicitly discourages the use of multiple knowledge-based factors as a sole means of achieving MFA.

This layered approach aligns with defense-in-depth principles and is foundational to identity and access management frameworks across industries.

A deeper analysis of each factor category reveals important subtleties often overlooked in practice. Knowledge factors, while ubiquitous, suffer from a fundamental paradox: the easier a secret is to remember, the easier it is to predict. Research consistently shows that when left to their own devices, humans create passwords drawn from a small vocabulary of patterns, names, birthdays, common words with predictable substitutions, that dramatically reduce the theoretical entropy. The "75-character random password" is perfectly secure but practically unusable without a password manager; the "dog's name + birth year" is memorable but trivially guessable.

Possession factors solve the memorability problem but introduce a new threat model: device theft, SIM swapping, and account recovery attacks. When an attacker cannot attack the credential directly, they often attack the recovery mechanism, which may itself be knowledge-based (security questions) or possession-based (SMS to a phone number that can be ported). This is why NIST SP 800-63B specifically calls out SMS-based OTP as a restricted authenticator, not forbidden for all uses, but explicitly disallowed for high-assurance levels.

Inherence factors (biometrics) introduce perhaps the most complex trade-offs. Biometrics are stable (your fingerprint does not change), convenient (no memorization required), and theoretically strong. However, unlike passwords, they cannot be "reset" if compromised. Sophisticated presentation attacks, using high-resolution photographs, silicone fingerprint replicas, or synthetic voice recordings, have successfully defeated consumer biometric systems. ISO/IEC 30107 defines a framework for Presentation Attack Detection (PAD) that attempts to distinguish genuine biometric inputs from synthetic fakes, but PAD implementation quality varies widely across commercial products.

Location factors represent the newest dimension and are typically used in conjunction with other factors rather than as a primary authenticator. Adaptive authentication systems from vendors like Okta, Microsoft, and Ping Identity use location signals to dynamically adjust the authentication challenge: a user logging in from a known device at their usual office IP address may receive a lighter challenge, while the same user logging in from an unrecognized country at 3 AM will be prompted for additional verification.
:::

%%%

---
unit: Foundations
code: AUT
title: Authentication vs. Authorization vs. Accounting
---
:::callout style=soft
The **AAA framework**, Authentication, Authorization, and Accounting, is the backbone of access control in virtually every enterprise security architecture. The three concepts are closely related but serve distinct purposes.
:::

:::table
| Concept | Question It Answers | Example | Standard Reference |
|---|---|---|---|
| **Authentication** | Who are you? | Username + password + MFA | NIST SP 800-63B |
| **Authorization** | What are you allowed to do? | Role-based access control (RBAC) | NIST SP 800-207 (Zero Trust) |
| **Accounting** | What did you do, and when? | SIEM audit logs, RADIUS accounting | ISO/IEC 27001 A.12.4 |
:::

::::columns
::col::
:::list heading="Why All Three Are Required" style=plain
- Authentication without authorization lets any verified user access everything
- Authorization without authentication cannot verify who is making the request
- Accounting without the other two produces logs with no meaningful identity context
- All three together form the foundation of Zero Trust Architecture
:::
::col::
:::callout style=line
**RADIUS** (Remote Authentication Dial-In User Service) and **TACACS+** are the two dominant AAA protocols in network infrastructure. RADIUS combines authentication and authorization; TACACS+ separates them, a distinction that matters for granular access control in complex environments.
:::
::::

:::image src="images/06_aaa_framework.png" alt="Three-step pipeline diagram: first gate labeled Authentication with a key icon, second gate labeled Authorization with a shield icon, third stage labeled Accounting with a clipboard icon; arrows show user moving through each gate before reaching the protected resource" caption="The AAA framework: all three stages must be present for complete access control, skipping any one creates a security gap" width=full
:::

:::notes
The AAA framework, Authentication, Authorization, and Accounting, is a cornerstone of network and information security architecture, referenced extensively in NIST SP 800-53 (Security and Privacy Controls for Information Systems) and implemented in virtually every enterprise network through protocols such as RADIUS and TACACS+.

Authentication, as covered throughout this lecture, answers the question "Who are you?" It verifies the claimed identity of a user or system before any access decisions are made. Authentication without proper controls is the leading cause of breaches, but even perfect authentication provides no protection if the subsequent access decisions are poorly designed.

Authorization answers the question "What are you allowed to do?" Once identity is verified, the system must determine what resources and actions that identity is permitted to access. Authorization is typically implemented through access control models: Role-Based Access Control (RBAC), where permissions are assigned to roles and users are assigned to roles; Attribute-Based Access Control (ABAC), where access decisions consider multiple attributes (user department, resource sensitivity, time of day); and Mandatory Access Control (MAC), used in high-security environments like defense systems where labels (Top Secret, Secret, Unclassified) govern access. The principle of least privilege, granting only the minimum access necessary, is fundamental to all authorization models and is codified in NIST SP 800-53 control AC-6.

Accounting (also called auditing) answers the question "What did you do, and when?" Accounting produces the audit trail that enables forensic investigation after an incident, compliance reporting for regulatory frameworks (HIPAA, PCI-DSS, SOC 2), and anomaly detection when integrated with SIEM systems. Without accounting, an organization may know that a breach occurred but be unable to determine what data was accessed, what commands were executed, or how long the attacker was present. ISO/IEC 27001 Annex A.12.4 specifically addresses logging and monitoring requirements.

The practical interplay between these three concepts is important. Consider a scenario where an employee's credentials are compromised. Authentication fails to block the attacker because the attacker has valid credentials. Authorization limits the damage by ensuring the employee only had access to their own department's files, not the entire database. Accounting provides the forensic record that allows the security team to determine exactly what the attacker accessed, when, and from what IP address. All three layers working together transform a catastrophic breach into a contained, documentable, recoverable incident.

Zero Trust Architecture (NIST SP 800-207) extends the AAA model by removing implicit trust: authenticated and authorized users are continuously re-verified and monitored rather than trusted indefinitely once inside the perimeter. U.S. federal agencies are required to adopt Zero Trust under Executive Order 14028 (2021).

The RADIUS vs. TACACS+ distinction is worth a brief mention for students pursuing network security or CompTIA Security+ certifications. RADIUS encrypts only the password in the authentication exchange, while TACACS+ encrypts the entire payload, making TACACS+ preferred for device administration in environments where the management channel itself may be at risk. Cisco devices default to TACACS+ for administrative authentication precisely for this reason.
:::

%%%

---
unit: Foundations
code: AUT
title: Password Entropy, Measuring Strength Mathematically
---
:::callout style=soft
**Password entropy** quantifies the unpredictability of a password in bits. Higher entropy means more possible combinations, making the password harder to guess or crack. It is calculated as: **H = L × log₂(N)** where L is password length and N is the size of the character set.
:::

::::columns
::col::
:::table
| Character Set | Size (N) | Bits per Character |
|---|---|---|
| Lowercase only (a–z) | 26 | 4.7 bits |
| Alphanumeric (a–z, A–Z, 0–9) | 62 | 5.95 bits |
| Full ASCII printable | 95 | 6.57 bits |
| Diceware word list (7,776 words) | 7,776 | 12.9 bits per word |
:::
::col::
:::table
| Password Example | Entropy (approx.) | Practical Strength |
|---|---|---|
| `password` | ~18 bits | Extremely weak |
| `P@ssw0rd1!` | ~34 bits | Weak (in dictionaries) |
| `xK#9mL!qPv2` (12 chars, full ASCII) | ~79 bits | Strong |
| `correct-horse-battery-staple` (4 random words) | ~44 bits | Moderate–Strong |
| 5-word Diceware passphrase | ~65 bits | Very Strong |
:::
::::

:::image src="images/06_password_entropy_chart.png" alt="Bar chart comparing entropy in bits for different password types: dictionary word, complex 8-char, complex 12-char, 4-word passphrase, 5-word Diceware passphrase; color-coded red to green showing weak to strong; crack time annotations at 100B attempts per second" caption="Password entropy comparison: length and randomness, not complexity rules, determine real-world strength" width=full
:::

:::notes
Password entropy is the mathematical foundation underlying all password strength assessments. Derived from information theory, entropy in this context measures the logarithm (base 2) of the number of equally likely possibilities in a password's search space. The formula H = L × log₂(N), where H is entropy in bits, L is the length of the password, and N is the size of the character set, provides a clean, comparable metric for evaluating different password strategies.

Understanding this formula reveals several counterintuitive truths about password security. First, length matters more than character-set diversity. Adding one character to a password increases entropy by log₂(N) bits, approximately 4.7 bits for lowercase letters, up to 6.57 bits for the full printable ASCII set. By contrast, the difference between using 62-character alphanumeric versus 95-character full ASCII is only about 0.62 bits per character, a much smaller gain than simply making the password one character longer. This is the mathematical basis for NIST SP 800-63B's emphasis on minimum length requirements over mandatory character complexity rules.

Second, entropy only reflects the theoretical maximum assuming the password is chosen uniformly at random from the character set. Human-chosen passwords consistently fall far short of this theoretical maximum because they are not random. A study by researchers at Carnegie Mellon found that requiring complexity rules (uppercase + number + symbol) only increased average guessing resistance by about 1–2 bits compared to an equivalent-length password without those rules, far less than adding two more random characters. This is because humans apply the complexity rules predictably: capitalize the first letter, append a number, replace 'a' with '@'. Attackers model these patterns explicitly in their rule sets.

The Diceware passphrase method, developed by Arnold Reinhold and referenced in NIST SP 800-63B as an acceptable approach to memorizable passwords, deserves special attention. It works by rolling physical dice to select words from a standardized 7,776-word list (7,776 = 6^5, so five dice rolls select one word). Each word provides log₂(7,776) ≈ 12.9 bits of entropy. A 5-word passphrase therefore yields approximately 65 bits, enough to resist even GPU-accelerated offline attacks for the foreseeable future, and produces something like "correct horse battery staple" (the famous xkcd #936 example), which is both highly memorable and genuinely strong.

xkcd 936, "Password Strength", sets out the entropy argument: four random common words give more entropy, about 44 bits, than a short password with substitutions, about 28 bits, while being far easier to remember.

The practical implication for security policy is clear: policies should mandate minimum entropy thresholds (NIST recommends systems accept passwords up to 64+ characters), encourage passphrases, and screen against breach databases (which eliminates weak passwords regardless of their theoretical entropy) rather than enforcing arbitrary complexity rules that produce predictably bad human behavior. The entropy of "P@ssw0rd1!" is perhaps 34 bits in theory but effectively 0 bits in practice, it appears verbatim in every major credential dump.
:::

%%%

---
unit: Password Attacks
code: PWA
title: Password Attacks, An Overview
---
::::columns
::col::
:::list heading="Common Attack Types" style=plain
- **Brute Force**, Exhaustively tries all possible character combinations
- **Dictionary Attack**, Uses precompiled lists of common passwords and dictionary words
- **Credential Stuffing**, Leverages previously breached credentials across other services
- **Password Spraying**, Tests a small set of common passwords across many accounts
:::
::col::
:::callout style=soft
These attack vectors exploit predictable human behavior and weak authentication policies. Each method varies in resource intensity, stealth, and effectiveness depending on target configurations and user habits.
:::
::::

:::image src="images/06_password_attack_taxonomy.png" alt="2x2 matrix diagram with axes labeled 'Accounts targeted (one vs. many)' and 'Passwords tried (few vs. many)'; brute force, dictionary, credential stuffing, and password spraying placed in appropriate quadrants" caption="Password attack taxonomy: attack type is determined by how many accounts and how many passwords are tested simultaneously" width=full
:::

:::steps heading="How a Credential Stuffing Campaign Works"
1. **Acquire breach data**, Purchase or download credential dumps (username:password pairs) from dark web markets or paste sites
2. **Deduplicate and normalize**, Scrub duplicates, format credentials to match the target's login schema
3. **Configure automation**, Deploy tools like Sentry MBA, OpenBullet, or Hydra with proxy rotation to evade IP-based blocks
4. **Execute and collect**, Run credential testing at scale; valid logins are logged as "hits"
5. **Exploit valid sessions**, Access accounts to steal data, pivot to linked services, or sell valid credentials
:::

:::notes
Password attacks represent a foundational category of threats in authentication security, exploiting weaknesses in user-selected passwords and system design. These attacks are broadly classified into four primary methodologies, each differing in approach, computational demand, and likelihood of success.

A **brute force attack** is the most resource-intensive but theoretically guaranteed method, systematically iterating through every possible combination of characters until the correct password is discovered. While effective against short or unsalted hashes, its feasibility decreases exponentially with password length and complexity. Modern systems often implement account lockout policies or rate-limiting mechanisms (e.g., exponential backoff) to mitigate this threat, as outlined in NIST Special Publication 800-63B.

In contrast, a **dictionary attack** leverages precomputed or curated lists of commonly used passwords, dictionary words, and previously breached credentials (such as those found in the RockYou dataset). This approach is far more efficient than brute force because it targets human predictability. Tools like John the Ripper or Hashcat often use these dictionaries to expedite cracking processes.

**Credential stuffing** exploits the widespread tendency of users to reuse passwords across multiple services. Attackers obtain credentials from one breach (e.g., through a data leak or via CVE-2021-32619 in certain web apps) and automate login attempts on unrelated platforms. This technique was notably used in the 2019 Capital One breach (CVE-2019-9978), where reused credentials played a contributing role.

Finally, **password spraying** reverses the traditional brute-force model by using a few commonly used passwords (e.g., "Password123!", "Admin2024") against a large number of accounts. This reduces the risk of triggering account lockouts while increasing the chance of finding at least one valid login. It is especially effective in environments without strict authentication monitoring, such as those lacking SIEM correlation rules or anomaly detection.

Each of these attack types underscores the importance of enforcing strong password policies, implementing multi-factor authentication (MFA), and monitoring authentication logs for anomalous behavior in compliance with frameworks like ISO/IEC 27001 and NIST SP 800-53.

Understanding the attacker's perspective on these techniques is essential for defenders. Attackers do not choose randomly between these methods, they select based on what information they already have and what constraints they face. If an attacker has obtained a password hash database via SQL injection, they will use offline brute force or dictionary attacks with GPU-accelerated tools like Hashcat, which can test billions of hashes per second. If they are attacking a live login portal with no breach data, they will use spraying to stay under lockout thresholds. If they have obtained credentials from a previous breach, credential stuffing is the logical next step, since it requires minimal effort for potentially high returns.

The RockYou dataset, 14.3 million plaintext passwords leaked from the RockYou social gaming platform in 2009, remains one of the most commonly used wordlists in penetration testing to this day. It represents not a collection of sophisticated secrets but a statistical sample of real human password behavior, and that sample has proven remarkably predictive: the same patterns (number appends, common substitutions, short words) appear again and again in every subsequent breach. This durability of poor password behavior across 15 years is precisely why policy-level interventions are so important: individual education alone is insufficient when the behavior is systemic.
:::

%%%

---
unit: Password Attacks
code: PWA
title: Brute Force Attacks
---
:::callout style=soft
A **brute force attack** is a cryptographic and password-cracking technique in which an attacker systematically attempts every possible combination of characters until the correct password or key is discovered. It is a deterministic but computationally intensive method that relies on exhaustive search rather than exploiting weaknesses in algorithms or implementations.
:::

::::columns
::col::
:::table
| Password Length | Character Set (95 ASCII) | Approximate Combinations |
|----------------|--------------------------|---------------------------|
| 6 characters   | Alphanumeric + symbols   | ~735 billion              |
| 8 characters   | Same                     | ~6.6 quadrillion          |
| 12 characters  | Same                     | ~5.4 × 10²⁰               |
:::
::col::
:::callout style=line
#### Key Insight:
Each additional character in a password exponentially increases the search space. This combinatorial explosion is the core reason why longer passwords are exponentially more secure against brute force attacks.
:::
::::

:::pullquote
Brute force complexity grows exponentially with password length, not linearly.
:::

:::image src="images/06_brute_force_search_space.png" alt="Logarithmic bar chart showing password search space in number of combinations on the Y axis against password length 6 through 16 on the X axis; bars grow exponentially; annotations show equivalent GPU crack times at 100 billion attempts per second" caption="Password search space grows exponentially with length, a 12-character password takes billions of times longer to crack than an 8-character one" width=full
:::

:::notes
A brute force attack represents the most resource-intensive yet conceptually straightforward method of password cracking. It operates on the principle of exhaustive key space exploration, iterating through all possible character combinations until the correct one is found. This method does not rely on exploiting protocol weaknesses, social engineering, or dictionary-based shortcuts, it is purely computational.

The feasibility of a brute force attack is governed by the size of the search space, which is determined by two primary factors: password length and character set size. For a password of length $ n $ and a character set of size $ c $, the total number of possible combinations is $ c^n $. As shown in the table, increasing password length from 6 to 12 characters increases the search space from the order of billions to quintillions, a difference of more than 100 million times.

This exponential growth is why modern password policies, such as those recommended by NIST in Special Publication 800-63B, emphasize password length over complexity rules. While character diversity is important, length provides the most significant barrier against brute force attacks due to the mathematical properties of exponentiation.

In practice, attackers often combine brute force with other techniques, such as dictionary attacks or rule-based transformations, to reduce the effective search space. However, against systems that enforce sufficiently long, random passwords and implement proper rate-limiting or account lockout mechanisms (as outlined in ISO/IEC 27001 controls), brute force becomes computationally infeasible within a reasonable timeframe.

Notable examples of brute force attack mitigations include the use of salted password hashes (to prevent precomputed attacks like rainbow tables), key derivation functions such as PBKDF2 or Argon2 (which add computational cost), and multi-factor authentication (MFA) as recommended by frameworks like MITRE ATT&CK (T1110.001 - Brute Force: Password Guessing).

To ground this in concrete numbers: a modern GPU cluster used for password cracking (for example, a rig with eight NVIDIA RTX 4090s running Hashcat) can test approximately 300 billion MD5 password hashes per second. Against a 6-character password using only lowercase letters (26^6 ≈ 308 million combinations), this cracks every possible password in under 0.001 seconds. Against an 8-character mixed-case alphanumeric password (62^8 ≈ 218 trillion combinations), the same rig takes about 12 minutes on average. Against a 12-character random password with the full 95-character printable ASCII set (95^12 ≈ 5.4 × 10²⁰), the expected crack time exceeds the age of the universe.

This analysis underscores two critical policy conclusions. First, the historical minimum of 8 characters is now dangerously inadequate for any password stored with a weak or fast hash function (MD5, SHA-1, unsalted SHA-256). Second, the right defense against brute force is a combination of password length, a strong memory-hard key derivation function (Argon2id being the current gold standard per OWASP), and rate-limiting at the authentication layer. No single control is sufficient; all three must be present.

The concept of "password entropy" formalizes this: entropy in bits equals log₂(search space). A 12-character random alphanumeric password yields approximately 71 bits of entropy, which is sufficient even against near-future hardware improvements. NIST SP 800-63B suggests targeting at least 112 bits of security for high-value accounts when using approved cryptographic mechanisms.
:::

%%%

---
unit: Password Attacks
code: PWA
title: Rainbow Tables & Precomputed Hash Attacks
---
:::callout style=soft
A **rainbow table** is a precomputed lookup table mapping password hashes back to their plaintext originals. Rather than cracking a hash in real time, an attacker simply looks up the hash in the table, reducing cracking time from hours to milliseconds, at the cost of significant storage.
:::

::::columns
::col::
:::flow
Password "hunter2" is hashed → MD5: bc50d48e76e3f7d2a5de0609e3e45d7f
Attacker queries rainbow table with that MD5 hash
Table returns "hunter2" in milliseconds
Account is compromised without any computation
:::
::col::
:::callout style=line
**Why Salting Defeats Rainbow Tables**

A cryptographic salt is a random value appended to the password before hashing. Because every password gets a unique salt, precomputed tables are useless, the attacker must crack each hash individually from scratch. NIST SP 800-132 mandates salting for all password storage.
:::
::::

:::table
| Hash Function | Speed (GPU) | Rainbow Table Feasible? | Recommended for Passwords? |
|---|---|---|---|
| MD5 | ~300 billion/sec | Yes (without salt) | No |
| SHA-1 | ~150 billion/sec | Yes (without salt) | No |
| SHA-256 | ~12 billion/sec | Yes (without salt) | No |
| bcrypt (cost 12) | ~20,000/sec | No (salt built-in) | Yes |
| Argon2id | ~1,000/sec | No (salt + memory-hard) | Yes (preferred) |
:::

:::image src="images/06_rainbow_table_vs_salt.png" alt="Split diagram: left side shows a rainbow table attack where a hash lookup instantly returns a plaintext password; right side shows the same attack failing because each hash includes a unique salt prefix, making precomputed tables useless" caption="Rainbow tables versus salted hashes: the simple addition of a per-password salt renders entire precomputed databases worthless" width=full
:::

:::notes
Rainbow tables represent one of the most elegant time-space trade-off attacks in cryptography. The concept was formalized by Philippe Oechslin in his 2003 paper "Making a Faster Cryptanalytic Time-Memory Trade-Off," building on prior work by Martin Hellman. The core insight is that computing a hash is cheap and fast, but storing every possible hash-to-plaintext mapping would require astronomical storage. Rainbow tables use chains of alternating hash and reduction functions to compress this mapping into a manageable table that can cover billions of passwords in gigabytes rather than exabytes of storage.

In practical terms, rainbow tables made it possible for an attacker with a modest amount of disk space to crack any unsalted MD5 or SHA-1 password hash instantly, regardless of password complexity. Websites like CrackStation maintain rainbow tables covering billions of common passwords and can crack most unsalted MD5 hashes in seconds through a web interface. This is why the MD5 or SHA-1 storage of passwords, regardless of how complex those passwords are, is categorically unacceptable for any modern system.

The defense against rainbow tables is the cryptographic salt: a random value, typically 16–32 bytes, generated uniquely for each password at the time it is created and stored alongside the hash. Because the salt is unique per password, an attacker who obtains the database cannot use precomputed tables, they would need to generate a separate table for every possible salt value, which is computationally infeasible. NIST SP 800-132 (Recommendation for Password-Based Key Derivation) mandates the use of salts for all password hashing, specifying a minimum salt length of 32 bits (though 128 bits is now standard practice).

Salting alone, however, is not sufficient if a fast hash function like MD5 or SHA-256 is used. Even with salts, a modern GPU cluster can test billions of candidate passwords per second against a salted MD5 hash by simply computing hash(salt + candidate) for each guess. This is why password-specific key derivation functions (KDFs) that are intentionally slow and memory-intensive are required.

bcrypt (designed by Niels Provos and David Mazières, 1999) was one of the first widely adopted slow password hashing algorithms. It incorporates a configurable cost factor that allows the computational cost to be increased as hardware improves, a system configured for bcrypt cost 12 performs approximately 2^12 = 4,096 rounds of the Blowfish cipher setup per hash, limiting GPU-accelerated cracking to around 20,000 guesses per second rather than billions. bcrypt also generates and stores its own salt automatically.

Argon2id, the winner of the Password Hashing Competition (2015), is now the OWASP-recommended choice for new systems. Unlike bcrypt, Argon2id is memory-hard, it requires significant RAM to compute, not just CPU time. This specifically targets GPU and ASIC-based cracking rigs, which have abundant parallel processing but limited per-core memory. Argon2id with m=64MB, t=3, p=4 (as recommended by OWASP) limits cracking rates to around 1,000 per second on modern hardware, a dramatic reduction from the billions-per-second rate achievable against fast hashes.

LinkedIn stored passwords as unsalted SHA-1 hashes. When 6.5 million hashes leaked in June 2012, followed by about 117 million more in 2016, most were cracked within hours using precomputed tables and dictionary attacks. Salted bcrypt, already standard practice in 2012, would have made the breach far less damaging.
:::

%%%

---
unit: Password Attacks
code: PWA
title: Dictionary Attacks
---
:::callout style=soft
A **dictionary attack** is a password cracking technique that leverages precompiled lists of likely passwords, such as common words, leaked credentials, and predictable patterns, rather than exhaustively testing every possible character combination. This method exploits human tendencies toward weak and reused passwords.
:::

:::list heading="Components of a Dictionary" style=plain
- Common dictionary words (e.g., "password", "admin")
- Names and personal identifiers (e.g., "Michael2023")
- Previously breached passwords from sources like Have I Been Pwned
- Keyboard patterns (e.g., "12345678", "qwerty")
- Substituted variants (e.g., "P@ssw0rd", "Adm1n!")
:::

::::columns
::col::
:::callout style=line
**Why It Works**
Users often choose easy-to-remember passwords, which are inherently insecure. These choices reduce the effective entropy of passwords, making dictionary attacks significantly more efficient than brute-force methods.
:::
::col::
:::callout style=line
**Attack Efficiency**
A well-curated dictionary can crack a high percentage of weak passwords in seconds or minutes, especially when compared to the exponential time required for brute-force attacks on longer, random strings.
:::
::::

:::image src="images/06_dictionary_attack_pipeline.png" alt="Flowchart showing wordlist sources (breach databases, common password lists, keyboard patterns) feeding into a rule engine that generates variations, which are then tested against a hash database; match rate percentage shown on the right" caption="Dictionary attack pipeline: wordlists are transformed by rules before being tested against hashed credentials, this dramatically reduces search space while preserving high coverage of real passwords" width=full
:::

:::notes
Dictionary attacks represent a class of password cracking strategies that exploit the predictability of human-selected passwords. Rather than attempting every possible combination of characters, a process known as brute-force cracking, attackers use curated lists of probable passwords. These dictionaries are constructed using common dictionary words, names, leaked credentials from previous data breaches (such as those cataloged by Have I Been Pwned), and predictable user behaviors like substituting characters (e.g., replacing "o" with "0" or "a" with "@").

The National Institute of Standards and Technology (NIST) specifically addresses this vulnerability in Special Publication 800-63B, which discourages the use of commonly used passwords and emphasizes the importance of checking submitted passwords against known compromised lists. This guidance directly counters the effectiveness of dictionary attacks by promoting stronger, less predictable authentication secrets.

Because dictionary attacks rely on precomputed or curated wordlists, they are far more efficient than brute-force techniques, especially when targeting systems without rate-limiting or account lockout mechanisms. For example, a dictionary containing the top 100,000 most common passwords can successfully compromise a significant portion of user accounts in mere seconds on modern hardware, particularly when augmented with rule-based transformations (e.g., toggling case, appending numbers).

This attack method underscores the critical importance of enforcing strong password policies, implementing secure credential storage (e.g., using salted PBKDF2, bcrypt, or Argon2), and educating users about password hygiene. Real-world incidents such as the 2013 Adobe breach and the 2016 LinkedIn breach have provided attackers with millions of plaintext or poorly hashed passwords, many of which continue to appear in dictionaries used in contemporary attacks.

What makes dictionary attacks particularly insidious is that they scale with the quality of available breach data, and breach data has become both more abundant and more actionable over time. The Have I Been Pwned database maintained by Troy Hunt now contains over 14 billion compromised accounts spanning thousands of breaches. These credentials are not merely data points, they are ground truth about how real humans create passwords under real conditions.

Hashcat, the dominant password-cracking tool in both penetration testing and criminal use, supports an extensive rule language that applies transformations to base wordlists: capitalize the first letter, append a two-digit year, replace 'a' with '@', prepend the target company's name. A single moderately-sized wordlist of 1 million words, when expanded with 100 common transformation rules, effectively tests 100 million candidate passwords, covering the vast majority of user-selected passwords in most corporate environments.

The implication for defenders is that password policies based on complexity requirements (uppercase + lowercase + number + symbol) are insufficient. An attacker's rule engine will test "P@ssw0rd1!" just as quickly as "Password1!", both are effectively in the dictionary once the rule is applied. The only reliable defense against dictionary attacks (absent MFA or account lockout) is genuinely random, machine-generated passwords of sufficient length, or passphrases constructed from truly random word selection (e.g., a 5-word Diceware passphrase yielding approximately 65 bits of entropy).
:::

%%%

---
unit: Password Attacks
code: PWA
title: Credential Stuffing, When One Breach Becomes Many
---
:::callout style=soft
**Credential stuffing** is an automated attack that uses username-password pairs stolen from one data breach to attempt unauthorized logins across other services, exploiting widespread password reuse. Unlike brute force, the passwords being tested were valid somewhere; the attacker is betting they're valid everywhere.
:::

::::columns
::col::
:::steps heading="Anatomy of a Stuffing Campaign"
1. Attacker acquires breach dump (e.g., Collection #1: 773M credentials)
2. Filters to email:password format matching target's login scheme
3. Deploys automation tool (OpenBullet, Sentry MBA) with residential proxy network to evade IP blocks
4. Submits credential pairs against target login endpoint at scale
5. Captures "hits", valid logins, for exploitation or resale
:::
::col::
:::list heading="Why It Works So Well" style=plain
- ~65% of users reuse passwords across multiple sites (Google/Harris Poll, 2019)
- Automation tools can test thousands of credentials per minute
- Residential proxy networks bypass IP-based rate limiting
- Defenders cannot distinguish stuffing traffic from legitimate logins without behavioral analysis
:::
::::

:::image src="images/06_credential_stuffing_flow.png" alt="Diagram showing a breached site on the left releasing a credential database, arrows flowing through a credential stuffing tool with proxy rotation, then fanning out to multiple target sites (bank, email, e-commerce) with green checkmarks on sites where reused passwords succeed" caption="Credential stuffing: a single breach multiplies into attacks against dozens of services when users reuse passwords" width=full
:::

:::notes
Credential stuffing is classified under MITRE ATT&CK as technique T1110.004 (Brute Force: Credential Stuffing) and represents one of the most volume-efficient attack techniques available to adversaries today. Unlike traditional brute-force or dictionary attacks, which require guessing at password content, credential stuffing uses verified, real-world password:email pairs that succeeded at authentication on at least one service. The fundamental vulnerability being exploited is not a technical flaw in any system but a human behavioral pattern: password reuse.

The scale of available credential data is staggering. The "Collection #1" dataset, publicized by Troy Hunt in January 2019, contained 773 million unique email addresses and 21 million unique passwords, assembled from thousands of individual breaches. This was not even the largest known collection, subsequent datasets dubbed "Collections #2–#5" added several billion more records. Operators of credential stuffing campaigns purchase or freely download these datasets and use specialized automation tools to systematically test them.

The technical cat-and-mouse between defenders and stuffers has grown sophisticated. Early defenses, IP-based rate limiting, CAPTCHA, were defeated by residential proxy networks (which distribute attack traffic across thousands of legitimate home IP addresses) and CAPTCHA-solving services (which use human workers or ML models to bypass CAPTCHAs at scale for fractions of a cent each). Modern defenses focus on behavioral analytics: studying mouse movement patterns, typing cadence, and device fingerprints to identify automated clients that move too predictably, too fast, or from too many geographically inconsistent locations.

Real-world consequences of credential stuffing are severe. The 2018 Dunkin' Donuts breach (reported under CVE records and FTC disclosures) involved stuffing attacks against their loyalty app, attackers harvested loyalty points worth real money. The 2020 Nintendo breach exposed approximately 160,000 accounts through credential stuffing of legacy NNID credentials. Numerous financial institutions report millions of stuffing attempts daily; successful hits are immediately monetized through fraudulent transactions or account takeover.

The defense is conceptually simple but organizationally difficult to implement at scale. Password uniqueness, using a different password on every service, completely eliminates the cross-service reuse that stuffing exploits. Password managers make this feasible. MFA provides a second layer: even if the password is valid, the attacker cannot complete authentication without the second factor. Bot detection (via tools like Cloudflare Bot Management, Akamai Bot Manager, or PerimeterX) identifies and blocks automated traffic before it reaches the authentication endpoint. Breach notification services alert users when their credentials appear in new dumps, prompting proactive password changes.

Have I Been Pwned (haveibeenpwned.com) reports which known breaches have exposed a given email address, showing directly how widely personal credentials circulate.
:::

%%%

---
unit: Password Attacks
code: PWA
title: Password Spraying, Low and Slow Wins the Race
---
:::callout style=soft
**Password spraying** is the inverse of brute force: instead of trying many passwords against one account, the attacker tries a few very common passwords against many accounts. This evades lockout policies while still exploiting predictable human password choices.
:::

::::columns
::col::
:::table
| Technique | Passwords per Account | Accounts Targeted | Lockout Risk |
|---|---|---|---|
| Brute Force | Thousands–millions | One | High |
| Dictionary Attack | Hundreds–thousands | One | High |
| Password Spraying | 1–3 | Thousands | Low (by design) |
| Credential Stuffing | One (known) | Millions | Low (by design) |
:::
::col::
:::callout style=line
**The Lockout Threshold Problem**

Most enterprise systems lock accounts after 5–10 failed attempts. Spraying tests only 1–3 passwords per account, never triggering the lockout threshold, while the broad coverage across thousands of accounts virtually guarantees at least some successes.
:::
::::

:::list heading="Most Commonly Sprayed Passwords (Enterprise)" style=plain
- `[CompanyName]2024!`, seasonal, company-branded patterns
- `Welcome1!` / `Welcome2024`, new-hire defaults that go unchanged
- `Password1!`, satisfies most legacy complexity requirements
- `[Month][Year]!`, e.g., `January2024!`
- `[Season][Year]!`, e.g., `Spring2024!`
:::

:::image src="images/06_password_spraying_diagram.png" alt="Grid diagram showing many user accounts on the left and a small set of passwords on the right; arrows show each password being tested against every account; highlighted cells show the small percentage that succeed; lockout counter below each account remains at 1 or 2 never reaching the threshold" caption="Password spraying: staying below the lockout threshold while testing at breadth, a few successes across thousands of accounts is enough" width=full
:::

:::notes
Password spraying is classified under MITRE ATT&CK as T1110.003 (Brute Force: Password Spraying) and represents a particularly effective attack against enterprise Active Directory environments. The technique exploits a fundamental tension in access control design: account lockout policies are intended to stop brute-force attacks, but they create a perverse incentive, attackers simply reduce their per-account password attempts to stay below the threshold.

The attack is especially effective against organizations with large user populations, because even a low success rate translates to multiple compromised accounts when thousands of users are tested. In an organization with 5,000 users, if just 1% use "Welcome1!" as their password, the attacker gains 50 valid credentials, more than enough to begin lateral movement and privilege escalation within the network.

Enterprise Active Directory environments are the primary target because the organizational email address format (firstname.lastname@company.com) is predictable and discoverable through LinkedIn, company websites, or email format guessing tools like Hunter.io. An attacker outside the network can enumerate a target list of email addresses and then attempt spraying against cloud services like Microsoft 365 or Google Workspace, which authenticate against the same Active Directory or LDAP directory as the internal network.

Several high-profile nation-state campaigns have used password spraying as an initial access technique. The SolarWinds attackers (NOBELIUM/Cozy Bear) used password spraying as one component of their reconnaissance phase. Iranian state-sponsored group APT33 (Refined Kitten) has extensively used password spraying against energy, aerospace, and government targets. The FBI and CISA have issued joint advisories specifically warning about spraying as a persistent threat to critical infrastructure.

Detection of password spraying requires different monitoring approaches than brute-force detection. Rather than alerting on multiple failures for a single account, defenders need to monitor across accounts: multiple different accounts each receiving a small number of failed authentication attempts within a short window, especially using the same password, is the spraying signature. SIEM rules that implement this cross-account correlation are critical, as are tools like Microsoft Defender for Identity (formerly Azure ATP), which specifically detects spraying patterns in Active Directory environments.

Prevention is straightforward in principle: MFA eliminates spraying as an effective attack immediately, because even when a password is successfully guessed, the second factor blocks access. Breach password screening eliminates the specific passwords most likely to be sprayed. Conditional access policies that block authentication from unexpected geographies or unmanaged devices add another layer. For organizations that cannot immediately implement MFA for all users, a targeted rollout prioritizing accounts with elevated privileges, administrators, finance staff, executives, provides the highest risk reduction per unit of implementation effort.

Microsoft's published analysis of password-spraying attacks against Azure AD lists the passwords most often tried and shows that spray campaigns run during business hours to blend in with normal authentication traffic.
:::

%%%

---
unit: Password Attacks
code: PWA
title: Worked Example, Cracking a Password Hash Step by Step
---
:::callout style=soft
This worked example traces the complete process an attacker follows after obtaining a database of hashed passwords, from acquiring the hash to cracking it and accessing the account. Understanding the attack process in detail is essential for designing effective defenses.
:::

:::steps heading="Step-by-Step: Cracking an MD5 Hash with Hashcat"
1. **Obtain hash database**, SQL injection on vulnerable login page yields: `user@example.com:482c811da5d5b4bc6d497ffa98491e38`
2. **Identify hash type**, `hashid 482c811da5d5b4bc6d497ffa98491e38` → MD5 (32-character hex string, no salt detected)
3. **Select attack mode**, dictionary attack with rules: `hashcat -m 0 -a 0 hash.txt rockyou.txt -r best64.rule`
4. **GPU acceleration**, Hashcat leverages GPU; MD5 processes at ~300 billion hashes/second on modern hardware
5. **Result**, `482c811da5d5b4bc6d497ffa98491e38:password123` cracked in < 1 second
6. **Credential stuffing follows**, attacker tests `user@example.com:password123` across 50 other services automatically
:::

::::columns
::col::
:::table
| Hash Algorithm | Example Hash (of "password123") | Crack Time (GPU) |
|---|---|---|
| MD5 | `482c811da5d5b4bc6d497ffa98491e38` | < 1 second |
| SHA-1 | `cbfdac6008f9cab4083784cbd1874f76...` | < 1 second |
| bcrypt (cost 10) | `$2a$10$N9qo8uLOickgx2ZMRZoMye...` | Hours–days |
| Argon2id | `$argon2id$v=19$m=65536,t=3,p=4$...` | Days–years |
:::
::col::
:::callout style=line
**What the Attacker Sees vs. What the Defender Controls**

The attacker controls the GPU hardware and tool selection. The defender controls the hash algorithm, the salt, the cost factor, and whether MFA is required, all of which can make cracking computationally infeasible.
:::
::::

:::image src="images/06_hash_cracking_worked_example.png" alt="Terminal-style screenshot showing Hashcat command, progress bar showing 100% completion, and the cracked result 'password123'; annotations point to hash type, dictionary file, rule file, and crack speed in billions of hashes per second" caption="Hashcat cracking an MD5 hash in under one second, the entire cracking process takes longer to read about than to execute against a weak hash" width=full
:::

:::notes
Walking through a concrete cracking example is the most effective way to make abstract cryptographic concepts tangible for students. The scenario above is realistic and representative: SQL injection vulnerabilities that expose database contents remain one of the most common initial access vectors, ranked in the OWASP Top 10 (A03:2021 – Injection). An attacker who obtains a database table containing usernames and password hashes has effectively captured credentials for every account in that database, the question is only whether cracking those hashes is feasible.

The tool of choice for offline password cracking is Hashcat, an open-source project that leverages GPU acceleration to achieve cracking speeds that are orders of magnitude faster than CPU-based tools. Hashcat supports over 300 hash types and multiple attack modes: straight dictionary, combination, brute-force mask, rule-based, and hybrid. It is used by penetration testers, red teams, and criminal actors alike, the same tool serves both offensive research and malicious exploitation.

MD5, despite being formally deprecated for security purposes since at least 2004 (RFC 6151), continues to appear in production systems discovered during breach investigations. The reasons are historical inertia and technical debt: web applications built in the early 2000s used MD5 because it was the available option in PHP's password hashing functions (`md5()` was the idiomatic approach), and many were never migrated. The 2013 Adobe breach (153 million accounts) stored passwords as unsalted 3DES-ECB (technically an encryption rather than a hash, but equally weak for this purpose), allowing cracking of nearly all passwords within weeks of the breach.

The comparison table illustrates the dramatic difference that algorithm selection makes. Against MD5 at 300 billion attempts per second, "password123" is found essentially instantly, it's near the top of the RockYou wordlist. Against bcrypt at cost 10 (approximately 100ms per hash on a single CPU core), the same GPU cluster achieves perhaps 10,000–20,000 attempts per second, meaning a 10-million-word dictionary takes 10 minutes rather than microseconds, and a 100-billion combination brute-force search takes effectively forever. Argon2id with its memory-hardness requirement reduces GPU throughput even further, often to the point where even dedicated cracking hardware provides negligible speed advantage over a standard CPU.

The takeaway for defenders is that algorithm selection is a policy decision with enormous security consequences. Migrating from MD5 or SHA-1 to Argon2id, a one-time code change in the authentication layer, transforms a breach from "all passwords compromised immediately" to "all passwords secure for years." PHP 5.5 introduced `password_hash()` with bcrypt as the default; Python has `passlib`; Java has Spring Security's `BCryptPasswordEncoder`. Every major web framework provides appropriate password hashing as a first-class feature, there is no longer any excuse for using weak hash functions in new code.

Unsalted MD5 hashes of weak passwords fall almost instantly to tools such as Hashcat, including passwords that look complex. The speed of cracking is the strongest argument for slow, salted password storage.
:::

%%%

---
unit: Password Attacks
code: PWA
title: Case Study, The LinkedIn Breach (2012 & 2016)
---
:::callout style=soft
In June 2012, LinkedIn disclosed that approximately 6.5 million password hashes had been leaked. In 2016, it emerged that the actual breach was vastly larger, 117 million accounts, and the underlying cause was a fundamental failure of secure password storage: **unsalted SHA-1 hashes**.
:::

::::columns
::col::
:::steps heading="Breach Timeline"
1. **2012, Initial disclosure:** 6.5 million SHA-1 hashes posted to Russian forum; LinkedIn confirms breach
2. **Hours later:** Security researchers crack 90%+ of the 6.5M hashes using rainbow tables and dictionary attacks
3. **2016, Full scope revealed:** Hacker "Peace_of_Mind" sells 117M credential pairs on dark web for 5 Bitcoin (~$2,200)
4. **2016, Cracking:** Majority of 117M hashes cracked within days using Hashcat + RockYou wordlist
5. **Cascading impact:** Credentials used in credential stuffing campaigns against dozens of other services
:::
::col::
:::callout style=line
**Why SHA-1 Was the Wrong Choice**

LinkedIn stored passwords as unsalted SHA-1 hashes, a cryptographic hash function designed for speed and data integrity, not password storage. Without salts, identical passwords produced identical hashes, allowing one rainbow table lookup to reveal every instance of "password123" across all 117 million accounts simultaneously.
:::
::::

:::table
| Failure | Technical Root Cause | Correct Control |
|---|---|---|
| Passwords cracked instantly | Unsalted SHA-1 (fast hash) | Argon2id or bcrypt with per-password salt |
| Scope unknown for 4 years | Insufficient log retention / audit | SIEM with long-term log archival (ISO 27001 A.12.4) |
| Cascading damage to other services | Users reused passwords | MFA + password manager adoption |
:::

:::image src="images/06_linkedin_breach_timeline.png" alt="Horizontal timeline from 2012 to 2016 showing: breach occurs, 6.5M hashes leaked, rapid cracking, full 117M scope revealed, dark web sale, cascading credential stuffing attacks on other platforms; icons show each event" caption="LinkedIn breach timeline: four years elapsed between the breach and full public disclosure, illustrating both the scale of the failure and the persistence of credential exposure" width=full
:::

:::notes
The LinkedIn breach is one of the most instructive case studies in password security history, not because LinkedIn was unusually negligent but because they made choices that were common practice at the time, and the consequences were severe enough to reshape industry standards.

In 2012, SHA-1 was already known to be weakening as a cryptographic hash (theoretical collision attacks existed), but it remained widely used for password storage largely because it was the default in many web frameworks and had not yet produced spectacular failures. LinkedIn's specific failure was not using SHA-1 per se, but using it without salts, a practice that was already known to be insecure. The OWASP Password Storage Cheat Sheet had been recommending salted bcrypt since at least 2010. LinkedIn's engineering team either was unaware of this guidance or chose not to implement it, a choice that would ultimately expose 117 million users.

The technical impact of the unsalted storage was precisely what security practitioners had warned about. Because there was no per-password salt, every instance of "password123" in the database produced the same SHA-1 hash: `cbfdac6008f9cab4083784cbd1874f76570de616`. A single crack of that hash, taking milliseconds, simultaneously revealed the password for every user who chose "password123." Analysis of the leaked dataset found that over 1 million LinkedIn users had that password. Rainbow table lookups handled a massive percentage of the database without any per-hash computation.

The four-year gap between the 2012 breach and the 2016 full disclosure is itself a significant finding. LinkedIn's initial 2012 investigation apparently failed to identify the full scope of the breach, or if they did, they chose not to disclose it. This underscores the importance of comprehensive audit logging (ISO/IEC 27001 Annex A.12.4) and breach notification requirements (now mandated under GDPR Article 33 and various state laws including California's CCPA). A breach notification law requiring disclosure within 72 hours of discovery would have fundamentally changed the 2012 response.

The cascading damage from the breach extended for years. The 2016 dark web sale triggered waves of credential stuffing attacks against email providers, financial services, and other tech platforms. Users who had used the same email:password combination on other services found their accounts compromised, often without any obvious connection to LinkedIn. This pattern, a single breach creating years of downstream credential-stuffing attacks, is now so well-documented that major platforms like Dropbox, Spotify, and others have implemented automatic credential stuffing detection and forced password resets when they detect login attempts using credentials from known breach dumps.

After the 2012 breach LinkedIn moved all stored passwords to bcrypt and forced resets for affected users. Its engineering posts on the incident are an unusually transparent record of post-breach remediation at a major technology company.
:::

%%%

---
unit: Password Attacks
code: PWA
title: Case Study, The 2020 Twitter Hack
---
:::callout style=soft
In July 2020, attackers compromised 130 high-profile Twitter accounts, including Barack Obama, Elon Musk, and Joe Biden, to run a Bitcoin scam that netted over $120,000 in hours. The breach was not a password crack or a technical exploit: it was a **social engineering attack on Twitter's own employees**.
:::

::::columns
::col::
:::steps heading="Attack Chain"
1. **Vishing (voice phishing):** Attackers called Twitter employees posing as IT support, convincing them to enter credentials on a fake internal VPN portal
2. **Internal admin tool access:** Stolen employee credentials provided access to Twitter's "@admin" tooling
3. **Account takeover:** Attackers used admin tools to change email addresses and disable 2FA on target accounts, then changed passwords
4. **Scam deployment:** High-profile accounts tweeted Bitcoin scam links; $120,000+ collected in hours
5. **Attribution:** Three individuals arrested, a 17-year-old in the UK, a 22-year-old in Florida, and a 16-year-old in Massachusetts
:::
::col::
:::callout style=line
**What MFA Would and Would Not Have Stopped**

Standard TOTP-based MFA would not have stopped this attack, the social engineering obtained real-time credentials from willing employees. Only **phishing-resistant MFA** (FIDO2 hardware keys) would have prevented the vishing step, because the authentication challenge is cryptographically bound to the real domain and cannot be replayed from a fake portal.
:::
::::

:::table
| Attack Step | Control That Would Have Helped | Standard Reference |
|---|---|---|
| Vishing of employee credentials | FIDO2 hardware keys (phishing-resistant MFA) | NIST SP 800-63B AAL3 |
| Admin tool misuse | Privileged Access Management (PAM), just-in-time access | CIS Control 12 |
| Rapid account changes | Admin action rate limiting, dual approval for sensitive actions | ISO 27001 A.9.4 |
| Delayed detection | SIEM alerting on unusual admin activity patterns | NIST CSF DE.CM-3 |
:::

:::image src="images/06_twitter_hack_attack_chain.png" alt="Step-by-step attack chain diagram: phone icon with voice phishing arrow to employee laptop, credential capture arrow to fake VPN portal, access arrow to Twitter admin tool interface, bulk account change arrows to celebrity account icons, Bitcoin scam deployment at end" caption="2020 Twitter hack attack chain: the entire compromise hinged on social engineering one employee, authentication strength at the final service meant nothing when the admin tools had no second-approval controls" width=full
:::

:::notes
The 2020 Twitter hack is a pivotal case study because it illustrates the limitations of authentication controls when the attack targets the human layer rather than the technical layer. Twitter's regular user accounts had MFA options available; many of the compromised celebrities may well have had MFA enabled. None of that mattered, because the attacker never needed to authenticate as those users, they obtained Twitter employee credentials through social engineering and then used Twitter's own administrative tooling to bypass all user-level authentication controls entirely.

The attackers, later identified as a loosely organized group of teenagers, used telephone-based social engineering (vishing) to target Twitter employees. They posed as members of Twitter's IT department and convinced employees to enter their credentials on a fraudulent website designed to mimic Twitter's internal VPN login portal. This is a textbook credential-harvesting phishing attack, executed over the phone rather than via email. Once they had valid employee credentials, they used them to access Twitter's internal tools, tools that apparently had very broad capabilities, including the ability to change account email addresses, disable 2FA, and initiate password resets.

The technical failure that enabled escalation was the existence of overly permissive internal admin tools with insufficient access controls. The principle of least privilege (NIST SP 800-53 AC-6) requires that even internal tools grant only the minimum capabilities necessary for the user's role. Twitter's tooling apparently allowed any employee with access to perform account takeover operations that should have required multiple approvals, out-of-band verification, or privileged access management controls. Privileged Access Management (PAM) solutions, which enforce time-limited, purpose-specific access to sensitive tools with comprehensive logging, exist precisely to prevent this class of insider or socially-engineered attack.

The authentication lesson is subtle but important: FIDO2 hardware keys would have blocked the credential-harvesting phase. FIDO2's phishing resistance is cryptographic, the authentication response is bound to the specific origin URL (twitter-internal-vpn-real.corp.twitter.com), so credentials captured on the fake phishing site (twitter-support-help.com) would fail when replayed at the real site. This is why NIST SP 800-63B Authenticator Assurance Level 3 (AAL3) mandates hardware-based phishing-resistant authenticators for high-value privileged accounts. Google's mandatory rollout of FIDO2 keys to all employees in 2017 resulted in zero successful phishing attacks against employee accounts thereafter, a direct, measurable security improvement.

Three people were charged for the July 2020 Twitter breach. The organizer, Graham Ivan Clark, a 17-year-old from Florida, was sentenced to three years in juvenile detention; his co-defendants were Mason Sheppard of the United Kingdom and Nima Fazeli of Florida. The attack needed no advanced technical skill, only social engineering of employees who believed they were dealing with internal IT staff.
:::

%%%

---
unit: Defense
code: CHK
title: Mid-Lecture Checkpoint, Concepts So Far
---
:::callout style=soft
Let's pause and verify understanding of the concepts covered so far before moving into defensive strategies. These questions mirror the style used on CompTIA Security+ exam.
:::

:::list heading="Check Your Understanding" style=plain
- **Q1:** A penetration tester obtains a database of unsalted MD5 hashes. What attack type is MOST efficient, and why?
- **Q2:** An attacker attempts "Password1!" against 10,000 user accounts, trying each account only once. What attack technique is this?
- **Q3:** A user's LinkedIn credentials from the 2016 breach are used to access their bank account. What attack technique does this represent?
- **Q4:** Which authentication factor type does a hardware FIDO2 key represent?
- **Q5:** NIST SP 800-63B moved away from mandatory password rotation. What does it recommend instead?
:::

:::table
| Question | Answer | Key Concept |
|---|---|---|
| Q1 | Rainbow table / dictionary attack, fast hash + no salt = instant precomputed lookup | Hash algorithm selection, salting |
| Q2 | Password spraying, low volume per account, broad account coverage | Lockout evasion via breadth |
| Q3 | Credential stuffing, breach credentials reused across services | Password reuse exploitation |
| Q4 | Something you have (possession factor) | Authentication factor categories |
| Q5 | Screen against breach databases; rotate only on confirmed compromise | NIST SP 800-63B evidence-based policy |
:::

:::image src="images/06_checkpoint_quiz_graphic.png" alt="Clean quiz-style graphic with five numbered question cards arranged in a grid, each with a brief question text; below the grid, five answer cards with matching numbers; a stopwatch icon in the corner indicates timed review" caption="Mid-lecture checkpoint: five questions covering authentication fundamentals, attack taxonomy, and NIST policy guidance, essential Security+ exam concepts" width=full
:::

:::notes
This checkpoint is designed to consolidate the first half of the lecture before moving into defensive strategies. Research in educational psychology consistently shows that retrieval practice, actively recalling information from memory, produces significantly stronger long-term retention than passive re-reading or listening. The act of formulating an answer, even when uncertain, activates memory consolidation processes that passive review does not. This is the "testing effect" described in Roediger and Butler (2011) and replicated extensively in subsequent research.

The five questions are calibrated to CompTIA Security+ exam style and difficulty. Question 1 tests understanding of why hash algorithm and salting choices determine attack feasibility, a purely technical question about the relationship between MD5's speed, the absence of salts, and rainbow table applicability. The key insight is that "most efficient" refers to the fact that a precomputed rainbow table lookup is O(1), essentially instant, whereas even dictionary attacks require per-hash computation. Without salts, a single crack reveals all accounts with the same password.

Question 2 tests the ability to recognize password spraying from its behavioral signature: low per-account attempts, broad account coverage. Students sometimes confuse spraying with credential stuffing; the distinction is that spraying uses a small set of guessed passwords (not verified credentials from a breach), while stuffing uses known valid credentials from a prior breach. The single attempt per account pattern and the use of a common password across many accounts is the spraying signature.

Question 3 tests credential stuffing recognition, the chain of events is the giveaway: credentials from a known breach at one service being used against a different service. The multi-service scope and the use of previously verified credentials distinguish this from spraying.

Question 4 tests authentication factor classification. Hardware security keys can confuse students because they involve cryptographic computation (which sounds like "something you know", cryptographic knowledge), but the security property comes from physical possession of the device. The private key inside a FIDO2 key is hardware-bound and cannot be extracted, so the possession of the physical device is the authentication factor. This matches the "something you have" category.

Question 5 tests NIST SP 800-63B knowledge specifically around the policy shift on mandatory rotation. The correct answer, breach database screening, rotation only on confirmed compromise, is frequently tested on Security+ because it represents a documented reversal of long-standing conventional wisdom. Students who have only studied older materials may have the wrong answer memorized from prior guidance.

Two points are commonly confused at this stage: precomputed lookup with a rainbow table is not the same as brute force, and regular forced rotation is no longer recommended by NIST SP 800-63B.
:::

%%%

---
unit: Defense
code: POL
title: Password Policies, Building Better Defenses
---

::::columns
::col::
:::list heading="What Modern Guidance Recommends" style=plain
- Prioritize password length over arbitrary complexity
- Screen new passwords against known breached-password datasets
- Avoid mandatory periodic password changes unless there's evidence of compromise
- Enforce unique passwords per account to limit credential-stuffing risks
:::

::col::
:::callout style=line
NIST SP 800-63B moved away from traditional complexity rules like "1 uppercase, 1 number, 1 symbol", these often led to predictable substitutions (e.g., "P@ssw0rd").
:::
::::

:::table
| Policy Element               | Old Approach                          | Modern Best Practice                          |
|----------------------------|----------------------------------------|------------------------------------------------|
| Minimum Length             | 8 characters                           | 12–16+ characters (passphrases encouraged)     |
| Character Requirements     | Forced symbols/numbers                 | No enforced complexity; prioritize entropy     |
| Password Expiry            | Every 30–90 days                       | Only when breach or compromise is suspected    |
| Reuse Prevention           | Limited history (e.g., last 5)         | Comprehensive check against breached datasets  |
| User Feedback              | Generic rejection messages             | Real-time feedback on breached or weak entries |
:::

:::image src="images/06_password_policy_evolution.png" alt="Timeline showing password policy evolution from 2000 to present: left side shows old NIST rules (complexity, expiry) with checkmarks evolving to right side showing modern guidance (length, breach screening, no forced rotation); arrows indicate the shift" caption="Password policy evolution: research-backed NIST SP 800-63B (2017) reversed decades of conventional wisdom on complexity and mandatory rotation" width=full
:::

:::steps heading="Modern Password Policy Implementation Checklist"
1. **Set minimum length to 12 characters**, NIST recommends at least 8 but 12–16 is the operational target; allow up to 64 characters (or more) to support passphrases
2. **Integrate breach database screening**, Check submitted passwords against Have I Been Pwned's Pwned Passwords API (k-anonymity model preserves privacy) at account creation and password change
3. **Remove mandatory rotation schedules**, Eliminate 90-day forced resets; institute rotation only upon confirmed or suspected compromise
4. **Provide real-time strength feedback**, Use zxcvbn or similar entropy estimation libraries to give users actionable guidance at the point of password creation
5. **Enforce account-level uniqueness**, Flag or block password reuse across departmental systems where technically feasible
6. **Support password managers**, Ensure login fields allow paste, disable clipboard overrides, and accept long passwords to encourage use of password managers
:::

:::notes
In the past, password policies were largely shaped by compliance frameworks that emphasized visible complexity, such as requiring uppercase letters, numbers, and special characters. These rules, while well-intentioned, often resulted in predictable user behavior. For example, users frequently appended a "1" or replaced an "o" with a "0", leading to passwords like "P@ssw0rd1", which are easily guessed by modern cracking tools using pattern dictionaries.

The shift toward evidence-based password policies is most clearly articulated in NIST Special Publication 800-63B, *Digital Identity Guidelines*, which emphasizes usability and resistance to common attack vectors. NIST recommends a minimum of 8 characters for user-chosen passwords (14+ for administrators), but strongly encourages the use of longer passphrases, sequences of random or semi-random words that are easier to remember and harder to crack via brute-force or dictionary attacks.

One of the most impactful changes is the deprecation of mandatory periodic password changes for users who have not exhibited signs of compromise. Research, including studies cited by Microsoft and Carnegie Mellon University, has shown that frequent password resets often result in weaker passwords over time, as users resort to simple patterns or slight variations of old credentials. Instead, NIST advises organizations to monitor for breaches and enforce changes only when necessary.

Another key recommendation is screening new passwords against known compromised password databases, such as those compiled from breaches and exposed credential sets (e.g., the Have I Been Pwned API). This prevents users from selecting passwords that are already in the hands of attackers.

Finally, enforcing password uniqueness across accounts is critical to mitigating credential-stuffing attacks, where adversaries use previously breached credentials en masse to gain unauthorized access to other systems. CVE-2021-32619 and similar incidents underscore the risks of password reuse in enterprise environments.

By aligning password policies with behavioral science and cryptographic realities, organizations can build more resilient authentication systems without sacrificing usability.

The organizational change management dimension of password policy is often underestimated. Telling employees that they no longer need to change their password every 90 days is frequently met with confusion or skepticism, it runs counter to ingrained habits instilled by years of prior policy. Security awareness programs must therefore explicitly explain the reasoning: that forced rotation produces predictable incremental changes (Password1! → Password2! → Password3!) that attackers account for, while stable strong passphrases combined with MFA provide substantially better security. The "why" must accompany every "what" in security policy communication or adoption will lag.

Password managers deserve special mention here. NIST SP 800-63B explicitly endorses the use of password managers as a means of enabling strong, unique passwords across accounts without imposing an impossible memorability burden on users. Organizations should therefore ensure that their systems are password-manager-friendly: login forms must allow clipboard paste (many web applications explicitly block this, defeating password managers), must accept passwords of 64+ characters, and must not impose arbitrary character-set restrictions that prevent use of manager-generated random strings.
:::

%%%

---
unit: Defense
code: POL
title: Passphrases, Memorability Without Sacrificing Security
---
:::callout style=soft
A **passphrase** is an authentication secret composed of multiple words rather than a single complex string. When words are selected randomly (not chosen by the user), passphrases combine high entropy with genuine memorability, solving the fundamental tension between security and usability.
:::

::::columns
::col::
:::table
| Approach | Example | Entropy | Memorability |
|---|---|---|---|
| Complex password rule | `P@ssw0rd1!` | ~34 bits (but in dictionaries) | Low |
| Random 12-char password | `xK#9mL!qPv2@` | ~79 bits | Very low |
| 3-word passphrase (user-chosen) | `mydog2023summer` | ~20–30 bits (predictable) | High |
| 4-word Diceware | `correct-horse-battery-staple` | ~52 bits | High |
| 5-word Diceware | `staple-horse-battery-correct-lamp` | ~65 bits | Moderate-High |
:::
::col::
:::callout style=line
**The Diceware Method**

Diceware uses five physical dice rolls to select each word from a standardized 7,776-word list (6^5 = 7,776). Because the selection is truly random and from a large word pool, each word contributes ~12.9 bits of entropy, making a 5-word Diceware passphrase resistant to all practical attacks while remaining genuinely memorable.
:::
::::

:::steps heading="Creating a Diceware Passphrase"
1. Obtain or print the EFF Diceware word list (publicly available at eff.org)
2. Roll five dice for each word, the five numbers map to one word on the list
3. Repeat for 4–6 words depending on required security level
4. Record the resulting phrase (e.g., "piano raven orbit chess flame")
5. Memorize through spaced repetition, use it daily for a week, then it sticks
:::

:::image src="images/06_passphrase_diceware_visual.png" alt="Illustration showing five physical dice with numbers, an arrow pointing to a Diceware word list with the matching row highlighted, and the resulting word shown; repeated four more times producing a five-word passphrase at the bottom" caption="Diceware passphrase generation: physical randomness (dice) combined with a public word list ensures entropy cannot be gamed by human choices" width=full
:::

:::notes
The passphrase concept is not new, it was advocated by cryptographer Bruce Schneier as far back as the 1990s, but it gained widespread recognition through Randall Munroe's xkcd comic #936 (2011), which illustrated with clear mathematics why four random words like "correct horse battery staple" are both more memorable and more secure than a complex password like "Tr0ub4dor&3." NIST SP 800-63B has since formally endorsed passphrases as an acceptable and encouraged approach to memorizable secrets, provided the words are genuinely randomly selected rather than user-chosen.

The critical distinction is between user-selected passphrases and randomly generated ones. Research by Joseph Bonneau and colleagues at Cambridge found that human-chosen passphrases cluster around common patterns: famous quotes, song lyrics, pop culture references, and phrases that are personally meaningful. "MayTheForceBeWithYou" might seem like a passphrase with high entropy, but because it's a recognizable cultural phrase, it would appear early in any attack that includes phrase-based wordlists. True passphrase entropy requires randomness in the selection process, which is exactly what Diceware provides.

The EFF (Electronic Frontier Foundation) updated the original Diceware word list in 2016 to use longer, more common words that are easier to spell and visualize, improving memorability without reducing entropy. The EFF's five-word list provides 5 × log₂(7,776) ≈ 64.6 bits of entropy, exceeding the 60-bit minimum recommended for high-security applications.

From a usability perspective, passphrases are superior to complex random strings in several measurable ways. Password recall accuracy is higher for passphrases than for random character strings of equivalent entropy. Typing speed is faster (words are chunked motor programs, while random character strings require character-by-character attention). Error rates during typing are lower. These usability advantages mean that organizations promoting passphrase adoption actually see improved security outcomes, not just theoretical improvements, because users are less likely to write down passphrases, less likely to store them insecurely, and less likely to need password resets.

The principal limitation of passphrases is length, a 5-word Diceware passphrase averages about 32 characters (including separators). Some legacy systems have maximum password length limits as low as 16 characters, making passphrase adoption impossible on those platforms. NIST SP 800-63B explicitly states that systems must support passwords of at least 64 characters to accommodate passphrases, systems with shorter maximums are technically non-compliant with NIST guidance and should be flagged for remediation.

Diceware generates passphrases by rolling physical dice to select words from a list such as the EFF long word list (7,776 words). Five words give about 64.6 bits of entropy, enough to resist offline GPU cracking of a properly hashed password for many years.
:::

%%%

---
unit: Defense
code: STO
title: Password Hashing, bcrypt, scrypt, and Argon2
---
:::callout style=soft
Passwords must never be stored in plaintext or with fast general-purpose hash functions. **Password hashing algorithms**, bcrypt, scrypt, and Argon2, are specifically designed to be slow and resource-intensive, making brute-force cracking computationally impractical even after a database breach.
:::

::::columns
::col::
:::table
| Algorithm | Year | Memory-Hard? | GPU Resistant? | OWASP Recommendation |
|---|---|---|---|---|
| MD5 | 1992 | No | No | Never use for passwords |
| SHA-256 | 2001 | No | No | Never use for passwords |
| bcrypt | 1999 | No | Moderate | Acceptable (cost ≥ 10) |
| scrypt | 2009 | Yes | Yes | Acceptable |
| PBKDF2 | 2000 | No | Moderate | Acceptable (FIPS compliant) |
| Argon2id | 2015 | Yes | Yes | **Preferred** |
:::
::col::
:::callout style=line
**What "Memory-Hard" Means**

A memory-hard function requires large amounts of RAM to compute, not just CPU time. This specifically resists GPU and ASIC-based cracking, because GPUs have many cores but limited per-core memory. Argon2id with m=64MB requires each crack attempt to use 64MB of RAM, a GPU with 8GB VRAM can run fewer than 128 parallel attempts, versus millions of parallel attempts against a non-memory-hard hash.
:::
::::

:::steps heading="How bcrypt Works"
1. Accept plaintext password and a cost factor (e.g., 12)
2. Generate a 16-byte cryptographically random salt
3. Run 2^cost (4,096 for cost=12) rounds of the Blowfish key setup
4. Output a 60-character string containing: algorithm version + cost + salt + hash
5. Store the complete 60-character string, the salt is embedded, no separate storage needed
:::

:::image src="images/06_password_hashing_comparison.png" alt="Side-by-side comparison of MD5 versus Argon2id: left panel shows MD5 hash computed in nanoseconds with no salt, GPU cracking at 300B/sec; right panel shows Argon2id taking 300ms per hash with embedded salt and memory requirements, GPU limited to ~1000 attempts/sec" caption="Password hashing algorithms compared: Argon2id's computational and memory costs make GPU-accelerated cracking orders of magnitude slower than fast hashes like MD5" width=full
:::

:::notes
The choice of password hashing algorithm is one of the highest-leverage security decisions an application developer makes. Unlike most security controls, which can be added after deployment, the password hashing algorithm is baked into every stored credential, migrating to a stronger algorithm requires a complete re-hash of all stored passwords, typically at the next successful login for each user. This makes getting it right at initial deployment critical.

The fundamental property that distinguishes a password hashing algorithm from a general-purpose cryptographic hash is intentional computational cost. Cryptographic hash functions like SHA-256 are designed for speed, they need to hash large files or data streams efficiently, which means computing millions or billions of hashes per second per CPU core. This speed is a catastrophic property for password storage: an attacker who obtains a database of SHA-256-hashed passwords can test every password in the RockYou dataset (14 million entries) in milliseconds.

bcrypt, designed by Niels Provos and David Mazières and introduced in 1999, was the first widely adopted slow password hash specifically designed to counter offline cracking. Its key innovation is the configurable cost factor, which controls the number of Blowfish cipher key setup rounds performed. As hardware becomes faster, the cost factor can be increased, OWASP currently recommends a cost factor of at least 10, with 12 preferred for new systems. At cost 12, a modern server CPU can compute approximately 1–4 bcrypt hashes per core per second, compared to billions of SHA-256 hashes per second. This ratio, a billion-fold speed reduction for the attacker, is the core security benefit.

scrypt, designed by Colin Percival and published in 2009, introduced memory-hardness as an additional dimension of resistance. Beyond requiring time, scrypt requires memory, specifically, the working set of each hash computation must fit in RAM and cannot be reduced without increasing computation time. This specifically targets GPU-based cracking: while GPUs have thousands of shader cores for parallel computation, each core has access to only a small amount of dedicated memory. A memory-hard function that requires 32MB per hash attempt limits a GPU with 8GB VRAM to 256 parallel attempts, compared to potentially millions of parallel SHA-256 attempts.

Argon2id, the winner of the 2015 Password Hashing Competition (a NIST-organized public competition to identify a new standard), combines the time-hardness of bcrypt with the memory-hardness of scrypt while adding resistance to time-memory trade-off attacks. It offers three variants: Argon2d (memory-hard, optimal for CPU/GPU resistance), Argon2i (resistant to side-channel attacks), and Argon2id (hybrid, recommended for most applications). OWASP currently recommends Argon2id with m=19,456 KB (19 MB), t=2 iterations, p=1 parallelism for general use, scaling up to m=65,536 KB for high-security applications.

PBKDF2 (Password-Based Key Derivation Function 2), while not memory-hard, remains significant because it is FIPS 140-2 compliant, a requirement for US federal government systems and many regulated industries. When FIPS compliance is mandated, PBKDF2-HMAC-SHA256 with at least 310,000 iterations (OWASP 2023 recommendation) is the appropriate choice. The iteration count effectively slow the hash computation proportionally, achieving similar (though not identical) resistance to Argon2id.

Password hashing should use maintained libraries, never custom code. PHP offers password_hash with PASSWORD_BCRYPT (since PHP 5.5) and PASSWORD_ARGON2ID (since PHP 7.3); Python has argon2-cffi and passlib; Java has Spring Security's Argon2PasswordEncoder.
:::

%%%

---
unit: Defense
code: STO
title: Salting, Why Every Hash Must Be Unique
---
:::callout style=soft
A **cryptographic salt** is a random value generated uniquely for each password and combined with the password before hashing. Salts ensure that identical passwords produce different hash values, defeating precomputed attacks like rainbow tables and preventing batch cracking of multiple accounts simultaneously.
:::

::::columns
::col::
:::flow
User creates password: "hunter2"
System generates random 32-byte salt: `a3f8...c92d`
System concatenates: `a3f8...c92d` + `hunter2`
System hashes the combined value: bcrypt(`a3f8...c92d:hunter2`, cost=12)
System stores: salt + hash together in the database
:::
::col::
:::callout style=line
**Without Salts:** Two users with the same password → identical hashes → one crack reveals both accounts; rainbow table lookup takes milliseconds.

**With Salts:** Two users with the same password → completely different hashes → attacker must crack each account individually; no precomputed table applies.
:::
::::

:::table
| Scenario | Without Salt | With Salt |
|---|---|---|
| 1,000 users use "password123" | One hash crack reveals all 1,000 | Must crack 1,000 different hashes |
| Rainbow table attack | Applicable (precomputed table works) | Not applicable (unique salt per hash) |
| Attacker targets specific user | No advantage from other cracked hashes | Each account's hash is independent |
| Storage requirement | Hash only | Hash + salt (negligible overhead) |
:::

:::image src="images/06_salting_diagram.png" alt="Split diagram: left side shows two users with 'password123' producing the same MD5 hash (unsalted), with a single rainbow table lookup arrow cracking both simultaneously; right side shows same two users with different salts producing completely different hashes, requiring separate attack effort for each" caption="Password salting: the same plaintext password produces completely different hash values when unique salts are used, eliminating precomputed attacks and preventing batch cracking" width=full
:::

:::notes
Cryptographic salting is one of the simplest and most effective mitigations in the password storage threat model, yet its absence has been responsible for dramatically amplified damage in numerous major breaches. The concept is straightforward: before hashing a password, append (or prepend) a random value unique to that password. Because each password now has a different input to the hash function, even if the underlying passwords are identical, the resulting hash values are completely different.

The formal security property provided by salting is the prevention of precomputation attacks. A rainbow table or precomputed hash database is useful precisely because the attacker has computed hash(password) for millions of candidate passwords in advance, and can now look up any observed hash in O(1) time. When salts are used, the relevant computation is hash(salt + password), and since each salt is different, the attacker would need to build a separate precomputed table for every possible salt value, which is computationally equivalent to cracking each account individually. The precomputation advantage disappears entirely.

The secondary benefit of salting, preventing batch cracking, is also significant. Without salts, if the attacker cracks one hash (say, by finding that hash(password123) = abc123), they immediately know the passwords of every user in the database who also used "password123." With salts, cracking one user's password reveals nothing about any other user's password, even if they chose the same underlying value. This means the attacker's work scales linearly with the number of unique accounts they want to crack, rather than providing free mass cracking of all identical passwords.

Salt values should be generated using a cryptographically secure random number generator (CSPRNG), not a deterministic pseudorandom function based on predictable values like usernames or timestamps. The salt must be at least 16 bytes (128 bits) to ensure that different salts are effectively never repeated even across very large user databases. Most modern password hashing libraries (bcrypt, Argon2) handle salt generation automatically and embed the salt in the output hash string, eliminating the need for developers to manage salts separately.

A common mistake in early implementations was using a single application-wide "pepper", a secret value stored in application configuration, as a substitute for per-user salts. While peppers add a layer of protection against attackers who obtain the database but not the application configuration, they do not provide the same properties as salts: if the pepper is compromised (which it will be if the attacker has full system access), all accounts are equally vulnerable to batch cracking. Peppers are a useful additional control on top of salting, not a replacement for it.

Salting alone would have changed the LinkedIn outcome. Salted SHA-1, still a weak choice, would have forced attackers to crack each of the 117 million accounts individually instead of looking hashes up in bulk. Many accounts would still have fallen, but at far higher cost and over a longer window, giving time for forced resets and user notification. Even imperfect improvements to storage have real protective value.
:::

%%%

---
unit: Defense
code: POL
title: Have I Been Pwned & Breach Database Screening
---
:::callout style=soft
**Have I Been Pwned (HIBP)** is a free public service maintained by security researcher Troy Hunt that aggregates data from thousands of known data breaches. It allows individuals and organizations to check whether specific email addresses or passwords appear in known breach datasets, enabling proactive remediation before attackers exploit the exposure.
:::

::::columns
::col::
:::list heading="How Organizations Use HIBP" style=plain
- **At account creation:** Screen new passwords against the Pwned Passwords API, reject any password that appears in breach data
- **At password change:** Re-screen to prevent rotating to an already-compromised password
- **Periodic credential monitoring:** Check organizational email addresses against HIBP for breach alerts
- **Incident response:** Determine scope of exposure after a breach by querying known credential dumps
:::
::col::
:::callout style=line
**The k-Anonymity Privacy Model**

The HIBP Pwned Passwords API uses k-anonymity to screen passwords without transmitting the full password hash:
1. Client hashes the password (SHA-1)
2. Sends only the first **5 characters** of the hash to HIBP
3. HIBP returns all hashes starting with those 5 characters (~500 on average)
4. Client checks locally whether the full hash appears in the returned set
5. HIBP never sees the full hash; the password is never transmitted
:::
::::

:::table
| HIBP Service | Use Case | Who Should Use It |
|---|---|---|
| Email address lookup (web UI) | Personal breach awareness | Individual users |
| Domain monitoring | Organizational breach alerting | Security teams |
| Pwned Passwords API | Real-time breach screening at login | Developers, IT administrators |
| Notification service | Automatic alert on new breach inclusion | All users |
:::

:::image src="images/06_hibp_kanonymity.png" alt="Step-by-step diagram showing the k-anonymity password check: user's password hashed to SHA-1, first 5 hex characters sent to HIBP API, HIBP returns list of matching hash suffixes, client-side check determines if full hash is in the list, password never transmitted in full" caption="HIBP k-anonymity model: breach screening without privacy sacrifice, only a 5-character hash prefix is ever transmitted to the external service" width=full
:::

:::notes
Have I Been Pwned was created by Troy Hunt in December 2013 in response to the Adobe data breach, which exposed 153 million user accounts including passwords stored in an extremely weak format (3DES-ECB with a global encryption key). Hunt's initial goal was to create a simple reference service to help people check whether their email address appeared in known breaches. The service has since grown to encompass data from thousands of individual breaches and is now one of the most-used cybersecurity tools globally.

The Pwned Passwords feature, introduced in 2017, expanded HIBP's utility from breach notification to proactive password screening. The current Pwned Passwords dataset contains over 900 million real-world passwords sourced from known breaches, every password in this dataset was at some point used by a real person and subsequently exposed. NIST SP 800-63B Section 5.1.1.2 explicitly recommends checking passwords against this type of database: "When processing requests to establish and change memorized secrets, verifiers SHALL compare the prospective secrets against a list that contains values known to be commonly-used, expected, or compromised."

The k-anonymity privacy model that protects users during API queries is elegant and worth understanding in detail. Developed as a privacy concept by Latanya Sweeney, k-anonymity in this context means that any query to the API cannot uniquely identify the password being checked. By transmitting only the first five hexadecimal characters of the SHA-1 hash (covering 1/16^5 = 1/1,048,576 of the hash space), the query is ambiguous among a group of roughly 500 different hash values that share the same prefix. HIBP returns all of these, and the client checks locally whether the complete hash is present. This design means that HIBP's servers never see a hash that can be linked to a specific password, a meaningful privacy protection for a service that handles billions of sensitive queries.

Organizations integrating the Pwned Passwords API into their authentication systems should note that this check should occur at every password creation or change event, not just at account creation. An account password that was acceptable in 2020 may appear in a breach dataset by 2024, periodic re-screening of stored password hashes against the HIBP dataset (using the same k-anonymity query protocol) is a best practice for high-security environments, though this is more complex to implement and requires careful handling of the comparison process.

The breach notification functionality of HIBP (separate from the password API) allows organizations to register their email domains and receive automatic alerts when new breach data is added that includes email addresses from their domain. This provides an organizational early-warning system: when a supplier, partner, or cloud service provider suffers a breach that exposes employee email addresses, the organization can proactively reach out to affected employees and prompt credential changes before attackers exploit the exposure.

The Pwned Passwords API shows how often a password appears in breach data: "password123" appears hundreds of millions of times. Screening new passwords against such corpora, as NIST SP 800-63B requires, blocks the passwords attackers try first.
:::

%%%

---
unit: Defense
code: POL
title: Password Managers, The Practical Solution
---
:::callout style=soft
A **password manager** is software that generates, stores, and retrieves strong, unique passwords for every account. It solves the fundamental human limitation that makes password reuse inevitable: the impossibility of memorizing dozens of long, random, unique passwords without technological assistance.
:::

::::columns
::col::
:::list heading="What a Password Manager Provides" style=plain
- Generates cryptographically random passwords of any length and character set
- Stores credentials in an encrypted vault (AES-256 or ChaCha20) protected by a single master password
- Auto-fills credentials at the correct site (providing phishing resistance, no autofill on fake sites)
- Syncs across devices via encrypted cloud storage or local vault
- Alerts users when stored passwords appear in breach databases (HIBP integration)
- Enables completely unique passwords on every site without memorization
:::
::col::
:::table
| Category | Examples | Key Differentiator |
|---|---|---|
| Cloud-synced | 1Password, Bitwarden, Dashlane | Accessible everywhere; vault encrypted client-side |
| Local-only | KeePassXC, KeePass | No cloud dependency; maximum control |
| Browser-integrated | Chrome Password Manager, Safari Keychain | Convenient; tied to browser/platform ecosystem |
| Enterprise | CyberArk, Thycotic, 1Password Teams | PAM integration; admin control; audit logging |
:::
::::

:::image src="images/06_password_manager_architecture.png" alt="Architecture diagram showing user's master password unlocking an encrypted local vault, which syncs (encrypted) to cloud storage; browser extension intercepting login forms and auto-filling from vault; HIBP API integration checking stored passwords against breach data" caption="Password manager architecture: the master password unlocks a locally-encrypted vault; all cloud sync and data storage uses client-side encryption, the provider never sees plaintext credentials" width=full
:::

:::notes
The password manager represents the most pragmatic solution to the fundamental tension in password security: the human memorability constraint versus the security requirement for long, random, unique passwords. Without a password manager, users face an impossible choice, memorize dozens of strong unique passwords (cognitively infeasible), or reuse passwords across services (which credential stuffing exploits). With a password manager, a user needs to remember exactly one strong passphrase (the master password), and the manager handles generation and storage of all others.

NIST SP 800-63B explicitly endorses the use of password managers (referred to as "password vaults" in some NIST documents). The endorsement is pragmatic: a system that enables strong, unique passwords via tooling is preferable to a system that enforces complexity rules that produce predictable, reused passwords that users can actually remember. The security model of a password manager, strong encryption of the vault, secure key derivation from the master password, and isolation from potential phishing sites through domain-aware autofill, is well-understood and robustly implemented in leading products.

The encryption model of reputable cloud-synced password managers uses client-side encryption with zero-knowledge architecture: the vault is encrypted on the user's device before transmission, and the provider's servers store only ciphertext that they cannot decrypt. 1Password uses AES-256-GCM encryption with keys derived via PBKDF2 and an additional "Secret Key" stored locally. Bitwarden is open-source and has undergone independent security audits. LastPass, while once the market leader, suffered two significant breaches (2022) that resulted in encrypted vault data being stolen, analysis of the LastPass breach illustrated both the importance of the encryption model and the consequences of weak master passwords (which allowed attackers to brute-force some vaults offline).

Bitwarden is worth specific mention as the leading open-source option. Its source code is publicly available and has been independently audited by Cure53. It offers both cloud-hosted (Bitwarden's servers) and self-hosted (organization's own servers) deployment options, making it appropriate for both personal use and enterprise environments concerned about third-party data custody. The open-source model provides transparency and auditability that proprietary alternatives cannot match.

Enterprise password management extends beyond personal vaults to Privileged Access Management (PAM) systems like CyberArk and HashiCorp Vault, which manage credentials for service accounts, privileged administrator accounts, API keys, and database passwords, secrets that cannot be managed through a browser-based password manager. These systems typically implement just-in-time privilege elevation (granting access only when needed and only for the required duration), session recording (capturing the full video and command stream of privileged sessions for audit), and automatic credential rotation (changing service account passwords on a schedule without human involvement).

Browser-integrated password managers resist phishing. Autofill happens only when the current page's domain matches the stored domain, so a page at secure-paypal-login.com receives no PayPal credentials. This supplements MFA but does not replace it. Bitwarden is a free, open-source example.
:::

%%%

---
unit: MFA
code: MFA
title: Multi-Factor Authentication, The Real Fix
---
:::callout style=soft
**Multi-factor authentication (MFA)** enhances security by requiring two or more distinct authentication factors, typically categorized as knowledge, possession, and inherence, before access is granted.
:::

::::columns
::col::
:::list heading="Authentication Factor Categories" style=plain
- **Knowledge** (e.g., passwords, PINs)
- **Possession** (e.g., smartphones, hardware tokens)
- **Inherence** (e.g., fingerprints, facial recognition)
:::
::col::
:::table
| Factor Type   | Example                  | Security Strength     |
|---------------|--------------------------|------------------------|
| Knowledge     | Password, PIN            | Low (easily phished)   |
| Possession    | TOTP app, SMS, U2F key   | Medium to High         |
| Inherence     | Fingerprint, Voiceprint  | Medium (biometric drift)|
:::
::col::
:::pullquote
Even a perfectly stolen password is useless without the second factor.
:::
::::

:::image src="images/06_mfa_flow_diagram.png" alt="Step-by-step authentication flow diagram: user enters password (Step 1), system sends TOTP challenge to smartphone (Step 2), user enters 6-digit code (Step 3), access granted (Step 4); a red X branch shows 'stolen password alone rejected'" caption="MFA authentication flow: even a compromised password is insufficient without the second factor, the stolen credential becomes a dead end" width=full
:::

:::flow
User submits username + password (Factor 1: Knowledge)
System verifies password against salted hash, passes
System issues second-factor challenge based on enrolled method
User responds with TOTP code, hardware key press, or biometric
System validates second factor response
Access granted, session token issued with expiry
:::

:::notes
Multi-factor authentication (MFA) is a foundational security control that requires a user to present two or more independent authentication factors to verify their identity. These factors are typically drawn from three distinct categories: something you know (knowledge), something you have (possession), and something you are (inherence). This layered approach ensures that the compromise of one factor, such as a password leaked in a data breach or phished via social engineering, does not lead to a complete authentication failure.

The National Institute of Standards and Technology (NIST) provides authoritative guidance on digital identity and authentication in Special Publication 800-63B. NIST emphasizes that for authentication to be considered "multi-factor," the factors must be independent and drawn from different categories. For example, a password and a PIN, both knowledge factors, do not constitute MFA. Similarly, relying on two forms of inherence (e.g., fingerprint and facial recognition) on the same device does not meet NIST's independence requirement if both can be bypassed via the same endpoint compromise.

MFA significantly mitigates risks associated with well-known attack vectors such as credential stuffing (e.g., CVE-2021-40438), password spraying, and phishing. Even in cases where attackers successfully obtain valid credentials, MFA acts as a critical last line of defense. For instance, time-based one-time passwords (TOTP) or hardware tokens like YubiKey (implementing FIDO/U2F standards) introduce a possession factor that is extremely difficult for remote attackers to replicate.

In enterprise environments, protocols such as RADIUS, SAML, and OAuth 2.0 can be configured to enforce MFA through integration with identity providers like Microsoft Azure AD or Okta. These systems often support adaptive authentication, where risk-based triggers (e.g., login from a new device or location) dynamically require additional factors.

Ultimately, MFA is not just a best practice, it is a critical defense mechanism formally recognized by frameworks such as the NIST Cybersecurity Framework (CSF) and ISO/IEC 27001 as an essential control for identity and access management.

The real-world impact of MFA adoption is well-documented and dramatic. Microsoft reported in 2021 that MFA blocks approximately 99.9% of automated account compromise attacks. Google published similar findings from their own user base. The reason is statistical: credential-stuffing and password-spraying campaigns are fundamentally volume plays, attackers test millions of accounts hoping a small percentage succeed. MFA eliminates that success rate entirely for accounts that have it enabled, because possession of a valid password alone does not complete authentication.

It is important, however, to distinguish between MFA implementations of different strengths. Not all second factors are equal:

- **SMS OTP**: Widely available, broadly adopted, but vulnerable to SIM swapping and SS7 interception. NIST classifies this as a "restricted authenticator", acceptable for lower assurance levels, not recommended for high-value targets.
- **TOTP (Time-based One-Time Password)**: App-based codes (Google Authenticator, Authy, Microsoft Authenticator) are significantly stronger than SMS because they do not transit the cellular network. However, real-time phishing attacks can still steal valid TOTP codes if the user is tricked into entering them on a fake site.
- **FIDO2/WebAuthn hardware keys**: The strongest available consumer MFA. Challenge-response authentication is bound to the specific domain, making phishing-based interception cryptographically impossible, a fake site cannot complete the authentication exchange. This is the standard that Google moved its employees to in 2017, after which they reported zero successful phishing attacks on employee accounts.

The technical principle behind FIDO2's phishing resistance is worth understanding: rather than transmitting a reusable code, the hardware key signs a challenge that is cryptographically bound to the requesting origin URL. A phishing page at "rny-bank.com" receives a completely different challenge than "my-bank.com," and the signature from the key would fail verification at the real server, making interception useless.
:::

%%%

---
unit: MFA
code: MFA
title: MFA Methods Compared
---
::::columns
::col::
:::table
| Method | Security Level | Primary Trade-off |
|---|---|---|
| SMS-based OTP | Moderate | Susceptible to SIM swapping (CVE-2021-42758) and SS7 attacks |
| TOTP (Authenticator App) | High | Requires a secure, synchronized device |
| Hardware Security Key (FIDO2/WebAuthn) | Very High | Physical loss or device dependency |
| Biometric Factor | Strong (Contextual) | Irrevocable if compromised |
:::
::col::
:::callout
**NIST Digital Identity Guidelines (SP 800-63B)** emphasize that out-of-band verification using SMS is *not* recommended for high-security applications due to its inherent vulnerabilities. Meanwhile, **FIDO2-compliant** hardware tokens offer the strongest phishing-resistant authentication when properly implemented.
:::
::::

:::image src="images/06_mfa_comparison_spectrum.png" alt="Horizontal security spectrum from left (lower security) to right (higher security) with four MFA methods plotted along it: SMS OTP, TOTP app, push notification, hardware FIDO2 key; below each method, icons indicate vulnerabilities: SIM swap icon under SMS, device compromise icon under TOTP, phishing-proof badge on hardware key" caption="MFA security spectrum: hardware FIDO2 keys provide phishing-resistant authentication that other methods cannot match" width=full
:::

:::notes
Multi-Factor Authentication (MFA) significantly enhances security by requiring two or more independent authentication factors: something you know (e.g., password), something you have (e.g., token or phone), and something you are (e.g., biometric). However, not all MFA methods are equally secure, and each comes with distinct trade-offs in usability, cost, and resilience to attack.

SMS-based One-Time Passwords (OTPs) are widely used due to their accessibility but are vulnerable to **SIM swapping**, **SS7 protocol exploits**, and **interception via malware**. NIST SP 800-63B explicitly discourages SMS as a secure out-of-band method for sensitive systems.

Time-Based One-Time Passwords (TOTP), generated via apps like Google Authenticator or Authy, improve upon SMS by eliminating network-based interception risks. However, they depend on device integrity and time synchronization. If the device is compromised or the clock drifts, authentication may fail or be spoofed.

Hardware security keys implementing **FIDO2/WebAuthn** standards provide the highest level of protection by using public-key cryptography and offering resistance to phishing and replay attacks. These methods are endorsed by NIST and widely adopted in enterprise environments. Their main drawback is physical dependency, loss or damage renders the user locked out unless backup methods exist.

Biometrics (e.g., fingerprints, facial recognition) offer convenience and strong day-to-day security but introduce a critical flaw: **permanence**. Unlike passwords, biometric identifiers cannot be reset if stolen, raising long-term privacy and security concerns. ISO/IEC 30107 outlines frameworks for biometric presentation attack detection (PAD) to mitigate spoofing risks.

Ultimately, the selection of an MFA method should align with the system's risk profile, user context, and compliance requirements.

A nuanced understanding of the attack surface of each MFA method is essential for making informed deployment decisions. SIM swapping, the most commonly exploited attack against SMS MFA, involves social engineering a mobile carrier's customer service staff into transferring a victim's phone number to a SIM card controlled by the attacker. Once the number is ported, all SMS messages including OTP codes are delivered to the attacker. This attack has been used to compromise cryptocurrency exchanges, corporate VPNs, and even high-profile social media accounts (the 2020 Twitter Bitcoin scam involved SIM swapping as a component). Because the attack exploits the mobile carrier's identity verification process rather than any technical flaw, it cannot be fixed by the relying party, only avoided by not using SMS as an authentication channel.

TOTP is immune to SIM swapping but vulnerable to real-time phishing. A sophisticated phishing attack can proxy login requests to the real site in real time: as the victim types their username, password, and TOTP code on the fake site, the attacker's server immediately submits them to the real site. The TOTP window (typically 30 seconds) gives the attacker enough time to complete this relay. Tools like Evilginx2 and Modlishka automate exactly this attack. Against FIDO2, this attack fails: the hardware key's signature is cryptographically bound to the origin URL, so credentials captured from a phishing proxy are mathematically useless at the authentic server.

For most enterprise deployments, the pragmatic recommendation is: use TOTP app MFA for all staff, enforce FIDO2 hardware keys for privileged accounts (system administrators, finance staff, executives), and categorically disallow SMS for any account with access to sensitive data. This provides a strong security improvement over password-only authentication across the board while concentrating the highest-assurance control where it matters most.
:::

%%%

---
unit: MFA
code: MFA
title: FIDO2 & Passkeys, The Passwordless Future
---
:::callout style=soft
**FIDO2** (Fast IDentity Online 2) is an open standard developed by the FIDO Alliance that enables passwordless and phishing-resistant authentication using public-key cryptography. **Passkeys** are the consumer-facing implementation, private keys stored securely on devices, synced via cloud, replacing passwords entirely.
:::

::::columns
::col::
:::steps heading="FIDO2 Authentication Flow"
1. User initiates login; server sends a random challenge
2. Client device (hardware key or platform authenticator) signs the challenge using a private key bound to the specific site domain
3. Signed response is returned to the server
4. Server verifies the signature using the public key stored during registration
5. Authentication succeeds, no password, no code, no phishable secret
:::
::col::
:::callout style=line
**Why FIDO2 Is Phishing-Resistant**

The private key signs a challenge that cryptographically includes the **origin URL**. A phishing site at `secure-bank-login.com` requesting a sign for `mybank.com` will generate a different challenge, and the server at `mybank.com` will reject it because the origin doesn't match. The attacker captures a cryptographically worthless response.
:::
::::

:::table
| Feature | TOTP | FIDO2 / Passkeys |
|---|---|---|
| Phishing-resistant | No (real-time relay possible) | Yes (origin-bound signature) |
| Requires shared secret | Yes (TOTP seed) | No (asymmetric key pair) |
| Works offline | Yes | Yes (device holds private key) |
| Account recovery if device lost | TOTP backup codes | Synced passkeys or backup hardware key |
| NIST AAL Level | AAL2 | AAL2 / AAL3 (hardware bound) |
:::

:::image src="images/06_fido2_passkeys_flow.png" alt="Split diagram showing FIDO2 registration (left): device generates key pair, public key stored at server, private key stays on device, and FIDO2 authentication (right): server sends challenge, device signs with private key bound to origin URL, server verifies with stored public key; phishing site shown failing at verification step" caption="FIDO2 registration and authentication: no shared secret ever leaves the device, the private key signs challenges locally, making interception and replay attacks cryptographically impossible" width=full
:::

:::notes
FIDO2 represents the most significant advancement in authentication technology in decades, a fundamental redesign of the authentication model that eliminates the shared-secret paradigm that underlies every phishable authentication mechanism. FIDO2 combines two specifications: WebAuthn (Web Authentication, a W3C standard) and CTAP2 (Client to Authenticator Protocol, a FIDO Alliance specification), which together define how browsers, operating systems, and authenticator devices interact during authentication.

The core cryptographic model is asymmetric key cryptography applied to authentication. During registration, the authenticator (hardware key or platform authenticator like Windows Hello or Face ID) generates a public-private key pair unique to the combination of user and relying party (the website). The public key is sent to and stored by the server; the private key never leaves the authenticator. During authentication, the server sends a random challenge; the authenticator signs it using the private key and returns the signature. The server verifies the signature using the stored public key. Because the signing operation is performed locally on the device, the private key is never transmitted, it cannot be intercepted, stolen from server storage (there is no server-side private key), or replayed from a different origin.

Passkeys are the consumer-friendly evolution of FIDO2 credentials, announced jointly by Apple, Google, and Microsoft in 2022. The key innovation of passkeys over traditional FIDO2 credentials is synchronization: passkeys can be backed up to cloud keychain services (Apple iCloud Keychain, Google Password Manager, Microsoft account) and restored to new devices. This solves the primary usability complaint about hardware security keys (what happens if I lose it?) while preserving most of the security properties of FIDO2. Hardware-bound FIDO2 credentials (those that cannot be synced because the private key is physically locked in the hardware token) remain the strongest option and correspond to NIST AAL3; synced passkeys correspond to AAL2.

Major platforms have moved aggressively toward passkey adoption. Apple enabled passkeys in iOS 16 and macOS Ventura (2022). Google announced passkey support in Google accounts (2023). Microsoft has passkey support across Azure AD and consumer Microsoft accounts. GitHub, Shopify, PayPal, and hundreds of other services have deployed passkey support for users.

The FIDO Alliance's mission, "reducing the world's reliance on passwords", is achievable precisely because passkeys remove the need for a memorized secret entirely. From a security perspective, eliminating the shared secret eliminates the most prolific attack surface in authentication. From a usability perspective, a biometric prompt (Face ID, fingerprint) to authenticate to any service with a stored passkey is both faster and simpler than typing a password plus a TOTP code.

The remaining challenge is ecosystem coverage. As of 2025, not all services support FIDO2 or passkeys, and enterprise deployment requires identity provider support. Organizations using Microsoft Azure AD, Okta, or Ping Identity can enforce FIDO2 for managed devices. Consumer adoption will accelerate as browser and platform support matures.

YubiKey is the most widely deployed hardware FIDO2 authenticator. One key supports FIDO2/WebAuthn, FIDO U2F, TOTP/HOTP, PIV smart card and OpenPGP, and at about $50–60 it provides phishing-resistant authentication at AAL3 strength for every supported service.
:::

%%%

---
unit: MFA
code: MFA
title: Adaptive Authentication, Context-Aware Access Control
---
:::callout style=soft
**Adaptive authentication** (also called risk-based authentication) dynamically adjusts the authentication challenge based on contextual risk signals, granting lighter challenges for low-risk logins and requiring additional verification for high-risk or anomalous access attempts.
:::

::::columns
::col::
:::list heading="Risk Signals Used in Adaptive Auth" style=plain
- **Device recognition**, Known managed device vs. unrecognized personal device
- **IP reputation**, Corporate network IP vs. Tor exit node or anonymizing VPN
- **Geolocation**, User's home country vs. foreign country; "impossible travel" detection
- **Time of access**, Business hours vs. 3 AM access outside normal patterns
- **Behavior baseline**, Normal typing speed, navigation patterns vs. anomalous bot-like behavior
- **Threat intelligence**, IP address matches known bad actor lists
:::
::col::
:::callout style=line
**Impossible Travel Detection**

If a user successfully authenticates from New York at 9:00 AM and then authenticates from London at 10:30 AM, the elapsed time is 90 minutes, physically impossible given flight time. Adaptive authentication flags this as high-risk and requires step-up authentication or blocks access pending investigation.
:::
::::

:::flow
User initiates authentication
Risk engine evaluates contextual signals (device, location, behavior, IP)
Risk score calculated: Low / Medium / High
Low risk → standard authentication (password + saved device)
Medium risk → step-up: require TOTP code
High risk → step-up: require hardware key or block pending review
All authentication events logged with risk score for SIEM analysis
:::

:::image src="images/06_adaptive_authentication_flow.png" alt="Decision tree diagram: authentication request enters risk scoring engine; low risk branch leads to standard auth; medium risk triggers TOTP step-up; high risk triggers hardware key requirement or account freeze; all branches converge at session establishment with risk score recorded" caption="Adaptive authentication: risk signals determine the authentication challenge dynamically, ordinary logins stay frictionless while anomalous access triggers additional verification" width=full
:::

:::notes
Adaptive authentication represents the convergence of authentication security with machine learning and threat intelligence. Rather than applying a uniform authentication challenge to every login attempt, adaptive systems continuously evaluate the risk profile of each authentication event and adjust the challenge accordingly. The goal is to minimize friction for legitimate users while maximizing barriers for attackers, recognizing that a user logging in from their familiar laptop on the corporate network during business hours is fundamentally different from a login attempt from an unrecognized device in a foreign country at midnight.

The technical foundation of adaptive authentication is the risk engine, a system that aggregates signals from multiple sources, weights them according to historical patterns and threat intelligence, and produces a risk score that drives the authentication decision. Signals typically include device fingerprinting (browser user agent, installed fonts, screen resolution, hardware characteristics, combined, these produce a fairly unique device signature that can identify returning devices without cookies), network characteristics (IP address, ASN, hosting provider, Tor exit node status, VPN/proxy detection), geolocation (country, city, velocity between recent locations), and behavioral biometrics (typing speed, mouse movement patterns, keystroke dynamics).

The "impossible travel" detection example in the slide is a classic adaptive authentication signal. Azure Active Directory's Conditional Access policies include impossible travel detection natively, when two authentications for the same account originate from geographically disparate locations within a timeframe that makes physical travel impossible, the system automatically elevates risk. Okta, Ping Identity, and Duo Security all provide similar capabilities. False positives can occur (users who VPN from different countries, or frequent international travelers who land and immediately authenticate), but these are manageable through exception policies tied to specific users or device attributes.

Behavioral biometrics, the analysis of how a user interacts with input devices, represent the frontier of adaptive authentication. Companies like BioCatch analyze thousands of behavioral signals (typing rhythm, pressure, mouse acceleration curves, touchscreen gesture characteristics) to build behavioral models of individual users. Deviations from these models, which often occur when an account has been taken over and the attacker's behavior differs from the account owner's, can trigger authentication challenges mid-session, not just at login. This "continuous authentication" model is particularly valuable for high-value applications like banking and trading platforms.

The NIST Cybersecurity Framework (CSF) and NIST SP 800-63B support adaptive authentication as a mechanism for achieving higher assurance levels without uniformly applying the most restrictive authentication challenge to every user session. NIST's concept of "authentication assurance levels" (AAL1, AAL2, AAL3) can be dynamically applied based on risk: a user accessing low-sensitivity resources receives AAL1 treatment, while the same user accessing highly sensitive resources, or accessing from an anomalous context, is required to satisfy AAL2 or AAL3 requirements.

For enterprise deployment, adaptive authentication is typically implemented through identity providers (Microsoft Azure AD Conditional Access, Okta Adaptive MFA, Duo Beyond) that integrate with existing directory services and applications. These platforms allow security teams to define risk policies ("if location is outside the United States and device is unmanaged and time is outside business hours, require hardware key authentication") without requiring changes to individual applications.

Adaptive authentication must be tuned to the organization. Too aggressive, it issues constant step-up challenges that frustrate users and create pressure to weaken policy; too permissive, it misses real threats. The right setting depends on the organization's risk tolerance and user population.
:::

%%%

---
unit: MFA
code: MFA
title: Single Sign-On, One Authentication, Many Services
---
:::callout style=soft
**Single Sign-On (SSO)** allows users to authenticate once to a central identity provider and gain access to multiple applications without re-authenticating. SSO improves usability while centralizing authentication control, but it also creates a high-value single point of failure.
:::

::::columns
::col::
:::flow
User logs into Identity Provider (IdP), e.g., Okta, Azure AD, Google Workspace
IdP authenticates user (password + MFA)
User navigates to application (Service Provider, SP)
SP redirects to IdP to verify session
IdP confirms active session; issues assertion (SAML) or token (OAuth/OIDC)
SP grants access, user never re-authenticates
:::
::col::
:::list heading="SSO Protocols" style=plain
- **SAML 2.0**, XML-based; widely used in enterprise; browser redirect model
- **OAuth 2.0**, Authorization framework; "Sign in with Google/GitHub" consumer flows
- **OpenID Connect (OIDC)**, Identity layer on top of OAuth 2.0; issues ID tokens (JWT)
- **Kerberos**, Ticket-based; used internally in Windows Active Directory environments
:::
::::

:::table
| SSO Benefit | SSO Risk | Mitigation |
|---|---|---|
| Single strong authentication point | Single point of compromise | Strong MFA on the IdP is non-negotiable |
| Reduced password fatigue | Session token theft grants broad access | Short token expiry + continuous re-auth |
| Centralized access control | IdP outage blocks all services | HA IdP deployment; breakglass accounts |
| Consistent MFA enforcement | Misconfigured SP bypass | SP must validate assertions; no fallback auth |
:::

:::image src="images/06_sso_flow_diagram.png" alt="Sequence diagram showing user, identity provider (IdP), and service provider (SP) as three columns; authentication flow arrows: user authenticates to IdP, SP redirects to IdP, IdP issues SAML assertion, SP validates assertion and grants access; token lifetime indicator shows session expiry" caption="SSO authentication flow: one strong authentication event at the identity provider grants access across multiple service providers via cryptographically-signed assertions" width=full
:::

:::notes
Single Sign-On is one of the most impactful architectural decisions an organization can make for both security and usability. From a security perspective, SSO centralizes authentication so that MFA can be enforced once at the identity provider level and automatically applied to every integrated application, solving the adoption problem that occurs when each application independently manages MFA enrollment and enforcement. From a usability perspective, users experience fewer authentication prompts, reduced password fatigue, and streamlined access to dozens of tools from a single login.

The dominant enterprise SSO protocol is SAML 2.0 (Security Assertion Markup Language), a mature XML-based standard ratified in 2005. In a SAML flow, the identity provider (e.g., Azure AD, Okta, Ping Identity) is a trusted authority that issues signed XML assertions attesting that a particular user has authenticated. The service provider (e.g., Salesforce, Box, Workday) validates the signature on the assertion before granting access. The private key used to sign assertions is held only by the IdP, service providers only need the corresponding public key to verify signatures, and never handle credentials directly.

OAuth 2.0 and OpenID Connect (OIDC) represent the modern, API-centric evolution of SSO, designed for the web and mobile application patterns that emerged after SAML. OAuth 2.0 is fundamentally an authorization framework ("grant this application access to my Google Drive"), while OIDC adds an identity layer on top ("and tell this application who I am"). The "Sign in with Google" and "Sign in with GitHub" buttons ubiquitous in web applications implement the OIDC implicit or authorization code flow. JWT (JSON Web Tokens) carry identity claims in a compact, cryptographically-signed format.

The security risk of SSO is the centralization it creates: an attacker who compromises the identity provider gains access to every service integrated with it. This makes the IdP the highest-value attack target in the organization. Accordingly, IdP accounts, especially administrative accounts, should have the strongest available MFA (FIDO2 hardware keys), and IdP logs should be continuously monitored for suspicious authentication patterns. MITRE ATT&CK identifies SSO session token theft (T1550.001) as a specific technique used to pivot from a compromised endpoint to a broader set of services.

Token lifetime and session management are critical SSO security parameters. Long-lived session tokens increase usability (users don't need to re-authenticate frequently) but increase the damage window if a token is stolen. Organizations handling sensitive data should use short-lived access tokens (15–60 minutes) combined with longer-lived refresh tokens that are invalidated immediately upon reported compromise. NIST SP 800-63B addresses session management in Section 7, recommending reauthentication after extended inactivity periods and mandating reauthentication before privilege elevation.

The "breakglass" account pattern deserves mention: SSO creates a dependency where a functional IdP is required for all access. Organizations should maintain a small number of local administrator accounts on critical systems that are not tied to SSO, these "breakglass" accounts allow recovery if the IdP becomes unavailable (due to configuration error, outage, or compromise). These accounts must be monitored extremely carefully (any use should immediately generate an alert) and stored securely (in a physical safe, with the password in a sealed envelope).

A SAML login involves an identity provider (IdP) issuing a signed assertion to a service provider (SP), with trust established by exchanging metadata and signing certificates. Understanding the flow is what allows misconfigurations to be found: SPs that fail to validate signatures correctly, parsing flaws such as CVE-2017-11427 (XML comment handling), and Golden SAML attacks, in which assertions are forged with a stolen IdP signing key.
:::

%%%

---
unit: MFA
code: MFA
title: Biometric Authentication Deep Dive
---
:::callout style=soft
Biometric authentication uses unique physiological or behavioral characteristics, fingerprints, facial geometry, iris patterns, voice, to verify identity. Biometrics offer compelling usability advantages but introduce distinct security and privacy challenges fundamentally different from knowledge and possession factors.
:::

::::columns
::col::
:::table
| Biometric Type | FAR* | FRR* | Vulnerability |
|---|---|---|---|
| Fingerprint | 0.001% | 0.1% | Silicone replicas, latent prints |
| Facial recognition | 0.001% | 0.1% | Photos, 3D printed masks |
| Iris scan | 0.0001% | 0.5% | High-res photographs |
| Voice recognition | 0.01% | 1% | AI-generated deepfake audio |
| Behavioral (typing) | 0.1% | 5% | Difficult to spoof; lower accuracy |
:::
*FAR = False Accept Rate; FRR = False Reject Rate
::col::
:::callout style=line
**The Irrevocability Problem**

Passwords can be reset when compromised. Biometric identifiers cannot. If a fingerprint template is stolen from a database, the victim cannot issue themselves a new fingerprint. This makes the secure storage of biometric templates, and the preference for on-device matching that never transmits raw biometrics, critical design requirements.
:::
::::

:::list heading="Security Design Principles for Biometrics" style=plain
- Match on device (MoD): biometric matching occurs on the device; only a cryptographic confirmation is sent to the server, raw templates never leave the device
- Liveness detection (anti-spoofing): PAD (Presentation Attack Detection) per ISO/IEC 30107 distinguishes live subjects from replicas
- Biometrics as unlock, not authentication: in FIDO2/passkey flows, biometrics unlock the private key on-device; the actual authentication is the FIDO2 cryptographic challenge
- Template protection: if templates must be stored centrally, use cancelable biometrics (mathematically transform templates so they can be "cancelled" and reissued)
:::

:::image src="images/06_biometric_authentication_architecture.png" alt="Architecture diagram showing biometric sensor capturing fingerprint, liveness detection layer rejecting spoofed samples, on-device matching comparing against locally-stored template, and cryptographic confirmation sent to server, raw biometric data never transmitted; FIDO2 integration shown" caption="Secure biometric architecture: liveness detection filters spoofing attacks, on-device matching prevents template exposure, and FIDO2 integration means the actual authentication is cryptographic, not biometric data transmission" width=full
:::

:::notes
Biometric authentication has become ubiquitous in consumer devices, Apple's Touch ID (2013) and Face ID (2017) demonstrated that high-quality biometric authentication could be both secure and genuinely convenient for everyday use, accelerating adoption across the industry. Understanding the security properties of biometrics, both genuine strengths and genuine limitations, is essential for security professionals designing authentication systems.

The False Accept Rate (FAR) and False Reject Rate (FRR) are the fundamental accuracy metrics for biometric systems, and they exist in an inherent trade-off. A system with very strict matching criteria (low FAR, rejecting all but near-perfect biometric matches) will incorrectly reject legitimate users more often (high FRR). A system with loose matching criteria (low FRR, accepting most attempts that are in the right neighborhood) will incorrectly accept imposters more often (high FAR). The operating point on this curve is a policy decision that reflects the security-usability trade-off. Apple Face ID, for example, has a published FAR of approximately 1-in-1,000,000, chosen to balance strong security with acceptable usability.

The attack surface against biometric systems has evolved significantly with advances in materials science, photography, and AI. Fingerprint spoofing using gelatin or silicone replicas cast from latent fingerprints (left on surfaces) has been demonstrated against numerous commercial fingerprint sensors. Facial recognition has been defeated with high-resolution photographs on some systems and 3D-printed masks on others. Voice authentication systems have been defeated using AI-generated deepfake audio that mimics the target's voice characteristics with high accuracy, a threat that will only grow as voice synthesis technology improves (CVE-2023-42842 and similar advisories document specific voice spoofing vulnerabilities).

ISO/IEC 30107 (Biometric Presentation Attack Detection) defines the framework for evaluating and certifying anti-spoofing capabilities in biometric systems. APCER (Attack Presentation Classification Error Rate) and BPCER (Bona Fide Presentation Classification Error Rate) are the PAD-specific metrics. Apple Face ID uses an IR flood illuminator and dot projector to build a 3D depth map, explicitly designed to defeat 2D photograph attacks. This hardware-level liveness detection is why Face ID has a significantly better spoofing resistance than many software-only facial recognition systems.

The "match on device" architecture, used by Apple's Secure Enclave and Android's Trusted Execution Environment (TEE), is the gold standard for biometric privacy and security. In this model, the biometric template is enrolled and stored in a hardware-isolated secure element. Matching occurs entirely within that secure element, the raw sensor data and the stored template never enter the main processor or operating system, and are never transmitted over any network. The application receives only a boolean "match succeeded" / "match failed" cryptographic attestation. This architecture means that even if the main operating system is fully compromised by malware, the attacker cannot extract the biometric template.

The FIDO2 integration of biometrics is architecturally important and often misunderstood. In a FIDO2/passkey flow where biometrics are used, the biometric does not authenticate the user to the server. Instead, the biometric authenticates the user to the device, which then uses the FIDO2 private key to complete the actual cryptographic authentication. The server never receives any biometric data, it only receives a FIDO2 signature that could theoretically have been produced by any authorized method (PIN, biometric, or other) that unlocks the platform authenticator. This design means that biometric compromise at the device level does not compromise the authentication credential, the attacker would still need to compromise the FIDO2 private key, which is hardware-bound in the secure element.

Biometric data carries legal obligations. Illinois's Biometric Information Privacy Act (BIPA) restricts the collection, storage and commercial use of biometrics and has produced substantial litigation, and GDPR Article 9 classifies biometric data as special-category data requiring explicit consent and heightened protection.
:::

%%%

---
unit: Defense
code: FRM
title: NIST SP 800-63B, A Framework Deep Dive
---
:::callout style=soft
**NIST Special Publication 800-63B** (*Digital Identity Guidelines: Authentication and Lifecycle Management*) is the authoritative US federal standard for digital authentication. Published in 2017 and updated in 2020, it defines three Authenticator Assurance Levels (AAL) with specific control requirements for each.
:::

:::table
| Assurance Level | Authentication Requirement | Example Use Cases | Binding |
|---|---|---|---|
| **AAL1** | Single factor (including software-based) | Low-risk services, public information portals | Self-assertion; low fraud risk |
| **AAL2** | Multi-factor; one factor must be a cryptographic device or OTP | Healthcare portals, financial services | Identity-proofed; moderate fraud risk |
| **AAL3** | Hardware-bound cryptographic key (phishing-resistant); verifier impersonation resistance required | Federal systems, high-value targets | In-person proofing; high fraud risk |
:::

::::columns
::col::
:::list heading="Key NIST SP 800-63B Policy Changes (vs. Prior Guidance)" style=plain
- Eliminated mandatory periodic password rotation (unless compromise suspected)
- Removed requirements for arbitrary complexity rules (uppercase/number/symbol)
- Mandated breach database screening for new/changed passwords
- Classified SMS OTP as "restricted", not recommended for AAL2+
- Endorsed password managers and passphrases
- Required support for passwords up to 64 characters minimum
:::
::col::
:::callout style=line
**Federal Mandate & Industry Adoption**

NIST SP 800-63B is mandatory for US federal agencies and widely adopted as best practice by commercial organizations. CISA, FedRAMP, and many state governments reference it directly. Industry frameworks including PCI-DSS v4, HIPAA guidance, and ISO/IEC 27001 align with its core recommendations.
:::
::::

:::image src="images/06_nist_800_63b_aal_levels.png" alt="Three-column diagram labeled AAL1, AAL2, AAL3; each column shows a shield icon with increasing complexity, lists required authenticator types, required verification ceremonies, and example use cases; AAL3 column has a hardware key icon and 'phishing-resistant' badge" caption="NIST SP 800-63B Authenticator Assurance Levels: AAL1 permits single factor for low-risk systems; AAL2 requires multi-factor; AAL3 requires hardware-bound cryptographic authenticators and phishing resistance" width=full
:::

:::notes
NIST Special Publication 800-63B is not merely a government compliance document, it represents the most rigorous, evidence-based synthesis of digital identity security knowledge available in any public standard. Its development involved input from academic researchers, industry practitioners, and government agencies, and its departures from prior conventional wisdom (particularly on password rotation and complexity) were backed by empirical research rather than intuition.

The three Authenticator Assurance Levels (AALs) provide a framework for mapping authentication requirements to risk level. AAL1 is intentionally permissive, it permits single-factor authentication for genuinely low-risk scenarios where the consequences of a compromised account are minimal. AAL2 is appropriate for the majority of business applications and requires that at least one authentication factor be a hardware-based cryptographic device (like a TOTP app or smart card) rather than a knowledge factor alone. AAL3 is reserved for the highest-risk scenarios, typically federal systems handling classified or highly sensitive information, and requires hardware-bound cryptographic authentication that is verifier impersonation resistant (a formal term meaning the authenticator cannot be spoofed even by a sophisticated active attacker performing a real-time phishing attack).

The classification of SMS OTP as a "restricted authenticator" at AAL2 deserves careful explanation. NIST did not categorically prohibit SMS MFA, rather, it identified specific conditions under which its use is acceptable and required additional controls when SMS is used. Organizations using SMS OTP are required to have a risk assessment documenting why SMS was selected, to have a plan to migrate to a more secure authenticator, and to provide alternative authentication options for users who cannot receive SMS (due to phone number porting risks or lack of cellular service). In practice, "restricted" status effectively discourages SMS adoption for anything sensitive and drives organizations toward stronger second factors.

The lifecycle management provisions of SP 800-63B (Section 6) are often overlooked but operationally important. They cover authenticator binding (how a new authenticator is issued to a user), authenticator recovery (what happens when an authenticator is lost), and reauthentication requirements (how often sessions must be refreshed). The reauthentication interval recommendations, every 12 hours for AAL2 in sessions involving sensitive operations, or after 30 minutes of inactivity, are important parameters for session management policy design.

NIST SP 800-63-4, the successor to SP 800-63B, was in public review as of 2024 and is expected to further strengthen passkey and phishing-resistant authenticator requirements, potentially reclassifying TOTP as "restricted" similar to SMS in high-assurance contexts. Students and practitioners should monitor NIST's website for updates to this foundational standard.

The main requirements of NIST SP 800-63B to retain are: the three Authenticator Assurance Levels and their requirements, the restricted status of SMS one-time codes, and the policy changes from earlier practice: no mandatory periodic rotation, no composition rules, and mandatory screening against breached passwords.
:::

%%%

---
unit: Defense
code: FAQ
title: Common Misconceptions About Password Security
---
:::callout style=soft
Password security is surrounded by persistent myths, many of which were once officially recommended. Understanding why these beliefs are wrong is as important as knowing the correct guidance.
:::

:::table
| Misconception | Why It's Wrong | What's Actually True |
|---|---|---|
| "Changing passwords every 90 days improves security" | Forces predictable incremental patterns (Password1→Password2); research shows net security decrease | Rotate only when compromise is confirmed or suspected (NIST SP 800-63B) |
| "Complex passwords (P@ssw0rd) are strong" | Complexity rules are in every attacker's ruleset; patterns are predictable | Length and randomness matter more; "correct horse battery staple" > "P@ssw0rd1!" |
| "My password is safe because I haven't been breached" | Your credentials may be in breach dumps without you knowing | Check haveibeenpwned.com; assume exposure |
| "Security questions add meaningful protection" | Security question answers are publicly discoverable or guessable | Questions are knowledge factors, they don't constitute MFA |
| "Biometrics are more secure than passwords" | Biometrics can be spoofed; they cannot be reset; they're a convenience factor | Best used as a device unlock layer for FIDO2, not as standalone authentication |
| "MFA is too inconvenient for regular use" | One extra tap prevents 99.9% of automated attacks (Microsoft, 2021) | Inconvenience is real but negligible vs. risk; TOTP apps take 3 seconds |
| "A long random password is enough without MFA" | Passwords can be phished, keylogged, or obtained via breach, regardless of strength | Password strength and MFA are complementary, not substitutes |
:::

:::image src="images/06_password_misconceptions.png" alt="Seven myth cards arranged in a grid, each showing a myth statement crossed out in red and the corrected truth below in green; icons indicate source of confusion (legacy policy, intuition, media myth)" caption="Password security myths busted: most misconceptions stem from outdated policy guidance, intuitive-but-wrong reasoning, or oversimplification of security trade-offs" width=full
:::

:::notes
Misconceptions in security are not merely harmless misunderstandings, they drive security decisions that leave systems vulnerable. The myths catalogued on this slide are particularly persistent because many of them were once official guidance. The mandatory 90-day rotation rule, for example, was recommended by organizations including NIST itself in earlier guidance documents (NIST SP 800-118 draft, 2009) before being reversed in SP 800-63B (2017) based on accumulated empirical evidence. Security practitioners who were trained on the old guidance carry those mental models forward unless they actively update their knowledge base.

The complexity myth is perhaps the most consequential. For years, organizations enforced rules requiring uppercase letters, lowercase letters, numbers, and special characters, often with minimum length requirements as short as 8 characters. The theory was that requiring diverse character types would increase entropy. In practice, users responded to complexity requirements by applying predictable transformations to memorable base words: capitalizing the first letter, replacing 'a' with '@', replacing 'o' with '0', and appending a required number at the end. The resulting passwords are immediately testable with Hashcat rules, "P@ssw0rd1!" appears within seconds of running any remotely current dictionary attack with a basic rule set.

The security question misconception is particularly insidious because security questions feel like a second factor, they're a separate step in the authentication flow. But they are knowledge factors, just like passwords, and they suffer from the same fundamental vulnerability: the answers are often publicly discoverable (mother's maiden name, hometown, high school, all available on social media or data broker sites), predictable within a small set of guesses, or the same across multiple services. Using security questions as an MFA factor explicitly violates NIST SP 800-63B's requirement that factors be from different categories. Organizations should eliminate security questions entirely and replace them with proper MFA and secure account recovery flows.

The biometric misconception requires nuance: biometrics are not less secure than passwords in all contexts, but they are not categorically more secure either. Their appropriate role is as a convenient unlock mechanism for a cryptographic credential (as in FIDO2/passkey architectures), not as a standalone authentication factor for high-assurance systems. The irrevocability issue, you cannot be issued a new fingerprint, means that biometric data requires extraordinary protection, and any system that stores raw biometric templates faces elevated long-term risk.

The MFA convenience objection is worth addressing directly because it is the most common reason organizations resist broad MFA deployment. The "inconvenience" of TOTP is approximately 3–5 seconds per login, opening an authenticator app, reading a 6-digit code, and entering it. In a typical workday involving perhaps 10–20 login events, this represents roughly 1–2 minutes of added friction. Against a backdrop of breaches that cost organizations an average of $4.45 million (IBM Cost of a Data Breach Report, 2023), the ROI calculation is not close. The framing that sometimes helps: "We are asking employees to spend 2 minutes per day to prevent a $4 million incident."

Many common password policies are now recognized as counterproductive under NIST SP 800-63B: 90-day rotation, eight-character minimums, mandatory special characters, and security questions used as a second factor.
:::

%%%

---
unit: Defense
code: CMP
title: Comparison, Password-Only vs. MFA vs. Passwordless
---
:::callout style=soft
The authentication landscape offers a spectrum of approaches, from traditional password-only to fully passwordless FIDO2. Understanding the security properties, usability trade-offs, and deployment complexity of each helps organizations make informed decisions about their authentication architecture.
:::

:::table
| Dimension | Password Only | Password + MFA (TOTP) | Password + MFA (FIDO2) | Passwordless (Passkey) |
|---|---|---|---|---|
| Phishing resistance | None | Partial (TOTP interceptable) | Full (origin-bound) | Full (origin-bound) |
| Credential stuffing resistance | Low | High (2nd factor blocks) | High | High (no reusable secret) |
| Brute force resistance | Length-dependent | High | High | High (no password to brute force) |
| User friction | Low (single step) | Moderate (2 steps) | Low (tap hardware key) | Very low (biometric/PIN) |
| Deployment complexity | Low | Moderate | Moderate-High | Moderate (growing ecosystem) |
| Recovery if factor lost | Password reset | Backup codes | Backup hardware key | Synced passkey or recovery code |
| NIST AAL level achievable | AAL1 | AAL2 | AAL2–AAL3 | AAL2 (synced) / AAL3 (hardware-bound) |
| Recommended for | Legacy systems only | All organizations now | Privileged accounts | Consumer + enterprise (emerging) |
:::

:::image src="images/06_auth_approach_comparison.png" alt="Four-column comparison chart with password-only, TOTP MFA, FIDO2 MFA, and passwordless passkey as columns; rows show phishing resistance, stuffing resistance, user friction, deployment complexity, and NIST AAL; color coding from red (poor) through yellow (moderate) to green (excellent) in each cell" caption="Authentication approach comparison: FIDO2 and passkeys offer the best security-usability combination, the goal is to move all organizations from the left columns toward the right" width=full
:::

:::notes
The comparison table on this slide serves as a strategic planning tool for security architects choosing authentication approaches for their organizations. The ideal authentication system is simultaneously as secure as possible (eliminating the widest range of attack techniques) and as usable as possible (minimizing friction to encourage adoption and prevent workarounds). The historical challenge has been that these goals often appeared to be in conflict, stronger security required more steps and created more friction. FIDO2 and passkeys represent a paradigm shift because they simultaneously improve both dimensions.

Password-only authentication should now be considered a legacy approach acceptable only for genuinely low-risk systems where the cost of MFA deployment would exceed the risk value. NIST AAL1 explicitly permits single-factor authentication for such scenarios, acknowledging that the cost-benefit calculation does not always favor MFA deployment for every system. However, the definition of "low-risk" has narrowed considerably: any system that touches personal data, financial information, or organizational internal resources should be considered above AAL1 risk.

The TOTP MFA column represents the current practical baseline that all organizations should achieve. TOTP apps (Google Authenticator, Authy, Microsoft Authenticator) are free, widely understood, and supported by virtually every service with MFA capabilities. The moderate user friction (the extra step of checking the TOTP app) is a real cost, but one that most users find acceptable once they understand the security benefit. Microsoft's measurement that TOTP MFA blocks 99.9% of automated attacks makes this the highest-ROI security control available to most organizations per unit of implementation cost.

FIDO2 hardware key MFA is the appropriate control for privileged accounts, system administrators, finance staff, executives, developers with production access. The "tap a hardware key" user experience is arguably lower friction than TOTP (no need to open a separate app), and the phishing resistance eliminates the entire class of real-time TOTP relay attacks that increasingly sophisticated threat actors use. The deployment complexity is higher (purchasing and distributing hardware keys, enrolling them, managing spares) but justified by the risk profile of privileged accounts.

Passwordless passkeys represent the emerging direction for both consumer and enterprise authentication. The "login with passkey" experience, a biometric prompt on a device or a hardware key tap, with no password entry required, consistently tests as both faster and more satisfying than password-based login in user research. The growing platform support (Apple, Google, Microsoft all supporting passkeys natively) and service adoption (major websites and apps adding passkey support in 2023–2025) means that the deployment complexity is decreasing rapidly. Security practitioners should expect passkeys to become the default authentication mechanism within the next few years for most consumer-facing services.

The recovery dimension highlights a critical operational consideration often overlooked in authentication design. Every strong authentication mechanism creates a recovery problem: what happens when the second factor is unavailable? MFA deployment without a well-designed recovery process leads either to permanent lockouts (if recovery is too strict) or to a weak backdoor that attackers target (if recovery is too permissive). Backup codes for TOTP, redundant hardware keys, and cloud-synced passkeys each represent different points on the recovery complexity-security trade-off. Security teams must explicitly design the recovery flow before deploying any MFA mechanism, not as an afterthought.

Authentication maturity varies widely in practice: most banking applications now offer or require TOTP or push MFA, while many small-business and legacy applications remain password-only. The gaps cluster in exactly those legacy systems.
:::

%%%

---
unit: Summary
code: SUM
title: Authentication as the Last Line of Defense
---

::::columns
::col::
:::callout style=soft
Authentication serves as the final barrier between an attacker and a compromised account. Even if earlier defenses such as phishing awareness or network segmentation are bypassed, strong authentication mechanisms can prevent unauthorized access.
:::

::col::
:::list heading="Key Concepts" style=chips
- Authentication Factors
- Brute Force Resistance
- Dictionary Attack Mitigation
- Password Policy Enforcement
- Multi-Factor Authentication (MFA)
:::
::::

:::table
| Threat Type         | Mitigation Strategy       | Standard/Reference              |
|---------------------|----------------------------|----------------------------------|
| Brute Force         | Account Lockout, Rate Limiting | NIST SP 800-63B                 |
| Dictionary Attacks  | Complexity Requirements    | ISO/IEC 27001 Annex A.9.4.3     |
| Credential Reuse    | Unique Password Policies   | RFC 6974 (Password Auth Guidelines) |
| Stolen Credentials  | MFA Enforcement            | MITRE ATT&CK T1078, T1110       |
:::

:::steps heading="Defense-in-Depth with Authentication"
1. **Enforce Strong Password Policies**  
   - Minimum length (NIST recommends at least 8 characters; longer is better)  
   - Prohibit commonly used or breached passwords (e.g., "password123")  
   - Avoid periodic mandatory resets unless there's evidence of compromise  

2. **Implement Multi-Factor Authentication (MFA)**  
   - Use at least two authentication factors: something you know, have, or are  
   - Prefer hardware tokens or authenticator apps over SMS (NIST SP 800-63B discourages SMS for MFA)  

3. **Monitor for Compromised Credentials**  
   - Integrate with threat intelligence feeds (e.g., Have I Been Pwned API)  
   - Detect and respond to credential stuffing attempts (MITRE ATT&CK T1110.004)
:::

:::image src="images/06_authentication_defense_summary.png" alt="Layered defense-in-depth diagram for authentication: outermost ring shows password policy, next ring shows MFA, innermost ring shows monitoring and breach detection; arrows show how each layer stops different attack types" caption="Authentication defense in depth: password policies stop weak credentials, MFA stops stolen credentials, monitoring catches the attacks that slip through" width=full
:::

:::notes
Authentication represents the final control point in securing user accounts. Even when upstream defenses, such as email filtering, endpoint protection, or user training, fail, robust authentication can still prevent unauthorized access. This is especially critical in environments where initial compromise vectors like phishing or social engineering succeed in capturing user credentials.

A brute force attack systematically attempts every possible combination of characters until the correct password is found. While computationally expensive, it becomes feasible against short or predictable passwords. To counter this, systems implement account lockout policies or rate-limiting mechanisms, as recommended by NIST SP 800-63B, which emphasizes the importance of throttling repeated authentication attempts.

Dictionary attacks, on the other hand, exploit commonly used passwords or leaked credentials from previous breaches. These attacks are more efficient than brute force because they prioritize high-probability guesses. Effective mitigation includes enforcing password complexity, banning known weak passwords, and implementing real-time checks against breach databases.

Password policies form the foundational layer of defense. They should mandate sufficient entropy, typically through minimum length requirements, and discourage re-use of previously compromised passwords. NIST SP 800-63B discourages mandatory periodic password changes unless there is evidence of compromise, as frequent resets often lead to predictable patterns or weaker passwords.

However, even strong passwords can be stolen through phishing, keylogging, or network interception. This is where Multi-Factor Authentication (MFA) becomes essential. MFA requires users to present two or more distinct authentication factors: something they know (password), something they have (token or smartphone), or something they are (biometric). By adding this second layer, MFA ensures that a stolen password alone is insufficient for access.

Not all MFA methods are equally secure. For example, SMS-based codes are vulnerable to SIM swapping and should be avoided in high-security contexts, as outlined in NIST guidelines. Instead, organizations should favor app-based authenticators or hardware tokens.

In the context of MITRE ATT&CK, techniques such as Valid Accounts (T1078) and Brute Force (T1110) highlight how adversaries exploit weak authentication. Implementing layered authentication controls directly counters these tactics, reducing the likelihood of successful account takeover.

As we conclude this unit, remember that authentication is not a silver bullet, it must be part of a broader defense-in-depth strategy. Next, we will shift our focus to network-level security, particularly how wireless networks are exploited and defended in public and enterprise environments.

The summary slide serves a double purpose: consolidating the technical content of this lecture and situating it within the broader course arc. Authentication is not a solved problem, it is an active area of research and standards development. The FIDO Alliance continues to evolve the WebAuthn and Passkey specifications; NIST is developing SP 800-63-4 which further refines identity assurance guidance; and the threat landscape continues to evolve with increasingly sophisticated credential-harvesting tools.

Looking ahead in this course, the concepts introduced here, particularly MFA and the notion that identity verification is a layered problem, will resurface repeatedly. Wireless security (next class) intersects with authentication because attackers who conduct MITM attacks on Wi-Fi are often ultimately trying to capture credentials. AI-enabled attacks (classes 8 and 9) include AI-generated phishing specifically designed to steal credentials and MFA codes. Physical security (class 10) is partly about preventing unauthorized physical access that could allow hardware-based credential extraction.

Authentication is not a self-contained topic, it is the thread that connects every layer of the security stack, from the physical device to the network channel to the application logic. Students who deeply understand the failure modes of authentication will find themselves better equipped to analyze security problems across every domain they encounter in practice.
:::
