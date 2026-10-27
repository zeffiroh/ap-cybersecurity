# 2.3.a, Physical access controls (locks, badges, biometrics, mantraps)

> **Unit 2 · 2.3 Protecting Physical Spaces**
> **AP Learning Objective(s):** 2.3.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)

Identify the purpose of each physical access control layer, locks, badge readers, biometrics, and mantraps, explain how they combine into a defense-in-depth strategy, and pinpoint gaps when one or more controls are absent.

## Lesson

### Why physical access matters

Every firewall rule, encryption key, and intrusion-detection alert becomes irrelevant if an attacker can walk through the front door, plug a USB drive into a server, or tailgate an employee into a restricted corridor. Physical security is not a legacy concern; it is the outermost layer of a layered defense model. The AP Cybersecurity framework places it in Unit 2 for exactly this reason: before any data can be protected logically, it must be protected physically.

The four controls covered here, locks, badge/RFID readers, biometrics, and mantraps, each address a different threat and serve a different point in the access flow. Understanding all four, and how they interact, is the foundation for auditing any facility.

### Locks: the first line

A mechanical keyed lock is the oldest and most universally understood physical control. A lock restricts entry to anyone who possesses the correct physical key. Its strengths are simplicity and independence from power or networks. Its weaknesses are equally plain: keys can be copied, lost, or stolen without leaving a digital trace. A maintenance worker who leaves employment still holds a copy of the key unless the lock is physically rekeyed or replaced.

Combination locks replace the physical key with a memorized sequence, reducing the risk of key duplication but introducing the risk of shoulder surfing, watching someone enter the combination. Neither type produces an audit log. You cannot review a lock's history to determine who entered a room at 2 a.m. last Tuesday.

Despite these limits, a good quality keyed deadbolt or cipher lock remains a necessary baseline. It is cheap, reliable, and requires no infrastructure. In a layered model it acts as the default fallback when electronic controls fail.

### Badge readers and RFID

An electronic access control system replaces or supplements the mechanical key with a credential stored on a smart card or RFID badge. When the badge is presented to a reader, the system checks whether that credential is authorized for that door at that time and logs the transaction. This solves two problems that locks cannot: credential revocation and audit trails.

Revoking a physical key requires retrieving it from the person. Revoking a badge credential requires one database update; the physical card becomes useless immediately even if the employee keeps it. The audit log allows administrators to review exactly which badge accessed which door at what time, critical evidence after a security incident.

RFID badges operate at short range (typically a few centimeters to a few meters depending on frequency). A common weakness is that standard RFID signals can be cloned using inexpensive reader hardware if the credential is not cryptographically protected. Modern systems use mutual authentication and encrypted tokens to defeat cloning, but older systems may not.

Badge systems do not verify identity, they verify possession of the badge. If an employee loses a badge or it is stolen, an unauthorized person gains access until the badge is revoked. This is why badge systems are typically combined with a second factor.

### Biometrics

Biometric controls verify identity by measuring a physical or behavioral characteristic that is unique to the individual: fingerprint patterns, retinal or iris structure, hand geometry, facial geometry, or voice pattern. Unlike a badge or password, a biometric characteristic cannot be handed to another person, cannot be forgotten, and is very difficult to replicate without the subject's cooperation.

Fingerprint readers are the most common. Retinal scanners offer higher accuracy but are slower, more expensive, and require the user to hold still close to the lens, factors that affect usability in high-throughput areas. Iris recognition achieves similar accuracy at a greater stand-off distance and is increasingly common in high-security facilities.

Biometrics introduce privacy considerations absent from locks and badges. The system must store a template derived from the biometric sample. If that template database is breached, unlike a password it cannot simply be changed. Modern systems store a mathematical hash of the biometric feature, not the raw image, but the sensitivity remains high.

False acceptance rate (FAR) and false rejection rate (FRR) are the two error metrics. FAR is the probability the system grants access to an unauthorized person; FRR is the probability it incorrectly denies an authorized person. Tuning a system for very low FAR raises FRR and frustrates legitimate users, and vice versa. Setting the threshold is a policy decision that balances security against operational friction.

