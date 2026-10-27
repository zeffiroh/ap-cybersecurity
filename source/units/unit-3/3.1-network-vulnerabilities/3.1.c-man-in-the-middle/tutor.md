# 3.1.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The mental model worth having before lecture: ARP is a network's equivalent of everyone in a room shouting their own name whenever asked, with zero ID check, and everyone else just believing the loudest recent answer. That's not a metaphor stretched to fit, it's literally how a gratuitous ARP reply works, an answer nobody even asked for that devices accept anyway. Once you've internalized that ARP has no authentication at all, ARP spoofing isn't a clever exploit, it's just... using the protocol exactly as specified, except lying.

## The big picture
The detail worth keeping long after this skill: a man-in-the-middle position is not the same thing as a broken connection, and that distinction is what makes MITM attacks so dangerous. Both the victim and the gateway keep working normally the entire time the attacker is silently relaying their traffic, nothing breaks, nothing looks wrong, which is exactly why detection tools like Dynamic ARP Inspection and ARP-watch software matter: the attack is invisible from inside the conversation and only visible from outside it, by noticing a MAC address suddenly claiming an IP it never owned before. Also worth locking in: HTTPS limits what a MITM attacker can *read*, but does nothing to stop them from *occupying the position* in the first place, that's a subtlety this course keeps returning to (you'll see it again with DNS in 3.1.b and packet sniffing in 3.1.d): encryption protects the payload, not the position, and those are two completely different problems with two completely different fixes.
