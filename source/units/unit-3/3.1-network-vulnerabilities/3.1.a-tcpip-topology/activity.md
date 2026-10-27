# In-class activity, 3.1.a TCP/IP fundamentals and network topology flaws

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students trace a network connection through all four TCP/IP layers, identify which header fields
are forgeable, and explain why a flat network topology amplifies risk. Ties to LO 3.1.A (describe
TCP/IP stack structure and topology-based attack surfaces).

## Materials (all local)
- the SimLab simulation on each machine, or the printed packet diagram set below.

## Steps
1. Each pair opens the simulation and steps through the simulated TCP connection. For each packet
   displayed, they label: (a) which layer's header is shown, (b) which field could be forged by
   an attacker and why.
2. Pairs draw a simple network diagram showing two scenarios: a flat network and a segmented
   network. For each, they mark where a compromised host could reach without crossing a firewall.
3. Using the packet log in the simulation, pairs identify which packets show evidence of IP spoofing
   and write one sentence describing the defense that would block each one.

## Collaborate (AP skill 4)
Assign roles: one partner is the "network analyst" (describes what each header field means
legitimately), the other is the "attacker" (explains how to forge or abuse that field). Swap roles
halfway through. For the topology diagram step, both partners must agree before writing.

## Exit ticket
Each student submits: the name of the TCP/IP layer targeted by IP spoofing, the name of one
network topology defense, and one sentence explaining why switches alone do not prevent all
sniffing attacks.

## Instructor notes
- Common stumble: students confuse IP addresses (internet layer) with MAC addresses (network
  access layer). Reinforce: IP = routing across networks, MAC = delivery on one local segment.
- Common stumble: students think switches make all interception impossible. Clarify MAC flooding
  and ARP spoofing as switch-defeating techniques (bridged to 3.1.c).
- The topology diagram step surfaces the concept of lateral movement, connect it to the
  breach-containment role of segmentation.
- This activity feeds the unit project (network threat model) and connects to 3.1.b-d for the
  full attack chain.
