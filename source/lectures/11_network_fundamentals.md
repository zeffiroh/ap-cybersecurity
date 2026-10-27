---
deck:
  title: Network Fundamentals
  kicker: Class 11
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 11
  description: Packets, protocols, TCP/IP, addressing, and ports, the plumbing every other network class builds on.
  topics: [Networks, Packets, Protocols, TCP/IP, IP Addressing, Ports]
---

---
title: Network Fundamentals
cover: true
---
:::text class=sub
Before you can defend a network, you have to know how it actually works
:::
::::columns
::col::
:::list heading="Core Concepts" style=plain
- TCP/IP Model
- Packet Structure and Flow
- Port Numbers and Services
:::
::col::
:::list heading="Key Protocols" style=plain
- IP (Internet Protocol)
- TCP (Transmission Control Protocol)
- UDP (User Datagram Protocol)
:::
::col::
:::list heading="Security Relevance" style=plain
- Attack Surface Identification
- Traffic Analysis
- Vulnerability Mapping (e.g., CVE-2021-34527 "PrintNightmare")
:::
::::
:::image src="images/11_network_fundamentals_overview.png" alt="Overview diagram showing TCP/IP stack layers, packets flowing between devices, and security controls layered on top" caption="Network fundamentals form the substrate on which every cybersecurity security control is built" width=full
:::
:::notes
Understanding network fundamentals is essential for effective cybersecurity defense. Networks operate using layered communication models, the most widely adopted being the TCP/IP model, which consists of four layers: the Network Interface Layer, Internet Layer, Transport Layer, and Application Layer. Each layer encapsulates data with specific headers that provide routing, segmentation, and service information necessary for successful communication.

At the Internet Layer, the Internet Protocol (IP), in its two prevalent versions, IPv4 and IPv6, assigns logical addresses to devices, enabling data to traverse diverse and heterogeneous networks. These IP addresses serve as identifiers for source and destination nodes. Above this, the Transport Layer ensures reliable or fast data delivery using protocols such as Transmission Control Protocol (TCP), which is connection-oriented and provides error correction and sequencing, and User Datagram Protocol (UDP), which is connectionless and prioritizes speed over reliability. These transport protocols use port numbers, ranging from 0 to 65535, to identify specific services or applications running on a host. Well-known ports (0–1023) are reserved for standard services such as HTTP (port 80), HTTPS (port 443), and SMB (port 445).

Packets are the fundamental units of data transmission. Each packet contains headers with metadata such as source and destination IP addresses, port numbers, sequence numbers (in TCP), and the payload itself. Analyzing packet structures is critical for intrusion detection, forensic investigations, and identifying malicious traffic patterns. For example, CVE-2021-34527, also known as "PrintNightmare," exploited the SMB protocol over TCP port 445, allowing attackers to execute remote code and move laterally within a network. This real-world example illustrates that attacks do not emerge from a vacuum, they exploit specific, identifiable protocol behaviors at precisely defined layers of the stack.

Consider an analogy: the network stack is like a postal system. The Application Layer writes the letter (the content and meaning). The Transport Layer packages the letter into an envelope with a tracking number (TCP) or sends it first-class without tracking (UDP). The Internet Layer writes the delivery address (IP addresses) on the outside of the envelope. The Network Interface Layer is the physical act of loading it onto a truck and driving it to the next sorting facility. Each layer has a distinct job and communicates only with the layers immediately above and below it, a design principle that makes the system both modular and maintainable, but also creates well-defined attack surfaces that adversaries can target.

Frameworks such as NIST Special Publication 800-53 emphasize the importance of understanding network architecture for implementing access controls, monitoring mechanisms, and secure configurations. Similarly, ISO/IEC 27001 mandates that organizations conduct risk assessments based on a clear understanding of data flows and communication pathways to manage network security effectively. Without mastering these foundational elements, defensive strategies such as firewalls, intrusion detection/prevention systems (IDS/IPS), and network segmentation lack precision and overall efficacy.

From a historical perspective, early networks like ARPANET (1969) were designed with resilience and resource sharing in mind, not security. The TCP/IP protocol suite that emerged from this research made deliberate design tradeoffs that prioritized interoperability and open standards over authentication and integrity. Many of today's most common vulnerabilities, IP spoofing, ARP poisoning, DNS cache poisoning, are direct consequences of these original design decisions. Understanding the protocols is therefore inseparable from understanding the threat landscape.
:::

%%%

---
unit: Foundations
code: NET
title: What Is a Network?
---
:::callout style=soft
A **network** is a system of interconnected devices, such as computers, servers, printers, and routers, that communicate using standardized protocols to share data and resources.
:::

::::columns
::col::
:::list heading="Common Network Types" style=plain
- **LAN** (Local Area Network), confined to a small geographic area like a home, office, or campus
- **WAN** (Wide Area Network), spans large geographical regions, often connecting multiple LANs
- **MAN** (Metropolitan Area Network), covers a city or large campus
- **PAN** (Personal Area Network), connects personal devices within a short range (e.g., Bluetooth)
:::
::col::
:::table
| Network Type | Coverage       | Typical Use Case             |
|--------------|----------------|------------------------------|
| LAN          | Single building| Office or home networks      |
| MAN          | City or region | University or city network   |
| WAN          | Country/global | ISP or enterprise backbone   |
| PAN          | Personal space | Smartphone and wearable sync |
:::
:::
::::

:::image src="images/11_network_types_comparison.png" alt="Diagram showing LAN, MAN, WAN, and PAN at different geographic scales with example devices at each level" caption="Network types organized by geographic scope: from personal device pairs (PAN) to global interconnection (WAN/Internet)" width=full
:::

:::notes
At its core, a network is a structured interconnection of computing devices that enables communication and resource sharing through standardized protocols. These protocols, such as TCP/IP (Transmission Control Protocol/Internet Protocol), Ethernet, and HTTP (Hypertext Transfer Protocol), define how data is formatted, addressed, transmitted, routed, and received. The interoperability of devices from different manufacturers and running disparate operating systems is made possible by adherence to these open standards, many of which are maintained by organizations such as the Internet Engineering Task Force (IETF) through RFCs (Request for Comments).

Networks are not only foundational to modern computing but are also central to information security frameworks. For example, NIST Special Publication 800-30 provides guidelines for conducting risk assessments on networked systems, while ISO/IEC 27001 outlines requirements for establishing, implementing, maintaining, and continually improving an information security management system (ISMS) that includes network infrastructure.

Local Area Networks (LANs) are typically confined to a single building or site and often utilize Ethernet or Wi-Fi technologies. They are characterized by high data transfer rates and low latency. In contrast, Wide Area Networks (WANs) connect LANs across cities, countries, or even continents. The Internet is the most prominent example of a WAN, functioning as a decentralized "network of networks" where autonomous systems exchange routing information using protocols such as BGP (Border Gateway Protocol). Misconfigurations or vulnerabilities in BGP can lead to severe security incidents, such as BGP hijacking, where malicious actors reroute Internet traffic through unauthorized nodes.

Understanding network typologies is crucial for cybersecurity professionals. For instance, vulnerabilities like CVE-2021-34527 (PrintNightmare) exploit networked printers commonly found in LANs, allowing attackers to execute remote code and gain unauthorized access. Similarly, insecure WAN configurations can expose organizations to man-in-the-middle attacks or unauthorized surveillance. Historical incidents such as the 2010 Pakistan Telecom BGP hijacking, in which a misconfigured route advertisement briefly redirected a significant portion of YouTube's global traffic through Pakistani infrastructure, demonstrate that WAN-level vulnerabilities have broad, real-world consequences.

Metropolitan Area Networks (MANs) occupy a middle ground, often used by universities, city governments, or large enterprises to connect multiple buildings across an urban area. Personal Area Networks (PANs), though limited in range, are increasingly relevant to enterprise security due to the proliferation of Bluetooth-connected devices; attacks such as BlueBorne (CVE-2017-1000251 through CVE-2017-1000256) exploited Bluetooth protocol vulnerabilities to achieve remote code execution without user interaction.

In enterprise environments, network segmentation is a critical defensive strategy. Frameworks such as NIST SP 800-207 (Zero Trust Architecture) emphasize the principle of "never trust, always verify," advocating for micro-segmentation and strict access controls to limit lateral movement of threats. This conceptual understanding of networks is essential for analyzing attack surfaces, implementing defense-in-depth strategies, and deploying network-based intrusion detection systems (NIDS) that monitor for anomalous traffic patterns.

Ultimately, a strong grasp of network fundamentals, including topologies, protocols, and architectural models, is indispensable for designing secure, resilient, and scalable information systems.
:::

%%%

---
unit: Foundations
code: PKT
title: How Data Travels, Packets
---
:::callout style=soft
Data transmitted over networks is not sent as a continuous stream, but rather segmented into discrete units known as **packets**. These packets are independently routed through the network infrastructure and reassembled at their destination to reconstruct the original message or file.
:::

::::columns
::col::
:::flow
Data
↓
Segmented into packets
↓
Each packet routed independently
↓
Packets arrive at destination
↓
Reassembled into original data
:::
::col::
:::list heading="Key Packet Characteristics" style=plain
- Contain both **header** and **payload**
- Header includes source/destination addresses, sequencing info, error detection codes
- Payload carries the actual user data
- May traverse different paths in the network
- Reordered upon arrival and checked for integrity
:::
::col::
:::table
| Component        | Description                                  |
|------------------|----------------------------------------------|
| Header           | Metadata including addressing and control info |
| Payload          | The actual data being transmitted            |
| Trailer/Footer   | Error-checking data (e.g., CRC)              |
| Size             | Typically 64 bytes to 65,535 bytes            |
:::
::::

:::image src="images/11_packet_structure_anatomy.png" alt="Exploded diagram of an IP packet showing header fields (version, IHL, TTL, source IP, destination IP), payload section, and trailer with CRC checksum, with each field labeled and annotated" caption="Anatomy of an IP packet: the header carries routing metadata, the payload carries application data, and the trailer provides error detection" width=full
:::

:::notes
In modern networking, communication between devices occurs through the exchange of structured data units called **packets**. This packet-based approach underpins nearly all digital communications and is fundamental to the operation of the Internet Protocol (IP) suite, as defined in RFC 791 (IPv4) and RFC 2460 (IPv6). The modular nature of packetization enables efficient use of network resources, supports fault tolerance, and allows for dynamic routing decisions.

When a device sends data, such as an email, a video stream, or a web request, it does not transmit the entire content as a single entity. Instead, the Transmission Control Protocol (TCP), as specified in RFC 793, or User Datagram Protocol (UDP), per RFC 768, segments the data into smaller, manageable packets. Each packet contains two primary components: the **header**, which includes metadata such as source and destination IP addresses, sequence numbers, and protocol-specific flags; and the **payload**, which holds the actual data being sent.

Packets are routed independently across the network, often taking different paths based on current traffic conditions and routing algorithms. This flexibility enhances resilience and efficiency but also introduces challenges such as packet loss, duplication, and reordering. Upon arrival at the destination host, the receiving transport layer reassembles the packets using sequence numbers and validates their integrity using checksums. Consider a large file transferred over TCP: it might be split into thousands of packets, each taking a potentially different path across the internet, and the destination system reassembles them in the correct sequence using the TCP sequence number field, a remarkable feat of distributed coordination performed billions of times per day.

From a security standpoint, the packet is the atom of network forensics. Captured packets (via tools like Wireshark or tcpdump) reveal the exact content, timing, origin, and destination of every exchange. Security professionals performing incident response or threat hunting analyze packet captures (PCAPs) to reconstruct attack timelines, identify exfiltrated data, and understand attacker methodologies. Malicious actors, understanding this visibility, often attempt to blend into normal traffic patterns or exploit fragmentation behaviors, for example, splitting a payload across multiple fragments to evade signature-based inspection engines, a technique documented in various evasion studies and relevant to vulnerabilities like CVE-2021-3587.

The IPv4 header itself contains a wealth of security-relevant fields. The Time-to-Live (TTL) field, decremented at each hop, can reveal the approximate number of hops a packet has traveled and is often used in traceroute-style reconnaissance tools. The Protocol field distinguishes TCP, UDP, and ICMP traffic at the IP layer. The Flags and Fragment Offset fields govern packet fragmentation, which has historically been a rich source of evasion techniques.

This mechanism aligns with principles outlined in NIST Special Publication 800-95, which discusses secure network communications and emphasizes the importance of understanding data flow for implementing effective monitoring and protection strategies. Understanding how packets function is essential for mastering core networking concepts, including Quality of Service (QoS), congestion control, and network security frameworks such as those detailed in ISO/IEC 27033, which addresses network security architecture and controls.
:::

%%%

---
unit: Foundations
code: PRO
title: Protocols, The Rules of Communication
---
:::callout style=soft
A **protocol** is a standardized set of rules and conventions that govern how data is transmitted, formatted, sequenced, and interpreted between devices in a network. These rules ensure interoperability, reliability, and security across heterogeneous systems.
:::

::::columns
::col::
:::list heading="Core Protocol Functions" style=plain
- **Syntax**: Data format and structure
- **Semantics**: Meaning of control information
- **Synchronization**: Timing and sequencing of data exchange
- **Error Handling**: Detection and correction mechanisms
:::
::col::
:::table
| Layer | Protocol | Purpose |
|---|---|---|
| Application | HTTP/HTTPS | Web communication |
| Application | FTP/SFTP | File transfer |
| Application | SMTP/IMAP | Email services |
| Transport | TCP/UDP | End-to-end data delivery |
| Network | IP (IPv4/IPv6) | Addressing and routing |
| Data Link | Ethernet | Local network framing |
| Physical | DSL, Wi-Fi | Transmission media |
:::
::col::
:::list heading="Protocol Design Principles" style=plain
- **Statefulness**: Maintains session context
- **Idempotency**: Repeated operations have same effect
- **Extensibility**: Allows future enhancements
- **Interoperability**: Works across vendors |
:::
::::

:::flow
Application layer generates data (e.g., HTTP request body)
↓
Transport layer adds port numbers and reliability controls → Segment (TCP/UDP)
↓
Network layer adds source and destination IP addresses → Packet (IP datagram)
↓
Data Link layer adds MAC addresses and frame delimiters → Frame (Ethernet)
↓
Physical layer converts frame to bits and transmits on the medium
↓
Receiving host strips each header in reverse order (decapsulation)
:::

:::image src="images/11_protocol_stack_layers.png" alt="Clean technical diagram of the OSI/TCP-IP protocol stack showing protocols at each layer, with arrows showing encapsulation from Application down to Physical layer, professional textbook style with labeled boxes" caption="Protocol stack: each layer adds its own header as data travels downward through the stack (encapsulation), and strips its header as data travels upward (decapsulation)" width=full
:::

:::notes
In computer networking, a **protocol** is a formalized set of rules that defines how data is exchanged between devices. These rules are essential for ensuring that diverse systems, regardless of manufacturer, operating system, or internal architecture, can communicate effectively. Without such standardization, even two devices designed to work together would be unable to interpret each other's signals.

Protocols operate within a layered model, most commonly the **OSI model** (Open Systems Interconnection) or the **TCP/IP model**. Each layer has specific responsibilities and uses its own set of protocols. For example, at the **Application Layer**, protocols like **HTTP** and **HTTPS** manage web traffic; at the **Transport Layer**, **TCP** ensures reliable delivery while **UDP** provides faster but less reliable transmission. At the **Network Layer**, **IP** handles logical addressing and routing, while **Ethernet** operates at the **Data Link Layer** to frame packets for physical transmission.

