---
deck:
  title: Network Vulnerabilities & Attacks
  kicker: Class 12
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 12
  description: DNS attacks, spoofing, sniffing, ARP poisoning, and session hijacking, attacking the plumbing directly.
  topics: [DNS Attacks, Spoofing, Packet Capture, Sniffing, MITM, Session Hijacking]
---

---
title: Network Vulnerabilities & Attacks
cover: true
---
:::text class=sub
Every foundational network component and protocol introduced in the previous module is also a potential vector for exploitation. Understanding how these elements can be subverted is essential to securing modern network infrastructures.
:::
:::list style=chips
- DNS Attacks
- ARP Spoofing
- Session Hijacking
:::
::::columns
::col::
:::callout
**Foundational Protocols as Attack Surfaces**
Each protocol studied, such as DNS, ARP, and TCP, was designed for functionality, not security. This inherent weakness is frequently exploited by adversaries to compromise network integrity and confidentiality.
:::
::col::
:::callout
**Common Exploitation Patterns**
Attackers often leverage protocol trust models, session predictability, and lack of encryption to intercept, redirect, or impersonate network entities. These methods remain effective in environments lacking proper segmentation or monitoring.
:::
::::

:::image src="images/12_protocol_trust_attack_surface.png" alt="Diagram showing DNS, ARP, TCP, and IP protocol layers with red attack arrows pointing at each protocol, annotated with attack type names (cache poisoning, spoofing, SYN flood, session hijacking), clean technical style, white background" caption="Classic protocols were designed for functionality in trusted networks, each trust assumption becomes an exploitable attack surface in adversarial environments" width=full
:::

:::notes
Every protocol and infrastructure component introduced in foundational networking, be it DNS, ARP, TCP/IP, or routing mechanisms, represents a potential attack surface. These technologies were developed in an era where network trust was assumed and security was not a primary design consideration. As such, they inherently lack the robustness required to defend against modern adversarial behaviors.

For instance, the Domain Name System (DNS), which translates human-readable domain names into IP addresses, is vulnerable to cache poisoning (CVE-1999-0028), spoofing, and tunneling attacks. These vulnerabilities can lead to man-in-the-middle scenarios or data exfiltration, as outlined in NIST SP 800-81 on Secure Domain Name System (DNS) Deployment. DNS was designed in the early 1980s with the assumption that DNS resolvers would communicate with trusted servers; the protocol includes no mechanism for resolvers to verify that they are receiving authentic responses. This fundamental design gap is what cache poisoning exploits.

Similarly, the Address Resolution Protocol (ARP), which maps IP addresses to MAC addresses within a local network, is susceptible to ARP spoofing. This allows attackers to perform session hijacking or conduct man-in-the-middle attacks by poisoning ARP tables, a technique well-documented in RFC 6099 and various MITRE ATT&CK entries such as T1071.002 (Application Layer Protocol: DNS) and T1040 (Network Sniffing). ARP was defined in RFC 826 in 1982 and operates entirely on honor: any device on the network can send an ARP reply claiming to be any other device, and neighboring devices will update their ARP cache accordingly without any verification.

Session hijacking, another critical threat, exploits weaknesses in session management protocols. It enables attackers to assume control of a legitimate user session, often by predicting or stealing session tokens. This aligns with ISO/IEC 27001 controls regarding secure session management and access control. The sophistication of session hijacking has evolved from early TCP sequence number prediction attacks (1990s) to modern cookie theft via cross-site scripting, but the underlying principle, stealing or predicting the credential that proves identity, remains constant.

A recurring theme across all these attacks is the exploitation of implicit trust: DNS trusts that responses come from authoritative sources; ARP trusts that replies correspond to the claimed IP address; session management trusts that whoever presents a session token is the legitimate session owner. Modern security architectures address this by adopting zero-trust principles (NIST SP 800-207), which demand verification of identity and integrity for every transaction regardless of network position.

Understanding these vulnerabilities is not merely academic, it is foundational to implementing effective network defense strategies. Each protocol must be hardened using cryptographic protections, monitoring, and network segmentation to mitigate risks effectively. This class builds directly on Class 11's protocol foundations to show exactly where those foundations crack under adversarial pressure.
:::

%%%

---
unit: Foundations
code: REC
title: The Network Layer as Attack Surface
---
:::callout style=soft
Every foundational network concept, from DNS resolution and IP addressing to packet routing and session management, has a corresponding class of attacks designed to exploit its inherent weaknesses.
:::

:::pullquote
To understand network attacks, one must first understand the protocols and mechanisms that enable communication.
:::

::::columns
::col::
:::text
The network layer serves as a critical attack surface due to its role in facilitating communication across systems. Each protocol and mechanism introduces potential vulnerabilities:
:::

:::list heading="Key Protocols and Their Attack Classes"
- **DNS** → Cache poisoning, tunneling, amplification DDoS
- **IP** → Spoofing, fragmentation attacks, IP scanning
- **TCP/UDP** → Session hijacking, SYN flooding, port scanning
- **ICMP** → Ping of death, smurf attacks
- **Routing** → Route poisoning, BGP hijacking
:::

::col::
:::table
| Layer        | Protocols       | Common Attack Vectors                     |
|--------------|------------------|-------------------------------------------|
| Application  | DNS, HTTP        | DNS spoofing, HTTP header injection       |
| Transport    | TCP, UDP         | SYN flood, UDP flood                      |
| Network      | IP, ICMP, BGP    | IP spoofing, Smurf attack, Route hijacking|
| Data Link    | Ethernet, ARP    | ARP spoofing, MAC flooding                |
:::
::::

:::steps
1. **Reconnaissance**, Attacker scans the target network to identify live hosts, open ports, and active protocols (MITRE ATT&CK T1046 – Network Service Scanning).
2. **Protocol Identification**, Attacker maps which protocols are in use (DNS, ARP, HTTP, BGP) and researches their documented vulnerabilities via CVE databases and MITRE ATT&CK.
3. **Trust Assumption Analysis**, Attacker identifies what each protocol trusts implicitly (e.g., DNS trusts unsolicited replies; ARP trusts gratuitous announcements; IP trusts source addresses are authentic).
4. **Exploit Selection**, Attacker selects the technique that best targets the exploitable trust assumption given the network topology and available tooling.
5. **Attack Execution**, Attacker injects forged traffic, poisoned cache entries, or crafted packets to subvert the targeted protocol's behavior.
6. **Objective Achievement**, Depending on goal: traffic redirection (DNS/ARP), credential theft (sniffing/session hijack), service disruption (DoS/amplification), or persistence.
:::

:::image src="images/12_attack_surface_map.png" alt="TCP/IP layer stack diagram with attack vectors radiating out from each layer as labeled arrows: Application (DNS spoofing, HTTP injection), Transport (SYN flood), Network (IP spoofing, BGP hijack), Data Link (ARP spoofing, MAC flood), professional textbook style" caption="Mapping attacks to protocol layers: every layer of the stack has associated attack classes that exploit its unique design assumptions" width=full
:::

:::notes
The network layer is fundamentally the infrastructure that enables communication between devices in a networked environment. As such, it becomes a primary target for attackers seeking to disrupt, intercept, or manipulate data flows. Each protocol that operates at this layer introduces potential vulnerabilities due to design limitations, implementation flaws, or misconfigurations.

For instance, the Domain Name System (DNS), which translates human-readable domain names into IP addresses, is susceptible to cache poisoning attacks such as those described in CVE-2008-1447. These attacks allow adversaries to redirect traffic to malicious servers. Similarly, the Internet Protocol (IP) is vulnerable to spoofing attacks where an attacker falsifies the source IP address to impersonate another system or bypass access controls.

At the transport layer, Transmission Control Protocol (TCP) is prone to session hijacking and denial-of-service (DoS) attacks like the SYN flood, which exploits the three-way handshake process. User Datagram Protocol (UDP), being connectionless, is often abused in amplification attacks such as DNS amplification, where attackers leverage publicly accessible DNS servers to overwhelm targets with large volumes of traffic.

The Internet Control Message Protocol (ICMP), used for diagnostic purposes, has been weaponized in attacks like the "Ping of Death" and "Smurf" attacks, which exploit how systems handle ICMP packets to cause buffer overflows or amplify traffic for DDoS purposes. The Ping of Death (CVE-1999-0128) exploited the fact that certain operating systems could not handle ICMP Echo Request packets larger than 65,535 bytes, causing kernel crashes. The Smurf attack amplified traffic by sending ICMP echo requests to a network's broadcast address with the victim's spoofed IP, causing every host on the network to respond simultaneously to the victim.

Routing attacks represent a higher-level concern. BGP (Border Gateway Protocol), the protocol that exchanges routing information between autonomous systems on the internet, relies almost entirely on trust between peer networks. BGP hijacking, deliberately announcing more-specific or alternative routes for address blocks that belong to another organization, can divert large volumes of internet traffic through attacker-controlled infrastructure. The 2018 Route Origin Validation incidents and the 2010 China Telecom BGP leak (which temporarily rerouted 15% of global internet traffic through China) illustrate the real-world impact of routing protocol weaknesses.

From a standards perspective, NIST Special Publication 800-53 provides guidelines on securing network communications, emphasizing the importance of validating inputs, implementing secure configurations, and monitoring network traffic for anomalies. ISO/IEC 27001 also outlines controls for managing network security risks through risk assessment and continuous improvement processes.

Understanding these foundational concepts allows cybersecurity professionals to anticipate attack vectors and implement appropriate defensive measures. This principle aligns with the MITRE ATT&CK framework, which categorizes adversary behaviors based on the tactics, techniques, and procedures (TTPs) used at different stages of an attack lifecycle. By mapping known vulnerabilities to specific network functions, defenders can better prepare for and mitigate potential threats.
:::

%%%

---
unit: Attacks
code: DNS
title: DNS Attacks
---
:::callout style=soft
**DNS Spoofing (Cache Poisoning)** is a network-layer attack in which an adversary introduces false DNS records into a DNS resolver's cache. This causes legitimate domain name queries to resolve to malicious IP addresses controlled by the attacker, enabling traffic interception, phishing, or malware delivery.
:::

::::columns
::col::
:::list heading="Common DNS Attack Vectors" style=plain
- DNS Cache Poisoning
- DNS Tunneling
- DNS Amplification/Reflection DDoS
- Domain Hijacking
- Fast Flux Networks
:::
::col::
:::table
| Attack Type            | Objective                          | Impact                          |
|------------------------|------------------------------------|---------------------------------|
| Cache Poisoning        | Redirect traffic                   | MITM, phishing, malware spread  |
| Tunneling              | Exfiltrate data or bypass filters  | Data loss, C2 communication     |
| Amplification DDoS     | Overwhelm target with traffic      | Service unavailability          |
| Domain Hijacking       | Gain control of domain records     | Brand impersonation, fraud      |
| Fast Flux              | Rapidly change IP mappings         | Evasion of blacklists           |
:::
::col::
::::

:::flow
You request a legitimate domain (e.g., bank.example)
Resolver queries upstream DNS servers
Attacker injects forged reply with malicious IP
Resolver caches the fake record
You are redirected to attacker's server
Attacker serves malicious or fraudulent content
:::

:::image src="images/12_dns_cache_poisoning_flow.png" alt="Sequence diagram showing DNS cache poisoning attack: client queries resolver, attacker races to send forged reply before legitimate authoritative server, resolver caches fake record, subsequent clients are redirected to malicious IP, labeled with timing annotations showing the race condition" caption="DNS cache poisoning exploits the race between a legitimate DNS response and the attacker's forged reply, once cached, all users of that resolver are affected" width=full
:::

:::notes
DNS (Domain Name System), defined in RFC 1034 and RFC 1035, is the foundational protocol that translates human-readable domain names into IP addresses. Due to its critical role in internet communication and the historically stateless, unauthenticated nature of DNS responses, it has become a prime target for attackers.

DNS spoofing, also known as DNS cache poisoning (as referenced in CVE-2008-1447 and addressed in RFC 5452), exploits the trust DNS resolvers place in unsolicited replies. An attacker sends a forged DNS response to a resolver, mimicking an authoritative server's reply. If successful, the resolver caches the malicious record and serves it to subsequent users querying the same domain. This can lead to man-in-the-middle (MITM) attacks, credential theft, or malware distribution. The 2008 Kaminsky Attack (CVE-2008-1447), discovered by security researcher Dan Kaminsky, demonstrated that by flooding a resolver with forged responses across all 65,536 possible UDP source ports simultaneously, an attacker could reliably poison a cache within seconds. This vulnerability affected nearly every DNS implementation in use at the time and required emergency coordinated patching by virtually every major operating system and DNS software vendor.

The attack is particularly insidious because the user's browser displays the correct domain name, creating a false sense of legitimacy. Unlike phishing sites that use deceptive domains (e.g., paypa1.com), DNS spoofing preserves the authentic URL, making detection extremely difficult without additional security layers such as DNS Security Extensions (DNSSEC), as recommended by NIST SP 800-81.

**DNS Tunneling** is a separate but equally concerning attack class. Attackers embed data in DNS queries and responses, using the TXT, CNAME, or MX record types, to create a covert communication channel that can bypass firewalls and content filters. Because most organizations allow outbound DNS traffic, this technique is effective for data exfiltration and command-and-control (C2) communication. Tools like iodine, dns2tcp, and DNScat2 automate DNS tunneling and are commonly used by penetration testers and malicious actors alike. Detection requires analyzing DNS traffic for unusually high query volumes, long domain names, or unusual record types (MITRE ATT&CK T1071.004 – Application Layer Protocol: DNS).

**DNS Amplification DDoS** exploits open DNS resolvers, servers that respond to queries from any source, to amplify attack traffic. The attacker sends small DNS queries (typically requesting large ALL-type records) with a spoofed source address pointing to the victim. The resolver sends large responses to the victim, achieving amplification factors of 30–100x. Combined with a botnet, this can generate hundreds of Gbps of attack traffic against a target. The Spamhaus DDoS attack in 2013 reached 300 Gbps using this technique, briefly affecting internet routing across Europe.

Other DNS-based attacks include fast flux networks, where criminal infrastructure rapidly cycles through thousands of compromised hosts as DNS answers to evade IP-based blacklisting, and domain hijacking, where an attacker compromises a domain registrar account to redirect a domain's DNS records. These attacks highlight the need for secure DNS configurations, resolver hardening, and the deployment of security frameworks such as those outlined in ISO/IEC 27001 and the MITRE ATT&CK framework under the "Network Services" category (T1071.004).

The primary mitigation for DNS cache poisoning is DNSSEC, which adds cryptographic signatures to DNS records. However, DNSSEC deployment remains incomplete globally. Additional defenses include source port randomization (RFC 5452), Response Rate Limiting (RRL) on authoritative servers, and monitoring DNS traffic for anomalous patterns consistent with tunneling or amplification activity.
:::

%%%

---
unit: Attacks
code: SPF
title: IP Spoofing
---
:::callout style=soft
**IP spoofing** is a network-layer attack in which an attacker forges the source IP address in a packet header to impersonate another device. This technique is used to exploit trust relationships, evade detection, or facilitate other attacks such as Denial of Service (DoS) or man-in-the-middle scenarios.
:::

::::columns
::col::
:::list heading="Motivations for IP Spoofing" style=plain
- Circumvent IP-based access controls (e.g., firewall rules)
- Conceal the true origin of malicious traffic
- Exploit trust relationships in legacy or misconfigured systems
- Facilitate reflection/amplification DoS attacks
:::
::col::
:::table
| Technique              | Purpose                                 |
|-----------------------|-----------------------------------------|
| Source Address Spoofing | Impersonate trusted hosts               |
| Blind Spoofing         | Attack without bidirectional channel    |
| Non-blind Spoofing     | Maintain session for data exfiltration  |
:::
:::list heading="Common Protocols Exploited" style=chips
- TCP (with sequence number prediction)
- UDP (stateless, easier to spoof)
- ICMP (used in ping-based reconnaissance)
:::
::::

:::flow
Attacker selects victim's IP address as the spoofed source
↓
Attacker crafts packet with forged source IP in the IP header
↓
Packet is sent to an open reflector (DNS server, NTP server, Memcached instance)
↓
Reflector processes request and sends large response to the spoofed (victim) IP
↓
Victim receives amplified flood, attacker's address never appears in traffic
↓
Victim's bandwidth or server resources are exhausted (DoS achieved)
:::

:::image src="images/12_ip_spoofing_reflection.png" alt="Diagram showing IP spoofing in a reflection DDoS attack: attacker sends UDP queries to open DNS resolvers with victim IP as source, resolvers send large responses to victim, amplification factor shown with arrow sizes, attacker identity hidden" caption="IP spoofing enables reflection/amplification DDoS: the attacker's true address is never exposed because all responses are directed at the spoofed victim IP" width=full
:::

:::notes
IP spoofing is a foundational network attack that exploits the stateless nature of the Internet Protocol (IP), particularly in IPv4 environments where packet headers are not cryptographically protected. Defined broadly in RFC 791, IP does not inherently validate the source address of packets, making it possible for attackers to forge this field. This vulnerability is especially dangerous when combined with trust-based access control mechanisms, such as those relying on IP allowlists, which are still prevalent in legacy systems and misconfigured networks.

The technique is categorized into two types: **blind spoofing**, where the attacker has no ability to receive responses (common in one-way attacks like DoS), and **non-blind spoofing**, where bidirectional communication is maintained, often through sequence number prediction in TCP sessions. The latter was historically exploited in attacks such as those leveraging TCP sequence number prediction (CVE-1999-0016), where attackers could hijack sessions if they guessed the correct sequence number. The seminal "IP Spoofing Attacks and Hijacking Internet Sessions" paper by Kevin Mitnick and Tsutomu Shimomura in 1994 demonstrated non-blind TCP session hijacking in a high-profile attack against Shimomura's own systems, kicking off one of the most famous manhunts in cybersecurity history.

IP spoofing is also a critical enabler of **distributed denial-of-service (DDoS)** attacks, particularly in reflection and amplification attacks. For example, an attacker may spoof the victim's IP address as the source in DNS queries sent to open resolvers, causing large volumes of traffic to flood the target. In NTP amplification attacks, a similar technique achieves amplification factors of up to 556x, making it one of the most devastating DDoS vectors. This is documented in various NIST guidelines, including NIST SP 800-97.

