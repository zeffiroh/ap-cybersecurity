# In-class activity, 5.4.b RSA algorithm

**Format:** pairs · **Time:** 30 min · **Offline:** yes

## Goal
Working with a partner, students hand-compute a complete RSA round trip from two small primes
through key derivation, encryption, and decryption, confirming by hand that `decrypt(encrypt(m))
== m`. Ties to LO 5.4.A, 5.4.B.

## Materials (all local)
- the SimLab simulation, or the printed worksheet below, per pair.
- Scratch paper for the modular arithmetic (a basic calculator is fine for the exponentiation).

## Steps
1. Each pair is assigned two small primes (e.g. p = 5, q = 11) and computes n = p * q and
   phi(n) = (p-1)(q-1) by hand.
2. The pair is given a candidate public exponent e (e.g. e = 3) and must verify
   gcd(e, phi(n)) = 1, then find d by testing small integers until (e * d) mod phi(n) = 1. This
   is the modular inverse, the same computation `mod_inverse()` performs in `problem/`.
3. The pair picks a message m less than n (e.g. m = 9) and computes the ciphertext
   c = m^e mod n by hand (repeated multiplication and reduction mod n, showing intermediate
   steps rather than jumping straight to a calculator answer).
4. The pair decrypts: m' = c^d mod n, and confirms m' equals the original message m. If it does
   not match, they re-check phi(n), d, or the exponentiation arithmetic before moving on.
5. Pairs open the simulation to check their hand-computed key pair, ciphertext, and decrypted message
   against the simulation, and try the escalating rounds until they reach the target score.

## Collaborate (AP skill 4)
One partner is the "key deriver" (computes n, phi(n), and finds d, narrating the modular-inverse
search aloud), the other is the "cipher operator" (performs the encrypt and decrypt exponentiation
steps). Swap roles for a second prime pair if time allows, and compare final (n, e, d, c) values
with a neighboring pair working the same primes to confirm they agree.

## Exit ticket
Each student submits: their pair's (n, phi(n), e, d) values, the message m and ciphertext c they
computed, and one sentence explaining what part of the process an attacker who only has (e, n)
and c would be unable to redo without the private key.

## Instructor notes
- Expected reasoning: n and phi(n) come directly from p, q; d is the modular inverse of e mod
  phi(n) (verify with (e*d) mod phi(n) == 1); encryption and decryption are the same operation
  (modular exponentiation) with different exponents; the round trip always recovers m exactly.
- Common stumble: students forget m must be less than n, or make an arithmetic slip in the
  repeated-multiplication exponentiation, have them reduce mod n after each multiplication step
  rather than computing the full power first, to keep numbers small.
- Feeds the simulation's encrypt/decrypt rounds and the coding problem (`problem/`), which implements
  the same key derivation, encrypt, and decrypt operations programmatically via modular
  exponentiation.
