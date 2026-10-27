# 1.3.b, Evil twin attack

> **Unit 1 · 1.3 The Dangers of Public Wi-Fi**
> **AP Learning Objective(s):** 1.3.B
> **Course skill(s):** Analyze Risk, Detect Attacks

## Learning objective (student-facing)
Explain how an evil twin attack works at the network level, identify
the indicators that reveal a rogue access point in a wireless scan, and apply those indicators to
detect one programmatically.

## Lesson
When you connect to Wi-Fi in a cafe, airport, or hotel, your device searches for a network name
(SSID) it recognizes or that you select from a list. It does not, by default, verify that the
access point broadcasting that name is the legitimate one. An **evil twin attack** exploits this
blind spot: an attacker sets up a second access point with the same SSID as a legitimate network,
often broadcasting a stronger signal to attract victims. Your device connects to the attacker's
hardware, and every byte of traffic you send passes through them before reaching the internet.

**How it works, step by step.** The attacker arrives at a location with a known public network, "Airport-Free-WiFi" or "CoffeeHouseGuest", and configures their own device (a laptop with a
wireless adapter in access-point mode, or a dedicated portable router) to broadcast the same
SSID. They often boost transmit power to outcompete the legitimate AP. Your device, scanning for
known networks, sees the SSID and connects, possibly automatically, if it connected to a network
with that name before. Once connected, you are on the attacker's network, not the real one.

From that position the attacker can perform a **man-in-the-middle (MitM)** attack: all your
traffic flows through their hardware. Unencrypted HTTP traffic is readable immediately. Even
HTTPS traffic can sometimes be downgraded or intercepted using a technique called SSL stripping,
which tricks your browser into communicating in plain text. The attacker can also serve you a
**captive portal**, a fake login page, that captures your credentials before forwarding you to
the real network so you do not notice anything wrong.

**What makes an evil twin detectable.** Every wireless access point has a **BSSID** (Basic
Service Set Identifier), which is the hardware MAC address of the radio that is broadcasting.
Two legitimate access points in the same building might both broadcast the SSID
"BuildingGuest" (this is normal for enterprise deployments with multiple APs), but each will
have a different BSSID, and in an enterprise, those BSSIDs are known and managed. An evil
twin has a BSSID that the legitimate administrator did not install: it is the MAC address of
the attacker's hardware.

Additional detection signals:
- **SSID matches a known-good name but the BSSID is not in the approved set**, the clearest
  red flag.
- **Security downgrade**, the legitimate network uses WPA3, but the evil twin broadcasts the
  same SSID with WPA2 or no security, because the attacker cannot replicate the enterprise
  credentials.
- **Duplicate SSID with different security settings**, same SSID, two different security
  levels appearing simultaneously.
- **Unusually strong signal from an unexpected direction**, a signal stronger than expected
  from a stationary AP may indicate a device placed very close to the victim.

**Why this matters on public Wi-Fi.** On a private home network, you configured the AP
yourself, you know its BSSID. On a public network, you have no prior knowledge. The evil
twin attack is particularly effective in public spaces precisely because users have no
reference point. They see the expected name and connect. The simulation (the simulation) gives you
practice scanning a list of detected access points and identifying which one is the rogue
based on BSSID and security anomalies, the same analytic process a wireless-security tool
would automate.

**Detection in practice.** Professional tools like wireless intrusion detection systems (WIDS)
maintain an approved list of known BSSIDs for each SSID and alert when an unknown BSSID
appears broadcasting an authorized SSID. The coding problem for this skill
asks you to implement the core detection logic: given a list of access points, return the
BSSIDs that are suspicious because the SSID is advertised by more than one BSSID, or because
an AP's SSID matches a known-good name but uses a different BSSID or weaker security.

**Defenses.** For end users: avoid connecting to public Wi-Fi when handling sensitive
information; use a VPN that encrypts all traffic regardless of the underlying network; check
for HTTPS on every page you visit; be skeptical if a site that previously worked over HTTPS
suddenly appears insecure. For administrators: deploy a WIDS, maintain an approved BSSID
list, use WPA3 Enterprise where possible, and educate users to report unexpected captive
portals. For device configuration: disable auto-connect to open networks so your device
does not silently join an evil twin without asking.

The evil twin is not exotic or rare, it requires no special skill beyond setting up a Wi-Fi
hotspot, which is built into most modern operating systems. A low-skilled adversary (covered
in atom 1.3.a) can execute it in minutes. That accessibility is what makes it so prevalent
and why recognizing it is a core AP competency.

## Key terms
- **SSID (Service Set Identifier)**, the human-readable name of a Wi-Fi network (e.g., "CafeGuest").
- **BSSID (Basic Service Set Identifier)**, the hardware MAC address of the radio broadcasting the network; each physical access point has a unique BSSID.
- **Evil twin**, a rogue access point broadcasting the same SSID as a legitimate network to intercept victim traffic.
- **Man-in-the-middle (MitM)**, an attack where the adversary secretly relays and can read or modify communications between two parties.
- **SSL stripping**, a MitM technique that downgrades an HTTPS connection to plain HTTP without the user noticing, exposing traffic to eavesdropping.
- **Captive portal**, a web page shown to new network users, often requiring authentication; attackers use fake versions to harvest credentials.

## Common misconceptions
- "If I see HTTPS in my browser, the connection is safe even on public Wi-Fi." → SSL stripping can remove HTTPS before your browser receives the page. Always check for HTTPS and be suspicious if it is absent where you expected it.
- "The same SSID appearing twice means my device is glitching." → Multiple BSSIDs for one SSID is normal in enterprise Wi-Fi, but an unexpected BSSID for a small public network is a strong indicator of an evil twin.
- "Evil twin attacks need sophisticated equipment." → Any device that can broadcast Wi-Fi, including a smartphone, can be configured as an evil twin in minutes.

## Try it
- **Simulation:** Scan a list of detected access points and click the rogue AP before the timer expires. Score full points by correctly identifying the evil twin in each round.
- **Coding problem:** Implement `solve(aps: list[dict]) -> list[str]` that returns the sorted list of suspicious BSSIDs given a scan result.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Open Security Training (wireless protocol security), rebuilt as original prose above; see `vendor/web/opensecuritytraining/`.
- Reference: NIST SP 800-153 (Guidelines for Securing Wireless Networks), `vendor/web/nist/`.
- Practice: Wikiversity wireless security modules, rebuilt locally as the simulation.
- Repo: CSIRT-MU/edu-resources, `vendor/repos/csirt-mu-edu-resources`.
