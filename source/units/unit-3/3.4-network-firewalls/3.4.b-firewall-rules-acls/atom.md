# 3.4.b, Firewall rules and access control lists (ACLs)

> **Unit 3 · 3.4 Protecting Networks: Firewalls**
> **AP Learning Objective(s):** 3.4.B, 3.4.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Write and evaluate an ordered firewall access control list (ACL),
correctly apply first-match-wins evaluation, and identify when a rule's placement creates a
security gap by shadowing a more specific rule below it.

## Lesson
A firewall's decisions are only as good as the rule list it is given. That rule list is called an
access control list (ACL): an ordered sequence of statements, each specifying an action (allow or
deny) and a set of matching conditions, source address, destination address, destination port,
and protocol. Understanding how a firewall reads and applies an ACL is the difference between a
network that is actually protected and one that only looks protected on paper.

**Rule anatomy.** Each ACL entry names four things a packet is checked against: source IP (or
range), destination IP (or range), destination port, and protocol (TCP, UDP, or "any"). A rule
also carries an action, `allow` or `deny`. A typical entry reads: "allow TCP from 10.0.4.0/24 to
10.0.1.5 on port 3306", the accounting subnet may reach the database server on its MySQL port.
Everything else about the packet is irrelevant to that rule; only the four match fields and the
action matter.

**First-match-wins evaluation.** A firewall evaluates an ACL top to bottom, in the exact order the
rules are written. The instant a packet matches a rule's conditions, that rule's action is applied
and evaluation stops, no later rule is ever consulted for that packet, even if a later rule would
also have matched and specified a different action. This ordering dependency is the single most
important fact about ACLs: two lists containing the identical set of rules, written in different
orders, can produce completely different security outcomes.

**The implicit deny.** Every well-formed ACL ends, explicitly or implicitly, with a final rule that
denies everything not already matched: "deny any any any." If a packet reaches the bottom of the
list without matching any earlier rule, it is dropped. This default-deny posture is a foundational
security principle, an ACL should permit only what is explicitly needed and reject everything
else by default, rather than trying to enumerate every possible bad packet.

**The shadowing anomaly.** The most common real-world ACL mistake is placing a broad "allow" rule
above a narrower rule that was meant to restrict a subset of that traffic. Suppose an administrator
at Meridian High School writes rule 1 as "allow TCP any any port 22" (SSH from anywhere, meant as a
temporary troubleshooting rule) and, three lines later, rule 4 as "deny TCP from
203.0.113.0/24 to 10.0.1.10 port 22" (block a known-hostile range from reaching the file server via
SSH). Because rule 1 matches first, every SSH packet, including the ones from 203.0.113.0/24, is
allowed before the ACL ever reaches rule 4. Rule 4 is not wrong; it is unreachable. This is called
rule shadowing: a broad rule earlier in the list makes a more specific rule later in the list dead
code. The fix is always about order, not content, the specific deny rule must be placed before the
broad allow, or the broad allow must be narrowed.

**Building a correct ACL.** The safe pattern is: place the most specific rules first (exceptions
and denies for particular hosts or subnets), then the general allows, and finish with the implicit
or explicit deny-all. When auditing an existing ACL, check each rule against every rule above it, if an earlier, broader rule already matches everything the later rule would match, the later rule
is shadowed and the ACL does not do what its author intended.

**Ports and protocols matter as much as addresses.** An ACL is not just about which hosts may talk;
matching on protocol and destination port lets an administrator permit narrow application traffic
(e.g., TCP/443 for HTTPS) while denying everything else from the same hosts. A rule that omits the
port field (matches "any port") is far broader than one written to match a single service, and
broad rules are exactly the kind that tend to shadow later, more careful rules.

**Simulation.** The simulation presents a small, editable Meridian High School
perimeter ACL and a stream of packets. You reorder and edit rules so that every packet gets its
intended verdict, directly experiencing how moving a single line changes outcomes without changing
any rule's content.

**Coding problem.** The `problem/` directory implements the ACL evaluator itself: given an ordered
rule list and a batch of packets, return the correct "allow"/"deny" verdict for each packet using
first-match-wins logic with an implicit deny-all appended at the end, the exact algorithm every
real firewall runs.

## Key terms
- **Access control list (ACL)**, an ordered list of allow/deny rules a firewall applies to
  traffic, matched on source, destination, port, and protocol.
- **First-match-wins**, the evaluation model where a packet is judged by the first rule it
  matches, top to bottom; later rules are never consulted for that packet.
- **Implicit deny (default deny)**, the unwritten or explicit final ACL rule that drops any
  packet matching nothing above it.
- **Rule shadowing**, when a broad rule earlier in the list matches everything a more specific
  rule below it would match, making the lower rule unreachable.
- **Rule specificity**, how narrowly a rule's conditions match traffic; a rule scoped to one host
  and one port is more specific than one that matches "any" for those fields.

## Common misconceptions
- "The order of ACL rules doesn't matter as long as all the right rules exist." → Order is
  everything under first-match-wins; a correct rule placed after a broader matching rule never
  fires.
- "If there's no explicit deny-all at the end, unmatched traffic is allowed." → Real firewall ACLs
  are default-deny; unmatched traffic is dropped by the implicit deny even if no rule states it.
  (Some routers default to allow, the AP framework assumes default-deny for security devices.)
- "A more specific deny rule automatically overrides a broader allow rule." → Nothing "overrides"
  anything in a first-match-wins engine. The only thing that matters is which rule is physically
  listed first.

## Try it
- **Simulation:** Reorder/adjust a Meridian High School ACL so
  every packet in the test stream receives its intended verdict, resolving a shadowing bug.
- **Coding problem:** Implement an ACL evaluator: given an ordered rule list and a
  list of packets, return "allow"/"deny" per packet using first-match-wins with implicit deny-all.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (Network and Computer Security), rebuilt as original prose above; concepts drawn
  from open-courseware notes on packet filtering and access control lists.
- Reference: NIST SP 800-41 Rev. 1 (Guidelines on Firewalls and Firewall Policy), local rebuild
  summarizing ACL rule-ordering and default-deny guidance.
- Practice: SANS Cyber Aces networking module, rebuilt locally as the simulation ACL-editing exercise.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity`
