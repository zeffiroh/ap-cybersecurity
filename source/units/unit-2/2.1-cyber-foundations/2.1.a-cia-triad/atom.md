# 2.1.a, CIA triad: confidentiality, integrity, availability

> **Unit 2 · 2.1 Cyber Foundations**
> **AP Learning Objective(s):** 2.1.A
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Name and define each pillar of the CIA triad, give a concrete example and a countermeasure for each, and explain how the three pillars can come into conflict.

## Lesson
Every security decision in cybersecurity traces back to three questions: Is this information being kept from those who should not see it? Has this information been changed without authorization? Can the people and systems that need this information actually reach it? Those three questions define the **CIA triad**, **Confidentiality**, **Integrity**, and **Availability**, the foundational framework that organizations use to categorize security goals, evaluate threats, and justify controls. NIST (the National Institute of Standards and Technology) formalizes this triad in its core security publications, and the AP Cybersecurity course treats it as the entry point for all risk analysis.

**Confidentiality** is the property that information is accessible only to those authorized to have it. The classic threat to confidentiality is unauthorized disclosure: a competitor reading your trade secrets, an attacker intercepting an unencrypted login, or a misconfigured cloud bucket exposing customer records. Controls that protect confidentiality include **encryption** (transforming data so it is unreadable without a key), **access control** (authenticating identity and limiting what each account can reach), and **classification policies** (labeling data by sensitivity so handling rules apply automatically). A hospital that encrypts patient records in transit and at rest and limits access to clinical staff is defending confidentiality. When confidentiality fails, data has been exposed, sometimes without anyone noticing for months.

**Integrity** is the property that information and systems are accurate and have not been altered without authorization. The threat is modification: an attacker quietly changes a financial record, a file is corrupted in transit, or a software update is replaced with malware. The key controls are **cryptographic hashing** and **digital signatures**. A hash function produces a fixed-length fingerprint of any data; if even one bit changes, the hash changes entirely. When you download software, the publisher often provides a hash alongside the installer, you compute the hash on what you received and compare; a mismatch means tampering or corruption. **Audit logs** and **version control** also serve integrity: they create an immutable record of who changed what and when, so tampering can be detected and reversed. Integrity failures are insidious because the system keeps running, it just produces wrong answers.

**Availability** is the property that systems and data are accessible when needed by authorized users. The threat is denial: a ransomware attack encrypts files and refuses access until payment, a distributed denial-of-service (DDoS) attack floods a web server with traffic until it crashes, or a hardware failure takes a database offline. Controls include **redundancy** (backup servers, mirrored data centers), **DDoS mitigation** (traffic filtering, rate limiting, content-delivery networks), **regular backups**, and **disaster-recovery plans** that define how quickly systems must be restored (Recovery Time Objective) and how much data loss is acceptable (Recovery Point Objective). An e-commerce site that goes down for a day loses revenue, trust, and potentially customers permanently, availability is as real a security goal as keeping secrets.

The three pillars are connected, but they can pull in opposite directions. Consider encryption: encrypting everything strongly protects confidentiality, but encryption adds computational overhead and key-management complexity. If the key is lost or the decryption system fails, the data is inaccessible, an availability problem you created while solving a confidentiality problem. Similarly, strict access control (confidentiality) can mean that a doctor in an emergency cannot quickly access a patient's drug allergies, a life-threatening availability failure. Security architects are constantly trading off among the three pillars, and the AP course's Analyze Risk skill is precisely the practice of reasoning through those tradeoffs for a given context.

A useful mental move: when you read about any security incident, ask which pillar(s) were violated. The 2017 WannaCry ransomware worm primarily hit **availability**, it encrypted files and demanded payment, locking hospitals out of patient records. A phishing campaign that harvests passwords targets **confidentiality**. An attacker who edits a database entry to redirect payments hits **integrity**. Many real incidents violate multiple pillars: an attacker might breach confidentiality (steal credentials), use them to compromise integrity (modify records), and then cover their tracks by crashing logging systems (availability). The triad gives you a structured vocabulary to analyze any incident rather than treating it as a single undifferentiated "hack."

Security goals, authentication, authorization, non-repudiation, privacy, resilience, all derive from or serve the CIA triad. Recognizing which pillar a goal serves is the first step in evaluating whether a proposed control is addressing the right problem. The coding problem in `problem/` puts this into practice: given a description of an incident, your code should identify which CIA pillar(s) were violated.

## Key terms
- **CIA triad**, the three foundational security properties: confidentiality, integrity, and availability.
- **Confidentiality**, the property that information is accessible only to authorized parties.
- **Integrity**, the property that information and systems have not been altered without authorization.
- **Availability**, the property that systems and data are accessible to authorized users when needed.
- **Encryption**, a process that transforms data into an unreadable form, protecting confidentiality.
- **Cryptographic hash**, a fixed-length fingerprint of data used to detect unauthorized modification.
- **DDoS (Distributed Denial-of-Service)**, an attack that floods a system with traffic to make it unavailable.
- **Redundancy**, duplicating critical systems or data so that a failure in one does not cause an outage.

## Common misconceptions
- "Security is mainly about keeping things secret." → Confidentiality is only one pillar; many attacks target integrity or availability and cause equal or greater harm without stealing any data.
- "Encrypting everything makes a system maximally secure." → Strong encryption protects confidentiality but can reduce availability (key loss, decryption latency) and does nothing to guarantee integrity on its own.
- "Availability is an IT problem, not a security problem." → Ransomware, DDoS, and sabotage are deliberate security attacks that target availability; it is explicitly part of the security mandate.

## Try it
- **Simulation:** Read each incident description, click the CIA pillar(s) violated, and reach 5 correct answers.
- **Coding problem:** Implement a CIA classifier that, given an incident description, returns the sorted list of pillars violated.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-12 Rev. 1 (Introduction to Information Security), rebuilt as original prose above; see `vendor/web/nist/sp800-12/` notes.
- Reference: Wikiversity "Information Security" module, foundational triad definitions.
- Practice: SANS Cyber Aces online modules (Module 1: Operating Systems), CIA examples rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/free-cybersecurity-resources`.
