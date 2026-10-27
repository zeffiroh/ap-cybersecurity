---
deck:
  title: Wireless Security & Public Wi-Fi
  kicker: Class 7
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 7
  description: Evil twins, MITM, packet sniffing, and how WPA3 and VPNs defend the connection itself.
  topics: [Wi-Fi Risks, Evil Twin, MITM, Packet Sniffing, WPA2/WPA3, VPN]
---

---
title: Wireless Security & Public Wi-Fi
cover: true
---
:::text class=sub
Wireless networks introduce a unique and expansive attack surface that differs fundamentally from wired networks. Unlike traditional Ethernet, radio frequency (RF) signals propagate through open space, making them inherently more susceptible to interception, impersonation, and unauthorized access.
:::
:::list style=chips
- Evil Twin
- WPA3
- VPN
:::
::::columns
::col::
::::card
:::text
**Evil Twin**
An Evil Twin attack involves an adversary setting up a rogue wireless access point (AP) that mimics a legitimate one. Users unknowingly connect to the malicious AP, allowing the attacker to intercept credentials, inject malware, or redirect traffic.
:::
::::
::col::
::::card
:::text
**WPA3**
Wi-Fi Protected Access 3 (WPA3) is the latest security protocol for wireless networks, offering stronger encryption via Simultaneous Authentication of Equals (SAE) and enhanced protection against offline dictionary attacks.
:::
::::
::col::
::::card
:::text
**VPN**
A Virtual Private Network (VPN) creates an encrypted tunnel between the user's device and a remote server, securing data in transit, even over untrusted public Wi-Fi networks.
:::
::::
::col::
::::card
:::text
**Additional Risks**
- **Krack Attacks (CVE-2017-13077–13087)**: Exploit the WPA2 handshake.
- **Rogue Access Points**: Unauthorized devices connected to the network.
- **RF Interference & Jamming**: Disrupts availability.
:::
::::
::::

:::image src="images/07_wireless_attack_surface.png" alt="Overhead view of a coffee shop showing multiple wireless devices, a legitimate AP, and a rogue AP broadcasting the same SSID; signal bubbles overlap; an attacker laptop sits on the side with lines showing intercepted traffic flowing through it" caption="The wireless attack surface: RF signals propagate through open space, allowing any nearby device to intercept, impersonate, or interfere with communication" width=full
:::

:::notes
Wireless communication fundamentally alters the network security paradigm by replacing physical cables with radio waves that propagate through shared space. This shift introduces a broad attack surface that adversaries can exploit without requiring physical access to network infrastructure. Unlike wired networks, where an attacker must tap into a cable or compromise a switch, wireless signals can be intercepted by any device within range, making eavesdropping and man-in-the-middle attacks significantly more feasible.

One of the most prevalent threats in wireless environments is the **Evil Twin** attack. In this scenario, an attacker deploys a rogue access point (AP) configured to appear as a legitimate network, often mimicking the SSID and even the MAC address of a trusted AP. Unsuspecting users connect to the rogue AP, believing it to be safe, which allows the attacker to capture sensitive data such as login credentials, session cookies, or financial information. These attacks are particularly effective in public spaces like airports, cafes, and hotels, where users are accustomed to connecting to unfamiliar networks.

To mitigate such risks, robust encryption protocols like **WPA3** have been standardized. WPA3 improves upon WPA2 by introducing **Simultaneous Authentication of Equals (SAE)**, also known as Dragonfly, which replaces the vulnerable PSK handshake and provides resistance against offline dictionary attacks. Additionally, WPA3 enhances forward secrecy, ensuring that session keys are not compromised even if the long-term credentials are exposed.

However, even with WPA3, users on public Wi-Fi remain vulnerable to broader network-level threats. This is where **VPNs** become essential. A VPN encrypts all traffic between the user's device and a trusted endpoint, effectively shielding data from prying eyes, even if the underlying wireless network is compromised.

Other notable vulnerabilities include **Krack Attacks (CVE-2017-13077 through CVE-2017-13087)**, which exploit weaknesses in the WPA2 four-way handshake, allowing attackers to decrypt network traffic. **Rogue access points**, unauthorized devices plugged into the corporate network, can serve as backdoors for attackers. RF jamming and interference also pose availability risks, falling under the CIA triad's "Availability" principle.

From a compliance perspective, standards such as **NIST SP 800-48** provide guidelines for securing wireless networks, emphasizing the importance of configuration management, encryption, and continuous monitoring. Similarly, **ISO/IEC 27001** includes controls for managing wireless access and securing communications.

Wireless networks, particularly in public environments, demand layered defenses. Understanding the mechanisms behind threats like Evil Twin attacks, leveraging modern encryption standards like WPA3, and enforcing secure communication tunnels via VPNs are critical components of a robust wireless security posture.

The fundamental difference between wired and wireless network security deserves deeper attention because it changes the threat model in a qualitative way. In a wired network, gaining the ability to intercept traffic requires either physical access to a cable segment, compromise of a network device (switch, router), or access to a span port, all of which require substantial attacker effort and usually leave forensic evidence. In a wireless network, the radio medium is shared by design: every nearby device with a wireless adapter and the appropriate software can receive every frame broadcast by every other device within range. The "shared medium" property was deliberately designed for convenience and interoperability, but it fundamentally eliminates the physical access barrier that wired networks rely on for baseline security.

This architectural difference is why the IEEE 802.11 working group has continuously iterated on wireless security standards, from the deeply flawed WEP (1999), through WPA and WPA2 (2003/2004), to WPA3 (2018), and why even WPA3 cannot fully address threats that arise above the link layer. Encrypting the link protects against passive eavesdropping but does not protect against an attacker who controls a rogue access point that a victim connects to willingly. The higher-order defense, a VPN that provides end-to-end encryption regardless of the link-layer security, is the correct architectural response to this residual threat.
:::

%%%

---
unit: Foundations
code: WRF
title: 802.11 RF Fundamentals, The Physics Behind the Threat
---
:::callout style=soft
Wireless security begins with understanding the medium. Radio frequency (RF) signals do not respect walls, property boundaries, or organizational perimeters, they radiate outward in all directions to any receiver within range.
:::

::::columns
::col::
:::list heading="Key 802.11 Frequency Bands" style=plain smartart=chevron2
- **2.4 GHz**: Longer range, higher wall penetration, more congested (Bluetooth, microwaves share this band)
- **5 GHz**: Shorter range, faster throughput, less interference, most modern Wi-Fi 5/6 devices
- **6 GHz (Wi-Fi 6E/7)**: Newest band, least interference, requires close proximity
- **60 GHz (WiGig/802.11ad)**: Very short range, extremely high throughput, near-line-of-sight only
:::
::col::
:::table
| Band | Typical Range | Wall Penetration | Primary Risk |
|------|---------------|-----------------|--------------|
| 2.4 GHz | ~70m indoors | High | Long-range sniffing |
| 5 GHz | ~35m indoors | Medium | Evil twin at closer range |
| 6 GHz | ~15m indoors | Low | Limited but emerging |
:::
:::callout style=line
**Security implication**: A 2.4 GHz evil twin set up in a parking lot can reach targets inside a building. Threat actors do not need to be in the same room.
:::
::::

:::image src="images/07_rf_propagation_bands.png" alt="Overhead building floor plan showing three concentric signal-range circles from a central AP: innermost circle labeled 6 GHz reaches one room, middle circle labeled 5 GHz covers the floor, outermost circle labeled 2.4 GHz extends beyond building walls into the parking lot where an attacker vehicle is parked with a high-gain antenna" caption="RF propagation vs. frequency band: 2.4 GHz signals routinely extend beyond physical building perimeters, enabling attacks from outside the premises" width=full
:::

:::notes
Understanding radio frequency propagation is foundational to grasping why wireless networks present a qualitatively different security challenge from wired infrastructure. In a wired Ethernet network, the signal is confined to the physical cable, gaining access to the signal requires physical access to the cable or a network device. In an 802.11 wireless network, the signal radiates omnidirectionally from the antenna, propagating through air, walls, floors, and ceilings until it attenuates below the noise floor.

The three primary frequency bands in use for Wi-Fi have distinct propagation characteristics with direct security implications. The **2.4 GHz band**, used by original 802.11b/g/n and still widely supported, offers the greatest range, typically 70 meters indoors and up to 250 meters in open space, and the best ability to penetrate solid obstacles like concrete walls. This range is a security liability: an adversary with a directional high-gain antenna (readily available for under $50 online) can extend their effective reception range to several hundred meters, enabling attacks from a parked vehicle in a neighboring parking lot. The 2.4 GHz band is also shared with Bluetooth, microwave ovens, baby monitors, and ZigBee devices, creating interference that attackers can exploit for denial-of-service scenarios.

The **5 GHz band**, used by 802.11a/n/ac and Wi-Fi 5/6, offers greater throughput due to wider channel widths (up to 160 MHz vs. 40 MHz for 2.4 GHz) but has shorter range and less wall penetration. From a security perspective, this means 5 GHz evil twin attacks generally require the attacker to be closer to the target, reducing the attack range slightly. However, modern devices often support dual-band and will select whichever band has the stronger signal, meaning an attacker broadcasting a powerful 5 GHz signal can still succeed.

The **6 GHz band**, introduced with Wi-Fi 6E (802.11ax) and extended in Wi-Fi 7 (802.11be), is the newest addition and offers the least interference due to its relative scarcity of devices. However, its shorter range and higher susceptibility to physical obstructions mean it is primarily useful for high-density indoor deployments. From a security perspective, the 6 GHz band includes new security mandates: WPA3 is required for all 6 GHz operation, and Enhanced Open (OWE) is mandated for open networks, which closes some of the vulnerabilities present on older bands.

The concept of **monitor mode** is critical for understanding both offensive and defensive wireless security tools. In normal (managed) mode, a wireless adapter only processes frames addressed to its MAC address, discarding all others. In monitor mode, the adapter captures every 802.11 frame it can receive regardless of destination, beacon frames, probe requests, probe responses, authentication frames, association frames, and data frames from all devices on all SSIDs within range. This is the mode used by tools like Wireshark, Kismet, and Aircrack-ng for both legitimate network analysis and offensive reconnaissance. Understanding that any device in monitor mode can see all your wireless traffic, even if it is not the intended recipient, is the most important conceptual takeaway from RF fundamentals.

A wireless adapter in monitor mode captures the beacon frames of every access point in range. A typical building reveals dozens of networks, including those of neighboring businesses and homes, all broadcasting their names and security settings.

The IEEE 802.11 working group (part of the IEEE Standards Association) is responsible for maintaining and extending the 802.11 standard. The base standard was published in 1997; amendments include 802.11b (1999), 802.11a (1999), 802.11g (2003), 802.11i (2004, security enhancements later incorporated into WPA2), 802.11n (2009), 802.11ac (2013), and 802.11ax (2021). The naming convention changed from amendment letters to Wi-Fi generation numbers (Wi-Fi 4, 5, 6, 6E, 7) to simplify marketing, but the amendment designations remain in technical documentation. NIST references to 802.11 typically use the amendment designation, so familiarity with both naming systems is useful.
:::

%%%

---
unit: Foundations
code: WEP
title: WEP, Wired Equivalent Privacy and Why It Failed
---
:::callout style=soft
**WEP (Wired Equivalent Privacy)**, ratified in 1999 as part of the original IEEE 802.11 standard, was designed to provide data confidentiality equivalent to a wired network. Within three years, it was shown to be completely broken, an instructive case study in cryptographic design failure.
:::

::::columns
::col::
:::list heading="WEP's Fatal Design Flaws" style=plain smartart=VaryingWidthList
- **Short IV (24-bit)**: Initialization vectors repeat in busy networks within hours, enabling statistical key recovery
- **CRC-32 integrity check**: Not a cryptographic MAC; can be forged without knowing the key
- **Static keys**: Single shared key for all clients with no per-session derivation
- **RC4 stream cipher misuse**: WEP reused the keystream when IVs collided, enabling XOR-based decryption
- **No replay protection**: Attackers can capture and retransmit frames
:::
::col::
:::steps heading="WEP Key Recovery Attack (Fluhrer-Mantin-Shamir)" smartart=process2
1. Attacker places adapter in monitor mode and captures packets
2. Collects thousands to millions of unique IV values from captured frames
3. Applies FMS statistical analysis to identify "weak IVs" that leak key bytes
4. Recovers WEP key with sufficient IV samples, often in under 60 seconds with modern tools
5. Decrypts all past and future traffic captured on that network
:::
::::

:::image src="images/07_wep_iv_collision.png" alt="Timeline diagram showing WEP traffic over time: horizontal axis is time, vertical axis is IV value 0 to 16777215; green dots show IV values used over the first hour; by the second hour red dots show IV collisions reappearing; inset shows two captured packets with same IV being XORed to extract plaintext; attacker figure with magnifying glass on the right" caption="WEP IV collision: with only 24 bits of IV space (16.7 million values), a busy access point exhausts unique IVs in hours, enabling the Fluhrer-Mantin-Shamir statistical attack" width=full
:::

:::notes
WEP represents one of the most studied and pedagogically valuable failures in cryptographic protocol design. Understanding precisely what went wrong, and why it went wrong at a fundamental level rather than just an implementation level, provides lessons that apply far beyond wireless security.

WEP was designed in 1997 and standardized in 1999 to provide "a level of security equivalent to a wired LAN." The design used RC4, a stream cipher, for confidentiality and CRC-32 for integrity. Both choices contained serious flaws that would not be fully articulated until 2001, when Scott Fluhrer, Itsik Mantin, and Adi Shamir published "Weaknesses in the Key Scheduling Algorithm of RC4," describing what became known as the FMS attack.

The core problem is the **initialization vector (IV)**. RC4 requires a unique key for each message to maintain security, reusing keystreams from the same key allows trivial decryption via XOR. WEP attempted to solve this by prepending a 24-bit random IV to the shared key, creating a per-packet "key" of IV + shared-secret. The problem: 24 bits allows only 16,777,216 distinct IV values. On a busy network transmitting hundreds of packets per second, IV values begin colliding within hours. Two packets encrypted with the same IV can be XORed together, canceling the keystream and revealing the XOR of the two plaintexts, from which both plaintexts can often be recovered using statistical language analysis.

The FMS attack goes further: certain IV values are "weak" in RC4's key scheduling algorithm in a way that leaks information about the first byte of the key. By collecting thousands of packets encrypted with these weak IVs, an attacker can statistically recover the full WEP key. The aircrack-ng tool, released in 2004, automated this attack and could recover a 128-bit WEP key from a packet capture in under 60 seconds on consumer hardware. A follow-up technique called the PTW attack (Pyshkin-Tews-Weinmann, 2007) reduced this to under 5,000 packets.

The **CRC-32 integrity check** failure is equally instructive. CRC-32 is a linear function, it was designed to detect accidental data corruption, not deliberate modification. An attacker who knows any part of the plaintext can predictably modify bits in the ciphertext such that the CRC-32 of the modified plaintext remains valid. This enables bit-flipping attacks: the attacker can change the destination IP address, inject data, or modify financial amounts in transit while the integrity check passes.

The regulatory and standards response to WEP's failure is instructive: NIST deprecated WEP in SP 800-48 (Revision 1, 2008), explicitly prohibiting its use in federal systems. The Wi-Fi Alliance introduced WPA as a software upgrade path in 2003 and WPA2 (based on 802.11i) in 2004. Despite this, WEP-enabled devices remained common for years, and some legacy industrial and embedded systems still use it today.

WEP illustrates the failure of security through obscurity. Its algorithm was available only to licensed implementers, so researchers first had to reverse-engineer it from shipping hardware; once it was analyzed independently, its flaws were found quickly. WPA and WPA2 were published openly through the IEEE standards process, which allowed far more rigorous review. WPA2 still had weaknesses, notably KRACK, but none as fundamental as WEP's design failures.

CVE-2007-1337 is one of the CVE entries specifically tracking WEP vulnerabilities in certain Cisco Aironet implementations, though the WEP weaknesses are fundamentally protocol-level rather than implementation-specific, virtually every WEP implementation is vulnerable to FMS/PTW because the flaw is in the specification.
:::

%%%

---
unit: Foundations
code: PTL
title: Wireless Security Protocol Timeline
---
:::callout style=soft
Wireless security standards have evolved in direct response to discovered vulnerabilities. Each generation introduced to fix a predecessor's flaws reveals the iterative nature of cryptographic standards development.
:::

:::table
| Year | Standard | Key Feature | Key Vulnerability | Status |
|------|----------|-------------|-------------------|--------|
| 1999 | WEP | RC4 + 24-bit IV | FMS/PTW key recovery in minutes | **Deprecated** |
| 2003 | WPA (TKIP) | Per-packet key mixing, MIC | TKIP weaknesses (CVE-2008-2441) | **Deprecated** |
| 2004 | WPA2 (CCMP) | AES-128 encryption | KRACK (CVE-2017-13077–13087) | **Supported (weakening)** |
| 2018 | WPA3-Personal | SAE/Dragonfly | Dragonblood side-channels (CVE-2019-9494) | **Current standard** |
| 2018 | WPA3-Enterprise | 192-bit CNSA Suite | Requires 802.1X infrastructure | **Current standard** |
| 2022 | Wi-Fi 6E (6 GHz) | WPA3 mandatory for 6 GHz | Emerging device support | **Recommended** |
:::

:::code language=mermaid caption="Wireless security protocol evolution: each generation was a direct response to demonstrated vulnerabilities in the previous standard, the timeline reflects both cryptographic progress and the persistent gap between standard adoption and device deployment"
flowchart LR
  A["1999 WEP<br/>broken"] --> B["2003 WPA<br/>stopgap"] --> C["2004 WPA2<br/>AES-CCMP"] --> D["2017 KRACK<br/>flaw disclosed"] --> E["2018 WPA3<br/>SAE"]
:::

:::notes
The wireless security protocol timeline is more than a history lesson, it illustrates the recurring dynamic in cryptography where a standard is deployed, academic researchers discover fundamental weaknesses, and a new standard must be developed and deployed while the old one remains in widespread use. Understanding this cycle is critical for anticipating future vulnerabilities and planning upgrade strategies.

**WEP (1999)** was the original 802.11 security mechanism. As discussed in the previous slide, its use of RC4 with a 24-bit IV was fatally flawed. The Fluhrer-Mantin-Shamir attack was published in 2001; by 2004, automated tools made WEP cracking trivial. Despite this, WEP remained widely deployed for years because device replacement cycles are slow. NIST formally deprecated WEP in SP 800-48 Rev. 1 (2008), but WEP-enabled devices remained on the market and in use well into the 2010s.

**WPA (2003)** was an emergency interim fix developed by the Wi-Fi Alliance specifically because 802.11i (the permanent replacement for WEP) was not yet finalized. WPA used the Temporal Key Integrity Protocol (TKIP), which was designed as a software upgrade to WEP hardware by adding per-packet key mixing and a Message Integrity Check (MIC, nicknamed "Michael"). TKIP was explicitly designed to be implementable on existing WEP hardware via firmware update, it deliberately avoided requiring new hardware. This constraint meant TKIP retained RC4 as its cipher (though used more carefully). In 2008, researchers Tews and Beck demonstrated a partial plaintext recovery attack against TKIP (CVE-2008-2441), and in 2009, a more practical TKIP attack was demonstrated at PacSec Tokyo. WPA/TKIP is now deprecated.

**WPA2 (2004)** introduced AES-CCMP, a fundamentally different and much stronger encryption mechanism. AES (Advanced Encryption Standard) had been standardized by NIST in 2001 following an international competition; its inclusion in WPA2 represented a major security improvement. WPA2 remained the dominant wireless security standard for nearly 15 years. The KRACK vulnerability (2017) revealed weaknesses in the four-way handshake, but notably did not break AES-CCMP itself, the vulnerability was in the key management protocol, not the cipher. KRACK is patchable and patched devices are not vulnerable. WPA2 with patched implementations and PMF (Protected Management Frames) is still considered acceptable for non-sensitive environments.

**WPA3 (2018)** was certified by the Wi-Fi Alliance in June 2018. It comes in two variants: WPA3-Personal, which uses SAE (Simultaneous Authentication of Equals) to replace PSK; and WPA3-Enterprise, which adds a 192-bit security mode based on the Commercial National Security Algorithm (CNSA) Suite for high-security environments. Shortly after WPA3 was released, researchers discovered the "Dragonblood" vulnerabilities (CVE-2019-9494 and related CVEs), which exploited timing and cache side-channels in some WPA3-SAE implementations. These were patched quickly, demonstrating that even well-designed protocols can have implementation-level vulnerabilities.

