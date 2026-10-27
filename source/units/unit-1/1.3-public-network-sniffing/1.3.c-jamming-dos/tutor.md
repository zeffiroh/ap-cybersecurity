# 1.3.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Jamming is the one attack in this unit that isn't really about deception at all, there's no fake network, no stolen credential, nothing to trick you into trusting. It's brute physical denial: flood the shared medium with noise until CSMA/CA politeness forces every legitimate device to back off. The intuition worth keeping is that Wi-Fi's cooperative design, devices listening before they transmit so they don't collide, is precisely the mechanism a jammer weaponizes. The same courtesy that makes Wi-Fi work efficiently among cooperating devices makes it exploitable by one that refuses to cooperate.

## The big picture
The distinction between a jamming attack and ordinary microwave-oven interference is a small, concrete example of a detection principle that recurs constantly in security: it's rarely the presence of an anomaly that matters, it's the *duration*. A brief spike is noise; a sustained plateau is an event. You'll meet this exact reasoning again, a single failed login versus a sustained burst (1.2.a), a single loud sound versus continuous elevated noise here, because "sustained over a threshold" is one of the most broadly reusable detection heuristics in the entire field.
