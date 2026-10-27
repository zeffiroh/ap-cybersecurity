# 3.1.c, Man-in-the-middle and ARP spoofing

> **Unit 3 · 3.1 Network Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 3.1.B
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Explain how the Address Resolution Protocol (ARP) can be abused to
insert an attacker between two hosts on a local network, trace the mechanics of an ARP spoofing
attack step by step, and identify the technical controls that detect or prevent it.

## Lesson

### What a man-in-the-middle attack is
A **man-in-the-middle (MITM)** attack is any attack where an adversary secretly positions itself
between two communicating parties, relaying (and often reading or altering) traffic while both
sides believe they are talking directly to each other. MITM is a category, not a single technique, DNS cache poisoning (covered in 3.1.b) is one way to become a man in the middle at the naming
layer; ARP spoofing, the subject here, is the classic way to become one at the local
network (Layer 2) layer. What makes MITM attacks dangerous is that neither endpoint necessarily
sees anything wrong: the victim's browser still loads a page, the server still gets a request that
looks legitimate, the difference is who is relaying, and possibly modifying, the traffic in
between.

### How ARP works (and why it trusts everyone)
On an Ethernet/Wi-Fi local network, devices address each other with **MAC addresses** (hardware
addresses), while applications address each other with **IP addresses**. Before host A can send an
IP packet to host B on the same local network, it must learn B's MAC address. The **Address
Resolution Protocol (ARP)** solves this: A broadcasts an "ARP request" asking "who has
192.168.1.5?", and the host with that IP replies "192.168.1.5 is at MAC aa:bb:cc:dd:ee:ff." A
caches this mapping in its **ARP table** (also called an ARP cache) so it does not have to ask
again for every packet.

The problem is that ARP was designed in 1982 for a small, trusted network, with **no
authentication whatsoever**. Any device on the local network can send an ARP reply, even one that
was never requested (a "gratuitous ARP"), and other devices will update their ARP table to match
it, no questions asked. There is no cryptographic signature, no challenge, nothing that lets a
receiving host verify that the reply actually came from the device that owns that IP address.

### ARP spoofing mechanics
An attacker who is already on the same local network (having joined the Wi-Fi, or plugged into the
switch) can exploit this trust directly. To intercept traffic between a victim (192.168.1.10) and
the router/gateway (192.168.1.1), the attacker sends two streams of forged ARP replies:

1. To the victim: "192.168.1.1 (the gateway) is at [attacker's MAC]."
2. To the gateway: "192.168.1.10 (the victim) is at [attacker's MAC]."

Both devices update their ARP tables to point at the attacker's MAC address instead of each
other's real hardware. Now every packet the victim sends "to the gateway" is actually delivered to
the attacker's network interface first, and vice versa. If the attacker simply forwards the
traffic on to the real destination after copying it (a technique called **IP forwarding** or
acting as a transparent relay), neither the victim nor the gateway notices any disruption, the
connection still works, just with an invisible extra hop where the attacker can read, log, or even
alter the traffic in transit. This entire technique is called **ARP spoofing** or **ARP cache
poisoning**, and because it typically targets the gateway to intercept all of a victim's outbound
traffic, it is the most common way to set up a local-network MITM position.

### What the attacker can do once in the middle
Once positioned as the man in the middle, an attacker's capabilities depend on what protections the
victim's traffic has. Unencrypted protocols (plain HTTP, unauthenticated DNS, Telnet, plain FTP)
are trivially readable, usernames, passwords, and content pass in cleartext. For HTTPS-protected
traffic, the attacker cannot read the content directly because TLS encrypts it end-to-end, but the
attacker can still see which servers are being contacted (via the TLS SNI field), can perform a
downgrade or SSL-stripping attack to trick a victim into using plain HTTP first, or can attempt to
present a forged certificate, which a properly configured browser and a certificate that fails
validation will reject and warn the user about. A MITM position also enables **packet injection**
(covered further in 3.1.d) and selective traffic dropping, the attacker doesn't have to be
passive; it can actively break specific connections or redirect specific requests.

### Detection and defense
Several technical controls address ARP spoofing directly:

- **Dynamic ARP Inspection (DAI)**, a switch feature that validates ARP packets against a trusted
  binding table (built from DHCP snooping records of which MAC is legitimately assigned which IP)
  and drops ARP replies that don't match, before they ever reach other hosts.
- **Static ARP entries**, manually configuring the correct IP-to-MAC mapping for critical devices
  (like the default gateway) so the OS ignores any ARP reply that tries to change it. This does not
  scale to large networks but is common for high-value hosts.
- **ARP monitoring tools** (e.g. arpwatch-style software), watch for a MAC address suddenly
  claiming an IP address that was previously mapped to a different MAC, which is the signature of
  an active spoofing attempt, and alert an analyst.
- **Network segmentation (VLANs)**, ARP spoofing only works within the same broadcast domain (the
  same local subnet/VLAN); segmenting sensitive hosts onto their own VLAN limits which devices can
  even attempt to spoof them.
- **Encryption end-to-end (TLS/HTTPS, VPN)**, does not stop the MITM positioning itself, but limits
  what the attacker gains from occupying that position, since the payload stays confidential and
  tamper-evident even while transiting the attacker's machine.

The coding problem in `problem/` asks you to scan a stream of observed ARP replies for the
telltale signature of spoofing: a MAC address that suddenly, and repeatedly, claims ownership of an
IP address that a different MAC had already claimed, exactly the heuristic that real ARP-watch
tools use.

## Key terms
- **Man-in-the-middle (MITM)**, an attack where an adversary secretly relays and can observe or
  alter traffic between two parties who believe they are communicating directly.
- **ARP (Address Resolution Protocol)**, the protocol that maps IP addresses to MAC addresses on a
  local network; has no built-in authentication.
- **ARP spoofing / ARP cache poisoning**, sending forged ARP replies to make a victim's device (or
  the gateway) associate a legitimate IP address with the attacker's MAC address.
- **Gratuitous ARP**, an unsolicited ARP reply, which devices accept and cache even though they
  never asked the question, enabling spoofing.
- **Dynamic ARP Inspection (DAI)**, a switch-level control that validates ARP packets against a
  trusted binding table and drops forged ones.

## Common misconceptions
- "HTTPS fully protects you from a man-in-the-middle." → HTTPS encrypts and authenticates the
  content of the connection, preventing the attacker from reading or silently modifying it without
  detection, but it does not stop the attacker from occupying the MITM position in the first place,
  seeing which servers you connect to, or degrading service.
- "ARP spoofing requires access to the router." → It requires only that the attacker be on the same
  local network/broadcast domain as the victim (e.g. the same Wi-Fi or switch segment), no router
  or gateway access is needed, since ARP replies are sent directly between hosts on the LAN.

## Try it
- **Simulation:** Inspect a stream of ARP replies for a target IP
  and decide whether each is legitimate or a spoofing attempt, reaching the scoring goal.
- **Coding problem:** Scan a log of observed ARP replies and flag IP addresses that
  show the spoofing signature (a second MAC claiming an IP already bound to a different MAC).
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-77 (Guide to IPsec VPNs, background on Layer 2 threats), rebuilt as original
  prose above; reference copy at `vendor/nist/sp800-77-l2-threats.md`.
- Reference: Open Security Training, "ARP and Layer 2 Attacks", rebuilt equivalent at
  `vendor/reference/3.1.c-arp-spoofing-ref.md`.
- Practice: Cybrary network-attacks module (ARP spoofing lab), rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/LetsDefend-Free-Cybersecurity-Resources/`.