The **device replacement lag** is a persistent challenge in wireless security. When WPA3 was certified in 2018, billions of WPA2 devices were in service. Enterprise environments with managed device fleets can be upgraded on a planned schedule, but consumer devices (phones, laptops, smart TVs, IoT devices) are replaced on multi-year cycles driven by economics rather than security. This creates environments where WPA3 and WPA2 and sometimes even WEP coexist on the same network, requiring access points to operate in "transition mode" that supports all three, which can undermine WPA3's security guarantees in some configurations.

Each Wi-Fi security standard has taken about five years to develop and five or more years to become the majority deployment, so weaknesses in a standard are usually found and fixed over the decade after its release. WPA3, released in 2018, should be expected to follow the same pattern.
:::

%%%

---
unit: Foundations
code: WIF
title: Why Public Wi-Fi Is Risky
---
:::callout style=soft
On a public Wi-Fi network, you can't verify who actually controls the access point, or who else is sharing the same airwaves.
:::

::::columns
::col::
:::list heading="Threat Vectors in Public Wi-Fi" style=plain smartart=radial6
- **Eavesdropping**: Unencrypted traffic can be captured using tools like Wireshark or tcpdump
- **Rogue Access Points**: Malicious APs mimicking legitimate ones (e.g., "Free Airport WiFi" spoofing)
- **Man-in-the-Middle (MITM)**: Interception and possible alteration of data in transit
- **Sidejacking**: Session hijacking via stolen cookies (e.g., Firesheep attacks)
:::
::col::
:::list heading="Common Encryption Weaknesses" style=plain
- **Open Networks**: No encryption (WEP/WPA/WPA2/WPA3 missing)
- **WEP (Deprecated)**: Vulnerable to key recovery (CVE-2007-1337)
- **Weak WPA2**: Susceptible to KRACK attacks (CVE-2017-13080)
- **Captive Portals**: Often unencrypted HTTP, exposing credentials
:::
:::callout style=line
**NIST SP 800-48** emphasizes the importance of verifying wireless network authenticity and warns against transmitting sensitive data over untrusted networks.
:::
::::

:::image src="images/07_public_wifi_threat_map.png" alt="Network topology diagram of a public café Wi-Fi scenario: central router connects to internet; legitimate AP on one side; rogue AP on other side; victim laptop connects to rogue; arrows show traffic path to attacker; labels identify eavesdropping, MITM, sidejacking attack vectors at each connection point" caption="Public Wi-Fi threat map: multiple attack vectors operate simultaneously on the same shared RF medium" width=full
:::

:::notes
Public Wi-Fi networks introduce a unique set of security risks primarily due to their open and unregulated nature. Unlike enterprise or home networks, users on public Wi-Fi often connect to access points (APs) they cannot authenticate or trust. This lack of verification opens the door to several attack vectors.

One of the most prominent threats is **eavesdropping**, where adversaries use readily available tools to capture unencrypted traffic. If a network lacks encryption (e.g., uses WEP or open authentication), attackers can intercept sensitive data such as login credentials, emails, or session tokens. Even with WPA2 encryption, vulnerabilities like the **KRACK attack (CVE-2017-13080)** allow attackers to decrypt packets under certain conditions.

Another serious concern is the presence of **rogue access points**, where attackers deploy malicious APs with names like "Starbucks WiFi" to trick users into connecting. These rogue APs can perform **man-in-the-middle (MITM)** attacks, enabling attackers to monitor, modify, or steal data in real time. Tools like *Ettercap* or *BetterCAP* automate such attacks.

Additionally, **session hijacking** (or sidejacking) remains a threat, especially on networks where session cookies are transmitted over unencrypted channels. Historical tools like *Firesheep* demonstrated how easily attackers could hijack active web sessions on open networks.

From a compliance perspective, **NIST Special Publication 800-48** provides guidelines for securing wireless networks, emphasizing the importance of verifying network authenticity and avoiding sensitive transactions over untrusted networks. Similarly, **ISO/IEC 27001** highlights the need for secure communication channels and risk assessment for wireless usage.

The risks of public Wi-Fi stem from a combination of weak or absent encryption, lack of endpoint authentication, and the shared nature of the wireless medium. These factors collectively make public Wi-Fi a fertile ground for passive and active network attacks.

The 2010 release of Firesheep serves as a landmark case study in why public Wi-Fi session security matters. Firesheep was a Firefox browser extension created by security researcher Eric Butler to demonstrate that session hijacking on open Wi-Fi networks was trivially easy. The tool would passively sniff HTTP traffic on the local network, automatically identify session cookies for popular websites (Facebook, Twitter, Amazon, Flickr, and dozens of others), and present them in a graphical interface, allowing anyone nearby to click a button and instantly take over another user's session on those sites. Butler released it specifically to force the major web platforms to universally adopt HTTPS, which they subsequently did. The episode illustrates a recurring pattern in security: theoretical vulnerabilities that practitioners know about for years are often only addressed at scale when a tool makes exploitation accessible to non-experts and the resulting public outcry creates reputational and commercial pressure.

Captive portals, the web pages that public Wi-Fi networks use to display terms of service or accept payment, introduce a specific and often overlooked risk. To display the captive portal, the network must redirect HTTP traffic to the portal page before the user has authenticated. This means the initial connection phase is always unencrypted and subject to interception or tampering. Additionally, many captive portals themselves use HTTP (not HTTPS), transmitting any credentials (e.g., hotel loyalty program login) in plaintext. Users who reuse passwords across their loyalty account and their email are therefore at risk even from the login step of joining the "secure" hotel Wi-Fi network.
:::

%%%

---
unit: Attacks
code: CPR
title: Captive Portals, The Hidden Risk at Every Hotel and Airport
---
:::callout style=soft
Captive portals are the web pages displayed when you first connect to a public Wi-Fi network. They are a mandatory security weakness: they require HTTP (unencrypted) redirects to function, creating a window of vulnerability every time a user joins the network.
:::

:::steps heading="How a Captive Portal Interception Attack Works"
1. **Victim connects** to a public Wi-Fi network (hotel, airport, café)
2. **Device sends HTTP request**, the only way to trigger the portal redirect (HTTPS cannot be intercepted this way)
3. **Network redirects** victim to captive portal page at an HTTP URL
4. **Victim enters credentials** (loyalty program login, room number, email), over HTTP if the portal is unencrypted
5. **Attacker captures** credentials from shared network using passive sniffing or by running a rogue portal page on their evil twin
6. **Victim is authenticated** and believes connection is now secure, but credentials are already stolen
:::

::::columns
::col::
:::list heading="Captive Portal Attack Vectors" style=plain
- Passive sniffing of HTTP credential submission
- DNS hijacking to serve fake portal on evil twin AP
- SSL stripping to downgrade HTTPS portal to HTTP
- Form injection to add credential-harvesting fields
- Fake "upgrade" or "terms acceptance" pages collecting PII
:::
::col::
:::callout style=line
**CVE-2015-5307 and related**: Various implementations of captive portal detection (used by Android, iOS, macOS) use hard-coded HTTP URLs for connectivity testing, these requests can be intercepted to spoof successful authentication.

**NIST SP 800-48** Section 4.3: "Users should be cautious about entering personal credentials on captive portal pages and should prefer networks that use encrypted portals (HTTPS)."
:::
::::

:::code language=mermaid caption="Captive portal credential theft: the mandatory HTTP phase of portal authentication creates an unavoidable plaintext credential exposure window, an evil twin AP can serve a convincing fake portal transparently"
sequenceDiagram
  participant V as Victim device
  participant E as Evil twin AP
  participant R as Real network
  V->>E: Connects to the familiar network name
  V->>E: Opens a web page
  E-->>V: Fake captive portal page
  V->>E: Enters email and password
  E->>E: Credentials recorded
  E->>R: Forwards traffic so nothing seems wrong
:::

:::notes
Captive portals are a ubiquitous feature of public Wi-Fi that most users encounter without thinking about the security implications. Every time you connect at an airport, hotel, coffee shop, or conference center and are redirected to a terms-of-service or login page, you are experiencing a captive portal. These systems work by intercepting your first HTTP request and redirecting it to the portal page. This mechanism is, by design, an attack against the normal operation of HTTP, the network is performing a form of man-in-the-middle redirection before you have authenticated.

The fundamental security problem with captive portals is that they require the initial connection to be unencrypted. The portal must intercept and redirect your first HTTP request, if your browser were already on HTTPS, the portal could not perform the redirect without triggering a TLS certificate error (because the certificate of the portal page would not match the domain you were trying to visit). The portal's network infrastructure therefore suppresses all HTTPS traffic and waits for an HTTP request to trigger the redirect. This means every device connecting to a captive portal network goes through a period of forced HTTP connectivity.

Several major operating systems use "captive portal detection" mechanisms that automatically detect when a network has a captive portal. Android sends HTTP requests to `connectivitycheck.gstatic.com`; Apple devices request `captive.apple.com`; Microsoft Windows requests `msftconnecttest.com`. These are all HTTP (not HTTPS) requests specifically so that captive portals can intercept them. An attacker running an evil twin AP with captive portal functionality can intercept these requests and respond with a redirect to a credential-harvesting page, the operating system's captive portal detection will then open a browser window pointed at the attacker's fake portal, presenting it as the network's login page.

The quality and security of legitimate captive portals varies enormously. Well-implemented captive portals serve their login pages over HTTPS with valid certificates, minimizing the credential exposure window. Poorly implemented captive portals (unfortunately common in hotels and smaller venues) serve the login page over HTTP, transmitting entered email addresses, room numbers, or loyalty program credentials in plaintext over the shared wireless medium, where any device in monitor mode can capture them.

A practical security concern for business travelers: hotel loyalty program credentials are among the most commonly targeted by captive portal interception attacks. This is because many users reuse their hotel loyalty credentials with their corporate email address. An attacker who captures these credentials gains not only the hotel loyalty account but potentially a valid username and password to try against corporate VPN portals, email systems, and other services. NIST SP 800-46 Rev. 2 ("Guide to Enterprise Telework, Remote Access, and Bring Your Own Device Security") specifically recommends that VPN connections be established before any other network activity when connecting to untrusted networks, this would prevent captive portal credential exposure by routing all traffic through the VPN tunnel before the credentials are entered. However, most captive portals block VPN traffic until the user has authenticated, creating a circular dependency that cannot be fully resolved at the user level.

The correct defense for organizations is to deploy their own VPN client with a "pre-logon" feature that connects to the VPN using device certificates before the user logs in, bypassing the captive portal requirement entirely. This is available in enterprise VPN solutions like Cisco AnyConnect and Palo Alto GlobalProtect.

Captive portals persist despite being insecure because they are usable: most guests cannot configure a VPN or enterprise Wi-Fi credentials. Real-world security balances protection against user experience, support cost and deployment complexity.
:::

%%%

---
unit: Attacks
code: DEA
title: Deauthentication Attacks, Forcing Clients Off the Network
---
:::callout style=soft
The 802.11 standard includes deauthentication and disassociation management frames, and until WPA3, these frames were unauthenticated, allowing any attacker to impersonate an access point and forcibly disconnect any client from any network.
:::

::::columns
::col::
:::steps heading="Deauthentication Attack Sequence" smartart=process5
1. Attacker captures beacon frames to learn the AP's BSSID (MAC address) and client MACs
2. Attacker crafts 802.11 deauthentication frames spoofing the AP's MAC address
3. Deauth frames are broadcast or sent to a specific client, no encryption or signing required
4. Client receives deauth, believes it is legitimate, terminates connection
5. Client attempts to reconnect, attackers can capture the WPA2 handshake during this process
6. Attack can be sustained continuously to create a denial-of-service condition
:::
::col::
:::list heading="Uses of Deauthentication Attacks" style=plain smartart=vList5
- **WPA handshake capture**: Force reconnection to obtain handshake for offline cracking
- **Evil twin facilitation**: Knock client off legitimate AP, capture on rogue AP instead
- **DoS attack**: Sustained deauth flood prevents clients from maintaining connectivity
- **Forced protocol downgrade**: If only rogue AP is available, client may accept weaker security
:::
:::callout style=line
**Protected Management Frames (PMF / 802.11w)**: WPA3 mandates PMF, which cryptographically authenticates management frames, making spoofed deauthentication frames detectable and ignorable by compliant clients.
:::
::::

:::code language=mermaid caption="Deauthentication attack flow: the attacker spoofs the AP's MAC address to send a legitimate-looking disconnect command, PMF in WPA3 closes this attack by requiring management frame authentication"
sequenceDiagram
  participant AP as Legitimate AP
  participant C as Client
  participant A as Attacker
  AP-->>A: Beacon reveals the AP's address
  A->>C: Forged deauthentication frame, appears to come from the AP
  C->>C: Disconnects
  C->>AP: Reconnects, handshake can be observed
  Note over AP,A: Defense: 802.11w Protected Management Frames (required in WPA3)
:::

:::notes
The deauthentication attack is one of the most elegantly simple attacks in the wireless security toolkit, and it illustrates how the original 802.11 designers prioritized network management simplicity over security in a way that created lasting vulnerabilities. Management frames, the frames used for connection setup, maintenance, and teardown, were not encrypted or authenticated in the original 802.11 standard. This was a conscious design choice: authentication and encryption require computational resources and key material, and the designers wanted management operations to be lightweight and universally supported.

The specific frame type abused in deauthentication attacks is the 802.11 Type 0, Subtype 12 (deauthentication) management frame. When an access point sends this frame to a client, the client is required by the standard to immediately terminate the association and return to an unauthenticated state. There is no authentication or verification of the frame source, the client cannot distinguish a legitimate deauthentication from a spoofed one. An attacker with a wireless adapter in monitor/injection mode can capture a beacon frame to learn the AP's BSSID, craft a deauthentication frame with the source address set to that BSSID, and transmit it on the same channel. The targeted client will dutifully disconnect.

This attack has two primary uses in the attacker's workflow. First, it enables **WPA handshake capture**. Offline password cracking attacks against WPA2 require capturing the 4-way handshake that occurs when a client connects. Rather than waiting for a client to naturally connect (which might take hours), the attacker sends deauthentication frames to force an immediate reconnection, capturing the handshake as part of the attack. Tools like aircrack-ng's aireplay-ng make this a two-command operation.

Second, it is a key enabler for **evil twin attacks**. An evil twin is most effective when the legitimate AP is also deauthenticating clients (either by design or because the attacker has put the client out of range of the real AP). Targeted deauthentication from the attacker's device knocks clients off the real AP, making the evil twin's association offer more likely to succeed, especially if the evil twin is operating at higher signal strength.

**Protected Management Frames (PMF)**, defined in IEEE 802.11w (2009) and incorporated into WPA2 as an optional feature, was specifically designed to address this vulnerability. PMF uses the negotiated session keys to provide data confidentiality and replay protection for unicast management frames, and uses a broadcast integrity protocol (BIP-CMAC-128) for multicast and broadcast management frames. WPA3 makes PMF mandatory, any device claiming WPA3 compliance must support and enforce PMF for all management frames. This means a spoofed deauthentication frame, which is not cryptographically authenticated with the session keys, will be rejected by a WPA3 client.

The transition from optional to mandatory PMF in WPA3 is a good example of how security standards can close protocol-level vulnerabilities, but only once there is sufficient device turnover to make the mandate enforceable. During the WPA3 transition period, networks running in "transition mode" that support both WPA2 and WPA3 clients may still be vulnerable to deauthentication attacks targeting WPA2 clients specifically.

The deauthentication attack works because management frames in WPA2 networks without 802.11w (Protected Management Frames) are unauthenticated, so a client can be forced to disconnect by a spoofed deauthentication frame. It requires no knowledge of the network password, which is why 802.11w is the necessary defense.
:::

%%%

---
unit: Attacks
code: TWN
title: Evil Twin Attacks
---
:::callout style=soft
An **evil twin** is a type of wireless attack in which an adversary deploys a fraudulent access point (AP) that mimics a legitimate one, typically by replicating its SSID (Service Set Identifier) and sometimes even its MAC address or signal strength, to deceive users into connecting to it.
:::

::::columns
::col::
:::list heading="Key Characteristics" style=plain
- Same SSID as the legitimate network
- Often uses open or weakly secured network settings
- Positioned to overpower or mimic the real AP's signal
- Designed to harvest credentials, intercept traffic, or deliver malware
:::
::col::
:::list heading="Common Targets" style=plain
- Public Wi-Fi hotspots (airports, cafes, hotels)
- Enterprise guest networks
- Residential networks with default configurations
:::
::::

:::flow
1. Attacker configures a rogue AP with the same SSID as a trusted network
2. Victim's device auto-connects based on prior network profiles
3. All traffic is routed through the attacker's machine
4. Man-in-the-middle (MITM) or traffic inspection occurs
5. Sensitive data (e.g., passwords, session cookies) may be captured
:::

:::image src="images/07_evil_twin_setup.gif" alt="Side-by-side comparison showing legitimate AP on the left broadcasting 'Airport_WiFi' at -70dBm signal strength, and evil twin AP on the right broadcasting the same SSID at -50dBm; victim device chooses the stronger signal; attacker's laptop connected to evil twin with a 'traffic mirror' arrow going to attacker" caption="Evil twin setup: rogue AP broadcasts the same SSID at higher signal strength, causing automatic client association to the attacker's device" width=full
:::

:::notes
An evil twin attack is a form of wireless man-in-the-middle (MITM) attack that exploits the automatic network selection behavior of wireless clients. These devices often maintain a list of previously connected networks (preferred network list or PNL) and will automatically reconnect to any network broadcasting a matching SSID. The attacker leverages this by broadcasting the same SSID, often with a stronger signal to ensure precedence.

The rogue access point typically does not enforce strong encryption or authentication, making it appear more appealing to the client than the legitimate network. Once connected, the attacker can inspect, modify, or log all unencrypted traffic. Even when HTTPS is used, attackers may attempt to bypass it using techniques like SSL stripping or by leveraging vulnerabilities such as those catalogued under CVE (e.g., CVE-2017-13089 related to WPAv2 Key Reinstallation Attacks).

According to NIST Special Publication 800-48, "Wireless Network Security," organizations should implement strict network access controls, user awareness training, and enforce encrypted connections (e.g., via VPNs) to mitigate such risks. ISO/IEC 27001 also emphasizes the importance of managing wireless network risks as part of an organization's broader information security management system (ISMS).

From a protocol perspective, evil twin attacks exploit weaknesses in IEEE 802.11 network discovery and association mechanisms. Unlike rogue access points, which may simply be unauthorized but benign devices, evil twins are intentionally deceptive and malicious in design.

The technical mechanics of evil twin attacks are worth examining in detail because they reveal how a protocol-level design choice, automatic re-association to known SSIDs, becomes a security liability. The 802.11 standard does not provide any mechanism for a client to cryptographically verify that a particular AP is the same physical device it previously trusted. The SSID is simply a human-readable string broadcast openly in beacon frames; any device can broadcast any SSID at any time. This design was intentional in the early 802.11 era, when usability and roaming were the primary concerns, but it creates a structural weakness that has never been fully addressed in subsequent versions of the standard.

An attacker setting up an evil twin needs only a laptop with a wireless adapter that supports monitor mode and packet injection (such as an Alfa AWUS036ACH), and freely available software like hostapd (for access point functionality), dnsmasq (for DHCP/DNS), and a traffic proxy like mitmproxy or Bettercap. The entire setup can be completed in minutes and fits in a backpack. The attack is passive in the sense that the attacker does not need to do anything once configured, victim devices will associate automatically when they come within range.

The evil twin threat is compounded by the prevalence of automatic reconnection. When a user joins "Airport_Free_WiFi" once on a trip, their device stores this network in its Preferred Network List (PNL) and will silently reconnect to any network broadcasting that same SSID without user interaction. At any airport the user subsequently passes through, or in any coffee shop that happens to have a network with the same name, their device may connect to a completely different and potentially malicious network without displaying any warning.

Defense against evil twin attacks operates at multiple levels: network authentication (802.1X with RADIUS prevents unauthorized APs from completing the authentication handshake), endpoint behavior (VPNs protect traffic regardless of which AP the device connects to), and user awareness (verifying SSID names and being suspicious of unexpected automatic connections). No single control is sufficient; defense requires combining all three.
:::

