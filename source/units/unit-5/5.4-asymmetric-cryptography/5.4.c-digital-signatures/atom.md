# 5.4.c, Digital signatures

> **Unit 5 · 5.4 Asymmetric Cryptography**
> **AP Learning Objective(s):** 5.4.B
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain how a digital signature is created and verified using an
asymmetric key pair and a cryptographic hash, and articulate why a valid signature provides
authenticity, integrity, and non-repudiation in a way that a shared-secret MAC (5.3.c) cannot.

## Lesson
In 5.4.a you learned that a key pair can be used two ways: encrypt with the public key so only the
private-key holder can decrypt, or sign with the private key so anyone with the public key can
verify. This skill is about that second use case, the digital signature, which is the asymmetric
analogue of the HMAC you studied in 5.3.c. Where HMAC uses one shared secret that both sides
possess, a digital signature uses a key pair: only the signer holds the private key, and anyone can
hold the public key. That single structural difference is what unlocks a guarantee HMAC cannot
offer, which this lesson builds up to.

**Why you don't sign the whole message.** A natural first guess is to run the entire message
through RSA's private-key operation directly: signature = message^d mod n. This has two problems.
First, RSA's math operates on numbers smaller than the modulus n, so an arbitrarily long message
would need to be chopped into blocks and signed piece by piece, slow, and it opens structural
attacks (an attacker who can get certain chosen messages signed can sometimes combine the
signatures algebraically to forge a signature on a message that was never actually signed).
Second, signing a large message directly is computationally expensive since RSA exponentiation
cost grows with the size of the input.

**The real flow: hash, then sign.** Real signature schemes fix both problems by never signing the
message itself. Instead:

1. The signer computes a fixed-size digest of the message using a cryptographic hash function, SHA-256, the same hash family from 5.3.b.
2. The signer signs the digest, not the message: `signature = digest^d mod n`, using their private
   exponent d and modulus n from 5.4.b.
3. To verify, anyone with the signer's public key (e, n) recomputes `hash(message)` themselves,
   then recovers the digest the signer actually signed via `digest' = signature^e mod n`, and
   checks that the two match.

Hashing first means the signature is always a fixed, small size regardless of message length, the
expensive RSA operation only ever runs once per signature, and, critically, the hash's avalanche
property (5.3.b) means even a one-bit change to the message produces a completely different digest,
so any tampering is caught by the comparison in step 3.

**The three guarantees.** A signature that verifies successfully gives the verifier three distinct
properties:

- **Authenticity**, the signature could only have been produced by whoever holds the private key
  matching the public key used to verify it. If Bob's public key verifies a signature, only Bob's
  private key could have produced it (assuming that key has not been compromised).
- **Integrity**, because the signature is over a hash of the message, any modification to the
  message after signing changes its hash, which no longer matches the digest recoverable from the
  signature. Verification fails the instant a single byte changes.
- **Non-repudiation**, Bob cannot credibly claim "I never signed that." Only Bob possesses his
  private key, so nobody else could have produced a signature that verifies against his public key.

**Why this beats HMAC (5.3.c).** HMAC gives integrity and authenticity between exactly two parties
who share a secret key, but it gives no non-repudiation. If Alice and Bob share an HMAC key, and
Alice receives a validly-tagged message, she knows it came from "Bob or herself," because either
party holding the shared secret could have produced that exact tag. There is no way to prove to a
third party which of the two actually created it. Digital signatures remove this ambiguity because
signing and verifying use different keys: only the signer can produce a valid signature, but anyone
can verify one. This also lets signatures scale far beyond two parties, a single public key lets
an unlimited number of verifiers check authenticity, whereas HMAC would require a separate shared
secret with every party who needs to verify (and each of those parties could then forge tags for
all the others).

**Where this shows up.** Code signing lets an operating system verify that an installer actually
came from the vendor it claims and was not altered in transit. Signed software updates prevent an
attacker on the network from substituting a malicious update package. S/MIME uses signatures to let
an email recipient verify the sender's identity and detect tampering. TLS certificates (previewed
here, covered fully in 5.4.d) are themselves digitally signed by a certificate authority, which is
what lets a browser trust that a public key really belongs to the website it claims to belong to.

Open the simulation to see several message/signature/public-key combinations and decide whether each
one is VALID or FORGED/TAMPERED, including cases where the message was altered after signing and
cases where the wrong public key was used to verify. The coding problem in `problem/` has you
implement `sign()` and `verify()` directly against small, textbook-scale RSA parameters, using
SHA-256 for the hash step described above.

## Key terms
- **Digital signature**, a value computed from a message digest and a private key that lets
  anyone with the matching public key verify the message's authenticity and integrity.
- **Signing**, computing `signature = hash(message)^d mod n` with the signer's private exponent.
- **Verification**, recomputing `hash(message)` and comparing it to `signature^e mod n`, computed
  with the signer's public exponent.
- **Authenticity**, assurance that a message originated from the claimed sender.
- **Non-repudiation**, the signer cannot plausibly deny having signed, since only they hold the
  private key; a property HMAC (shared-secret) schemes cannot provide.
- **Message digest**, the fixed-size hash output that is actually signed, rather than signing the
  raw message.

## Common misconceptions
- "A digital signature encrypts the message for confidentiality." → It does not provide secrecy at
  all; the message is often sent in the clear alongside the signature. Signing proves authenticity
  and integrity, not confidentiality, that requires separately encrypting with the recipient's
  public key (5.4.a).
- "HMAC and digital signatures provide the same guarantees." → Both give integrity and
  authenticity, but only digital signatures give non-repudiation, because HMAC's shared secret
  means either party could have produced a valid tag.
- "You sign the message directly with RSA." → Real schemes hash the message first and sign the
  fixed-size digest, both for performance and to avoid structural weaknesses in signing large raw
  inputs directly.
- "If verification succeeds, the message was never read by anyone else in transit." → Verification
  proves integrity and authenticity, not secrecy; an unencrypted signed message can still be read
  by anyone who intercepts it.

## Try it
- **Simulation:** Given a message, a claimed signature, and a
  public key, decide VALID or FORGED/TAMPERED across several deterministic cases, and reach the
  target score.
- **Coding problem:** Implement `sign(message, d, n)` and `verify(message, signature,
  e, n)` using SHA-256 digests reduced mod n and modular exponentiation.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (6.875 / cryptography lectures), rebuilt as original prose above; see
  `vendor/web/mit-ocw/`.
- Reference: NIST FIPS 186-5 (Digital Signature Standard).
- Practice: GeeksforGeeks (Digital Signatures overview), rebuilt locally as the simulation
  interactive cases.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
