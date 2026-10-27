# 3.4.a, Firewall types (stateful vs. stateless)

> **Unit 3 · 3.4 Protecting Networks: Firewalls**
> **AP Learning Objective(s):** 3.4.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Distinguish stateless from stateful firewalls, explain how each
inspects traffic, and identify which type is better suited to a given threat scenario.

## Lesson
Every network sits behind some form of gatekeeper, a device that decides which packets may enter
or leave. The firewall is the most fundamental of those gatekeepers. Before you can configure one,
you need to understand how it thinks about traffic. Two fundamentally different models exist:
stateless inspection and stateful inspection.

**The packet and the problem it creates.** Data traveling across a network is chopped into small
chunks called packets. Each packet carries a header, source IP address, destination IP address,
protocol (TCP, UDP, ICMP), source port, and destination port, and a payload. The simplest
possible firewall looks only at those header fields, makes a decision for each packet
independently, and moves on. This is a stateless (or packet-filtering) firewall.

**Stateless firewalls: fast, but blind to context.** A stateless firewall applies a list of rules
(an ACL) to every packet in isolation. The rule might read: "allow TCP packets from any source to
destination port 443." The firewall checks the header, matches the rule, and forwards the packet.
It does not remember the previous packet. It does not know whether this packet is part of an
established connection or is an unsolicited probe arriving out of nowhere. That blindness is both
its strength and its weakness. It is extremely fast and inexpensive to implement, routers,
switches, and early border firewalls used this approach. But because it cannot distinguish an
answer to a legitimate request from an uninvited knock, an attacker can sometimes craft packets
that look valid in isolation yet carry malicious intent. A spoofed TCP packet with the ACK bit set
will sail through most stateless rules because such packets look like part of an existing
conversation to a rule that only reads headers.

**The TCP three-way handshake and why it matters.** To understand stateful inspection, recall how
TCP connections begin. A client sends a SYN packet; the server replies with SYN-ACK; the client
completes the handshake with ACK. Only then does data flow. This handshake creates a shared
understanding between the two endpoints that a connection exists. A stateless firewall does not
track this; a stateful firewall does.

**Stateful firewalls: connection awareness.** A stateful (or stateful-inspection) firewall
maintains a connection-tracking table in memory. When the first SYN packet for a new TCP
connection arrives and passes the rule set, the firewall logs the connection: source IP, source
port, destination IP, destination port, protocol, and state (SYN_SENT). As the three-way
handshake completes, the entry advances to ESTABLISHED. Return traffic, the SYN-ACK from the
server, subsequent ACKs, data segments, is automatically permitted because the firewall recognizes
these packets as belonging to a tracked, legitimate session. If a packet arrives claiming to be
part of a connection that is not in the table, the firewall drops it, even if the individual
header would otherwise satisfy a static rule. This single capability defeats many spoofing and
session-hijacking attacks.

**Concrete scenario.** Suppose the internal network at Meridian High School uses a stateless
firewall that allows inbound TCP packets on port 80. An attacker outside the network sends a TCP
packet with the RST (reset) flag set, destination port 80, spoofing the source address of an
internal web server. The stateless firewall sees "TCP, port 80, allow" and forwards it. The
packet disrupts an active connection inside the network. Under a stateful firewall, the same
packet would be checked against the connection table: is there an established session with these
endpoints? No. Dropped.

**Stateful does not mean stateful knows everything.** Stateful inspection tracks connection state,
but it does not examine the application-layer content of those packets. Malware delivered inside
an HTTPS stream will pass through a stateful firewall if port 443 is permitted, because the
firewall only knows the connection is established and the destination port is correct. Application
layer inspection (the function of next-generation firewalls and proxies) is a separate capability
covered in later units. For the AP exam, the key distinction is stateful vs. stateless, not
stateful vs. NGFW.

**Choosing the right type.** Stateless firewalls are still used at high-speed network edges where
raw throughput matters more than fine-grained inspection, and where simple permit/deny rules by
IP or port are sufficient. Stateful firewalls are the standard for protecting internal networks,
servers, and endpoints because connection awareness closes the gaps that stateless rules leave
open. In practice, most enterprise firewalls are stateful; stateless rules sometimes appear on
embedded or legacy devices.

**Simulation.** The simulation presents a stream of inbound packets and asks you to
decide, operating first as a stateless firewall, then as a stateful one, which packets to allow
or drop. The challenge in the stateful round is that some packets claim membership in sessions that
were never established. Correctly dropping those while passing legitimate return traffic is the
target skill.

**Coding problem.** The `problem/` directory contains a packet-classification challenge: given a
ruleset and a sequence of packets (including SYN, SYN-ACK, ACK, and RST packets), implement a
stateless firewall first, then extend it to track connection state and emit "allow" or "drop" for
each packet, demonstrating the behavioral difference between the two types.

## Key terms
- **Stateless (packet-filter) firewall**, examines each packet independently against a fixed rule
  set; no memory of prior packets or connection state.
- **Stateful (stateful-inspection) firewall**, maintains a connection-tracking table; permits
  return traffic for established sessions and drops packets that do not match any tracked session.
- **Connection-tracking table**, data structure the firewall uses to record active sessions
  (source IP, destination IP, ports, protocol, and connection state).
- **Packet header**, the metadata portion of a packet (IP addresses, ports, flags, protocol)
  that both firewall types examine.
- **TCP three-way handshake**, the SYN / SYN-ACK / ACK exchange that establishes a TCP session;
  stateful firewalls use this to know when a connection is legitimately open.

## Common misconceptions
- "A stateful firewall is always more secure than a stateless one." → Stateful is more aware of
  connection context, but security also depends on the rules written. A stateful firewall with a
  rule that permits all inbound traffic is still insecure.
- "Stateful firewalls inspect the content of packets." → Stateful inspection tracks connection
  state, not application payload. Content inspection is a separate, application-layer function.
- "Stateless firewalls are obsolete." → They are still used where performance and simplicity
  matter, such as high-throughput edge routers or embedded devices with limited CPU.

## Try it
- **Simulation:** Correctly allow or drop each packet in both
  stateless mode and stateful mode, reaching the target score by correctly handling out-of-state
  packets in the stateful round.
- **Coding problem:** Implement a stateless then stateful packet classifier: given an
  ordered ruleset and a packet sequence, return "allow" or "drop" per packet using first-match
  logic; the stateful version additionally tracks TCP session state.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (Network and Computer Security), rebuilt as original prose above; concepts
  drawn from the open-courseware lecture notes on packet filtering and stateful inspection.
- Reference: NIST SP 800-41 Rev. 1 (Guidelines on Firewalls and Firewall Policy), local rebuild
  summarizing packet-filter vs. stateful firewall characteristics.
- Practice: SANS Cyber Aces networking module, rebuilt locally as the simulation packet-decision
  exercise.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity`