%%%

---
unit: Attacks
code: RVE
title: Rogue Access Points vs. Evil Twins, Know the Difference
---
:::callout style=soft
"Rogue access point" and "evil twin" are often used interchangeably, but they describe different threat scenarios requiring different defenses. Understanding the distinction matters for both detection and response.
:::

:::table
| Attribute | Rogue Access Point | Evil Twin |
|-----------|-------------------|-----------|
| Intent | May be accidental (employee plugs in personal AP) or malicious | Always malicious |
| Location | Connected to the wired corporate network | Standalone, provides its own internet via attacker's connection |
| SSID | May use any SSID, often its own default name | Deliberately copies a legitimate SSID |
| Detection method | Wired-side monitoring: unexpected MACs on switch ports | RF monitoring: duplicate SSIDs with different BSSIDs |
| Primary risk | Bypasses perimeter controls; creates unauthorized network entry point | MITM, credential harvesting, malware injection |
| NIST reference | NIST SP 800-153 Section 4.2 | NIST SP 800-48 Section 3.3 |
| MITRE ATT&CK | T1200 (Hardware Additions) | T1557.002 (ARP Cache Poisoning) / T1040 (Network Sniffing) |
:::

::::columns
::col::
:::list heading="Detecting Rogue APs" style=plain
- Audit switch port MAC address tables for wireless adapter MACs
- Use 802.1X port authentication, unauthorized devices cannot pass traffic
- Deploy WIDS to alert on unexpected SSIDs
- Conduct periodic physical inspections of network closets and open ports
:::
::col::
:::list heading="Detecting Evil Twins" style=plain
- WIDS: alert on duplicate SSIDs with different BSSIDs on the same channel
- Monitor for signal strength anomalies (unexpectedly strong signal from known SSID)
- Track channel: legitimate corporate APs have known channels, alert on SSID appearing on wrong channel
- 802.1X: client rejects any AP that cannot complete EAP authentication
:::
::::

:::code language=mermaid caption="Rogue AP vs. evil twin: rogue APs are physically connected to your network and bypass perimeter controls; evil twins impersonate your network from outside it, each requires different detection and response"
flowchart LR
  R["<b>Rogue AP</b><br/>Plugged into the corporate switch<br/>physically on your network<br/>Find it: switch port and wired scans"] ~~~ E["<b>Evil twin</b><br/>Separate device, no wired link<br/>impersonates your network name<br/>Find it: wireless IDS, BSSID mismatch"]
:::

:::notes
The distinction between rogue access points and evil twins is important to get right, especially for students heading into network security roles where the response to each is quite different.

A **rogue access point** is an unauthorized AP that is physically connected to the organization's wired network. The most common source is a well-intentioned employee who plugs in a personal wireless router to get better Wi-Fi coverage at their desk, or to share internet access with personal devices. The security problem is not that the AP itself is malicious, it usually is not, but that it creates an unmonitored, unmanaged wireless entry point into the wired corporate network, bypassing the organization's perimeter controls entirely. An attacker who discovers this rogue AP (by wardiving, scanning from a parking lot, or being a building visitor) can access the internal network without going through any firewall or intrusion prevention system. Rogue APs may also violate regulatory requirements: in a PCI DSS environment, for example, any unauthorized device that creates a pathway to the cardholder data environment is a compliance violation.

Detection of rogue APs is primarily a wired-side problem: you look for unexpected MAC addresses on switch ports, particularly MAC addresses belonging to vendors known for producing consumer wireless routers (Netgear, ASUS, TP-Link, Linksys). 802.1X port-based network access control is the strongest defense, if every switch port requires 802.1X authentication before passing traffic, a rogue AP plugged into an open port will not be able to put traffic on the network without valid credentials.

An **evil twin** is an entirely different scenario. The attacker has no physical connection to the target network at all. They set up a standalone AP that broadcasts the same SSID as the target network, provides DHCP to connecting clients, and routes their internet traffic through the attacker's own internet connection (which may be a mobile hotspot or the attacker's own wired connection). The evil twin is not on your network, it is a completely separate network that happens to look identical from the perspective of a victim's device.

Detection of evil twins is an RF-domain problem. The primary detection method is monitoring for the same SSID broadcasting from a different BSSID (MAC address) than the known legitimate AP. A wireless intrusion detection system (WIDS) configured with the BSSIDs of all legitimate APs will alert when an unknown BSSID appears broadcasting a known SSID. This is why maintaining an accurate inventory of all access points (including their BSSIDs, operating channels, and approximate signal strengths) is a critical input to effective evil twin detection.

NIST SP 800-153 ("Guidelines for Securing Wireless Local Area Networks") addresses both threat types and provides specific guidance on deploying WIDS systems, conducting regular RF surveys to establish baselines, and integrating wireless security monitoring into overall security operations.

A rogue access point and an evil twin differ in origin. A rogue AP is an unauthorized device connected inside the organization's own network, a threat from within the perimeter. An evil twin is an external device that imitates a trusted network's name to lure clients, a threat from outside that exploits the network's identity. The defenses differ accordingly: wired-side detection for rogue APs, client-side verification for evil twins.
:::

%%%

---
unit: Attacks
code: ETE
title: Worked Example, Evil Twin with Bettercap
---
:::callout style=soft
This worked example walks through how an evil twin attack is executed using Bettercap, a freely available penetration testing framework. Understanding the attacker's workflow informs how to build effective defenses.
:::

:::steps heading="Evil Twin Attack, Step by Step (Bettercap)"
1. **Reconnaissance**: `bettercap -iface wlan0` → `wifi.recon on` captures beacon frames; `wifi.show` lists all nearby SSIDs with BSSIDs, channels, and client counts
2. **Target selection**: Identify target SSID (e.g., "CoffeeShop_Free") and its operating channel (e.g., CH 6)
3. **Deauthentication**: `wifi.deauth all` sends deauth frames to all clients of the target AP, forcing reconnection
4. **Evil twin creation**: Configure `hostapd` to broadcast "CoffeeShop_Free" on CH 6; configure `dnsmasq` for DHCP; route traffic through attacker's internet connection
5. **Credential capture**: `bettercap` HTTPS proxy with `net.sniff on` captures credentials; `http.proxy` with SSL stripping intercepts HTTPS
6. **Cleanup**: All tools terminate; adapter returns to managed mode; no persistent traces on any network device
:::

::::columns
::col::
:::list heading="Tools in the Attack Stack" style=plain
- **Bettercap**: Reconnaissance, deauth, sniffing, proxy
- **hostapd**: Access point daemon (Linux), creates the rogue AP
- **dnsmasq**: DHCP/DNS server, provides IP addresses to victims, enables DNS spoofing
- **iptables/nftables**: NAT and traffic routing through attacker's internet uplink
- **mitmproxy** (optional): Interactive proxy for inspecting/modifying HTTPS traffic
:::
::col::
:::callout style=line
**Legal and ethical note**: Performing these attacks on any network or device without explicit written authorization is illegal under the Computer Fraud and Abuse Act (18 U.S.C. § 1030), the UK Computer Misuse Act 1990, and equivalent laws in virtually every jurisdiction. This material is presented for defensive awareness only. In authorized penetration tests, these techniques are used to demonstrate risk and drive remediation.
:::
::::

:::notes
Walking through the attacker's workflow in detail is one of the most effective teaching techniques in offensive security education. When defenders understand precisely what steps an attacker takes, what tools they use, and what artifacts the attack produces, they can design detection and prevention controls that specifically interrupt those steps. This is the "know your enemy" principle articulated in Sun Tzu's Art of War and encoded in the adversary emulation approach of frameworks like MITRE ATT&CK.

The evil twin workflow described in this slide maps to the following MITRE ATT&CK techniques: **T1040 (Network Sniffing)** for the passive reconnaissance and sniffing phases, **T1557 (Adversary-in-the-Middle)** and specifically **T1557.002 (ARP Cache Poisoning)** for the interception phase, and **T1110 (Brute Force)** if the captured handshake is subjected to offline dictionary cracking.

**Step 1, Reconnaissance** is entirely passive and leaves no trace on any network device. Bettercap in `wifi.recon` mode places the wireless adapter in monitor mode and collects beacon frames, probe responses, and data frames. The `wifi.show` command displays a table of discovered SSIDs with their BSSIDs (MAC addresses), signal strengths, channels, encryption types, and associated client counts. This information is sufficient to plan the rest of the attack.

**Step 2, Target selection** involves choosing which SSID to impersonate. Common targets are networks with many clients (higher chance of capturing valuable credentials), networks with weak or no encryption (easier to create a convincing twin), and networks with names suggesting public use ("Guest_WiFi", "Airport_Free", "CoffeeShop_WiFi"). The attacker also notes the operating channel, the evil twin must broadcast on the same channel to be effective.

**Step 3, Deauthentication** speeds up victim association to the evil twin. Without deauth, the attacker must wait for clients to naturally disconnect and reconnect, or outpower the legitimate AP (which requires the attacker to be physically close and risks detection). With deauth frames, clients are forcibly disconnected in seconds. The `wifi.deauth` command in Bettercap handles the spoofed frame construction and transmission automatically.

**Step 4, Evil twin creation** requires two main components: the AP daemon (hostapd on Linux) configured to match the target SSID and channel, and the network services (dnsmasq for DHCP and DNS). The evil twin provides internet access through the attacker's own uplink, NAT via iptables or nftables routes victim traffic through the attacker's machine and then to the internet. This is essential for the attack to be undetected: if the victim cannot access the internet, they will suspect something is wrong and disconnect.

**Step 5, Credential capture** is where the payload of the attack is collected. Bettercap's `net.sniff` module captures all traffic; `http.proxy` can intercept HTTP transactions; with SSL stripping enabled, HTTPS sessions are downgraded to HTTP and credentials are exposed in plaintext. For services that implement HSTS or certificate pinning, SSL stripping will not work, and the attacker would need to use a different technique (such as serving a fake lookalike domain with a valid-looking certificate obtained via a certificate authority that does not verify domain control adequately).

**Step 6, Cleanup** is often overlooked in classroom discussions but is critically important in real incidents. Because the evil twin attack requires no persistent installation on any victim device or network infrastructure, and because the attacker's adapter in monitor/injection mode leaves no network-level trace (it transmits but does not associate with any network), forensic investigation of a completed evil twin attack is extremely difficult. There are no server logs, no firewall logs, and no authentication logs on the victim side. Detection must happen in real-time via WIDS.

Credential capture on an open or evil-twin network is possible because traffic that is not independently encrypted passes through the attacker's device in cleartext. Seeing this makes concrete why a VPN or end-to-end encryption is required on untrusted networks.
:::

%%%

---
unit: Attacks
code: MIM
title: Man-in-the-Middle on Wi-Fi
---
:::callout style=soft
A **Man-in-the-Middle (MITM)** attack occurs when an attacker inserts themselves into the communication path between two parties, enabling them to intercept, monitor, and potentially alter data in transit without the knowledge of either party.
:::

:::pullquote
An evil twin is often just the setup, MITM is what happens next.
:::

::::columns
::col::
:::list heading="Common MITM Techniques on Wi-Fi" style=plain
- Evil Twin Access Points
- ARP Spoofing (on local networks)
- DNS Spoofing
- SSL Stripping
- Packet Injection
:::
::col::
:::flow
st=>start: Victim Device
ap=>operation: Rogue AP (MITM)
dest=>end: Destination Server

st->ap->dest
:::
::::

:::image src="images/07_mitm_traffic_flow.png" alt="Data flow diagram showing victim device on the left sending an HTTPS login request; attacker in the center performs SSL stripping, converting HTTPS to HTTP; plaintext credentials flow from victim through attacker to server; attacker shows credential capture sidebar with logged username and password" caption="MITM with SSL stripping: attacker downgrades HTTPS to HTTP to read plaintext credentials in transit, HSTS protects against this but many sites still lack it" width=full
:::

:::steps heading="MITM Attack Execution on Public Wi-Fi"
1. **Position**, Attacker deploys evil twin AP and victim auto-connects
2. **Intercept**, All victim traffic now passes through attacker's machine
3. **SSL strip**, Attacker tool downgrades HTTPS connections to HTTP using sslstrip or Bettercap
4. **Harvest**, Credentials, session cookies, and form data captured in plaintext
5. **Relay**, Attacker forwards traffic to real destination so victim's session appears normal
6. **Exfiltrate**, Captured data logged, saved, or immediately used to access victim's accounts
:::

:::notes
A Man-in-the-Middle (MITM) attack in wireless environments exploits the inherent trust users place in network connectivity and the lack of end-to-end encryption in many legacy or misconfigured systems. In a typical Wi-Fi MITM scenario, the attacker positions themselves logically between the victim's device and the intended destination server, often by deploying an **evil twin** access point or compromising a legitimate one.

Once in this privileged position, the attacker can perform both **passive** and **active** attacks. Passive attacks involve eavesdropping on unencrypted traffic or capturing encrypted data for later analysis (e.g., using tools like Wireshark). Active attacks include modifying packets, injecting malicious content, redirecting users to phishing sites, or performing **SSL stripping**, where HTTPS connections are downgraded to HTTP to bypass encryption.

The effectiveness of such attacks is significantly increased in open or poorly secured public Wi-Fi networks, where Transport Layer Security (TLS) may be improperly implemented or entirely absent. Standards such as NIST SP 800-48 and ISO/IEC 27001 emphasize the importance of secure configuration management and user awareness to mitigate these risks.

Notable CVEs related to MITM vulnerabilities include CVE-2017-13089 (KRACK attack against WPA2) and CVE-2020-12674 (TLS stripping in certain mobile apps), which demonstrate real-world exploitation of weak cryptographic implementations and protocol flaws.

To detect and prevent MITM attacks, network administrators should enforce mutual authentication, certificate pinning, encrypted DNS (e.g., DNS over HTTPS), and regular vulnerability scanning in accordance with frameworks like the MITRE ATT&CK framework (Initial Access > Valid Accounts, T1078).

SSL stripping, originally documented by Moxie Marlinspike at Black Hat 2009, exploits the gap between the theoretical security of HTTPS and its practical deployment. The attack works as follows: when a user types "bank.com" into their browser without the "https://" prefix, the browser sends an unencrypted HTTP request first. The attacker, positioned in the middle, intercepts this HTTP request, establishes its own HTTPS connection to the real bank.com, and serves the victim an HTTP version of the site. The victim sees their bank's login page but is communicating with the attacker over unencrypted HTTP, while the attacker communicates with the real bank over encrypted HTTPS on their behalf.

HTTP Strict Transport Security (HSTS), defined in RFC 6797, was developed specifically to counter SSL stripping. A web server that sends the HSTS header tells browsers to always use HTTPS for that domain, even if the user types the URL without the "https://" prefix. The HSTS preload list (maintained by browser vendors) extends this to domains that have never been visited before. However, HSTS is only effective for domains the browser already has an HSTS record for, a first-time visitor to a domain without preloading is still vulnerable.

DNS spoofing represents another dimension of MITM attacks: the attacker's controlled access point serves as the DHCP server, assigning itself as the DNS server for connected clients. It can then return falsified DNS responses directing victims to attacker-controlled IP addresses for any domain, enabling credential phishing even when the victim types the correct URL. DNS over HTTPS (DoH, RFC 8484) and DNS over TLS (DoT, RFC 7858) protect against this by encrypting DNS queries, preventing the attacker from seeing or modifying the resolution process.
:::

%%%

---
unit: Attacks
code: DNS
title: DNS Spoofing on Wi-Fi
---
:::callout style=soft
When an attacker controls the Wi-Fi access point, they also control the DHCP server, which assigns the DNS server to every client. By returning falsified DNS responses, the attacker can redirect any domain to a phishing server under their control.
:::

:::steps heading="DNS Spoofing Attack Chain"
1. Victim connects to evil twin AP
2. DHCP response assigns attacker's machine (e.g., 192.168.1.1) as default DNS server
3. Victim's browser resolves "bankofamerica.com", query goes to attacker's dnsmasq
4. Attacker's DNS server returns 192.168.1.100 (attacker's phishing server) instead of real IP
5. Victim's browser connects to 192.168.1.100, served a pixel-perfect phishing page
6. Victim enters credentials, sent to attacker; attacker optionally forwards to real site
:::

::::columns
::col::
:::list heading="DNS Spoofing Defenses" style=plain
- **DNS over HTTPS (DoH, RFC 8484)**: Encrypts DNS queries to a trusted resolver, DHCP-assigned DNS server cannot intercept or modify
- **DNS over TLS (DoT, RFC 7858)**: TLS-encrypted channel to DNS resolver
- **DNSSEC**: Cryptographic signing of DNS records, prevents response forgery (but not query interception)
- **Hardcoded DNS in applications**: Apps that bypass OS DNS settings are immune to DNS hijacking
- **VPN**: Routes all DNS queries through the encrypted tunnel
:::
::col::
:::callout style=line
**CVE-2020-25681 through CVE-2020-25687**: "DNSpooq", buffer overflow and cache poisoning vulnerabilities in dnsmasq (the same tool used by many routers and by attackers in evil twin setups). Affected millions of devices; patched in dnsmasq 2.83 (January 2021). Demonstrates that DNS infrastructure itself is a target.

**NIST SP 800-81-2** (Secure Domain Name System Deployment Guide) provides authoritative guidance on DNSSEC deployment and DNS security hardening.
:::
::::

:::code language=mermaid caption="DNS spoofing on an evil twin network: the attacker's DHCP server assigns itself as DNS resolver, enabling any domain to be redirected to a phishing server, DoH bypasses this by encrypting DNS queries to a remote trusted resolver"
sequenceDiagram
  participant V as Victim laptop
  participant A as Attacker AP and DNS
  participant B as Real bank server
  V->>A: Where is bankofamerica.com?
  A-->>V: 192.168.1.100 (attacker's server)
  V->>A: Connects to the fake address
  A-->>V: Phishing copy of the bank site
  V->>A: Enters credentials
  Note over V,B: The real bank server is never contacted
:::

:::notes
DNS spoofing in the context of wireless MITM attacks is particularly insidious because it operates at a layer below the application, the victim's browser never makes a connection attempt to the real server at all, yet receives a perfectly functional web page that looks identical to the real site. Unlike SSL stripping, which requires the victim to visit a site for the first time without HTTPS, DNS spoofing works regardless of whether the victim has previously visited the site, because the fake DNS response is returned before any connection is made.

The attack is enabled by the DHCP protocol's design: when a device connects to a network, it sends a DHCP discovery broadcast requesting network configuration. The DHCP server (in this case the attacker's evil twin AP running dnsmasq or a similar tool) responds with an IP address, subnet mask, default gateway, and, critically, the address of the DNS resolver to use. The victim's operating system trusts this response and routes all subsequent DNS queries to the attacker-controlled resolver. There is no authentication of DHCP responses in standard DHCPv4; any machine that responds first can assign itself as the DNS server.

The consequences of this are far-reaching: every unencrypted DNS query reveals which domains the victim is visiting (providing a behavioral profile even before any credentials are captured), and every domain can be redirected to an attacker-controlled server. This is why DNS has been described as the "phonebook of the internet", and why controlling it gives an attacker extraordinary power over the victim's internet experience.

**DNS over HTTPS (DoH)** and **DNS over TLS (DoT)** are the most effective defenses against DNS spoofing in the public Wi-Fi threat model. Both protocols encrypt DNS queries between the client and a remote DNS resolver (e.g., Cloudflare 1.1.1.1 or Google 8.8.8.8) in a way that the DHCP-assigned local DNS server cannot intercept or modify. Even if the attacker's DHCP server assigns 192.168.1.1 as the DNS server, if the victim's device uses DoH to send all queries to 1.1.1.1 over HTTPS, the attacker sees only an encrypted HTTPS connection to 1.1.1.1 and cannot redirect or inspect the DNS queries. Firefox and Chrome both support DoH natively, and Windows 11 includes built-in DoT support.

**DNSSEC** (DNS Security Extensions) provides a different form of protection: it cryptographically signs DNS records at the authoritative server, allowing resolvers to verify that responses have not been tampered with. However, DNSSEC does not encrypt DNS queries, it only verifies their integrity. An attacker who controls the local DNS resolver can still see all DNS queries (privacy violation) even with DNSSEC. More importantly, DNSSEC only protects against response forgery if the client performs DNSSEC validation; many clients rely on the resolver to perform validation (validator trust model) rather than performing it themselves. In the evil twin scenario, the resolver is the attacker, who would simply claim DNSSEC validation succeeded regardless of the actual record signatures.

