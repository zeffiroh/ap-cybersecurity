# 3.4.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The question to carry into this lecture: does the firewall remember anything, or does it wake up with total amnesia before every single packet? That's the entire stateless-versus-stateful distinction in one sentence, and it's worth having ready because the exam scenario that trips students up almost always hinges on exactly this, a packet that looks perfectly legitimate in isolation (correct port, correct protocol, an ACK bit set) but that no real connection ever actually started.

## The big picture
The scenario worth remembering by name is the spoofed RST packet: a stateless firewall sees TCP, port 80, allowed and waves it through, because a stateless firewall genuinely cannot ask whether this is part of a connection that actually exists, it has no memory to ask that question with. A stateful firewall's connection-tracking table is what makes that question askable at all, and that's precisely why stateful inspection defeats a whole category of spoofing and session-hijacking attacks that a stateless ruleset simply cannot see. Don't let stateful expand in your head into smart, though, this skill is explicit that stateful inspection tracks *connection state*, not *payload content*; malware riding inside an already-permitted HTTPS session sails straight through a stateful firewall because the firewall's only question is whether the session is established, not what's actually inside it. That gap, connection-aware but content-blind, is exactly the opening the next atom's ACL precision starts to narrow, and it's also the reason 3.5's IDS/IPS atom needs to exist at all: something has to inspect what a stateful firewall, by design, does not.
