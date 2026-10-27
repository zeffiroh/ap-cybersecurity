# 2.2.a, Unauthorized physical access (tailgating, piggybacking, lock bypass)

> **Unit 2 · 2.2 Physical Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 2.2.A, 2.2.B
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Identify tailgating, piggybacking, and lock-bypass techniques, explain how each circumvents physical access controls, and flag suspicious entry-log records that indicate an unauthorized access attempt.

## Lesson
Every cybersecurity textbook covers firewalls and encryption, but the most damaging breaches often begin with an attacker simply walking through the front door. Physical access controls, locked doors, badge readers, security checkpoints, are the first layer of defense for servers, wiring closets, and workstations. When that layer fails, an attacker can install a hardware keylogger, steal a laptop, plug in a rogue USB device, or photograph sensitive screens without ever cracking a password. Understanding how attackers bypass physical controls is the first step in defending them.

**Tailgating.** Tailgating occurs when an unauthorized person follows an authorized employee through a secured door without using their own credentials. The attacker exploits the social norm of holding a door open for the person behind you. A typical scenario: an attacker in business attire approaches a card-reader door carrying a box or coffee, hands full, appearing legitimate. A courteous employee swipes in and holds the door. The attacker says "thanks" and walks into a restricted area. No badge was scanned, no alarm sounded. The access log shows only the legitimate employee's entry.

Tailgating succeeds because of the same social-engineering pressure studied in 1.1.a: people feel awkward demanding that a colleague produce a badge, especially when time pressure ("I'm running late"), authority cues (a visitor badge, a suit, a clipboard), or simple politeness are in play. The physical and psychological attacks reinforce each other.

**Piggybacking.** Piggybacking is the consensual version of tailgating, the authorized employee knowingly lets someone through, usually as a favor. An employee holds the door for a familiar contractor or a visitor they think has clearance. In access logs, piggybacking looks identical to tailgating: one badge swipe, two people through the door. The critical distinction is intent, but the security risk is the same: an unverified person now has physical access.

Most organizations prohibit piggybacking in their acceptable-use or physical-security policies, but enforcement depends on culture. An environment that normalizes "just hold the door" trains employees to disable their own physical controls.

**Lock bypass techniques.** When tailgating is not possible, attackers may attack the lock itself. Common techniques include:

- **Lock picking:** Using pick tools to manipulate the pins of a pin-tumbler lock without the correct key. Inexpensive pick sets are commercially available and require only hours of practice for simple locks.
- **Bump keys:** A specially cut key that, when struck ("bumped") with a mallet while turned, momentarily bounces pins past the shear line, opening the lock. Effective against most residential and many commercial pin-tumbler locks.
- **Shimming:** Inserting a thin metal shim into a padlock's shackle to retract the locking mechanism without the key.
- **Credential cloning:** Copying the data from an RFID badge using a concealed reader, then replaying that data from a clone badge. Older 125 kHz HID proximity cards (common in older installations) have no cryptographic protection and can be cloned in seconds with hardware costing under $50.

Lock bypass is relevant not only to external perimeter doors but to server racks, network closets, and filing cabinets, any physical container that a padlock or cabinet lock is expected to protect.

**Why physical access is a force multiplier.** When an attacker reaches a device physically, most software-layer controls can be neutralized. A locked laptop can be booted from a USB drive to reset the password or dump the disk. An Ethernet port behind a locked panel can be reached with a simple lock bypass and used to plant a rogue network tap. Full-disk encryption is one of the few controls that survives physical access, but only if the device is powered off. This is why defense-in-depth stacks physical controls together with encryption, logging, and detection systems rather than treating any single layer as sufficient.

**What access logs reveal.** Many physical access systems write timestamped records: badge ID, door ID, result (granted or denied), and sometimes CCTV frame references. A well-maintained log can flag tailgating heuristics: if door D1 logs one swipe in a 30-second window but building cameras (or a second sensor) detect two people passing through, the difference is a red flag. Piggybacking appears as unusually fast sequential entries at nearby doors, one badge swipes D1 at 08:04:11 and again at D2 at 08:04:13 (physically impossible alone), suggesting a badge was passed back or the person ran, which itself may indicate anomalous behavior.

The coding problem for this skill asks you to implement exactly this log analysis: flag entries where the time gap between door events is too short for a single person, or where a door shows one badge swipe but a second sensor records two crossings.

**Defensive practices.** Awareness training that emphasizes the "one badge, one person" rule significantly reduces tailgating. Mantraps (two-door interlocks that prevent a second person from passing until the first door closes) eliminate the physical opportunity. RFID systems should be upgraded to encrypted, mutually authenticated 13.56 MHz cards (ISO 14443 / MIFARE DESFire) rather than legacy proximity cards. Locks on server racks and wiring closets should be high-security (Medeco, Abloy) and regularly audited. Badge-access logs should be reviewed algorithmically for the heuristics described above.

## Key terms
- **Tailgating**, following an authorized person through a secured entry without using one's own credentials; the authorized person is unaware or does not consent.
- **Piggybacking**, an authorized employee knowingly allows an unverified individual through a secured entry; the risk is identical to tailgating despite the consent.
- **Lock picking**, manipulating a lock's internal mechanism with specialized tools to open it without the correct key.
- **Bump key**, a specially cut key used with a striking blow to momentarily bypass pin-tumbler lock pins.
- **RFID badge cloning**, capturing the radio signal of an access badge and writing the data to a blank credential to gain unauthorized entry.
- **Mantrap**, a physical security control consisting of two interlocked doors; only one can be open at a time, preventing a second person from following through.

## Common misconceptions
- "Tailgating only works in movies." → It is one of the most frequently reported physical-penetration vectors in professional red-team assessments; social courtesy is a real and exploitable vulnerability.
- "A locked door means the room is secure." → Locks are a delay mechanism, not an absolute barrier; lock-bypass techniques, credential cloning, and tailgating all circumvent them without leaving obvious evidence.
- "Piggybacking is fine for people I recognize." → Recognition is not authorization; a familiar face may be a former employee, a social-engineering attacker who built rapport, or a contractor whose access has been revoked.

## Try it
- **Simulation:** Analyze a building access log stream, identify which entry events show tailgating or suspicious patterns, and flag them before unauthorized access reaches the server room.
- **Coding problem:** Implement a function that processes a list of badge-access log records and returns the IDs of events flagged as tailgating or impossible-speed violations.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (physical security principles), rebuilt as original prose above; see `vendor/web/mit-ocw/` notes.
- Reference: GeeksforGeeks (physical security overview), rebuilt locally.
- Practice: Cybrary physical-access awareness module, rebuilt locally as the simulation.
- Repo: her0marodeur/awesome-free-cybersecurity → `vendor/repos/her0marodeur-awesome-free-cybersecurity`.