### Mantraps and airlocks

A mantrap, also called an airlock or access vestibule, is an architectural control rather than an electronic one. It consists of two interlocked doors with a small chamber between them. The outer door must close and lock before the inner door can open. This eliminates tailgating: the practice of a second person following an authorized person through a door before it closes.

A mantrap can operate purely mechanically (a timed delay on the second door) or can incorporate weight sensors, CCTV, and a human guard watching a screen. In high-security variants, the chamber includes biometric or badge verification so that each person must authenticate individually before the inner door releases. Some facilities use the mantrap as the chokepoint for a thorough bag search.

The key limitation is throughput. A mantrap slows entry to one person (or one small group) per cycle. In a busy office building this creates queues and user frustration; for a data center server room it is entirely acceptable.

### Layering the controls

None of these controls is sufficient alone. The standard model is defense in depth: each layer assumes the previous one may fail.

A typical secure facility applies them in sequence:

1. Perimeter fence or wall, keeps casual intruders out.
2. Keyed lock or cipher lock on the building entrance, baseline physical barrier.
3. Badge reader at the secured zone entrance, provides audit trail and revocation.
4. Mantrap between the badge reader lobby and the server floor, eliminates tailgating.
5. Biometric reader inside the mantrap, verifies identity, not just badge possession.
6. CCTV throughout, provides visual evidence and deters internal threats.
7. Security guard, human judgment for exceptions, emergencies, and escort duties.

The coding problem in `problem/` formalizes this layering: given a description of which controls a facility has or lacks, identify the security gaps. The simulation in the simulation puts you in the role of a facility auditor working through six different facility configurations.

## Key terms

- **Keyed lock**, a mechanical barrier that requires a physical key to disengage; provides no audit trail.
- **RFID badge**, a credential token that communicates with a reader via radio frequency; supports audit logging and remote revocation.
- **Biometric**, an identity-verification method based on a measurable physical characteristic unique to a person (fingerprint, iris, etc.).
- **Mantrap**, a two-door vestibule with interlocked operation that prevents tailgating by allowing only one entry cycle at a time.
- **Tailgating**, following an authorized person through a secured door without authenticating; also called piggybacking.
- **False acceptance rate (FAR)**, the probability a biometric system incorrectly grants access to an unauthorized subject.
- **False rejection rate (FRR)**, the probability a biometric system incorrectly denies access to an authorized subject.
- **Defense in depth**, a security strategy that layers multiple independent controls so that the failure of one does not expose the asset.

## Common misconceptions

- "A badge reader is enough; locks are old-fashioned.", Locks provide power-independent fallback. If the badge system loses power or is misconfigured, a lock prevents the door from becoming unsecured.
- "Biometrics are infallible.", Every biometric system has FAR and FRR greater than zero. Fingerprints can be lifted and spoofed; some facial recognition systems are defeated by photographs. Biometrics should be one factor in a multi-factor scheme, not the only one.
- "A mantrap is only for spy movies.", Any data center or evidence room handles this threat seriously. Tailgating is one of the simplest physical attacks and requires no technical skill.
- "CCTV prevents intrusion.", CCTV is a detective control, not a preventive one. It records what happened; it does not stop an attacker from entering.

## Try it

- **Simulation:** Act as a facility security auditor, check which controls are installed at a fictional facility, identify all gaps, and score your audit across six rounds.
- **Coding problem:** Implement `solve(facility)` that returns a sorted list of access-control gap labels for a given facility configuration.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)

- Deep: NIST SP 800-116 Rev. 1 (Guidelines for the Use of PIV Credentials in Facility Access), vendor path `vendor/nist/sp800-116r1-summary.md`
- Reference: GeeksforGeeks, "Physical Security in Information Security", rebuilt equivalent at `vendor/reference/2.3.a-physical-access-ref.md`
- Practice: Wikiversity, "Introduction to Computer Security/Physical Security", rebuilt equivalent at `vendor/practice/2.3.a-physical-access-practice.md`
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/LetsDefend-Free-Cybersecurity-Resources/`
