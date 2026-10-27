# 3.1.d, Packet capture and traffic sniffing

> **Unit 3 · 3.1 Network Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 3.1.B, 3.1.C
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Explain how packet capture tools intercept network traffic, apply
capture and display filters to isolate relevant packets, and analyze a small packet log to identify
credentials or indicators of compromise sent in cleartext.

## Lesson

### What packet capture is
**Packet capture** (often called "sniffing") is the process of intercepting and logging network
traffic as it passes across a network interface. Every packet that a network interface card (NIC)
sees can, in principle, be copied and inspected, this is exactly what tools like **Wireshark**
(graphical) and **tcpdump** (command-line) do. Packet capture is a dual-use capability: network
administrators use it constantly for legitimate troubleshooting (why is this connection slow? why
did this handshake fail?), while attackers use the exact same technique to eavesdrop on traffic
they should not have access to. The tool itself is neutral; what makes capture an attack is the
position (does the attacker have legitimate access to see this traffic?) and the content
(cleartext credentials, PII, session tokens).

### How traffic becomes visible to a listener
On older shared-media networks (hubs), every packet was physically broadcast to every port, so any
connected device could see all traffic without any special effort, this is why sniffing was
trivial in the 1990s. Modern switched networks are smarter: a switch normally sends a frame only to
the port where the destination MAC address lives, which limits what a passive listener on a random
port can see. Attackers get around this in one of three ways: (1) **ARP spoofing** (3.1.c) to
redirect traffic through the attacker's machine, after which the attacker can sniff everything that
transits; (2) **port mirroring / SPAN ports**, a legitimate switch feature (intended for monitoring
tools and IDS sensors) that copies all traffic from one or more ports to a monitoring port, if
misconfigured or granted to the wrong party, this becomes an attack surface; (3) **promiscuous
mode**, a NIC setting that tells the network stack to accept and process every frame it physically
receives, not just frames addressed to its own MAC, necessary for a capture tool to see anything
beyond its own traffic, but only useful once traffic is actually reaching that NIC (via a hub, a
mirrored port, or a MITM position).

### Capture filters vs. display filters
Both Wireshark and tcpdump distinguish two filtering stages. A **capture filter** is applied at
capture time, before packets are ever written to disk or memory, for example, `tcp port 80`
captures only HTTP traffic and discards everything else on the wire, which reduces file size and
resource use for a targeted investigation. A **display filter** is applied after capture, to a
file (or live session) that already contains everything, for example, in Wireshark,
`http.request.method == "POST"` narrows the view without discarding any of the underlying capture.
The practical tradeoff: a capture filter cannot be "undone" (you cannot recover packets you never
captured), so analysts often capture broadly and filter the display narrowly when they are unsure
exactly what they are looking for, then tighten capture filters once the investigation is focused.

### What cleartext protocols leak
Any protocol that does not encrypt its payload is fully readable by anyone in a position to capture
it. Classic examples: **HTTP** (plain, not HTTPS) sends form data, including login credentials, as
readable text in the request body; **Telnet** sends every keystroke, including passwords, in the
clear; **FTP** sends the username and password in plaintext during authentication; and older mail
protocols like unencrypted **POP3/IMAP** and **SMTP** can expose both credentials and message
content. A packet analyst reviewing a capture of any of these protocols can typically reconstruct
the entire login attempt, username, password, and the resulting session, just by reading the
payload bytes. This is precisely why the industry has moved toward encrypted equivalents (HTTPS,
SSH, FTPS/SFTP, IMAPS/SMTPS): encryption does not stop the attacker from capturing the packets, but
it makes the captured payload unreadable without the decryption key.

### Reading a capture: the anatomy of a logged packet
A captured packet record typically includes, at minimum, a timestamp, source and destination IP
addresses, source and destination ports, the transport protocol (TCP/UDP), and (for cleartext
protocols) the readable payload. Analysts scan for known indicators: a payload containing strings
like `Authorization: Basic`, `password=`, or a Telnet login banner immediately followed by
plaintext keystrokes are all signatures of exposed credentials. Port number is also a strong hint, port 80 (HTTP), port 23 (Telnet), and port 21 (FTP control) are all cleartext-by-default; port 443
(HTTPS) and port 22 (SSH) are encrypted by design and their payload will appear as unreadable binary
in a capture (unless the analyst has the private key, as in a lawful/enterprise TLS-inspection
setup).

### Defense
The primary defense against traffic sniffing is not preventing capture (which is often impossible
to fully block on a shared network) but ensuring that anything captured is useless to the attacker:
**end-to-end encryption** (TLS/HTTPS, SSH, VPNs) so payload contents are unreadable even if
captured; **switched networks with port security** to limit unauthorized port mirroring; and
**network segmentation** so a compromised or malicious device only has visibility into a small
slice of traffic rather than an entire subnet. Detecting active sniffing itself is hard because
passive listening leaves no direct trace on the wire, defenders instead focus on detecting the
techniques that enable a sniffing position, like ARP spoofing (3.1.c) or unauthorized port-mirror
configuration changes.

The coding problem in `problem/` asks you to scan a small captured traffic log and flag every
entry that exposes a plaintext credential, based on the protocol/port and payload content, the
same triage a junior SOC analyst performs on a Wireshark export.

## Key terms
- **Packet capture (sniffing)**, intercepting and logging network traffic passing a network
  interface.
- **Promiscuous mode**, a NIC setting that accepts all frames it physically receives, not just
  those addressed to its own MAC.
- **Port mirroring / SPAN port**, a switch feature that copies traffic from one or more ports to a
  monitoring port for legitimate analysis (or, if misused, for eavesdropping).
- **Capture filter**, a filter applied before capture that determines which packets are recorded
  at all.
- **Display filter**, a filter applied after capture to narrow which already-captured packets are
  shown.
- **Cleartext protocol**, a protocol (HTTP, Telnet, FTP, unencrypted SMTP/POP3/IMAP) that sends
  payload data, including credentials, without encryption.

## Common misconceptions
- "You need to be an attacker to use Wireshark." → Packet capture is a standard, legitimate
  network-troubleshooting and security-monitoring tool; it becomes an attack only through
  unauthorized access or misuse of legitimate positioning (e.g. a misconfigured SPAN port granted
  to the wrong party).
- "A switched network makes sniffing impossible." → A switch limits sniffing compared to a hub, but
  ARP spoofing, port mirroring misuse, and compromised network taps all still allow an attacker to
  see traffic they should not on a fully switched network.

## Try it
- **Simulation:** Review captured packet log entries and flag
  which ones expose a plaintext credential, reaching the scoring goal.
- **Coding problem:** Scan a list of captured packet records and return the ones that
  leak a plaintext credential based on protocol/port and payload content.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Wireshark User's Guide (capture and display filter chapters), rebuilt as original prose
  above; reference copy at `vendor/reference/3.1.d-wireshark-guide-ref.md`.
- Reference: SANS Reading Room, "Packet Sniffing: An Overview", rebuilt equivalent at
  `vendor/reference/3.1.d-packet-sniffing-ref.md`.
- Practice: Cybrary network-forensics module (packet analysis lab), rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/LetsDefend-Free-Cybersecurity-Resources/`.
