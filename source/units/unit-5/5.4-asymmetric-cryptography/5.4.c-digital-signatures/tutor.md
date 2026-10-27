# 5.4.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The upgrade worth anticipating before this lecture: everything HMAC (5.3.c) gave you, proof the data wasn't altered, proof it came from someone who held a secret, a digital signature gives you too, plus one thing HMAC structurally cannot: non-repudiation. The reason is almost embarrassingly simple once you see it, HMAC's two parties share one secret, so either one of them could have produced any given tag, and there's no way to prove after the fact which one actually did. A signature uses two different keys for the two different actions, so only the signer's own private key could have produced it, and nobody, not even the verifier, could have forged it themselves.

## The big picture
The detail worth remembering longest is why you hash before you sign rather than signing the raw message directly: it keeps every signature a fixed, small size regardless of how long the original document is, it keeps the expensive RSA operation to a single pass, and it inherits the avalanche effect from 5.3.a so that a one-bit change anywhere in the message produces a completely different digest, meaning tampering is caught the instant verification recomputes the hash. Hold onto the three guarantees (authenticity, integrity, non-repudiation) as a set, because 5.4.d is about to show you the one gap none of this solves on its own: even a perfect signature only proves the person who holds a particular private key signed something, it says nothing about whether that person is who they claim to be. That identity-binding problem is exactly what PKI exists to close.