A critical point about IP spoofing is its relationship with network topology: spoofing is far easier when the attacker does not receive responses (blind spoofing), since TCP's sequence number requirement makes full session impersonation difficult without a return path. Reflection DDoS works precisely because the spoofed victim receives the amplified response instead of the attacker, the attacker never needs to receive the traffic they generate. This asymmetry makes attribution extremely difficult in large-scale DDoS attacks.

Mitigation strategies include ingress and egress filtering (commonly known as **BCP 38** or RFC 2827), which blocks packets with source addresses that do not belong to the originating network. BCP 38 deployment by ISPs would significantly reduce the effectiveness of reflection attacks, yet its adoption remains incomplete globally. Additionally, the adoption of **IPsec** (RFC 4301) and **IPv6** with Secure Neighbor Discovery (SEND) can provide cryptographic integrity and reduce spoofing risks. Modern cloud DDoS scrubbing services and anycast network architectures also provide practical mitigation by absorbing and filtering spoofed-source attack traffic at geographically distributed scrubbing centers.

In enterprise environments, egress filtering, blocking outbound packets with source addresses not belonging to the enterprise's own IP space, is recommended by both NIST and the CIS Controls as a baseline network security configuration that prevents enterprise infrastructure from being used as a spoofing source in attacks against others.
:::

%%%

---
unit: Attacks
code: ARP
title: ARP Spoofing
---
:::callout style=soft
**Address Resolution Protocol (ARP) spoofing**, also known as ARP poisoning, is a local network attack wherein an attacker sends falsified ARP messages to associate their own Media Access Control (MAC) address with the IP address of another device, typically a gateway or router. This allows the attacker to intercept, modify, or block traffic intended for the legitimate device.
:::

::::columns
::col::
:::list heading="Key Concepts"
- ARP maps IP addresses to MAC addresses
- No authentication in standard ARP
- Local network (Layer 2) attack
- Enables man-in-the-middle (MITM)
:::
::col::
:::list heading="Common Attack Goals"
- Traffic interception
- Session hijacking
- Credential theft
- Lateral movement
:::
::col::
:::list heading="Typical Targets"
- Default gateways
- Workstations
- Servers on the LAN
:::
::::

:::flow
Attacker broadcasts forged ARP reply
Victim updates ARP table with attacker's MAC
Victim routes traffic to attacker instead of gateway
Attacker forwards or alters traffic
:::

:::table
| Component        | Role in ARP Spoofing                     |
|------------------|------------------------------------------|
| Attacker         | Sends forged ARP replies                 |
| Victim           | Updates ARP cache with spoofed entry     |
| Gateway/Target   | IP address being impersonated            |
| ARP Table        | Stores IP-to-MAC mappings (cache)        |
| Switch           | Forwards based on MAC; unaware of spoof  |
:::

:::image src="images/12_arp_spoofing_mitm.png" alt="Network diagram showing ARP spoofing MITM attack: victim machine, attacker machine, and gateway on same LAN segment, with forged ARP reply arrows from attacker to victim and gateway, and resulting intercepted traffic flow through attacker, labeled with MAC and IP addresses" caption="ARP spoofing inserts the attacker between victim and gateway at Layer 2: both sides update their ARP caches with the attacker's MAC address, making the attacker invisible to higher-layer protocols" width=full
:::

:::notes
ARP spoofing exploits the inherent trust model of the Address Resolution Protocol (ARP), a core protocol in IPv4 networks defined in RFC 826. ARP's primary function is to resolve a known IP address into its corresponding MAC address, enabling communication at the data link layer (Layer 2) of the OSI model. However, ARP was designed without any built-in authentication or integrity checks, making it vulnerable to spoofing attacks.

In a typical ARP spoofing attack, the attacker sends unsolicited ARP replies to a victim's machine, falsely claiming that the attacker's MAC address corresponds to the IP address of a trusted host, most commonly the default gateway. The victim updates its ARP cache with this forged mapping, causing all subsequent traffic destined for the gateway to be sent to the attacker's machine instead. The attacker can then choose to forward the traffic to the actual gateway (remaining transparent and enabling a man-in-the-middle position) or drop, inspect, or modify the packets.

A critical detail is that ARP caches are dynamic and time-limited: hosts update their ARP caches whenever they receive an ARP reply, whether solicited or not (gratuitous ARP). This "stateless update" behavior, designed for efficiency, is precisely what attackers exploit. The attacker simply needs to send periodic forged ARP replies to maintain the poisoned cache entries, as entries expire after a configurable timeout period (typically 20 minutes on most operating systems). Tools like arpspoof (from the dsniff suite), Ettercap, and Scapy automate this process.

Double-sided ARP spoofing is often used to achieve a clean MITM position: the attacker sends forged replies both to the victim (claiming to be the gateway) and to the gateway (claiming to be the victim). Both parties update their ARP caches, and all traffic between them flows through the attacker. Because the attacker enables IP forwarding on their machine, neither side observes connection disruption, making the attack undetectable without network monitoring tools.

