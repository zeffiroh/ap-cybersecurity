# 3.2.a, Wi-Fi basics and wireless security protocols (WPA2/WPA3)

> **Unit 3 · 3.2 Protecting Networks: Managerial & Wireless Security**
> **AP Learning Objective(s):** 3.2.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Compare WPA2 and WPA3 wireless security protocols, explain the
vulnerabilities each addresses, and evaluate a Wi-Fi network configuration against current best
practice.

## Lesson
Every modern office, school, and home relies on Wi-Fi, the family of wireless networking
standards collectively known as IEEE 802.11. Radio signals are convenient, but they are also
inherently public: anyone within range can receive the same frames your device sends. Without a
strong security protocol layered on top, an attacker sitting in a parking lot can eavesdrop on
every packet. Wireless security protocols exist to solve exactly that problem: they authenticate
who may join a network and encrypt the traffic between devices and the access point (AP).

**How Wi-Fi frames reach everyone nearby.** When a device sends a Wi-Fi frame, it radiates in all
directions. Unlike a wired Ethernet cable, where only the two endpoints see a conversation, every 802.11 device in range can detect the radio energy. A security protocol must therefore do
two things before any application data is exchanged: (1) prove the joining device is authorized,
and (2) negotiate encryption keys so that captured frames cannot be read.

**WEP, the failed first attempt.** The original Wired Equivalent Privacy (WEP) protocol, from
1997, used RC4 with a static 40- or 104-bit key. Researchers discovered by 2001 that WEP's key
scheduling algorithm leaked enough information that an attacker could recover the key by capturing
as few as 40,000 frames, achievable in minutes on a busy network. WEP is entirely broken and is
mentioned here only to show why its successors were necessary.

**WPA2, the long-standing standard.** Wi-Fi Protected Access 2 (WPA2), ratified in 2004, replaced
WEP's broken cipher suite with AES in Counter Mode with CBC-MAC (CCMP). AES-CCMP provides both
confidentiality and data integrity; even if an attacker captures every frame, they cannot decrypt
the payload or forge packets. WPA2 operates in two modes:

- Personal mode (WPA2-PSK), a single Pre-Shared Key (PSK) is given to everyone. When a device
  joins, it runs a four-way handshake with the AP using the PSK and derives a unique session key.
  The session key differs for every connection, so capturing one device's traffic does not expose
  another device's traffic. Personal mode is practical for homes and small offices.

- Enterprise mode (WPA2-EAP), clients authenticate with individual credentials through an
  802.1X authentication server (typically RADIUS). Each user or device has its own identity, so
  revoking one account does not affect others. Enterprise mode is required by most security
  frameworks for corporate environments.

WPA2's main weakness is the four-way handshake itself. An attacker who captures the handshake
can take it offline and run a dictionary or brute-force attack against the PSK. If the password
is weak or guessable, the attacker recovers the key and can decrypt all traffic to and from any
device that used that PSK. In 2017, the KRACK (Key Reinstallation Attack) vulnerability showed
that nonce reuse in the handshake could force decryption of certain frames, though patched
implementations are safe.

**WPA3, addressing WPA2's gaps.** WPA3, introduced in 2018 and required on new Wi-Fi certified
devices since 2020, closes the offline dictionary attack threat with Simultaneous Authentication
of Equals (SAE), also called Dragonfly. Instead of a static PSK hashed directly against network
traffic, SAE uses a zero-knowledge proof: both sides prove they know the password without ever
transmitting anything an offline attacker can use to mount a dictionary attack. Forward secrecy is
built in, each session negotiates fresh keys, so compromising today's session key cannot decrypt
yesterday's captured traffic.

WPA3-Enterprise upgrades the minimum cipher strength to 192-bit AES, matching Suite B
cryptographic requirements used in high-security government and defense networks.

WPA3 also introduces Enhanced Open (OWE) for open networks like coffee shops. Rather than
leaving traffic in plaintext, OWE negotiates unauthenticated but encrypted connections, meaning
an eavesdropper in the same coffee shop cannot read your traffic even though there is no password.

**Practical configuration decisions.** When evaluating a wireless network configuration:

1. Protocol version: prefer WPA3; accept WPA2-AES as a minimum; reject TKIP (a deprecated cipher
   that reintroduced RC4-level weaknesses) and WEP entirely.
2. Password strength: WPA2-PSK passwords should be at least 20 characters, randomly generated,
   and never dictionary words, each character adds exponential cost to offline attacks.
3. Network segmentation: guest devices should be on a separate SSID, ideally in an isolated VLAN
   that cannot reach internal resources.
4. Management interface: the AP's administrative console should require a strong unique password
   and, ideally, restrict access to a wired management VLAN.
5. Firmware: APs must run current firmware; KRACK and similar protocol bugs are patched at the
   firmware level.

The coding problem in `problem/` asks you to implement a function that inspects a Python
dictionary representing a Wi-Fi configuration and returns a sorted list of security gaps based on
these exact criteria. Applying the check systematically mirrors what enterprise wireless
assessment tools do automatically.

**Connecting to the AP framework.** LO 3.2.A asks you to evaluate controls that protect a
network. Wireless protocols are a technical control: they are implemented in hardware/software and
enforce policy without human action at each step. Choosing WPA3 over WPA2 (or WPA2 over WEP) is
a concrete, measurable mitigation decision, exactly the kind of risk-reduction choice the AP
course assesses.

## Key terms
- **IEEE 802.11**, the family of wireless networking standards defining Wi-Fi.
- **Access point (AP)**, the device that bridges wireless clients onto a wired network.
- **WPA2 (Wi-Fi Protected Access 2)**, the 2004 wireless security standard using AES-CCMP; current minimum acceptable.
- **WPA3**, the 2018 successor; uses SAE to prevent offline dictionary attacks and provides forward secrecy.
- **Pre-Shared Key (PSK)**, a shared password used in WPA2/WPA3 Personal mode to derive session keys.
- **SAE (Simultaneous Authentication of Equals)**, WPA3's zero-knowledge handshake that resists offline attacks.
- **Forward secrecy**, property ensuring that compromise of one session key cannot decrypt past sessions.
- **CCMP (AES-CCMP)**, the AES-based cipher suite providing confidentiality and integrity in WPA2/WPA3.
- **TKIP**, deprecated RC4-based cipher used in WPA (v1); do not use.
- **Four-way handshake**, WPA2's session-key negotiation; capturable and subject to offline attack.

## Common misconceptions
- "Hiding the SSID makes the network secure." → A hidden SSID is still broadcast in probe responses; any passive scanner finds it in seconds. SSID hiding is not a security control.
- "WPA2 with a strong password is good enough for enterprise." → Personal mode shares one key across all users; a departing employee who knew the PSK retains access until the password is changed for everyone. Enterprise mode (802.1X) is required for individual accountability.
- "WPA3 is automatically used if the router supports it." → Mixed-mode deployments allow WPA2-only clients to connect using WPA2; an attacker can force a downgrade. For maximum protection, disable WPA2 compatibility on networks where all clients support WPA3.

## Try it
- **Simulation:** Classify Wi-Fi configuration cards as secure, acceptable, or insecure based on protocol and password criteria.
- **Coding problem:** Implement `evaluate_wifi_config(cfg)` that returns a sorted list of security gaps in a Wi-Fi configuration dictionary.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-97 (Establishing Wireless Robust Security Networks), rebuilt as original prose above; reference copy at `vendor/web/nist/`.
- Reference: GeeksforGeeks wireless security overview, rebuilt equivalently.
- Practice: Cybrary wireless security micro-challenges, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/letsdefend-free-cybersecurity-resources`.