The **DNSpooq** vulnerability cluster (CVE-2020-25681 through CVE-2020-25687), disclosed by researchers at JSOF in January 2021, is worth discussing because it demonstrates that DNS infrastructure itself can be targeted. DNSpooq was a set of vulnerabilities in dnsmasq, software used by hundreds of millions of routers, IoT devices, and Linux systems as a lightweight DNS/DHCP server. The vulnerabilities included cache poisoning (allowing an attacker to inject false DNS records into the cache) and buffer overflows (allowing remote code execution). The irony is that dnsmasq is also the tool most commonly used by attackers to run the DNS server in evil twin setups, making it simultaneously a target and a weapon.

Standard DNS queries are unencrypted, so anyone positioned on the path sees every domain a victim visits in real time, including the identity of HTTPS sites (whose content stays encrypted but whose destination does not). This is why DNS privacy matters independently of DNS integrity, and why DNS over HTTPS and DNS over TLS exist.
:::

%%%

---
unit: Attacks
code: SSL
title: SSL Stripping & HTTP Strict Transport Security (HSTS)
---
:::callout style=soft
**SSL stripping** downgrades a victim's HTTPS connection to HTTP without their knowledge, exposing credentials and session data in plaintext. **HSTS** was specifically designed to prevent this, but only for sites the browser has already seen or that are on the preload list.
:::

::::columns
::col::
:::steps heading="SSL Stripping Attack"
1. Victim types "bank.com" (no HTTPS prefix), browser sends HTTP GET
2. Attacker intercepts HTTP GET before it reaches the server
3. Attacker establishes HTTPS connection to real bank.com on victim's behalf
4. Attacker serves victim an HTTP version of the bank page
5. Victim enters credentials → sent over HTTP to attacker in plaintext
6. Attacker relays credentials to real bank → victim session appears normal
:::
::col::
:::steps heading="HSTS Protection"
1. Browser visits bank.com over HTTPS for the first time
2. Server responds with `Strict-Transport-Security: max-age=31536000; includeSubDomains`
3. Browser stores HSTS record for 1 year
4. On subsequent visits, browser sends HTTPS directly, skips HTTP entirely
5. SSL stripping cannot intercept, there is no HTTP request to intercept
6. **HSTS Preload**: Domains on chromium.org/hsts preload list are HSTS-enforced even on first visit
:::
::::

:::table
| Defense | Protects first visit? | Protects repeat visits? | Requires server support? |
|---------|----------------------|------------------------|--------------------------|
| HSTS | No (unless preloaded) | Yes | Yes |
| HSTS Preload | Yes | Yes | Yes + submission to preload list |
| VPN | Yes | Yes | No (client-side) |
| Certificate Pinning | Yes | Yes | Yes (app-level) |
:::

:::code language=mermaid caption="SSL stripping vs. HSTS: HSTS eliminates the HTTP first-request window that SSL stripping depends on, but only for domains the browser has an HSTS record for, which is why the HSTS preload list is critical"
flowchart TB
  subgraph S["SSL stripping"]
    direction LR
    V1["Victim browser"] -->|"HTTP, readable"| A1["Attacker"]
    A1 -->|"HTTPS"| W1["Real server"]
  end
  subgraph H["With HSTS"]
    direction LR
    V2["Browser remembers:<br/>this site is HTTPS only"] -->|"HTTPS straight away"| W2["Real server"]
    A2["Attacker cannot downgrade"] -.-x V2
  end
  S ~~~ H
:::

:::notes
SSL stripping is one of the most elegant and dangerous attacks in the wireless MITM toolkit because it exploits a gap between how HTTPS is theoretically supposed to work and how users and browsers actually initiate connections. The attack was first publicly demonstrated by Moxie Marlinspike at the Black Hat Security Conference in 2009, in a talk titled "New Tricks for Defeating SSL in Practice." The sslstrip tool released with the talk automated the attack and made it trivially reproducible.

The fundamental insight behind SSL stripping is that HTTPS cannot be enforced by the server alone if the client's initial request is sent via HTTP. When you type "bank.com" into a browser address bar without typing "https://", the browser sends an HTTP GET request. If a web server wants to force HTTPS, it responds to this HTTP request with a redirect to the HTTPS URL (HTTP 301 or 302). The browser then follows the redirect and establishes an HTTPS connection. The problem: the initial HTTP request and the HTTP redirect response are both unencrypted, and an attacker positioned in the middle can intercept both.

In the SSL stripping attack, the attacker intercepts the HTTP GET, establishes their own HTTPS connection to the real server, and then serves the victim an HTTP version of the page (removing all HTTPS links and converting them to HTTP). The victim's browser has never made an HTTPS connection, it has been talking to the attacker over HTTP the entire time, while the attacker has been talking to the real server over HTTPS. The victim's browser address bar shows "http://bank.com" rather than "https://bank.com," but many users do not notice this or do not know what to look for.

**HTTP Strict Transport Security (HSTS)**, defined in RFC 6797 (published 2012, three years after sslstrip was released), directly addresses this attack. HSTS allows a web server to instruct the browser to always use HTTPS for that domain for a specified duration (the `max-age` directive). After the browser receives an HSTS header, it will refuse to make HTTP connections to that domain and will automatically upgrade HTTP URLs to HTTPS before sending any request. Because the HTTP request is never sent, there is nothing for the attacker to intercept with SSL stripping.

However, HSTS has a critical limitation: the browser only has the HSTS record if it has previously visited the site over HTTPS and received the HSTS header. A first-time visitor, or a visitor using a fresh browser profile, has no HSTS record and is still vulnerable to SSL stripping. The **HSTS Preload List** (maintained at hstspreload.org by Google and incorporated into all major browsers) addresses this: domains that have been submitted to and accepted for the preload list are hardcoded into browser releases as HSTS domains, so they are protected even on the very first visit. As of 2024, the preload list contains over 130,000 domains. Submission requirements include serving HTTPS with a valid certificate, redirecting HTTP to HTTPS, serving an HSTS header with `max-age` of at least 1 year and the `preload` directive, and including `includeSubDomains`.

