# 1.2.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
It's worth pausing on why TOTP specifically, not SMS, not email, became the default second factor: the whole scheme works *offline*, with zero network trust required at verification time. Both the phone and the server independently compute the same 30-second-windowed function of a shared secret and the clock. No code ever crosses a network where it could be intercepted, spoofed, or SIM-swapped. That's a fundamentally different security posture than SMS codes, which do travel over an inherently interceptable carrier network, and it's why this skill asks you to build TOTP from `hmac`/`hashlib` yourself: once you've computed a code by hand, "the app just knows" stops being magic and becomes math you own.

## The big picture
The real lesson underneath the RFC 6238 mechanics is this: strong authentication isn't one strong thing, it's two *independent* weak things stacked so an attacker has to defeat both simultaneously through completely different means. A phished password and a phished TOTP code both individually compromise a factor, but an attacker who only got one of the two still has nothing. That's the actual security property MFA buys you, and it's why phishing-resistant factors (hardware keys) matter more than which specific app you use: the goal is factors that fail independently, not factors that feel different but fail together.
