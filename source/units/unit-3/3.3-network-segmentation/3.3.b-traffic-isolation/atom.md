# 3.3.b, Traffic isolation and zero-trust segmentation

> **Unit 3 · 3.3 Protecting Networks: Segmentation**
> **AP Learning Objective(s):** 3.3.B, 3.3.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain the limitations of traditional network segmentation, define the core principles of Zero Trust Network Architecture (ZTNA), and apply traffic isolation and microsegmentation strategies to prevent lateral movement.

## Lesson

Traditional network security relies on a "perimeter" model, often compared to a castle with a moat. Under this design, the organization builds strong defenses at the network perimeter (using firewalls and intrusion prevention systems) to keep attackers out. However, once a user or device crosses this boundary, by entering the correct credentials, connecting to an internal port, or establishing a VPN connection, they are granted broad, implicit trust. They are assumed to be safe, allowing them to communicate freely with other internal devices. 

This model has proven dangerously obsolete. Once an adversary gains a foothold inside the perimeter (such as through phishing or a physical intrusion), they exploit this implicit trust to move laterally from machine to machine. Traditional VLAN segmentation divides the network into large zones (such as "Employees" or "Servers"), but within each VLAN, devices can still freely talk to one another without passing through a security checkpoint. If one employee's laptop is compromised, the attacker can scan and attack every other device in the same Employee VLAN.

### The Zero Trust Paradigm

To address this vulnerability, security architects developed the **Zero Trust** model. The foundational mantra of Zero Trust is: **Never trust, always verify.**

In a Zero Trust Network Architecture (ZTNA), network access is never granted implicitly based on a user's physical or logical location (e.g., being plugged into an office ethernet port, or connected to the corporate Wi-Fi). Instead, every request to access a resource must be explicitly authenticated, authorized, and encrypted before access is granted. The location of the device is treated as an untrusted variable, just like the public internet.

A Zero Trust architecture is built on three core principles:
1. **Verify explicitly:** Always authenticate and authorize access based on all available data points, including user identity, device health, location, service or workload context, and anomaly detection.
2. **Use least privilege access:** Limit user and device access with Just-In-Time (JIT) and Just-Enough-Access (JEA) policies, protecting data with role-based access control and microsegmentation.
3. **Assume breach:** Minimize the blast radius of an attack by segmenting access by network, user, devices, and application. Encrypt all sessions, use analytics to gain visibility, and monitor traffic continuously to detect anomalies.

### Traffic Isolation and Microsegmentation

To implement "assume breach" and limit lateral movement, networks must move beyond coarse VLANs to **microsegmentation** and strict **traffic isolation**.

#### 1. Microsegmentation
Microsegmentation is a security technique that enables fine-grained security policies to be applied to individual workloads or devices, down to the single host level. Instead of grouping 500 employee laptops into one VLAN and letting them communicate directly, microsegmentation treats each device as its own isolated segment. Security policies are enforced by software-defined networking (SDN) controllers or endpoint-based host firewalls. For example, employee laptops are forbidden from communicating with each other entirely; they may only communicate with specific central servers and the internet.

#### 2. Private VLANs (PVLANs)
At the physical switch level, traffic isolation can be enforced using Private VLANs. A PVLAN divides a primary VLAN's broadcast domain into sub-domains using three types of switch ports:
- **Isolated ports:** Ports that cannot communicate with any other port in the same PVLAN, except for Promiscuous ports. Traffic from an isolated port is blocked from reaching other isolated ports, even though they share the same subnet.
- **Community ports:** Ports that can communicate with other community ports in the same community group, and with Promiscuous ports, but are isolated from all other communities and isolated ports.
- **Promiscuous ports:** Ports that can communicate with all ports in the PVLAN, including isolated and community ports. Typically, routers and default gateways plug into promiscuous ports so all hosts can reach the internet and DNS servers.

### How Zero Trust Halts Attacks

Consider a ransomware attack in two scenarios:

*   **Scenario A (Traditional VLANs):** An attacker compromises a reception desk PC on VLAN 10. Because the reception PC shares VLAN 10 with the HR team, the finance workstations, and printers, the ransomware scans the subnet, finds active ports, uses an exploit (like EternalBlue), and encrypts 50 other machines within minutes.
*   **Scenario B (Zero Trust & Microsegmentation):** The reception PC is connected to an Isolated PVLAN port. When the malware attempts to scan its local subnet, the network switch drops the packets. The malware cannot communicate with any peer workstations. To access a server, the request must pass through a Zero Trust proxy that verifies the machine's security posture. Because the workstation's posture is compromised (unusual outbound scans detected), its token is revoked. The blast radius is limited to exactly one machine.

## Key terms
- **Zero Trust**, A cybersecurity paradigm centered on the belief that organizations should not automatically trust anything inside or outside its perimeters; instead, they must verify anything and everything trying to connect.
- **Implicit trust**, The practice of automatically trusting a device or user based on their network location, IP address, or initial login.
- **Microsegmentation**, A method of creating secure zones in data centers and cloud environments to isolate workloads from one another and secure them individually.
- **Private VLAN (PVLAN)**, A layer-2 isolation mechanism that divides a VLAN into sub-domains, preventing devices in the same subnet from communicating directly.
- **Isolated port**, A PVLAN port that is completely blocked from talking to any other host in the same VLAN, except the gateway (promiscuous port).
- **Promiscuous port**, A PVLAN port that can communicate with all other ports (isolated, community, promiscuous) in the VLAN, typically reserved for gateways.

## Common misconceptions
- "Zero Trust means we don't trust our employees." → Zero Trust is a technical posture, not a human resource policy. It protects employees' credentials from being abused by automating checks and preventing compromised devices from spreading malware.
- "Once we set up VLANs, we have achieved Zero Trust." → VLANs are a tool for traditional segmentation. Zero Trust requires continuous verification of identity and device health, not just IP address routing. A flat VLAN network still relies on implicit trust within the subnet.

## Try it
- **Simulation:** Configure PVLAN port types (Promiscuous, Isolated, Community) for a corporate branch network to isolate workstations while allowing gateway access.
- **Coding problem:** Implement a simulation of a Zero Trust Access Proxy that evaluates connection requests based on user role, device posture, and IP location.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-207 "Zero Trust Architecture", rebuilt as original prose above; see `vendor/web/nist/sp800-207/` notes.
- Reference: GeeksforGeeks (Private VLANs), rebuilt locally; no external fetch required.
- Practice: SANS Zero Trust Whitepaper, rebuilt locally.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
