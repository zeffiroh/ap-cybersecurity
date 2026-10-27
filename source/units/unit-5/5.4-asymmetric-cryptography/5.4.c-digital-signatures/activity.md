# In-class activity, 5.4.c Digital signatures

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Working with a partner, students hand-trace the hash-then-sign construction for a small RSA key
pair, then classify a set of message/signature/public-key combinations as VALID or
FORGED/TAMPERED, explaining which of authenticity, integrity, or non-repudiation is violated in
each forged case. Ties to LO 5.4.B.

## Materials (all local)
- the SimLab simulation, or the printed worksheet below, per pair.
- Scratch paper for the arithmetic (or a basic calculator, numbers stay small).

## Steps
1. Each pair is given the same small key pair used in `problem/`: `p = 61, q = 53` so
   `n = 3233`, public exponent `e = 17`, private exponent `d = 2753`. Confirm together that this
   is a signing key pair (private `d` signs, public `e` verifies), the reverse roles from
   confidentiality (5.4.a).
2. The pair is given a short message (e.g. `"pay Bob $50"`). Working by hand (or with the simulation
   as a calculator), they compute `digest = SHA-256(message) mod n`, then
   `signature = digest^d mod n`, writing down each intermediate value.
3. To verify, the pair recomputes `digest` from the message independently, then computes
   `recovered = signature^e mod n`, and confirms `digest == recovered`.
4. The pair opens the simulation and works through its set of message/signature/public-key cases,
   classifying each as VALID or FORGED/TAMPERED, including a case where the message was edited
   after signing, and a case where the wrong public key was used to verify. For each FORGED case,
   they write one sentence naming which guarantee (authenticity, integrity, or non-repudiation)
   the forgery would have broken if verification had wrongly said VALID.

## Collaborate (AP skill 4)
One partner is the "signer" (computes the digest and signature, narrates each modular
exponentiation step aloud), the other is the "verifier" (recomputes the digest independently and
checks it against the recovered value). Swap roles for the second case in the simulation and compare
reasoning with a neighboring pair on the trickiest forged case.

## Exit ticket
Each student submits: the (digest, signature) pair they hand-computed, their VALID/FORGED
classification for the simulation's "wrong public key" case, and one sentence explaining why that
case is forged even though the signature itself was never altered.

## Instructor notes
- Expected reasoning: signing uses the private exponent `d`; verification uses the public
  exponent `e`; a tampered message changes the recomputed digest so it no longer matches the
  recovered value; verifying with the wrong public key recovers a different (wrong) digest even
  though the signature bytes are untouched, so it must be classified FORGED.
- Common stumble: students think "the signature itself wasn't changed" means a wrong-public-key
  case should verify as VALID, walk through the fact that `pow(signature, e, n)` depends on
  *which* `(e, n)` you use, so an unrelated key pair recovers an unrelated digest.
- Feeds the simulation's VALID/FORGED classification rounds and the coding problem (`problem/`),
  which implements the same hash-then-sign math programmatically and tests exactly these
  tampered-message and wrong-key scenarios.