The design of protocols involves several key principles:
- **Syntax** defines the structure and format of data.
- **Semantics** assigns meaning to the information (e.g., whether it's a request or response).
- **Timing** controls synchronization and sequencing.
- **Error handling** includes checksums, acknowledgments, and retransmission mechanisms.

Standards organizations like the **Internet Engineering Task Force (IETF)** publish **RFCs (Request for Comments)** that define widely used protocols. For instance, **RFC 791** defines IPv4, and **RFC 7230** defines HTTP/1.1. The **National Institute of Standards and Technology (NIST)** also plays a role in securing protocol implementations through guidelines such as those found in **NIST SP 800-53**, which outlines security controls for federal information systems.

Security vulnerabilities often arise from improper implementation or misuse of protocols. For example, **CVE-2014-0160 (Heartbleed)** was a flaw in the **TLS/SSL** protocol implementation, specifically in the heartbeat extension, that allowed attackers to read up to 64 kilobytes of server memory per request, exposing private keys, session tokens, and user passwords. The vulnerability existed not in the protocol specification itself but in the OpenSSL library's implementation of it, illustrating the critical distinction between a protocol specification and its real-world implementation. Similarly, **CVE-2009-3555** targeted the TLS renegotiation process, allowing an attacker to inject plaintext into an encrypted connection. These historical examples emphasize that understanding both the design of protocols and the common failure modes of their implementations is essential for modern security practitioners.

A useful mental model is to think of protocols as legal contracts between communicating parties. Both parties agree in advance on the language, format, and sequence of their exchange. When one party deviates from the contract, whether due to a bug, misconfiguration, or deliberate manipulation, the result can range from a dropped connection to a full remote compromise. Defending networked systems thus requires not only knowing what protocols are supposed to do, but recognizing when they are being abused.

Understanding protocols deeply allows security professionals to detect and mitigate such risks effectively, perform traffic analysis, write detection signatures, and reason about the attack surface of any networked application.
:::

%%%

---
unit: Models
code: TCP
title: The TCP/IP Model
---
::::columns
::col::
:::table
| Layer | Role | Protocols & Functions |
|---|---|---|
| Application | Provides network services to user applications | HTTP, HTTPS, SMTP, FTP, DNS, TLS |
| Transport | Ensures reliable or fast delivery between endpoints | TCP (reliable), UDP (fast, no guarantee) |
| Internet | Logical addressing and routing across networks | IP (IPv4/IPv6), ICMP, IGMP |
| Network Access | Physical transmission over local network media | Ethernet, Wi-Fi, ARP, MAC framing |
:::
::col::
:::callout
Each layer encapsulates data from the layer above, adding its own header. This process is called **encapsulation**.
:::
::::

:::steps
1. **Application Layer**, Browser or application generates an HTTP/HTTPS request. Data is still called *data* at this stage.
2. **Transport Layer**, TCP adds a header containing source port, destination port (e.g., 443), sequence number, and checksum. The unit is now called a *segment*.
3. **Internet Layer**, IP adds a header with source and destination IP addresses, TTL, and protocol identifier. The unit is now a *packet* (or datagram).
4. **Network Access Layer**, Ethernet (or Wi-Fi) wraps the packet in a *frame*, prepending the source and destination MAC addresses and appending a CRC checksum for error detection.
5. **Physical Transmission**, The frame is converted to electrical, optical, or radio signals and sent across the medium to the next hop.
6. **Decapsulation at Destination**, Each receiving layer strips its own header, passing the inner payload upward until the original application data is reassembled.
:::

:::image src="images/11_tcpip_model_encapsulation.png" alt="Side-by-side comparison of the OSI 7-layer model and TCP/IP 4-layer model, with encapsulation arrows showing how data unit changes from data to segment to packet to frame, clean technical textbook style, white background" caption="The TCP/IP model maps to the OSI model: data is encapsulated at each layer, becoming a segment (Transport), then a packet (Internet), then a frame (Network Access)" width=full
:::

:::notes
The TCP/IP model is a foundational conceptual framework that describes how data is transmitted across interconnected networks. It serves as the core architecture of the modern Internet and underpins virtually all network communication today. Unlike the OSI model, which has seven layers, the TCP/IP model is composed of four layers, each with clearly defined responsibilities.

At the top is the **Application Layer**, which directly interfaces with end-user software and implements high-level protocols such as HTTP, HTTPS, SMTP, and FTP. This layer consolidates the functions of the OSI model's Session, Presentation, and Application Layers. For example, TLS operates at this layer to provide encryption and secure communication for protocols like HTTPS. The Application Layer is where the most user-visible attacks occur, SQL injection, cross-site scripting, and credential phishing all target Application Layer protocols or the applications that implement them.

Beneath it lies the **Transport Layer**, primarily implemented by either Transmission Control Protocol (TCP) or User Datagram Protocol (UDP). TCP ensures reliable, ordered delivery through mechanisms like sequence numbers, acknowledgments, and retransmission, making it suitable for applications such as web browsing or file transfer. In contrast, UDP offers faster but connectionless delivery without guarantees, ideal for real-time applications like VoIP or streaming. The Transport Layer introduces the concept of the **port number**, which multiplexes multiple application streams over a single IP address, a concept we explore in detail in the Ports slide.

The third layer, the **Internet Layer**, is governed by the Internet Protocol (IP), which handles logical addressing (via IP addresses) and routing packets across diverse networks. IPv4 and IPv6 are the two versions currently in use, with IPv6 addressing the limitations of address space exhaustion. Protocols like ICMP (used for diagnostics such as ping) and IGMP (used for multicast group management) also operate at this layer. IP routing is what makes the internet scale: by making each router responsible only for finding the next hop rather than the full path, IP distributes routing intelligence across thousands of independent systems.

Finally, the **Network Access Layer** (also called the Link or Network Interface Layer) deals with the physical transmission of data over network hardware, including Ethernet, Wi-Fi, and other local network technologies. It encapsulates IP packets into frames and manages access to the physical medium using protocols like ARP (Address Resolution Protocol) for mapping IP addresses to MAC addresses. ARP's lack of authentication is exploited in ARP spoofing attacks, covered in Class 12.

Each layer in the TCP/IP stack encapsulates the data from the layer above, adding its own header (and sometimes trailer), forming a packet structure known as encapsulation. As data moves down the stack, each layer treats the entire payload from the layer above as opaque data, ensuring modularity and abstraction. This modularity is both the stack's greatest strength and one of its persistent security challenges: each layer trusts data from the layers above and below without cryptographically verifying its source or integrity.

This layered architecture promotes interoperability, scalability, and fault isolation. For example, changes in the physical medium (e.g., switching from Ethernet to Wi-Fi) do not require modifications to higher-layer protocols. Similarly, security vulnerabilities can often be isolated to a specific layer, for instance, CVE-2021-3449 (a TLS vulnerability) affects the Application Layer, while CVE-2021-27065 (related to TCP/IP stack processing) impacts the Internet or Transport Layers.

Frameworks such as NIST SP 800-53 emphasize the importance of layered defense strategies, aligning with the modular nature of the TCP/IP model. Understanding these layers is essential for diagnosing network issues, designing secure systems, and implementing effective monitoring and mitigation techniques.
:::

%%%

---
unit: Addressing
code: IPV
title: IP Addressing
---
:::callout style=soft
An **IP address** uniquely identifies a device on a network, the way a street address identifies a building.
:::

::::columns
::col::
:::list heading="Public vs Private Addresses" style=plain
- **Public IP**, Globally routable on the internet (assigned by IANA/RIRs)
- **Private IP**, Reserved for internal use (RFC 1918); not routable on the internet
- **NAT**, Enables translation between private and public addresses
:::
::col::
:::table
| Class     | Private Range         | Subnet Mask    |
|-----------|------------------------|----------------|
| Class A   | 10.0.0.0 – 10.255.255.255 | 255.0.0.0     |
| Class B   | 172.16.0.0 – 172.31.255.255 | 255.240.0.0  |
| Class C   | 192.168.0.0 – 192.168.255.255 | 255.255.0.0 |
:::
:::code language=bash caption="Viewing local IP configuration on Linux (ip addr show)"
# ip addr show, Lists all network interfaces (e.g., eth0, lo, wlan0) with their
# assigned IPv4 and IPv6 addresses, subnet masks, and interface states (UP/DOWN).
# The output also shows MAC (hardware) addresses at the link layer.
# This is the modern replacement for the deprecated 'ifconfig' command.
ip addr show
:::
:::code language=bash caption="Querying your public IP via the CLI (curl ifconfig.me)"
# curl, A command-line tool for transferring data using URLs.
# ifconfig.me, A public web service that reflects the caller's IP address back as plain text.
# When this command runs, the packet leaving your machine carries your PRIVATE IP as source.
# Your router's NAT function replaces that with the PUBLIC IP before the packet hits the internet.
# The ifconfig.me server sees only the public IP and returns it as the response body.
curl ifconfig.me
:::
::col::
:::flow
st=>start: Device sends packet
nat=>operation: NAT translates src IP
pub=>end: Packet routed on internet

st->nat->pub
:::
::::

:::image src="images/11_nat_private_public_ip.png" alt="Diagram showing a home or office network with multiple devices using private 192.168.x.x addresses, connecting through a NAT router that holds a single public IP, with arrows showing private-to-public translation for outbound traffic" caption="NAT allows many devices sharing private RFC 1918 addresses to communicate on the internet through a single public IP address" width=full
:::

:::notes
An Internet Protocol (IP) address is a numerical identifier assigned to devices participating in a network that uses the Internet Protocol for communication. It enables accurate routing of data packets between source and destination nodes across interconnected networks. Analogous to a physical mailing address, an IP address ensures that data reaches the correct recipient in a timely and secure manner.

IP addresses are fundamentally categorized into two scopes: public and private. Public IP addresses are globally unique and routable on the internet. They are assigned by the Internet Assigned Numbers Authority (IANA) and distributed through Regional Internet Registries (RIRs), such as ARIN (North America), RIPE NCC (Europe), and APNIC (Asia-Pacific). These addresses must be globally unique to ensure proper end-to-end communication and are typically used by servers, routers, and other internet-facing infrastructure.

In contrast, private IP addresses are reserved for internal network use and are defined in RFC 1918. These addresses are non-routable on the public internet and include the following ranges:
- Class A: 10.0.0.0 to 10.255.255.255 (supports ~16.7 million host addresses per network)
- Class B: 172.16.0.0 to 172.31.255.255 (supports ~1 million host addresses across 16 networks)
- Class C: 192.168.0.0 to 192.168.255.255 (supports 256 addresses per /24 network, 256 such networks)

Private addressing conserves the limited IPv4 address space and enhances security by isolating internal networks from direct exposure to the internet. However, this isolation necessitates a translation mechanism to enable communication with external networks.

Network Address Translation (NAT), standardized under RFC 3022, bridges this gap by modifying IP header information, typically replacing the source IP address of outgoing packets with the router's public IP. This allows multiple internal hosts to share a single public IP address, a critical strategy in mitigating IPv4 address exhaustion. NAT also provides a basic layer of obfuscation, as internal addresses are not directly exposed to the internet. However, NAT is not a security control, it is an address translation mechanism. Attackers who gain an internal foothold are not impeded by NAT, and NAT provides no authentication or encryption guarantees.

IPv6, defined in RFC 8200, provides a vastly larger address space (2^128 addresses) and eliminates the need for NAT in most cases, allowing every device to have a globally unique, publicly routable address. IPv6 also introduces Secure Neighbor Discovery (SEND, RFC 3971), which provides cryptographic authentication for the neighbor discovery process, addressing the ARP spoofing vulnerabilities inherent in IPv4. Despite its advantages, IPv6 adoption has been gradual, and dual-stack environments (running both IPv4 and IPv6 simultaneously) introduce their own complexity and potential security gaps.

From a cybersecurity perspective, improper NAT configurations or lack of proper ingress filtering can lead to vulnerabilities such as NAT traversal attacks or unauthorized access, as noted in CVE entries like CVE-2019-11043. Understanding IP addressing fundamentals is essential for implementing secure network architectures in alignment with frameworks such as NIST SP 800-53 and ISO/IEC 27001. Subnetting, the division of a large network into smaller subnetworks using subnet masks and CIDR notation, is a prerequisite for network segmentation, which is covered in Class 15.
:::

%%%

---
unit: Ports
code: PRT
title: Ports
---
:::callout style=soft
A **port** is a 16-bit numerical identifier used in network communications to direct traffic to the correct process or service running on a device. Think of the IP address as the street address of a building, the port number is like the apartment number, specifying exactly which service should handle the incoming data.
:::

::::columns
::col::
:::table
| Port | Service | Protocol | Description |
|---|---|---|---|
| 20/21 | FTP | TCP | File Transfer Protocol (control and data) |
| 22 | SSH | TCP | Secure Shell for encrypted remote login |
| 23 | Telnet | TCP | Unencrypted remote login (deprecated) |
| 25 | SMTP | TCP | Simple Mail Transfer Protocol for sending email |
| 53 | DNS | UDP/TCP | Domain Name System for resolving hostnames |
| 80 | HTTP | TCP | Hypertext Transfer Protocol (unsecured web) |
| 110 | POP3 | TCP | Post Office Protocol v3 for email retrieval |
| 143 | IMAP | TCP | Internet Message Access Protocol for email |
| 443 | HTTPS | TCP | HTTP over TLS/SSL (secure web traffic) |
| 993 | IMAPS | TCP | IMAP over SSL |
| 995 | POP3S | TCP | POP3 over SSL |
:::
::col::
:::text
### Port Categories

Ports are divided into three ranges based on IANA (Internet Assigned Numbers Authority) standards:

- **Well-Known Ports (0–1023)**  
  Reserved for system or core services (e.g., HTTP on 80, HTTPS on 443).  
  Managed by IANA; require administrative privileges to bind.

- **Registered Ports (1024–49151)**  
  Assigned to user processes or applications by IANA upon request.

- **Dynamic/Private Ports (49152–65535)**  
  Used temporarily by clients for outgoing connections (ephemeral ports).
:::

:::callout style=line
**Security Note:**  
Unnecessary open ports increase the attack surface of a system. For example, leaving Telnet (port 23) open exposes credentials in plaintext, as highlighted in CVE-2000-0268 and others. Always follow NIST SP 800-53 guidelines on minimizing open services and applying network segmentation.
:::
::::

:::image src="images/11_well_known_ports_chart.png" alt="Visual reference chart showing well-known TCP and UDP port numbers from 0-1023 grouped by category (web, email, remote access, file transfer, DNS), with icons for each service and color-coded security risk levels" caption="Well-known port reference: ports 0–1023 are reserved for core internet services and require administrative privileges to bind on most operating systems" width=full
:::

:::notes
In network communication, an IP address alone is insufficient to deliver data to the correct application. A **port** serves as a secondary addressing mechanism that allows a device to differentiate between multiple services or processes running concurrently. This concept is foundational to the **TCP/IP model**, particularly at the transport layer, where protocols like TCP and UDP use port numbers to multiplex and demultiplex traffic.

Each port is a 16-bit integer, allowing for a theoretical maximum of 65,536 ports per IP address (0 through 65535). These are categorized by IANA into well-known, registered, and dynamic/private ports. Well-known ports (0–1023) are reserved for standard services such as HTTP (80), HTTPS (443), SSH (22), and DNS (53). These assignments are standardized to ensure interoperability across global networks. The binding of any service to a well-known port typically requires administrative (root) privileges on UNIX/Linux systems, providing a modest level of protection against unauthorized service impersonation.

The combination of an IP address and a port number forms a **socket**, the fundamental endpoint of a network connection. A TCP connection is uniquely identified by a 4-tuple: (source IP, source port, destination IP, destination port). This 4-tuple is what allows a single server at one IP address to simultaneously serve thousands of clients on the same port (e.g., 443 for HTTPS), because each client connects from a different source port.

From a cybersecurity standpoint, understanding port usage is crucial for both defensive and offensive operations. Open ports are potential entry points for attackers, as seen in vulnerabilities like CVE-2017-11882, which exploited open SMB ports (445) in WannaCry ransomware attacks that caused billions of dollars in global damage in 2017. The NIST Cybersecurity Framework (CSF) and ISO/IEC 27001 both emphasize the importance of network monitoring and port management as part of a defense-in-depth strategy.

Port scanning, performed by tools such as Nmap (Network Mapper), is a standard technique in both penetration testing and attacker reconnaissance. By sending packets to various ports and analyzing responses, an attacker can determine which services are running, infer the operating system type, and identify potentially vulnerable service versions. This reconnaissance step (mapped to MITRE ATT&CK T1046 – Network Service Scanning) directly precedes exploitation and underscores why minimizing the attack surface through port management is so important.

In practice, firewalls and intrusion detection systems (IDS) often filter traffic based on port numbers. For example, blocking outbound traffic on port 25 can mitigate spam relay attacks. Similarly, restricting access to administrative ports like SSH (22) or RDP (3389) to trusted IP ranges is a common hardening technique recommended by both NIST and CIS Controls. The CIS Benchmarks for operating systems and network devices include explicit guidance on disabling unused services and closing unnecessary ports, directly reducing the attack surface available to adversaries.

Ephemeral ports (49152–65535) deserve particular attention: these are the source ports assigned dynamically by the operating system to outgoing client connections. They are short-lived and are released when the connection closes. Monitoring ephemeral port usage can reveal unusual outbound connection patterns indicative of malware command-and-control (C2) communication or data exfiltration.
:::

%%%

---
unit: Delivery
code: TUD
title: TCP vs UDP
---
::::columns
::col::
:::table
| Feature         | TCP                                 | UDP                              |
|----------------|--------------------------------------|----------------------------------|
| **Connection**  | Connection-oriented                  | Connectionless                   |
| **Reliability** | Guaranteed delivery, ordered data    | No guarantees                    |
| **Overhead**    | High (ACKs, retransmissions, flow control) | Low                        |
| **Use Cases**   | Web browsing, email, file transfers  | Live video, VoIP, online gaming  |
:::
::col::
:::callout
**Key Takeaway:**  
The choice between TCP and UDP depends on the application's tolerance for data loss versus its sensitivity to latency.
:::
::::

:::flow
Client sends SYN
↓
Server responds with SYN-ACK
↓
Client sends ACK (connection established)
↓
Data transfer begins
↓
FIN/FIN-ACK exchange (connection teardown)
:::

:::image src="images/11_tcp_three_way_handshake.png" alt="Sequence diagram showing the TCP three-way handshake (SYN, SYN-ACK, ACK) between client and server, followed by data exchange and four-way teardown (FIN, FIN-ACK, FIN, FIN-ACK), labeled with sequence numbers, clean technical style" caption="TCP's three-way handshake establishes a reliable connection before any data is exchanged, each step is a vector for attacks like SYN flooding" width=full
:::

:::notes
At the transport layer of the Internet Protocol Suite, two dominant protocols govern how data is transmitted between hosts: Transmission Control Protocol (TCP) and User Datagram Protocol (UDP). These protocols differ fundamentally in their design philosophy and operational characteristics, making them suitable for distinct types of network communication.

TCP, defined in RFC 793, is a connection-oriented protocol that ensures reliable, ordered, and error-checked delivery of data between applications. Before any application data is exchanged, TCP establishes a logical connection through a three-way handshake (SYN, SYN-ACK, ACK). This process synchronizes sequence numbers and confirms that both endpoints are ready to communicate. Once established, TCP uses sequence numbers and acknowledgments (ACKs) to track and confirm receipt of each segment. If an acknowledgment is not received within a timeout period, TCP automatically retransmits the segment. Additionally, TCP implements flow control via sliding window mechanisms and congestion control algorithms such as slow start, congestion avoidance, fast retransmit, and fast recovery, which are essential for maintaining network stability under varying load conditions.

In contrast, UDP, as defined in RFC 768, is a lightweight, connectionless protocol that offers minimal overhead and maximum speed. It does not establish a connection before sending data, nor does it guarantee delivery, ordering, or error correction. Each UDP datagram is sent independently, with only 8 bytes of header information (compared to TCP's minimum 20-byte header). This makes UDP ideal for real-time applications where low latency is more critical than reliability, such as Voice over IP (VoIP), live video streaming, and online gaming. In these scenarios, minor packet loss is acceptable if it avoids the delays associated with retransmission and acknowledgment. DNS primarily uses UDP (port 53) for its query-response pattern, where a single short exchange is faster than establishing a full TCP connection.

From a cybersecurity perspective, both protocols present unique attack vectors. TCP is vulnerable to resource exhaustion attacks such as SYN flooding (CVE-1999-0569), where an attacker sends a high volume of SYN requests without completing the handshake, filling the server's connection table with half-open connections until it can accept no new legitimate connections. Modern SYN flood mitigation techniques include SYN cookies (RFC 4987), which allow servers to avoid storing state for incomplete connections, and rate limiting at the firewall level. UDP, due to its stateless nature and lack of built-in rate limiting, is often exploited in amplification attacks, such as DNS amplification (CVE-2013-2566) and NTP amplification, where attackers spoof source addresses and send queries to open UDP services, resulting in large responses being directed to victims, achieving traffic multiplication factors of 50x or more.

TCP session hijacking represents a further attack class: if an attacker can predict or observe the sequence numbers of an active TCP connection, they can inject forged segments that are accepted as legitimate by one or both parties. Historical implementations with weak sequence number randomization were particularly susceptible, as documented in CVE-1999-0016. Modern operating systems implement cryptographically random initial sequence numbers (ISN) to mitigate this risk.

Understanding the operational differences between TCP and UDP is crucial for secure network design. Frameworks like NIST SP 800-53 emphasize the importance of protocol selection based on mission requirements, performance needs, and risk tolerance. Proper configuration and monitoring of these protocols are essential to ensure both functionality and resilience against common network-based threats.
:::

%%%

---
unit: Models
code: CSM
title: Communication Models
---
::::columns
::col::
:::table
| Model         | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| Client-server | Clients initiate requests to a centralized server, which processes and responds. |
| Peer-to-peer  | Nodes communicate directly without a central authority; each acts as both client and server. |
:::
::col::
:::callout
**Key Differentiator**: In client-server, communication is **asymmetric** and **centralized**, whereas peer-to-peer is **decentralized** and **symmetrical**.
:::
::::

:::list heading="Client-Server Characteristics" style=plain
- Centralized control and management
- Scalable with proper infrastructure
- Single point of failure (the server)
- Common in enterprise and web services (HTTP, SMTP, DNS)
- Supports authentication, authorization, and auditing (AAA)
- Aligns with **NIST SP 800-53** security controls and **ISO/IEC 27001** ISMS
:::

:::list heading="Peer-to-Peer Characteristics" style=plain
- Decentralized and distributed architecture
- Nodes share resources directly
- No single point of failure
- Used in file-sharing (BitTorrent), VoIP (Skype), and blockchain networks
- Challenging to monitor and secure
- Vulnerable to abuse in malware propagation and data exfiltration
:::

:::callout style=soft
**Security Implication**: Client-server architectures centralize risk, compromising the server (e.g., via **CVE-2021-44228**, Log4Shell) can yield broad access. P2P systems, while resilient, are harder to monitor and more prone to abuse in threat models defined by **MITRE ATT&CK**, especially under techniques like **T1071** (Application Layer Protocol) and **T1571** (Non-Standard Port).
:::

:::flow
Client constructs request (e.g., HTTP GET /resource)
↓
Request is authenticated (credentials, API key, or session token verified)
↓
Server authorizes the request (checks permissions for the resource)
↓
Server processes request and generates response
↓
Response is sent back to client over the established connection
↓
Client renders or consumes the response
↓
Session may be maintained (stateful) or terminated (stateless/REST)
:::

:::image src="images/11_client_server_vs_p2p.png" alt="Side-by-side architectural diagrams: left shows client-server model with multiple clients connecting to a central server, right shows peer-to-peer mesh where all nodes connect to each other directly, with security annotations on each" caption="Client-server centralizes control (and risk); peer-to-peer distributes both, each model has distinct security implications for defenders" width=full
:::

:::notes
Communication models define the structural and logical framework by which devices in a network interact. These models are foundational to both network design and cybersecurity strategy, as they determine where control, trust, and potential vulnerabilities lie.

The **client-server model** is the dominant paradigm in enterprise and internet-based systems. In this model, clients, such as web browsers, email clients, or mobile apps, initiate requests to a centralized server, which processes those requests and returns responses. This architecture supports centralized management, access control, and auditing, making it ideal for regulated environments governed by standards such as **NIST SP 800-53**, which outlines security controls for federal information systems, and **ISO/IEC 27001**, which provides a framework for managing information security through a systematic ISMS (Information Security Management System). Protocols such as HTTP, HTTPS, SMTP, and DNS operate under this model. However, the centralization introduces a **single point of failure**: if the server is compromised or becomes unavailable, the entire service may be disrupted. For instance, vulnerabilities like **CVE-2021-44228** (Log4Shell) in server-side logging libraries can allow remote code execution, granting attackers broad access to backend systems and affecting any client that communicates with that server.

The client-server model also centralizes the **attack target**: threat actors focus on compromising the server because doing so yields access to data and sessions belonging to all clients simultaneously. High-profile breaches such as the 2013 Adobe breach (153 million user records) and the 2017 Equifax breach (147 million records) both exploited server-side vulnerabilities in client-server architectures. This is why server hardening, patch management, and runtime application self-protection (RASP) are critical defensive priorities in client-server environments.

In contrast, the **peer-to-peer (P2P)** model enables direct communication between nodes without a central server. Each node acts as both a client and a server, sharing resources such as files, processing power, or bandwidth. This decentralized architecture avoids single points of failure and reduces infrastructure costs, making it resilient to server outages. P2P is widely used in applications like BitTorrent for file sharing, Skype for VoIP, and blockchain networks like Bitcoin. However, the lack of centralized control introduces significant challenges in monitoring, securing, and governing data flows. These systems are often exploited in threat models defined by **MITRE ATT&CK**, particularly under techniques like **T1071** (Application Layer Protocol), where adversaries use common protocols to avoid detection, and **T1571** (Non-Standard Port), which involves using unconventional ports to bypass firewall rules. The distributed nature of P2P also complicates compliance with regulatory frameworks like **ISO/IEC 27001**, which require centralized audit trails and access control mechanisms. Malware families such as Conficker and ZeroAccess used P2P protocols for command-and-control communication precisely because P2P traffic is difficult to distinguish from legitimate use and difficult to block without impacting legitimate applications.

From a cybersecurity perspective, the choice between client-server and P2P architectures directly impacts risk exposure, monitoring capabilities, and incident response strategies. Client-server models centralize risk but also centralize control, making them more amenable to traditional security controls. P2P models distribute risk but also distribute responsibility, complicating threat detection and mitigation.
:::

%%%

---
unit: Synthesis
code: REQ
title: A Web Request's Journey
---
:::steps
1. **User Action**  
   You type a website address (e.g., `https://www.example.com`) into your browser.

2. **DNS Resolution**  
   The browser initiates a DNS query to resolve the domain name into an IPv4 or IPv6 address.

3. **Packet Formation**  
   The HTTP/HTTPS request is encapsulated into TCP segments, then into IP packets, and finally into Ethernet frames for transmission.

4. **Port Addressing**  
   Packets are addressed to destination port 443 (HTTPS) and source port assigned dynamically by the OS.

5. **Routing Across Networks**  
   Packets traverse multiple routers using IP routing tables, following the most efficient path based on routing protocols like OSPF or BGP.

6. **Server Processing**  
   The destination server receives the packets, reassembles them, and processes the HTTPS request using TLS decryption and HTTP parsing.

7. **Response Return**  
   The server sends the response (HTML, CSS, JS, etc.) back through the same layered protocol stack, routed in reverse.
:::

::::columns
::col::
:::callout
**Protocols in Action**
- **Application Layer**: HTTP/HTTPS
- **Transport Layer**: TCP
- **Network Layer**: IP (IPv4/IPv6)
- **Data Link & Physical Layers**: Ethernet, Wi-Fi
:::
::col::
:::callout
**Security Considerations**
- DNS queries may be spoofed (see CVE-2008-1447)
- TLS 1.3 (RFC 8446) secures data in transit
- Firewalls and IDS inspect traffic at multiple layers
:::
::col::
:::callout
**Standards References**
- **NIST SP 800-53**: Network Security Controls
- **ISO/IEC 27001**: Information Security Management
- **RFC 1035**: DNS Specification
- **RFC 791**: Internet Protocol
:::
::::

:::image src="images/11_web_request_journey.png" alt="Step-by-step timeline diagram tracing a single HTTPS web request from the browser through DNS resolution, TCP handshake, TLS negotiation, HTTP GET, server response, and back to the browser, with protocol labels at each step and security checkpoints annotated" caption="A single browser request involves at least four distinct protocols (DNS, TCP, TLS, HTTP) and traverses multiple network layers, each step is a potential security checkpoint or attack surface" width=full
:::

:::notes
This sequence represents a canonical example of network communication, integrating foundational concepts from across the OSI and TCP/IP models. When a user enters a Uniform Resource Locator (URL) into a browser, the system begins a complex, layered interaction governed by well-defined protocols and standards.

The process begins with **DNS resolution**, a critical service defined in RFC 1035, which translates human-readable domain names into machine-usable IP addresses. This lookup may traverse multiple DNS servers, resolver, root, TLD, and authoritative, and is vulnerable to attacks such as cache poisoning (e.g., CVE-2008-1447). DNS operates primarily over UDP port 53, though modern implementations may use TCP for larger responses or secure extensions like DNSSEC (DNS Security Extensions, RFC 4033–4035), which add cryptographic signatures to DNS records to detect tampering. DNS-over-HTTPS (DoH, RFC 8484) and DNS-over-TLS (DoT, RFC 7858) are emerging standards that encrypt DNS queries, preventing eavesdropping on which domains a user is resolving, information that has historically been available to any network observer.

Once the IP address is resolved, the browser initiates a TCP connection using the three-way handshake (SYN → SYN-ACK → ACK), followed immediately by the **TLS handshake** which negotiates the cryptographic parameters for the session. TLS 1.3 (RFC 8446) streamlines this to a single round-trip, significantly reducing connection latency compared to earlier TLS versions while also removing support for legacy cryptographic algorithms. The secure connection thus established ensures confidentiality (encryption), integrity (HMAC), and authenticity (certificate validation against a trusted certificate authority).

The browser then sends the HTTP/HTTPS request, which is segmented into **TCP packets** for reliable delivery, encapsulated in **IP datagrams**, and further wrapped in **Ethernet frames** for physical transmission. This encapsulation reflects the **TCP/IP model's layering**, where each layer adds its own header for addressing and control. The encapsulation order follows a strict hierarchy: Application → Transport → Network → Data Link → Physical.

Packets are routed through the internet using **IP routing protocols**, such as OSPF or BGP, which determine the optimal path based on metrics like hop count or latency. At each hop, routers inspect the IP header to forward the packet closer to its destination. Intermediate devices such as firewalls inspect both IP headers and, in some configurations, higher-layer content. Content Delivery Networks (CDNs) may intercept requests at geographically proximate edge nodes, reducing latency and providing DDoS mitigation.

Upon arrival, the server reassembles the TCP stream, decrypts the **TLS-encrypted** payload (as per RFC 8446 for TLS 1.3), and processes the HTTP request. The response follows the reverse path, retracing the same encapsulation and routing steps, to deliver content back to the browser.

This entire journey exemplifies the interplay of protocols, addressing schemes, and security mechanisms that underpin modern networked systems. It also highlights the relevance of standards such as **NIST SP 800-53**, which outlines controls for securing network communications, and **ISO/IEC 27001**, which governs information security management practices. These frameworks emphasize the importance of layered defense, secure configuration, and continuous monitoring to protect against evolving threats.
:::

%%%

---
unit: Addressing
code: DNS
title: DNS, The Internet's Phone Book
---
:::callout style=soft
The **Domain Name System (DNS)** translates human-readable domain names (e.g., `www.example.com`) into machine-readable IP addresses (e.g., `93.184.216.34`). Without DNS, users would need to memorize numeric addresses for every website they visit.
:::

::::columns
::col::
:::steps
1. Browser checks local cache, if cached, resolution is complete.
2. Query sent to **Recursive Resolver** (usually provided by ISP or configured manually, e.g., 8.8.8.8).
3. Recursive resolver queries **Root Name Server**, returns referral to TLD server.
4. Resolver queries **TLD Name Server** (e.g..com), returns referral to authoritative server.
5. Resolver queries **Authoritative Name Server**, returns the actual IP address.
6. Answer is cached by the resolver and returned to the client.
:::
::col::
:::table
| Record Type | Purpose | Example |
|---|---|---|
| A | Maps hostname to IPv4 address | example.com → 93.184.216.34 |
| AAAA | Maps hostname to IPv6 address | example.com → 2606:2800::1 |
| CNAME | Alias from one name to another | www → example.com |
| MX | Mail exchange server | example.com → mail.example.com |
| TXT | Arbitrary text (SPF, DKIM) | v=spf1 include:... |
| NS | Authoritative name servers | example.com → ns1.example.com |
| PTR | Reverse DNS lookup | 34.216.184.93.in-addr.arpa → example.com |
:::
::::

:::callout style=line
**Attack: DNS Cache Poisoning**, Attackers inject forged DNS responses into a resolver's cache, redirecting users to malicious servers. CVE-2008-1447 (the "Kaminsky Bug") exposed this at scale; DNSSEC (RFC 4033) was widely adopted as a countermeasure.
:::

:::code language=mermaid caption="DNS resolution involves up to four distinct server types; each hop is a potential target for cache poisoning or man-in-the-middle interception"
sequenceDiagram
  participant B as Browser
  participant R as Recursive resolver
  participant Root as Root server
  participant T as .com TLD server
  participant A as Authoritative server
  B->>R: www.example.com?
  R->>Root: www.example.com?
  Root-->>R: Ask the .com servers
  R->>T: www.example.com?
  T-->>R: Ask example.com's name servers
  R->>A: www.example.com?
  A-->>R: 93.184.216.34, TTL 3600
  R-->>B: 93.184.216.34 (cached for the TTL)
  Note over R: Cache poisoning targets this step
:::

:::notes
The Domain Name System (DNS) is one of the most critical and most frequently targeted components of internet infrastructure. Defined in RFC 1034 and RFC 1035 (1987), DNS is a hierarchical, distributed database that maps human-readable hostnames to IP addresses. Its hierarchical structure consists of root servers (13 logical root server clusters), top-level domain (TLD) servers (such as .com.org.gov), and authoritative name servers maintained by individual domain owners. A global network of recursive resolvers (also called caching resolvers) sits between clients and this hierarchy, handling the multi-step lookup process on the client's behalf and caching results to improve efficiency.

DNS operates primarily over UDP port 53 for queries and responses under 512 bytes, and switches to TCP port 53 for larger responses (such as zone transfers) or when reliability is required. Modern implementations also support DNS-over-HTTPS (DoH, RFC 8484) and DNS-over-TLS (DoT, RFC 7858), which encrypt DNS traffic to prevent eavesdropping on which domains a client is querying, information that is highly sensitive from a privacy and threat-intelligence standpoint.

From a security perspective, DNS is a rich attack surface. The most famous attack is **DNS cache poisoning**, where an attacker injects a forged DNS response into a resolver's cache, causing all clients who query that resolver to be directed to a malicious IP address. Dan Kaminsky's 2008 discovery (CVE-2008-1447) demonstrated that the classic DNS protocol's use of predictable transaction IDs and source ports made cache poisoning trivially feasible at scale, affecting virtually every recursive resolver on the internet simultaneously. The industry response was to randomize both the source port and transaction ID (source port randomization), dramatically increasing the work required for a successful attack. DNSSEC (DNS Security Extensions, RFC 4033–4035) provides a more permanent solution by adding cryptographic signatures to DNS records, allowing resolvers to verify that records are authentic and have not been tampered with in transit.

DNS is also heavily abused for **data exfiltration** and **command-and-control (C2)** communication by malware. Because DNS traffic is almost universally permitted through firewalls (blocking it would break internet functionality), attackers encode data in DNS query and response fields, a technique known as DNS tunneling. Tools like dnscat2 and iodine demonstrate this capability. Detection requires analyzing DNS query frequency, subdomain length distributions, and entropy patterns, behavioral analytics rather than simple blocklisting.

**DNS hijacking** (MITRE ATT&CK T1584.002) occurs when attackers gain control of DNS records, either through compromising domain registrar accounts or via BGP-level manipulation, to redirect traffic. The 2019 Sea Turtle campaign targeted registrars and DNS providers across the Middle East and North Africa, redirecting traffic from government and military domains to attacker-controlled infrastructure for credential harvesting. NIST SP 800-81-2 provides guidance on securing DNS infrastructure, recommending DNSSEC deployment, split-horizon DNS configurations, and strict access controls on zone management interfaces.

A DNS response contains an answer section, an authority section and a time-to-live (TTL). When the TTL expires the record must be fetched again; very low TTLs are used by fast-flux malware infrastructure to rotate addresses faster than blocklists can keep up.
:::

%%%

---
unit: Addressing
code: ARP
title: ARP, Mapping IP Addresses to MAC Addresses
---
:::callout style=soft
The **Address Resolution Protocol (ARP)** is used within a local network segment to discover the MAC (hardware) address associated with a known IP address. Without ARP, devices on the same LAN could not deliver Ethernet frames to each other even if they knew the destination IP address.
:::

::::columns
::col::
:::flow
Device A wants to reach 192.168.1.10
↓
Checks ARP cache, not found
↓
Broadcasts ARP Request: "Who has 192.168.1.10?"
↓
Device B (192.168.1.10) sends unicast ARP Reply with its MAC address
↓
Device A stores the mapping in its ARP cache
↓
Ethernet frame sent directly to Device B's MAC
:::
::col::
:::table
| ARP Cache Entry | Type | Description |
|---|---|---|
| Dynamic | Auto-learned | Expires after timeout (typically 2–20 min) |
| Static | Manually configured | Permanent; used to prevent ARP spoofing |
:::

:::callout style=line
**ARP Spoofing Attack:** A malicious host sends unsolicited ARP replies associating its own MAC with a legitimate IP (e.g., the default gateway), poisoning other hosts' ARP caches and enabling man-in-the-middle interception of all their traffic.
:::
::::

:::code language=mermaid caption="ARP has no authentication, any host can claim any IP address, making ARP spoofing one of the oldest and most reliable LAN-layer attacks"
flowchart TB
  subgraph L["Legitimate ARP"]
    direction LR
    H1["Host A: who has 10.0.0.1?<br/>(broadcast)"] --> G1["Gateway: 10.0.0.1 is at AA:AA<br/>(unicast reply)"]
  end
  subgraph P["ARP spoofing"]
    direction LR
    X["Attacker sends unsolicited replies"] -->|"10.0.0.1 is at EE:EE"| V["Victim cache poisoned"]
    X -->|"10.0.0.50 is at EE:EE"| G2["Gateway cache poisoned"]
    V --> M["Traffic flows through the attacker"]
    G2 --> M
  end
  L ~~~ P
:::

:::notes
The Address Resolution Protocol (ARP), defined in RFC 826 (1982), operates at the boundary between the Network Layer (Layer 3) and the Data Link Layer (Layer 2) in the TCP/IP model. Its role is straightforward but essential: given a known IPv4 address on the local network segment, ARP discovers the corresponding MAC (Media Access Control) address so that an Ethernet frame can be addressed and delivered to the correct physical interface.

ARP works through a simple broadcast-and-reply mechanism. When Host A wants to send a packet to a destination IP address on the same subnet, it first checks its local ARP cache, a short-lived table of IP-to-MAC mappings. If the mapping is absent or expired, Host A sends an ARP Request as a broadcast frame (destination MAC: FF:FF:FF:FF:FF:FF) containing the target IP address. Every device on the LAN segment receives this broadcast. The device whose IP address matches the query sends back a unicast ARP Reply containing its MAC address. Host A stores this mapping in its ARP cache and uses it for subsequent frames until the entry times out (typically 2–20 minutes depending on the OS).

The critical security weakness of ARP is that it has **no authentication mechanism**. Any host on the local network can send ARP Replies, including unsolicited "gratuitous ARP" replies, and other hosts will accept them and update their ARP caches accordingly. This enables **ARP spoofing** (also called ARP poisoning or ARP cache poisoning), in which an attacker sends forged ARP Replies associating its own MAC address with the IP address of a legitimate host (such as the default gateway). Once neighboring hosts update their ARP caches with the forged mapping, their traffic intended for the gateway is instead delivered to the attacker, a classic **man-in-the-middle (MITM)** position. The attacker can then passively eavesdrop on plaintext protocols (HTTP, FTP, Telnet), inject or modify traffic, or perform further attacks such as SSL stripping. This attack class is catalogued in CVE-1999-0667 and remains relevant in unprotected switched LANs today.

Defensive countermeasures include **Dynamic ARP Inspection (DAI)** on managed switches, which validates ARP packets against a trusted DHCP snooping binding table and drops spoofed entries. **Static ARP entries** configured manually for critical hosts (such as the default gateway) also prevent cache poisoning but are difficult to maintain at scale. IPv6 replaces ARP with **Neighbor Discovery Protocol (NDP)**, which, when used with Secure Neighbor Discovery (SEND, RFC 3971), provides cryptographic authentication for address resolution, directly addressing the authentication gap that makes ARP vulnerable.

Tools such as `arpspoof` (from the dsniff suite) and `Ettercap` automate ARP spoofing attacks, making them accessible to unskilled attackers. Detection tools such as `arpwatch` monitor the network for unexpected changes in IP-to-MAC mappings and alert administrators. NIST SP 800-94 (Guide to Intrusion Detection and Prevention Systems) and CIS Control 12 (Network Infrastructure Management) both reference the importance of monitoring Layer 2 traffic for anomalous ARP activity.

In a normal ARP exchange a host broadcasts a request for an IP's MAC address and receives one reply. ARP has no authentication, so an attacker can send unsolicited ("gratuitous") replies continuously to keep a false entry in victims' caches, the mechanism of ARP cache poisoning.
:::

%%%

---
unit: Models
code: OSI
title: OSI Model vs TCP/IP Model, A Side-by-Side Comparison
---
:::callout style=soft
The **OSI (Open Systems Interconnection) model** is a seven-layer conceptual framework developed by ISO in 1984 to standardize network communication. The **TCP/IP model** is the pragmatic four-layer model that actually powers the internet. Understanding both is essential, practitioners use OSI layer numbers as a shared vocabulary, while real implementations follow TCP/IP.
:::

:::table
| OSI Layer | OSI Name | TCP/IP Layer | Key Protocols | Common Attack |
|---|---|---|---|---|
| 7 | Application | Application | HTTP, HTTPS, DNS, SMTP, FTP | SQL injection, XSS, phishing |
| 6 | Presentation | Application | TLS/SSL, MIME, JPEG encoding | SSL stripping, weak cipher negotiation |
| 5 | Session | Application | NetBIOS, RPC, SMB sessions | Session hijacking, replay attacks |
| 4 | Transport | Transport | TCP, UDP, SCTP | SYN flood, UDP amplification, port scanning |
| 3 | Network | Internet | IP (v4/v6), ICMP, OSPF, BGP | IP spoofing, fragmentation attacks, BGP hijacking |
| 2 | Data Link | Network Access | Ethernet, ARP, Wi-Fi (802.11), VLANs | ARP spoofing, MAC flooding, VLAN hopping |
| 1 | Physical | Network Access | Cables, fiber, radio, DSL | Wiretapping, signal jamming, hardware implants |
:::

::::columns
::col::
:::callout style=soft
**Why OSI if TCP/IP is what we use?** OSI gives engineers a precise vocabulary. Saying "this is a Layer 3 problem" immediately tells every engineer in the room that IP addresses and routing are involved, not the application or the cable. This shared shorthand is invaluable during incident response.
:::
::col::
:::list heading="Memory Aid for OSI Layers (top to bottom)" style=plain
- **A**ll, Application (7)
- **P**eople, Presentation (6)
- **S**eem, Session (5)
- **T**o, Transport (4)
- **N**eed, Network (3)
- **D**ata, Data Link (2)
- **P**rocessing, Physical (1)
:::
::::

:::code language=mermaid caption="OSI provides precision vocabulary; TCP/IP provides the actual implementation, security professionals need fluency in both"
flowchart LR
  O7["7 Application"] --> T4
  O6["6 Presentation"] --> T4
  O5["5 Session"] --> T4
  O4["4 Transport"] --> T3
  O3["3 Network"] --> T2
  O2["2 Data Link"] --> T1
  O1["1 Physical"] --> T1
  T4["Application<br/>HTTP, DNS, TLS, SSH"]
  T3["Transport<br/>TCP, UDP"]
  T2["Internet<br/>IP, ICMP"]
  T1["Network Access<br/>Ethernet, Wi-Fi, ARP"]
:::

:::notes
The OSI model was published by the International Organization for Standardization (ISO) in 1984 as a framework to guide the development of interoperable network products and protocols. It divides network communication into seven distinct layers, each with a specific and well-defined role. From bottom to top: Physical (Layer 1), Data Link (Layer 2), Network (Layer 3), Transport (Layer 4), Session (Layer 5), Presentation (Layer 6), and Application (Layer 7). The OSI model was intended to form the basis of a suite of standardized network protocols, but the pragmatic TCP/IP suite, which evolved from ARPANET research, became the dominant implementation in real-world networks.

The TCP/IP model consolidates the OSI model into four layers. The OSI Application, Presentation, and Session layers collapse into a single TCP/IP Application Layer. The OSI Transport Layer maps directly to the TCP/IP Transport Layer. The OSI Network Layer maps to the TCP/IP Internet Layer. The OSI Data Link and Physical layers are combined into the TCP/IP Network Access Layer (also called the Link Layer). This consolidation reflects the practical reality that protocols like TLS (which spans OSI Presentation and Session concerns) and HTTP (which spans OSI Application and Session concerns) do not map cleanly to individual OSI layers.

Despite the TCP/IP model being the operational standard, cybersecurity professionals universally reference OSI layer numbers in their daily work. The phrase "Layer 7 firewall" immediately conveys that the device inspects application-layer content (HTTP headers, URLs, payloads) rather than just IP addresses and ports. "Layer 2 attack" signals involvement of MAC addresses and switching. This vocabulary is embedded in industry certifications (CompTIA Security+, CISSP, CEH), vendor documentation, and frameworks like MITRE ATT&CK, which organizes network-based techniques partly by the OSI layer at which they operate.

Each OSI layer has characteristic attack classes. Physical Layer (L1) attacks include wiretapping, installation of hardware keyloggers or network taps, and radio frequency jamming of wireless links. Data Link Layer (L2) attacks include ARP spoofing (CVE-1999-0667), MAC flooding attacks against switches (causing them to fail open and broadcast all traffic), and VLAN hopping using double-tagging of 802.1Q frames. Network Layer (L3) attacks include IP spoofing, ICMP-based attacks such as Smurf amplification, and BGP route injection. Transport Layer (L4) attacks include TCP SYN floods (CVE-1999-0569), RST injection, and port scanning reconnaissance. Application Layer (L7) attacks include SQL injection, cross-site scripting, and credential phishing, by far the most prevalent category in modern breach reports.

NIST SP 800-53 organizes many of its security controls in ways that implicitly reflect this layered model. For example, SC-8 (Transmission Confidentiality and Integrity) addresses protections at the Transport/Presentation layer equivalents, while SC-5 (Denial-of-Service Protection) addresses threats spanning L3 through L7. ISO/IEC 27033 (Network Security) provides guidance on securing each layer of the network stack in enterprise environments.

Sophisticated attacks usually span several OSI layers. Stuxnet operated at the physical layer (industrial control systems), the network layer (worm propagation) and the application layer (PLC logic manipulation) at once. Analyzing attacks across layers builds the habit of thinking about them holistically rather than as a single vulnerability.
:::

%%%

---
unit: Addressing
code: SUB
title: Subnetting and CIDR Notation
---
:::callout style=soft
**Subnetting** divides a large IP address block into smaller, more manageable sub-networks. **CIDR (Classless Inter-Domain Routing)** notation compactly expresses both the IP address and the size of its subnet using a slash followed by the prefix length (e.g., `192.168.1.0/24`).
:::

::::columns
::col::
:::table
| CIDR Prefix | Subnet Mask     | Host Addresses | Typical Use |
|---|---|---|---|
| /8  | 255.0.0.0       | ~16.7 million | Large ISP or Class A enterprise |
| /16 | 255.255.0.0     | ~65,534 | Large campus or data center |
| /24 | 255.255.255.0   | 254 | Typical office subnet |
| /28 | 255.255.255.240 | 14 | Small VLAN, DMZ segment |
| /30 | 255.255.255.252 | 2 | Point-to-point router links |
| /32 | 255.255.255.255 | 1 (single host) | Host route, loopback |
:::
::col::
:::list heading="Why Subnetting Matters for Security" style=plain
- Limits **broadcast domains**, smaller blast radius for broadcast-based attacks
- Enables **network segmentation**, separate sensitive systems (HR, finance, OT/ICS) onto isolated subnets
- Supports **access control**, firewall rules and ACLs apply at subnet boundaries
- Reduces **lateral movement**, attackers cannot directly route between segments without crossing a firewall
- Enables **Zero Trust** micro-segmentation per NIST SP 800-207
:::
::::

:::callout style=soft
**Worked Example:** `10.10.5.0/28`, Subnet mask is 255.255.255.240. Usable host range: 10.10.5.1 – 10.10.5.14. Network address: 10.10.5.0. Broadcast: 10.10.5.15. Total hosts: 16 addresses, 14 usable.
:::

:::code language=mermaid caption="CIDR subnetting divides address space and creates security boundaries: traffic between subnets must cross a router or firewall, enabling enforcement of access controls"
flowchart TB
  N["192.168.1.0/24<br/>mask 255.255.255.0, 254 hosts"] --> A["192.168.1.0/26<br/>hosts .1 to .62<br/>broadcast .63"]
  N --> B["192.168.1.64/26<br/>hosts .65 to .126<br/>broadcast .127"]
  N --> C["192.168.1.128/26<br/>hosts .129 to .190<br/>broadcast .191"]
  N --> D["192.168.1.192/26<br/>hosts .193 to .254<br/>broadcast .255"]
  M["/26 mask: 255.255.255.192<br/>last octet 11000000, two bits borrowed, 62 hosts each"] -.- N
:::

:::notes
Subnetting and CIDR notation are foundational skills for network engineers and cybersecurity practitioners alike. Prior to CIDR, IPv4 address allocation followed a rigid classful scheme (Class A, B, C) that wasted large blocks of addresses and provided no flexibility for network sizing. CIDR, introduced in RFC 4632 (originally RFC 1519, 1993), abandoned fixed class boundaries and allowed any prefix length from /0 to /32, enabling efficient allocation that closely matches actual network size requirements and dramatically slowing the exhaustion of the IPv4 address space.

The subnet mask determines which bits of an IP address represent the network portion (fixed) and which represent the host portion (variable). A /24 prefix means the first 24 bits identify the network, leaving 8 bits for host addressing, supporting 2^8 = 256 addresses, of which 254 are usable (the network address and broadcast address are reserved). A /28 prefix leaves only 4 host bits, supporting 16 addresses (14 usable), making it appropriate for small DMZ segments or point-to-point links between security zones.

From a security architecture perspective, subnetting is the enabling technology for **network segmentation**, one of the most effective and cost-efficient security controls available. By placing sensitive systems (such as payment card data systems governed by PCI-DSS, medical records systems governed by HIPAA, or industrial control systems) on dedicated subnets, organizations create logical boundaries that traffic must cross via a router or firewall. This means that access control lists (ACLs) and firewall policies can enforce the principle of least privilege at the network layer: a compromised workstation on the user subnet cannot directly communicate with the finance database subnet without its traffic being inspected and potentially blocked at the intervening firewall.

The 2017 NotPetya ransomware attack provided a devastating illustration of what happens without segmentation: the malware spread laterally through corporate networks at extraordinary speed because workstations, servers, and operational technology (OT) systems were on flat, unsegmented networks. Once a single host was compromised, the worm could reach every other host with no intervening security controls. Maersk, one of the most severely affected organizations, lost approximately $300 million in a matter of hours. Proper network segmentation, specifically isolating OT/ICS systems per IEC 62443 and NIST SP 800-82 guidance, would have significantly limited the blast radius.

NIST SP 800-207 (Zero Trust Architecture) elevates segmentation to a core architectural principle, recommending micro-segmentation that extends the concept down to individual workload or even process boundaries rather than just physical subnets. This is often implemented through software-defined networking (SDN) or overlay technologies such as VXLAN, which decouple logical network segments from physical topology.

For the binary math: to find usable hosts, calculate 2^(32 − prefix_length) − 2. For subnetting problems on certification exams (Security+, CCNA, CISSP), practice converting between decimal subnet masks and CIDR prefix lengths until it becomes automatic, the ability to quickly determine whether two IP addresses are on the same subnet is essential for firewall rule analysis and incident response.

Segmentation should follow a threat model, not just address arithmetic. In a hospital network, clinical workstations, medical imaging (DICOM), administrative HR systems and an external EHR vendor connection each warrant their own subnet and inter-segment firewall rules based on what must talk to what.
:::

%%%

---
unit: Foundations
code: MAC
title: MAC Addresses and the Data Link Layer
---
:::callout style=soft
A **MAC (Media Access Control) address** is a 48-bit hardware identifier assigned to a network interface card (NIC) by its manufacturer. It uniquely identifies a device on a local network segment and is used by Layer 2 protocols like Ethernet to deliver frames to the correct physical device.
:::

::::columns
::col::
:::list heading="MAC Address Structure" style=plain
- **48 bits** total, written as 6 pairs of hexadecimal digits (e.g., `00:1A:2B:3C:4D:5E`)
- **First 24 bits (OUI)**, Organizationally Unique Identifier; assigned to the manufacturer by the IEEE
- **Last 24 bits**, Device-specific identifier assigned by the manufacturer
- **Bit 41** (multicast bit): 0 = unicast, 1 = multicast or broadcast
- **Bit 42** (LAA bit): 0 = globally administered (factory), 1 = locally administered (overridden)
:::
::col::
:::table
| Address Type | Example | Description |
|---|---|---|
| Unicast | 00:1A:2B:3C:4D:5E | Single destination NIC |
| Broadcast | FF:FF:FF:FF:FF:FF | All devices on the LAN segment |
| Multicast | 01:00:5E:xx:xx:xx | Specific group of devices |
:::

:::callout style=line
**MAC Spoofing:** Attackers change their NIC's MAC address using OS commands (`ip link set dev eth0 address XX:XX:XX:XX:XX:XX` on Linux). This bypasses MAC-based access controls and can impersonate trusted devices. Countermeasure: 802.1X port-based authentication.
:::
::::

:::code language=mermaid caption="The first three bytes of a MAC address identify the manufacturer (OUI); this is publicly searchable and can reveal device types during network reconnaissance"
block-beta
  columns 6
  b1["00"] b2["1A"] b3["2B"] b4["3C"] b5["4D"] b6["5E"]
  oui["OUI: first 3 bytes, assigned to the manufacturer<br/>e.g. Intel, Cisco, Apple"]:3 nic["Device identifier: last 3 bytes,<br/>chosen by the manufacturer"]:3
  f1["First byte, lowest bit: 0 unicast, 1 multicast<br/>second-lowest bit: 0 globally unique, 1 locally administered (LAA)"]:6
:::

:::notes
The Media Access Control (MAC) address is a Layer 2 identifier that plays a fundamental role in local network communication. Defined by the IEEE 802 standards family, particularly IEEE 802.3 (Ethernet) and IEEE 802.11 (Wi-Fi), MAC addresses enable switches and other Layer 2 devices to deliver Ethernet frames to the correct physical interface on a network segment without requiring knowledge of IP addresses.

Every NIC manufactured for commercial sale is assigned a globally unique MAC address by its manufacturer, in accordance with IEEE assignment guidelines. The first three bytes (24 bits) form the **Organizationally Unique Identifier (OUI)**, which is registered with the IEEE and publicly searchable. Knowing the OUI of a device immediately reveals its manufacturer (e.g., OUI 00:50:56 belongs to VMware, 3C:22:FB to Apple). This is valuable during network reconnaissance: an attacker or penetration tester who captures MAC addresses from ARP traffic or Wi-Fi beacons can immediately infer what types of devices are present on the network, a capability mapped to MITRE ATT&CK T1016 (System Network Configuration Discovery).

Ethernet switches build and maintain a **MAC address table** (also called a CAM table, Content Addressable Memory table) that maps MAC addresses to switch ports. When a frame arrives, the switch looks up the destination MAC in this table and forwards the frame only to the appropriate port (unicast forwarding), rather than broadcasting it to all ports. This is in contrast to a hub, which broadcasts every frame to every port. The MAC address table is learned dynamically from the source MAC addresses of incoming frames and has a configurable aging timeout.

**MAC flooding** is an attack that deliberately fills the switch's CAM table by rapidly sending frames with thousands of spoofed source MAC addresses. Once the CAM table is full, the switch can no longer learn new mappings and falls back to broadcasting all frames to every port, effectively turning a switch into a hub, allowing the attacker to eavesdrop on all network traffic. Tools like `macof` (from the dsniff suite) automate this attack. Port security features on managed switches (e.g., limiting the number of MAC addresses per port, using "sticky" MAC binding) mitigate this class of attack.

**MAC spoofing** refers to changing the MAC address of a NIC using software, overriding the factory-burned-in address. On Linux, this is done with `ip link set dev eth0 address XX:XX:XX:XX:XX:XX`; on Windows, it can be done through the NIC's advanced driver properties. MAC spoofing allows attackers to impersonate a trusted device to bypass MAC-based network access controls (a common but weak security measure used in some Wi-Fi networks and NAC systems). The proper countermeasure is 802.1X port-based authentication, which uses EAP (Extensible Authentication Protocol) and a RADIUS server to authenticate both the device and the user with credentials or certificates rather than relying on the easily spoofed MAC address.

NIST SP 800-153 (Guidelines for Securing Wireless Local Area Networks) and CIS Control 1 (Inventory and Control of Enterprise Assets) both emphasize the importance of actively inventorying and monitoring MAC addresses on the network, precisely because unauthorized or unknown MAC addresses on a network segment can indicate rogue devices or active attacks.

The first three bytes of a MAC address are the Organizationally Unique Identifier (OUI), which identifies the manufacturer. Captured frames can reveal device vendors, phone models and even virtual-machine software from the OUI alone, using the IEEE public database.
:::

%%%

---
unit: Addressing
code: IP6
title: IPv4 vs IPv6, Key Differences
---
:::callout style=soft
IPv4 has been the dominant internet protocol since 1983, but its 32-bit address space (~4.3 billion addresses) is exhausted. **IPv6**, standardized in RFC 8200 (2017), provides a 128-bit address space, over 340 undecillion addresses, along with built-in security, auto-configuration, and improved routing efficiency.
:::

:::table
| Feature | IPv4 | IPv6 |
|---|---|---|
| Address length | 32 bits (4 bytes) | 128 bits (16 bytes) |
| Address space | ~4.3 billion addresses | ~3.4 × 10^38 addresses |
| Address notation | Dotted decimal: 192.168.1.1 | Colon-hex: 2001:db8::1 |
| Header size | 20–60 bytes (variable, options) | 40 bytes (fixed) |
| Fragmentation | Handled by routers | Handled by source only |
| ARP | Yes (broadcast-based) | No, replaced by NDP (Neighbor Discovery Protocol) |
| IPsec | Optional | Mandatory specification (commonly optional in practice) |
| Auto-configuration | DHCP only | SLAAC (Stateless Address Autoconfiguration, RFC 4862) |
| NAT | Required (address exhaustion) | Not required (each device gets global address) |
| Multicast | Optional | Built-in, replaces broadcast |
| Loopback | 127.0.0.1 | ::1 |
:::

::::columns
::col::
:::callout style=soft
**Security implication of dual-stack environments:** Organizations running both IPv4 and IPv6 simultaneously must apply security controls to both protocol stacks. Attackers often probe IPv6 on networks where administrators have only secured IPv4, exploiting the "forgotten stack." This is called a **dual-stack bypass** and is increasingly documented in penetration testing engagements.
:::
::col::
:::list heading="IPv6 Address Types" style=plain
- **Global Unicast** (2000::/3), Publicly routable, globally unique
- **Link-Local** (FE80::/10), Valid only on the local link; auto-assigned; never routed
- **Loopback** (::1/128), Internal communications only
- **Unique Local** (FC00::/7), Private addressing equivalent; not globally routable
- **Multicast** (FF00::/8), Sent to a group of subscribers
:::
::::

:::code language=mermaid caption="IPv6 simplifies the header (fixed 40 bytes vs IPv4's variable 20–60 bytes), improving router processing speed but requiring entirely new security policies"
flowchart LR
  V4["<b>IPv4 header</b><br/>20 to 60 bytes, variable<br/>Version, IHL, DSCP, Total Length<br/>Identification, Flags, Fragment Offset<br/>TTL, Protocol, Header Checksum<br/>32-bit source and destination<br/>Options"] ~~~ V6["<b>IPv6 header</b><br/>fixed 40 bytes<br/>Version, Traffic Class, Flow Label<br/>Payload Length, Next Header<br/>Hop Limit<br/>128-bit source and destination<br/>No checksum, options in extension headers"]
:::

:::notes
The transition from IPv4 to IPv6 is one of the most significant and long-running engineering projects in computing history. IPv4 (defined in RFC 791, 1981) uses 32-bit addresses, providing approximately 4.3 billion unique addresses. This seemed ample when the protocol was designed, but the explosive growth of internet-connected devices, including smartphones, IoT sensors, industrial controllers, and consumer electronics, consumed the available address space far faster than anticipated. IANA officially allocated the last remaining IPv4 address blocks to regional registries in 2011, and most RIRs have since exhausted their free pools, resorting to waitlists and reclamation of abandoned blocks.

IPv6 (originally RFC 2460, updated to RFC 8200 in 2017) addresses this limitation with a 128-bit address space, providing approximately 3.4 × 10^38 unique addresses, enough to assign a globally unique address to every atom on the surface of the Earth several times over. Beyond address space, IPv6 introduces several architectural improvements: a **simplified, fixed-size 40-byte header** that eliminates the variable-length options field and the IHL (Internet Header Length) field of IPv4, improving router forwarding performance; **Stateless Address Autoconfiguration (SLAAC, RFC 4862)**, which allows devices to automatically configure a globally unique address using their MAC address and the network prefix, without requiring DHCP; and mandatory support for **IPsec** in the specification (though this is frequently not enforced in practice due to performance considerations).

From a security perspective, the shift to IPv6 creates both improvements and new challenges. On the improvement side, **Neighbor Discovery Protocol (NDP)**, which replaces ARP in IPv6, supports Secure Neighbor Discovery (SEND, RFC 3971) using RSA cryptographic signatures to authenticate neighbor advertisements, directly addressing the ARP spoofing vulnerability that has plagued IPv4 networks for decades. IPv6 also eliminates broadcast addresses (replacing them with multicast), reducing the attack surface for broadcast-based amplification attacks.

However, IPv6 introduces new attack vectors. The very large address space (a single /64 subnet has 2^64 host addresses) makes traditional sequential host scanning impractical, but attackers can still find hosts through other means such as DNS enumeration, DHCPv6 logs, or passive monitoring of NDP traffic. **Router Advertisement (RA) spoofing** is the IPv6 equivalent of rogue DHCP: an attacker sends forged RA messages to claim the role of default gateway or inject malicious DNS server addresses, performing a man-in-the-middle attack. RA Guard (RFC 6105) is the recommended countermeasure, implemented on managed switches.

The most practically significant security issue today is the **dual-stack gap**: organizations that have deployed IPv6 alongside IPv4 but have only configured security controls for IPv4. Firewalls, IDS signatures, DLP systems, and logging infrastructure that lack IPv6 support create blindspots that attackers exploit. Multiple penetration testing firms report that bypassing perimeter security via IPv6 is frequently possible in enterprise environments that have not explicitly audited their IPv6 security posture. NIST SP 800-119 (Guidelines for the Secure Deployment of IPv6) provides comprehensive guidance on addressing this risk.

Most modern devices already hold IPv6 addresses, typically a link-local address (FE80::/10) and often a global unicast address, even on networks managed as IPv4. Firewall policies that address only IPv4 leave this dual-stack traffic uncontrolled, a common gap in practice.
:::

%%%

---
unit: Foundations
code: ICM
title: ICMP, The Network Diagnostic Protocol
---
:::callout style=soft
The **Internet Control Message Protocol (ICMP)**, defined in RFC 792, is an auxiliary protocol that operates at the Internet Layer alongside IP. It carries **error messages** and **operational information** between network devices, not user data. Tools like `ping` and `traceroute` use ICMP to test connectivity and map network paths.
:::

::::columns
::col::
:::table
| ICMP Type | Code | Message | Security Relevance |
|---|---|---|---|
| 0 | 0 | Echo Reply | Response to ping; confirms host is alive |
| 3 | 0–15 | Destination Unreachable | Reveals network topology; port 3/3 exposes filtered ports |
| 5 | 0–3 | Redirect | Historically abused to reroute traffic (MITM) |
| 8 | 0 | Echo Request | Ping; host discovery (MITRE ATT&CK T1018) |
| 11 | 0 | Time Exceeded (TTL=0) | Used by traceroute to map routing hops |
| 13 | 0 | Timestamp Request | Can be used for OS fingerprinting |
:::
::col::
:::list heading="ICMP-Based Attacks" style=plain
- **Ping Flood (ICMP Flood)**, Overwhelming a host with Echo Requests; a simple DoS attack
- **Smurf Attack**, Spoofed ICMP Echo Requests sent to broadcast addresses; amplifies traffic toward victim (largely mitigated by RFC 2644)
- **Ping of Death**, Oversized ICMP packets cause buffer overflow on receiving host (CVE-1999-0128)
- **ICMP Tunneling**, Encodes data in ICMP Echo Request/Reply payloads to exfiltrate data or establish covert C2 channel
- **ICMP Redirect Attacks**, Forged Type 5 messages manipulate routing tables
:::
::::

:::code language=mermaid caption="Ping uses ICMP Types 8 and 0 to test reachability; traceroute uses the TTL field and Type 11 Time Exceeded replies to map every hop along a network path"
sequenceDiagram
  participant H as Host
  participant R1 as Router 1
  participant R2 as Router 2
  participant D as Destination
  H->>D: Ping: Echo Request
  D-->>H: Echo Reply, round-trip time measured
  H->>R1: Traceroute probe, TTL 1
  R1-->>H: Time Exceeded
  H->>R2: Probe, TTL 2
  R2-->>H: Time Exceeded
  H->>D: Probe, TTL 3
  D-->>H: Reply: destination reached
:::

:::notes
ICMP (Internet Control Message Protocol), defined in RFC 792 for IPv4 and RFC 4443 for ICMPv6, is an integral part of the IP protocol suite. Unlike TCP or UDP, ICMP does not carry user application data, its purpose is entirely operational: reporting errors, testing connectivity, and providing feedback about routing conditions. Despite its auxiliary role, ICMP is frequently involved in both network diagnostics and network attacks, making it essential knowledge for security professionals.

The most widely known use of ICMP is the `ping` utility, which sends ICMP Type 8 (Echo Request) messages to a target host and expects Type 0 (Echo Reply) responses. The round-trip time (RTT) for each exchange indicates network latency. On Windows, `ping` sends four requests by default; on Linux/macOS, it continues indefinitely until interrupted. Similarly, `traceroute` (or `tracert` on Windows) works by sending packets with progressively increasing TTL values. When a packet's TTL reaches zero at an intermediate router, that router sends back an ICMP Type 11 (Time Exceeded) message, revealing its IP address. By incrementing the TTL from 1 upward, traceroute maps every hop along the path to the destination.

From a security standpoint, ICMP is a double-edged protocol. On the diagnostic side, it is indispensable for troubleshooting connectivity issues and verifying network paths. On the offensive side, it is frequently abused. **ICMP host discovery** (MITRE ATT&CK T1018, T1046) uses Echo Requests to identify live hosts on a subnet, a common first step in network reconnaissance. Blocking ICMP entirely at perimeter firewalls (a common but misguided practice) prevents this discovery but also breaks legitimate diagnostic tools and can interfere with TCP's Path MTU Discovery mechanism (RFC 1191), causing performance issues with connections to some destinations.

**ICMP tunneling** encodes arbitrary data within the payload field of ICMP Echo Request and Reply packets, creating a covert channel that bypasses firewalls that permit ICMP while blocking other protocols. Tools like ptunnel and ICMP-shell implement this technique. Detection requires inspecting ICMP payload sizes and content patterns, legitimate ping payloads are typically small and contain predictable byte patterns, while tunneled payloads are larger, carry higher-entropy data, and appear in sustained bidirectional flows rather than isolated exchanges.

The **Smurf attack** (largely historical but instructive) exploited ICMP broadcasts: an attacker sent ICMP Echo Requests to subnet broadcast addresses with a spoofed source IP matching the victim's address. All hosts on the target subnet would simultaneously reply to the victim, generating amplified traffic. RFC 2644 addressed this by recommending that routers not forward directed broadcast packets, effectively mitigating Smurf attacks at the network level, an early example of a protocol-level design change made specifically to close a security vulnerability.

NIST SP 800-41 (Guidelines on Firewalls and Firewall Policy) recommends a nuanced approach to ICMP filtering: block Echo Requests from untrusted networks inbound (to prevent host discovery) while permitting Time Exceeded and Destination Unreachable messages that are required for TCP's proper operation. CIS Benchmark firewall rules provide specific ICMP filtering recommendations by type and code, allowing defenders to permit operationally necessary ICMP while blocking commonly abused types.

A traceroute to a public destination shows each hop, an ISP router, a backbone peering point, a data center edge router, along the path. Any hop under an attacker's control can observe, and potentially modify, the traffic passing through it.
:::

%%%

---
unit: Infrastructure
code: SRH
title: Hubs, Switches, and Routers, What's the Difference?
---
:::callout style=soft
Hubs, switches, and routers are all devices that forward network traffic, but they operate at different layers and make forwarding decisions in fundamentally different ways. Confusing them is one of the most common sources of network misconfiguration and security blindspots.
:::

:::table
| Device | OSI Layer | Forwarding Basis | Intelligence | Security Relevance |
|---|---|---|---|---|
| Hub | Layer 1 (Physical) | None, broadcasts all traffic to every port | Dumb, no address awareness | All traffic visible to every connected device; ideal for passive sniffing but completely insecure |
| Switch | Layer 2 (Data Link) | Destination MAC address from CAM table | Learns MAC-to-port mappings dynamically | Traffic isolated per port (unicast); vulnerable to MAC flooding, ARP spoofing |
| Router | Layer 3 (Network) | Destination IP address from routing table | Consults routing table, runs routing protocols | Enforces subnet boundaries; natural firewall policy enforcement point |
| Layer 3 Switch | Layer 2 + 3 | MAC and IP, performs both switching and routing | Combines switch and router functions | Used in campus networks for inter-VLAN routing; inherits vulnerabilities of both |
:::

::::columns
::col::
:::callout style=soft
**Why hubs disappeared:** Because hubs broadcast every frame to every port, any device connected to a hub could passively capture all network traffic, making LAN-level eavesdropping trivial. Switches eliminated this by forwarding frames only to the destination port, confining traffic. However, switches can be forced back into hub-like behavior via MAC flooding attacks.
:::
::col::
:::list heading="Key Concepts" style=plain
- **Collision domain**, Hub: one shared collision domain for all ports; Switch: each port is its own collision domain
- **Broadcast domain**, Both hubs and switches forward broadcast frames to all ports (same broadcast domain); routers do NOT forward broadcasts
- **CAM table**, Switch's MAC-to-port mapping table; target of MAC flooding attacks
- **Routing table**, Router's IP-to-next-hop mapping table; populated by static routes or routing protocols (OSPF, BGP)
:::
::::

:::code language=mermaid caption="Hubs broadcast everything; switches forward by MAC; routers forward by IP, each device creates different traffic visibility and different attack surfaces"
flowchart LR
  H["<b>Hub</b> (layer 1)<br/>Every frame repeated to every port<br/>Anyone can listen"] ~~~ S["<b>Switch</b> (layer 2)<br/>Learns MAC addresses<br/>Frames sent only to the right port"] ~~~ R["<b>Router</b> (layer 3)<br/>Connects different subnets<br/>e.g. 10.0.1.0/24 and 10.0.2.0/24"]
:::

:::notes
Understanding the functional and security differences between hubs, switches, and routers is foundational for network defenders. These three device types span the bottom three layers of the OSI model and define the basic architecture of any LAN.

A **hub** is a Layer 1 (Physical) device that simply repeats every incoming electrical signal out to every other port simultaneously. It has no awareness of addresses, protocols, or frame boundaries, it is purely a signal repeater. This means that every frame sent by any device connected to the hub is received by every other device. In the 1990s, Ethernet hubs were ubiquitous, and passive eavesdropping on hub-connected networks was trivial, any connected device running a packet sniffer could capture all traffic on the segment. Hubs have been almost entirely replaced by switches in modern networks, but understanding them explains both the security history of Ethernet and why certain attack techniques exist.

A **switch** is a Layer 2 (Data Link) device that learns which MAC addresses are reachable through which ports by examining the source MAC address of every incoming frame. It stores these mappings in a CAM (Content Addressable Memory) table. When a frame arrives destined for a MAC address that is in the CAM table, the switch forwards the frame only to the appropriate port (unicast forwarding), rather than broadcasting it to all ports. This dramatically improves both performance (no unnecessary traffic) and security (traffic is isolated between ports). However, switches are not immune to attack: MAC flooding (sending frames with thousands of spoofed source MACs to overflow the CAM table) causes the switch to fail open and revert to hub-like behavior, and ARP spoofing allows an attacker to hijack traffic at the switch by corrupting ARP caches. Managed switches address these vulnerabilities through port security, Dynamic ARP Inspection (DAI), and 802.1X authentication.

A **router** is a Layer 3 (Network) device that forwards packets based on destination IP addresses using a routing table. Unlike switches, routers do not forward broadcast packets between interfaces, effectively creating boundaries between broadcast domains. This is the mechanism that allows network administrators to isolate subnets: a router sits at the boundary between subnets and enforces which traffic is permitted to cross by consulting its routing table and, if combined with ACLs or firewall functionality, security policies. Routers run routing protocols such as OSPF (Open Shortest Path First, RFC 2328) or BGP (Border Gateway Protocol, RFC 4271) to dynamically discover network topology and maintain routing tables. BGP is particularly security-sensitive: BGP hijacking (where an autonomous system advertises incorrect routing prefixes) can reroute internet traffic through attacker-controlled infrastructure, as seen in numerous incidents including the 2018 Amazon Route 53 BGP hijack that redirected cryptocurrency traffic.

**Layer 3 switches** combine the MAC-based switching of Layer 2 with IP-based routing, making them common in enterprise campus networks for inter-VLAN routing. They offer the port density and performance of a switch with the subnet-separation capabilities of a router.

NIST SP 800-189 (Resilient Interdomain Traffic Exchange) provides guidance on securing router infrastructure, while CIS Controls include specific benchmarks for switch and router hardening (disabling unused ports, enabling port security, securing management interfaces with SSH rather than Telnet).

Whether a network uses hubs or switches changes an attacker's options after compromising one host: a hub broadcasts all traffic to every port, while a switch forwards only to the destination port, which is why network visibility and segmentation are central defensive concerns.
:::

%%%

---
unit: Infrastructure
code: TOP
title: Network Topologies
---
:::callout style=soft
A **network topology** describes the physical or logical arrangement of nodes and connections in a network. Topology choices affect performance, fault tolerance, cost, and, critically, the blast radius of a security incident.
:::

::::columns
::col::
:::table
| Topology | Shape | Fault Tolerance | Scalability | Security Notes |
|---|---|---|---|---|
| Bus | Linear | Low, one break affects all | Poor | All traffic on shared medium; easy to sniff |
| Star | Hub/switch at center | Medium, switch failure kills segment | Good | Central device is single point of compromise |
| Ring | Circular | Low, break disrupts ring | Moderate | Single failure disrupts entire ring |
| Mesh (Full) | All-to-all connections | Very high, multiple redundant paths | Poor (expensive) | Used in critical infrastructure; no single point of failure |
| Mesh (Partial) | Selective redundancy | High | Good | Common in enterprise WAN and internet backbone |
| Tree (Hierarchical) | Root-branch-leaf | Moderate | Excellent | Most enterprise networks; attacks on trunk links are high-impact |
| Hybrid | Combination | Varies | Varies | Most real-world enterprise networks are hybrid star-tree or star-mesh |
:::
::col::
:::callout style=soft
**Real-World Impact of Topology on Incidents:** In the 2003 Slammer worm outbreak, flat (bus-like) internal network topologies allowed the worm to spread to all visible hosts within seconds of first infection. Organizations with hierarchical or segmented topologies experienced significantly slower propagation, giving defenders more time to respond.
:::
::::

:::image src="images/11_network_topologies_comparison.png" alt="Six topology diagrams arranged in a grid: bus (linear nodes on shared cable), star (nodes radiating from central switch), ring (nodes in circle), full mesh (all nodes interconnected), tree (hierarchical layers), and hybrid (star segments connected in tree); each labeled with fault tolerance and scalability ratings" caption="Topology determines how failures and attacks propagate: flat topologies maximize blast radius while hierarchical and segmented designs limit lateral movement" width=full
:::

:::notes
Network topology is one of the most consequential design decisions in network architecture, with direct implications for performance, availability, and security. The topology, both physical (how cables and devices are actually connected) and logical (how traffic flows regardless of physical arrangement), determines the pathways available for both legitimate communication and malicious lateral movement.

The **bus topology**, common in early Ethernet (10BASE2, 10BASE5), connected all devices to a single shared coaxial cable. Every device received every transmission; a device that wanted to send had to wait for the medium to be idle (CSMA/CD, Carrier Sense Multiple Access with Collision Detection). This architecture made passive eavesdropping trivially easy and meant that a single cable break could disable the entire network. While bus topologies have been replaced by switched Ethernet in virtually all modern deployments, the concept remains relevant when analyzing legacy OT/ICS environments or understanding the historical context of Ethernet security.

The **star topology**, now the dominant LAN architecture, connects all devices to a central switch or hub. Traffic between devices passes through the central device, which provides a natural point for traffic monitoring, access control, and segmentation. The central device is a single point of failure for the segment it serves, which is why enterprise designs typically include redundant switches (via Spanning Tree Protocol, STP, and its modern variants like RSTP and MSTP). The central switch is also a high-value attack target: an attacker who compromises the management interface of a core switch gains visibility into and control over all traffic on that segment, which is why switch management should be isolated in a dedicated management VLAN with strict access controls per NIST SP 800-53 Control SC-7.

The **mesh topology** connects each node to multiple other nodes, creating redundant paths that provide high fault tolerance and resilience. Full mesh (every node connected to every other node) is extremely expensive in port count and cabling but provides maximum redundancy, it is used in critical infrastructure such as military communications and inter-datacenter links. Partial mesh selectively adds redundant links to the most critical paths and is the basis of internet backbone architecture. BGP (Border Gateway Protocol) is the routing protocol that navigates this partial mesh, dynamically selecting among multiple available paths.

The **tree (hierarchical) topology** organizes the network into layers, typically a core layer (high-speed backbone switches), distribution layer (aggregation and policy enforcement), and access layer (end-user connectivity). This is the dominant enterprise campus network design, recommended by Cisco's Enterprise Network Design guide and consistent with NIST guidance on network architecture. The hierarchical model provides clear security enforcement points at each layer boundary: distribution layer switches apply ACLs and VLAN policies; the core layer focuses on forwarding performance; access layer ports apply port security and 802.1X authentication. An attacker who compromises a trunk link between the distribution and core layers gains broad visibility, making these links particularly important to protect with physical security, encrypted management, and monitoring.

Understanding topology is essential for threat modeling: when constructing an attack path analysis, defenders must ask "given the topology, which hosts can this compromised device reach directly, and which require traversal of a controlled boundary?" MITRE ATT&CK's lateral movement tactic (TA0008) is fundamentally constrained by network topology and segmentation.

Attack impact depends on topology. From a compromised switch, an attacker reaches the traffic that switch carries; VLAN segmentation limits that reach, and a device at the distribution layer carries far more traffic than one at the access layer. Reasoning topologically about position clarifies impact.
:::

%%%

---
unit: Infrastructure
code: VLN
title: VLANs, Virtual Network Segmentation
---
:::callout style=soft
A **VLAN (Virtual Local Area Network)** creates logically isolated network segments on the same physical switch infrastructure. Traffic in one VLAN cannot reach another VLAN without passing through a router or Layer 3 switch, enabling segmentation without requiring separate physical hardware.
:::

::::columns
::col::
:::list heading="Why VLANs Matter for Security" style=plain
- **Isolation**, Separate sensitive systems (finance, HR, IoT, guest) onto dedicated VLANs without physical separation
- **Broadcast containment**, Limits broadcast domains, reducing noise and broadcast-based attack impact
- **Access control**, Inter-VLAN traffic must traverse a Layer 3 device where ACLs and firewall rules apply
- **Compliance**, PCI-DSS requires cardholder data to be isolated in a dedicated network segment (VLAN achieves this)
- **Manageability**, Logical groupings independent of physical location
:::
::col::
:::table
| VLAN | Purpose | Typical Security Controls |
|---|---|---|
| VLAN 10, Corporate | Employee workstations | 802.1X authentication, antivirus, DLP |
| VLAN 20, Finance | Accounting systems, POS | Strict ACLs, encrypted inter-VLAN traffic |
| VLAN 30, IoT | Cameras, printers, sensors | Isolated from corporate; outbound-only ACLs |
| VLAN 40, Guest Wi-Fi | Visitor internet access | Internet-only access, no internal reachability |
| VLAN 99, Management | Switch/router management interfaces | Accessible only from jump host; MFA required |
:::
::::

:::callout style=line
**VLAN Hopping Attack:** In a double-tagging attack, an attacker on an access port crafts frames with two 802.1Q tags. The first tag matches the attacker's native VLAN; the switch strips it and forwards the frame to a trunk port. The remaining tag causes the frame to be delivered to the target VLAN, bypassing VLAN isolation. **Mitigation:** Never use the default VLAN (VLAN 1) as the native VLAN; explicitly tag all frames on trunk ports.
:::

:::code language=mermaid caption="VLANs provide logical isolation on shared hardware; inter-VLAN traffic must pass through a firewall, creating enforcement points, but VLAN hopping attacks can bypass this isolation if native VLAN is misconfigured"
flowchart TB
  SW["One physical switch"]
  SW --- V10["VLAN 10 Corporate"]
  SW --- V20["VLAN 20 Finance"]
  SW --- V30["VLAN 30 IoT"]
  SW --- V40["VLAN 40 Guest"]
  V10 --> FW["Router / firewall<br/>enforces inter-VLAN rules"]
  V20 --> FW
  V30 --> FW
  V40 --> FW
  FW --> NET["Internet"]
  H["VLAN hopping by double tagging:<br/>prevented by not using the native VLAN for users"] -.- SW
:::

:::notes
VLANs (Virtual Local Area Networks), defined in IEEE 802.1Q, allow a single physical switch to host multiple logically isolated network segments. Each frame is tagged with a 12-bit VLAN ID (supporting up to 4,094 VLANs) in the 802.1Q header, which is inserted between the Ethernet source address and the EtherType field. Switches use this tag to determine which VLAN a frame belongs to and forward accordingly, frames in VLAN 10 are never forwarded to ports in VLAN 20 unless traffic is explicitly routed through an inter-VLAN routing device.

VLAN segmentation is one of the most cost-effective security controls available to network architects. Rather than purchasing separate physical switches for each department or security zone, VLANs allow the same hardware to host multiple isolated segments. This capability is foundational to **defense in depth** and directly supports the principle of **least privilege at the network layer**: a compromised device on the guest Wi-Fi VLAN should not be able to communicate with the finance VLAN at all, regardless of what credentials or exploits the attacker possesses.

Compliance frameworks mandate VLAN-style segmentation explicitly. **PCI-DSS Requirement 1.3** requires that the cardholder data environment (CDE) be isolated from other networks using network controls, in practice, this almost always means a dedicated VLAN with strict ingress/egress firewall rules. **HIPAA's Technical Safeguard** requirements mandate that systems containing electronic protected health information (ePHI) be segregated from general network traffic. **IEC 62443** (Industrial Automation and Control Systems security) requires that operational technology (OT) networks be isolated from corporate IT networks, typically implemented via air gaps or dedicated VLANs with a demilitarized zone (DMZ) between them.

The most significant VLAN-specific attack is **VLAN hopping**, which exploits misconfigured switch port modes. There are two primary techniques. The first is **switch spoofing**: an attacker sends Dynamic Trunking Protocol (DTP) negotiation frames from an access port, causing the switch to establish a trunk link with the attacker's device, giving access to all VLANs carried on that trunk. Mitigation: disable DTP on all access ports (`switchport nonegotiate`, `switchport mode access`). The second is **double-tagging**: an attacker crafts a frame with two 802.1Q tags, the outer tag matches the native VLAN of the trunk, which the ingress switch strips before forwarding; the inner tag targets a different VLAN, which the next switch forwards to the victim segment. This attack is unidirectional (replies cannot reach the attacker through the same path) but can be used for reconnaissance or DoS. Mitigation: configure the native VLAN to a dedicated, unused VLAN ID and tag it explicitly, so that access ports carrying user traffic are never in the native VLAN.

Management VLANs (often VLAN 99 by convention) deserve special attention: management access to network devices should be segregated from production traffic and accessible only through a designated jump host or bastion server. Access to the management VLAN should require strong authentication (ideally multi-factor) and all management sessions should be encrypted (SSH, HTTPS, never Telnet or HTTP). CIS Controls and NIST SP 800-53 Control AC-17 specifically address the security of remote and out-of-band management access.

On a single flat network, ransomware on one workstation can reach every other system. With segmentation, employee workstations, finance systems with no inbound file-sharing from the employee VLAN, and isolated IoT devices on separate VLANs, propagation is confined to one segment. The contrast shows what segmentation buys.
:::

%%%

---
unit: Infrastructure
code: DHP
title: DHCP, Dynamic Host Configuration
---
:::callout style=soft
The **Dynamic Host Configuration Protocol (DHCP)**, defined in RFC 2131, automatically assigns IP addresses and network configuration parameters to devices when they join a network, eliminating the need for manual IP address configuration on every host.
:::

::::columns
::col::
:::steps
1. **DISCOVER**, New device broadcasts a DHCPDISCOVER message (source: 0.0.0.0, destination: 255.255.255.255) seeking any available DHCP server.
2. **OFFER**, DHCP server responds with DHCPOFFER containing an available IP address, subnet mask, default gateway, DNS server, and lease duration.
3. **REQUEST**, Client broadcasts DHCPREQUEST accepting the offered address (may be seen by multiple servers if multiple replied).
4. **ACK**, Server sends DHCPACK confirming the assignment; client configures its interface with the provided parameters.
:::
::col::
:::table
| DHCP Lease Parameter | Example Value | Security Relevance |
|---|---|---|
| IP Address | 192.168.1.105 | Assigns network identity |
| Subnet Mask | 255.255.255.0 | Defines local segment |
| Default Gateway | 192.168.1.1 | Routes all non-local traffic through this device |
| DNS Server | 8.8.8.8 | Resolves domain names, attacker can redirect here |
| Lease Duration | 86400 seconds (1 day) | How long before client must renew |
| Domain Name | corp.example.com | Reveals internal domain structure |
:::
::::

:::callout style=line
**DHCP Spoofing Attack:** An attacker runs a rogue DHCP server on the LAN that responds to DHCPDISCOVER messages faster than the legitimate server. Victims receive malicious configuration: the attacker's IP as the default gateway (enabling MITM) and malicious DNS server (enabling DNS hijacking). Countermeasure: **DHCP Snooping** on managed switches limits DHCP server responses to trusted ports only.
:::

:::code language=mermaid caption="DHCP's DORA process is unauthenticated, any device can claim to be a DHCP server; DHCP Snooping on managed switches is the primary countermeasure"
sequenceDiagram
  participant C as Client
  participant D as Legitimate DHCP server
  participant X as Rogue DHCP server
  C->>D: Discover (broadcast)
  C->>X: Discover reaches every host
  X-->>C: Offer arrives first: attacker as gateway and DNS
  D-->>C: Offer arrives too late
  C->>X: Request
  X-->>C: Acknowledge
  Note over C,X: Defense: DHCP snooping,<br/>only trusted ports may send offers
:::

:::notes
DHCP (Dynamic Host Configuration Protocol), standardized in RFC 2131 (1997) and extended by RFC 2132 (options) and RFC 3315 (DHCPv6 for IPv6 environments), is one of the most critical yet frequently overlooked infrastructure protocols in enterprise networks. Without DHCP, network administrators would need to manually configure the IP address, subnet mask, default gateway, DNS server addresses, and other parameters on every device that joins the network, an unmanageable burden in organizations with thousands of devices, high employee turnover, or guest wireless access.

The DHCP process is often abbreviated as **DORA**: Discover, Offer, Request, Acknowledge. It begins when a device connects to the network with no IP address. The client broadcasts a DHCPDISCOVER frame on the local segment (UDP source port 68, destination port 67, broadcast destination). Any DHCP server that receives the broadcast may respond with a DHCPOFFER containing available configuration parameters. The client typically accepts the first offer received, sending a DHCPREQUEST broadcast to confirm its selection (broadcast so that all servers know which offer was accepted and others can reclaim their tentative allocations). Finally, the authoritative DHCP server sends a DHCPACK to confirm the assignment and start the lease timer.

The lease mechanism is significant from a security perspective: DHCP leases have a configurable duration, after which the client must renew the lease. If the renewal fails (e.g., the DHCP server is unreachable), the client loses its network configuration. The lease database maintained by the DHCP server is a valuable forensic artifact: it records which MAC address (and thus which device) held which IP address at which time, enabling investigators to correlate network activity logs with physical devices. Many organizations fail to preserve or audit DHCP logs, creating gaps in their ability to trace network-based attacks to specific devices.

The primary security vulnerability of DHCP is its complete lack of authentication. The protocol was designed for administrative convenience in a trusted LAN, with the assumption that all devices on the LAN were legitimate. **DHCP spoofing** (MITRE ATT&CK T1557.003) exploits this by deploying a rogue DHCP server that responds to client DISCOVER messages faster than the legitimate server. Clients that receive the rogue OFFER will configure their interfaces with attacker-controlled parameters, most critically, an attacker-controlled default gateway (enabling all traffic to flow through the attacker's machine for MITM interception) and attacker-controlled DNS servers (enabling DNS hijacking for all unencrypted protocol traffic). This attack requires physical or logical access to the LAN segment (or a compromised device on the segment) and is a common follow-on step after establishing a foothold in an enterprise network.

**DHCP Snooping** is the primary defense, implemented on managed switches. It designates specific ports as "trusted" (where legitimate DHCP servers are connected) and "untrusted" (end-device access ports). DHCP server messages (OFFER and ACK) arriving on untrusted ports are silently dropped, preventing rogue servers from influencing client configuration. DHCP Snooping also builds a binding table mapping IP addresses to MAC addresses and switch ports, which is used by Dynamic ARP Inspection (DAI) and IP Source Guard to detect and prevent related attacks.

DHCPv6, defined in RFC 3315, provides address assignment for IPv6 environments. In many IPv6 deployments, however, SLAAC (Stateless Address Autoconfiguration) is used instead, eliminating the DHCP server entirely. In such environments, Router Advertisement (RA) messages from the default gateway provide prefix information to clients, introducing the RA spoofing attack vector as a substitute for DHCP spoofing.

DHCP assigns an address through a four-step Discover-Offer-Request-Acknowledge exchange that also delivers the DNS server and default gateway. A rogue DHCP server can supply attacker-controlled values for both, placing itself in a man-in-the-middle position.
:::

%%%

---
unit: Infrastructure
code: FWL
title: Firewalls, The Network Gatekeeper
---
:::callout style=soft
A **firewall** is a network security device (hardware or software) that monitors and controls incoming and outgoing network traffic based on predefined security rules. It creates a boundary between trusted internal networks and untrusted external networks.
:::

::::columns
::col::
:::table
| Firewall Type | Inspection Method | Key Feature | Limitation |
|---|---|---|---|
| Packet filter | IP/port headers only | Very fast, low overhead | Cannot inspect payload or track state |
| Stateful | Connection state table | Tracks established sessions | Cannot inspect application-layer content |
| Application (Layer 7) | Full packet content | Understands application protocols (HTTP, DNS) | Higher latency, higher cost |
| Next-Generation (NGFW) | Layer 7 + IPS + TLS inspection | Identifies apps regardless of port, blocks exploits | Requires TLS decryption infrastructure |
| Web Application Firewall (WAF) | HTTP/HTTPS content | Protects web apps from SQLi, XSS, CSRF | Specific to web traffic only |
:::
::col::
:::list heading="Firewall Rule Concepts" style=plain
- **Default deny**, Block everything not explicitly permitted (recommended baseline per CIS Controls)
- **Ingress filtering**, Filter packets entering the network; blocks spoofed source IPs (RFC 2827, BCP 38)
- **Egress filtering**, Filter outbound traffic; prevents data exfiltration and C2 beaconing
- **DMZ (Demilitarized Zone)**, A network zone for public-facing services, isolated from both the internet and internal network
- **Implicit deny**, The unwritten last rule: if no rule matches, block the traffic
:::
::::

:::code language=mermaid caption="A DMZ places public-facing servers in a controlled zone between two firewalls, neither fully trusted nor fully exposed, limiting the blast radius of a server compromise"
flowchart LR
  I["Internet"] --> F1["Perimeter firewall<br/>allow 443 to web, 25 to mail"]
  F1 --> DMZ["DMZ<br/>web server, email gateway"]
  DMZ --> F2["Internal firewall<br/>allow only web to app on 8443"]
  F2 --> LAN["Corporate LAN"]
  I -.-x|"no direct path"| LAN
:::

:::notes
Firewalls are among the most fundamental and longest-established security controls in network architecture. The concept dates to the late 1980s, when the first packet-filtering routers (described by Jeff Mogul at DEC in 1988) were used to restrict traffic between network segments. The technology has evolved dramatically since then, but the core mission remains the same: enforce a security policy on network traffic by permitting authorized flows and blocking unauthorized ones.

**Packet-filtering firewalls** operate at the Network and Transport layers (OSI Layers 3–4), making forwarding decisions based solely on information in the IP and TCP/UDP headers: source IP address, destination IP address, source port, destination port, and protocol type. They are extremely fast and have minimal processing overhead, making them suitable for high-throughput environments. However, they cannot distinguish between a legitimate HTTP request and an HTTP-tunneled attack, they only see that port 80 is permitted, not what the HTTP payload contains.

**Stateful inspection firewalls** maintain a connection state table that tracks the state of each active network connection (SYN sent, established, FIN-WAIT, etc.). This allows the firewall to distinguish between a new incoming connection (which might be an attack) and a returning response packet from an outbound connection the protected host initiated (which is expected). Stateful firewalls significantly reduce false positives compared to packet filters and block many spoofed packet attacks that exploit the stateless nature of early packet filters. Cisco's PIX (1994) popularized stateful inspection in enterprise environments.

**Next-Generation Firewalls (NGFWs)**, introduced by Palo Alto Networks around 2007 and now the industry standard, combine stateful inspection with deep packet inspection (DPI), intrusion prevention system (IPS) capabilities, application identification (App-ID), user identification (User-ID), and TLS/SSL decryption. NGFWs can identify applications by their behavior and payload patterns rather than just port numbers, recognizing that modern applications often use non-standard ports or tunnel over HTTPS. This is critical because MITRE ATT&CK technique T1571 (Non-Standard Port) and T1572 (Protocol Tunneling) both exploit the assumption that port-based filtering is sufficient.

The **DMZ (Demilitarized Zone)** architecture places public-facing servers, web servers, email gateways, VPN concentrators, in a network zone that is partially protected from both the internet and the internal corporate network. A two-firewall DMZ design uses one firewall between the internet and the DMZ, and a second between the DMZ and the internal network. This means that an attacker who compromises a public-facing server gains a foothold in the DMZ but still faces a second firewall before reaching internal systems. The 2020 SolarWinds supply chain attack demonstrated the importance of DMZ architecture: once the SUNBURST backdoor was active on internal systems, it communicated outbound through the corporate firewall to C2 infrastructure, highlighting the importance of egress filtering, which many organizations neglect compared to ingress filtering.

NIST SP 800-41 (Guidelines on Firewalls and Firewall Policy) provides comprehensive guidance on firewall architecture, rule management, and testing. CIS Control 12 (Network Infrastructure Management) and CIS Control 13 (Network Monitoring and Defense) specify hardening requirements for firewall configurations. Key recommendations include: implementing a default-deny baseline, documenting every firewall rule with a business justification, reviewing rules quarterly to remove stale permit entries, and logging all dropped connections to a centralized SIEM for anomaly detection.

Firewall rule analysis asks of each rule: does it achieve the intended goal, is it broader than necessary, does it conflict with another rule, and what does the implicit deny at the end catch. This is a core practical skill for both defensive and assessment work.
:::

%%%

---
unit: Infrastructure
code: VPN
title: VPNs, Virtual Private Networks
---
:::callout style=soft
A **VPN (Virtual Private Network)** creates an encrypted, authenticated tunnel over a public network (typically the internet), allowing remote users or branch offices to communicate securely as if they were directly connected to a private network.
:::

::::columns
::col::
:::list heading="VPN Types" style=plain
- **Remote Access VPN**, Individual users connect from untrusted networks (home, hotel Wi-Fi) to the corporate network; client software establishes an encrypted tunnel to a VPN concentrator
- **Site-to-Site VPN**, Connects two entire networks (e.g., headquarters and branch office) through a permanent encrypted tunnel between routers or firewalls
- **Split Tunneling**, Only traffic destined for corporate resources routes through the VPN; other traffic goes directly to the internet; reduces VPN load but may expose corporate data
- **Full Tunneling**, All traffic routes through VPN; ensures corporate inspection and logging of all user activity; increases VPN load
:::
::col::
:::table
| VPN Protocol | Port | Encryption | Notes |
|---|---|---|---|
| OpenVPN | 1194/UDP or 443/TCP | TLS (AES-256) | Open source; highly configurable; widely trusted |
| WireGuard | 51820/UDP | ChaCha20-Poly1305 | Modern; very fast; small codebase (~4,000 lines) |
| IKEv2/IPsec | 500, 4500/UDP | AES-256-GCM | Native on iOS/Windows; strong security |
| L2TP/IPsec | 1701/UDP | AES (via IPsec) | Legacy; slower; L2TP alone provides no encryption |
| PPTP | 1723/TCP | MPPE (RC4) | Deprecated; broken encryption; avoid completely |
| SSL/TLS VPN | 443/TCP | TLS 1.2/1.3 | Browser-based or client; traverses most firewalls |
:::
::::

:::callout style=line
**Security Note:** VPNs authenticate the tunnel endpoint, not the individual user's device posture. A compromised device connected via VPN brings that compromise inside the network perimeter. NIST SP 800-207 (Zero Trust Architecture) recommends supplementing or replacing VPN with identity-aware proxies that evaluate device health, user identity, and context before granting access to individual resources, not blanket network access.
:::

:::code language=mermaid caption="A VPN tunnel encrypts traffic between the client and concentrator but does not protect against a compromised endpoint device, the tunnel brings whatever is on the device inside the network perimeter"
flowchart LR
  L["Remote laptop"] ==>|"encrypted tunnel (IPsec or TLS)"| C["VPN concentrator"]
  C --> S["Internal servers"]
  L -.->|"split tunnel: other traffic goes direct"| I["Internet"]
  C -->|"full tunnel: all traffic via company"| I
:::

:::notes
Virtual Private Networks (VPNs) emerged in the late 1990s as enterprises needed to provide secure remote access over the public internet without the cost of dedicated leased lines. The concept is straightforward: encapsulate network traffic inside an encrypted tunnel so that even though the underlying transport is a shared, untrusted public network, the payload is protected from eavesdropping and tampering in transit.

Early VPN protocols like PPTP (Point-to-Point Tunneling Protocol) and L2TP/IPsec have significant cryptographic weaknesses. PPTP's MS-CHAPv2 authentication is broken (CVE-2012-2690) and its MPPE encryption using RC4 provides weak confidentiality. PPTP should never be used for any security-sensitive application. L2TP provides no encryption by itself and relies on IPsec for security; when properly configured with AES-256, it is acceptable but slower than modern alternatives.

Modern VPN protocols provide strong security. **IPsec (Internet Protocol Security)**, standardized in RFC 4301-4309, operates at the Network Layer and can encrypt either individual IP datagrams (transport mode) or entire IP packets within new IP datagrams (tunnel mode). IKEv2 (Internet Key Exchange version 2, RFC 7296) provides fast session establishment and supports MOBIKE (mobility and multihoming), making it well-suited for mobile devices that change network connections. **OpenVPN** uses TLS for both key exchange and data encryption, benefits from decades of TLS security research, and is highly configurable. **WireGuard**, designed from scratch with modern cryptographic principles (ChaCha20 for encryption, Poly1305 for authentication, Curve25519 for key exchange), achieves better performance than IPsec with a dramatically smaller codebase, reducing the attack surface inherent in complex implementations.

From a security operations perspective, VPNs create both defensive capabilities and new risks. On the defensive side, they prevent eavesdropping on remote connections, provide authentication of the tunnel endpoints, and can route remote traffic through corporate inspection infrastructure (intrusion detection, DLP, proxy filtering). On the risk side, VPN concentrators are attractive, high-value targets for attackers: a vulnerability in the concentrator (e.g., CVE-2019-11510, the Pulse Secure VPN authentication bypass that exposed credentials of tens of thousands of organizations) can provide direct access to the corporate network without requiring any end-user interaction or credential theft. The 2021 Colonial Pipeline ransomware attack exploited compromised VPN credentials for initial access. VPN infrastructure must be patched aggressively and monitored for authentication anomalies.

**Split tunneling** deserves specific security attention. When split tunneling is enabled, only traffic destined for corporate subnets routes through the VPN; other traffic (e.g., general web browsing, streaming) goes directly to the internet. This reduces VPN bandwidth but creates a risk: if the remote device is compromised, the attacker on that device can reach both the internet and, through the VPN, the corporate network, using the compromised device as a bridge. Full tunneling avoids this by routing all traffic through corporate inspection, at the cost of increased VPN load and potentially slower browsing for remote users.

NIST SP 800-77 (Guide to IPsec VPNs) and NIST SP 800-113 (Guide to SSL VPNs) provide implementation guidance. NIST SP 800-207 (Zero Trust Architecture) argues that the VPN model itself is architecturally flawed for modern environments because it grants overly broad network access, a user authenticated to the VPN can typically reach any system on the corporate network, not just the specific systems they need. Zero Trust replaces this with per-resource access decisions based on user identity, device health, and context.

Once a VPN tunnel is established, an on-path observer sees only encrypted packets to the VPN concentrator, with no visible application content. This is what encryption in transit means at the network level.
:::

%%%

---
unit: Tools
code: WRK
title: Tool Spotlight, Wireshark for Packet Analysis
---
:::callout style=soft
**Wireshark** is the world's most widely used open-source network protocol analyzer. It captures live packets from network interfaces and displays them in a human-readable, richly annotated format, enabling deep analysis of network traffic for troubleshooting, forensics, and security research.
:::

::::columns
::col::
:::list heading="Key Wireshark Capabilities" style=plain
- Live packet capture from physical and virtual interfaces
- Deep protocol dissection, supports 3,000+ protocols
- Powerful display filters (`http`, `tcp.port == 443`, `ip.src == 10.0.0.1`)
- Follow TCP/UDP stream to reconstruct conversations
- Export captured objects (files, images transmitted over HTTP)
- Statistics and I/O graphs for traffic analysis
- Reads/writes standard PCAP and PCAPng file formats
:::
::col::
:::table
| Common Filter | What It Shows |
|---|---|
| `arp` | All ARP request and reply traffic |
| `dns` | All DNS queries and responses |
| `http` | Unencrypted HTTP traffic (can see content) |
| `tcp.flags.syn == 1` | All TCP SYN packets (new connection attempts) |
| `ip.src == 192.168.1.5` | All traffic originating from a specific host |
| `tcp.port == 443` | HTTPS traffic (encrypted; headers visible, payload not) |
| `icmp` | All ICMP messages (ping, traceroute, unreachable) |
| `!(arp or dns)` | Exclude ARP and DNS to reduce noise |
:::
::::

:::notes
Wireshark (originally named Ethereal, renamed in 2006) was created by Gerald Combs in 1998 and has grown into the reference-standard tool for network protocol analysis. It is available on Windows, macOS, and Linux and is used by network engineers, security analysts, malware researchers, protocol developers, and students worldwide. Its power lies in its protocol dissectors, parsing engines that decode the fields of a captured frame at every layer and present them in a structured, labeled tree that maps directly to the relevant RFC specifications.

To capture traffic, Wireshark uses the **libpcap** library (on Linux/macOS) or **WinPcap/Npcap** (on Windows) to place a network interface into **promiscuous mode**, a state in which the NIC passes all received frames to the OS, regardless of whether the destination MAC matches the local address. On a switched network, promiscuous mode allows a capture device to see all traffic sent to its own MAC address plus all broadcast and multicast frames, but generally not unicast traffic destined for other hosts (unlike a hub environment). To capture all traffic on a switched segment, defenders use a **port mirror/SPAN (Switched Port Analyzer)** configuration on the switch that duplicates all frames from a target port or VLAN to the capture port, or they insert a passive network tap.

The **display filter** syntax is one of Wireshark's most powerful features. Filters can reference any field from any protocol dissector, combined with logical operators (and, or, not), comparison operators, and field existence tests. For example, `http.request.method == "POST" and ip.dst == 10.0.0.5` shows only HTTP POST requests sent to a specific server, immediately relevant when investigating suspected credential exfiltration. The `Follow TCP Stream` feature reconstructs the complete bidirectional content of a TCP connection (useful for reading HTTP conversations, SMTP sessions, or FTP transfers in plaintext) from the fragmented packet sequence.

Wireshark is an indispensable tool for learning networking because it makes protocol fields directly visible. Students who struggle with the abstract description of TCP's three-way handshake immediately understand it upon seeing SYN, SYN-ACK, and ACK packets in the capture with their sequence and acknowledgment numbers displayed. Similarly, DNS's hierarchical resolution process becomes concrete when students see the actual QUERY and RESPONSE messages, the TTL values in answers, and the authoritative flag.

From a security investigation standpoint, Wireshark is used for: incident response (reconstructing attack timelines from PCAP evidence); malware analysis (identifying C2 protocols, data exfiltration patterns, and lateral movement techniques from infected host captures); penetration testing (verifying that protocols are unencrypted where encryption is required, capturing credentials over Telnet or HTTP); and forensic analysis (recovering files transmitted over HTTP or FTP from PCAP captures using File → Export Objects). CVE-2014-0160 (Heartbleed) was validated using Wireshark: researchers could capture the heartbeat request and subsequent response and literally see private key material in the response payload when the vulnerability was present.

Legal and ethical note: capturing network traffic without authorization is illegal in most jurisdictions under laws such as the U.S. Computer Fraud and Abuse Act (CFAA, 18 U.S.C. § 1030) and the UK Computer Misuse Act. Wireshark should only be used on networks where you have explicit authorization, your own lab environment, a dedicated classroom network, or a network you are authorized to test. Unauthorized packet capture, even passively, can constitute a criminal offense.

Over plain HTTP, the full conversation, request headers, response headers and HTML body, travels in cleartext and is readable by anyone on the path. Over HTTPS the same payload is indistinguishable ciphertext. The contrast is the clearest demonstration of why HTTPS matters.
:::

%%%

---
unit: Tools
code: NMP
title: Tool Spotlight, Nmap for Network Scanning
---
:::callout style=soft
**Nmap (Network Mapper)** is an open-source tool for network discovery and security auditing. It uses raw IP packets to determine which hosts are on a network, what services those hosts are running, what operating systems they use, and whether known vulnerabilities are present.
:::

::::columns
::col::
:::list heading="Common Nmap Scan Types" style=plain
- **`-sn` (Ping Scan)**, Discovers live hosts without port scanning; uses ICMP echo, TCP SYN/ACK, ARP
- **`-sS` (SYN Scan / Stealth Scan)**, Sends SYN, records SYN-ACK (open) or RST (closed); never completes handshake; harder to detect in application logs
- **`-sV` (Version Detection)**, Probes open ports to determine service and version (e.g., "Apache httpd 2.4.51")
- **`-O` (OS Detection)**, Analyzes TCP/IP stack behavior (TTL, window size, etc.) to fingerprint the OS
- **`-A` (Aggressive)**, Combines `-sV`, `-O`, traceroute, and NSE scripts
- **`--script vuln`**, Runs NSE vulnerability detection scripts against open services
:::
::col::
:::table
| Port State | Meaning | Nmap Detection Method |
|---|---|---|
| Open | Application is accepting connections | Received SYN-ACK (TCP) or valid UDP response |
| Closed | Port reachable but no application listening | Received RST (TCP) or ICMP Port Unreachable (UDP) |
| Filtered | Firewall or filter is blocking the probe | No response received; packet dropped silently |
| Open/Filtered | Cannot distinguish between open and filtered | Common with UDP scans |
:::
::::

:::notes
Nmap was created by Gordon Lyon (known online as Fyodor) in 1997 and published in Phrack magazine before becoming one of the most widely used security tools in existence. It is available on all major platforms, included in most Linux distributions, and is a staple of penetration testing, vulnerability assessment, and network inventory work. Nmap's Scripting Engine (NSE) extends its capabilities far beyond simple port scanning, with hundreds of community-contributed scripts for vulnerability detection, brute-force authentication testing, service enumeration, and exploitation assistance.

At its core, Nmap performs **host discovery** (determining which IP addresses are responding on the network) and **port scanning** (determining which ports on a discovered host are open, closed, or filtered). The default SYN scan (`-sS`) is preferred over the older connect scan (`-sT`) because it never completes the TCP three-way handshake: Nmap sends a SYN, waits for the response, and sends a RST rather than the final ACK. This means the connection is never fully established, application-level logs on the target may not record the probe, and the scan completes faster. However, network-level IDS/IPS systems (and modern endpoint detection) will detect SYN scans, the notion of "stealth" refers only to application log evasion, not to evading network monitoring.

**Service version detection** (`-sV`) is particularly security-relevant: by sending carefully crafted probe packets to open ports and analyzing the responses against a database of service signatures, Nmap can often identify not just the service (e.g., SSH) but its specific version (e.g., OpenSSH 7.4). This version information is directly actionable for an attacker: a quick search of the NVD (National Vulnerability Database at nvd.nist.gov) or CVE databases can reveal whether that specific version has known exploitable vulnerabilities. CVE-2016-10009, CVE-2018-15473, and dozens of other OpenSSH CVEs have specific version ranges that Nmap's version detection output immediately maps to exploitable conditions.

**OS fingerprinting** (`-O`) works by analyzing subtle differences in TCP/IP stack implementations across operating systems, values like the initial TTL, TCP window size, IP ID sequence behavior, and responses to unusual flag combinations all vary between Windows, Linux, macOS, and embedded systems. These differences are catalogued in Nmap's OS fingerprint database (nmap-os-db). While imperfect, OS detection is often accurate enough to narrow the choice of exploits significantly: a Windows 10 host requires different attack paths than an embedded Linux device.

Nmap's use is governed by both legal and ethical considerations. Running an Nmap scan against systems without authorization is illegal under the CFAA and equivalent laws in most jurisdictions. Even scanning one's own network without notifying system owners can cause disruptions, particularly SYN scans on production systems, which can fill connection tables and cause temporary service degradation. Penetration testers and security teams must operate under explicit written authorization (a signed penetration testing agreement or management authorization memo) that specifies the scope of permitted scanning. Nmap reconnaissance maps directly to MITRE ATT&CK T1046 (Network Service Scanning) and T1595 (Active Scanning), which are initial reconnaissance techniques used by threat actors before exploitation.

From a defensive perspective, Nmap scans against your own infrastructure are a valuable component of continuous vulnerability management. Running periodic Nmap sweeps and comparing results against expected baselines reveals unexpected open ports (rogue services, misconfigured firewall rules), unauthorized hosts, and service version drift (a service that should have been patched but wasn't). NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment) recommends port scanning as part of a regular security assessment program.

A port scan that reports open ports with service versions and an OS guess is the reconnaissance step of an attack: each version maps to known CVEs, which an attacker uses to choose an exploit. The same scan run defensively finds unexpected open ports before an attacker does.
:::

%%%

---
unit: Synthesis
code: ATK
title: Common Network Attack Categories
---
:::callout style=soft
Every network attack exploits a specific protocol behavior, misimplementation, or misconfiguration at a specific layer of the TCP/IP stack. Understanding attack categories by layer allows defenders to apply the right detection and mitigation at the right point.
:::

:::table
| Attack Category | Example Attacks | Target Layer | Mitigation Principles |
|---|---|---|---|
| Reconnaissance | Nmap scan, ping sweep, traceroute | All layers (passive) | IDS/IPS detection; rate limiting; RFC 2827 ingress filtering |
| Spoofing | IP spoofing, ARP spoofing, DNS spoofing | L2, L3, L7 | BCP 38 ingress filtering; DAI; DNSSEC |
| Denial of Service | SYN flood, ICMP flood, UDP amplification, volumetric DDoS | L3, L4 | SYN cookies; rate limiting; DDoS scrubbing services |
| Man-in-the-Middle | ARP poisoning, rogue DHCP, SSL stripping | L2, L3, L7 | 802.1X; HSTS; TLS certificate pinning; DAI; DHCP Snooping |
| Eavesdropping | Passive packet capture, Wi-Fi sniffing | L1, L2 | Encryption (TLS, IPsec, WPA3); port security; 802.1X |
| Session Hijacking | TCP RST injection, cookie theft, session fixation | L4, L7 | Random ISNs; HTTPS; HttpOnly/Secure cookie flags |
| Lateral Movement | SMB exploits, RDP brute force, pass-the-hash | L4, L7 | Network segmentation; firewall ACLs; MITRE ATT&CK defenses |
| Exfiltration | DNS tunneling, HTTPS C2, ICMP tunneling | L3, L4, L7 | Egress filtering; DLP; DNS monitoring; TLS inspection |
:::

::::columns
::col::
:::callout style=soft
**MITRE ATT&CK alignment:** The MITRE ATT&CK framework maps adversary techniques to network protocols. Key network tactics: Reconnaissance (TA0043), Initial Access (TA0001), Lateral Movement (TA0008), Command and Control (TA0011), Exfiltration (TA0010). Each technique ID links to detection analytics and mitigation guidance.
:::
::col::
:::list heading="Principle: Every Attack Is a Protocol Abuse" style=plain
- ARP spoofing abuses ARP's lack of authentication
- SYN flood abuses TCP's stateful handshake
- DNS cache poisoning abuses DNS's lack of response validation
- VLAN hopping abuses 802.1Q native VLAN behavior
- BGP hijacking abuses BGP's trust model between autonomous systems
- The pattern: find a protocol with no authentication or no integrity check → forge or flood it
:::
::::

:::code language=mermaid caption="Network attacks map precisely to protocol layers, knowing the layer tells you which protocol is being abused and which defensive control addresses the root cause"
flowchart TB
  A["<b>Application</b><br/>DNS spoofing, phishing, session hijacking, SSL stripping (MITM)"]
  T["<b>Transport</b><br/>SYN flood, port scanning"]
  N["<b>Internet</b><br/>IP spoofing, ICMP floods, BGP hijacking"]
  L["<b>Network Access</b><br/>sniffing, ARP spoofing (MITM), MAC flooding, rogue APs"]
  A --- T --- N --- L
:::

:::notes
Understanding network attacks requires recognizing that every attack is, at its core, an exploitation of a specific protocol's design limitations, implementation flaws, or misconfiguration. The designers of most internet protocols prioritized functionality, performance, and interoperability over security, partly because the internet was originally a research network with trusted participants, and partly because adding security mechanisms to protocols increases complexity and reduces performance. The security industry has spent decades layering compensating controls on top of fundamentally insecure protocol foundations.

**Reconnaissance** attacks gather information about a target network without directly exploiting it. Passive reconnaissance captures traffic that is already flowing (no packets sent to the target, very difficult to detect) while active reconnaissance, like Nmap scanning, generates traffic that appears in firewall and IDS logs. MITRE ATT&CK TA0043 (Reconnaissance) covers both categories and maps to specific techniques such as T1595 (Active Scanning) and T1590 (Gather Victim Network Information). Defenders detect active reconnaissance through IDS signatures and anomaly detection on firewall logs.

**Spoofing attacks** forge source addresses or identifiers to impersonate trusted parties. IP spoofing (RFC 2827/BCP 38 recommends ingress filtering at network boundaries to block packets with source addresses that cannot legitimately originate from the ingress direction) enables DoS amplification by making reflection attacks appear to come from the victim. ARP spoofing exploits the authenticated nature of ARP. DNS spoofing exploits the historically unauthenticated nature of DNS responses. Each has its own protocol-layer countermeasure: BCP 38 for IP spoofing, DAI for ARP spoofing, DNSSEC for DNS spoofing.

**Denial of Service (DoS) and Distributed DoS (DDoS)** attacks seek to make a service unavailable by exhausting resources, connection table entries (SYN flood), bandwidth (volumetric DDoS), processing capacity (application-layer DDoS targeting expensive operations like database queries), or memory. The 2018 GitHub DDoS attack peaked at 1.35 Tbps, the largest ever recorded at the time, using memcached UDP amplification (CVE-2018-1000115) to achieve an amplification factor of approximately 51,000x. The 2020 AWS DDoS attack peaked at 2.3 Tbps. Mitigation requires a combination of traffic scrubbing infrastructure (cloud-based DDoS protection services), anycast routing to distribute attack traffic, rate limiting, and SYN cookies.

**Man-in-the-Middle (MITM)** attacks position the attacker between two legitimate communicating parties, enabling passive eavesdropping or active manipulation of traffic. The attacker must defeat both the routing/addressing that would normally direct traffic between the parties (achieved via ARP spoofing, rogue DHCP, or BGP hijacking) and any encryption or authentication that would reveal the interposition (attempted via SSL stripping, downgrading HTTPS to HTTP, or presenting a fraudulent certificate). Countermeasures include HSTS (HTTP Strict Transport Security), which prevents SSL stripping by instructing browsers to always use HTTPS; certificate transparency and certificate pinning, which detect fraudulent certificates; and 802.1X network access control, which prevents rogue devices from connecting to the network in the first place.

The MITRE ATT&CK framework provides the most comprehensive taxonomy of network attack techniques, with detailed descriptions, detection analytics, and mitigation guidance for each technique. Security operations teams use ATT&CK to structure their detection coverage analysis: "Which of these techniques do we have detections for? Which have no visibility?" This gap analysis directly prioritizes defensive investment.

Working backward from an effect, for example "web traffic through a floor switch is being intercepted", to the protocol abused, the OSI layer and the confirming forensic evidence (anomalous ARP cache entries, gratuitous ARP packets, traffic to an unexpected MAC) is the analytic habit of incident response.
:::

%%%

---
unit: Synthesis
code: MCN
title: Common Misconceptions About Network Security
---
:::callout style=soft
Network security is full of well-intentioned but incorrect assumptions. These misconceptions lead to misplaced defenses, wasted resources, and dangerous false confidence. Let's address the most common ones directly.
:::

:::table
| Misconception | Reality | Correct Approach |
|---|---|---|
| "NAT protects us from the internet" | NAT translates addresses; it does not inspect, authenticate, or block malicious traffic | Deploy a real stateful firewall; NAT is not a security control |
| "We have a firewall, so we're secure" | Firewalls enforce port-based rules; modern attacks use permitted ports (80/443) and encrypted channels | Layer with IDS/IPS, WAF, EDR, and TLS inspection |
| "Internal traffic is trusted" | Most breaches involve lateral movement across internal networks after initial compromise | Apply Zero Trust: verify every connection regardless of source |
| "Disabling ICMP makes us invisible" | Attackers use TCP/UDP probes, not just ping; disabling ICMP breaks PMTUD and troubleshooting | Selectively filter ICMP types instead of blanket blocking |
| "VLANs provide complete isolation" | VLAN hopping attacks can bypass isolation if native VLANs are misconfigured | Proper 802.1Q configuration + inter-VLAN firewall rules required |
| "Our private IPs are hidden" | Misconfigurations and OSINT regularly expose internal addressing in DNS, error messages, and headers | Treat internal network information as sensitive; suppress in error messages |
| "HTTPS means the site is safe" | HTTPS means the connection is encrypted, not that the server or content is trustworthy | Phishing sites routinely use HTTPS; validate the certificate owner, not just the padlock |
| "Complexity equals security" | Unnecessary complexity increases attack surface; attackers exploit what defenders forget exists | Minimize, document, and audit, simplicity enables security |
:::

:::notes
One of the most valuable things an introductory network security course can do is dismantle harmful misconceptions before they become deeply embedded beliefs that inform future decisions. Each of the misconceptions in this slide has contributed to real-world security failures, some at enormous scale.

**"NAT protects us"** is perhaps the most persistent and dangerous misconception. Network Address Translation, as defined in RFC 3022, performs address substitution to conserve IPv4 addresses. It has the incidental effect of making internal hosts unreachable from the internet without an explicit port-forwarding rule, which creates an illusion of protection. However, NAT does nothing to inspect the content of permitted connections, authenticate traffic sources, block malware downloading over permitted ports, or prevent outbound C2 communication. An attacker who tricks an internal user into running malware bypasses NAT entirely because the malicious connection is initiated from inside, flowing outbound through the NAT router. Treating NAT as a security boundary has led organizations to deprioritize internal network security, a decision that has proven catastrophic in breach scenarios.

**"Our firewall means we're secure"** conflates the presence of a security control with actual security. Traditional firewalls operate on the assumption that port 443 carries legitimate HTTPS traffic, and they permit it. Modern malware routinely uses port 443 (and sometimes port 80) for C2 communication, wrapped in legitimate-looking TLS sessions. Without TLS inspection (which requires terminating and re-inspecting encrypted sessions), a firewall is blind to the content of this traffic and cannot distinguish legitimate HTTPS from malware C2. The CrowdStrike 2023 Global Threat Report noted that 80%+ of malware C2 communications observed in the wild use encrypted channels on common ports.

**"Internal traffic is trusted"** was the architectural assumption of early enterprise networks, the "hard shell, soft inside" (or "castle and moat") security model. The 2020 SolarWinds attack demonstrated definitively that this model is broken: the SUNBURST backdoor operated entirely within the trusted internal network, using legitimate-looking DNS requests and HTTP traffic to communicate with C2 infrastructure. Once an attacker establishes a foothold inside the perimeter (through phishing, supply chain compromise, or any other initial access technique), a flat, unsegmented, mutually trusting internal network provides no resistance to lateral movement. NIST SP 800-207 (Zero Trust Architecture) was published specifically to provide a framework for replacing the implicit-trust model with per-connection verification.

**"Disabling ICMP makes us invisible"** is a security-through-obscurity measure that causes real operational problems. ICMP Type 3 (Destination Unreachable) Code 4 messages are required for Path MTU Discovery (RFC 1191), which allows TCP to discover the maximum packet size that can traverse the path without fragmentation. Blocking these messages causes TCP connections to experience mysterious hangs when path MTU is smaller than the default segment size, a symptom known as the "black hole" problem. Attackers who want to discover hosts use TCP SYN probes, UDP probes, and many other techniques that work regardless of ICMP filtering. The correct approach is selective ICMP filtering: permit operationally required types, block those with no legitimate operational use (such as inbound Echo Requests from untrusted networks).

**"HTTPS means the site is safe"** has been actively made worse by browser UI changes. Modern browsers display a padlock icon for any HTTPS connection, regardless of whether the certificate owner is a legitimate organization or a phisher who obtained a free certificate from Let's Encrypt for their phishing domain. Google Safe Browsing data shows that a significant and growing proportion of phishing sites use HTTPS. The padlock means the connection is encrypted and the certificate is valid, it says nothing about the legitimacy of the entity on the other end.

Many students arrive holding several network security misconceptions absorbed from consumer media and from IT practice that has not kept pace with the threat landscape; naming each one explicitly is what displaces it.
:::

%%%

---
unit: Synthesis
code: CHK
title: Mid-Lecture Checkpoint, Test Your Understanding
---
:::callout style=soft
Pause here. Before moving to advanced topics, verify that the foundational concepts are solid. Answer these questions without referring to your notes, then check your answers.
:::

::::columns
::col::
:::list heading="Concept Check Questions" style=plain
- Q1. A packet arrives at a router with TTL=1. What happens, and what protocol message is sent back to the sender?
- Q2. You run `nmap -sS 192.168.1.50` and port 22 shows as "filtered." What does this tell you about the network path to that host?
- Q3. Your organization uses 192.168.10.0/27 for a server subnet. How many usable host addresses does this subnet support?
- Q4. A host ARP cache shows that the gateway IP (192.168.1.1) maps to an unexpected MAC address that belongs to another workstation on the segment. What attack is likely occurring?
- Q5. A web server on port 443 shows "open" in an Nmap scan. A colleague says "so we can see the HTTPS traffic in Wireshark." What is the error in this reasoning?
- Q6. You observe many DNS queries from an internal host for subdomains like `aGVsbG8gd29ybGQ=.evil.com` with base64-encoded characters. What is the likely attack technique?
:::
::col::
:::list heading="Answer Key" style=plain
- A1. TTL=0 at the router → router drops packet → sends ICMP Type 11 (Time Exceeded) back to source. Traceroute exploits exactly this behavior.
- A2. A firewall or filtering device is silently dropping SYN probes to port 22 before they reach the host. The host may be running SSH or not, you cannot tell from a filtered result.
- A3. /27 = 32 addresses total; 32 − 2 = **30 usable host addresses** (network address and broadcast reserved).
- A4. Likely **ARP spoofing / ARP cache poisoning**. The attacker is redirecting gateway-bound traffic through their workstation for MITM interception.
- A5. Port 443 open confirms the port is reachable, but TLS encryption means the **payload is encrypted**. Wireshark can capture the frames but cannot decrypt the application content without the private key or a session key log.
- A6. **DNS tunneling** / C2 over DNS. Base64-encoded subdomains are a classic indicator of data exfiltration or C2 communication encoded in DNS query fields.
:::
::::

:::notes
This checkpoint slide serves a pedagogical function that is often undervalued in technical training: it creates a structured moment for students to test their own understanding before the material becomes more complex. Research on learning (Roediger & Karpicke, 2006, "Test-Enhanced Learning") consistently shows that retrieval practice, actively trying to recall information rather than passively re-reading it, is one of the most effective techniques for long-term retention and transfer. By pausing here and requiring students to answer questions without notes, we activate retrieval practice on exactly the concepts that subsequent advanced material depends upon.

Each question in this checkpoint is designed to test applied understanding rather than rote memorization. Question 1 targets understanding of TTL mechanics and ICMP, essential for interpreting Wireshark captures and traceroute output. Question 2 requires students to reason about what "filtered" means in the context of a network path with a firewall, distinguishing between a closed port (RST received) and a filtered port (no response). Many students incorrectly conclude that a filtered port means the service is not running; understanding that it means a firewall is silently dropping probes is essential for accurate attack surface assessment.

Question 3 tests basic subnetting arithmetic, the ability to quickly calculate usable hosts from a CIDR prefix is a practical skill used daily in firewall rule analysis, network design, and incident response. A /27 gives 2^5 = 32 addresses; minus the network address and broadcast address leaves 30 usable hosts. Question 4 bridges knowledge of ARP protocol mechanics to attack identification, the unexpected MAC-to-IP mapping in the ARP cache is the classic forensic indicator of ARP spoofing, and recognizing it quickly can prevent a MITM attack from lasting long enough to cause significant harm.

Question 5 addresses a very common misconception: the confusion between "port is open" (a connectivity fact about the network) and "we can read the traffic" (a question about encryption). HTTPS on port 443 is encrypted with TLS; Wireshark captures the frames but displays them as encrypted payload that is unreadable without the private key or pre-master secret logging. This distinction is critical when investigating incidents: capturing HTTPS traffic is possible; reading its content requires either TLS inspection infrastructure or obtaining the session keys.

Question 6 brings together DNS protocol knowledge and threat intelligence: base64-encoded subdomains of unusual length appearing in high volumes from a single internal host are a high-fidelity indicator of DNS tunneling. Tools like dnscat2 and iodine encode data in precisely this way. Detection requires monitoring DNS query entropy, subdomain length distribution, and query volume per client, behavioral analytics that go beyond simple domain blocklisting.

:::

%%%

---
unit: Synthesis
code: FRM
title: Network Security Framework Summary
---
:::callout style=soft
The frameworks governing network security are not independent checklists, they are complementary lenses that, together, define a comprehensive approach to protecting networked systems at technical, operational, and governance levels.
:::

:::table
| Framework | Scope | Key Network Security Relevance | Published By |
|---|---|---|---|
| NIST SP 800-53 | Federal information systems (broadly adopted) | SC-7 (Boundary protection), SC-8 (Transmission confidentiality), AC-17 (Remote access), SI-3 (Malicious code) | NIST |
| NIST CSF 2.0 | Risk-based cybersecurity program | Protect (PR.AC network access control, PR.PT protective technologies), Detect (DE.CM continuous monitoring) | NIST |
| NIST SP 800-207 | Zero Trust Architecture | Eliminate implicit network trust; verify every connection; micro-segmentation | NIST |
| ISO/IEC 27033 | Network security architecture | Six-part standard: concepts, guidelines, scenarios, securing inter-network communications, VPNs, IP convergence | ISO/IEC |
| ISO/IEC 27001 | Information security management system | Annex A Controls: A.8.20 (Network security), A.8.21 (Security of network services), A.8.22 (Segregation of networks) | ISO/IEC |
| CIS Controls v8 | Prioritized cyber hygiene | Control 12 (Network infrastructure management), Control 13 (Network monitoring and defense) | CIS |
| MITRE ATT&CK | Adversary behavior taxonomy | Network-based techniques across Reconnaissance, Initial Access, Lateral Movement, C2, Exfiltration tactics | MITRE |
| PCI-DSS v4.0 | Payment card industry | Requirements 1 (Network controls), 4 (Encryption in transit), 6 (Secure systems and software) | PCI SSC |
:::

::::columns
::col::
:::callout style=soft
**How these frameworks relate:** NIST CSF provides the "what" (identify, protect, detect, respond, recover). NIST SP 800-53 provides the "how" (specific technical controls). MITRE ATT&CK provides the "against what" (attacker techniques). CIS Controls provide a prioritized starting point. ISO standards provide the governance structure for making it all repeatable and auditable.
:::
::col::
:::list heading="Framework Selection Guidance" style=plain
- **US Federal agencies**, NIST SP 800-53 is mandatory (FISMA)
- **All organizations**, NIST CSF 2.0 for risk-based program management
- **Global or multinational**, ISO/IEC 27001/27033 for internationally recognized certification
- **Payment card environments**, PCI-DSS is contractually mandatory
- **OT/ICS environments**, IEC 62443 + NIST SP 800-82
- **Any organization**, CIS Controls as implementation prioritization guide
:::
::::

:::code language=mermaid caption="Security frameworks are not alternatives but complements: CSF governs the program, 800-53/ISO 27001 specify the controls, CIS Controls prioritize implementation, and ATT&CK maps controls to real adversary techniques"
flowchart TB
  G["<b>Governance</b><br/>NIST CSF: what outcomes to achieve"]
  C["<b>Control specification</b><br/>NIST SP 800-53, ISO 27001: which controls"]
  I["<b>Implementation and threat focus</b><br/>CIS Controls: priorities<br/>MITRE ATT&CK: what attackers actually do"]
  G --> C --> I
  I -->|"gaps feed back"| G
:::

:::notes
The landscape of cybersecurity frameworks can be overwhelming, there are dozens of standards, guidelines, and regulatory mandates, and organizations are often required to comply with multiple simultaneously. Understanding how these frameworks relate to each other and to practical network security is essential for both practitioners who implement controls and governance professionals who audit and certify compliance.

The **NIST Cybersecurity Framework (CSF)**, originally published in 2014 and significantly updated to version 2.0 in 2024, is a risk-based framework that organizes security activities into six functions: Identify, Protect, Detect, Respond, Recover, and (new in 2.0) Govern. It is intentionally non-prescriptive, it tells organizations what to achieve (maintain an inventory of network assets; protect data in transit; detect anomalous network activity) without specifying exactly how. This flexibility makes it applicable across industries and organization sizes, from small businesses to large federal agencies.

**NIST SP 800-53** is the prescriptive companion to the CSF for federal information systems, providing a catalog of security and privacy controls organized into 20 families. Controls directly relevant to network security include SC-7 (Boundary Protection, define network boundaries and control traffic flows), SC-8 (Transmission Confidentiality and Integrity, protect data in transit using encryption), SC-5 (Denial-of-Service Protection), AC-17 (Remote Access, secure VPN and remote desktop configurations), and SI-3 (Malicious Code Protection, deploy endpoint protection on network-connected devices). Under FISMA (Federal Information Security Modernization Act), federal agencies and their contractors are legally required to implement appropriate SP 800-53 controls based on system categorization (Low, Moderate, High impact per FIPS 199).

**ISO/IEC 27001** and its companion standards (27002 for controls, 27033 for network security, 27035 for incident response) provide an internationally recognized certification framework. Organizations that achieve ISO 27001 certification demonstrate to customers, partners, and regulators that they have implemented a systematic Information Security Management System (ISMS) with documented policies, risk assessments, control implementations, and continuous improvement processes. ISO/IEC 27033 specifically addresses network security architecture across six parts, including securing inter-network communications, VPN implementations, and network design for specific scenarios.

**CIS Controls v8** takes a different approach: rather than comprehensive coverage, it provides 18 prioritized controls (organized into Implementation Groups, IG1 for essential hygiene, IG2 for standard enterprise, IG3 for advanced) that have been empirically shown to prevent the majority of common attacks. For network security, CIS Control 12 (Network Infrastructure Management, manage and harden network devices) and Control 13 (Network Monitoring and Defense, monitor network traffic and deploy detection capabilities) are directly applicable. The CIS Benchmarks, which accompany the Controls, provide specific, vendor-verified configuration settings for routers, switches, firewalls, and operating systems.

**MITRE ATT&CK** plays a unique role: it is not a compliance framework but a threat intelligence taxonomy that maps real adversary behaviors to detectable techniques. Security teams use ATT&CK to assess their detection coverage, "For each of these 200+ network-relevant techniques, do we have a detection in place? If not, which ones are most likely to be used against us based on the threat actors targeting our industry?" This adversary-centric perspective is what transforms a compliance exercise into actual security improvement.

For students entering the cybersecurity field, familiarity with all of these frameworks, at least at the conceptual level, is expected by employers. Security+, CISSP, and CISM certification exams all test framework knowledge. More importantly, the ability to map a technical control (such as "deploy DHCP Snooping on all access layer switches") to a specific framework requirement (CIS Control 12.2; NIST SP 800-53 SC-7(10); PCI-DSS Requirement 1.3.2) is the skill that makes security practitioners credible to auditors, management, and business stakeholders who think in terms of compliance obligations rather than protocol mechanics.

Network security controls map across frameworks: firewall rule review, VLAN configuration, router patch management, 802.1X and DNSSEC each have a corresponding requirement in NIST, ISO/IEC 27002, CIS Controls and others. This cross-framework literacy is essential in governance, risk and compliance roles.
:::

%%%

---
unit: Summary
code: SUM
title: The Plumbing Underneath Everything
---
::::columns
::col::
:::callout style=pull
Every network attack you'll study from here on is really an attack on one of these pieces, a packet, a protocol, an address, or a port.
:::
::col::
:::list style=chips
- Packets
- Protocols
- TCP/IP
- IP Addressing
- Ports
:::
::::
::::columns
::col::
:::table
| Layer        | Protocols       | Functions                          | Vulnerabilities                   |
|--------------|------------------|------------------------------------|-----------------------------------|
| Application  | HTTP, DNS, SMTP  | Data representation and services   | Injection, DNS spoofing           |
| Transport    | TCP, UDP         | End-to-end communication           | SYN flood, UDP amplification      |
| Internet     | IP (v4/v6)       | Logical addressing and routing     | IP spoofing, fragmentation attacks|
| Link         | Ethernet, ARP    | Physical addressing and framing    | ARP spoofing, MAC flooding        |
:::
::col::
:::list heading="Core Concepts" style=plain
- **Packets** are structured data units with headers and payloads.
- **Protocols** define syntax, semantics, and synchronization.
- **IP Addresses** identify devices on a network.
- **Ports** distinguish services on a single host.
:::
::::

:::image src="images/11_attack_surface_by_layer.png" alt="TCP/IP model diagram with attack vectors annotated at each layer: DNS spoofing and injection at Application, SYN flood and UDP amplification at Transport, IP spoofing and fragmentation at Internet, ARP spoofing and MAC flooding at Link layer, using color-coded threat icons and arrows" caption="Every network attack maps to a specific layer and protocol: knowing the layer tells you both where the vulnerability lives and what defensive control addresses it" width=full
:::

:::notes
In this foundational lecture, we have examined the core components that constitute the infrastructure of all network communications. These elements, packets, protocols, addressing schemes, and port numbers, are not merely abstract concepts but the tangible substrates upon which every network transaction depends. Understanding them in detail is essential for both defensive and offensive cybersecurity practices.

A **packet** is the fundamental unit of data transmission in modern networks. Defined by standards such as those in the IEEE 802 series and RFC 791 (Internet Protocol), packets encapsulate data along with headers containing metadata like source and destination addresses, protocol type, and sequencing information. Attackers often manipulate packet fields to perform actions such as IP spoofing (RFC 2827, also known as ingress filtering) or crafting malformed packets to exploit buffer overflows (e.g., CVE-2003-0147, the WINS Remote Code Execution vulnerability). Packet manipulation is the foundation of many network-layer attacks and is why packet-level inspection in firewalls and IDS/IPS systems is so valuable.

**Protocols** define the rules and conventions for communication. The TCP/IP model, which includes layers such as the Network Interface, Internet (IP), Transport (TCP/UDP), and Application layers, governs how data is segmented, addressed, transmitted, and received. Each protocol has its own vulnerabilities. For instance, TCP is susceptible to session hijacking and SYN flood attacks, while UDP's stateless nature makes it ideal for amplification DDoS attacks. Protocol-level security analysis, understanding not just how protocols are designed but how they behave under adversarial conditions, is a core skill for network security professionals.

**IP addressing**, governed by RFC 791 for IPv4 and RFC 8200 for IPv6, provides the logical topology of the internet. Misconfigurations or lack of proper subnetting can lead to exposure of internal systems. Address Resolution Protocol (ARP), which maps IP addresses to MAC addresses, is vulnerable to ARP spoofing (CVE-1999-0710), enabling man-in-the-middle attacks where traffic is redirected through an attacker's system without the victim's knowledge. IPv6's Neighbor Discovery Protocol (NDP) has analogous vulnerabilities, addressed partially by SEND (Secure Neighbor Discovery, RFC 3971).

**Ports** are logical endpoints for communication. Defined by IANA port number registries, they allow multiplexing of network services on a single host. Port scanning (e.g., using tools like Nmap) is a common reconnaissance technique that falls under MITRE ATT&CK technique T1046, and open ports can expose vulnerable services such as SMB (port 445), historically exploited in attacks like EternalBlue (CVE-2017-0144) that formed the basis of the WannaCry ransomware attack. Reducing open ports through service minimization and host-based firewall rules is one of the most impactful and immediately actionable hardening steps available to security teams.

In this expanded lecture, we covered additional critical topics: DNS resolution and its vulnerability to cache poisoning (CVE-2008-1447, the Kaminsky Bug); ARP's authentication gap and the ARP spoofing attack class; the OSI model as shared vocabulary for the security profession; subnetting and CIDR as the enabling technology for network segmentation; MAC addresses and their role in Layer 2 forwarding and attacks; the IPv4-to-IPv6 transition and its dual-stack security implications; ICMP's diagnostic role and its abuse in tunneling and amplification attacks; the hierarchy of hubs, switches, and routers and why topology matters for security; VLAN segmentation and VLAN hopping attacks; DHCP's DORA process and rogue DHCP spoofing; firewalls, DMZ architecture, and NGFW capabilities; VPN protocols and their limitations in a Zero Trust world; Wireshark for packet capture and protocol analysis; Nmap for network discovery and vulnerability scanning; a taxonomy of network attack categories by layer; common misconceptions that create false security confidence; and an alignment of these topics to governing frameworks including NIST SP 800-53, NIST CSF 2.0, ISO/IEC 27001/27033, CIS Controls, and MITRE ATT&CK.

In the next lecture, we will explore how adversaries exploit these primitives through DNS cache poisoning, IP spoofing, and TCP session hijacking. These attacks directly manipulate the mechanisms introduced here, underscoring why a solid grasp of network fundamentals is indispensable for cybersecurity professionals.
:::
