# 3.2.c, Layered network defense overview

> **Unit 3 · 3.2 Protecting Networks: Managerial & Wireless Security**
> **AP Learning Objective(s):** 3.2.B, 3.2.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain the principle of defense in depth, place a given security
control at the correct layer of a layered network defense model, and evaluate why relying on any
single control creates a single point of failure.

## Lesson

### Why one control is never enough
Every control studied so far in Unit 3, DNS protections (3.1.b), ARP/MITM defenses (3.1.c),
encryption against packet sniffing (3.1.d), strong Wi-Fi protocols (3.2.a), and managerial policy
(3.2.b), addresses a specific threat at a specific point. None of them, alone, protects an
organization completely. **Defense in depth** (also called layered defense) is the security
principle that an organization should never rely on a single control to stop an attack; instead,
multiple independent layers of controls should each be capable of stopping or slowing an attacker,
so that a failure or bypass of any one layer does not immediately result in a full compromise. The
core justification is straightforward: every individual control has known weaknesses, undiscovered
weaknesses, or can be misconfigured, a firewall rule can be written incorrectly, a patch can be
delayed, an employee can be tricked by a sufficiently convincing phishing email. Depth ensures that
a single point of failure does not become a single point of total compromise.

### A layered model of network defense
While organizations describe their layers differently, a commonly taught model orders defense from
the outside in:

1. **Perimeter layer**, controls at the boundary between the organization's network and the
   public internet: firewalls, intrusion prevention systems (IPS), and DNS filtering. This layer
   tries to stop obviously malicious traffic before it ever reaches internal systems.
2. **Network layer**, controls inside the perimeter that limit lateral movement and segment
   traffic: VLANs, network segmentation, internal firewalls between segments, and secure Wi-Fi
   protocols (WPA3, 3.2.a) protecting the wireless portion of the internal network. Even if an
   attacker gets past the perimeter, network-layer segmentation limits how far they can move.
3. **Host layer**, controls on individual devices: endpoint antivirus/EDR (endpoint detection and
   response), host-based firewalls, and OS patching. This layer assumes network-layer controls may
   fail and protects the device itself.
4. **Application layer**, controls built into the software running on hosts and servers: input
   validation, secure coding practices, web application firewalls (WAF), and authentication/
   authorization logic within the application itself.
5. **Data layer**, controls protecting the data itself regardless of where it travels or who has
   network access: encryption at rest and in transit, data loss prevention (DLP) tooling, and
   access controls tied to data classification. This is the innermost layer, even if every outer
   layer fails and an attacker reaches the data, strong data-layer controls (like encryption with
   keys the attacker doesn't have) can still prevent the data from being usable.
6. **Human/managerial layer**, not a network location at all, but a layer that spans all the
   others: security awareness training, the Acceptable Use Policy, least-privilege access review,
   and incident response procedures (3.2.b). This layer is what keeps every technical layer
   correctly configured, monitored, and improved over time, and it is often the layer that catches
   what automated controls miss (an employee reporting a suspicious email that slipped past a spam
   filter).

### Mapping this unit's controls to layers
Every control this unit has covered fits somewhere in this model, which is exactly the point of
studying them together rather than in isolation: DNSSEC and source-port randomization (3.1.b) sit
at the network/perimeter layer, protecting the name-resolution step traffic depends on before it
even reaches its destination. Dynamic ARP Inspection and VLAN segmentation against ARP spoofing
(3.1.c) sit at the network layer. TLS/HTTPS encryption defeating the value of packet capture (3.1.d)
sits at the data layer (protecting the payload) even though the capture itself might happen at any
layer. WPA3 (3.2.a) sits at the network layer, specifically protecting the wireless segment.
Managerial controls (3.2.b) sit at the human/managerial layer, spanning and reinforcing every other
layer.

### Why depth beats a single "best" control
A student might reasonably ask: if WPA3 is strong and DNSSEC is strong, why not just deploy the
single strongest control and skip the rest? The answer is that different controls defend against
fundamentally different attack vectors that do not overlap. WPA3 does nothing to stop DNS cache
poisoning; DNSSEC does nothing to stop an ARP-spoofing MITM on the local network; strong encryption
does nothing to stop a socially engineered employee from handing over a password directly. An
attacker only needs to find the one vector that is weakest, the entire discipline of "attack
surface" thinking is about recognizing that an organization is only as secure as its weakest
control, at whichever layer that weakness happens to exist. Depth means an attacker who defeats one
layer's control still has to defeat the next layer's control, and the next, multiplying the
difficulty and the chance of detection along the way (each additional layer is also another
opportunity to notice the attack in progress).

### Ordering an incident by layer
The coding problem in `problem/` gives you a list of security controls (each labeled with what it
protects and how) and asks you to sort them into the correct layer of the defense-in-depth model, directly practicing LO 3.2.C, and reinforcing that every control studied across this entire unit
has a specific, identifiable place in the bigger picture.

## Key terms
- **Defense in depth (layered defense)**, the principle of using multiple independent security
  layers so that failure of any single control does not result in full compromise.
- **Perimeter layer**, the boundary between an internal network and the public internet (firewall,
  IPS, DNS filtering).
- **Network layer**, internal segmentation and traffic control (VLANs, internal firewalls, Wi-Fi
  security).
- **Host layer**, controls on individual devices (endpoint antivirus/EDR, host firewalls,
  patching).
- **Data layer**, controls protecting data itself (encryption at rest/in transit, DLP).
- **Single point of failure**, any control whose failure alone results in a complete compromise,
  which defense in depth is specifically designed to avoid.

## Common misconceptions
- "The strongest single control is better than several weaker ones." → Different controls defend
  against different, non-overlapping attack vectors; an attacker only needs to find the one gap
  a single-control strategy leaves open. Depth matters more than any individual control's strength.
- "Managerial controls (policy, training) aren't really part of network defense." → The
  human/managerial layer spans and reinforces every technical layer, it is what keeps technical
  controls correctly configured and catches what automated tools miss, making it a genuine and
  necessary layer, not an afterthought.

## Try it
- **Simulation:** Sort security controls into their correct
  defense-in-depth layer, reaching the scoring goal.
- **Coding problem:** Given a list of controls, assign each to its correct layer in
  the defense-in-depth model.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-53 Rev. 5 (control baselines across families), rebuilt as original prose
  above; reference copy at `vendor/nist/sp800-53-defense-in-depth.md`.
- Reference: NSA/CISA "Defense in Depth" guidance summary, rebuilt equivalent at
  `vendor/reference/3.2.c-defense-in-depth-ref.md`.
- Practice: Cybrary network-defense-architecture module, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/LetsDefend-Free-Cybersecurity-Resources/`.
