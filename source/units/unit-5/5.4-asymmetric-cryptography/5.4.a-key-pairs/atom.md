# 5.4.a, Public/private key pairs

> **Unit 5 · 5.4 Asymmetric Cryptography**
> **AP Learning Objective(s):** 5.4.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain how a public/private key pair is generated and used, describe the mathematical relationship between the two keys, and identify which key is used for encryption versus decryption in common asymmetric scenarios.

## Lesson
Every secure interaction on the internet, HTTPS, email signing, SSH login, ultimately depends on a single elegant idea: two mathematically linked numbers, one of which you can hand to anyone in the world, and one of which you keep to yourself forever. This is asymmetric cryptography, and the foundation of the whole system is the key pair.

**The problem that key pairs solve.** In symmetric cryptography (covered in 5.3), both parties must already share a secret key before they can communicate securely. That works well once two parties are connected, but it creates an uncomfortable bootstrap question: how do you share the secret key the first time, over a network where anyone can listen? Asymmetric cryptography sidesteps this entirely. One of your two keys, the public key, can travel over any insecure channel, even be posted on a public web page, without weakening your security at all.

**How a key pair is generated.** The process starts with a hard mathematical problem, one that is easy to compute in one direction and computationally infeasible to reverse without special knowledge. For RSA (covered in 5.4.b), the hard problem is integer factorization: multiplying two large primes is fast, but given only their product, recovering the primes takes an impractical amount of time for large values. Key generation works by:

1. Choosing two large prime numbers, p and q (in practice, hundreds of digits long).
2. Computing their product n = p * q. This number n becomes part of both keys.
3. Deriving a public exponent e (commonly 65537, a prime chosen for efficiency).
4. Computing a private exponent d such that e * d ≡ 1 (mod phi(n)), where phi(n) = (p−1)(q−1). Finding d requires knowing p and q; without them, d cannot be recovered efficiently from e and n alone.

The **public key** is the pair (e, n). The **private key** is the pair (d, n). Both keys share n, they are mathematically linked, but the private key is computationally unrecoverable from the public key alone.

**What each key does.** The keys are asymmetric in function, not just in secrecy:

- **Encrypt with the public key; decrypt with the private key.** If Alice wants to send Bob a secret message, she fetches Bob's public key and uses it to encrypt. Only Bob's private key can reverse that operation. Even Alice, who did the encrypting, cannot decrypt it afterward. This is the foundation of confidential messaging.
- **Sign with the private key; verify with the public key.** If Bob wants to prove he authored a document, he signs it with his private key. Anyone with his public key can verify the signature, and they know only Bob could have produced it (since only he holds the private key). This is the foundation of digital signatures (5.4.c).

These two use cases, confidentiality and authenticity, are the twin pillars of asymmetric cryptography, and they flow directly from the asymmetric structure of the key pair.

**The one-way trapdoor.** A useful mental model is a trapdoor in a floor: easy to fall through in one direction, but impossible to climb back through without a special key. In the RSA case, multiplying p and q is the easy fall; factoring n back into p and q is the locked climb. The private key is the trapdoor mechanism that makes the reverse direction possible for its holder alone. Other asymmetric systems use different one-way problems (discrete logarithms for Diffie-Hellman; elliptic curve discrete logarithms for ECC), but the trapdoor structure is universal.

**Key sizes and security.** The security of a key pair depends on how hard it is to break the underlying one-way problem. Larger key sizes make the problem harder. NIST currently recommends at least 2048-bit RSA keys for general use; 4096-bit keys provide a larger safety margin. Elliptic-curve keys achieve equivalent security at much smaller sizes (256-bit ECC ≈ 3072-bit RSA), which makes them attractive for resource-constrained devices.

**Public key distribution.** The whole system requires that you actually receive the genuine public key of the person you want to communicate with, not an attacker's key that has been substituted. The mechanism for trustworthy distribution of public keys is the public-key infrastructure (PKI, covered in 5.4.d), which uses digital certificates to bind a public key to an identity verified by a trusted third party.

To explore these relationships hands-on, open the simulation: the simulation uses small, textbook-scale key pairs so you can see the arithmetic in action. The coding problem in `problem/` asks you to implement the key generation step from p and q, computing n, phi(n), and validating that a given (e, d) pair is correct for those parameters.

## Key terms
- **Asymmetric cryptography**, a cryptographic system that uses two mathematically linked keys: a public key and a private key.
- **Public key**, the key that can be freely distributed; used to encrypt messages or verify signatures.
- **Private key**, the key kept secret by its owner; used to decrypt messages or create signatures.
- **Key pair**, the matched (public key, private key) set derived together from the same mathematical relationship.
- **One-way trapdoor function**, a function easy to compute in one direction but infeasible to reverse without special information (the trapdoor = private key).
- **Key size**, the bit length of the key; larger sizes increase the difficulty of breaking the underlying mathematical problem.

## Common misconceptions
- "If I encrypt with the private key, it is more secure." → Encrypting with the private key does not provide confidentiality; anyone holding the public key can decrypt. Sign-with-private-key is used for authenticity, not secrecy.
- "The two keys are interchangeable." → They are not: the mathematical relationship is asymmetric. What one key does, only its partner can undo.
- "Publishing your public key lets attackers impersonate you." → Knowing your public key lets an attacker send you encrypted messages or verify your signatures, both harmless. Only possessing your private key would allow impersonation.

## Try it
- **Simulation:** Step through a small-number key-generation example, observe how encryption with the public key is reversed only by the private key, and reach the target score on the self-check questions.
- **Coding problem:** Given prime inputs p and q, compute RSA key parameters (n, phi_n) and verify that a proposed (e, d) pair is valid.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (6.875 / cryptography lectures), rebuilt as original prose above; see `vendor/web/mit-ocw/`.
- Reference: NIST SP 800-56B Rev. 2 (Recommendation for Pair-Wise Key-Establishment Using Integer Factorization Cryptography).
- Practice: GeeksforGeeks (RSA Algorithm overview), rebuilt locally as the simulation interactive steps.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
