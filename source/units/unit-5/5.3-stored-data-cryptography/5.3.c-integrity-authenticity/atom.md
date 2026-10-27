# 5.3.c, Integrity and authenticity (HMAC)

> **Unit 5 · 5.3 Protecting Stored Data with Cryptography**
> **AP Learning Objective(s):** 5.3.B, 5.3.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain why a plain hash cannot prove who sent a message,
describe how HMAC combines a secret key with a hash function to provide both integrity and
authenticity, and classify a given integrity-check design as secure or vulnerable to tampering.

## Lesson
5.3.a established that a hash lets you detect whether data changed: store a digest, recompute
it later, and compare. That is enough when the only threat is accidental corruption, a bad
disk sector, a dropped byte in transit. It is not enough when the threat is an intelligent
attacker who can intercept and rewrite the data. Hash functions are public and keyless: anyone,
including an attacker, can run SHA-256 on any input they like. If an attacker intercepts a
message and its hash, changes the message, and recomputes the hash over the new message, the
recipient's integrity check passes cleanly, the digest matches, because the attacker computed
it correctly over the tampered content. A plain hash proves "this data matches this digest." It
proves nothing about who produced that pairing in the first place. That gap is the difference
between **integrity** (the data was not altered) and **authenticity** (the data really came
from who it claims to have come from, and only that party could have produced this digest).
Plain hashing gives you integrity checking only when the digest itself arrives over a channel
the attacker cannot also tamper with, which, in most real network scenarios, they can.

**The fix: put a secret into the hash.** If only the sender and the legitimate recipient know a
shared secret key, and that key is mixed into the hashing process, then an attacker who
intercepts and edits the message cannot recompute a matching digest, they do not know the key.
This construction is called a **MAC (Message Authentication Code)**: a keyed hash that proves
both that the data is unaltered (integrity) and that it was produced by someone holding the
key (authenticity), which is why HMAC output is often called a **tag** rather than just a
digest.

**Why not simply `H(key || message)`?** The obvious first attempt, concatenate the key and
message, then hash, has a real weakness in hash functions built on the Merkle-Damgard
construction (which includes MD5, SHA-1, and SHA-256). These functions process input in fixed
blocks and expose their entire internal state as the output digest. Knowing `H(key || message)`,
an attacker can, without ever learning the key, compute a valid hash for
`key || message || padding || attacker_data`, because the digest already gives them the exact
internal state the hash function would be in after processing `key || message`, and they can
resume hashing from there. This is a **length-extension attack**, and it has been used in real
exploits against APIs that naively authenticated requests with `H(secret + message)`.

**HMAC's construction defeats length extension.** Standardized in NIST FIPS 198-1, HMAC nests
the hash function twice around the key so the attacker never sees an exposed intermediate state
they can extend:
```
HMAC(key, message) = H( (key XOR opad) || H( (key XOR ipad) || message ) )
```
`ipad` and `ipad` are fixed padding constants (`0x36` and `0x5c` repeated to the hash's block
size) that are XORed with the key to derive two different keyed prefixes. The message is hashed
once with the inner keyed prefix, and the *result* of that inner hash is hashed again with the
outer keyed prefix. Because the final output is a hash of a hash, with the key folded in both
times, an attacker who only sees the final tag cannot recover any usable internal state to
extend, and cannot produce a valid tag for any message without knowing the key. Nesting the hash
twice, plus using two independently-derived keyed inputs, is what makes HMAC provably resistant
to length extension even when built on a Merkle-Damgard hash like SHA-256. You do not need to
memorize the padding constants, what matters conceptually is: HMAC is "hash the message with
the key baked in, twice," and that double nesting is intentional, not decorative.

**Verifying a tag.** To check a message's integrity and authenticity, the verifier recomputes
`HMAC(key, message)` themselves and compares it to the tag that arrived with the message. If they
match, the verifier has strong evidence the message is unaltered and was produced by whoever
holds the shared key. If even a single bit of the message changed in transit, tampered by an
attacker or corrupted accidentally, the avalanche effect means the recomputed tag will look
completely different, and verification fails.

**Where HMAC shows up in practice.** API request signing (a client and server share a secret,
and every request carries an HMAC tag over its contents so the server can reject tampered or
forged requests), verifying webhook payloads (many SaaS platforms sign webhook bodies with
HMAC-SHA256 so your server can confirm the request really came from them), and JWT tokens using
the `HS256` algorithm (the token's header and payload are HMAC-signed with a server-side secret,
so the server can detect if a client edited its own claims). In every case, HMAC answers the
same question: "did this data arrive unmodified, from someone who holds the shared secret?"

**Looking ahead.** HMAC requires both parties to share a secret key in advance, which does not
scale to scenarios like verifying a stranger's public software release. 5.4.c covers digital
signatures, the asymmetric equivalent: the signer uses a private key only they hold, and anyone
can verify with the matching public key, without ever sharing a secret.

The simulation (the simulation) has you decide, case by case, whether a tampered message would still
pass an integrity check under different designs (plain hash, naive `H(key+message)`, and real
HMAC), and the coding problem (`problem/`) has you implement the FIPS 198-1 HMAC construction
by hand on top of SHA-256 so you see the ipad/opad nesting directly instead of just calling a
library function.

## Key terms
- **MAC (Message Authentication Code)**, a keyed hash/tag that proves both integrity and authenticity.
- **HMAC**, the standardized (NIST FIPS 198-1) hash-based MAC construction using nested, keyed hashing.
- **Tag**, the output of a MAC/HMAC computation, compared during verification (analogous to a digest, but keyed).
- **Integrity**, assurance that data was not altered.
- **Authenticity**, assurance that data really came from the claimed, key-holding sender.
- **Length-extension attack**, exploiting a Merkle-Damgard hash's exposed internal state to extend `H(secret||message)` without knowing the secret.
- **ipad / opad**, fixed padding constants XORed with the key to derive HMAC's two nested keyed inputs.
- **Digital signature**, the asymmetric analog to a MAC, using a private/public key pair instead of a shared secret (see 5.4.c).

## Common misconceptions
- "A matching hash proves the message wasn't tampered with." → Only if the attacker could not also recompute the hash after tampering. A plain, keyless hash gives no such guarantee once an attacker can rewrite both the message and its accompanying hash.
- "`H(key + message)` is basically the same as HMAC." → Naive concatenation is vulnerable to length-extension attacks on Merkle-Damgard hashes (MD5/SHA-1/SHA-256); HMAC's nested nested construction is specifically designed to prevent this.
- "HMAC encrypts the message." → HMAC produces a tag for verification; it does not hide or encrypt the message content at all. Confidentiality requires separate encryption.
- "Integrity and authenticity are the same thing." → Integrity means unaltered; authenticity means it really came from the claimed sender. A plain hash can offer integrity (over a trusted channel) without authenticity; HMAC offers both because only the key holder can produce a valid tag.

## Try it
- **Simulation:** Classify each integrity-check design and
  tampering scenario as SECURE or VULNERABLE, reaching the target score.
- **Coding problem:** Implement the FIPS 198-1 HMAC-SHA256 construction by hand
  (ipad/opad nesting, using `hashlib.sha256` only for the inner `H()` step) plus a `verify()`
  helper, and confirm a single tampered bit changes the tag.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (6.858 Computer Systems Security, lecture notes on message authentication), rebuilt as original prose above.
- Reference: NIST FIPS 198-1 (The Keyed-Hash Message Authentication Code, HMAC standard), see vendor/web/nist/ notes.
- Practice: SANS Cyber Aces Module 3 (cryptography exercises), rebuilt locally as the simulation and problem/.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`
