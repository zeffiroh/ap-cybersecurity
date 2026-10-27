# 3.1.a, TCP/IP fundamentals and network topology flaws

> **Unit 3 · 3.1 Network Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 3.1.A
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Describe how the TCP/IP protocol stack works, identify structural
weaknesses in common network topologies, and explain how those weaknesses create attack surfaces
that adversaries exploit.

## Lesson
Every network attack starts with a target: a device, a service, or a data stream that an attacker
wants to reach, disrupt, or spy on. To understand how attacks work, and how defenses fail, you
first need to understand the underlying plumbing. That plumbing is **TCP/IP**, a family of
protocols that governs how data moves between any two points on the internet or a private network.

**The protocol stack.**
Network communication is organized into layers, each responsible for one job. The TCP/IP model
uses four layers:

1. **Application layer**, the program the user sees (a web browser, an email client, SSH). Data
   here is in human-readable or application-specific formats: HTTP, DNS, SMTP, etc.
2. **Transport layer**, TCP (Transmission Control Protocol) and UDP (User Datagram Protocol)
   live here. TCP breaks data into numbered **segments**, delivers them reliably, and acknowledges
   receipt. UDP is faster but offers no delivery guarantee. Port numbers (e.g., 443 for HTTPS,
   53 for DNS) identify which application on a host should receive the data.
3. **Internet layer**, IP (Internet Protocol) handles **routing**: it assigns each device an IP
   address and determines the path a packet takes across networks. IPv4 addresses are 32-bit
   dotted-decimal numbers (e.g., 192.168.1.1). IPv6 addresses are 128-bit hexadecimal.
4. **Network access layer**, governs how bits move over a physical medium (Ethernet, Wi-Fi).
   Devices on the same local segment are identified by **MAC addresses** (48-bit hardware IDs).

When you visit a website, your browser (application layer) passes data to the OS, which wraps it
in a TCP segment (transport), then an IP packet (internet), then an Ethernet or Wi-Fi frame
(network access). Each layer adds a **header**, its own metadata. At the destination, each layer
strips its header off, reading only what belongs to it. This layering is called **encapsulation**.

**Structural weaknesses built into TCP/IP.**
TCP/IP was designed in the 1970s for a cooperative research network, not an adversarial global
internet. Trust was assumed. That design philosophy left several structural gaps:

- **IP addresses are not authenticated.** A host can claim any IP address in a packet header. An
  attacker can craft packets with a forged source address, called **IP spoofing**, and the
  receiving host has no built-in way to verify the claim.
- **TCP handshakes are stateful but not encrypted.** The three-way handshake (SYN, SYN-ACK, ACK)
  that establishes a connection uses predictable sequence numbers in early implementations. An
  attacker who can predict the next sequence number can inject data into or hijack an existing
  session without knowing the user's password.
- **ARP operates on trust.** The Address Resolution Protocol maps IP addresses to MAC addresses on
  a local segment. Any host can broadcast a false ARP reply and redirect traffic, this is
  covered in depth in atom 3.1.c.
- **DNS relies on caching and forgeable replies.** The Domain Name System translates names to IPs
  and caches results. Forged DNS replies can redirect traffic to attacker-controlled servers, covered in 3.1.b.

**Topology flaws.**
The physical or logical arrangement of a network, its **topology**, also shapes the attack
surface. A **hub-based** topology broadcasts every frame to every port; any device on the segment
can capture all traffic with a passive sniffer (3.1.d). Switches fixed that by sending frames only
to the correct port, but attackers found ways to defeat switches too: **MAC flooding** fills a
switch's address table with fake entries until it falls back to broadcasting like a hub, and **ARP
spoofing** tricks the switch into routing traffic through the attacker.

A **flat network** with a single broadcast domain gives every internal host direct visibility to
every other. If one workstation is compromised, the attacker can reach servers, printers, and
cameras without crossing a firewall. **Network segmentation**, dividing a network into subnets or
VLANs with controlled inter-segment routing, limits this blast radius.

**Why the layered model matters for defense.**
Each layer of the stack is a potential interception or injection point. Understanding which layer
an attack targets tells you which layer the defense must operate at. IP spoofing is fought at the
internet layer (ingress filtering at routers). Malicious HTTP payloads are fought at the
application layer (web application firewalls). This specificity is what the AP framework means by
"Analyze Risk": a defender who cannot name the layer cannot choose the right countermeasure.

The simulation for this skill lets you step through a network connection packet by packet, labeling
each header field and identifying which ones are forgeable. The coding problem asks you to parse a
synthetic packet log and flag entries that exhibit IP spoofing indicators.

## Key terms
- **TCP/IP**, the suite of protocols governing internet communication, organized into four layers: application, transport, internet, network access.
- **Encapsulation**, each layer wraps data from the layer above in its own header, creating a protocol data unit (frame, packet, segment, data).
- **IP address**, a numerical label assigned to a device at the internet layer; identifies source and destination of packets. IPv4 = 32-bit; IPv6 = 128-bit.
- **MAC address**, a 48-bit hardware identifier used at the network access layer for communication within a single local segment.
- **Port number**, a 16-bit number at the transport layer identifying which application service should handle incoming data.
- **IP spoofing**, forging the source IP address in a packet header to hide the sender's true identity or impersonate another host.
- **Three-way handshake**, the TCP connection setup sequence: SYN (client), SYN-ACK (server), ACK (client).
- **Network topology**, the arrangement (physical or logical) of devices and links in a network; shape determines broadcast domains and attack surface.
- **Network segmentation**, dividing a network into isolated subnets or VLANs to limit lateral movement after a breach.
- **MAC flooding**, sending large numbers of fake MAC entries to overflow a switch's table, causing it to broadcast all frames.

## Common misconceptions
- "Switches make sniffing impossible." → Switches reduce passive sniffing but MAC flooding and ARP spoofing let attackers redirect traffic through their own machine even on switched networks.
- "IP addresses prove identity." → IP addresses are easily forged; they are routing labels, not authentication tokens. Actual identity verification requires higher-layer mechanisms (TLS certificates, authenticated protocols).
- "A firewall on the perimeter is enough." → Flat internal networks let a compromised internal host reach everything; segmentation is needed to contain breaches inside the perimeter.

## Try it
- **Simulation:** Trace a TCP connection through all four layers, identify which header fields an attacker could forge in a synthetic packet log, and reach a score of 5.
- **Coding problem:** Parse a list of synthetic packet records and return the indices of packets that exhibit IP spoofing (source IP outside the expected subnet).
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Open Security Training (network fundamentals modules), rebuilt as original prose above; local equivalent notes in `vendor/web/open-security-training/`.
- Reference: MIT OCW 6.829 Computer Networks lecture notes, see `vendor/web/mit-ocw/6.829/`.
- Practice: SANS Cyber Aces online (TCP/IP module), rebuilt locally as the simulation.
- Repo: CSIRT-MU/edu-resources, `vendor/repos/csirt-mu-edu-resources`.