This technique is widely used in local network attacks, including credential harvesting, session hijacking, and lateral movement within enterprise networks. It is especially effective in switched Ethernet environments, where switches forward frames based solely on MAC addresses and do not inherently protect against such spoofing. MAC flooding attacks on switches (exploiting the limited size of a switch's CAM table) can force a switch into hub mode, making ARP spoofing even more powerful by causing the switch to broadcast all frames rather than unicasting them to the appropriate port.

Mitigation strategies include static ARP entries (manually mapping critical IP-to-MAC bindings), Dynamic ARP Inspection (DAI) on managed switches (which validates ARP packets against a trusted DHCP snooping binding table), network segmentation (reducing the number of hosts that share a broadcast domain), and encrypted communication protocols such as IPsec or TLS to protect data even if ARP spoofing occurs. ARP spoofing is a foundational technique in many real-world attacks and is referenced in numerous CVEs related to network security tools and vulnerabilities in network stacks. Although not explicitly covered by a dedicated NIST guideline, ARP spoofing aligns with NIST SP 800-53 controls under SC-8 (Transmission Confidentiality and Integrity) and SI-4 (System Monitoring), which emphasize the need for secure network communications and detection of unauthorized network changes.
:::

%%%

---
unit: Attacks
code: SNF
title: Packet Capture & Sniffing, Revisited
---
:::callout style=line
Packet sniffing is a foundational technique in network reconnaissance and exploitation. While often associated with wireless networks due to their broadcast nature, sniffing is equally effective on wired networks when an attacker achieves a strategic position, such as through ARP spoofing, switch port mirroring, or exploiting hub-based infrastructure.
:::

:::list heading="Capabilities of a MITM Position" style=plain
- **Passive Eavesdropping**: Intercepting unencrypted traffic such as HTTP, FTP, or Telnet sessions.
- **Session Hijacking**: Capturing authentication tokens, cookies, or session identifiers for replay attacks (e.g., CVE-2009-3555 related to TLS renegotiation vulnerabilities).
- **Active Traffic Manipulation**: Injecting, modifying, or redirecting data in real time using tools like Ettercap or BetterCAP.
:::

:::flow
Attacker achieves MITM position (via ARP spoofing, DHCP spoofing, or physical access to a hub segment)
↓
Attacker enables promiscuous mode on network interface, NIC now captures all frames, not just those addressed to it
↓
Packet capture tool (Wireshark / tcpdump / Ettercap) records all visible traffic to a PCAP file
↓
Attacker filters captures for target protocols (HTTP, FTP, Telnet, SMTP without STARTTLS)
↓
Credentials, session cookies, or tokens are extracted from cleartext payloads
↓
Extracted secrets are replayed or used to escalate access (session hijacking, lateral movement)
:::

::::columns
::col::
:::text
**Protocols Vulnerable to Sniffing**
- HTTP
- FTP
- Telnet
- SMTP (without STARTTLS)
- SNMPv1/v2c
:::
::col::
:::text
**Tools Commonly Used**
- Wireshark
- tcpdump
- Ettercap
- BetterCAP
- Cain & Abel (legacy)
:::
::col::
:::text
**Defensive Countermeasures**
- Encryption (TLS 1.3, IPsec)
- Network segmentation
- Switched networks over hubs
- Port security and DAI (NIST SP 800-97)
:::
::::

:::image src="images/12_packet_sniffing_landscape.png" alt="Diagram showing a LAN with legitimate traffic flowing between client and server, an attacker in a MITM position capturing packets via ARP spoofing, with Wireshark interface overlay showing captured HTTP credentials in plaintext, and a separate section showing TLS-encrypted traffic the attacker cannot read" caption="Packet sniffing yields plaintext credentials from unencrypted protocols, TLS encryption is the primary technical countermeasure, rendering captured traffic unreadable" width=half
:::

:::notes
Once an attacker gains a man-in-the-middle (MITM) position, whether through ARP cache poisoning, DHCP spoofing, or physical network access, the ability to perform packet capture becomes a powerful offensive capability. This technique, known as sniffing, allows adversaries to monitor and analyze network traffic in real time. The medium, wired or wireless, is less significant than the attacker's visibility into the communication path.

In passive sniffing, attackers silently capture packets to extract sensitive data such as usernames, passwords, or session tokens. For example, an unencrypted HTTP session can expose credentials directly in the payload, this is exactly how Firesheep (a Firefox extension released in 2010) demonstrated the severity of session cookie theft over public Wi-Fi, causing a wave of concern that accelerated HTTPS adoption. Telnet (port 23), FTP (port 21), and SNMPv1/v2c transmit not only credentials but all exchanged data in cleartext, making them trivially sniffable.

Session hijacking exploits this by reusing captured session identifiers to impersonate legitimate users, a tactic mitigated by secure session management and encrypted transport layers. The HTTP-only and Secure flags on cookies, combined with HTTPS enforcement via HSTS (HTTP Strict Transport Security), are the primary technical controls that make cookie theft via sniffing ineffective, but only if fully deployed.

Active sniffing goes further, enabling attackers to inject malicious payloads or alter data in transit. Tools like Ettercap automate many of these techniques, allowing for DNS spoofing, HTML injection, or credential harvesting. SSL stripping attacks (first demonstrated by Moxie Marlinspike in 2009) exploit MITM positions to downgrade HTTPS connections to HTTP, enabling cleartext sniffing even on sites that nominally enforce HTTPS. HSTS preloading and HTTPS Everywhere are countermeasures to SSL stripping.

Network-level sniffing tools deserve specific mention: Wireshark is the industry-standard graphical packet analyzer used by both legitimate network administrators and attackers; tcpdump is its command-line equivalent, commonly available on UNIX/Linux systems; Ettercap combines ARP spoofing with real-time packet interception and modification. From a forensics perspective, the same tools used for attacks are used for defense, security analysts examine PCAP (packet capture) files to reconstruct incident timelines and identify compromised credentials or data.

The risks associated with unsecured protocols are well-documented in standards such as NIST SP 800-53 and ISO/IEC 27001, which emphasize the importance of encryption and network monitoring. To defend against sniffing, organizations must enforce end-to-end encryption (e.g., TLS 1.3), implement secure network architectures (e.g., switched Ethernet with port security), and regularly audit for insecure protocols. The principle of least privilege and network access control (NAC) frameworks also play a critical role in minimizing exposure. From a monitoring perspective, detecting ARP spoofing (which enables most wired-network sniffing) is achievable through network monitoring tools that flag ARP cache changes and gratuitous ARP anomalies.
:::

%%%

---
unit: Attacks
code: SES
title: Session Hijacking
---
:::callout style=soft
**Session hijacking** is a network-level attack wherein an adversary gains unauthorized access to an active communication session between a client and a server by stealing or predicting the session token, a temporary credential that authenticates and identifies the user during the session.
:::

::::columns
::col::
:::list heading="Key Characteristics"
- Bypasses authentication entirely
- Exploits weaknesses in session management
- Can occur at different layers (Network, Application)
- Often combined with other attacks (e.g., XSS, MITM)
:::
::col::
:::list heading="Common Targets"
- Web applications (HTTP cookies, JWTs)
- SSH sessions
- TCP connections
- VoIP or media sessions
:::
::col::
:::list heading="Attack Vectors"
- Packet sniffing (unencrypted traffic)
- Session fixation
- Cross-site scripting (XSS)
- Man-in-the-middle (MITM)
- Session token prediction
:::
::::

:::pullquote
Why guess a password when you can inherit a fully authenticated session?
:::

:::steps
1. **Target identifies active session**, Victim logs into a web application; session cookie is issued
2. **Attacker intercepts token**, Via ARP spoofing + sniffing, XSS payload, or network tap
3. **Token replay**, Attacker presents stolen cookie to server in a new HTTP request
4. **Server grants access**, Server validates cookie and treats attacker as legitimate user
5. **Session abuse**, Attacker reads, modifies, or exfiltrates data; changes passwords; makes transactions
:::

:::image src="images/12_session_hijacking_flow.png" alt="Three-panel diagram: panel 1 shows victim authenticating to server and receiving session cookie, panel 2 shows attacker stealing cookie via ARP spoof and packet capture, panel 3 shows attacker using stolen cookie to impersonate victim, with server unable to distinguish legitimate user from attacker" caption="Session hijacking bypasses authentication entirely: the session token is the proof of identity, so whoever holds it is treated as the legitimate user" width=full
:::

:::notes
Session hijacking represents a critical class of attacks that exploit weaknesses in session management mechanisms. Unlike credential theft, which focuses on stealing login information such as usernames and passwords, session hijacking allows an attacker to bypass authentication entirely by assuming control of an already-authenticated session. This is typically achieved by stealing or predicting the session identifier, often stored in cookies, URL parameters, or custom headers, that is exchanged between a client and server after successful authentication.

The session token serves as a temporary proof of identity for the duration of the session. If an attacker can intercept or predict this token, they can impersonate the legitimate user without ever knowing their password. This makes session hijacking particularly dangerous in environments where sessions remain active for long periods or where tokens are transmitted insecurely. A session token that functions for 24 hours gives an attacker who steals it the same access as the legitimate user for that entire period.

Session hijacking can occur at multiple layers. At the network layer, attackers may perform packet sniffing on unencrypted networks (e.g., public Wi-Fi) to capture session tokens in transit. At the application layer, vulnerabilities such as Cross-Site Scripting (XSS) or inadequate session management (e.g., predictable session IDs) can be exploited. Predictable session IDs, such as sequential integers or timestamps, can be guessed by attackers who observe even one valid session ID and then iterate nearby values. The OWASP Testing Guide details methods for assessing session token randomness and entropy. The MITRE ATT&CK framework categorizes this under T1563 – Remote Service Session Hijacking and T1185 – Browser Session Hijacking.

Session fixation is a related attack where the attacker does not steal a token generated after authentication but instead provides a known token to the victim before they authenticate. If the application does not regenerate the session token upon successful login, the attacker already knows the valid post-authentication token. Prevention requires that applications always issue a new session token after a successful login event.

Standards such as NIST SP 800-63B emphasize secure session management practices, including the use of Secure, HttpOnly, and SameSite cookie attributes, encryption of session tokens in transit (via TLS), and proper session invalidation upon logout or timeout. CVEs like CVE-2021-44228 (Log4Shell) have shown how remote code execution can lead to session token exposure, further enabling hijacking. Modern frameworks like JSON Web Tokens (JWTs) introduce their own session hijacking risks if tokens are long-lived, if the signing key is weak, or if the "none" algorithm is accepted (CVE-2015-9235).

Prevention strategies include enforcing HTTPS everywhere, regenerating session IDs after login, implementing idle and absolute timeouts, monitoring for concurrent sessions from different geographic locations (which may indicate token theft), and implementing single-use tokens for sensitive operations. Understanding session hijacking is essential for securing modern web applications and maintaining user privacy and trust.
:::

%%%

---
unit: Synthesis
code: CHN
title: Putting Together an Attack Chain
---
:::steps
1. Attacker performs ARP spoofing on a coffee shop Wi-Fi network
2. Victim's traffic now routes through the attacker's machine
3. Attacker sniffs traffic and captures an active session cookie
4. Attacker reuses that cookie to access the victim's account directly
:::

:::callout
This attack chain demonstrates how individual vulnerabilities can be composed into a full compromise without requiring direct encryption breaking. Each phase exploits a different layer of trust or protocol assumption in network communication.
:::

:::text
This scenario illustrates a classic **session hijacking** attack executed over an unsecured public network. It leverages weaknesses in the Address Resolution Protocol (ARP), HTTP session management, and user trust in network infrastructure.
:::

:::list heading="Key Concepts Exploited"
- **ARP Spoofing**: Manipulation of the ARP table to redirect traffic
- **Man-in-the-Middle (MITM)**: Positioning to intercept and observe traffic
- **Session Cookie Reuse**: Authentication bypass via token theft
- **Insecure Public Networks**: Lack of encryption or endpoint validation
:::

:::image src="images/12_attack_chain_coffee_shop.png" alt="Realistic network diagram of a coffee shop environment: victim laptop and attacker laptop on same Wi-Fi, attacker executing ARP spoof, capturing HTTP session cookie in Wireshark, and using that cookie to log into victim's account from a different browser tab, timeline of attack phases shown at bottom" caption="A complete real-world attack chain: ARP spoofing → MITM position → session cookie theft → account takeover, no encryption was broken, only trust was exploited" width=full
:::

:::notes
This attack chain exemplifies how adversaries exploit weaknesses in network protocols and user assumptions rather than attempting to break cryptographic protections directly. It begins with **ARP spoofing**, a well-documented technique (CVE-2002-1166, CVE-2015-2549) that abuses the trust model of the Address Resolution Protocol. ARP operates at Layer 2 and lacks built-in authentication, making it vulnerable to spoofing attacks in local networks. By sending falsified ARP replies, the attacker convinces the victim's machine that the attacker's MAC address is associated with the default gateway's IP address.

Once successful, the attacker achieves a **Man-in-the-Middle (MITM)** position, enabling traffic interception. This aligns with **NIST SP 800-53** controls such as SC-7 (Boundary Protection) and CA-3 (Network Access Control), which aim to prevent unauthorized network traversal. In this position, the attacker can perform **passive eavesdropping**, capturing unencrypted or inadequately protected data. The attacker must also poison the gateway's ARP cache to intercept traffic flowing in both directions, otherwise they only see traffic from victim to gateway, not the server's responses.

The final phase involves **session hijacking**, where the attacker steals a valid session identifier (e.g., a session cookie) and presents it to the server to impersonate the victim. This bypasses authentication and is categorized under **OWASP Top 10: Broken Authentication**. It also reflects weaknesses in session management as outlined in **ISO/IEC 27001 Annex A** control A.9.2.

This scenario plays out in real life regularly on public Wi-Fi networks at airports, hotels, and coffee shops. A study published by Avast at Mobile World Congress demonstrated that 63% of Wi-Fi connections at the conference were vulnerable to packet interception. The Firesheep tool, mentioned earlier, made this attack accessible to non-technical users with a single click, exposing the scale of the problem and contributing to the industry's shift toward HTTPS-by-default.

Importantly, this attack does not require cracking encryption. Instead, it exploits the inherent trust in network protocols and the absence of secure communication enforcement, common in public Wi-Fi environments. This highlights the importance of end-to-end encryption (e.g., HTTPS/TLS) and certificate validation as defensive strategies. VPNs (Virtual Private Networks) also provide effective protection in public Wi-Fi environments by encrypting all traffic before it leaves the user's device, rendering ARP spoofing-based interception ineffective because the captured traffic is encrypted at the VPN tunnel layer.

This attack chain also illustrates the defender's challenge: each individual step (connecting to Wi-Fi, ARP cache update, session cookie in HTTP response) is normal behavior. Only by analyzing the full chain does the attack become visible, and this is precisely why security monitoring and correlation across multiple data sources is so valuable, a theme that will recur in Class 14 on IDS, IPS, and SIEM.
:::

%%%

---
unit: Defense
code: DEF
title: Defenses Overview
---
::::columns
::col::
:::table
| Attack | Key Defense Mechanisms |
|---|---|
| DNS Spoofing | DNSSEC, trusted resolvers, response validation |
| ARP Spoofing | Static ARP tables, DAI, network segmentation |
| Session Hijacking | HTTPS/TLS, secure cookies, short TTLs |
:::
::col::
:::callout
Each network-layer attack has a corresponding defense rooted in cryptographic integrity, protocol hardening, and infrastructure validation.
:::
::::

:::steps
1. **Deploy DNSSEC**, Add cryptographic signatures to DNS records so resolvers can verify authenticity
2. **Enable Dynamic ARP Inspection**, Configure managed switches to validate ARP packets against DHCP binding tables
3. **Enforce HTTPS everywhere**, Use HSTS headers and certificate pinning to prevent SSL stripping
4. **Implement secure cookie attributes**, Set Secure, HttpOnly, and SameSite=Strict on all session cookies
5. **Monitor ARP traffic**, Alert on unusual gratuitous ARP patterns that may indicate spoofing
6. **Deploy network segmentation**, Reduce the Layer 2 blast radius so ARP attacks are limited to smaller segments
:::

:::image src="images/12_network_defenses_layered.png" alt="Defense-in-depth diagram showing countermeasures layered against each attack type: DNSSEC blocks DNS poisoning, DAI on switch blocks ARP spoofing, TLS encrypts sessions to stop sniffing, HSTS prevents SSL stripping, session token hardening prevents hijacking, with green shield icons for each defense" caption="Each attack has a targeted technical countermeasure: defense in depth means deploying multiple controls so that the failure of one does not leave the system unprotected" width=full
:::

:::notes
Network defense mechanisms are not merely reactive patches but are grounded in well-established security principles and standardized frameworks. For instance, DNS spoofing, which involves corrupting DNS cache to redirect traffic, is effectively mitigated through DNS Security Extensions (DNSSEC), a suite of IETF specifications that add cryptographic signatures to DNS records, ensuring authenticity and integrity (RFC 4033–4035). Trusted DNS resolvers such as those provided by Cloudflare (1.1.1.1) or Google (8.8.8.8) also reduce exposure to malicious servers. DNS-over-HTTPS (DoH) and DNS-over-TLS (DoT) further protect the confidentiality of DNS queries in transit.

Address Resolution Protocol (ARP) spoofing, commonly exploited in local network attacks like man-in-the-middle (MITM), can be defended against by implementing static ARP entries for critical hosts or enabling Dynamic ARP Inspection (DAI) on managed switches. DAI validates ARP packets against a trusted binding table (typically populated via DHCP snooping), preventing gratuitous or forged ARP replies from compromising the network. This aligns with recommendations in NIST SP 800-97 and IEEE 802.1x port-based network access control. Additional Layer 2 protections include DHCP snooping (which prevents rogue DHCP servers from providing false gateway information), IP Source Guard (which validates that traffic from a switch port comes from the expected IP and MAC), and private VLANs (which restrict Layer 2 communication between hosts in the same VLAN).

Session hijacking, where attackers steal or predict session tokens to impersonate users, is countered through the consistent enforcement of HTTPS/TLS encryption, the use of secure and HttpOnly cookie flags, and the implementation of short session timeouts. The SameSite cookie attribute (Strict or Lax) prevents cross-site request forgery attacks that can expose session tokens. These practices conform to OWASP session management guidelines and are referenced in ISO/IEC 27001 controls regarding secure system architecture. Token binding (RFC 8471) is an emerging mechanism that cryptographically ties session tokens to the TLS connection, making stolen tokens unusable from a different connection context.

Together, these defenses reflect a layered approach to network hardening, consistent with the defense-in-depth model advocated by both NIST and ISO standards. No single control is sufficient on its own: DNSSEC protects DNS but not ARP; DAI protects ARP but not application-layer session tokens; TLS protects session tokens but relies on correct certificate validation by the client. Defense in depth ensures that multiple independent controls must be simultaneously defeated for an attacker to succeed.
:::

%%%

---
unit: Summary
code: SUM
title: Attacking the Plumbing Directly
---
:::pullquote
DNS, ARP, and sessions are all built on trust, and every attack today exploited that trust rather than breaking encryption outright.
:::

:::list style=chips
- DNS Cache Poisoning
- IP Spoofing
- ARP Spoofing
- Network Sniffing
- Session Hijacking
:::

:::text
These attacks exploit implicit trust mechanisms in network protocols rather than attempting to break cryptographic protections. They manipulate the foundational infrastructure of communication, the "plumbing" of the network, to redirect, intercept, or hijack traffic.
:::

:::callout style=soft
**Core Principle**: Modern attackers rarely attempt to decrypt secure traffic. Instead, they subvert the trust relationships that determine *where* traffic goes and *who* is allowed to send or receive it.
:::

:::image src="images/12_trust_exploitation_summary.png" alt="Summary concept map showing the five attack types (DNS poisoning, IP spoofing, ARP spoofing, sniffing, session hijacking) connected to their exploited trust assumptions (DNS resolver trust, IP source trust, ARP cache trust, cleartext traffic, session token trust), with arrows pointing to real-world impact for each, clean infographic style" caption="The common thread across all class 12 attacks: exploiting trust rather than breaking cryptography, the plumbing was designed to trust, and adversaries design attacks to abuse that trust" width=full
:::

:::notes
In this final segment of our exploration into network vulnerabilities, we emphasize a foundational concept in cybersecurity: the exploitation of implicit trust in network protocols. While encryption technologies such as TLS have made it increasingly difficult for attackers to intercept or decode traffic directly, adversaries have shifted their focus to compromising the underlying mechanisms that route and identify traffic, the network plumbing.

For instance, **DNS Cache Poisoning** (e.g., CVE-2008-1447) exploits the trust a resolver places in a DNS response, allowing an attacker to redirect users to malicious sites. Similarly, **ARP Spoofing** leverages the stateless and trust-based nature of the Address Resolution Protocol to perform man-in-the-middle attacks on local networks. **IP Spoofing** abuses the lack of source address validation in IP communications, a vulnerability addressed in part by ingress filtering guidelines such as those outlined in **BCP 38** (RFC 2827) and **NIST SP 800-97**.

**Session Hijacking** techniques capitalize on the trust a server places in session tokens (e.g., cookies), often obtained through cross-site scripting (XSS) or network sniffing. Even **Network Sniffing**, while passive, becomes potent when combined with ARP spoofing or unencrypted protocols, violating the principle of secure data-in-transit as defined in **ISO/IEC 27001** and **NIST SP 800-53** controls.

An important meta-lesson from this class is that protocol vulnerabilities do not disappear when encryption is added at one layer. Adding TLS to HTTP (creating HTTPS) protects the payload from sniffing, but does not protect the DNS resolution that precedes the connection, the ARP resolution that identifies the gateway, or the session management logic in the application. Comprehensive security requires hardening every trust relationship in the communication chain, not just adding encryption at one point.

These attacks underscore a critical lesson: secure communication is not solely about encryption. It requires **continuous validation**, **source authentication**, and **robust trust models**, principles foundational to Zero Trust Architectures (NIST SP 800-207). Zero Trust explicitly rejects the idea that network location implies trustworthiness: a device on the internal LAN is not inherently more trustworthy than one on the internet, because ARP spoofing, insider threats, and lateral movement can all compromise the implicit LAN trust model.

In the next unit, we will examine how firewalls and access control systems enforce these trust boundaries at the network perimeter, and why even well-configured firewalls cannot fully protect against the attacks studied in this class.
:::

%%%

---
unit: Deep Dive
code: KAM
title: "Case Study: The Kaminsky DNS Attack (2008)"
---
:::callout style=soft
In 2008, security researcher Dan Kaminsky discovered a critical flaw (CVE-2008-1447) in DNS that allowed cache poisoning at a scale previously thought impractical. The disclosure triggered the largest coordinated emergency patch in internet history, with virtually every DNS implementation patched simultaneously on July 8, 2008.
:::

::::columns
::col::
:::list heading="Attack Mechanics"
- DNS uses 16-bit transaction IDs, only 65,536 possibilities
- Attacker floods resolver with forged replies guessing the transaction ID
- Birthday paradox: ~256 guesses gives 50% chance of success per query
- Kaminsky found a way to trigger repeated, new queries, not just repeat the same one
- Result: cache can be poisoned in seconds, not hours
:::
::col::
:::list heading="Why It Was Revolutionary"
- Previous attacks required waiting for the cached record to expire before retrying
- Kaminsky's insight: poison a non-existent sub-domain, include a malicious NS record in the "additional" section
- This redirects the entire domain to an attacker-controlled authoritative server
- Impact: attacker controls ALL records under the poisoned domain, not just one hostname
:::
::::

:::table
| Parameter             | Before Kaminsky  | Kaminsky Attack |
|-----------------------|------------------|-----------------|
| Attack time           | Hours to days    | Under 10 seconds|
| Records poisoned      | Single A record  | Entire zone     |
| Retry barrier         | Cache TTL wait   | New sub-domain per attempt |
| Detection difficulty  | Moderate         | Very high       |
:::

:::code language=mermaid caption="The Kaminsky attack's genius was in poisoning the NS delegation record rather than a single hostname, one successful attack redirected all lookups under a domain to attacker-controlled DNS"
flowchart TB
  A["July 2008: coordinated disclosure and patching across DNS vendors"]
  B["Old limit: poisoning one name meant waiting for its TTL to expire"]
  C["Kaminsky's insight: query endless random subdomains,<br/>so every query is a fresh chance to win the race"]
  D["A forged reply can also claim authority for the whole zone"]
  E["Fixes: source-port randomization, then DNSSEC signatures"]
  A --> B --> C --> D --> E
:::

:::notes
The Kaminsky DNS vulnerability, disclosed in 2008, fundamentally changed how the security community thinks about DNS reliability. Dan Kaminsky, while working on an unrelated project, discovered that DNS cache poisoning was not merely a theoretical concern but a practical, rapid attack. Prior to his discovery, the conventional wisdom held that cache poisoning required either very large amounts of traffic (to guess 16-bit transaction IDs before the legitimate response arrived) or waiting for cached entries to expire before retrying.

Kaminsky's key insight exploited the structure of DNS itself. Instead of trying to poison a specific hostname, say, www.bank.com, he targeted sub-domains that did not actually exist, such as a1234.bank.com. Because these sub-domains are not cached, each query is a fresh opportunity to send forged replies. Crucially, the forged reply could include an "authoritative" or "additional" section pointing the target's resolver to a malicious name server for the entire bank.com zone. If the attacker successfully poisoned even one of these fabricated sub-domain lookups, the resolver would now consult the attacker's server for all future bank.com queries, giving the attacker full control over every hostname under that domain.

The mathematics are alarming. DNS transaction IDs are only 16 bits, 65,536 possible values. A standard DNS resolver on UDP accepts the first response that matches the transaction ID and the source port. If source ports were also predictable, the attacker's search space was trivially small. Kaminsky's attack could typically succeed within about 10 seconds of sustained forged-reply flooding, well within the timeout window before the legitimate authoritative response arrived.

The coordinated disclosure process was itself remarkable. Kaminsky notified major DNS software vendors (ISC BIND, Microsoft, Cisco, etc.) and OS vendors in secret approximately 90 days before public disclosure, a period used to develop and test patches. On July 8, 2008, patches were simultaneously released by virtually every major vendor in an unprecedented coordinated effort (CERT/CC Vulnerability Note VU#800113). The primary fix was source port randomization, using randomly chosen UDP source ports for outgoing queries, increasing the attacker's guessing space from 65,536 to over 4 billion combinations.

DNSSEC is the definitive fix for cache poisoning, yet it was not deployed immediately after Kaminsky's 2008 disclosure because of operational complexity, key management burden and resolver upgrade requirements. Global adoption remains below 30% more than 17 years later. The gap between a known fix and a deployed fix is a recurring theme in network security.

The Kaminsky attack also established a template for responsible disclosure that continues to influence the security industry: private notification to affected vendors, coordinated public release, and embargo periods long enough to allow patch development but short enough to limit exposure. This model is codified in ISO/IEC 30111 (vulnerability handling processes) and NIST SP 800-216 (federal vulnerability disclosure guidelines).
:::

%%%

---
unit: Deep Dive
code: BGP
title: BGP Hijacking, Routing Gone Wrong
---
:::callout style=soft
**BGP (Border Gateway Protocol)** is the routing protocol that connects autonomous systems (ASes) on the internet. Because BGP was designed in an era of trusted peers, it has no built-in cryptographic validation of route announcements, any AS can announce routes for IP address blocks it does not own, and its peers will often accept those announcements.
:::

::::columns
::col::
:::list heading="How BGP Hijacking Works"
- An AS announces a more-specific prefix (e.g., /24 vs /20) for IP space it doesn't own
- BGP's longest-prefix-match means the more-specific announcement wins
- Victim AS's traffic is now routed through the hijacking AS
- Hijacker can eavesdrop, drop, or selectively forward traffic
:::
::col::
:::list heading="Real-World Incidents"
- **2010 China Telecom**: Announced 37,000 BGP prefixes, rerouting 15% of global internet traffic through China for ~18 minutes
- **2018 Amazon Route 53 hijack**: Attackers redirected MyEtherWallet.com to steal cryptocurrency via BGP prefix hijack
- **2019 Rostelecom incident**: Russian ISP briefly hijacked routes for Google, Amazon, Cloudflare
:::
::::

:::table
| Mitigation          | Description                                      | Status           |
|---------------------|--------------------------------------------------|------------------|
| RPKI                | Resource Public Key Infrastructure, cryptographic route origin validation | Partially deployed |
| BGPsec              | Cryptographic path validation for AS-PATH        | Experimental     |
| Route filtering     | Manually filtering accepted prefixes from peers  | Widely used      |
| IRR                 | Internet Routing Registry records for verification| Inconsistently maintained |
:::

:::code language=mermaid caption="BGP hijacking exploits longest-prefix-match routing: a more-specific route announcement wins even without authorization, diverting large volumes of internet traffic through attacker-controlled infrastructure"
flowchart LR
  L["Legitimate AS<br/>announces 203.0.112.0/20"] --> N["Internet routers"]
  H["Hijacking AS<br/>announces 203.0.112.0/24"] --> N
  N -->|"more specific prefix wins"| H
  H -.->|"traffic meant for the /24"| X["Intercepted or dropped"]
  D["Defense: RPKI route origin validation"] -.- N
:::

:::notes
BGP (Border Gateway Protocol), defined in RFC 4271, is the protocol that knits together the approximately 100,000 autonomous systems that collectively form the internet. An autonomous system (AS) is a network under a single administrative control with a unique AS number (ASN). BGP's job is to exchange reachability information between ASes: "I can reach these IP prefixes; route traffic for them to me." The problem is that BGP was designed with the assumption that all peers are trusted and announce only the routes they legitimately own. In practice, nothing in the protocol prevents an AS from announcing routes for IP space that belongs to someone else.

BGP hijacking exploits this lack of origin authentication. The attack typically involves a malicious (or misconfigured) AS announcing an IP prefix that either exactly matches or is more specific than a legitimate announcement. BGP routers prefer more-specific routes due to longest-prefix-match, so a /24 announcement (256 addresses) will be preferred over a /20 announcement (4,096 addresses) even if the /20 is the legitimate owner. This asymmetry is the mechanism attackers exploit: by announcing a covering /24 for part of a victim's /20, they can divert just that slice of traffic without disrupting the rest of the victim's routing.

The 2018 Amazon Route 53 BGP hijack is particularly instructive. Attackers hijacked a portion of Amazon's IP space for approximately two hours during which the MyEtherWallet.com DNS resolution was rerouted to attacker-controlled servers. Users visiting the site received a TLS certificate warning (the attackers could not obtain a valid certificate for the domain) but many ignored the warning and proceeded, having their Ethereum wallet credentials stolen. The attack demonstrates how BGP hijacking can enable credential theft and financial fraud at scale, and how TLS certificate validation errors should never be ignored.

The primary technical mitigation for BGP hijacking is Resource Public Key Infrastructure (RPKI), defined in RFC 6480. RPKI creates cryptographically signed Route Origin Authorizations (ROAs) that specify which AS is permitted to originate each IP prefix. BGP routers that perform RPKI validation can reject route announcements whose origin AS does not match a valid ROA. However, RPKI only validates route origin, not the AS-path, BGPsec (RFC 8205) addresses path validation but has seen minimal deployment due to performance concerns and operational complexity.

RPKI is a correct cryptographic solution that is hard to deploy retroactively: every prefix owner must create Route Origin Authorizations in its Regional Internet Registry, and every transit ISP must run validating routers configured to drop invalid routes. With roughly 40% of routes covered and many routers still not validating, prefix hijacking remains feasible, especially against prefixes without ROAs.

NIST SP 800-54 (Border Gateway Protocol Security) provides guidance on securing BGP deployments including prefix filtering, AS-path filtering, and the use of MD5 authentication for BGP sessions. While MD5 authentication prevents TCP session hijacking of the BGP control plane, it does not prevent fraudulent route announcements from authenticated peers, for which RPKI and route filtering are the appropriate controls.
:::

%%%

---
unit: Deep Dive
code: TUN
title: DNS Tunneling, Covert Channels Through Port 53
---
:::callout style=soft
**DNS tunneling** abuses the DNS protocol as a covert data channel. Because DNS (UDP/TCP port 53) is almost universally allowed through firewalls, attackers can encode arbitrary data in DNS queries and responses to exfiltrate data, bypass web filters, or maintain command-and-control (C2) communication with compromised hosts, even through highly restrictive network controls.
:::

:::flow
Malware on victim's host encodes data payload in Base32/Base64
↓
Encoded payload is embedded as sub-domain label: "data_chunk.attacker-c2.com"
↓
DNS query is sent to the internal resolver (outbound DNS always allowed)
↓
Resolver forwards query to attacker's authoritative NS for attacker-c2.com
↓
Attacker's NS server decodes the exfiltrated data and sends response with encoded C2 commands
↓
Malware decodes TXT/CNAME response to receive next instructions, full bidirectional channel established
:::

::::columns
::col::
:::list heading="Common Tools"
- **iodine**, tunnels IPv4 over DNS
- **dns2tcp**, TCP session over DNS
- **DNScat2**, encrypted C2 over DNS
- **Cobalt Strike**, DNS beacon built-in
:::
::col::
:::list heading="Detection Indicators"
- Unusually long DNS query names (>63 chars per label)
- High-entropy sub-domain strings
- High query volume to single domain
- Non-standard record types (TXT, NULL, PRIVATE)
- Queries to recently registered domains
:::
::::

:::code language=mermaid caption="DNS tunneling hides data exfiltration inside normal-looking DNS traffic, from the firewall's perspective, port 53 queries to an external domain appear routine"
flowchart LR
  W["Compromised workstation"] -->|"data encoded in subdomain labels"| F["Corporate firewall<br/>DNS on port 53 allowed"]
  F --> R["Internal resolver"]
  R --> A["Attacker's authoritative<br/>name server"]
  A -->|"commands in DNS answers"| R
  D["Detection: long random-looking labels,<br/>high query volume to one domain, TXT records"] -.- R
:::

:::notes
DNS tunneling is classified under MITRE ATT&CK T1071.004 (Application Layer Protocol: DNS) and T1048.003 (Exfiltration Over Alternative Protocol: Exfiltration Over Unencrypted Non-C2 Protocol). It represents a class of covert channel attacks where a protocol not designed for general data transport is repurposed to carry arbitrary data, exploiting the fact that network controls are typically configured to permit that protocol's traffic without deep inspection.

The fundamental mechanism exploits how DNS query names work. A DNS query for "YWx0ZXJuYXRpdmUgcGF5bG9hZA.exfil.attacker.com" looks superficially like a normal DNS lookup. The string before the first dot is treated as a sub-domain label, but it is actually Base32-encoded data that the attacker's authoritative name server decodes. Responses can carry data in TXT records, CNAME chains, or even the IP addresses returned in A records (encoding 4 bytes of payload per response). Bidirectional communication is achievable because both queries (exfiltration) and responses (C2 commands) can carry encoded payloads.

Bandwidth is limited, DNS queries are constrained in length and the protocol adds overhead, but DNS tunneling is not about speed. It excels in environments where no other outbound protocol is permitted, where the attacker needs a persistent low-bandwidth C2 channel that survives network changes (since DNS is typically always permitted), or where the attacker is specifically trying to evade a web proxy that logs and inspects HTTP/S traffic.

Detection requires DNS-aware security monitoring. Network Detection and Response (NDR) tools and DNS firewalls (such as Cisco Umbrella, Cloudflare Gateway, or BIND RPZ, Response Policy Zones) can detect tunneling by analyzing query patterns: unusually high query rates to a single domain, labels with high entropy (Base32/Base64 content has Shannon entropy close to 5 bits per character compared to ~2–3 for normal domain names), and queries for record types rarely used in legitimate traffic (TXT, NULL, PRIVATE). NIST SP 800-81r2 recommends deploying a recursive DNS resolver that logs queries with metadata for security analysis.

A DNS tunnel query is distinguishable from a normal one: it is long, high-entropy and often a TXT record, where a normal query is short, low-entropy and typically an A record. DNS is almost universally allowed outbound because legitimate services (software updates, CDN health checks) fail without it, and that necessity is exactly what makes DNS tunneling effective.

Mitigation includes deploying DNS monitoring with entropy analysis, using DNS-over-HTTPS (DoH) in a controlled way that routes queries through an enterprise resolver rather than allowing clients to bypass the enterprise DNS entirely, blocking external authoritative NS lookups from internal resolvers (requiring all queries to go through a controlled recursive resolver), and applying threat intelligence feeds of known tunneling domains to DNS sinkholes. DNSSEC does not prevent tunneling, it only validates that DNS records are authentic, not that the records are being used for legitimate purposes.
:::

%%%

---
unit: Tool Spotlight
code: WRK
title: "Tool Spotlight: Wireshark"
---
:::callout style=soft
**Wireshark** is the world's most widely used open-source network protocol analyzer. It captures live traffic or opens pre-recorded PCAP files and presents packets in a human-readable, filterable interface. It is used by network administrators, security analysts, penetration testers, and incident responders alike, the same tool serves both offense and defense.
:::

::::columns
::col::
:::list heading="Core Capabilities"
- Capture live traffic on any network interface
- Open and analyze PCAP/PCAPng files
- Decode 3,000+ protocols automatically
- Apply display filters to isolate traffic of interest
- Follow TCP/UDP/HTTP streams to reconstruct sessions
- Export extracted objects (files, images) from HTTP sessions
- Decrypt TLS sessions if the session key log is available
:::
::col::
:::list heading="Essential Display Filters"
- `http`, show all HTTP traffic
- `dns`, show all DNS queries and responses
- `arp`, show ARP packets (spot spoofing attempts)
- `tcp.flags.syn == 1`, show SYN packets (port scans, SYN floods)
- `ip.src == 192.168.1.50`, filter by source IP
- `http contains "password"`, search HTTP payloads
- `frame contains "cookie"`, find session cookies across protocols
:::
::::

:::table
| Use Case               | Technique in Wireshark                       |
|------------------------|----------------------------------------------|
| Credential hunting     | Follow HTTP stream → search for POST bodies  |
| ARP spoofing detection | Filter arp, look for duplicate IP→MAC mappings |
| DNS analysis           | Filter dns, check A record answers for anomalies |
| Session cookie theft   | Filter http, follow stream, find Set-Cookie header |
| SYN flood detection    | tcp.flags.syn == 1 && tcp.flags.ack == 0, check rate |
:::

:::notes
Wireshark, originally named Ethereal and renamed in 2006, has been the de facto standard for network packet analysis since its first release in 1998. Its strength lies not in any single feature but in the combination of a comprehensive protocol dissector library, a powerful display filter language, and the ability to reconstruct application-layer sessions from raw packet streams. Understanding Wireshark is considered a fundamental skill for network security practitioners, and it appears in virtually every major security certification curriculum including CompTIA Security+, CEH, and OSCP.

The tool operates in two modes: live capture and offline analysis. Live capture places the network interface in promiscuous mode, causing it to accept all frames regardless of destination MAC address. On a switched network, this typically limits capture to the attacker's own traffic unless they have achieved a MITM position via ARP spoofing, which is why ARP spoofing is so frequently paired with Wireshark in real attacks. Offline analysis opens PCAP files, which can come from any capture source: Wireshark itself, tcpdump, network taps, or Security Operations Center (SOC) network monitoring infrastructure.

The display filter language deserves specific attention because it is what separates effective Wireshark users from those who are overwhelmed by packet volume. A busy corporate network may generate millions of packets per hour, without precise filters, analysts cannot identify relevant traffic. Key patterns include: `http.request.method == "POST"` (to find form submissions that might include credentials), `dns.qtype == 16` (TXT record queries, which may indicate DNS tunneling), `arp.duplicate-address-detected` (Wireshark's built-in heuristic for detecting duplicate ARP mappings that may indicate ARP spoofing), and `tcp.analysis.retransmission` (to identify network congestion or packet loss patterns indicative of DoS attacks).

Session reconstruction via "Follow TCP Stream" is one of Wireshark's most powerful forensic features. By right-clicking on any TCP packet and selecting "Follow TCP Stream," Wireshark reassembles all packets in that TCP connection and displays the application-layer conversation in human-readable form. For unencrypted HTTP sessions, this reveals login forms, session cookies, and transmitted data exactly as the application sees it, making it an extremely effective tool for demonstrating why cleartext protocols are insecure.

Over plain HTTP, a captured POST login shows the username and password in cleartext; the same login over HTTPS shows only encrypted bytes. This contrast is the clearest motivation for enforcing HTTPS and retiring cleartext protocols.

Wireshark also supports TLS decryption if the session key log file is available (generated by browsers via the `SSLKEYLOGFILE` environment variable). This is extremely useful for debugging TLS applications and for incident response scenarios where the organization has legal authority to decrypt employee traffic and has configured session key logging on endpoints. In forensic contexts, decrypted TLS sessions can reveal malware C2 communications that would otherwise appear as opaque encrypted streams.
:::

%%%

---
unit: Tool Spotlight
code: ETC
title: "Tool Spotlight: Ettercap & BetterCAP"
---
:::callout style=soft
**Ettercap** and its modern successor **BetterCAP** are open-source network attack frameworks that combine ARP spoofing, packet capture, protocol dissection, and active traffic manipulation into a single unified tool. They are the standard tools for demonstrating and performing MITM attacks on local networks.
:::

::::columns
::col::
:::list heading="Ettercap Key Features"
- Automated ARP poisoning (single target or entire subnet)
- Built-in protocol dissectors for credential extraction (HTTP, FTP, Telnet, SMTP, POP3)
- Plugin system for custom attacks (DNS spoofing, SSL stripping)
- Graphical (GTK) and text-based (curses) interfaces
- Passive network mapping and OS fingerprinting
:::
::col::
:::list heading="BetterCAP Key Features"
- Modern REST API and web-based UI
- Modular architecture (caplets, scripted attack sequences)
- Wi-Fi, Bluetooth, and HID attack modules in addition to Ethernet
- Built-in HTTP/HTTPS proxy for traffic interception and modification
- ARP, NDP (IPv6), and DHCP spoofing
- JavaScript injection into HTTP responses in real time
:::
::::

:::table
| Capability         | Ettercap                        | BetterCAP                        |
|--------------------|---------------------------------|----------------------------------|
| ARP Spoofing       | Yes (unified & bridged)         | Yes (with IPv6 NDP support)      |
| SSL Stripping      | Via sslstrip plugin             | Built-in HTTPS proxy             |
| DNS Spoofing       | dns_spoof plugin                | dns.spoof module                 |
| Credential capture | Protocol dissectors built-in    | http-ui module + caplets         |
| Wi-Fi attacks      | Limited                         | Full 802.11 deauth + capture     |
| Scripting          | Etter.conf                      | Caplets (shell-like scripts)     |
:::

:::notes
Ettercap was first released in 2001 by Alberto Ornaghi and Marco Valleri and quickly became the standard tool for demonstrating local network MITM attacks in educational and penetration testing contexts. Its core value proposition is the integration of ARP spoofing and protocol dissection: rather than running a separate ARP spoofer and a separate credential sniffer, Ettercap handles both in a single tool with a unified interface.

The tool operates in two primary modes. In "unified sniffing" mode, Ettercap sniffs the interface directly, useful on Wi-Fi or when the attacker is inline. In "bridged sniffing" mode, Ettercap sits between two interfaces and forwards traffic, useful when the attacker has physically inserted themselves into the network path. The most common use case in testing is unified sniffing combined with the ARP poison plugin targeting specific hosts or the entire subnet.

Ettercap's protocol dissectors are what make credential harvesting automatic. When Ettercap captures FTP traffic, it automatically identifies and displays the USER and PASS commands. For HTTP form submissions, it extracts the POST body. For Telnet, it reconstructs the keystroke stream including the login sequence. This automation removes the manual effort of applying Wireshark filters and following streams, making the attack more accessible (and more dangerous in the wrong hands).

BetterCAP (released 2018) addresses several architectural limitations of Ettercap, particularly around Wi-Fi, IPv6, and modern HTTPS environments. Its caplet system allows complex attack sequences to be scripted and replayed, which is particularly useful in penetration testing where the same attacks need to be performed consistently across multiple test environments. BetterCAP's built-in HTTPS proxy, combined with a caplet that performs SSL stripping, automates the full attack chain from ARP poisoning to cleartext credential capture on sites that use HSTS improperly.

Man-in-the-middle tools require explicit authorization. Using them on a network one does not own or have written permission to test violates the Computer Fraud and Abuse Act in the United States and equivalent laws elsewhere. Penetration testers operate only within a signed Statement of Work and Rules of Engagement, and practice only on dedicated lab environments.

From a defensive standpoint, detecting Ettercap/BetterCAP usage involves monitoring for the characteristic patterns of ARP spoofing (duplicate IP-to-MAC mappings in ARP traffic), anomalous gratuitous ARP broadcasts, and the presence of two hosts simultaneously claiming the same IP address. Network Intrusion Detection Systems (NIDS) such as Snort and Suricata include signatures for Ettercap's ARP poisoning behavior. Enabling Dynamic ARP Inspection (DAI) on managed switches is the most effective automated defense.
:::

%%%

---
unit: Deep Dive
code: MAC
title: MAC Flooding & DHCP Spoofing
---
:::callout style=soft
**MAC flooding** and **DHCP spoofing** are two Layer 2 attacks that complement ARP spoofing by subverting the switch and DHCP infrastructure respectively. MAC flooding converts a switch into a hub, enabling passive eavesdropping without ARP poisoning. DHCP spoofing intercepts network configuration delivery, redirecting traffic before hosts even send their first packet.
:::

::::columns
::col::
:::list heading="MAC Flooding"
- Network switches maintain a Content Addressable Memory (CAM) table mapping MAC addresses to switch ports
- CAM table has finite size, typically 8,000–130,000 entries
- Flooding the switch with thousands of forged source MACs exhausts the CAM table
- Switch enters "failopen" mode: broadcasts all frames out all ports like a hub
- All hosts on the segment can now passively capture all traffic without ARP spoofing
- Tool: **macof** (dsniff suite)
:::
::col::
:::list heading="DHCP Spoofing"
- DHCP is stateless: a client broadcasts DHCPDISCOVER, any server can respond
- Attacker runs a rogue DHCP server that responds faster than the legitimate server
- Rogue server assigns: victim's IP, but attacker's IP as the default gateway
- All victim traffic is immediately routed to attacker, no ARP spoofing needed
- Attacker can also provide a rogue DNS server IP to the victim
- Tool: **Yersinia**, **DHCP Starvation + Rogue Server** in BetterCAP
:::
::::

:::table
| Attack          | Layer   | Mechanism                                     | Mitigation                        |
|-----------------|---------|-----------------------------------------------|-----------------------------------|
| MAC Flooding    | Layer 2 | Exhaust CAM table → switch broadcasts all     | Port security (max MAC per port)  |
| DHCP Spoofing   | Layer 2 | Rogue DHCP server wins the race               | DHCP Snooping on managed switches |
| ARP Spoofing    | Layer 2 | Forge ARP replies to poison caches            | Dynamic ARP Inspection (DAI)      |
:::

:::code language=mermaid caption="MAC flooding forces a switch into hub mode for passive sniffing; DHCP spoofing redirects all victim traffic to the attacker before the first legitimate connection, both operate below the ARP layer"
flowchart TB
  subgraph MF["MAC flooding"]
    direction LR
    A1["Attacker floods fake<br/>source MACs"] --> S1["Switch address table fills"] --> B1["Switch floods frames<br/>to every port"]
  end
  subgraph DS["DHCP spoofing"]
    direction LR
    A2["Rogue DHCP server"] --> C2["Clients get attacker's<br/>gateway and DNS"] --> B2["Traffic routed via attacker"]
  end
  D["Defenses: port security limits MACs per port;<br/>DHCP snooping trusts only uplink ports"]
  MF ~~~ DS ~~~ D
:::

:::notes
MAC flooding targets the Content Addressable Memory (CAM) table of a network switch. Modern Ethernet switches are fundamentally different from hubs: a hub blindly repeats frames out all ports, while a switch learns which MAC addresses are connected to which ports and forwards frames only to the appropriate destination port. This selective forwarding is what makes switches more efficient and more private than hubs, in a switched network, a passively sniffing host normally only sees broadcast traffic and traffic addressed to its own MAC.

The CAM table that enables this behavior has a finite size. When the CAM table is full, switches cannot learn new MAC addresses. Different switch vendors handle this "table full" condition differently: some switches drop new entries (causing connectivity problems for new hosts), but many commodity switches fail open, reverting to hub-like behavior and flooding all frames out all ports to ensure connectivity is maintained. macof, part of the dsniff suite, generates 155,000 random MAC addresses per minute, exhausting most switch CAM tables in seconds. Once the switch fails open, any host on the segment can passively capture all LAN traffic without any active poisoning.

DHCP spoofing exploits the race condition inherent in the DHCP protocol. When a host first connects to a network, it broadcasts a DHCPDISCOVER message and accepts the first DHCPOFFER it receives. A rogue DHCP server on the same subnet can race the legitimate server to provide an offer, with the malicious configuration. The key fields an attacker can control are the default gateway (Option 3) and DNS server (Option 6) in the DHCP response. By providing their own IP as the default gateway, the attacker positions themselves in the traffic path for all hosts that accept the rogue lease, without any further attack steps required.

The combination of DHCP starvation followed by DHCP spoofing is particularly effective. DHCP starvation exhausts the legitimate DHCP server's address pool by sending DHCPDISCOVER messages with random source MACs (the server allocates one IP per request), causing legitimate clients to receive no response from the real server. The attacker then runs a rogue DHCP server that serves the remaining clients with attacker-controlled configurations. This is essentially a denial-of-service against the DHCP server followed by infrastructure takeover.

TLS and HTTPS are necessary but not sufficient. An attacker who controls DHCP can direct a victim to a rogue DNS server that returns attacker addresses for any domain, bypassing DNSSEC because the victim's resolver is now the attacker's. This chain, DHCP spoof to rogue DNS to man-in-the-middle, shows why defense must address every layer of the stack.

Mitigations are Layer 2 switch features: port security limits the number of MAC addresses learned per switch port (defeating MAC flooding); DHCP snooping designates specific ports as "trusted" (where legitimate DHCP servers reside) and drops DHCP server messages arriving on untrusted ports; Dynamic ARP Inspection (DAI) validates ARP packets against the DHCP snooping binding table; IP Source Guard validates that packets arrive on the correct port for their claimed source IP. Together these form a coordinated Layer 2 security baseline recommended by NIST SP 800-53 under SC-5 (Denial-of-Service Protection) and SI-4 (System Monitoring).
:::

%%%

---
unit: Deep Dive
code: SSL
title: SSL Stripping, Downgrading HTTPS to HTTP
---
:::callout style=soft
**SSL stripping** is a MITM attack that transparently downgrades an HTTPS connection to HTTP. First demonstrated by security researcher Moxie Marlinspike at Black Hat 2009, it exploits the gap between when a user initiates a connection (often via plain HTTP) and when the server attempts to redirect to HTTPS, a window the attacker intercepts and keeps open.
:::

:::flow
User types "bank.com" in browser (no explicit https://)
↓
Browser sends plain HTTP GET to bank.com
↓
Attacker (in MITM position) intercepts the HTTP request
↓
Attacker forwards request to bank.com over HTTPS on the user's behalf
↓
Bank.com responds with HTTPS content including a 302 redirect to https://bank.com
↓
Attacker strips the HTTPS from the 302 response, sends plain HTTP back to victim
↓
User sees bank.com content over HTTP, attacker reads all cleartext traffic
↓
Victim's browser shows no lock icon, but user may not notice
:::

::::columns
::col::
:::list heading="Why SSL Stripping Works"
- Most users do not manually type https://
- Browser initially connects via HTTP, trusts the redirect
- Attacker intercepts the redirect before it reaches the browser
- User receives the content via HTTP, never makes an HTTPS connection
- No certificate error because no HTTPS connection is attempted
:::
::col::
:::list heading="Countermeasures"
- **HSTS** (HTTP Strict Transport Security), browser remembers to always use HTTPS for a domain
- **HSTS Preloading**, domain hardcoded into browser as HTTPS-only before first visit
- **HTTPS Everywhere** (extension), forces HTTPS on all known sites
- Browser padlock training, users should verify HTTPS before entering credentials
:::
::::

:::code language=mermaid caption="SSL stripping maintains two separate connections: the attacker speaks HTTPS to the server and HTTP to the victim, the victim receives legitimate content but over an unencrypted channel the attacker reads in full"
flowchart LR
  V["Victim"] -.->|"HTTP, plaintext"| A["Attacker in the middle"]
  A -->|"HTTPS"| S["Legitimate server"]
  N["Two separate connections: the victim never<br/>sees a certificate, so no warning appears.<br/>Defense: HSTS and HSTS preload"] -.- A
:::

:::notes
SSL stripping is a sophisticated evolution of the basic MITM attack that targets the critical moment of protocol negotiation. Prior to Marlinspike's demonstration at Black Hat DC 2009, the conventional wisdom was that HTTPS links were immune to passive sniffing, an attacker in a MITM position could see the TLS handshake but could not read the encrypted application data. SSL stripping circumvents this by preventing the victim from ever establishing an HTTPS connection in the first place.

The attack exploits a fundamental behavior of web browsing: when a user types "bank.com" into their browser's address bar without a protocol prefix, the browser defaults to http://. The server responds with a redirect to https://bank.com (often a 301 or 302 response). In a normal scenario, the browser follows this redirect and establishes an HTTPS connection. In an SSL stripping attack, the attacker intercepts the initial HTTP request, makes their own HTTPS connection to the server, and rewrites the server's redirect response to remove the "s", changing https:// URLs in the response to http:// URLs. The victim's browser then continues to request content over HTTP, while the attacker maintains the HTTPS connection to the server.

From the victim's perspective, the content looks correct, the page renders normally, the URL in the address bar shows the correct domain name. The only visible indicator is the absence of a padlock icon and the "http://" prefix rather than "https://". Security awareness training emphasizes checking for the padlock, but Marlinspike observed that many users do not notice or are conditioned to ignore its absence. Tools like sslstrip (written by Marlinspike) and BetterCAP's built-in HTTPS proxy automate the attack.

HTTP Strict Transport Security (HSTS, RFC 6797) was the direct technical response to SSL stripping. When a server includes the `Strict-Transport-Security` header in an HTTPS response, the browser records that this domain must only be accessed via HTTPS. On all subsequent visits, for the duration of the max-age period, the browser refuses to make HTTP connections to that domain and upgrades them to HTTPS automatically, before any network connection is made. This browser-side enforcement means there is no HTTP request for the attacker to intercept. However, HSTS requires that the user has visited the site at least once over HTTPS to receive the header, the first visit remains vulnerable.

HSTS preloading addresses the first-visit vulnerability. Browser vendors maintain a preload list (chromium.org/hsts) of domains that should always be accessed via HTTPS, hardcoded into the browser binary. Domains on the preload list are protected from SSL stripping from the very first visit, with no prior HTTPS session required. As of 2025, approximately 140,000 domains are on the Chrome HSTS preload list, including most major banking and government sites.

HSTS, and especially HSTS preloading, defeats the downgrade (SSL stripping) attack: a preloaded domain's browser refuses to make the initial HTTP request at all, so there is no cleartext connection to downgrade. This is why HSTS is recommended in CIS Control 12 and in NIST SP 800-53 SC-8 on transmission integrity.
:::

%%%

---
unit: Comparison
code: CMP
title: DoS vs. DDoS, Scale, Source, and Severity
---
:::callout style=soft
Denial-of-Service (DoS) and Distributed Denial-of-Service (DDoS) attacks both aim to make a resource unavailable by overwhelming it. The critical difference is scale: a DoS originates from a single source; a DDoS coordinates thousands to millions of compromised hosts simultaneously, making volumetric attacks trivially achieve bandwidth levels that overwhelm even well-provisioned targets.
:::

:::table
| Attribute           | DoS                              | DDoS                                          |
|---------------------|----------------------------------|-----------------------------------------------|
| Source              | Single attacker host             | Botnet: thousands–millions of compromised hosts |
| Traffic volume      | Limited by attacker's bandwidth  | Can exceed 1 Tbps (Mirai botnet: 1.2 Tbps, 2016) |
| Attribution         | Easier, single source IP        | Extremely difficult, thousands of IPs worldwide |
| Mitigation          | Block source IP                  | Requires scrubbing infrastructure, anycast     |
| Cost to attacker    | Free (attacker's own machine)    | Botnet rental ($5–$50/hr on dark web)          |
| Legal barrier       | Lower sophistication needed      | Requires botnet infrastructure                 |
:::

::::columns
::col::
:::list heading="DoS Techniques"
- SYN flood (TCP handshake exhaustion)
- ICMP flood (Ping flood)
- UDP flood
- HTTP slow-rate attacks (Slowloris)
- Application-layer (Layer 7) flood
:::
::col::
:::list heading="DDoS Categories"
- **Volumetric**, overwhelm bandwidth (UDP/ICMP flood)
- **Protocol**, exhaust stateful resources (SYN flood, ACK flood)
- **Application**, overwhelm web server logic (HTTP GET flood)
- **Amplification/Reflection**, use third-party servers to amplify (DNS, NTP, memcached)
:::
::::

:::code language=mermaid caption="The fundamental shift from DoS to DDoS is one of scale and distribution: mitigation that works against a single source (IP blocking) is completely ineffective against a distributed botnet spanning multiple countries and ISPs"
flowchart LR
  DOS["<b>DoS</b><br/>One attacking machine<br/>Limited by its own bandwidth<br/>Defense: block the single source"] ~~~ DDOS["<b>DDoS</b><br/>Thousands of botnet nodes worldwide<br/>Combined traffic overwhelms the link<br/>Defense: upstream scrubbing, CDN capacity"]
:::

:::notes
The distinction between DoS and DDoS is not merely academic, it fundamentally determines what mitigation strategies are applicable. A DoS from a single IP can be neutralized by a firewall rule blocking that IP. A DDoS from 500,000 compromised IoT devices distributed across 100 countries cannot be stopped by any amount of IP blocking because the traffic originates from legitimate IP addresses of real (compromised) devices distributed globally, and blocking them all would block legitimate users in those regions.

The SYN flood is the canonical DoS attack at the transport layer. TCP connections require a three-way handshake: SYN → SYN-ACK → ACK. A server allocates memory for a half-open connection after receiving a SYN and sending a SYN-ACK, waiting for the final ACK. A SYN flood sends thousands of SYN packets (often with spoofed source IPs) but never completes the handshake, filling the server's half-open connection table and making it unable to accept new legitimate connections. The mitigation is SYN cookies (RFC 4987), where the server encodes the connection state in the sequence number of the SYN-ACK rather than allocating memory, so no half-open state is maintained until the ACK is received.

Amplification and reflection DDoS combine IP spoofing with protocol amplification factors. The largest DDoS attacks on record have used these techniques: the 2016 Mirai botnet attack against Dyn DNS (1.2 Tbps), the 2018 GitHub DDoS attack using memcached amplification (1.35 Tbps), and the 2020 AWS Shield report of a 2.3 Tbps attack. Memcached amplification, exploiting publicly accessible memcached servers on UDP port 11211, achieved amplification factors of up to 51,000x, meaning 1 byte of attacker traffic produced 51,000 bytes of traffic at the victim. Cloudflare documented a 71 million RPS (requests per second) HTTP/2 DDoS attack in 2023, illustrating the ongoing escalation in attack scale.

DDoS economics are asymmetric. Attack capacity can be rented from illegal "booter" services for tens of dollars an hour, while defending against a terabit-scale flood requires expensive scrubbing infrastructure or a cloud mitigation provider. The barrier to attacking is far lower than the barrier to defending, which is why DDoS persists.

Mitigation strategies for DDoS include: scrubbing centers (traffic is redirected through infrastructure that filters attack traffic before forwarding clean traffic to the target), anycast routing (distributing the load of attack traffic across many geographically distributed nodes, this is how Cloudflare and Akamai absorb large-volume attacks), rate limiting and traffic shaping, RTBH (Remotely Triggered Black Hole) routing which discards all traffic to the victim IP at the ISP level (effective at stopping the attack but also takes the victim offline, a last resort), and BCP 38 ingress filtering which, if universally deployed, would prevent spoofed-source amplification attacks entirely.
:::

%%%

---
unit: Comparison
code: MIT
title: Types of Man-in-the-Middle Attacks
---
:::callout style=soft
**Man-in-the-Middle (MITM)** is a category of attack, not a single technique. Multiple distinct methods can place an attacker "in the middle" of a communication, and they operate at different network layers with different detection profiles and mitigation requirements.
:::

:::table
| MITM Variant          | Layer     | Mechanism                                 | Detection Indicator                    |
|-----------------------|-----------|-------------------------------------------|----------------------------------------|
| ARP Spoofing          | Layer 2   | Forge ARP replies to poison caches        | Duplicate MAC for gateway IP in ARP table |
| DHCP Spoofing         | Layer 2   | Rogue DHCP server wins allocation race    | Unknown DHCP server on network          |
| DNS Spoofing          | Layer 7   | Inject forged DNS responses               | DNS responses not from trusted resolver |
| BGP Hijacking         | Layer 3   | Announce unauthorized route prefixes      | Unexpected AS path in BGP routing tables|
| SSL Stripping         | Layer 7   | Downgrade HTTPS to HTTP                   | Missing HTTPS / lock icon in browser    |
| Evil Twin Wi-Fi       | Layer 1–2 | Rogue AP mimicking legitimate SSID        | Duplicate SSID with different BSSID     |
| ICMP Redirect         | Layer 3   | Forge ICMP redirect messages to reroute   | Unexpected ICMP redirect packets        |
:::

:::callout style=line
The common requirement for all MITM attacks: the attacker must be **on the same network segment** (for L2 attacks), **positioned in the routing path** (for L3 attacks), or **able to intercept DNS** (for application-layer attacks). Physical or logical proximity to the victim is always required.
:::

:::code language=mermaid caption="MITM attacks exist at every layer of the stack: the lower the layer, the broader the impact but the closer the attacker must be to the victim, BGP hijacking works globally; ARP spoofing requires LAN access"
mindmap
  root((MITM by layer))
    Layers 1 and 2
      Evil twin
      MAC flooding
    Layer 2
      ARP spoofing
      DHCP spoofing
    Layer 3
      BGP hijacking
      ICMP redirect
    Layer 7
      DNS spoofing
      SSL stripping
:::

:::notes
The concept of man-in-the-middle is best understood as a positioning objective, the attacker wants to be in the communication path between two parties who believe they are communicating directly. How the attacker achieves that position varies enormously by network layer and available access, which is why understanding MITM as a category is more valuable than memorizing any single technique.

At Layer 2 (Data Link), ARP spoofing and DHCP spoofing require the attacker to be on the same Layer 2 broadcast domain as the victim. This typically means the same physical network segment or the same VLAN. These are highly effective for attacking public Wi-Fi users, corporate LAN users, or any environment where the attacker has wired or wireless network access. The proximity requirement also limits the blast radius: an ARP spoofing attack on a coffee shop Wi-Fi can only target users on that Wi-Fi segment, not users on other networks.

Evil Twin attacks operate at the physical and data link layers simultaneously. The attacker deploys a rogue Wi-Fi access point with the same SSID as a legitimate network (e.g., "Airport Free WiFi") but with their own infrastructure. Client devices that automatically reconnect to known SSIDs may connect to the evil twin rather than the legitimate AP, giving the attacker a MITM position on all traffic from those clients. Evil Twin attacks are particularly effective against 802.11 networks because the SSID is not cryptographically authenticated by default, any AP can broadcast any SSID. WPA3's Enhanced Open (Opportunistic Wireless Encryption) and certificate-based authentication (802.1x/EAP) mitigate Evil Twin attacks, but most public Wi-Fi still uses open (unauthenticated) access or simple pre-shared key WPA2.

At Layer 3, BGP hijacking achieves a global-scale MITM without any proximity requirement, an AS anywhere on the internet can announce fraudulent routes that affect traffic worldwide. ICMP redirect attacks are a more targeted Layer 3 technique: an attacker sends a forged ICMP Type 5 (Redirect) message to a victim, claiming that a more specific route exists via the attacker's address. Older operating systems and network stacks honor ICMP redirects from non-gateway sources, effectively routing the victim's traffic through the attacker. Modern operating systems (Linux, Windows) no longer accept ICMP redirects from non-gateway sources, largely eliminating this vector.

At the application layer, SSL stripping and DNS spoofing achieve MITM without any lower-layer position, they manipulate the application-layer identifiers and security indicators that clients rely on to validate their connections. However, these attacks typically require a lower-layer MITM position first (to intercept the DNS query or the initial HTTP connection), making them combinatorial attacks rather than standalone techniques.

ARP spoofing is a pivot: it establishes a man-in-the-middle position that in turn enables sniffing, session hijacking, SSL stripping and credential theft. Because the downstream attacks depend on it, preventing ARP spoofing with Dynamic ARP Inspection prevents all of them at once.
:::

%%%

---
unit: Misconceptions
code: FAQ
title: "Common Misconceptions: Network Security"
---
:::callout style=soft
Security concepts are frequently misunderstood, leading to dangerous false assumptions. These misconceptions apply to real security decisions, developers deploying "HTTPS" without HSTS, administrators relying on IP blocklists, users trusting URL bars without checking the protocol.
:::

:::table
| Misconception                                      | Reality                                                                                      |
|----------------------------------------------------|----------------------------------------------------------------------------------------------|
| "HTTPS makes me safe from all network attacks"     | HTTPS protects the payload in transit but not DNS resolution, ARP, or session management    |
| "VPNs prevent all eavesdropping"                   | VPNs protect traffic between client and VPN endpoint only; traffic beyond the endpoint is exposed |
| "Switched networks prevent sniffing"               | ARP spoofing, MAC flooding, and DHCP spoofing all defeat switched network privacy           |
| "A padlock icon means the site is safe"            | It means the connection is encrypted, not that the site is legitimate or not phishing       |
| "Firewalls block MITM attacks"                     | Firewalls inspect traffic at the perimeter; MITM attacks happen inside the network          |
| "IPv6 is immune to ARP spoofing"                   | IPv6 uses NDP (Neighbor Discovery Protocol) which is vulnerable to NDP spoofing, same problem, different protocol |
| "Strong passwords protect against session hijacking" | Session hijacking steals the token post-authentication; password strength is irrelevant   |
:::

:::notes
Misconceptions in network security are not merely academic errors, they lead to concrete security failures. Understanding why these misconceptions are wrong is often more valuable than simply memorizing the correct answer, because it builds the mental model needed to reason about novel situations.

**"HTTPS makes me safe from all network attacks"** is perhaps the most dangerous misconception because it contains a large kernel of truth that makes the exception easy to overlook. HTTPS (TLS) does protect the payload of an HTTP connection from eavesdropping and tampering. But it does not protect the DNS lookup that resolves the hostname to an IP address before the HTTPS connection is established. If an attacker poisons the DNS cache or controls the victim's resolver (via DHCP spoofing), the victim may establish a valid HTTPS connection to an IP address that belongs to the attacker, and if the attacker has a valid certificate for the domain (obtained fraudulently or via a compromised CA), the browser will show a valid padlock. HTTPS also does not protect the session token once it is issued: if the token is later stolen via XSS or a separate channel, the HTTPS connection that originally transmitted it provides no further protection.

**"Switched networks prevent sniffing"** was largely true before ARP spoofing became widespread. Switches forward unicast frames only to the destination port, so a passive attacker on a switched network sees only their own traffic and broadcast traffic. But ARP spoofing converts the switched network into a hub from the attacker's perspective by inserting the attacker into the MAC address table mappings. This misconception leads administrators to rely on the switched nature of their infrastructure as a security control rather than deploying DAI and port security.

**"A padlock icon means the site is safe"** conflates connection security with site legitimacy. Browsers show the padlock for any site with a valid HTTPS certificate, including phishing sites with valid certificates obtained from free CAs like Let's Encrypt. As of 2025, more than 80% of phishing sites use HTTPS, attackers understood years ago that users associate the padlock with legitimacy, and they adapted. The padlock's security meaning is limited to: "your connection to this server is encrypted and the server holds a certificate for this domain name." It says nothing about what the server does with your data.

**"IPv6 is immune to ARP spoofing"** reflects incomplete knowledge. IPv6 replaces ARP with the Neighbor Discovery Protocol (NDP), which operates over ICMPv6. NDP's Neighbor Advertisement messages, the IPv6 equivalent of ARP replies, are equally unauthenticated in the base protocol. NDP spoofing attacks are directly analogous to ARP spoofing attacks, with tools like parasite6 and fake_router6 automating the attack. SEND (Secure Neighbor Discovery, RFC 3971) adds cryptographic authentication to NDP, but its deployment is minimal. The same mitigation approach applies: RA Guard (the IPv6 equivalent of DHCP snooping for Router Advertisements) and DHCPv6 Guard protect against NDP-based attacks on managed switches.

Two common misconceptions, that a VPN makes all activity private and that a padlock icon means a site is safe, tend to generate the most debate because personal experience seems to confirm them. A VPN moves trust to the VPN provider rather than removing it, and the padlock certifies only an encrypted connection, not an honest site.
:::

%%%

---
unit: Framework
code: ATK
title: MITRE ATT&CK, Network Attack Techniques
---
:::callout style=soft
The **MITRE ATT&CK** framework catalogs adversary tactics, techniques, and procedures (TTPs) observed in real-world attacks. For network-layer attacks, the relevant tactics span Initial Access, Credential Access, Collection, and Exfiltration, with specific techniques mapping directly to DNS attacks, ARP spoofing, sniffing, and session hijacking.
:::

:::table
| ATT&CK ID  | Technique Name                              | Tactic              | Class 12 Attack          |
|------------|---------------------------------------------|---------------------|--------------------------|
| T1040      | Network Sniffing                            | Credential Access   | Packet capture / sniffing|
| T1557      | Adversary-in-the-Middle                     | Collection          | ARP spoofing, DHCP spoof |
| T1557.001  | LLMNR/NBT-NS Poisoning and SMB Relay        | Collection          | DNS-like poisoning on LAN|
| T1557.002  | ARP Cache Poisoning                         | Collection          | ARP spoofing             |
| T1071.004  | Application Layer Protocol: DNS             | C2                  | DNS tunneling            |
| T1048.003  | Exfiltration Over Alternative Protocol: DNS | Exfiltration        | DNS tunneling            |
| T1110.001  | Brute Force: Password Guessing              | Credential Access   | Session token prediction |
| T1563      | Remote Service Session Hijacking            | Lateral Movement    | Session hijacking        |
| T1565.002  | Stored Data Manipulation                    | Impact              | DNS record manipulation  |
:::

:::list heading="MITRE ATT&CK Navigator Use Cases" style=plain
- Map your organization's attack coverage to identify detection gaps
- Compare threat actor profiles (APT groups) against your monitored techniques
- Prioritize defensive controls based on technique prevalence in relevant threat intelligence
- Document red team findings using a common taxonomy understood across teams
:::

:::code language=mermaid caption="MITRE ATT&CK network technique coverage: techniques covered in Class 12 highlighted, defenders can use this map to ensure detection rules and controls address each relevant TTP"
flowchart TB
  CA["<b>Credential Access</b><br/>T1040 Network Sniffing<br/>T1557 Adversary-in-the-Middle"] --> LM["<b>Lateral Movement</b><br/>T1563 Remote Service Session Hijacking"]
  LM --> CC["<b>Command and Control</b><br/>T1071.004 DNS"]
  CC --> EX["<b>Exfiltration</b><br/>T1048.003 over an unencrypted protocol such as DNS"]
:::

:::notes
The MITRE ATT&CK framework (Adversarial Tactics, Techniques, and Common Knowledge) was first published in 2013 as an internal MITRE project and opened to the public in 2015. It has since become the de facto standard taxonomy for describing adversary behavior in the security industry, used by threat intelligence teams, red teams, blue teams, and security vendors alike. Its value lies in providing a common language: when a red teamer says they used T1557.002 (ARP Cache Poisoning), every stakeholder understands exactly what technique was used, what the potential impact is, and what detections might catch it.

For network-layer attacks, the primary relevant tactics are Credential Access, Collection (which in ATT&CK terms refers to gathering data from the target environment), Lateral Movement, Command and Control, and Exfiltration. T1040 (Network Sniffing) is classified under Credential Access because the primary value of sniffing in most attacks is the capture of credentials, session tokens, or other authentication material from network traffic. T1557 (Adversary-in-the-Middle) is classified under Collection because the MITM position enables collection of data flows that would not otherwise be accessible.

T1557.002 specifically describes ARP Cache Poisoning, and the description in MITRE ATT&CK includes both the attack mechanism (sending unsolicited ARP replies) and detection guidance (monitoring for anomalous ARP traffic patterns). This illustrates one of ATT&CK's key features: each technique entry includes not only the adversary perspective but also data sources and detection suggestions from the defender perspective.

DNS tunneling appears in two technique categories: T1071.004 (under Command and Control, for the C2 channel use case) and T1048.003 (under Exfiltration, for the data exfiltration use case). The same technical mechanism (embedding data in DNS queries and responses) serves both purposes, the ATT&CK framework captures this by classifying it under multiple tactics based on the attacker's objective.

LLMNR/NBT-NS Poisoning (T1557.001) is worth specific attention even though it was not covered explicitly in the main lecture: LLMNR (Link-Local Multicast Name Resolution) and NetBIOS Name Service are Windows-specific name resolution protocols that fall back to broadcast queries when DNS fails. An attacker can respond to these broadcast queries with their own IP address, capturing NTLMv2 credential hashes from hosts attempting to authenticate to the falsely claimed resource. The Responder tool automates this attack and is extremely effective in Active Directory environments. Detection requires disabling LLMNR (via Group Policy) and monitoring for Responder-like traffic patterns (MITRE ATT&CK data source: network traffic content with filter: anomalous LLMNR responses).

The ATT&CK Navigator records which techniques an organization can detect. Mapping the Class 12 network techniques onto it, and comparing with a specific actor's profile such as APT28, connects academic study to real threat-actor behavior and shows where detection is missing.
:::

%%%

---
unit: Worked Example
code: LAB1
title: "Worked Example: Executing an ARP Spoof with arpspoof"
---
:::callout style=soft
This worked example walks through the exact commands used to execute a double-sided ARP poisoning attack using **arpspoof** (from the dsniff suite) in a controlled lab environment. All commands assume Kali Linux, a target victim at 192.168.1.100, and a gateway at 192.168.1.1. This is for educational use in authorized lab environments only.
:::

:::steps
1. **Enable IP forwarding** so captured traffic is forwarded and the victim does not lose connectivity:
   `echo 1 > /proc/sys/net/ipv4/ip_forward`

2. **Identify target IPs** using a network scan:
   `arp-scan --localnet` or `nmap -sn 192.168.1.0/24`

3. **Poison the victim's ARP cache** (tell victim that the gateway's IP maps to your MAC):
   `arpspoof -i eth0 -t 192.168.1.100 192.168.1.1`

4. **Poison the gateway's ARP cache** (tell gateway that the victim's IP maps to your MAC):
   `arpspoof -i eth0 -t 192.168.1.1 192.168.1.100`
   *(Run both arpspoof commands simultaneously in separate terminal windows)*

5. **Verify the attack**, on the victim machine, check ARP table:
   `arp -a`, the gateway IP should now show the attacker's MAC address

6. **Capture intercepted traffic** with Wireshark or tcpdump:
   `tcpdump -i eth0 -w capture.pcap host 192.168.1.100`

7. **Stop the attack and restore ARP tables**, Ctrl+C on both arpspoof instances; legitimate ARP replies will naturally restore correct mappings after ~20 minutes, or send gratuitous ARP from legitimate hosts immediately
:::

:::table
| Step | Command                                          | Purpose                             |
|------|--------------------------------------------------|-------------------------------------|
| 1    | `echo 1 > /proc/sys/net/ipv4/ip_forward`         | Forward packets (prevent DoS on victim) |
| 3    | `arpspoof -i eth0 -t 192.168.1.100 192.168.1.1`  | Poison victim → think attacker is GW |
| 4    | `arpspoof -i eth0 -t 192.168.1.1 192.168.1.100`  | Poison GW → think attacker is victim |
| 6    | `tcpdump -i eth0 -w capture.pcap`                | Capture all forwarded traffic        |
:::

:::notes
This worked example is designed to make the abstract concept of ARP spoofing tangible through specific, executable commands. Understanding not just what to run but why each step is necessary builds deeper conceptual understanding than simply reading about the attack.

Step 1 is frequently forgotten by beginners and causes an immediately obvious symptom: the victim loses internet connectivity the moment ARP poisoning begins. When the victim's traffic arrives at the attacker's machine, the attacker's operating system must forward it to the actual gateway, otherwise the packets are simply dropped. Linux does not forward IP packets between interfaces by default (for security reasons). Writing "1" to /proc/sys/net/ipv4/ip_forward enables the IP forwarding behavior that makes the attack transparent. Without this step, ARP spoofing becomes a trivially detectable denial-of-service (the victim loses connectivity) rather than a stealthy interception.

Step 3 and 4 are both necessary for bidirectional interception. Step 3 causes the victim's outbound traffic to reach the attacker. Step 4 causes the server's responses (arriving at the gateway) to be returned to the attacker rather than directly to the victim. Without step 4, the attacker intercepts only one direction of the conversation, they see the victim's requests but not the server's responses. This partial capture is not only less useful but also disrupts the TCP session (the victim sends a SYN, the attacker intercepts it, the gateway replies to the victim directly, and the victim receives a SYN-ACK for a connection it believes the attacker is proxying, causing confusion). Proper double-sided poisoning is what makes the attack truly transparent.

Step 5, verifying the attack from the victim's perspective, is an important forensic and educational step. Running `arp -a` on the victim machine shows a cache line like "192.168.1.1 at aa:bb:cc:dd:ee:ff [ether] on eth0" where aa:bb:cc:dd:ee:ff is the attacker's MAC address rather than the router's real MAC. This is the exact indicator that Dynamic ARP Inspection would detect and alert on.

From the victim's side, ARP spoofing gives no visible indication unless the ARP table is explicitly inspected, which is why it is dangerous. Configuring static ARP entries, or deploying Dynamic ARP Inspection on managed switches, stops the attack directly.

NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment) provides the framework within which penetration testers use techniques like this in authorized assessments. Students intending to pursue ethical hacking or penetration testing careers should understand that all such tests require written authorization from the system owner, a defined scope, and rules of engagement, and that executing these techniques without authorization on networks you do not own is a criminal offense under 18 U.S.C. § 1030 (Computer Fraud and Abuse Act) and equivalent statutes in other jurisdictions.
:::

%%%

---
unit: Worked Example
code: LAB2
title: "Worked Example: Stealing a Session Cookie with Wireshark"
---
:::callout style=soft
This worked example shows how to extract a session cookie from captured HTTP traffic using Wireshark, and then use that cookie in a browser to hijack an active session, demonstrating why cleartext HTTP is unacceptable for any authenticated session, even on "internal" networks.
:::

:::steps
1. **Prerequisites**, Attacker is in a MITM position (ARP spoofing established) and Wireshark is capturing on the relevant interface.

2. **Filter for HTTP traffic**, In Wireshark, apply display filter:
   `http`

3. **Find a Set-Cookie header**, Look for HTTP responses containing "Set-Cookie". In the packet details, expand "Hypertext Transfer Protocol" → "HTTP/1.1 200 OK" → find "Set-Cookie" header.

4. **Note the session cookie value**, Example:
   `Set-Cookie: PHPSESSID=a1b2c3d4e5f6g7h8i9j0; Path=/; HttpOnly`

5. **Apply a targeted filter** to see all requests using that cookie:
   `http.cookie contains "PHPSESSID"`

6. **Open an attacker-controlled browser**, Open Firefox and navigate to the target application URL.

7. **Inject the stolen cookie**, Open browser DevTools (F12) → Application → Cookies → manually add the cookie with the stolen value.

8. **Refresh the page**, The attacker is now authenticated as the victim. No password was needed.

9. **Observe the lack of detection**, The server sees a valid session token from the correct application; it cannot distinguish the attacker from the legitimate user.
:::

:::table
| Wireshark Filter                     | Purpose                                            |
|--------------------------------------|----------------------------------------------------|
| `http`                               | Show all HTTP traffic                              |
| `http.set_cookie`                    | Show only responses setting cookies               |
| `http.cookie contains "PHPSESSID"`  | Find all requests using a specific session cookie  |
| `frame contains "password"`          | Search all packets for the word "password"         |
| `http.request.method == "POST"`      | Show only form submissions                         |
:::

:::notes
This worked example bridges the gap between the conceptual description of session hijacking and its practical execution, demonstrating exactly how trivially a session can be stolen from unencrypted HTTP traffic. The exercise is deliberately simple in its execution, the technical steps require only Wireshark (freely available and standard in any security curriculum) and a web browser's built-in developer tools, to emphasize that the attack barrier is low while the impact is high.

The critical insight in step 9, "the server cannot distinguish the attacker from the legitimate user", deserves emphasis. Session tokens are bearer tokens: whoever presents the token is assumed to be the legitimate session owner. This is a fundamental design decision in stateless web application architecture (the server does not maintain connection state; it relies entirely on the token for session identification). The security of the entire authentication model therefore depends on the confidentiality of the session token. Any mechanism that exposes the token, HTTP in cleartext, XSS vulnerabilities, insecure cookie attributes, physical shoulder surfing of a developer tool, breaks the authentication model entirely.

The HttpOnly flag visible in step 4 (`Set-Cookie: PHPSESSID=...; HttpOnly`) prevents JavaScript from reading the cookie value, which blocks XSS-based cookie theft. However, HttpOnly provides no protection against network-level interception (sniffing over HTTP). The Secure flag (not present in the example) would prevent the browser from sending the cookie over non-HTTPS connections, its absence is what makes this attack possible. A correctly configured session cookie would have both HttpOnly and Secure set, plus SameSite=Strict to prevent cross-site request forgery.

This example also illustrates a common development mistake: application developers sometimes set HttpOnly and Secure on the login page's cookie but serve other parts of the application over HTTP, assuming that only the login page needs protection. In fact, the session cookie set after login is transmitted on every subsequent request, if any of those subsequent requests go over HTTP, the cookie is exposed. The Secure flag prevents the browser from ever sending the cookie over HTTP, eliminating this mistake regardless of which URLs the application uses HTTP or HTTPS for.

Session hijacking via a stolen cookie is defeated by cookie flags: the Secure flag prevents the cookie from being sent over plain HTTP, and SameSite=Strict prevents it from being sent on cross-site requests. With both set, a captured cookie cannot be replayed over an insecure connection. Deliberately vulnerable practice applications exist for studying this safely; it must never be attempted against production systems or real user sessions.
:::

%%%

---
unit: Checkpoint
code: CHK
title: Mid-Lecture Checkpoint, Knowledge Check
---
:::callout style=soft
Before we proceed to defenses and real-world case studies, take a moment to test your understanding of the core attack concepts covered so far. These questions reflect common exam formats in CompTIA Security+, CEH, and OSCP certification assessments.
:::

:::list heading="Quick-Fire Questions (Answer Mentally Before Reading On)"
1. An attacker sends ARP replies to both the victim and the gateway without being asked. What is this technique called, and what does it enable?
2. A DNS resolver caches a forged record for "bank.com" pointing to 203.0.113.5 (attacker's IP). How long will users be redirected? What controls that duration?
3. Why does SSL stripping not trigger a certificate warning in the victim's browser?
4. What is the difference between blind spoofing and non-blind spoofing?
5. You capture network traffic and see DNS queries with 50-character Base32 labels. What attack should you suspect?
6. An attacker achieves MITM by sending a faster DHCP response than the legitimate server. What attack is this?
7. Which switch feature prevents MAC flooding from succeeding?
:::

:::table
| Question | Answer |
|----------|--------|
| 1 | Gratuitous ARP / ARP spoofing, enables MITM by poisoning both caches |
| 2 | Duration = DNS TTL value in the forged record; attacker sets TTL, can be hours |
| 3 | Because the victim never establishes HTTPS; attacker speaks HTTPS to server on victim's behalf |
| 4 | Blind = no return path (DoS/amplification); Non-blind = bidirectional (session hijack) |
| 5 | DNS tunneling, data encoded in sub-domain labels |
| 6 | DHCP spoofing, rogue DHCP server wins race condition |
| 7 | Port security, limits number of MACs learned per switch port |
:::

:::notes
Mid-lecture checkpoints serve two purposes: they help students consolidate knowledge before moving to applied exercises, and they provide the instructor with real-time feedback on which concepts need additional clarification. Research in educational psychology (particularly the "testing effect" or "retrieval practice" effect documented by Roediger and Karpicke, 2006) consistently shows that active recall during learning improves long-term retention more than passive re-reading. Even a few minutes of self-testing at the midpoint of a lecture significantly improves retention of the material that follows.

Question 1 tests understanding of the mechanism that makes ARP spoofing persistent. Students sometimes understand that ARP spoofing involves sending fake ARP replies but miss that the attacker sends them unsolicited (gratuitously) to both hosts continuously throughout the attack. The correct term "gratuitous ARP" is worth noting because it appears in NIST documentation and Wireshark's ARP analysis heuristics.

Question 2 addresses a nuance about DNS cache poisoning that is often overlooked: the attacker controls the TTL in the forged record. A sophisticated attacker sets a very long TTL (hours or days) so that even after the attack stops, users continue to be redirected. This is why DNS cache poisoning incidents can have impacts that outlast the attack itself, and why ISPs performing an incident response to cache poisoning must explicitly flush the cached records rather than waiting for natural TTL expiration.

Question 3 is the most conceptually challenging: students intuitively expect that an HTTPS protection failure would produce a warning. SSL stripping works precisely because the victim never attempts HTTPS at all, the attacker intercepts the HTTP request before the victim can follow the HTTPS redirect, so from the victim's perspective they are simply loading an HTTP page, which produces no warnings. The only indicator is the absence of HTTPS in the URL bar and the absence of a padlock icon, both of which require the user to actively check and notice.

Question 7 deserves expansion: port security (IEEE 802.1D) limits the number of MAC addresses that can be learned on a single switch port (typically to 1 or 3). When a MAC flooding attack attempts to fill the CAM table by generating thousands of random source MACs from a single port, port security detects the excess MAC addresses and can either restrict the port (allowing only the first N MACs learned) or shut it down entirely (err-disable mode). This both defeats the MAC flooding attack and alerts administrators to suspicious behavior on the affected port.

:::

%%%

---
unit: Defense
code: DNS2
title: DNSSEC, Cryptographic DNS Validation
---
:::callout style=soft
**DNSSEC** (DNS Security Extensions) adds cryptographic signatures to DNS records, allowing resolvers to verify that the data received came from the authorized zone and was not modified in transit. It is the definitive technical countermeasure for DNS cache poisoning and record spoofing.
:::

:::flow
Zone administrator signs DNS records with a private key → creates RRSIG records
↓
Public key (DNSKEY record) is published in the zone
↓
Parent zone signs a hash of the child zone's public key → DS (Delegation Signer) record
↓
Chain of trust established from Root DNS → TLD → authoritative zone
↓
Resolver requests DNSSEC-signed response (DO bit set in query)
↓
Resolver validates RRSIG against DNSKEY; if signature is invalid, response is rejected
↓
Resolver returns SERVFAIL for tampered or poisoned records, prevents cache poisoning
:::

::::columns
::col::
:::list heading="DNSSEC Record Types"
- **RRSIG**, Cryptographic signature for a resource record set
- **DNSKEY**, Public key used to verify RRSIG records
- **DS**, Delegation Signer; links parent to child zone key
- **NSEC/NSEC3**, Authenticated denial of existence (proves a record does NOT exist)
:::
::col::
:::list heading="DNSSEC Limitations"
- Does not encrypt DNS queries (DNS privacy requires DoH/DoT)
- Complex key management and rollover operations
- Adds overhead to DNS response size (amplification risk)
- Requires both authoritative server AND recursive resolver support
- Incomplete global deployment (~30% of zones signed as of 2025)
:::
::::

:::code language=mermaid caption="DNSSEC's chain of trust: every record's signature must be traceable back to the cryptographically anchored DNS root, a break anywhere in the chain causes the resolver to reject the record"
flowchart TB
  R["Root zone<br/>signed with the root KSK (trust anchor)"]
  C[".com zone<br/>DS record held in the root"]
  E["example.com zone<br/>DS record held in .com"]
  RR["A record for www.example.com<br/>with RRSIG signature"]
  R -->|"vouches for"| C -->|"vouches for"| E --> RR
  V["Validating resolver checks each signature<br/>from the root down"] -.- RR
:::

:::notes
DNSSEC (DNS Security Extensions) was developed by the IETF in response to the inherent lack of authentication in DNS, and is documented in RFC 4033 (Introduction), RFC 4034 (Resource Records), and RFC 4035 (Protocol Modifications). While the concept of signing DNS records was proposed as early as 1993 (RFC 1535), practical deployment was delayed for over a decade due to concerns about key management complexity, response size increases, and the operational challenge of maintaining signed zones. The root zone was not signed with DNSSEC until July 15, 2010, over 15 years after the first DNSSEC RFC.

The core mechanism is public-key cryptography applied to DNS resource record sets (RRsets). A zone administrator generates a Zone Signing Key (ZSK) pair and optionally a Key Signing Key (KSK) pair. The ZSK private key signs each RRset in the zone, producing RRSIG records. The ZSK public key is published as a DNSKEY record. The parent zone validates the child's public key by publishing a DS (Delegation Signer) record, a hash of the child's DNSKEY. When a DNSSEC-validating resolver receives a DNS response, it retrieves the RRSIG for the record, the DNSKEY for the zone, and verifies the signature. It then retrieves the DS record from the parent zone and verifies that it matches the DNSKEY, building a chain of trust upward to the root.

The chain of trust is the security model: an attacker who wants to inject a false DNS record must either compromise the zone's private signing key (to forge a valid RRSIG), compromise the parent's DS record (to substitute a different DNSKEY hash), or compromise a CA that issued the zone's signing certificate, none of which is achievable without significant, detectable compromise of the DNS infrastructure itself. This is fundamentally different from classical DNS, where forging a reply requires only guessing a transaction ID.

NSEC and NSEC3 records solve a subtle but important problem: how do you prove that a DNS record does NOT exist, without allowing an attacker to forge the absence? NSEC records provide authenticated denial of existence by listing the next existing record in the zone alphabetically, if your query for "xyz.example.com" gets an NSEC record pointing from "x.example.com" to "z.example.com," you can verify that no record exists between x and z. NSEC3 adds hashing to the record names to prevent "zone walking" (enumerate all hostnames by following NSEC chains).

DNSSEC's incomplete deployment illustrates the tension between security and operational complexity: generating keys, publishing them, distributing them to registrars and rolling them over without breaking resolution worldwide is a heavy burden. The 2018 root KSK rollover, the first replacement of the root zone's trust anchor, nearly caused outages because many resolvers still referenced the old key. This is why simpler defenses, source port randomization (RFC 5452) and response rate limiting, are often prioritized even though DNSSEC is more complete.
:::

%%%

---
unit: Defense
code: ZTA
title: Zero Trust Architecture and Network Attack Prevention
---
:::callout style=soft
**Zero Trust Architecture (ZTA)**, codified in NIST SP 800-207, rejects the implicit trust model that network position implies trustworthiness. It is the architectural response to the class of attacks studied today: because ARP spoofing, DHCP spoofing, and rogue access points can compromise any network-level trust assumption, Zero Trust demands verification of every request regardless of network origin.
:::

:::list heading="Zero Trust Core Tenets (NIST SP 800-207)"
- **Never trust, always verify**, No implicit trust based on network location (LAN ≠ trusted)
- **Assume breach**, Design as if the internal network is already compromised
- **Verify explicitly**, Use all available data points: identity, device health, location, behavior
- **Least privilege access**, Users and devices get minimum access needed, evaluated per-request
- **Microsegmentation**, Divide networks into small zones; lateral movement requires re-authentication
- **Continuous monitoring**, Log and analyze all access attempts and traffic flows
:::

::::columns
::col::
:::list heading="Zero Trust vs. Traditional Perimeter Security"
- Traditional: "inside the firewall = trusted"
- Zero Trust: "every request is untrusted until verified"
- Traditional: wide flat internal networks
- Zero Trust: microsegmented with per-flow authentication
- Traditional: VPN = trusted access
- Zero Trust: VPN provides network path, not trust; additional verification still required
:::
::col::
:::list heading="ZTA Countermeasures to Class 12 Attacks"
- ARP spoofing MITM → microsegmentation limits blast radius
- DNS poisoning → DNS-over-HTTPS to verified resolver; DNSSEC validation
- Session hijacking → short-lived tokens + continuous re-verification
- Credential theft via sniffing → mTLS (mutual TLS) replaces bearer tokens
- Lateral movement after compromise → per-session access control checks
:::
::::

:::code language=mermaid caption="Zero Trust removes the privileged position of the internal network: a compromised host inside the LAN must re-authenticate for every resource access, limiting the impact of ARP spoofing and lateral movement"
flowchart LR
  U["Users, devices, applications<br/>inside or outside the old perimeter"] --> PEP["Policy Enforcement Point"]
  PEP <-->|"allow or deny?"| PDP["Policy Decision Point"]
  ID["Identity provider"] --> PDP
  DP["Device posture"] --> PDP
  TI["Threat intelligence"] --> PDP
  PEP -->|"per-session access"| R["Resource"]
:::

:::notes
Zero Trust Architecture represents the conceptual evolution from perimeter-based security (the "castle and moat" model) to a model that treats every network location, device, and user as potentially compromised until proven otherwise. NIST SP 800-207, published in August 2020, provides the authoritative federal framework for ZTA implementation and has been widely adopted by enterprise security architects as well as mandated by U.S. Executive Order 14028 (Improving the Nation's Cybersecurity, May 2021) for federal agencies.

The relevance of ZTA to Class 12's attack content is direct and significant. Every attack studied today exploits an implicit trust assumption that traditional network architectures make: ARP poisoning works because the victim's OS trusts any ARP reply it receives; DNS cache poisoning works because resolvers trust DNS responses that match transaction IDs; session hijacking works because web servers trust any request presenting a valid session token; DHCP spoofing works because clients trust the first DHCP offer they receive. Zero Trust's principle of "never trust, always verify" is a systematic rejection of all of these assumptions.

In a Zero Trust implementation, even a host on the "internal" LAN cannot access resources without presenting verified credentials and a health certificate for each request. This means that even if an attacker successfully performs ARP spoofing and achieves a MITM position, they gain access to network traffic, but every application the victim communicates with also requires authentication that the attacker cannot forge (assuming mutual TLS and modern identity protocols are in use). The attacker may capture traffic, but if that traffic is TLS-encrypted end-to-end with mutual authentication, the captured ciphertext is useless.

Microsegmentation is particularly relevant as a countermeasure. In a traditionally flat Layer 2 network, ARP spoofing affects the entire broadcast domain. With microsegmentation, the broadcast domain is reduced to the minimum necessary, in some implementations, each device is in its own isolated VLAN with access controlled by policy rather than network topology. An attacker who compromises one segment cannot ARP spoof devices in adjacent segments because they are not on the same Layer 2 broadcast domain.

The "assume breach" principle is perhaps the most psychologically difficult aspect of Zero Trust to adopt, because it requires organizations to design security controls as if the internal network is already compromised, a mindset shift from traditional security thinking. However, this assumption aligns precisely with the reality demonstrated by Class 12 attacks: an attacker on public Wi-Fi, or an insider threat on a corporate LAN, can compromise Layer 2 infrastructure without any external attack. Security controls must remain effective even in that scenario.

Zero Trust Architecture is not a product but an architecture that ties together identity management, multi-factor authentication, endpoint detection and response, and SIEM/SOAR. Understanding the specific Class 12 attacks that motivated ZTA gives a stronger intuition for why each component is necessary.
:::

%%%

---
unit: Deep Dive
code: NTP
title: NTP Amplification, Weaponizing Time Servers
---
:::callout style=soft
**NTP amplification** is a reflection/amplification DDoS technique that exploits the Network Time Protocol's monlist command to generate a response up to 556 times larger than the query. By spoofing the victim's IP as the source, the attacker directs this amplified traffic at the target, one of the highest amplification factors of any known DDoS vector.
:::

::::columns
::col::
:::list heading="Attack Mechanics"
- NTP's "monlist" command returns a list of the last 600 hosts that queried the NTP server
- A single 8-byte monlist request generates up to 4,460 bytes of response
- Amplification factor: ~556x
- Attacker sends monlist requests with victim's IP as source (IP spoofing)
- NTP server sends 556x amplified response to victim
- Botnet of hundreds of hosts: 1 Mbps of queries generates ~556 Mbps at victim
:::
::col::
:::list heading="Defense"
- Disable NTP monlist command (`noquery` directive in ntpd.conf)
- Upgrade to ntpd 4.2.7p26+ (monlist disabled by default)
- Apply BCP 38 ingress filtering (blocks spoofed source traffic)
- Use Response Rate Limiting on NTP servers
- Block UDP/123 inbound from untrusted sources at perimeter
- Deploy DDoS scrubbing infrastructure for volumetric attack resilience
:::
::::

:::table
| DDoS Amplification Vector | Amplification Factor | Protocol      | Default Port |
|---------------------------|---------------------|---------------|--------------|
| NTP (monlist)             | ~556x               | UDP           | 123          |
| DNS (ANY query)           | ~28–54x             | UDP           | 53           |
| Memcached (stats items)   | ~51,000x            | UDP           | 11211        |
| SSDP (UPnP)               | ~30x                | UDP           | 1900         |
| CharGen                   | ~358x               | UDP           | 19           |
:::

:::code language=mermaid caption="NTP monlist amplification achieves 556x traffic multiplication: 1 Mbps of attacker queries generates 556 Mbps at the victim, combined with IP spoofing, the attack is nearly untraceable and extremely bandwidth-efficient"
flowchart LR
  A["Attacker"] -->|"small request,<br/>victim's address forged as source"| N1["Open NTP server"]
  A --> N2["Open NTP server"]
  A --> N3["Open NTP server"]
  N1 ==>|"response up to 556x larger"| V["Victim"]
  N2 ==> V
  N3 ==> V
  D["Defenses: disable monlist, BCP 38 ingress filtering,<br/>upstream DDoS scrubbing"] -.- N2
:::

:::notes
NTP amplification exploits a design feature of NTPv4's "monlist" extension command, documented in the NTP reference implementation (ntpd). The monlist command was designed for debugging purposes: it returns a list of the last 600 remote IP addresses that have queried the NTP server, along with statistics about their queries. This is useful for an NTP administrator troubleshooting synchronization issues but catastrophic when combined with IP spoofing.

The attack was first documented at scale in 2013–2014. The FBI issued an advisory in December 2013 warning of widespread NTP amplification attacks. The attack was particularly impactful because of the extremely high amplification factor: an 8-byte monlist query can generate up to 100 UDP packets totaling 4,460 bytes in response, a 556x amplification factor. This is far higher than DNS amplification (typically 28–54x) and enables attackers with modest bandwidth to generate very large attack volumes.

The 2014 CloudFlare report on NTP amplification documented attacks exceeding 400 Gbps, targeting organizations in Europe and Asia. The available pool of vulnerable NTP servers was enormous: ntpd's monlist command was enabled by default in versions prior to 4.2.7p26 (released December 2013), meaning every NTP server running an older version with a public internet IP was a potential amplifier. Attackers used tools like ntpdc and nmap scripts to enumerate open NTP servers and send spoofed monlist requests en masse.

The mitigation is straightforward and should have been applied universally but wasn't, due to the distributed nature of NTP server administration. The ntpd.conf setting "noquery" disables the monlist command and all other diagnostic queries. The CERT/CC advisory (VU#348126) provided specific configuration guidance, and the upgrade to ntpd 4.2.7p26 disabled monlist by default. NIST SP 800-81r2 recommends restricting NTP diagnostic access to trusted management networks only.

This attack exemplifies the broader pattern of amplification DDoS: any stateless UDP-based protocol that produces significantly larger responses than requests, combined with any publicly accessible server running that protocol, can be weaponized for amplification. Memcached (amplification factor of up to 51,000x, exploited in the 2018 GitHub DDoS attack reaching 1.35 Tbps) and SSDP (UPnP, ~30x amplification) follow the same pattern. The common defense across all amplification vectors is BCP 38 ingress filtering, if ISPs blocked packets with spoofed source addresses at the network edge, the victim's IP could not be spoofed as the source, and the amplified responses would simply return to the actual attacker rather than the victim. The persistent failure to deploy BCP 38 universally, despite it being documented since 2000, is one of the most consequential gaps in global internet security.

Amplification reflection turns a small query into a large flood: a Memcached server can return about 51,000 bytes for one spoofed byte of query. In the 2018 GitHub attack, roughly 100 exposed Memcached servers generated 1.35 Tbps. Memcached serves no legitimate internet-facing purpose, so every exposed instance is a latent DDoS weapon.
:::

%%%

---
unit: Deep Dive
code: TLS
title: TLS 1.3, Why the Latest Version Matters
---
:::callout style=soft
**TLS 1.3** (RFC 8446, published 2018) is the current version of Transport Layer Security and introduces major security improvements over TLS 1.2 and earlier. Understanding what changed, and specifically why older TLS versions were vulnerable, connects directly to the network attack content in this class.
:::

:::table
| Feature                   | TLS 1.2                           | TLS 1.3                                    |
|---------------------------|-----------------------------------|--------------------------------------------|
| Handshake round trips      | 2 RTT                             | 1 RTT (0-RTT option for resumption)        |
| Cipher suites             | 37 options (many weak)            | 5 options (all strong, no weak algorithms) |
| RSA key exchange          | Supported (no forward secrecy)    | Removed, only ECDHE (forward secrecy)     |
| Downgrade attacks         | Possible (POODLE, BEAST, etc.)    | Prevented by design                        |
| Session resumption        | Session IDs / session tickets     | PSK (Pre-Shared Key) with forward secrecy  |
| Record protocol encryption| Optional                          | Mandatory, all handshake messages encrypted|
| Weak ciphers (RC4, 3DES)  | Still negotiable                  | Completely removed                         |
:::

:::list heading="Forward Secrecy, Why It Matters for Session Hijacking"
- In TLS 1.2 with RSA key exchange: if the server's private key is ever compromised, an adversary can decrypt ALL past recorded TLS sessions retroactively
- In TLS 1.3 (ECDHE only): each session uses a unique ephemeral key pair, compromising the server's long-term key does NOT expose past sessions
- Forward secrecy directly limits the value of long-term packet capture to an attacker who does not have the per-session keys
:::

:::code language=mermaid caption="TLS 1.3 eliminates an entire class of downgrade and retroactive decryption attacks by removing all weak cipher suites and mandating ephemeral key exchange, upgrades from TLS 1.2 are not optional but a security imperative"
flowchart LR
  T12["<b>TLS 1.2</b><br/>2 round trips to set up<br/>Weak ciphers still negotiable<br/>RSA key exchange allowed<br/>Stolen server key decrypts past sessions"] -->|"TLS 1.3 changes"| T13["<b>TLS 1.3</b><br/>1 round trip (0-RTT optional)<br/>Only strong AEAD ciphers<br/>Ephemeral (EC)DHE only<br/>Forward secrecy for every session"]
:::

:::notes
TLS (Transport Layer Security) is the protocol that provides confidentiality, integrity, and authentication for application-layer protocols like HTTPS, SMTPS, and IMAPS. Understanding TLS version differences is directly relevant to the network attack content in this class because many historical TLS vulnerabilities enabled MITM attacks, session decryption, and downgrade attacks that bypass the protections HTTPS is supposed to provide.

The evolution from SSL (Secure Sockets Layer, now completely deprecated) through TLS 1.0, 1.1, 1.2, and 1.3 represents a series of security improvements driven by discovered vulnerabilities. Notable vulnerabilities in earlier TLS versions include: POODLE (CVE-2014-3566), which exploited SSLv3's CBC padding behavior and allowed MITM attackers to decrypt session content with sufficient patient observation; BEAST (CVE-2011-3389), which exploited TLS 1.0's CBC initialization vector predictability; CRIME and BREACH, which exploited TLS compression to leak session tokens; and ROBOT (CVE-2017-13099), which exploited RSA PKCS#1 v1.5 padding in TLS 1.2's RSA key exchange to decrypt captured sessions.

TLS 1.3 addresses all of these by removing the vulnerable components entirely rather than patching them. The elimination of RSA key exchange in favor of mandatory ECDHE (Elliptic Curve Diffie-Hellman Ephemeral) is the single most impactful change for long-term security. RSA key exchange allows a session to be decrypted retroactively if the server's private key is ever obtained, an attacker who has been recording TLS sessions for years can decrypt all of them if they eventually compromise or purchase the server's private key. ECDHE prevents this: each session generates a unique ephemeral key pair that exists only in memory during the session and is discarded immediately after. Even if the server's long-term certificate private key is compromised, past sessions cannot be decrypted.

This property, forward secrecy (also called Perfect Forward Secrecy, PFS), is critical in the context of long-term adversarial packet collection. Intelligence agencies and advanced persistent threat (APT) groups are known to collect and store encrypted traffic with the expectation of decrypting it later when keys become available. Forward secrecy makes this "collect now, decrypt later" strategy ineffective, since the per-session keys never leave memory and are never stored anywhere the attacker can reach.

The mandatory encryption of the TLS 1.3 handshake itself is another significant improvement. In TLS 1.2, the server certificate (including the server's hostname via Server Name Indication, SNI) is transmitted in cleartext during the handshake. This means a network observer can see which HTTPS sites a client is connecting to even without being able to decrypt the session content. TLS 1.3's Encrypted Client Hello (ECH), while not part of the base RFC 8446 standard but available as an extension, addresses this by encrypting the SNI field.

NIST SP 800-52 Rev. 2 requires TLS 1.2 as a minimum and recommends TLS 1.3, and a 2021 CISA/NSA guidance deprecates TLS 1.0 and 1.1. In practice this means disabling TLS 1.0 and 1.1 on servers, load balancers and API gateways, preferring TLS 1.3, and ordering cipher suites with ECDHE first. Free online analyzers grade a server's TLS configuration against current practice.
:::

%%%

---
unit: Synthesis
code: INC
title: "Real-World Incident: The 2018 MyEtherWallet BGP + DNS Hijack"
---
:::callout style=soft
In April 2018, attackers combined **BGP hijacking** and **DNS cache poisoning** to steal approximately $160,000 USD worth of Ethereum cryptocurrency from MyEtherWallet.com users over a two-hour period. The incident demonstrates how multiple Class 12 attack techniques, chained together, produce real-world financial impact at scale.
:::

:::steps
1. **BGP Hijack**, Attackers announced BGP routes for Amazon Route 53's IP prefix (205.251.196.0/24), causing BGP routers to forward DNS queries to attacker-controlled servers instead of Amazon's legitimate DNS infrastructure.

2. **Rogue DNS Server**, The attackers operated a rogue DNS server on the hijacked IP range that responded to queries for "myetherwallet.com" with the attacker's server IP (176.9.211.225, a server in Germany).

3. **Victim Connection**, MyEtherWallet users who queried DNS during the hijack received the attacker's IP for myetherwallet.com. Their browsers navigated to the attacker's server.

4. **TLS Certificate Warning**, The attacker's server could not present a valid TLS certificate for myetherwallet.com. Browsers displayed an "invalid certificate" warning.

5. **Users Ignored Warning**, Many users clicked through the certificate warning, loaded the phishing version of MyEtherWallet, and entered their private keys.

6. **Cryptocurrency Theft**, The attacker's server drained wallets: approximately 215 ETH (worth ~$160,000 USD at the time) was transferred to attacker-controlled wallets.

7. **Discovery**, Security researchers noticed anomalous BGP announcements and Amazon Route 53 connectivity issues. The hijack was identified and BGP routes restored within approximately 2 hours.
:::

:::callout style=line
**Key Lesson**: The TLS certificate warning was the one security control that could have prevented this attack for every user who encountered it. Users who heeded the warning, the browser's explicit alert that something was wrong, were protected. Those who dismissed it were compromised.
:::

:::code language=mermaid caption="The 2018 MyEtherWallet incident: a two-hour window of BGP and DNS attack infrastructure generated $160,000 in cryptocurrency theft, the only technical control that worked was the TLS certificate warning that many users dismissed"
flowchart TB
  A["April 24, 2018, about 11:00 UTC<br/>Bogus BGP routes claim part of Amazon Route 53's address space"]
  B["Hijacked DNS answers send myetherwallet.com to a phishing server"]
  C["The fake site uses an untrusted certificate; some users click through the warning"]
  D["Users report problems on Reddit"]
  E["About 13:10 UTC<br/>Routes withdrawn, about $150,000 in Ether stolen"]
  A --> B --> C --> D --> E
:::

:::notes
The 2018 MyEtherWallet BGP hijack is one of the most instructive real-world examples of chained network attacks because it combines multiple techniques studied in this class, BGP hijacking (covered in our BGP slide), DNS attack infrastructure (our DNS Attacks slide), and the human factor of users ignoring security warnings (connecting to our Common Misconceptions slide about padlocks and certificate warnings).

The technical details of the BGP component are particularly informative. The attackers hijacked IP space belonging to Amazon Route 53, Amazon's managed DNS service used by millions of domains including myetherwallet.com. By announcing a more-specific BGP prefix (/24 vs. the legitimate /20 or /21), the attackers caused BGP routers at multiple ISPs to route DNS queries to their infrastructure rather than Amazon's legitimate Route 53 servers. The attackers operated their rogue infrastructure within the hijacked IP range, so from the perspective of BGP routing, the source appeared to be Amazon's address space.

The DNS component was straightforward: the rogue DNS server simply returned the attacker's server IP for any query about myetherwallet.com. This is not a sophisticated DNS attack, the complexity was entirely in the BGP hijack that caused DNS queries to reach the rogue server in the first place. Once the BGP hijack was in place, the DNS manipulation was trivial.

The TLS certificate issue is the most important lesson for end users. The attacker's server could not obtain a valid TLS certificate for myetherwallet.com, certificate authorities perform domain validation (DV) checks to confirm that the certificate requester controls the domain. Because the attacker did not control the domain's DNS records through the legitimate registrar (only temporarily through the BGP/DNS attack), they could not pass domain validation and therefore could not obtain a trusted certificate. This caused browsers to display explicit security warnings: "Your connection is not private" with details about the certificate mismatch.

These warnings are not cosmetic. They represent the browser's identity verification layer, the assertion that the server you are connecting to has been cryptographically verified as the legitimate owner of the domain. When users click through certificate warnings for financial services (or indeed, any site), they are explicitly disabling the most powerful defense the browser provides. Security training should be unambiguous: a certificate warning on a financial or sensitive site is a critical security indicator. Do not proceed. Close the tab and report the anomaly.

A browser certificate warning ("Your connection is not private") is a security-critical signal, not a nuisance. The residual human-factor attack works because fake sites are built to look exactly like the real one and a hurried user is motivated to click through, which is why the warning alone does not fully protect against a convincing man-in-the-middle site.

BGP hijacking incidents are tracked by organizations including CAIDA (Center for Applied Internet Data Analysis), Cloudflare's BGP monitoring (bgp.tools), and Internet Society's MANRS (Mutually Agreed Norms for Routing Security) initiative. MANRS provides a framework for ISPs to implement routing security practices including RPKI validation, route filtering, and anti-spoofing, the technical countermeasures that would prevent BGP hijacking attacks like the one that enabled the MyEtherWallet incident.
:::

%%%

---
unit: Defense
code: MON
title: Detecting Network Attacks, Monitoring and Indicators
---
:::callout style=soft
Every network attack studied in this class leaves detectable traces. The challenge is not that detection is impossible, it is that detection requires deploying the right monitoring tools, knowing what patterns to look for, and having processes to act on alerts quickly. This slide maps each attack to its observable indicators.
:::

:::table
| Attack               | Observable Indicator                                              | Detection Tool/Method                        |
|----------------------|-------------------------------------------------------------------|----------------------------------------------|
| ARP Spoofing         | Duplicate IP-to-MAC mappings; gratuitous ARP flood               | Wireshark (arp.duplicate-address-detected), DAI alerts |
| MAC Flooding         | Thousands of unique source MACs from one port in seconds         | Switch port security counters, SNMP alerts    |
| DHCP Spoofing        | Unexpected DHCP Offer from non-authorized MAC/IP                 | DHCP Snooping logs on managed switches        |
| DNS Cache Poisoning  | DNS response from unexpected server IP; TTL anomalies            | DNS monitoring, DNSSEC validation failures    |
| DNS Tunneling        | High-entropy sub-domains; high query rate to single domain       | DNS analytics, threat intel feeds             |
| SSL Stripping        | HTTP traffic to normally-HTTPS domains; missing Secure cookies   | Web proxy logs; HSTS violation reports        |
| Session Hijacking    | Concurrent sessions from different geolocations; session anomalies | Application logs; UEBA (behavioral analytics)|
| BGP Hijacking        | Unexpected AS-path changes; route origin changes                 | BGP monitoring (bgp.tools, RIPE RIS)          |
| NTP Amplification    | Large UDP flows from port 123; spoofed source addresses          | NetFlow/sFlow analysis; ISP notification      |
:::

:::list heading="Detection Stack Priorities" style=plain
- **Layer 2**: Enable DAI + DHCP Snooping on all managed switches, automatic and low false-positive
- **DNS**: Deploy DNS logging with query analysis; integrate threat intelligence for known tunneling domains
- **Network Flow**: Collect NetFlow/IPFIX from all routers; baseline normal traffic and alert on volumetric anomalies
- **Application**: Log all authentication events, session creations, and concurrent session anomalies; feed to SIEM
- **BGP**: Subscribe to BGP monitoring service (Cloudflare Radar, RIPE RIS) for your own IP prefix alerts
:::

:::notes
Detection of network attacks requires matching the monitoring strategy to the attack technique's observable footprint. Too many security programs invest heavily in perimeter controls (firewalls, IDS at the internet edge) while neglecting internal network monitoring where Layer 2 attacks like ARP spoofing operate. NIST SP 800-137 (Information Security Continuous Monitoring) and CIS Control 13 (Network Monitoring and Defense) both emphasize that internal network visibility is as important as perimeter protection.

For ARP spoofing, the most effective automated detection is Dynamic ARP Inspection (DAI) on managed switches, which simultaneously prevents and alerts on ARP anomalies. Wireshark's built-in "ARP address conflict detected" expert information item flags any scenario where two different MAC addresses respond to the same IP, which is the signature of ARP spoofing. In environments without managed switches, host-based ARP monitoring tools like arpwatch (Linux) or XArp (Windows) can alert on ARP cache changes. A key operational requirement is baselining: knowing what the normal ARP state looks like makes anomaly detection feasible; without a baseline, every ARP cache change generates a false positive.

DNS tunneling detection requires analyzing DNS traffic at a statistical level, not just inspecting individual packets. The key metrics are: query length (DNS tunneling tools generate sub-domain labels much longer than legitimate hostnames, iodine generates 255-character maximum-length queries), entropy (Base32/Base64 encoded data has statistically higher Shannon entropy than human-readable domain names), and query rate (a host performing DNS tunneling may generate hundreds of queries per minute to a single domain, far above normal resolution patterns). DNS security products (Cisco Umbrella, Cloudflare Gateway, Infoblox BloxOne) apply machine learning to these metrics to identify tunneling with low false-positive rates.

BGP monitoring is a specialized area but essential for organizations that own IP address space. BGP hijacking of your prefix will cause your address space to appear in unexpected AS paths, a routing alert that services like RIPE RIS (Routing Information Service), CAIDA's BGPStream, and Cloudflare Radar can detect and alert on in near real-time. The MANRS (Mutually Agreed Norms for Routing Security) initiative provides a self-assessment framework for organizations hosting BGP infrastructure.

Session anomaly detection, identifying stolen session tokens in use, is the most challenging of these detections because a stolen token is, by definition, valid. The primary signals are behavioral: a session that simultaneously appears to originate from two different geographic locations, a session that appears at an unusual time for that user, or a session on an unfamiliar device type or browser. UEBA (User and Entity Behavior Analytics) systems build models of normal user behavior and alert on deviations, connecting to the SIEM and SOAR capabilities that will be covered in later classes.

CIS Controls distinguish foundational controls (inventory, configuration and vulnerability management) from the monitoring controls (network monitoring, malware defense, data recovery) that detect when the foundations fail. No program is complete with preventive controls alone; the "assume breach" mindset pairs prevention to lower the probability of success with detection to limit the impact of the attacks that get through.
:::

%%%

---
unit: Summary
code: FIN
title: Class 12 Wrap-Up, Key Takeaways
---
:::pullquote
Protocols trust. Attackers exploit trust. Defenders verify.
:::

:::list heading="Core Concepts Mastered in Class 12"
- **Network protocols as attack surfaces**, Every protocol's design assumptions are potential attack vectors
- **DNS attacks**, Cache poisoning, tunneling, amplification, and the Kaminsky attack
- **IP spoofing**, Blind vs. non-blind spoofing, reflection/amplification DDoS, BCP 38
- **ARP spoofing**, Layer 2 MITM, double-sided poisoning, MAC flooding, DHCP spoofing
- **Packet sniffing**, Promiscuous mode, MITM position, cleartext protocol exploitation
- **Session hijacking**, Token theft, replay, fixation, and the role of cookie security attributes
- **Defense mechanisms**, DNSSEC, DAI, DHCP snooping, HSTS, TLS 1.3, Zero Trust
- **Real-world incidents**, Kaminsky 2008, MyEtherWallet 2018, BGP hijacking events
- **Detection**, ARP monitoring, DNS analytics, NetFlow analysis, behavioral anomaly detection
:::

:::table
| Framework | Class 12 Relevance |
|-----------|--------------------|
| NIST SP 800-81 | DNSSEC deployment guidance |
| NIST SP 800-207 | Zero Trust Architecture |
| NIST SP 800-53 SC-8 | Transmission confidentiality and integrity |
| BCP 38 (RFC 2827) | Ingress filtering against IP spoofing |
| MITRE ATT&CK T1040, T1557, T1071.004 | Network sniffing, MITM, DNS C2 |
| RFC 6797 | HTTP Strict Transport Security (HSTS) |
| RFC 8446 | TLS 1.3 specification |
| ISO/IEC 27001 A.13 | Network security management controls |
:::

:::code language=mermaid caption="Class 12 complete concept map: six attack families, their enabling mechanisms, real-world examples, and corresponding defenses, each branch connects to multiple NIST, IETF, and MITRE standards"
mindmap
  root((Network vulnerabilities and attacks))
    DNS attacks
      Cache poisoning
      Tunneling
      Amplification
    IP spoofing
      Blind and non-blind
      Reflection DDoS
    ARP spoofing
      MITM
      MAC flooding
      DHCP spoofing
    Sniffing
      Promiscuous mode
      Session hijacking
    Denial of service
      Floods
      Amplification
    Defenses
      DNSSEC, DHCP snooping
      Dynamic ARP inspection
      TLS everywhere
:::

:::notes
Class 12 has covered the most fundamental class of network attacks: those that exploit the trust assumptions built into TCP/IP's foundational protocols. These are not exotic zero-day vulnerabilities, they are attacks that have been documented, exploited, and studied for decades, and that remain effective in 2025 because the underlying protocols continue to be deployed in their original, unauthenticated forms across billions of devices worldwide.

The meta-lesson is the most important one to internalize: security is not a feature that can be added to an insecure system by wrapping it in encryption. The MyEtherWallet incident showed that HTTPS (TLS) itself depends on correct DNS, and DNS has no built-in authentication without DNSSEC. The ARP spoofing attack chain showed that HTTPS depends on the traffic reaching the correct server, and on switched networks without DAI, ARP can redirect that traffic. Zero Trust Architecture is the architectural acknowledgment of this reality: no single security control is sufficient because every control depends on other components being correctly implemented and operating as designed.

Looking forward, the concepts from Class 12 are the foundation for the next three classes. Class 13 on firewalls and network controls shows which of these attacks a perimeter rule can stop and which it cannot. Class 14 on IDS and IPS shows how the detection indicators discussed in this class (ARP anomalies, DNS entropy, NetFlow patterns) are operationalized in real security monitoring products. Class 15 on network segmentation explains why perimeter controls alone are insufficient against internal network attacks. The wireless versions of these attacks, evil twins and Wi-Fi sniffing, were covered in Class 7.

A capstone-style analysis task gives students a packet capture of an ARP spoofing attack followed by credential capture over HTTP and asks them to identify the attacker and victim addresses, locate the captured credentials, determine the protocol used, and list controls that would have prevented it. This mirrors real incident-response work and tests protocol knowledge, defensive control selection and standards alignment at once.
:::