**Certificate pinning** is the strongest defense against SSL stripping and against certificate-based MITM attacks more broadly. An application (mobile app, browser with a pinned certificate extension, or native desktop app) that "pins" a specific certificate or public key will refuse to accept any other certificate for that domain, even if it is signed by a trusted certificate authority. This prevents an attacker from obtaining a fraudulent certificate for the target domain (or using a rogue CA certificate installed on the victim's device) to perform an HTTPS-level MITM. The downside of certificate pinning is operational: when the pinned certificate expires or is rotated, the app must be updated with the new pin, or it will fail to connect to the real server. High-profile certificate pinning failures (where apps broke because their pinned certificates were not updated in time) have led to some debate about whether pinning's security benefits outweigh its operational risks.

The HSTS preload list requirements are deliberately strict, because a domain is difficult to remove once added and would then be unreachable over HTTP for years. Checking whether a familiar domain is on the preload list shows which organizations have committed to HTTPS-only.
:::

%%%

---
unit: Tools
code: BTC
title: Tool Spotlight, Bettercap
---
:::callout style=soft
**Bettercap** is an open-source, modular penetration testing framework written in Go, designed for network reconnaissance, MITM attacks, and wireless attacks. It is widely used by both ethical hackers and adversaries for its ease of use and comprehensive feature set.
:::

::::columns
::col::
:::list heading="Key Bettercap Capabilities" style=plain
- **Wi-Fi reconnaissance**: Discovers SSIDs, BSSIDs, channels, encryption types, and associated clients in real time
- **Deauthentication**: Sends 802.11 deauth frames to force client disconnections
- **MITM**: ARP spoofing, DNS spoofing, HTTPS proxy with SSL stripping
- **Packet sniffing**: Captures credentials, cookies, and form data from HTTP traffic
- **BLE/Bluetooth**: Scans and interacts with Bluetooth Low Energy devices
- **HID attacks**: USB and wireless HID (keyboard/mouse) injection
:::
::col::
:::table
| Bettercap Module | Function | Threat Mapped To |
|-----------------|----------|-----------------|
| `wifi.recon` | Passive AP/client discovery | Reconnaissance (T1040) |
| `wifi.deauth` | Forced deauthentication | Denial of service / handshake capture |
| `arp.spoof` | ARP cache poisoning MITM | T1557.002 |
| `dns.spoof` | DNS response falsification | T1557 |
| `http.proxy` | HTTP/HTTPS MITM proxy | T1557 |
| `net.sniff` | Packet capture and credential logging | T1040 |
:::
::::

:::notes
Bettercap (bettercap.org) was created by Simone Margaritelli (evilsocket) as a complete rewrite of the earlier ettercap tool, with a focus on modularity, extensibility, and support for modern protocols. It is written in Go, making it efficient and easy to compile for multiple platforms including Linux, macOS, and Windows. It is included in Kali Linux, Parrot OS, and other penetration testing distributions.

From a defensive perspective, understanding Bettercap's capabilities is valuable for several reasons. First, it represents the current state of the art in accessible offensive wireless tooling, an attacker with basic Linux skills and an appropriate wireless adapter can conduct sophisticated multi-vector wireless attacks using Bettercap as a single integrated framework. Second, its modular architecture maps cleanly to the phases of an attack, helping security teams understand the sequence of techniques an attacker would use and identify the points in that sequence where detection or prevention controls could be most effective.

The **caplet** system is one of Bettercap's most powerful features. Caplets are scripting files (similar to shell scripts) that automate sequences of Bettercap commands, enabling attackers (and defenders in authorized testing) to execute complete attack chains with a single command. Pre-written caplets exist for common attack scenarios including evil twin with SSL stripping, credential harvesting, and WPA handshake capture. This automation significantly lowers the skill threshold required to execute sophisticated attacks.

From a detection perspective, Bettercap's wireless attacks produce several observable artifacts: deauthentication frames at above-normal rates (detectable by WIDS), duplicate SSIDs with different BSSIDs (detectable by WIDS), unusual DHCP server activity (if the organization monitors for unexpected DHCP servers), and ARP table inconsistencies (if the victim device has ARP monitoring enabled). Security teams should configure WIDS alerts for all of these indicators.

Bettercap is classified as a dual-use tool: it is widely used by authorized penetration testers and red team operators for legitimate security assessments, and is also used by malicious actors for attacks. This dual-use nature means it is unlikely to be flagged by antivirus software (it is not malware), and it is freely available without any access controls. The ethical and legal framework for its use, explicit written authorization from the asset owner before any testing, is absolute. The tool is described here purely for the purpose of understanding what defenders are up against.

**MITRE ATT&CK mappings** for Bettercap usage in a real attack scenario would include: TA0007 (Discovery), T1040 (Network Sniffing) for the recon phase; TA0006 (Credential Access), T1040 (Network Sniffing) for credential capture; TA0009 (Collection), T1557 (Adversary-in-the-Middle) for the MITM phase. Understanding the ATT&CK mapping helps security teams correlate tool-specific indicators with the broader kill chain.

:::

%%%

---
unit: Attacks
code: SNF
title: Packet Sniffing
---
:::callout style=soft
**Packet sniffing** is the process of intercepting and analyzing data packets as they traverse a network. In wireless environments, especially unencrypted or poorly secured ones, this technique allows attackers to capture sensitive information such as credentials, session tokens, and personal data.
:::

:::list heading="Sensitive Data Exposed via Sniffing on Unsecured Networks" style=plain
- HTTP requests revealing visited URLs and form data
- Plaintext usernames and passwords transmitted over protocols like Telnet, FTP, or HTTP
- Session cookies enabling session hijacking
- File transfers (e.g., via SMB or unencrypted FTP)
- Device identifiers and internal network structures
:::

::::columns
::col::
:::table
| Protocol | Encryption Status | Vulnerability to Sniffing |
|----------|-------------------|----------------------------|
| HTTP     | No                | High                       |
| HTTPS    | Yes (TLS)         | Low                        |
| FTP      | No                | High                       |
| SFTP     | Yes (SSH)         | Low                        |
| Telnet   | No                | High                       |
| SSH      | Yes               | Low                        |
:::
::col::
:::steps heading="Common Sniffing Tools Used by Attackers"
1. **Wireshark** – GUI-based analyzer for real-time packet inspection
2. **tcpdump** – Command-line utility for capturing traffic on Unix/Linux
3. **Airodump-ng** – Part of Aircrack-ng suite; captures 802.11 frames
4. **Kismet** – Wireless network detector and sniffer
5. **Ettercap** – Man-in-the-middle framework with sniffing capabilities
:::
::::

:::image src="images/07_packet_sniffing_protocols.png" alt="Network stack diagram showing protocols layered from physical to application; green lock icons on encrypted protocols (HTTPS, SFTP, SSH); red open padlock icons on unencrypted ones (HTTP, FTP, Telnet); sample Wireshark capture on the right showing plaintext 'USER admin' and 'PASS password123' visible in FTP stream" caption="Protocol encryption status: plaintext protocols transmit credentials and content in forms that any nearby network sniffer can trivially read" width=half
:::

:::notes
Packet sniffing represents one of the most fundamental and pervasive threats in wireless networks, particularly in open or poorly configured public Wi-Fi environments. At its core, sniffing involves capturing data packets as they are transmitted over a network medium. In wired networks, this typically requires physical access to the network segment, but in wireless networks, radio frequency propagation makes it inherently more susceptible to eavesdropping.

When an attacker gains access to a shared wireless medium, either through proximity, rogue access points (such as in evil twin attacks), or by exploiting weak authentication mechanisms, they can deploy packet capture tools to intercept all traffic within their reception range. This is especially effective in legacy or unencrypted protocols such as WEP or open networks where no encryption is applied at the data link layer.

The danger escalates when upper-layer protocols also lack encryption. For example, using HTTP instead of HTTPS, or Telnet instead of SSH, exposes application-layer data in plaintext. This allows attackers to extract login credentials, session identifiers, and other sensitive information directly from captured packets. The absence of end-to-end encryption renders even seemingly secure wireless implementations vulnerable.

Standards such as IEEE 802.11i (WPA2) and later WPA3 were developed to mitigate these risks by enforcing robust encryption at the link layer. However, vulnerabilities like KRACK (CVE-2017-13082) have demonstrated that even standardized encryption can be compromised under certain conditions. NIST Special Publication 800-48 emphasizes the importance of layered security, including the use of VPNs and end-to-end TLS, to defend against passive reconnaissance techniques like packet sniffing.

In academic and professional contexts, understanding how sniffing works is essential not only for red teams conducting penetration tests but also for blue teams designing secure communication architectures. It underscores the principle of defense in depth: relying solely on wireless encryption is insufficient if higher-layer protocols remain unsecured.

Packet sniffing in the wireless context has two distinct phases that are worth distinguishing. Passive sniffing involves placing a wireless adapter in "monitor mode", a special operating mode where the adapter captures all 802.11 frames in the vicinity regardless of whether they are addressed to it, and logging captured traffic to a file for later analysis. This is entirely non-interactive and leaves no trace on any network device. Active sniffing involves the attacker taking a more participatory role: injecting deauthentication frames to force clients to reconnect (capturing the WPA handshake during this process), replaying captured packets to extract information, or performing ARP poisoning on a local segment to redirect traffic through the attacker's machine.

Wireshark deserves special attention because it is simultaneously the most powerful legitimate network analysis tool available and one of the most commonly misused tools in offensive operations. Security professionals routinely use Wireshark to diagnose network issues, analyze protocol behavior, and debug applications. Its legitimacy means it is present in virtually every IT environment, and its power means it can extract extraordinary amounts of information from captured traffic. This dual-use nature is common in security tooling and reinforces why physical and link-layer security matter so much: once an attacker can see traffic, sophisticated application-layer analysis requires nothing more than standard sysadmin tools.

The encrypted vs. unencrypted protocol table has a practical takeaway for students beyond cybersecurity: in 2025, there is essentially no legitimate reason to use HTTP (rather than HTTPS), FTP (rather than SFTP), or Telnet (rather than SSH) for anything other than isolated testing environments. Any system you manage that still uses these protocols represents a security debt that should be tracked and remediated. The protocols themselves are not going away, legacy industrial systems, IoT devices, and old network equipment may be stuck on them, but the priority for encryption migration should be clear.
:::

%%%

---
unit: Tools
code: ACN
title: Tool Spotlight, Aircrack-ng Suite
---
:::callout style=soft
**Aircrack-ng** is the most widely used open-source suite for wireless network auditing and security testing. It includes tools for monitoring, attacking, testing, and cracking wireless networks, and is the standard toolkit for WPA/WPA2 password auditing.
:::

::::columns
::col::
:::list heading="Aircrack-ng Suite Components" style=plain
- **airmon-ng**: Puts wireless adapter into monitor mode; kills interfering processes
- **airodump-ng**: Passive capture of 802.11 frames; records BSSIDs, clients, and handshakes to PCAP files
- **aireplay-ng**: Active frame injection, deauthentication attacks, fake authentication, packet replay
- **aircrack-ng**: Dictionary and brute-force attack against captured WPA/WPA2 handshakes
- **airdecap-ng**: Decrypts WEP/WPA/WPA2 PCAP files using known keys
- **airbase-ng**: Creates a software access point for evil twin and man-in-the-middle scenarios
:::
::col::
:::steps heading="WPA2 Handshake Capture Workflow"
1. `airmon-ng start wlan0`, puts adapter in monitor mode (wlan0mon)
2. `airodump-ng wlan0mon`, lists all nearby APs with BSSIDs and channels
3. `airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon`, focuses capture on target AP, records to file
4. `aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF wlan0mon`, sends 5 deauth frames to force reconnection
5. Airodump-ng captures 4-way handshake (indicated by "WPA handshake" in display)
6. `aircrack-ng -w rockyou.txt capture-01.cap`, dictionary attack against captured handshake
:::
::::

:::notes
Aircrack-ng (aircrack-ng.org) is the de facto standard toolkit for wireless security auditing and has been continuously developed since 2006. It is included in Kali Linux, Parrot OS, and BlackArch, and is available for macOS and Windows as well. Understanding how Aircrack-ng works is essential for wireless security practitioners both because they may use it in authorized security assessments and because understanding its capabilities informs the design of defenses.

The suite's architecture reflects the phases of a wireless security assessment: the monitoring phase (airmon-ng, airodump-ng), the active testing phase (aireplay-ng), the analysis phase (aircrack-ng, airdecap-ng), and the assessment phase (airbase-ng for rogue AP testing). Each tool in the suite is designed to do one thing well, following the Unix philosophy of small, composable tools.

The **WPA2 handshake capture and crack workflow** is the most commonly discussed use of Aircrack-ng and illustrates a critical point about WPA2 security: **WPA2's cryptographic design is sound, but its security is entirely dependent on the strength of the network password**. When an attacker captures a WPA2 4-way handshake, they obtain a packet that contains enough information to verify whether a guessed password is correct. They can then run an offline dictionary attack, testing millions of candidate passwords per second on consumer GPU hardware, until they find the password or exhaust their wordlist.

The **rockyou.txt** wordlist referenced in step 6 of the workflow is a dataset of 14 million real passwords leaked in the 2009 RockYou.com breach. It is the standard starting point for password dictionary attacks and is included in Kali Linux. If a WPA2 network password appears anywhere in this list (or in common variations of its entries), it can typically be recovered in seconds to minutes. GPU-accelerated cracking tools like Hashcat can test WPA2 handshakes against the rockyou.txt list at approximately 1 million passwords per second on consumer hardware, substantially faster on dedicated cracking rigs.

This has a direct implication for network password policies: WPA2 passwords must be long (minimum 20 characters), random, and not based on dictionary words, names, or common patterns. A 20-character random alphanumeric password has approximately 10^35 combinations, infeasible to brute force with any current or foreseeable hardware. A 10-character password based on a word with letter substitutions (p@ssw0rd) can be cracked in seconds with modern tools and wordlists that include common substitution patterns.

**WPA3** resolves this by design: the SAE (Dragonfly) handshake does not produce a capturable handshake that can be subjected to offline dictionary attacks. Even if every frame of the SAE exchange is captured, the attacker cannot test password guesses against the capture without interacting with the live network. Rate-limiting at the AP (limiting how many SAE handshake attempts per minute are accepted from a given client) is therefore an effective defense.

**aireplay-ng** is also used in authorized penetration tests to test management frame protection. An AP with PMF (Protected Management Frames) enabled should be resilient to deauthentication attacks from unauthorized sources. Testing this with `aireplay-ng --deauth` in a controlled environment confirms that the PMF configuration is working as intended.

Recovering a WPA2 password offline depends on capturing the four-way handshake and testing candidate passwords against it. The attack's feasibility scales with password weakness, which is the direct argument for long, high-entropy pre-shared keys. This is a standard topic in wireless security certifications such as the OSWP.
:::

%%%

---
unit: Protocols
code: WPA
title: WPA2 vs WPA3
---
::::columns
::col::
:::table
| Feature | WPA2 | WPA3 |
|---|---|---|
| Encryption Standard | AES-CCMP (128-bit) | AES-CCMP (128-bit) + SAE (Simultaneous Authentication of Equals) |
| Key Exchange | 4-Way Handshake (PSK) | Simultaneous Authentication of Equals (SAE) |
| Forward Secrecy | No | Yes |
| Offline Password Cracking | Vulnerable (e.g., KRACK) | Resistant |
| Open Network Encryption | No | Yes ( Opportunistic Wireless Encryption - OWE ) |
| Management Frame Protection | Optional (WPA2-PMF) | Mandatory |
| Minimum Security Requirements | None beyond CCMP | Requires stronger cipher suites |
:::
::col::
:::callout
WPA3 introduces robust cryptographic improvements that address known vulnerabilities in WPA2, particularly around handshake integrity and password-based authentication.
:::
:::text
WPA3 strengthens Wi-Fi security through the use of the **Simultaneous Authentication of Equals (SAE)** protocol, which replaces the Pre-Shared Key (PSK) method used in WPA2. SAE is based on the Dragonfly key exchange and provides resistance to offline dictionary attacks, a critical vulnerability exploited in attacks like KRACK (CVE-2017-13082).
:::
::::

:::image src="images/07_wpa2_vs_wpa3_handshake.png" alt="Two-column technical diagram: left column shows WPA2 4-way handshake (ANonce, SNonce, MIC exchange steps) with a red annotation showing where KRACK intercepts nonce reuse; right column shows WPA3 SAE Dragonfly handshake with green annotations showing forward secrecy property and per-session key derivation" caption="WPA2 4-way handshake vs. WPA3 SAE: the KRACK vulnerability exploited nonce reuse in WPA2's handshake, WPA3's Dragonfly protocol derives independent session keys that cannot be pre-computed from captured traffic" width=full
:::

:::flow
WPA2 PSK Authentication:
Client broadcasts probe request and association request
AP sends ANonce (random value)
Client generates SNonce and PTK (Pairwise Transient Key) from ANonce + password
Client sends SNonce + MIC for integrity check
AP verifies MIC, derives PTK, installs key
>>> VULNERABILITY: Replayed messages can force key reinstallation (KRACK)

WPA3 SAE Authentication:
Both client and AP generate random secret values independently
Dragonfly commit exchange: both parties exchange blinded commitments
Confirmation exchange verifies both parties derived same session key
Each session produces unique key regardless of long-term credentials
>>> Forward secrecy: capturing handshake cannot decrypt past or future sessions
:::

:::notes
The transition from WPA2 to WPA3 represents a significant evolution in wireless local area network (WLAN) security, driven by the need to address persistent vulnerabilities and evolving threat landscapes. WPA2, introduced in 2004 and standardized under IEEE 802.11i, has long been the backbone of Wi-Fi security, utilizing the Advanced Encryption Standard (AES) with Counter Mode Cipher Block Chaining Message Authentication Code Protocol (CCMP) for data encryption and integrity.

However, WPA2's four-way handshake mechanism, which establishes temporal keys between clients and access points, was found to be vulnerable to key reinstallation attacks (KRACK), disclosed in 2017 (CVE-2017-13077 through CVE-2017-13082). These vulnerabilities allowed adversaries within radio range to decrypt packets, force nonce reuse, or even inject malicious traffic.

WPA3, certified by the Wi-Fi Alliance starting in 2018, addresses these shortcomings through several enhancements. It replaces the PSK-based handshake with **Simultaneous Authentication of Equals (SAE)**, also known as the Dragonfly protocol. SAE provides forward secrecy and resistance to offline dictionary attacks by ensuring that each session derives unique keys, even when using weak passwords.

Additionally, WPA3 introduces **Opportunistic Wireless Encryption (OWE)** for open networks, applying per-client encryption without requiring authentication, preventing passive eavesdropping on public hotspots. It also mandates **Protected Management Frames (PMF)** to prevent denial-of-service and frame injection attacks.

From a compliance perspective, NIST SP 800-48 and SP 800-153 recommend transitioning away from legacy protocols like WPA2 to mitigate risks associated with known exploits. As such, WPA3 aligns more closely with modern cryptographic best practices and regulatory expectations.

The KRACK vulnerability (Key Reinstallation Attack) disclosed by Mathy Vanhoef in October 2017 is one of the most significant wireless security findings of the last decade, and understanding it technically is important for appreciating what WPA3 fixed. The WPA2 four-way handshake is designed to be robust against packet loss in noisy wireless environments, if a packet is dropped, the handshake retransmits. Vanhoef discovered that an attacker positioned between the client and AP could replay the third message of the handshake (which contains the encryption key), causing the client to reinstall an already-in-use key and reset its nonce counter to zero. In cryptographic terms, this is catastrophic: nonce reuse in counter mode (CTR-mode) ciphers like AES-CCMP allows attackers to XOR captured ciphertexts to extract keystream material and decrypt previously captured packets.

The attack affected virtually every WPA2 implementation in existence and could not be fixed with a simple patch to the AP, client devices also needed patching because the flaw was in the client-side key reinstallation logic. This created a long tail of vulnerable devices: while Windows and major Linux distributions were patched within weeks, legacy Android devices, IoT hardware, and embedded systems remained vulnerable for years.

WPA3's SAE protocol eliminates this class of vulnerability by fundamentally redesigning the authentication exchange. Unlike WPA2's PSK handshake (where the shared password is directly used in key derivation), SAE uses a zero-knowledge proof protocol where both parties prove knowledge of the password without transmitting anything that could be used to verify a guessed password offline. Even if every frame of the SAE exchange is captured, an attacker cannot mount an offline dictionary attack against the captured handshake, they must interact with the live system to test guesses, making rate-limiting at the AP an effective defense.

The property of forward secrecy, that compromise of long-term credentials does not decrypt previously captured sessions, is the other major improvement. WPA2 with a captured 4-way handshake is permanently vulnerable to dictionary attacks if the network password is ever discovered. WPA3 sessions produce ephemeral keys that exist only for the duration of that session; even if the Wi-Fi password is later compromised, previously captured sessions cannot be decrypted retroactively.
:::

%%%

---
unit: Protocols
code: KRK
title: Case Study, KRACK Attack (CVE-2017-13077)
---
:::callout style=soft
On October 16, 2017, security researcher Mathy Vanhoef published "Key Reinstallation Attacks: Forcing Nonce Reuse in WPA2." The coordinated disclosure affected virtually every WPA2-enabled device on the planet and triggered an emergency patching response across the entire industry.
:::

::::columns
::col::
:::list heading="KRACK Attack Timeline" style=plain
- **May 2017**: Vanhoef discovers key reinstallation vulnerability in WPA2 handshake
- **August 2017**: Vulnerability disclosed to CERT/CC; coordinated disclosure process begins
- **October 16, 2017**: Public disclosure at CCS 2017; CVEs 2017-13077 through 13087 assigned
- **October 16, 2017**: Microsoft, Apple, Linux, Google simultaneously release patches
- **Ongoing (2018–2021)**: IoT devices and legacy Android remain unpatched; extended attack window
:::
::col::
:::list heading="What KRACK Actually Allowed Attackers to Do" style=plain
- **Decrypt WPA2-encrypted packets**: In CCMP mode, nonce reuse enables XOR-based decryption
- **Replay old packets**: Inject previously captured network traffic
- **Forge TKIP packets**: With TKIP (WPA/WPA2-TKIP), full packet forgery and injection was possible
- **Intercept TCP connections**: With sufficient packet decryption, HTTP traffic fully exposed
- **What it could NOT do**: Break AES-CCMP directly; the flaw was in key management, not the cipher
:::
::::

:::code language=mermaid caption="KRACK nonce reuse: by replaying the third message of the WPA2 handshake, the attacker forces the client to reinstall an already-in-use key, resetting the nonce counter and enabling XOR-based decryption of all subsequent traffic"
sequenceDiagram
  participant C as Client
  participant A as Attacker in the middle
  participant AP as Access point
  AP->>C: Message 1
  C->>AP: Message 2
  AP->>A: Message 3 (install key)
  A->>C: Message 3 replayed
  C->>C: Reinstalls the same key, nonce reset to zero
  Note over C,AP: Reused nonces let traffic be decrypted. Fix: patched clients and APs
:::

:::notes
The KRACK (Key Reinstallation Attack) disclosure is a landmark event in wireless security history, not only because of the technical severity of the vulnerability, but because of what it reveals about the security of widely deployed standards and the challenges of coordinated vulnerability disclosure at massive scale.

Mathy Vanhoef, then a PhD student at KU Leuven in Belgium, discovered the vulnerability in May 2017 while analyzing the formal specification of the WPA2 handshake. The insight was subtle: the 802.11 standard requires that if message 3 of the 4-way handshake is not acknowledged by the client, the AP retransmits it. This retransmission mechanism (designed for reliability in lossy wireless environments) could be exploited: an attacker could block the client's acknowledgment of message 3, force the AP to retransmit it, and replay the retransmission to the client. When the client receives message 3 a second time, it reinstalls the already-negotiated encryption key, and critically, also resets the nonce (a number-used-once) counter to zero.

The catastrophic consequence: the client now encrypts traffic using a key and nonce combination that was already used. In AES-CCMP mode (the standard encryption mode for WPA2), this is a violation of a fundamental cryptographic invariant, counter mode cipher security requires that (key, nonce) pairs are never reused. When the same (key, nonce) pair is used to encrypt two different messages, an attacker can XOR the two ciphertexts to cancel the keystream, obtaining the XOR of the two plaintexts. With knowledge of one plaintext (e.g., by inducing the victim to visit a known HTTP URL), the attacker can recover the other plaintext entirely.

The coordinated disclosure process for KRACK is instructive. Vanhoef disclosed to CERT/CC in late July 2017. CERT/CC coordinated with over 100 vendors (including Apple, Microsoft, Google, Cisco, Juniper, Samsung, and the Linux kernel team) simultaneously. All major platforms released patches on the same day the vulnerability went public (October 16, 2017), an extraordinary feat of logistics. This same-day patch release is the gold standard for coordinated disclosure and was possible because Vanhoef and CERT/CC gave vendors nearly three months of advance notice.

The patch itself was straightforward: client implementations should not reinstall a key if they receive message 3 with a nonce that has already been installed. Access points also needed to be patched to prevent an attacker from exploiting the AP's role in certain variations of the attack. The fix was a one-line change in many implementations, but deploying that fix to billions of devices was the real challenge.

The **long tail of unpatched devices** is the most significant ongoing consequence of KRACK. Major platform vendors patched quickly, but IoT devices (smart thermostats, IP cameras, industrial controllers, medical devices), older Android devices (whose manufacturers ceased providing security updates), and embedded systems running Linux without active maintenance remained vulnerable for years. The practical attack risk against patched devices dropped to near zero within weeks; the risk against unpatched devices persisted far longer.

**Dragonblood (2019)**: Shortly after WPA3 was released, Vanhoef (now a professor at NYU Abu Dhabi) and Ronen published "Dragonblood: Analyzing the Dragonfly Handshake of WPA3-SAE," disclosing several vulnerabilities in WPA3-SAE implementations (CVE-2019-9494 and related CVEs). These were implementation vulnerabilities (cache and timing side-channels in the SAE computation) rather than fundamental design flaws, and they were patched relatively quickly. However, they demonstrate that even well-designed protocols can have implementation-level vulnerabilities, and that formal analysis of protocol specifications (which WPA3-SAE has undergone more rigorously than WPA2) does not guarantee implementation correctness.

Vanhoef's original KRACK paper, "Key Reinstallation Attacks: Forcing Nonce Reuse in WPA2" (CCS 2017), is available at krackattacks.com and is accessible to advanced undergraduates as supplementary reading.
:::

%%%

---
unit: Protocols
code: OWE
title: Opportunistic Wireless Encryption (OWE), Encrypting Open Networks
---
:::callout style=soft
**OWE (Opportunistic Wireless Encryption)**, defined in RFC 8110 and mandated in WPA3 for open networks, provides per-client data encryption on networks with no authentication, protecting users from passive eavesdropping even on "open" public Wi-Fi.
:::

::::columns
::col::
:::steps heading="How OWE Works"
1. Client sends association request with a Diffie-Hellman public key in the OWE IE (Information Element)
2. AP responds with its own DH public key and a confirmation
3. Both parties independently compute the same shared secret using ECDH (Elliptic Curve Diffie-Hellman)
4. Shared secret is used to derive a PMK (Pairwise Master Key) for the session
5. Standard 4-way handshake completes, establishing a unique PTK for the client's session
6. All traffic between this client and the AP is now encrypted, unique per client, per session
:::
::col::
:::list heading="OWE vs. Traditional Open Networks" style=plain
- **Traditional open**: No encryption at all; any device in monitor mode can read all traffic
- **OWE**: Per-client encryption; traffic from other clients is unreadable even on the same AP
- **OWE limitation**: No authentication, user cannot verify they are connected to the right AP; still vulnerable to evil twin attacks
- **OWE + certificate/802.1X**: Full protection, but no longer "open" in the user-experience sense
:::
:::callout style=line
OWE is defined in **RFC 8110** (March 2017) and branded as "Enhanced Open" by the Wi-Fi Alliance. It requires WPA3 certification for access points and client devices.
:::
::::

:::code language=mermaid caption="OWE per-client encryption: each client derives a unique session key via ECDH, so even on the same open AP, one client cannot decrypt another's traffic, OWE closes the passive eavesdropping vulnerability of traditional open networks"
sequenceDiagram
  participant C as Client
  participant AP as Access point
  C->>AP: Association request with DH public key
  AP-->>C: Association response with DH public key
  Note over C,AP: Both compute the same shared secret (ECDH)
  Note over C,AP: Shared secret becomes the PMK
  C->>AP: 4-way handshake, unique per-client keys
  Note over C,AP: Open network, but traffic is encrypted
:::

:::notes
Opportunistic Wireless Encryption addresses a long-standing gap in wireless security: open networks (those requiring no password) have always transmitted all data completely unencrypted. Any device in monitor mode on the same channel could passively capture every byte of traffic from every device on the network. This has been a fundamental property of open Wi-Fi since the original 802.11 standard in 1997.

OWE changes this while preserving the user experience of an "open" network, the user does not need to enter a password or configure any credentials. The encryption happens automatically as part of the association process, transparently to the user. From the user's perspective, connecting to an OWE-enabled network looks exactly like connecting to a traditional open network; from a security perspective, their traffic is now encrypted.

The technical mechanism is elegant: during the association process (before any user credentials or traffic are exchanged), the client and AP perform an **Elliptic Curve Diffie-Hellman (ECDH)** key exchange. Each party generates an ephemeral key pair; the public keys are exchanged in 802.11 management frame Information Elements; each party independently computes the same shared secret from their own private key and the other party's public key, a property unique to DH-family protocols. This shared secret is used to derive a session key unique to this client-AP pair.

The key security properties OWE provides: **confidentiality** (traffic is encrypted, preventing passive eavesdropping from other devices on the network or nearby), **uniqueness** (each client-session pair has its own encryption key, so clients cannot decrypt each other's traffic even on the same AP), and **forward secrecy** (ephemeral key pairs mean captured traffic cannot be decrypted even if the AP's long-term identity is later compromised).

What OWE does **not** provide: **authentication**. OWE does not give the client any way to verify that the AP they are connecting to is the legitimate venue AP rather than an attacker's evil twin. This is the fundamental trade-off of "opportunistic" security, the term "opportunistic" in IETF parlance specifically means "encryption when possible, without authentication." An evil twin AP that implements OWE will encrypt traffic between the client and the attacker's device, protecting the connection from third-party eavesdroppers, but providing no protection against the attacker itself.

For the full protection required in sensitive environments, OWE should be layered with additional authentication mechanisms: 802.1X/RADIUS for enterprise environments, or a client-side VPN that provides authenticated end-to-end encryption. Many enterprise networks use OWE as the link-layer encryption for guest networks, combined with a captive portal that requires authentication before internet access is granted.

Wi-Fi 6E (802.11ax) and Wi-Fi 7 (802.11be) mandate OWE for all open networks operating in the 6 GHz band. This means any network operating in the 6 GHz band without authentication must use OWE, traditional open networks are prohibited in the 6 GHz space.

Opportunistic Wireless Encryption (OWE) applies the IETF's opportunistic security principle from RFC 7435: encryption without authentication is better than no encryption at all, even though it does not stop an active attacker. The trade-off between deployability, which requires no user action, and completeness, which would require credential management, recurs throughout security standardization.
:::

%%%

---
unit: Protocols
code: RAD
title: 802.1X and RADIUS, Enterprise Wireless Authentication
---
:::callout style=soft
**802.1X** is the IEEE standard for port-based network access control. In wireless networks, it provides a framework for strong, certificate-based authentication, preventing both unauthorized clients from joining the network and unauthorized access points from completing the authentication handshake.
:::

::::columns
::col::
:::list heading="802.1X Architecture Components" style=plain
- **Supplicant**: The client device seeking network access (laptop, phone, IoT device)
- **Authenticator**: The access point, forwards authentication exchanges between supplicant and server
- **Authentication Server**: A RADIUS server (typically FreeRADIUS, Cisco ISE, or Microsoft NPS) that validates credentials
- **EAP**: Extensible Authentication Protocol, the authentication framework carried over 802.1X
- **Common EAP methods**: EAP-TLS (certificate-based, strongest), PEAP-MSCHAPv2 (username/password, common), EAP-TTLS/PAP
:::
::col::
:::steps heading="802.1X Authentication Flow"
1. Client associates with AP (no traffic allowed yet, AP port is blocked)
2. AP sends EAP-Request/Identity to client
3. Client responds with EAP-Response/Identity (username or certificate)
4. AP forwards to RADIUS server via RADIUS Access-Request
5. RADIUS and client negotiate EAP method (e.g., EAP-TLS with mutual cert validation)
6. RADIUS sends Access-Accept with session keys → AP opens port → client gets network access
:::
::::

:::code language=mermaid caption="802.1X/RADIUS authentication flow: the AP acts as a gatekeeper, allowing no traffic until the RADIUS server has validated the client's identity, an evil twin AP cannot complete this handshake because it has no access to the RADIUS server"
sequenceDiagram
  participant S as Supplicant (laptop)
  participant A as Authenticator (AP)
  participant R as RADIUS server
  S->>A: 1 Connect
  A->>S: 2 EAP identity request
  S->>A: 3 Identity
  A->>R: 4 Forward identity
  R-->>S: 5 TLS tunnel set up, credentials checked
  R->>A: 6 Access-Accept with keying material
  A-->>S: 7 4-way handshake, network access
:::

:::notes
802.1X port-based network access control is the enterprise solution to the authentication gap that evil twin attacks exploit. Recall that a standard WPA2-PSK network has no way to verify that a connecting AP is legitimate, the protocol only verifies that the client knows the shared password. An evil twin that knows the network's PSK (e.g., because the attacker attended the company's visitor registration process) can successfully impersonate the network for WPA2-PSK clients.

802.1X fundamentally changes the authentication model. Instead of a shared secret, authentication is performed between the client and a centralized RADIUS (Remote Authentication Dial-In User Service) server, mediated by the AP. The AP itself does not need to know the client's credentials, it simply forwards the EAP exchange between the client and the RADIUS server. This has a critical security consequence: **an evil twin AP cannot complete 802.1X authentication** because it has no access to the organization's RADIUS server. The client's supplicant will attempt to authenticate with the RADIUS server through the evil twin AP; the evil twin cannot relay this to the real RADIUS server (because the RADIUS server will not accept connections from the unauthorized AP's IP address and does not have the AP's shared RADIUS secret). The authentication will fail, and the client will not connect.

