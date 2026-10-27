# In-class activity, 5.3.c Integrity and authenticity (HMAC)

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Classify a set of integrity-check designs (plain hash, naive `H(key+message)`, real HMAC) applied
to a tampered vs. untampered message as SECURE or VULNERABLE, and defend the classification by
naming the specific attack (or lack of one) that applies. Ties to LO 5.3.B, 5.3.C.

## Materials (all local)
- the SimLab simulation on each machine, or the printed scenario cards below.
- One "decision sheet" per pair to record classifications and justifications.

## Steps
1. With your partner, open the simulation and work through the scenario queue. For each scenario you
   are shown a design (plain hash / naive concatenation / real HMAC) and a message that may or may
   not have been tampered with in transit. Decide: is this design's integrity check SECURE or
   VULNERABLE against the described attacker?
2. Before submitting an answer in the sim, write one sentence on the decision sheet naming the
   specific weakness (or why there is none): "an attacker can recompute the hash over their own
   tampered message," "vulnerable to length-extension because the digest exposes internal state,"
   or "secure, the attacker cannot produce a valid tag without the shared key."
3. After finishing the sim's scenario queue, sketch the HMAC construction from memory:
   `HMAC(key, message) = H((key XOR opad) || H((key XOR ipad) || message))`, and annotate why
   nesting the hash twice (rather than once, as in naive concatenation) is what defeats length
   extension.

## Collaborate (AP skill 4)
Assign roles: an "attacker" argues how they would tamper with the message and forge a valid
hash/tag under each design, and a "verifier" explains why that attack succeeds or fails for that
specific design. Swap roles halfway through the scenario queue so each partner argues both sides.

## Exit ticket
Each student submits: one design (plain hash, naive `H(key+message)`, or HMAC) they classified,
whether it is SECURE or VULNERABLE, and a one-sentence explanation of what an attacker could (or
could not) do to forge a valid check under that design.

## Instructor notes
- Expected reasoning: plain hash is always VULNERABLE against an attacker who can rewrite both
  the message and its accompanying digest, since hashing is public and keyless. Naive
  `H(key+message)` is VULNERABLE to length-extension attacks even though a secret is involved,
  because Merkle-Damgard hashes (SHA-256 included) expose their internal state as the digest.
  Real HMAC is SECURE because its double-nested construction never exposes a state an attacker
  can extend.
- Common stumble: students think "any design with a secret key is safe." Reinforce that naive
  concatenation still has a real, historically-exploited weakness (length extension), the fix is
  specifically HMAC's nested structure, not just "add a key somewhere."
- Common stumble: conflating integrity with authenticity. A plain hash can offer integrity over a
  channel the attacker cannot tamper with, but never authenticity, since anyone can compute it.
- Feeds the coding problem (`problem/`), which has students implement HMAC-SHA256 by hand
  (ipad/opad nesting) and confirm a single tampered bit changes the tag.
