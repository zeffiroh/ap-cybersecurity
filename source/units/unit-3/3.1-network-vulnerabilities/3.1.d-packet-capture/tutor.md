# 3.1.d tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The idea to hold before this lecture: a sniffer is not itself the attack, the attack is whatever let the sniffer see traffic it shouldn't, and whatever that traffic exposed once seen. Wireshark and tcpdump are the exact same tools a network administrator runs every single day to debug a slow connection; nothing about the tool is malicious. That reframing matters because it means the real security question is never "is packet capture happening," it's "who has the position to capture, and is the payload readable once they do", which is precisely the two-part filter this skill hands you.

## The big picture
This skill is the payoff for everything Unit 3 has built up to this point: ARP spoofing (3.1.c) earns an attacker the *position* to sniff traffic that a switch would otherwise keep hidden from them, and this skill shows you what that position is actually worth, cleartext credentials on HTTP, Telnet, and FTP sitting there in plain readable bytes, versus HTTPS and SSH traffic that shows up as unreadable binary even to an attacker sitting directly in the traffic's path. That's the cleanest demonstration in the whole unit of a principle worth generalizing: you often cannot stop an attacker from reaching a position to listen, so the real defense is making sure whatever they hear is useless to them. Keep the capture-filter-versus-display-filter distinction straight for the exam too, a capture filter decides what's ever recorded, a display filter only decides what you're currently looking at within what was already recorded, and that's an irreversible-versus-reversible distinction the exam likes to probe.
