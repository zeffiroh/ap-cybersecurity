# In-class activity, 5.4.a Public/private key pairs

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Working with a partner, students hand-compute a small-number RSA key pair from two primes, then
correctly classify which key (public or private) is used for four common operations
(send-encrypted, receive-decrypt, sign, verify). Ties to LO 5.4.A.

## Materials (all local)
- the SimLab simulation, or the printed worksheet below, per pair.
- Scratch paper for the arithmetic.

## Steps
1. Each pair is assigned two small primes (e.g. p = 5, q = 11). By hand, compute n = p * q and
   phi(n) = (p-1)(q-1).
2. The pair is given a candidate exponent e (e.g. e = 3) and must verify gcd(e, phi(n)) = 1, then
   search small integers d until they find one where (e * d) mod phi(n) = 1. Record the (e, n)
   public key and (d, n) private key.
3. The pair works through four short scenario cards: "Send Bob a secret message," "Bob reads the
   message you sent," "Sign a document as Bob," "Verify Bob's signature." For each, they write
   down whether the public or private key is used and by whom (sender/receiver/signer/verifier).
4. Pairs open the simulation to check their hand-computed key pair and scenario answers against the
   simulation's self-check, and try the escalating scenario rounds until they reach the target score.

## Collaborate (AP skill 4)
One partner is the "key generator" (does the n / phi(n) / d arithmetic and narrates each step
aloud), the other is the "scenario analyst" (reasons through the four operation cards). Swap roles
for a second prime pair if time allows, and compare answers with a neighboring pair.

## Exit ticket
Each student submits: their pair's (n, phi(n)) values, the (e, d) pair they found, and one sentence
explaining why encrypting with the private key would NOT keep a message confidential.

## Instructor notes
- Expected reasoning: n and phi(n) come directly from p, q; d is the modular inverse of e mod
  phi(n); "encrypt with public / decrypt with private" for confidentiality, "sign with private /
  verify with public" for authenticity.
- Common stumble: students swap which key does what for signing vs. encryption, or think the
  message-sender uses their OWN key rather than the recipient's public key, walk through the
  Alice-to-Bob example from atom.md explicitly.
- Feeds the simulation's scenario-classification rounds and the coding problem (`problem/`), which
  implements the same n / phi(n) / valid-keypair math programmatically.
