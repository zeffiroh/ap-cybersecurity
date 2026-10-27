# In-class activity, 3.4.a Firewall types (stateful vs. stateless)

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students distinguish stateless and stateful firewall behavior by manually processing a packet
stream, first as a stateless rule-matcher and then as a stateful connection tracker. Ties to LO
3.4.A (explain the difference between firewall types and their inspection methods).

## Materials (all local)
- the SimLab simulation on each machine, or the printed packet table below.

## Steps
1. **Round 1, Stateless (10 min).** Each pair receives the packet table below. Working only with
   source IP, destination port, and protocol, they apply the three rules in order and mark each
   packet ALLOW or DROP. One partner reads the packet fields aloud; the other finds the matching
   rule and records the verdict.

2. **Round 2, Stateful (10 min).** The same packet stream is re-processed, but now the pair
   also tracks a connection table on paper (a blank grid: src_ip, dst_ip, src_port, dst_port,
   state). They update the table for SYN packets (add entry, state=SYN_SENT), SYN-ACK (update to
   ESTABLISHED), and RST/FIN (remove entry). Packets that do not match any table entry and also
   do not match an inbound-permit rule are dropped.

3. **Compare (5 min).** Pairs compare their stateless and stateful verdict lists. They identify
   every packet that received a different verdict in the two rounds and write one sentence
   explaining why the stateful result is more secure.

## Printed packet table (deterministic seed)
```
# Rule set (apply top to bottom, first match wins)
Rule 1: ALLOW TCP any -> 443
Rule 2: ALLOW TCP any -> 80
Rule 3: DROP  any any -> any  (implicit deny)

Pkt  Src IP          Dst IP          SrcPt  DstPt  Proto  Flags   Notes
A    203.0.113.10    10.0.0.5        55001  443    TCP    SYN     New HTTPS request
B    10.0.0.5        203.0.113.10    443    55001  TCP    SYN-ACK Server reply
C    203.0.113.10    10.0.0.5        55001  443    TCP    ACK     Handshake complete
D    198.51.100.7    10.0.0.5        44000  443    TCP    ACK     ACK with no prior SYN
E    192.0.2.99      10.0.0.5        62000  22     TCP    SYN     SSH attempt (not in rules)
F    203.0.113.10    10.0.0.5        55001  443    TCP    RST     Spoofed reset
G    10.10.10.1      10.0.0.5        51000  80     TCP    SYN     Internal HTTP request
H    10.0.0.5        10.10.10.1      80     51000  TCP    SYN-ACK HTTP server reply
```

Expected stateless verdicts: A=ALLOW, B=ALLOW, C=ALLOW, D=ALLOW, E=DROP, F=ALLOW, G=ALLOW, H=ALLOW

Expected stateful verdicts: A=ALLOW (add SYN_SENT), B=ALLOW (state->ESTABLISHED), C=ALLOW,
D=DROP (no session for this ACK), E=DROP (no rule + no session), F=DROP (RST for established
session from wrong direction, optional discussion), G=ALLOW (add SYN_SENT), H=ALLOW.

## Collaborate (AP skill 4)
Assign roles: one partner is the "firewall" (enforces rules strictly), the other is the
"network engineer" (maintains the connection table and challenges any rule the firewall misapplies).
After both rounds, partners swap roles and process two additional instructor-supplied packets.

## Exit ticket
Each student writes: one packet scenario that a stateless firewall would allow but a stateful
firewall would drop, plus one sentence explaining which firewall characteristic makes the
difference.

## Instructor notes
- Key learning moment: packet D (ACK with no prior SYN) is allowed by the stateless firewall
  because its port matches Rule 1. The stateful firewall drops it because no session exists.
  This is the central "aha" of the atom.
- Common stumble: students treat SYN-ACK return traffic as a new connection rather than as a
  response. Clarify that the firewall tracks the session from the initial SYN, so return traffic
  for an established session is automatically permitted regardless of direction rules.
- Feeds the unit project (firewall rule design) and the scenario stage where students configure
  a simulated network perimeter.