The strongest EAP method for wireless authentication is **EAP-TLS**, which requires both the client and the RADIUS server to present X.509 certificates for mutual authentication. In EAP-TLS, the client validates that the RADIUS server's certificate is signed by a trusted CA (protecting against rogue RADIUS servers), and the RADIUS server validates that the client's certificate is signed by a trusted CA and has not been revoked (protecting against unauthorized clients). EAP-TLS is recommended by NIST SP 800-97 ("Establishing Wireless Robust Security Networks") for environments requiring the highest assurance.

**PEAP-MSCHAPv2** (Protected EAP with Microsoft Challenge-Handshake Authentication Protocol version 2) is the most commonly deployed EAP method in corporate Windows environments because it integrates with Active Directory and does not require client certificates. It encapsulates MSCHAPv2 inside a TLS tunnel established between the client and the RADIUS server. A critical security consideration: if clients are not configured to validate the RADIUS server's certificate (which is unfortunately a common misconfiguration), an attacker can run a rogue RADIUS server that accepts the MSCHAPv2 exchange from the client, and because MSCHAPv2's response is deterministically derived from the password and a challenge, it can be cracked offline. Tools like asleap (available in the Aircrack-ng project) automate this attack. The defense is simple: configure clients to validate the RADIUS server certificate against a known CA and known server name.

NIST SP 800-153 ("Guidelines for Securing Wireless Local Area Networks") recommends 802.1X with EAP-TLS as the preferred authentication mechanism for enterprise wireless networks. NIST SP 800-97 provides detailed configuration guidance. ISO/IEC 27001 Annex A.9.1.2 (access to networks and network services) and A.13.1.1 (network controls) both support the use of strong network access control mechanisms.

Corporate and university Wi-Fi commonly uses WPA2-Enterprise (802.1X) rather than a shared password. EAP-TLS, the strongest option, requires a PKI to issue and manage client certificates, a significant operational investment; this is why PEAP-MSCHAPv2, which integrates with existing directories without a full PKI, is more common despite being weaker.
:::

%%%

---
unit: Protocols
code: SAE
title: SAE Deep Dive, The Dragonfly Key Exchange
---
:::callout style=soft
**SAE (Simultaneous Authentication of Equals)**, also known as the Dragonfly key exchange, is the core cryptographic innovation in WPA3-Personal. It replaces WPA2's PSK-based 4-way handshake with a zero-knowledge proof protocol that eliminates offline dictionary attacks.
:::

::::columns
::col::
:::steps heading="SAE Dragonfly Handshake"
1. **Password Encoding**: Both client and AP independently map the shared password to a point on an elliptic curve (the "hunting and pecking" or SSWU algorithm), this step produces the Password Element (PE)
2. **Commit Exchange**: Each party generates a random scalar and element; computes a "commit" value combining their random values with PE; exchanges commit values
3. **Commitment Verification**: Each party can verify the other's commit only if they know the password (zero-knowledge property)
4. **Confirm Exchange**: Each party computes and exchanges a confirmation value derived from both commits
5. **Key Derivation**: Both parties derive the same PMK (Pairwise Master Key) from the exchange, this becomes the session key
6. **Result**: Unique PMK per session; no information about the password is transmitted; no handshake to crack offline
:::
::col::
:::list heading="SAE Security Properties" style=plain
- **No offline cracking**: Captured SAE exchanges cannot be tested against a wordlist
- **Forward secrecy**: Ephemeral values per session; past sessions safe if password is later compromised
- **Simultaneous authentication**: Neither party is "authenticator" vs "supplicant", mutual proof of knowledge
- **Small subgroup attacks prevented**: Elliptic curve group validation prevents mathematical attacks
- **Side-channel mitigations**: Dragonblood vulnerabilities (CVE-2019-9494) led to constant-time implementation requirements
:::
::::

:::code language=mermaid caption="SAE Dragonfly key exchange: both parties independently prove knowledge of the password via elliptic curve operations, an intercepted exchange reveals nothing that would allow offline password verification"
sequenceDiagram
  participant C as Client
  participant AP as Access point
  Note over C,AP: Shared password mapped to a Password Element (hash-to-curve)
  C->>AP: Commit: scalar and element from random secret
  AP->>C: Commit: scalar and element from random secret
  Note over C,AP: Each side derives the same key without sending the password
  C->>AP: Confirm
  AP->>C: Confirm
  Note over C,AP: Offline guessing impossible, forward secrecy
:::

:::notes
The Simultaneous Authentication of Equals (SAE) protocol is the most important cryptographic innovation in WPA3, and understanding how it works technically provides insight into both its security guarantees and its limitations. SAE was designed by Dan Harkins, who has also designed several other security protocols for the IETF, and is based on the Dragonfly key exchange defined in RFC 7664.

The fundamental problem SAE solves is this: WPA2's PSK handshake (the 4-way handshake) produces a protocol exchange from which a verifier can determine whether a guessed password is correct without interacting with the live network. Specifically, the WPA2 handshake involves the client computing a MIC (Message Integrity Code) that is a function of the password and the handshake parameters. Anyone who captures the handshake can compute the MIC for guessed passwords and compare, this is the offline dictionary attack that makes weak WPA2 passwords catastrophically insecure.

SAE prevents this by ensuring that the handshake exchange is a **zero-knowledge proof of password knowledge**: both parties can verify that the other knows the password, but the exchange does not produce any value that a passive observer could use to test whether a guessed password is correct without interacting with a live peer.

The mechanism relies on **elliptic curve cryptography**. Both the client and AP independently hash the password to a point on an elliptic curve, the "Password Element" (PE). This mapping is designed to be deterministic (both parties with the same password get the same PE) but not invertible (given PE, you cannot recover the password, it is a one-way hash). Each party then generates random ephemeral values (scalars and elliptic curve points), performs elliptic curve operations combining their ephemeral values with PE, and exchanges the results. The mathematics of the elliptic curve group ensure that only parties who know the password (and therefore have the correct PE) can compute the same PMK at the end of the exchange. A passive observer who captures the exchange but does not know the password cannot compute PE, and therefore cannot derive the PMK or verify guesses.

**The Dragonblood vulnerabilities (CVE-2019-9494)** disclosed by Vanhoef and Ronen in April 2019 were timing and cache side-channel attacks against the "hunting and pecking" algorithm used in the original SAE specification to map the password to the Password Element. The algorithm involved a variable number of iterations depending on the password and group parameters, creating a timing variation that leaked information about the password's PE generation. With sufficient timing measurements, an attacker could determine whether a guessed password mapped to PE in the same number of iterations as the real password, enabling a form of online dictionary attack. The fix was to use a constant-time algorithm (the SSWU map, Simplified Shallue-Woestijne-Ulas) that takes the same amount of time regardless of the password, this was incorporated into the 802.11 standard as an amendment.

**SAE-PK** (SAE with Public Key Authentication), introduced in Wi-Fi 6 (802.11ax), extends SAE to provide mutual authentication: the AP signs its SAE commitment with a private key whose corresponding public key is printed on a label on the AP. This prevents an evil twin from completing SAE authentication because it cannot produce a valid signature without the physical AP's private key. SAE-PK is optional and not yet widely deployed, but it represents the next step in closing the remaining authentication gap in WPA3-Personal.

SAE (the handshake in WPA3) lets both sides prove they know the password without transmitting it. Each party's computation can only produce the same shared result if both started from the same password element, so a matching result proves shared knowledge of the password while neither the password nor that element is ever sent. The Quisquater-Guillou cave analogy makes this zero-knowledge property concrete.
:::

%%%

---
unit: Defense
code: VPN
title: VPNs, Encrypting Your Own Traffic
---
:::callout style=soft
A **VPN (Virtual Private Network)** encrypts your traffic in a secure tunnel between your device and a trusted server, regardless of how trustworthy the Wi-Fi network itself is.
:::

:::flow
Your device
Encrypted tunnel (TLS/IPsec/WireGuard)
VPN server (trusted endpoint)
Destination website
:::

:::image src="images/07_vpn_tunnel_diagram.png" alt="Network path diagram showing a user's laptop on the left connecting through a public Wi-Fi cloud labeled 'Untrusted Network'; a green encrypted pipe runs through this cloud to a VPN server on the right; from the VPN server, a standard connection goes to the destination website; an attacker device inside the 'Untrusted Network' cloud shows a red X indicating inability to read the encrypted tunnel contents" caption="VPN tunnel architecture: the encrypted tunnel ensures that even if the wireless network is compromised, the attacker sees only ciphertext and cannot read the user's traffic" width=full
:::

:::notes
Here's the defense that works even if every other protection on the
network has already failed: a VPN. It builds an encrypted tunnel from
your device to a server you trust, and everything traveling through that
tunnel is unreadable to anyone sniffing the Wi-Fi in between, including
on an evil twin.

It doesn't make the public network itself safe. It makes it not matter,
because your traffic is protected before it ever touches that risky
network.

To understand exactly why a VPN provides this protection, it is necessary to understand what it does at the protocol level. A VPN client on the user's device establishes a cryptographically authenticated and encrypted connection to a VPN server before any application traffic is sent. All network packets from the device, whether to a web server, an email server, or a DNS resolver, are encapsulated inside this encrypted tunnel and forwarded to the VPN server, which then forwards them to their actual destinations on the user's behalf. From the perspective of anyone monitoring the local network (including an attacker who controls the Wi-Fi access point), all they see is an encrypted stream of data flowing from the user's device to the VPN server's IP address. The content, destination, and nature of the traffic is entirely hidden.

This property, that the VPN protects traffic regardless of the underlying network's trustworthiness, is precisely what makes VPNs the correct defense against the entire class of wireless eavesdropping and MITM threats discussed in this lecture. An evil twin AP can intercept all traffic from a connected device, but if that traffic is already encrypted by a VPN, the attacker captures only ciphertext that provides no actionable intelligence.

Three primary VPN protocols are in common use, each with distinct security and performance characteristics:

**OpenVPN** is a mature, open-source protocol based on TLS/SSL. It uses standard TLS for the control channel and can be configured with strong cipher suites. It is highly configurable and audited but has somewhat higher latency and lower throughput than modern alternatives.

**IKEv2/IPsec** is widely used in enterprise environments and natively supported by iOS and Windows. It offers fast reconnection (important for mobile devices that frequently switch networks) and strong security when configured with modern ciphers.

**WireGuard** is the newest major VPN protocol, designed with a minimal codebase (~4,000 lines vs. OpenVPN's ~70,000) for easier security auditing. It uses state-of-the-art cryptography (ChaCha20, Poly1305, Curve25519) and is now integrated into the Linux kernel. It offers the best performance of the three and has been independently audited.

A VPN shifts trust from the local network to the VPN provider. If the VPN provider itself is malicious, compromised, or operates under a jurisdiction that compels data disclosure, it may undermine the privacy protection the VPN was intended to provide. For security-conscious use, organizations should operate their own VPN infrastructure rather than relying on commercial VPN services of unknown trustworthiness.
:::

%%%

---
unit: Defense
code: VPC
title: VPN Protocol Comparison, OpenVPN vs IKEv2 vs WireGuard
---
:::callout style=soft
Choosing the right VPN protocol involves trade-offs between security strength, performance, platform support, and operational complexity. All three major protocols are cryptographically sound when properly configured, the differences lie in their architecture and practical characteristics.
:::

:::table
| Attribute | OpenVPN | IKEv2/IPsec | WireGuard |
|-----------|---------|-------------|-----------|
| Year introduced | 2001 | 2005 | 2019 |
| Code size | ~70,000 lines | Varies by implementation | ~4,000 lines |
| Key exchange | TLS (RSA/ECDH) | IKEv2 with ECDH | Noise protocol (Curve25519) |
| Data encryption | AES-256-GCM (configurable) | AES-256-GCM or ChaCha20 | ChaCha20-Poly1305 |
| Forward secrecy | Yes (ECDHE) | Yes (ECDHE) | Yes (ephemeral keys) |
| Platform support | All platforms | iOS, Windows, Android native | Linux kernel; all via apps |
| Reconnection speed | Slower | Fast (MOBIKE protocol) | Very fast |
| UDP port | Custom (default 1194) | UDP 500/4500 | Custom |
| Firewall traversal | Excellent (TCP mode) | Moderate | Good |
| Audit status | Multiple audits | Widely deployed, spec audited | Independent audit (2019) |
:::

:::image src="images/07_vpn_protocol_comparison.png" alt="Radar chart comparing OpenVPN, IKEv2, and WireGuard across five dimensions: Security, Performance, Ease of Setup, Platform Support, and Firewall Traversal; WireGuard scores highest on Performance and Ease of Setup; IKEv2 highest on Platform Support; OpenVPN highest on Firewall Traversal; all three comparable on Security" caption="VPN protocol comparison radar: WireGuard excels in performance and simplicity; IKEv2 in native platform support; OpenVPN in firewall traversal flexibility, the 'best' protocol depends on deployment context" width=full
:::

:::notes
The three major VPN protocols in active use today, OpenVPN, IKEv2/IPsec, and WireGuard, each represent a different design philosophy and generation of thinking about how to build secure tunneling protocols.

**OpenVPN** was created in 2001 by James Yonan as an open-source alternative to proprietary VPN solutions. Its design decision to build on top of TLS (the same protocol used for HTTPS) was pragmatic: TLS was already well-analyzed, widely implemented, and its use over TCP port 443 makes OpenVPN traffic indistinguishable from HTTPS, giving it excellent firewall traversal properties. The downside of building on TLS is complexity: OpenVPN's codebase is large (~70,000 lines), and its configuration has many options that must be set correctly for maximum security (cipher suite selection, authentication method, certificate validation). The OpenVPN project underwent a professional security audit by Ostif/Quarkslab in 2017, which found several vulnerabilities that were promptly patched.

**IKEv2/IPsec** (Internet Key Exchange version 2 / IP Security) is a standardized IETF protocol suite defined in RFC 7296 (IKEv2) and the broader IPsec framework. It is natively supported by Windows, iOS, Android, and macOS without additional software, making it particularly attractive for enterprise deployment where software installation on managed devices is straightforward but third-party apps may be restricted. The MOBIKE extension (RFC 4555) enables fast reconnection when the client's IP address changes (e.g., switching from Wi-Fi to cellular), making IKEv2 the preferred choice for mobile devices. In enterprise deployments, IKEv2 is typically paired with EAP authentication for user identity verification.

**WireGuard** is the newest of the three and represents a fundamental rethinking of VPN protocol design. Its creator, Jason Donenfeld, built it with the explicit goal of being small enough to be formally verified and security-audited easily. At approximately 4,000 lines of C code (compared to OpenVPN's ~70,000 and strongSwan/IKEv2's ~300,000+), WireGuard's codebase is so small it was merged into the Linux kernel mainline in kernel 5.6 (March 2020) after review by Linus Torvalds. Its cryptography is fixed: ChaCha20 for encryption, Poly1305 for authentication, Curve25519 for key exchange, BLAKE2s for hashing, there is no cipher negotiation and therefore no downgrade attack surface. An independent security audit by Trail of Bits in 2019 found no critical vulnerabilities.

The **trust model** of VPNs deserves additional discussion. Using a VPN shifts trust from the local network to the VPN endpoint and the VPN provider. For enterprise VPNs where the organization controls both the client and the server, this trust shift is appropriate and well-controlled. For commercial VPN services ("VPN for privacy"), the user must trust the VPN provider not to log, sell, or disclose their traffic, a trust assumption that requires careful evaluation of the provider's jurisdiction, business model, and track record. Providers in 5-Eyes jurisdictions (US, UK, Canada, Australia, New Zealand) are subject to compelled disclosure laws. "No-log" VPN claims have been tested in practice when providers were served with legal demands; some providers who claimed no-log policies were found to have logs when their servers were seized by law enforcement.

NIST SP 800-77 Rev. 1 ("Guide to IPsec VPNs") provides detailed guidance on configuring and deploying IPsec VPNs in federal environments. It specifies minimum cryptographic requirements including the use of Suite B cryptography (AES-GCM, SHA-384, ECDH P-384) for high-assurance environments.

WireGuard shows how simplicity improves security. A smaller codebase has a smaller attack surface, is easier to audit and is more likely to be implemented correctly. WireGuard's roughly 4,000 lines contrast with much larger TLS stacks that have produced critical vulnerabilities such as Heartbleed (CVE-2014-0160). Simplicity is itself a security property.
:::

%%%

---
unit: Defense
code: WID
title: Wireless Intrusion Detection Systems (WIDS)
---
:::callout style=soft
A **Wireless Intrusion Detection System (WIDS)** monitors the RF environment for anomalous 802.11 traffic patterns, including evil twins, rogue APs, deauthentication floods, and unauthorized clients, and alerts security teams in real time.
:::

:::table
| Attack Type | WIDS Detection Method | Alert Trigger |
|-------------|----------------------|---------------|
| Evil Twin | Duplicate SSID with different BSSID | Same SSID broadcasting from unknown MAC |
| Rogue AP | Unexpected BSSID on known channel | MAC not in authorized AP inventory |
| Deauth Flood | Frame rate analysis | >N deauth frames per second to any client |
| WPA Handshake Capture | Deauth + handshake correlation | Deauth followed by handshake capture window |
| Client Misconfiguration | Probe request analysis | Client probing for known-vulnerable open SSIDs |
| RF Jamming | Signal-to-noise ratio monitoring | Sustained SNR degradation on channel |
:::

::::columns
::col::
:::list heading="WIDS Deployment Modes" style=plain
- **Dedicated sensors**: Overlay sensors monitor all channels continuously; no impact on AP throughput
- **AP-integrated**: Access points scan off-channel periodically while serving clients; may miss events during scan gaps
- **Wireless client sensors**: Endpoint software on managed devices detects anomalous APs during normal operation
- **Hybrid**: Combination of dedicated sensors for critical zones and AP-integrated scanning for general coverage
:::
::col::
:::callout style=line
**NIST SP 800-153** Section 4.4: "Organizations should deploy WIDS to continuously monitor the RF environment and detect unauthorized wireless activity. WIDS data should be integrated with the organization's SIEM for correlation with other security events."

**ISO/IEC 27001** A.13.1.1: "Networks should be managed and controlled to protect information in systems and applications." WIDS is a key control for wireless network monitoring.
:::
::::

:::code language=mermaid caption="WIDS deployment architecture: dedicated sensors provide continuous RF coverage; the alert console shows an evil twin detection event with the rogue BSSID identified and its approximate location triangulated from multiple sensor signal readings"
flowchart LR
  S1["Sensor S1"] --> W
  S2["Sensor S2"] --> W
  S3["Sensor S3"] --> W
  W["WIDS console"] --> AL["Alert: evil twin<br/>SSID Corp_WiFi from an unknown BSSID"]
  AL --> R["Response: locate by signal strength,<br/>contain, notify users"]
:::

:::notes
A Wireless Intrusion Detection System (WIDS) is the primary real-time defense against the class of wireless attacks discussed in this lecture. Without a WIDS, an evil twin attack or a rogue AP may operate undetected for hours, days, or weeks, the victim has no indication that their traffic is being captured, and forensic evidence of the attack may be minimal or non-existent since the attacker's device is not connected to any monitored infrastructure.

The core function of a WIDS is continuous monitoring of the RF environment on all relevant channels to identify 802.11 traffic that violates the organization's defined security baseline. This baseline is established during the WIDS configuration process and should include: the BSSID (MAC address) and SSID of every authorized AP, the channels those APs are configured to operate on, the expected signal strength range at various sensor locations, and the expected behavior of authorized clients.

**Evil twin detection** is one of the most critical WIDS functions. The detection logic is straightforward: if a WIDS sensor detects a beacon frame advertising a known SSID (one that appears in the authorized AP inventory) but the BSSID of the AP transmitting that beacon is not in the authorized inventory, an alert is generated. This is an extremely high-confidence indicator, it essentially cannot be a false positive if the authorized AP inventory is maintained accurately. The challenging operational requirement is maintaining an accurate, up-to-date inventory of all authorized APs, which requires change management processes that record every AP deployment, replacement, and configuration change.

**Deauthentication flood detection** monitors for the frame type exploited in deauthentication attacks. A single deauthentication frame to a specific client might be a legitimate AP management action; sustained deauthentication frames at high rates targeting multiple clients are almost certainly an attack. WIDS systems typically implement rate-based detection with configurable thresholds (e.g., alert when more than 10 deauth frames are sent to any client within 60 seconds from a source that is not an authorized AP).

**Rogue AP detection** requires correlating wireless observations with wired-side monitoring. A WIDS sensor that sees a new BSSID broadcasting in the building might be a visitor's mobile hotspot (not on the wired network, probably harmless) or a rogue AP physically plugged into the corporate network (a serious threat). Cross-correlating the new BSSID with switch port MAC address tables helps distinguish these cases.

Commercial WIDS solutions include Cisco DNA Center (with AireOS or IOS-XE APs), Juniper Mist (AI-driven wireless security), Aruba ClearPass (with policy enforcement), and Fortinet FortiWLM. Open-source alternatives include Kismet (with server-client architecture and plugin support for enterprise deployments) and SNORT with wireless-specific preprocessors. NIST SP 800-153 recommends that WIDS data be forwarded to a SIEM (Security Information and Event Management) system for correlation with network, endpoint, and authentication logs, an evil twin attack detected by WIDS can be correlated with unusual authentication failures from the same time period to identify potential victims.

**Location services and forensics**: Advanced WIDS implementations can use signal strength measurements from multiple sensors (triangulation or fingerprinting) to estimate the physical location of a detected rogue or evil twin AP. This is valuable for physical security response, an estimated location of "west end of 3rd floor parking garage" allows security personnel to investigate and potentially apprehend the attacker while the attack is still in progress. This capability distinguishes enterprise WIDS (with sensor density designed for location accuracy) from basic rogue detection that can only confirm presence, not location.

Wireless intrusion detection is where wireless security meets physical security: locating a rogue access point and sending personnel to investigate requires coordination between IT security operations and the physical security team. Security spans digital and physical domains.
:::

%%%

---
unit: Defense
code: NST
title: NIST SP 800-48 & SP 800-153, Wireless Security Frameworks
---
:::callout style=soft
NIST provides two key Special Publications specifically addressing wireless network security. These documents define organizational policies, technical controls, and operational procedures that constitute the federal baseline for wireless security, and are widely adopted in private sector organizations seeking authoritative guidance.
:::

::::columns
::col::
:::list heading="NIST SP 800-48 Rev. 1 (2008), Key Recommendations" style=plain
- Deploy WPA2 (or WPA3 in current implementations) as minimum encryption standard; explicitly prohibit WEP
- Establish a wireless security policy before deploying any wireless infrastructure
- Conduct regular wireless site surveys to detect rogue APs and unauthorized devices
- Require VPN for all sensitive data transmission over wireless networks
- Implement user awareness training on wireless security risks
- Segment wireless networks from wired infrastructure using firewalls
- Maintain audit logs of all wireless association and authentication events
:::
::col::
:::list heading="NIST SP 800-153 (2012), Key Recommendations" style=plain
- Deploy WIDS to continuously monitor the RF environment
- Maintain an inventory of all authorized APs with BSSIDs, channels, and locations
- Implement network access control (802.1X/RADIUS) for enterprise networks
- Separate guest wireless from corporate wireless using VLANs and firewalls
- Conduct periodic wireless penetration testing per NIST SP 800-115
- Review and update wireless security policies at least annually
- Integrate wireless security events with SIEM for correlation
- Apply FIPS 140-2/140-3 validated cryptographic modules for government systems
:::
::::

:::code language=mermaid caption="NIST wireless security framework: controls organized by the Identify-Protect-Detect cycle from the NIST Cybersecurity Framework, with specific SP 800-48 and SP 800-153 recommendations mapped to each phase"
flowchart LR
  I["<b>Identify</b><br/>Wireless asset inventory<br/>Risk assessment<br/>Policy"] --> P["<b>Protect</b><br/>WPA3, 802.1X<br/>VPN, segmentation<br/>FIPS 140-3 modules"]
  P --> D["<b>Detect</b><br/>Wireless IDS<br/>SIEM integration<br/>Audit logging, site surveys"]
  D -->|"findings update the inventory"| I
:::

:::notes
NIST Special Publications 800-48 and 800-153 are the authoritative federal guidance documents for wireless network security in the United States. While their primary audience is federal agencies (which are required to follow NIST guidance under FISMA, the Federal Information Security Management Act), they are widely adopted in private sector organizations, referenced in regulatory compliance frameworks, and cited in industry best practice documentation.

**NIST SP 800-48, "Guide to Securing Legacy IEEE 802.11 Wireless Networks" (Revision 1, 2008)** was originally published to address the transition from WEP to WPA/WPA2. Despite its age, its core recommendations remain highly relevant. The document explicitly deprecates WEP ("The use of WEP is not recommended. If WEP is in use, it should be upgraded to WPA or WPA2 as soon as possible"), a statement that was necessary in 2008 when many organizations were still running WEP despite its known vulnerabilities. The document also provides guidance on wireless security policies, site surveys, and the use of VPNs for sensitive data transmission. Its age means it predates WPA3 and several other modern developments, but its policy framework and organizational guidance remain applicable.

**NIST SP 800-153, "Guidelines for Securing Wireless Local Area Networks (WLANs)" (2012)** is more recent and provides more operational depth. It covers the full lifecycle of wireless security: planning (risk assessment, policy development), implementation (AP configuration, authentication, encryption), operations (WIDS, log management, incident response), and assessment (penetration testing, audits). Its Section 4.4 (WIDS) and Section 4.5 (Network Segmentation) are particularly relevant to this lecture's material.

The **FIPS 140-2 and FIPS 140-3** requirements are worth explaining briefly. FIPS (Federal Information Processing Standards) Publication 140 is a US government standard that specifies security requirements for cryptographic modules (hardware or software components that perform cryptographic operations). Federal agencies are required to use only FIPS 140-validated modules for protecting sensitive information. This means that wireless equipment deployed in federal environments must use access points and VPN clients whose cryptographic implementations have been validated by NIST's Cryptographic Module Validation Program (CMVP). FIPS 140-3 (current version, replacing 140-2) aligns with ISO/IEC 19790 and adds requirements for software cryptographic modules.

The **ISO/IEC 27001** context is also important for students entering organizations outside the US federal space. ISO/IEC 27001 (Information Security Management Systems, Requirements) is the international standard for information security management. Its Annex A controls that are most relevant to wireless security include: A.8.21 (Security of network services), A.8.20 (Networks security), A.8.22 (Segregation in networks), and A.8.15 (Logging). ISO/IEC 27002 provides implementation guidance for these controls and references wireless-specific considerations including the need for wireless network monitoring and the use of strong encryption.

The relationship between NIST and ISO/IEC guidance is complementary: NIST provides US-specific technical depth, while ISO provides internationally recognized management framework structure. Organizations seeking compliance with both (common in multinational companies) can generally satisfy both frameworks with the same underlying technical controls.

**PCI DSS** (Payment Card Industry Data Security Standard) also has relevant wireless requirements. Requirement 1.3.6 requires that wireless networks be segmented from the cardholder data environment; Requirement 2.2.7 prohibits the use of insecure wireless protocols; Requirement 11.2.1 requires quarterly wireless network scans to detect unauthorized access points. Organizations that process payment card transactions in environments with any wireless infrastructure must address these requirements.

NIST SP 800-153, ISO/IEC 27002 and PCI DSS v4.0 each address the same wireless controls in different language. Understanding the underlying technical controls lets an organization satisfy several compliance frameworks at once rather than treating each separately.
:::

%%%

---
unit: Defense
code: ATK
title: MITRE ATT&CK, Wireless Attack Techniques
---
:::callout style=soft
The **MITRE ATT&CK** framework catalogs adversary tactics, techniques, and procedures (TTPs) used in real-world attacks. Mapping wireless attack techniques to ATT&CK enables defenders to systematically evaluate their detection coverage and prioritize control improvements.
:::

:::table
| ATT&CK Tactic | Technique ID | Technique Name | Wireless Attack Example |
|---------------|-------------|----------------|------------------------|
| Reconnaissance | T1595 | Active Scanning | airodump-ng scan for SSIDs/clients |
| Initial Access | T1200 | Hardware Additions | Rogue AP physically connected to network |
| Initial Access | T1557 | Adversary-in-the-Middle | Evil twin AP intercepts client connections |
| Credential Access | T1040 | Network Sniffing | Wireshark/bettercap credential capture |
| Credential Access | T1110.003 | Password Spraying | WPA2 handshake offline dictionary attack |
| Defense Evasion | T1562.007 | Disable or Modify Cloud Firewall | Deauth flood overwhelming detection thresholds |
| Collection | T1557.002 | ARP Cache Poisoning | ARP spoof on connected wireless segment |
| Exfiltration | T1048 | Exfiltration Over Alternative Protocol | DNS exfiltration over attacker-controlled DNS |
:::

:::code language=mermaid caption="MITRE ATT&CK wireless technique mapping: orange cells represent techniques used in wireless attacks; green shields indicate detection coverage; the gap in Exfiltration techniques represents a common blind spot in wireless security monitoring programs"
flowchart LR
  subgraph R["Reconnaissance"]
    R1["T1595 Active Scanning"]
  end
  subgraph I["Initial Access"]
    I1["T1200 Hardware Additions"]
    I2["T1557 Adversary-in-the-Middle"]
  end
  subgraph C["Credential Access"]
    C1["T1040 Network Sniffing"]
    C2["T1110 Brute Force"]
  end
  subgraph CO["Collection"]
    CO1["T1557.002 ARP Cache Poisoning"]
  end
  R --> I --> C --> CO
:::

:::notes
The MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) framework, maintained by the MITRE Corporation, is one of the most widely used tools in defensive security for systematically understanding and addressing adversary behavior. ATT&CK organizes adversary behavior into a matrix of Tactics (the "why", what the adversary is trying to achieve) and Techniques (the "how", the specific method used). For each technique, ATT&CK provides detection guidance, mitigation recommendations, and real-world examples drawn from documented threat actor behavior.

