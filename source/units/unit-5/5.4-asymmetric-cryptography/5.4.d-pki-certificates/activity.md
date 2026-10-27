# In-class activity, 5.4.d PKI and digital certificates

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Working with a partner, students trace five printed certificate-chain scenario cards by hand,
decide TRUST or REJECT for each, and write down the specific reason (expired / revoked / broken
chain link / untrusted root / bad signature / valid). Ties to LO 5.4.B, 5.4.C.

## Materials (all local)
- the SimLab simulation, or the printed scenario cards below, per pair.
- A shared "local trust store" card listing one trusted root: `Meridian Root CA -> public_key
  [17, 2773]`.
- Scratch paper.

## Steps
1. Each pair receives the trust-store card and five scenario cards, each showing a leaf-first
   certificate chain (subject, issuer, public key, validity window, revoked flag, and whether the
   signature verifies, pre-computed and shown as true/false so the exercise stays focused on the
   chain logic, not the arithmetic).
2. For each card, the pair walks the chain leaf to root and checks, in order: (a) is the current
   time inside the validity window, (b) is the certificate revoked, (c) does the `issuer` field
   match the next certificate's `subject` (or, for the top cert, is it in the trust store with a
   matching public key), (d) does the signature verify. The first check that fails determines the
   reason; if all pass, the chain is TRUST.
3. The pair records, for each card: TRUST or REJECT, and if REJECT, which single check failed
   first.
4. Pairs open the simulation to check their five answers against the simulation's six scenarios (one
   extra) and read the explanation for any they got wrong.

## Collaborate (AP skill 4)
One partner is the "chain walker" (narrates the leaf-to-root walk aloud, cert by cert), the other
is the "trust store clerk" (checks every top-of-chain subject/key against the trust store card and
calls out any mismatch). Swap roles halfway through the five cards.

## Exit ticket
Each student submits: one scenario card's full reasoning chain in their own words, and one sentence
explaining why a self-signed certificate with a perfectly valid signature can still be correctly
rejected.

## Instructor notes
- Expected reasoning: checks run in a fixed order (validity window, then revocation, then
  issuer/subject linkage or trust-store membership, then signature) and the FIRST failure is the
  reported reason, this mirrors `validate_chain()` in `problem/solution.py`.
- Common stumble: students conflate "signature verifies" with "should be trusted." A self-signed
  cert's signature can verify (it signed itself) while still being untrusted because its subject is
  absent from the trust store, walk through scenario 4 from the simulation explicitly if this comes up.
- Another common stumble: checking the leaf's signature against its OWN public key instead of the
  issuer's (next certificate's) public key. Reinforce: "you never trust a certificate to vouch for
  itself except at the root, and only if the root is already in the trust store."
- Feeds the simulation's six-scenario TRUST/REJECT drill and the coding problem (`problem/`), which
  implements the identical leaf-to-root walk programmatically over real (small-number RSA)
  signatures instead of pre-computed true/false flags.
