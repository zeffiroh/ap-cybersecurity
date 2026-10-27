# 3.1.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Hold onto this framing before the lecture even starts: TCP/IP was built for a network of people who already trusted each other, and every structural weakness this skill covers is just that original assumption of trust refusing to die. Nobody added authentication to IP addresses or ARP because nobody in 1975 imagined a stranger would want to lie about who they were. That's not a bug that slipped through code review, it's the entire internet's foundation being built for a world that no longer exists. Once you see the stack that way, IP spoofing and ARP spoofing stop looking like clever hacks and start looking like the completely predictable consequence of never having asked "but what if the sender lies?"

## The big picture
The move worth carrying forward out of this skill is asking, for any attack, "which layer does this operate at, and which layer must the defense operate at?" That single question is what turns the four-layer stack from a memorization exercise into an actual diagnostic tool: IP spoofing gets fought at the internet layer, ARP spoofing (3.1.c) at the network access layer, DNS poisoning (3.1.b) at the application layer, and a flat topology's blast radius gets fought by segmenting the network itself rather than patching any single layer at all. Notice too that this skill quietly previews the entire rest of Unit 3, DNS attacks, MITM, packet sniffing, VLANs, firewalls, IDS/IPS are all just this skill's four weaknesses (unauthenticated IPs, predictable handshakes, trusting ARP, forgeable DNS) getting their own dedicated defense in later atoms. If you understand why TCP/IP trusts everyone, you already understand why the rest of this unit exists.
