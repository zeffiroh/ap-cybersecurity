# 5.4.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The bootstrap problem worth sitting with before this lecture: symmetric cryptography (5.3) is strong once both sides share a key, but it never actually explains how two strangers agree on a secret over a network where anyone could be listening, asymmetric cryptography is the answer to that exact gap. The elegant part is that one of your two keys is designed to be handed to literally anyone, posted publicly, shouted across an open channel, and none of that weakens your security at all, because possessing the public key was never the thing protecting you.

## The big picture
The image worth keeping is the one-way trapdoor: easy to fall through, computationally infeasible to climb back up without the specific private key that makes the climb possible. Multiplying two large primes together is trivial; factoring their product back into those primes, without already knowing one of them, is what real-world security rests on. Also lock in the two use cases now, because every atom for the rest of this section is just one of them elaborated: encrypt with the public key so only the private-key holder can read it (confidentiality, 5.4.a/b), or sign with the private key so anyone can verify only that key-holder could have produced it (authenticity, 5.4.c). Getting those two directions backwards is the single most common conceptual error students make in this unit, and it's worth drilling until "encrypt-with-public, sign-with-private" is automatic.