Mapping wireless attacks to ATT&CK serves several practical purposes. First, it enables **gap analysis**: security teams can identify which wireless attack techniques they currently have detection coverage for (via WIDS alerts, SIEM rules, or endpoint detection) and which represent blind spots. Second, it provides a **common language** for communicating risk to stakeholders who are familiar with the ATT&CK framework. Third, it facilitates **threat intelligence integration**: when a threat intelligence report describes a threat actor using specific ATT&CK techniques, security teams can immediately determine whether those techniques include wireless attack methods and adjust monitoring accordingly.

**T1595 (Active Scanning)** in the Reconnaissance tactic covers the attacker's initial wireless survey using tools like airodump-ng. Detection: WIDS may detect excessive probe requests or scanning patterns; however, passive monitor mode scanning (which does not transmit anything) is inherently undetectable.

**T1200 (Hardware Additions)** covers rogue AP attacks where the attacker physically connects unauthorized hardware to the wired network. Detection: switch port security, MAC address change alerts, 802.1X port authentication rejecting unauthorized devices.

**T1557 (Adversary-in-the-Middle)** is the primary technique for evil twin and MITM attacks. Sub-techniques include T1557.001 (LLMNR/NBT-NS Poisoning) and T1557.002 (ARP Cache Poisoning), both relevant to local network segments accessible via wireless. Detection: WIDS duplicate SSID detection, ARP monitoring on connected clients.

**T1040 (Network Sniffing)** covers passive traffic capture with tools like Wireshark and airodump-ng. Detection: very limited, passive sniffing is inherently undetectable. The primary mitigations are preventive: strong link-layer encryption (WPA3), VPN, and application-layer encryption (HTTPS/TLS).

