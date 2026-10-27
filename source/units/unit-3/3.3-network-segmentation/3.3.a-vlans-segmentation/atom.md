# 3.3.a, VLANs and network segmentation

> **Unit 3 · 3.3 Protecting Networks: Segmentation**
> **AP Learning Objective(s):** 3.3.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain what a VLAN is, describe how network segmentation limits the spread of an attack, and assign hosts to VLANs to enforce separation between different trust zones.

## Lesson
Networks that treat every connected device as equally trusted are far more dangerous than they appear. When an attacker compromises one machine on a flat network, a network where every device can freely reach every other device, they inherit access to printers, file servers, cameras, payroll databases, and anything else plugged into the same broadcast domain. The solution is segmentation: dividing the network into smaller, separated zones so that a breach in one zone cannot automatically reach the others.

**What is a VLAN?**

A Virtual Local Area Network (VLAN) is a logical grouping of devices configured in network switch software rather than by physical cabling. A single physical switch can support dozens of VLANs simultaneously. Each VLAN behaves like its own isolated broadcast domain: traffic broadcast on VLAN 10 never reaches devices on VLAN 20 unless a router or layer-3 switch explicitly forwards it.

Think of VLANs like walls inside a building. The building is one physical structure (the switch), but the walls separate HR from Engineering from the guest lobby. A fire breaking out in the lobby does not automatically spread to the server room, the wall is in the way.

In practice, a network administrator assigns each switch port to a VLAN by ID number (a number from 1 to 4094). A workstation plugged into a port assigned to VLAN 10 sends traffic that stays on VLAN 10. To communicate with a device on VLAN 20, the traffic must leave VLAN 10, pass through a router (a process called inter-VLAN routing), and enter VLAN 20, only if a firewall rule permits it.

**Why segmentation reduces risk**

When an attacker compromises a guest laptop on the visitor Wi-Fi VLAN, the damage stays within that VLAN. The attacker cannot reach the corporate file server on the internal employee VLAN because there is no physical path between them inside the switch, and the router only forwards traffic that an access control list explicitly permits. Without segmentation, that same compromised guest laptop could scan and reach every device on the network.

Segmentation also limits lateral movement. Lateral movement is the technique attackers use to hop from one compromised system to a more valuable target. A properly segmented network means that even after gaining a foothold, the attacker hits a wall. Each new zone requires a fresh exploit against a new access control boundary.

**Designing a segmentation scheme**

A common pattern in small and medium organizations uses four VLANs:

- Management VLAN, for switches, routers, and infrastructure devices only. Never exposed to users.
- Internal employee VLAN, workstations and printers for staff.
- Server VLAN, databases, file shares, application servers.
- Guest/IoT VLAN, visitor laptops, smart TVs, building sensors.

The firewall rules between these VLANs follow the principle of least privilege: employees can reach servers on specific ports (port 443 for HTTPS, port 445 for file sharing), but guest devices cannot reach any internal VLAN at all. IoT devices can only reach the internet, not internal resources.

**Trunk ports and tagged traffic**

When a single switch port must carry traffic from multiple VLANs, for example, the port connecting a switch to a router, it operates in trunk mode. Trunk ports add an 802.1Q tag to each Ethernet frame that identifies its VLAN. The router strips the tag, applies its routing and firewall rules, and re-tags the outbound frame for the destination VLAN. Access ports, the ports where end-user devices plug in, carry only one VLAN and do not use tags; the tag is invisible to the endpoint.

**The simulation**

In the simulation you will place hosts into VLANs and then test whether specific traffic flows between those hosts are blocked or allowed. The goal is to configure the VLAN assignments so that a simulated attacker who compromises a guest device cannot reach any internal server. This mirrors the real-world task a network engineer performs when designing a segmented campus network.

**The coding problem**

`problem/` asks you to implement a function that accepts a host-to-VLAN mapping and a list of traffic flows, and returns which flows are blocked by segmentation rules. This is the decision logic a switch's VLAN engine performs on every frame.

## Key terms
- **VLAN (Virtual Local Area Network)**, a logical broadcast domain created in switch software, isolating traffic between groups of ports without requiring separate physical switches.
- **Network segmentation**, dividing a network into zones with controlled, limited connectivity between them to reduce the blast radius of a breach.
- **Broadcast domain**, the set of devices that receive a broadcast frame; VLANs confine broadcasts to only the members of that VLAN.
- **Trunk port**, a switch port that carries tagged frames for multiple VLANs, used on uplinks between network devices.
- **Access port**, a switch port assigned to exactly one VLAN, used for end-user devices.
- **Inter-VLAN routing**, the process of forwarding traffic between VLANs through a router or layer-3 switch, where firewall rules can be applied.
- **Lateral movement**, the technique by which an attacker hops from one compromised host to another within a network.

## Common misconceptions
- "A VLAN is the same as a separate physical network." A VLAN is a logical separation on shared hardware. Physical separation (an air gap) provides stronger isolation, but VLANs are practical and sufficient for most environments when firewall rules are enforced at the routing boundary.
- "Setting up VLANs means attackers definitely cannot cross them." VLANs stop direct layer-2 traffic. If the router/firewall rules are misconfigured to allow all inter-VLAN traffic, segmentation is defeated. The firewall policy at the routing layer is what enforces the separation.
- "The management VLAN is fine to share with users for convenience." Placing user devices on the management VLAN exposes switch and router administration interfaces. The management VLAN must always be isolated.

## Try it
- **Simulation:** Assign hosts to VLANs and verify that a compromised guest device cannot reach any server, reaching the target score of 5 correct decisions.
- **Coding problem:** Given a host-to-VLAN map and a list of traffic flows, return which flows segmentation rules block.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST, rebuilt as original prose above; see `vendor/web/nist/` for SP 800-125B on network virtualization security.
- Reference: GeeksforGeeks (VLAN overview), rebuilt locally; no external fetch required.
- Practice: Cybrary network segmentation micro-lab, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
