# 5.4.b, RSA algorithm

> **Unit 5 · 5.4 Asymmetric Cryptography**
> **AP Learning Objective(s):** 5.4.A, 5.4.B
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Carry out the RSA encrypt and decrypt operations by hand on small numbers (including deriving the private exponent d), and explain why modular exponentiation with a public exponent is easy to compute but infeasible to reverse without the private key.

## Lesson
5.4.a introduced the key pair, (e, n) public, (d, n) private, both built from two primes p and q. This skill is about the actual algorithm that uses those numbers to scramble and unscramble a message: RSA, named for its inventors Rivest, Shamir, and Adleman. Everything RSA does boils down to one operation, applied twice: modular exponentiation.

**The two operations.** Once you have a key pair, RSA defines encryption and decryption as:
- Encrypt: `c = m^e mod n`, raise the message m to the power e, then take the remainder after dividing by n.
- Decrypt: `m = c^d mod n`, raise the ciphertext c to the power d, then take the remainder after dividing by n.

Here m is the plaintext message represented as an integer smaller than n, and c is the resulting ciphertext, also an integer smaller than n. Both operations are the same kind of arithmetic, modular exponentiation, just with a different exponent. What makes RSA work is a theorem from number theory (built on Euler's theorem) guaranteeing that `(m^e)^d mod n = m` whenever d is chosen correctly relative to e, p, and q. Encrypting and then decrypting always returns the original message, but only if you hold the matching d.

**Choosing e and finding d.** The public exponent e is chosen first, and it must satisfy `1 < e < phi(n)` and `gcd(e, phi(n)) = 1` (e and phi(n) share no common factors, so an inverse exists). The private exponent d is then computed as the **modular inverse of e mod phi(n)**: the unique value satisfying `e * d ≡ 1 (mod phi(n))`. Finding d by hand for small numbers can be done by trial, testing small integers until `(e * d) mod phi(n) == 1`, but in practice it is computed with the **extended Euclidean algorithm**, which finds this inverse directly without guessing, and remains fast even when phi(n) has hundreds of digits.

**A full worked example.** Let's pick small primes and walk every step end to end.
1. Choose primes: p = 3, q = 11.
2. Compute n = p * q = 33.
3. Compute phi(n) = (p-1)(q-1) = 2 * 10 = 20.
4. Choose e = 7 (check: gcd(7, 20) = 1, valid).
5. Find d such that (7 * d) mod 20 = 1. Testing d = 3: 7*3 = 21, 21 mod 20 = 1. So d = 3.
6. Public key = (e=7, n=33). Private key = (d=3, n=33).
7. Encrypt message m = 5: c = 5^7 mod 33. 5^7 = 78125. 78125 mod 33 = 14. So c = 14.
8. Decrypt c = 14: m = 14^3 mod 33. 14^3 = 2744. 2744 mod 33 = 5. We recover m = 5. Round trip confirmed.

Notice the message m must be an integer less than n (here, less than 33), in a real system, text is broken into numeric blocks smaller than n before this arithmetic is applied, but the atom-level math is identical to the toy example above.

**Why e = 65537 in practice.** Real RSA implementations almost always use e = 65537 (which is 2^16 + 1) as the public exponent, rather than picking a random small prime like our example's e = 7. Three reasons converge on this choice: it is prime (so gcd(e, phi(n)) = 1 is essentially guaranteed for random large primes p, q), its binary form (a 1 bit, fifteen 0 bits, a 1 bit) makes the repeated-squaring computation of modular exponentiation fast, and it is large enough to defeat certain low-exponent attacks that break RSA when e is very small (e.g., e = 3) and the same message is encrypted to multiple recipients without padding.

**Why this can't be reversed without d.** An attacker who intercepts c and knows the public key (e, n) faces the same wall described in 5.4.a: computing d from e and n requires knowing phi(n), which requires factoring n into p and q. For our toy n = 33 that's trivial, but for a real 2048-bit n, no known classical algorithm can factor it in a feasible amount of time. Modular exponentiation itself is fast in both directions once you know the right exponent, the asymmetry that protects RSA lives entirely in the difficulty of factoring, not in the exponentiation step.

**Looking ahead.** The exact same modular exponentiation operations power digital signatures (5.4.c), just with the roles of the keys reversed: signing raises a message (or its hash) to the power d (private key), and verifying raises the result to the power e (public key) to check it matches. If you are comfortable with `c = m^e mod n` and `m = c^d mod n` here, 5.4.c is largely the same arithmetic applied to a different problem.

The simulation (the simulation) walks you through the same p, q -> n, phi(n) -> e, d pipeline as this lesson, then has you encrypt and decrypt small messages yourself across a few rounds. The coding problem (`problem/`) has you implement the key derivation, encryption, and decryption functions directly with Python's built-in `pow()` for modular exponentiation.

## Key terms
- **RSA**, the asymmetric cryptosystem (Rivest-Shamir-Adleman) built on modular exponentiation and the difficulty of factoring large integers.
- **Modular exponentiation**, computing `base^exponent mod modulus`; the single operation underlying both RSA encryption and decryption.
- **Ciphertext (c)**, the encrypted integer produced by `c = m^e mod n`.
- **Modular inverse**, the value d such that `e * d ≡ 1 (mod phi(n))`; computed via the extended Euclidean algorithm.
- **Extended Euclidean algorithm**, an efficient method for computing modular inverses (and greatest common divisors) without brute-force search.
- **e = 65537**, the near-universal choice of public exponent in real RSA implementations, chosen for primality, computational efficiency, and resistance to low-exponent attacks.

## Common misconceptions
- "Encryption and decryption use different algorithms." → They use the exact same operation, modular exponentiation; only the exponent (e vs. d) and which key it comes from differ.
- "You can pick any e and d as long as they're different." → e and d must satisfy `e * d ≡ 1 (mod phi(n))`; d is mathematically determined by e, p, and q, not chosen freely.
- "Small numbers in the worked example mean RSA is easy to break." → The arithmetic is identical at any size; security comes from using primes hundreds of digits long, where factoring n becomes computationally infeasible, not from the operations themselves being complex.
- "A message can be any size." → In real RSA, m must be a numeric value smaller than n; larger content is chunked or (more commonly) RSA encrypts a symmetric key rather than the full message.

## Try it
- **Simulation:** Walk through deriving n, phi(n), e, and d from given primes, then correctly encrypt and decrypt small messages across several scenario rounds to reach the target score.
- **Coding problem:** Implement RSA key derivation (n, phi_n, d) plus `encrypt()` and `decrypt()` using modular exponentiation.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (6.875 / cryptography lectures), rebuilt as original prose above; see `vendor/web/mit-ocw/`.
- Reference: NIST SP 800-56B Rev. 2 (Recommendation for Pair-Wise Key-Establishment Using Integer Factorization Cryptography).
- Practice: GeeksforGeeks (RSA Algorithm overview), rebuilt locally as the simulation interactive steps.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
