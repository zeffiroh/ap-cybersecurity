# 3.1.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The intuition to carry in: DNS is a race, and the attacker doesn't need to be strong, just fast and lucky enough times in a row. Because DNS runs over UDP with no session and no built-in verification, a forged reply that arrives before the real one wins outright, not because it's more convincing, but because the resolver has no way to tell a real answer from a fake one except "which one showed up first." That's a genuinely uncomfortable fact to sit with: an entire layer of internet infrastructure that billions of devices depend on every day is, at its core, a guessing game about a 16-bit number.

## The big picture
The throughline worth remembering is that DNS poisoning and ARP spoofing (3.1.c, next atom) are the same underlying vulnerability, a device blindly trusting an unauthenticated reply, expressed at two different layers of the stack you just met in 3.1.a. DNS poisons the mapping from name to IP before a connection even starts; ARP spoofing poisons the mapping from IP to MAC once you're already on the local network. Keep that parallel sharp, because it's exactly the kind of connection the AP exam rewards: recognizing that "forge the trusted-but-unauthenticated reply" is a reusable attack pattern, not a one-off DNS quirk. And don't let the misconception slide by, HTTPS staying green in your browser tells you nothing about whether DNS lied to you; it only tells you the certificate matched whatever server you actually reached, which is precisely why a spoofed DNS answer pointing you to an attacker's server usually fails loudly (a cert warning) rather than silently, and why that failure is a feature of the system working, not proof DNS spoofing didn't happen.