**T1110.003 (Password Spraying)** maps to offline WPA2 handshake cracking, the attacker captures the handshake (using T1557 and deauthentication), then runs dictionary attacks offline. Detection: the deauthentication phase is detectable by WIDS; the offline cracking phase is undetectable (it occurs on the attacker's hardware with no network interaction). Mitigation: use WPA3 to eliminate handshake cracking; use strong, unique passwords if WPA3 is unavailable.

The **exfiltration gap** highlighted in the diagram deserves special attention. After an evil twin attack captures credentials or sensitive data, the attacker must exfiltrate this data. DNS exfiltration (encoding data in DNS query strings sent to an attacker-controlled domain) is particularly effective in wireless environments where the evil twin AP controls DNS and may not log outbound DNS queries. Many wireless security monitoring programs focus entirely on the initial access and collection phases and have no monitoring for the exfiltration phase. This gap can be addressed by deploying DNS monitoring (logging all DNS queries from wireless clients) and applying detection rules for common DNS exfiltration patterns (unusually long DNS queries, queries to newly registered domains, high query volumes to a single domain).

The MITRE ATT&CK Navigator annotates the ATT&CK matrix with detection coverage and mitigation status. The wireless-relevant techniques in this table map onto specific ATT&CK entries, which is how teams record where their monitoring is strong and where it is blind.
:::

%%%

---
unit: Habits
code: SAF
title: Safe Wi-Fi Habits
---
:::list heading="On any public network" style=plain
- Use a VPN whenever possible
- Confirm the exact network name with staff before connecting
- Avoid logging into sensitive accounts on unknown networks
- Turn off auto-connect to open Wi-Fi networks
- Look for HTTPS, even on a trusted-looking network
:::

::::columns
::col::
:::callout style=soft
**Why a VPN?**  
A Virtual Private Network (VPN) encrypts your traffic between your device and the VPN server, masking it from local eavesdroppers on the same network. Even if the network is compromised, your data remains protected in transit.
:::

::col::
:::callout style=soft
**Evil Twin Threats**  
Attackers often deploy rogue access points with names similar to legitimate ones (e.g., "FreeAirportWiFi" vs. "FreeAirportWiFi2"). These *evil twin* networks are designed to trick users into connecting, enabling man-in-the-middle (MITM) attacks.
:::

::col::
:::callout style=soft
**Auto-Connect Risks**  
Many devices are configured to automatically reconnect to previously joined open networks. This convenience can silently expose your device to malicious networks without your knowledge, especially in high-traffic areas.
:::
::::

:::image src="images/07_safe_wifi_habits_checklist.png" alt="Visual checklist poster design with five items: VPN icon with green checkmark; person asking a staff member about SSID; padlock icon for HTTPS verification; Wi-Fi settings screen showing auto-connect toggle turned off; sensitive account login crossed out in red; clean flat design, white background, red and grey color scheme" caption="Safe Wi-Fi habits: five behavioral controls that collectively reduce risk on any untrusted wireless network" width=half
:::

:::steps heading="Before Connecting to Public Wi-Fi"
1. **Ask staff for the exact network name**, Get the SSID letter-by-letter; attackers often use similar names like "Airport_WiFi" vs. "AirportWifi"
2. **Disable auto-connect**, Go to network settings and disable automatic connection to open networks
3. **Connect to VPN first, before any browsing**, Ensure VPN is active before opening any application
4. **Verify HTTPS on every site**, Look for the padlock icon; avoid entering credentials on HTTP sites
5. **Disable file sharing and AirDrop**, Reduce attack surface by disabling peer-to-peer sharing features while on public networks
6. **Log out and forget the network when done**, Prevents future automatic reconnection
:::

:::notes
Safe Wi-Fi habits are essential for protecting user privacy and data integrity when connecting to public or untrusted wireless networks. These behaviors are grounded in both cryptographic best practices and threat awareness, aligning with NIST Special Publication 800-48, which outlines wireless security guidelines for enterprise and personal use.

The use of a Virtual Private Network (VPN) is one of the most effective countermeasures against passive eavesdropping and active interception on open networks. Protocols such as OpenVPN, IKEv2/IPsec, and WireGuard provide encrypted tunnels that shield application-layer traffic from adversaries on the same local network. Even on networks that appear legitimate, a VPN ensures confidentiality and integrity, particularly when accessing sensitive services like banking portals or corporate resources.

Verifying the network name (SSID) with authorized staff mitigates the risk of connecting to an *evil twin* access point, a common social engineering tactic tracked under various CVEs related to rogue AP detection evasion. These malicious networks mimic legitimate ones and are often used to harvest credentials or deploy malware.

Logging into sensitive accounts over untrusted networks, even those that appear secure, can expose session tokens and credentials to interception. The lack of end-to-end encryption in many web applications makes them vulnerable to session hijacking unless HTTPS is enforced. TLS 1.2 and 1.3 help ensure secure communication, but users must verify the presence of valid certificates and the lock icon in the browser.

Disabling auto-connect features prevents devices from automatically rejoining previously connected open networks, which may no longer be safe. This aligns with ISO/IEC 27001 Annex A.12.6, which emphasizes control over mobile device usage and network connections.

Finally, always ensure that websites use HTTPS. The HTTP Strict Transport Security (HSTS) policy and certificate pinning further reduce the risk of SSL stripping or man-in-the-middle attacks, as defined in RFC 6797 and RFC 7469 respectively.

The human behavioral dimension of public Wi-Fi security is worth emphasizing because technical controls alone are insufficient without accompanying user habits. An organization can deploy the best VPN infrastructure, enforce WPA3, and implement certificate pinning in all its mobile applications, but if an employee connects to a malicious evil twin before enabling the VPN, or shares sensitive documents while on an open guest network, the technical controls provide no protection.

The habit of verifying the SSID with staff is particularly important and surprisingly underused. At any airport or hotel, there are typically multiple wireless networks with similar names, official networks from the venue, networks from co-located businesses, and potentially malicious networks set up by attackers. Taking 30 seconds to confirm "Is it 'Heathrow_Guest' or 'HeathrowGuest' or 'Heathrow WiFi'?" with an employee eliminates the ambiguity that evil twin attacks depend on.

Corporate mobile device management (MDM) policies can enforce many of these habits automatically: requiring VPN before any network traffic, disabling automatic connection to open networks, and enforcing HTTPS certificate validation at the device level. For organizations with a significant remote or traveling workforce, MDM-enforced VPN with always-on connectivity (so VPN is active from the moment the device connects to any network) provides the strongest protection with the least reliance on individual user discipline.
:::

%%%

---
unit: Habits
code: MIS
title: Common Misconceptions About Wi-Fi Security
---
:::callout style=soft
Dangerous myths about wireless security lead users and administrators to make decisions that leave them exposed. Correcting these misconceptions is as important as teaching the underlying technical concepts.
:::

:::table
| Misconception | Why It Is Wrong | Correct Understanding |
|---------------|-----------------|----------------------|
| "I'm safe because the site uses HTTPS" | HTTPS protects data in transit but doesn't protect against evil twin, the attacker is the endpoint your device connects to | HTTPS + VPN are both needed; HTTPS alone doesn't prevent MITM via evil twin |
| "Hidden SSIDs are more secure" | Hidden SSIDs still appear in probe requests from clients; trivially discovered with airodump-ng | Security through obscurity does not work; hiding SSIDs provides no real security benefit |
| "MAC address filtering keeps out attackers" | MAC addresses can be spoofed in seconds with a single ifconfig command; attacker captures a valid MAC from traffic | MAC filtering is trivially bypassed; use 802.1X for real access control |
| "WPA2 is uncrackable" | WPA2 with a weak password can be cracked in seconds using captured handshake + GPU + dictionary | WPA2 is as strong as the password; use 20+ random character passwords or move to WPA3 |
| "Public VPNs provide complete privacy" | VPN provider can log all traffic; jurisdiction may compel disclosure | VPNs shift trust to the VPN provider; self-operated VPNs or verified no-log providers preferred |
| "My home Wi-Fi is safe from outsiders" | 2.4 GHz signals propagate 70+ meters; neighbors or passers-by can reach your network | Treat home Wi-Fi with same rigor as any wireless network; use WPA3, strong password, disable WPS |
:::

:::notes
Misconceptions about wireless security are widespread, and some are actively harmful because they create a false sense of security that prevents users from taking appropriate precautions. Effective security awareness training must not only teach correct information but also explicitly address and debunk the myths that learners are likely to hold coming into the training.

**"I'm safe because the site uses HTTPS"** is perhaps the most dangerous misconception. HTTPS does provide strong protection against passive eavesdropping and against third-party MITM attackers, but it does not protect against an adversary who has positioned themselves as your gateway (i.e., an evil twin AP). When your device connects to an evil twin AP, all your HTTPS traffic is still encrypted, but it is encrypted to the real server and forwarded by the attacker, who can read it after decryption at the server. The attacker's access point itself is not breaking HTTPS; it is simply the network path through which your HTTPS traffic flows. The attacker can capture DNS queries (revealing which sites you visit), attempt SSL stripping on HTTP initial requests, and observe timing patterns of your HTTPS traffic. For the most sensitive operations, a VPN that provides an encrypted tunnel all the way from your device to a trusted endpoint server is necessary to prevent even the evil twin AP from seeing your traffic.

**"Hidden SSIDs are more secure"** is a myth that has been thoroughly debunked but persists in popular advice. When an SSID is "hidden," the AP's beacon frames contain an empty SSID field rather than the network name. However, client devices that have previously joined the hidden network continuously broadcast probe request frames looking for it, these probe requests contain the actual SSID. Any device in monitor mode can see these probe requests and learn the "hidden" SSID within seconds of a client device being present. Tools like airodump-ng display hidden SSIDs as soon as they appear in probe requests. Hidden SSIDs also cause usability problems (clients must actively probe for them, draining battery and potentially revealing their network membership history to observers). The NIST guidance in SP 800-48 explicitly states that hiding SSIDs provides no meaningful security benefit.

**"MAC address filtering keeps out attackers"** fails for the same reason as hidden SSIDs: it is security through obscurity, and the "secret" (the list of valid MAC addresses) is continuously broadcast in the clear. Every frame transmitted by a legitimate client includes the source MAC address in the unencrypted 802.11 header. An attacker in monitor mode can collect the MAC addresses of legitimate clients, change their own adapter's MAC address to match (with `ifconfig wlan0 hw ether AA:BB:CC:DD:EE:FF` on Linux, taking under a second), and then connect using that valid MAC address. MAC filtering adds no meaningful security but adds significant administrative overhead. It is security theater and should be removed from security guidelines.

**"WPA2 is uncrackable"** conflates the security of the AES cipher (which is essentially uncrackable with current technology) with the security of the WPA2 handshake (which depends entirely on password strength). AES-256 with a truly random key is not attackable by brute force with any foreseeable technology, the keyspace is astronomically large. But WPA2's dictionary attack vulnerability means an attacker with a captured handshake can test millions of candidate passwords per second. A password that appears in the rockyou.txt wordlist (14 million entries) will be cracked in under 15 seconds on consumer hardware. A password based on a common word with substitutions (P@ssw0rd!) will be cracked in minutes using rule-based mutation. The AES cipher is not the weak link, the password is.

**"My home Wi-Fi is safe from outsiders"** underestimates RF propagation. A typical 2.4 GHz 802.11n AP at 100mW transmit power covers approximately 70 meters indoors and 250 meters in open space. Anyone within range, a neighbor, someone parked on the street, someone in the adjacent office space, can attempt to access your network. With a directional high-gain antenna (a Yagi or parabolic dish), the effective receive range can be extended to several hundred meters. Users who use their home network for sensitive work (common in remote work scenarios) should treat it with the same security rigor as an enterprise network: WPA3, strong unique password, disable WPS (Wi-Fi Protected Setup, which has known vulnerabilities including Pixie Dust attack, CVE-2014-9151), and consider network segmentation between work and personal devices.

Stating a misconception before correcting it improves retention. Teaching only the correct information leaves the earlier incorrect belief in place beside it; naming the myth, explaining why it seems plausible and replacing it with an accurate model displaces it more durably.
:::

%%%

---
unit: Review
code: CHK
title: Mid-Lecture Knowledge Check
---
:::callout style=soft
Take five minutes to answer these questions, without looking at your notes. Then compare with a partner. These questions test conceptual understanding, not memorization.
:::

::::columns
::col::
:::list heading="Questions 1–5" style=plain
- **Q1**: An attacker in a coffee shop sets up an AP named "Starbucks_Free" matching the venue's real network. What specific attack is this, and what protocol vulnerability does it exploit?
- **Q2**: You're on public Wi-Fi using HTTPS for all your banking. Your friend says you're safe because HTTPS encrypts everything. Are they right? What's missing from their argument?
- **Q3**: A WPA2 network uses the password "Summer2024!", a common word with substitutions. Describe the specific attack that recovers this password and how long it might take.
- **Q4**: What is the difference between a rogue access point and an evil twin? Give one detection method specific to each.
- **Q5**: WPA3's SAE handshake is captured by an attacker. They run it through aircrack-ng with the rockyou.txt wordlist. What happens and why?
:::
::col::
:::list heading="Questions 6–10" style=plain
- **Q6**: Your company deploys 802.1X/RADIUS for Wi-Fi authentication. An attacker sets up an evil twin AP with the same SSID. Will employees' devices connect to the evil twin? Why or why not?
- **Q7**: A hotel captive portal asks for your email and room number over HTTP before granting internet access. What are the security risks, and what should you do?
- **Q8**: What is a deauthentication attack, and what WPA3 feature prevents it? Why was this feature optional in WPA2?
- **Q9**: Name three things a Wireless Intrusion Detection System (WIDS) can detect that a standard network firewall cannot.
- **Q10**: You're advising a small business that uses WPA2-PSK with the password "coffeeshop123". What three specific changes would most improve their wireless security, and why?
:::
::::

:::notes
The knowledge check questions are designed to assess the higher levels of Bloom's Taxonomy, application, analysis, and evaluation, rather than simple recall. This distinction is important in security education because real-world security decisions require applying conceptual knowledge to novel situations, not retrieving memorized facts.

**Q1, Evil Twin Analysis**: The expected answer should name the evil twin attack specifically, identify that it exploits the 802.11 client behavior of automatically associating with any AP broadcasting a known SSID (the Preferred Network List problem), and note that this is a protocol-level design issue rather than a vulnerability in the cryptography. A strong answer would also mention deauthentication as a facilitator.

**Q2, HTTPS Limitation**: The friend's argument is partially right but incomplete. HTTPS encrypts traffic between the client and the server, but in an evil twin scenario, the evil twin AP is the first hop in the network path. If the attacker is performing SSL stripping, HTTPS is bypassed. If the attacker is not performing SSL stripping, HTTPS protects the content of traffic, but the attacker can still see DNS queries (which sites you visit), can observe timing patterns, and can attempt certificate-based MITM. The complete protection requires HTTPS + VPN + HSTS + certificate validation.

**Q3, WPA2 Password Cracking**: "Summer2024!" is a common password pattern (capitalized word + year + punctuation). This type of password appears in extended wordlists and rule sets. The attack uses aircrack-ng or hashcat against a captured 4-way WPA2 handshake. With rule-based mutation (appending years to common words), modern GPU hardware can test this in seconds to minutes. The key insight is that WPA2's security is entirely dependent on password entropy, not the cipher.

**Q4, Rogue vs. Evil Twin Distinction**: This question specifically tests the conceptual distinction from the RVE slide. Rogue AP: physically connected to wired network, detected via switch port MAC monitoring or 802.1X rejection. Evil twin: standalone, broadcasting same SSID with different BSSID, detected via WIDS duplicate SSID alert.

**Q5, SAE and Aircrack-ng**: aircrack-ng cannot crack a WPA3-SAE handshake using a dictionary attack because the SAE exchange does not produce a capturable value that can be tested against guessed passwords offline. The attacker would see a captured exchange but could not derive the PMK or verify guesses from it, they would need to interact with the live AP for each guess (enabling rate limiting as an effective defense). Aircrack-ng would simply report that it cannot crack the capture.

**Q6, 802.1X Evil Twin Defense**: With 802.1X, the client's supplicant attempts EAP authentication through the AP to the RADIUS server. An evil twin AP has no access to the organization's RADIUS server and cannot complete the authentication on the RADIUS server's behalf. The client will receive an authentication failure from the evil twin (because the evil twin cannot produce a valid RADIUS Access-Accept response) and should not connect. This assumes the client is configured to validate the RADIUS server's certificate, if not, the evil twin could run its own RADIUS server and accept any credentials.

**Q7, Captive Portal Risk**: The risks include: credentials transmitted in plaintext over HTTP (sniffable by any device in monitor mode), DNS queries intercepted by the network's DNS server (revealing browsing patterns), and the potential for an evil twin to serve a fake captive portal. Recommended actions: use a mobile hotspot instead; if you must use the hotel Wi-Fi, enable VPN before entering any credentials (which many VPN clients prevent during the captive portal phase, creating the pre-authentication vulnerability discussed in the captive portal slide); use a throwaway email account that doesn't share credentials with other services.

**Q8, Deauthentication and PMF**: A deauthentication attack sends spoofed 802.11 management frames (Type 0, Subtype 12) impersonating the AP to force client disconnections. WPA3 mandates Protected Management Frames (PMF/802.11w), which cryptographically authenticate management frames using the session keys, a spoofed deauth frame that is not authenticated with the correct session keys is rejected by WPA3 clients. PMF was optional in WPA2 because: (1) it requires additional computational overhead; (2) it was designed as a backward-compatible enhancement, not a requirement, to allow gradual adoption without breaking compatibility with existing WPA2 devices; (3) the commercial urgency was not recognized until deauthentication attacks became common in commercial attack toolkits.

**Q9, WIDS vs. Firewall**: WIDS can detect: evil twin APs (duplicate SSID with different BSSID), deauthentication floods (unusual frame type at high rates), unauthorized clients probing the airspace, RF jamming (channel utilization anomalies), clients connecting to rogue APs, and physical location of wireless threats. A network firewall operates at the IP layer and above, it cannot see 802.11 layer events, cannot detect duplicate SSIDs, and cannot identify RF-layer attacks. The firewall operates after clients have already associated with an AP; WIDS operates at the association layer before IP traffic is possible.

**Q10, Small Business Recommendations**: The three highest-impact changes: (1) Move to WPA3 or WPA2 with a strong 20+ character random password, the current password "coffeeshop123" is trivially crackable. (2) Enable PMF (Protected Management Frames) if using WPA2, prevents deauthentication attacks. (3) Segment the guest network from the business network using a separate SSID and VLAN, prevents customers from accessing business systems. Secondary recommendations (worth mentioning): disable WPS (prevents Pixie Dust attacks), change default AP admin credentials, enable WIDS if the AP supports it.

:::

%%%

---
unit: Case Studies
code: FRE
title: "Case Study, Firesheep (2010): When Session Hijacking Went Mainstream"
---
:::callout style=soft
In October 2010, security researcher Eric Butler released **Firesheep**, a Firefox extension that let anyone in a coffee shop click to hijack another customer's Facebook, Twitter, or Amazon session in one click. It became the most downloaded Firefox extension of the year and forced the entire web industry to adopt HTTPS.
:::

::::columns
::col::
:::steps heading="How Firesheep Worked"
1. User installed Firesheep Firefox extension (no hacking experience required)
2. Firesheep placed the wireless adapter in promiscuous mode, capturing all HTTP traffic on the open Wi-Fi network
3. Extension parsed HTTP traffic looking for session cookies from popular websites
4. Recognized cookies appeared as profile pictures in a sidebar, Facebook, Twitter, Amazon, Flickr, Foursquare, and 26 others
5. User clicked a profile picture; Firesheep injected the captured cookie into the browser
6. User was now logged in as the victim, without needing their password
:::
::col::
:::list heading="Immediate Industry Impact" style=plain
- **Facebook**: Enabled HTTPS by default for all users, January 2011 (3 months after Firesheep)
- **Twitter**: Enabled HTTPS by default, March 2011
- **GitHub**: HTTPS-only enforced, 2012
- **Google**: HTTPS by default for all services, 2010 (already in process, accelerated)
- **Broader web**: Firesheep is credited with accelerating HTTPS adoption industry-wide by years
- **2024 baseline**: >95% of web traffic is now encrypted, per Google Transparency Report
:::
::::

:::notes
Firesheep is one of the most important events in recent web security history, not because it introduced a new technical attack, session hijacking on open networks had been documented for years, but because it made an existing attack accessible to anyone with basic computer skills and created undeniable public evidence of the risk, forcing a massively accelerated industry response.

Eric Butler released Firesheep on October 24, 2010, at TIGRCon (ToorCamp Internet Governance Research Conference). In his blog post announcing it, Butler explained his motivation clearly: "Websites have a responsibility to protect the people who use them by encrypting sensitive data. Failing to do so means that any time you access a website over an unencrypted wireless connection, like a coffee shop, you're leaving yourself open to having your account hijacked." He released Firesheep specifically to make the risk undeniable through demonstration, rather than through technical arguments that most web product managers and executives would not engage with.

The technical mechanism is straightforward and had been documented since the late 1990s. When a user logs into a website, the server creates a session and sends a session cookie to the browser. On subsequent requests, the browser sends this cookie back to prove it is the same logged-in session. In 2010, most websites (including Facebook and Twitter) used HTTPS only for the login page (where the password was transmitted) but then switched to HTTP for all subsequent browsing, citing performance concerns. This meant the session cookie, which is just as valuable as the password for accessing the account, was transmitted unencrypted in every HTTP request.

Firesheep automated the capture and display of these cookies in a user-friendly Firefox sidebar. The extension put the wireless adapter in promiscuous mode (similar to monitor mode, but for connected network traffic), parsed all HTTP traffic for Set-Cookie and Cookie headers from known websites, and displayed the captured sessions with profile pictures. Clicking a profile picture used the captured cookie to impersonate the victim in the attacker's browser.

The response was immediate and dramatic. Firesheep was downloaded over 2 million times in the first week. Reporters and bloggers demonstrated it in coffee shops and published articles showing that everyone's Facebook session was visible to anyone with the tool. Facebook's engineers received enormous pressure from the public and from the press. Within three months, Facebook had enabled HTTPS by default. Within six months, Twitter followed. The entire industry took notice and began the transition to universal HTTPS that we now largely take for granted.

Firesheep demonstrates several important principles beyond the technical: **security through demonstration** is often more effective than security through documentation; **tools that make abstract risks concrete** accelerate action; and **the principle of responsible disclosure** applied creatively, Butler did not report the vulnerability privately to each affected company (which would have been ignored for years), but disclosed it publicly in a way that made inaction impossible. This approach was controversial but ultimately resulted in better security for millions of users years faster than private disclosure would have.

The current state, where Google's Transparency Report shows over 95% of web traffic encrypted, all major browsers display prominent warnings for HTTP sites, and the HSTS preload list contains over 130,000 domains, is largely a consequence of the trajectory that Firesheep's release accelerated. The 2010 web and the 2024 web are different security environments, and Firesheep played a meaningful role in driving that change.

**CVE context**: The vulnerability Firesheep exploited does not have a single CVE because it is not a bug in a specific implementation, it is a design pattern (using HTTP rather than HTTPS for session traffic) that was widespread across the industry. CWE-614 ("Sensitive Cookie in HTTPS Session Without 'Secure' Attribute") and CWE-523 ("Unprotected Transport of Credentials") capture the underlying weakness class.

Firesheep (2010) demonstrated session hijacking over open Wi-Fi by capturing unencrypted session cookies, and its release was framed explicitly as a push to make sites adopt HTTPS everywhere rather than only on login pages. Whether releasing a working tool was the responsible way to make that point is a genuine question for a discussion of disclosure ethics.
:::

%%%

---
unit: Summary
code: SUM
title: Trusting the Connection, Not Just the Account
---

:::pullquote
Evil twins, MITM, and packet sniffing all attack the connection itself, which is exactly why WPA3 and VPNs defend the connection, not just the account.
:::

::::columns
::col::
:::list heading="Threats to Wireless Connections" style=chips
- Evil Twin
- Man-in-the-Middle (MITM)
- Packet Sniffing
:::

::col::
:::list heading="Defensive Mechanisms" style=chips
- WPA3 Encryption
- Virtual Private Networks (VPNs)
- Certificate Pinning
:::
::::

:::callout style=line
Wireless networks introduce a unique attack surface that exists below the application layer, targeting the transmission medium itself. Traditional account-level protections like strong passwords or MFA are insufficient when an attacker compromises the communication channel.
:::

:::steps heading="Applying Wireless Defense in Depth"
1. **Secure the link layer**, Deploy WPA3 on all access points; enforce WPA2 with PMF (Protected Management Frames) as the minimum acceptable configuration
2. **Verify the access point identity**, Confirm the exact SSID with staff before connecting; consider 802.1X/RADIUS enterprise authentication to prevent rogue APs from completing the handshake
3. **Tunnel traffic with a VPN**, Activate VPN before opening any browser or application on an untrusted network; use WireGuard, IKEv2/IPsec, or OpenVPN with a trusted endpoint
4. **Enforce application-layer encryption**, Verify HTTPS (TLS 1.2+) on every site; reject HTTP for any credential or sensitive data entry; rely on HSTS preload lists
5. **Eliminate auto-connect exposure**, Remove stored open-network profiles; require manual user confirmation before joining any new wireless network
6. **Monitor the wireless environment**, Log association events and alert on duplicate SSIDs; use WIDS (Wireless Intrusion Detection Systems) per NIST SP 800-153 recommendations
:::

:::image src="images/07_wireless_defense_layers.png" alt="Concentric circle diagram showing defense layers from outside in: outermost ring 'WPA3 link encryption,' next ring 'VPN tunnel encryption,' inner ring 'HTTPS/TLS application encryption,' and center circle 'User account with MFA'; arrows on the left side show evil twin, MITM, and sniffing attacks stopped at each layer" caption="Wireless defense in depth: multiple encryption layers each block a different class of attack, link encryption, VPN tunneling, and application TLS are not redundant but complementary" width=half
:::

:::notes
In previous modules, we have emphasized securing user accounts through authentication best practices such as multi-factor authentication (MFA), password hygiene, and awareness of social engineering tactics like phishing. While these remain critical, they do not protect against threats that occur at the network layer, specifically within the wireless medium over which data travels.

Wireless networks are inherently more vulnerable than wired ones due to the broadcast nature of radio frequency (RF) communications. Attackers can exploit this with techniques such as **evil twin attacks**, where a malicious access point mimics a legitimate one to trick users into connecting. Once connected, the attacker can perform **man-in-the-middle (MITM)** attacks or deploy **packet sniffers** to capture unencrypted traffic. These methods target the confidentiality, integrity, and availability of the communication channel itself, rather than the endpoint credentials.

To counter these threats, robust cryptographic protocols must be implemented at the link layer. **WPA3**, defined by the IEEE 802.11 standard and promoted by NIST in their cybersecurity frameworks, introduces stronger encryption via Simultaneous Authentication of Equals (SAE), replacing the vulnerable PSK method used in WPA2. Additionally, **Virtual Private Networks (VPNs)** provide end-to-end encryption that protects data even if the underlying wireless network is compromised.

Securing wireless communications requires layered defense strategies that go beyond user account protection. As defined in ISO/IEC 27001 and NIST SP 800-48, wireless security policies must include regular assessment of access point configurations, encryption standards, and the use of secure tunneling protocols such as IPsec or TLS within VPN implementations.

In the next unit, we will shift focus to examine how adversarial machine learning and AI-driven tools are being leveraged for automated reconnaissance, signal analysis, and protocol exploitation in modern wireless environments.

The lecture's central insight, that defending the account is insufficient if the communication channel itself is compromised, maps to a broader architectural principle in security: defense must be applied at every layer where the threat model dictates risk. The OSI model provides a useful framework here: threats can operate at the physical layer (RF jamming), the data link layer (KRACK, evil twin), the network layer (IP spoofing, routing attacks), the transport layer (TLS downgrade), and the application layer (session hijacking, credential theft). Each layer requires its own defenses, and no single control at one layer can fully compensate for absent controls at another.

The practical upshot for students entering the workforce is that wireless security is not a solved problem delegated entirely to IT infrastructure. Individual users make daily decisions, which networks to join, whether to enable VPN, whether to verify HTTPS, that directly affect their organization's security posture. Security awareness training that focuses exclusively on phishing emails and password hygiene, while neglecting wireless threat awareness, leaves a significant gap in the human layer of the defense stack.

Looking ahead in the course, the AI-enabled threats discussed in classes 8 and 9 can be combined with wireless attack techniques to create particularly dangerous threat scenarios: AI-generated fake captive portal pages that are indistinguishable from legitimate venue portals, AI-powered traffic analysis tools that can automatically extract credentials from captured packet captures, and AI-assisted deauthentication attacks that intelligently target specific high-value devices on a network. Understanding the wireless threat landscape at the protocol level is therefore not just relevant to this class but foundational to understanding the full landscape of threats the course will address.
:::
