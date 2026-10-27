---
deck:
  title: Asymmetric Cryptography
  kicker: Class 26
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 26
  description: Public/private keys, RSA, certificates, digital signatures, and the PKI trust system holding HTTPS together.
  topics: [Public/Private Keys, RSA, Certificates, Digital Signatures, PKI]
---

%%%
---
title: Asymmetric Cryptography
cover: true
---
:::text class=sub
Mathematical Foundations, Algorithms, and the Public Key Infrastructure (PKI)
:::

:::list style=chips
- Trapdoor Functions
- RSA & ECC Math
- FIPS 186-5 Signatures
- X.509 PKI Trust Chains
:::

:::image src="images/26_cover_asymmetric_overview.png" alt="Two-panel conceptual diagram: left panel shows a single symmetric key shared between Alice and Bob over an insecure channel, right panel shows Alice holding a private key and Bob using Alice's published public key, illustrating the paradigm shift of asymmetric cryptography" caption="Asymmetric cryptography resolves the key distribution dilemma by separating encryption and decryption into a mathematically paired public/private key relationship." width=full
:::

:::notes
Welcome to Class 26. Today we cover asymmetric cryptography, also known as public-key cryptography. This is one of the most significant intellectual breakthroughs in modern computer science, resolving the fundamental key distribution problem that plagued symmetric cryptography for millennia.

To understand why this matters, consider the state of cryptography before 1976. Every secure communication required that both parties already share a secret key. This worked in military and diplomatic contexts where couriers could physically deliver key material, but it was completely impractical for a world of millions of internet users who had never met. The question was: how can strangers communicate secretly over a public, monitored channel? This was the key distribution dilemma, and for over two thousand years, no satisfying solution existed.

The conceptual breakthrough came from Whitfield Diffie and Martin Hellman, who published their landmark 1976 paper "New Directions in Cryptography." Their insight was deceptively elegant: instead of sharing a single secret key, each party generates a mathematically linked key pair. The public key can be shared openly with the world; the private key is kept secret by its owner and never transmitted. A message encrypted with the public key can only be decrypted by the corresponding private key. This asymmetry, the fact that encryption and decryption use different keys, gives the field its name.

In this session, we will explore four foundational pillars. First, we examine the mathematical foundations, trapdoor one-way functions, that make asymmetric cryptography computationally secure. These are number-theory problems, including integer factorization and elliptic curve discrete logarithms, that are easy to compute forward but computationally infeasible to reverse without possessing the private trapdoor value. The entire security of the system rests on the hardness of these specific mathematical problems.

Second, we will walk through the mechanics of two primary algorithms. RSA, specified in RFC 8017, was the first practical implementation of public-key encryption and remains foundational today. Elliptic Curve Cryptography (ECC), specified in NIST SP 800-186, achieves equivalent security at dramatically smaller key sizes, making it ideal for constrained environments such as mobile devices, smart cards, and embedded systems.

Third, we analyze digital signatures as standardized by NIST FIPS 186-5. Digital signatures flip the encryption process to prove authenticity rather than confidentiality. By signing with their private key, an entity creates cryptographic proof that they, and only they, could have authored a message. This underpins the non-repudiation property that makes electronic contracts, code-signing, and software distribution legally and operationally trustworthy.

Fourth, we study the ITU-T X.509 standard, detailed in RFC 5280, which defines the digital certificate format, and the Public Key Infrastructure (PKI) ecosystem that distributes and validates these certificates. PKI is the global trust architecture enabling your browser to verify that a public key belongs to your bank rather than to an attacker performing impersonation. The hierarchical chain of trust from Root Certificate Authorities down to individual server certificates underpins secure commerce and communication at global scale.

By the end of this lecture, you will understand how asymmetric and symmetric systems are combined in TLS 1.3 (RFC 8446) to produce secure, high-performance encrypted connections, using asymmetric cryptography for trust establishment and key exchange, then transitioning to symmetric algorithms for bulk data encryption. This hybrid architecture is the pattern underlying virtually every HTTPS session on the internet today.
:::

%%%
---
unit: Key Exchange
code: KEX
title: The Key Distribution Dilemma
---
:::callout style=soft
Symmetric algorithms like AES (FIPS 197) offer exceptional performance and security, but they rely on a shared secret. If two remote entities must communicate securely over an insecure channel monitored by an active adversary, how can they agree on a symmetric key without exposing it?
:::

::::columns ratio=1:1
::col::
::::card heading="The Symmetric Constraint"
:::list style=tight
- **Shared Secret:** Both parties must possess identical keys prior to encryption.
- **Key Exhaustion:** An $N$-user network requires $N(N-1)/2$ keys.
- **Insecure Medium:** Transmitting a symmetric key directly invites interception.
:::
::::
::col::
::::card heading="The Diffie-Hellman Breakthrough"
:::list style=tight
- **RFC 2631 / RFC 3526:** Establishes public parameters to agree on a secret.
- **Mathematical Shield:** Relies on the Discrete Logarithm Problem (DLP).
- **Ephemerality:** Supports Perfect Forward Secrecy (PFS).
:::
::::
::::

:::image src="images/26_key_distribution_dilemma.png" alt="Diagram showing three scenarios: top row illustrates Alice and Bob exchanging a symmetric key over a network with Eve intercepting it; middle row shows the N-squared key problem with a mesh of users each needing unique shared keys; bottom row shows Diffie-Hellman with public parameters exchanged openly and a shared secret derived independently on each side" caption="The key distribution dilemma: symmetric encryption requires a pre-shared secret, but transmitting that secret over an untrusted network creates the very vulnerability encryption is meant to prevent." width=full
:::

:::notes
To appreciate asymmetric cryptography, we must first understand the crisis that led to its invention. Symmetric cryptosystems like AES, DES, and their predecessors require a shared secret key. The same key is used by the sender to encrypt and by the receiver to decrypt. This approach is highly efficient and produces very strong ciphertext, but it contains a fundamental structural weakness: both parties must already possess the key before they can communicate securely.

In practice, this creates a logical paradox. If Alice and Bob want to communicate securely over the internet for the first time, they need to exchange a key. But any key they transmit over the internet is subject to interception by an eavesdropper, Eve. If Eve captures the key, she can decrypt every subsequent message, defeating the entire purpose of encryption. This is the key distribution dilemma, and it is not a theoretical concern. In World War II, the British exploited exactly this problem to crack the Enigma cipher by obtaining key settings through espionage and captured material.

A secondary issue is key scalability. In a symmetric-only network of N users, every pair of users requires a unique shared key, because sharing a group key means any member can read messages intended for others. This produces a combinatorial explosion: a 10-user network needs 45 unique keys. A 1,000-user network needs 499,500 keys. An enterprise of 50,000 employees would require over 1.2 billion unique pre-shared keys. Distributing, storing, and rotating this quantity of key material is operationally impossible.

In 1976, Whitfield Diffie and Martin Hellman proposed a revolutionary protocol that addresses the exchange problem, formalized in RFC 2631. The Diffie-Hellman Key Exchange allows two parties to establish a shared secret without ever transmitting it. Both parties publicly agree on mathematical parameters, a large prime $p$ and a generator $g$. Each party then selects a private random integer and computes a public value. They exchange public values. Each party then computes the shared secret using their own private integer and the other's public value. Critically, the shared secret is mathematically identical on both sides, yet an eavesdropper who captures both public values cannot derive it efficiently, because doing so requires solving the Discrete Logarithm Problem, one of the computational hard problems that forms the foundation of asymmetric cryptography.

However, the original Diffie-Hellman protocol has one critical limitation: it does not provide authentication. If a man-in-the-middle attacker, Mallory, intercepts the initial exchange, she can establish separate shared secrets with both Alice and Bob, relaying and modifying messages between them while each party believes they are communicating directly. This is the Man-in-the-Middle (MitM) attack on unauthenticated key exchange. Asymmetric encryption solves this gap by introducing authenticated key agreement, where parties can cryptographically prove their identities using digital certificates and private key signatures, a topic we will explore in the later slides of this lecture.

Ephemeral Diffie-Hellman, used in modern TLS 1.3, goes further by generating a fresh key pair for each session. This provides Perfect Forward Secrecy (PFS): even if a private key is compromised in the future, recorded past sessions cannot be decrypted, because each session's secrets are ephemeral and never stored.
:::

%%%
---
unit: Mathematics
code: MATH
title: Mathematical Foundations & Trapdoor Functions
---
:::callout style=soft
The security of asymmetric cryptography rests on **trapdoor one-way functions**: mathematical operations that are computationally easy to perform in one direction but virtually impossible to invert unless one possesses a specific piece of auxiliary data known as the **trapdoor**.
:::

:::table
| Mathematical Problem | Underlying Operation | Inverse Operation (The Hard Problem) | Primary Standards / RFCs |
|---|---|---|---|
| **Integer Factorization** | Multiplication of large primes ($n = p \times q$) | Factoring $n$ into $p$ and $q$ without prior knowledge | RSA (PKCS #1, RFC 8017) |
| **Discrete Logarithms** | Modular exponentiation ($g^x \pmod p$) | Finding exponent $x$ given $g^x \pmod p$ | Diffie-Hellman, DSA |
| **Elliptic Curve Logarithms** | Point multiplication on a curve ($Q = kP$) | Finding scalar multiplier $k$ given $P$ and $Q$ | ECDH, ECDSA (NIST SP 800-186) |
:::

:::image src="images/26_trapdoor_function_diagram.png" alt="Conceptual illustration of a trapdoor function: left side shows a simple downward arrow labeled 'Easy: f(x) = y' with a padlock open; right side shows a steep upward climb labeled 'Hard: find x given y' with a locked padlock; in the center a trapdoor door on the floor represents the private key enabling the easy reverse path" caption="A trapdoor one-way function is computationally easy to compute forward but infeasible to reverse, unless the trapdoor (private key) is known. This mathematical asymmetry is the foundation of all public-key cryptography." width=full
:::

:::notes
Unlike symmetric encryption, which is built on substitution-permutation networks and bitwise operations designed to diffuse and confuse data, asymmetric cryptography is rooted in algebraic number theory. The core concept enabling it is the trapdoor one-way function. Understanding this concept precisely is essential, because it is the mathematical bedrock upon which RSA, ECC, and every other asymmetric system is built.

A one-way function is a function $f$ such that for any input $x$, computing $f(x) = y$ is easy and efficient. However, given $y$, finding any $x$ such that $f(x) = y$ is computationally infeasible, meaning it would require an astronomical number of operations even for the most powerful computers. The term "computationally infeasible" is a formal cryptographic concept: it means that no algorithm exists that can solve the problem in polynomial time with respect to the input size.

A trapdoor one-way function adds one additional property: there exists a special piece of auxiliary information $K$, called the trapdoor, such that computing $f^{-1}(y) = x$ becomes easy if and only if you know $K$. In asymmetric cryptography, this trapdoor is the private key. The entire security of the system depends on keeping $K$ secret and on the mathematical difficulty of solving the inverse problem without it.

We rely on three distinct hard mathematical problems across different asymmetric systems. The first is integer factorization. Multiplying two 1024-bit prime numbers $p$ and $q$ to get their 2048-bit product $n$ takes microseconds on any modern processor. However, given only $n$, recovering $p$ and $q$ is believed to require sub-exponential but still enormous time. Using the best known algorithm, the General Number Field Sieve (GNFS), factoring a 2048-bit RSA modulus would require computational resources exceeding the combined capacity of every computer on Earth for thousands of years. NIST SP 800-131A currently recommends a minimum RSA key size of 2048 bits, transitioning toward 3072 bits for new systems.

The second problem is the discrete logarithm problem (DLP) in modular arithmetic. Given a prime $p$, a generator $g$, and the value $y = g^x \pmod p$, finding $x$ is computationally hard for large $p$. Diffie-Hellman key exchange and the Digital Signature Algorithm (DSA) are both founded on this hardness assumption.

The third problem is the elliptic curve discrete logarithm problem (ECDLP). Point multiplication on an elliptic curve is straightforward: given point $P$ and integer $k$, computing $Q = kP$ is efficient. However, given $P$ and $Q$, finding $k$ is believed to be substantially harder than the integer DLP for equivalent key sizes. This hardness means ECC achieves the same security as RSA with keys roughly six times shorter, drastically reducing computational overhead. NIST SP 800-186 documents approved elliptic curves, including P-256, P-384, and P-521, each offering different security strengths suitable for different applications.

Importantly, these hardness assumptions are computational conjectures, we believe these problems are hard because no efficient algorithms have been found despite decades of research. However, as we will see in the final slide of this lecture, they are not unconditionally hard. Peter Shor's 1994 quantum algorithm can solve both factorization and discrete logarithms in polynomial time on a sufficiently powerful quantum computer, which is why post-quantum cryptography research is now a national security priority.
:::

%%%
---
unit: Algorithms
code: RSA
title: The RSA Cryptosystem Mechanics
---
:::callout style=soft
Patented in 1983 by Rivest, Shamir, and Adleman, **RSA** remains a foundational algorithm for encryption and digital signatures, operating within the multiplicative group of integers modulo $n$.
:::

:::steps
Select two large, distinct prime numbers $p$ and $q$. Compute their product $n = p \times q$, where $n$ is the modulus.
Compute Euler's totient function: $\phi(n) = (p - 1)(q - 1)$.
Choose a public exponent $e$ such that $1 < e < \phi(n)$ and $\gcd(e, \phi(n)) = 1$. Typically, $e = 65537$ is chosen.
Determine the private exponent $d$ as the modular multiplicative inverse of $e$: $d \equiv e^{-1} \pmod{\phi(n)}$.
**Encryption:** Convert message $m$ to integer. Compute ciphertext $c = m^e \pmod n$.
**Decryption:** Compute original message $m = c^d \pmod n$.
:::

:::image src="images/26_rsa_key_generation_steps.png" alt="Step-by-step flowchart of RSA key generation: box 1 shows two large primes p and q; box 2 shows their product n=pq; box 3 shows Euler totient phi(n)=(p-1)(q-1); box 4 shows selection of public exponent e=65537; box 5 shows computation of private exponent d via Extended Euclidean Algorithm; final box splits into Public Key (n,e) and Private Key (n,d)" caption="RSA key generation derives a mathematically paired key pair from two large prime numbers. The public key (n,e) is shared openly; the private key (n,d) must remain secret." width=full
:::

:::notes
Let's break down the mathematical mechanics of RSA in detail. RSA is specified in RFC 8017 (also known as PKCS #1 v2.2) and was originally proposed in 1977 by Ron Rivest, Adi Shamir, and Leonard Adleman at MIT, the initials of their surnames giving the algorithm its name. It was independently discovered slightly earlier by Clifford Cocks at GCHQ, though that discovery remained classified until 1997. RSA was the first practical asymmetric cryptosystem and remains widely used for key encapsulation and digital signatures today.

The algorithm begins with the selection of two massive, statistically independent prime numbers, $p$ and $q$. In practice, these are generated by selecting random integers of the desired bit length and applying probabilistic primality tests such as the Miller-Rabin test. Their product $n = p \times q$ becomes the modulus for both the public and private keys. The length of $n$ in bits is the RSA key length. NIST SP 800-131A mandates a minimum of 2048 bits for systems used beyond 2030, with 3072 bits recommended for new deployments. The key insight is that $n$ can be published publicly; an attacker who knows $n$ cannot easily determine $p$ and $q$, because factoring $n$ is computationally infeasible at these key sizes.

Next, we compute Euler's totient function, $\phi(n)$. Euler's totient counts the integers from 1 to $n-1$ that are coprime to $n$ (share no common factor with $n$). Because $n = p \times q$ and $p$, $q$ are prime, this simplifies elegantly: $\phi(n) = (p-1)(q-1)$. This value is the secret modulus for computing the private key. It must never be published, because knowing $\phi(n)$ would allow any attacker to derive the private key from the public key. In practice, PKCS #1 implementations use the closely related Carmichael function $\lambda(n) = \text{lcm}(p-1, q-1)$ instead, which produces a mathematically equivalent but slightly different private key.

We then select the public exponent $e$. The requirement is that $e$ must be coprime to $\phi(n)$ — that is, $\gcd(e, \phi(n)) = 1$ — ensuring that the modular inverse of $e$ exists. The near-universal choice is $e = 65537$, which equals $2^{16} + 1$ and is a Fermat prime. This value is computationally attractive: when performing modular exponentiation $m^e \pmod n$, the binary representation of $65537$ has only two ones (the most significant and least significant bits), minimizing the number of multiplications required via the square-and-multiply algorithm.

The private exponent $d$ is computed using the Extended Euclidean Algorithm (EEA) to find the modular multiplicative inverse of $e$ modulo $\phi(n)$, satisfying $e \times d \equiv 1 \pmod{\phi(n)}$. The public key is the pair $(n, e)$, which is published openly. The private key is the pair $(n, d)$, which is kept secret.

When Alice encrypts a message $m$ for Bob using Bob's public key $(n, e)$, she computes ciphertext $c = m^e \pmod n$. Only Bob, who knows the trapdoor $d$, can recover the message by computing $c^d \equiv (m^e)^d \equiv m^{ed} \pmod n$. The correctness of decryption is guaranteed by Euler's theorem, which states that $m^{\phi(n)} \equiv 1 \pmod n$ for any $m$ coprime to $n$, so $m^{ed} = m^{k\phi(n)+1} = m$ for some integer $k$.

In practice, RSA is never used to encrypt arbitrary messages directly. Instead, it is used for key encapsulation, encrypting a symmetric key or random seed, or for digital signatures. Direct RSA encryption is also padded using schemes defined in PKCS #1, such as OAEP (Optimal Asymmetric Encryption Padding), to prevent mathematical attacks on the raw modular exponentiation structure.
:::

%%%
---
unit: Algorithms
code: ECC
title: Elliptic Curve Cryptography (ECC)
---
:::callout style=soft
**ECC** offers equivalent cryptographic strength to RSA but with significantly smaller key sizes. This is achieved by mapping cryptographic operations to the algebraic structure of elliptic curves over finite fields.
:::

::::columns ratio=1:1
::col::
::::card heading="ECC Modulo $p$ Curve"
:::code language=mermaid caption="ECC security rests on point multiplication: computing Q=kP is fast, but finding k given P and Q (the ECDLP) is computationally infeasible. The curve equation and the finite field together define the algebraic group in which operations occur."
graph TD
    Curve["y² = x³ + ax + b (mod p)"] --> PointP["Base Point P (Generator, defined in curve standard)"]
    PointP --> Mult["Point Multiplication: Q = kP (private key k applied to generator)"]
    Mult --> Hard["Hard Problem: Find k given P and Q (ECDLP, infeasible for large k)"]
:::
::::
::col::
::::card heading="Key Size & Efficiency (NIST SP 800-57)"
:::table
| RSA Key Size | ECC Key Size | Security Strength |
|---|---|---|
| 1024 bits | 160 bits | Insufficient |
| 2048 bits | 224 bits | Secure (112-bit) |
| 3072 bits | 256 bits | Secure (128-bit) |
| 7680 bits | 384 bits | Secure (192-bit) |
:::
::::
::::

:::image src="images/26_ecc_point_multiplication.png" alt="Geometric visualization of elliptic curve point addition on the curve y²=x³-3x+3: a smooth S-shaped curve over a coordinate grid; a tangent line at point P intersects the curve at a second point, which is reflected across the x-axis to produce point 2P; the process is iterated to show 3P, 4P, illustrating how repeated point addition generates the key Q=kP" caption="Point addition on an elliptic curve: P is added to itself k times to produce Q. Given P and Q, recovering k (the private key) requires solving the Elliptic Curve Discrete Logarithm Problem, which is computationally infeasible for NIST-approved curve parameters." width=half
:::

:::notes
While RSA is mathematically elegant and remains important in practice, its key sizes must grow near-exponentially to counter improvements in factorization algorithms like the General Number Field Sieve. This creates performance overhead: larger keys mean more time spent on modular exponentiation during handshakes, more bits to transmit, and more power consumed on embedded devices. Elliptic Curve Cryptography, standardized in NIST SP 800-186 and SP 800-57, was developed to provide equivalent cryptographic strength at dramatically reduced key sizes.

Rather than working with integers in modular arithmetic, ECC defines operations on the set of points satisfying a curve equation of the form $y^2 = x^3 + ax + b$ over a finite field. The specific curves approved by NIST, such as P-256 (secp256r1), P-384, and P-521, are defined with carefully chosen coefficients $a$ and $b$, as well as a prime modulus $p$ that determines the field size. These parameters were selected to resist known attacks and to have a large prime order, meaning the group of points is as large as possible.

A key pair is generated as follows. The curve standard defines a base point $G$ (also called the generator point), which is a specific point on the curve with known coordinates. The private key is a randomly selected large integer $k$ in the range $[1, n-1]$, where $n$ is the order of the group (the number of distinct points). The public key is the point $Q = kG$, computed by adding $G$ to itself $k$ times using the rules of elliptic curve point arithmetic.

Elliptic curve point addition has a beautiful geometric interpretation. For two distinct points $P$ and $Q$ on the curve, a line through $P$ and $Q$ intersects the curve at exactly one other point. Reflecting that point across the x-axis gives the sum $P + Q$. Point doubling adds a point to itself by finding the tangent at $P$, intersecting the curve, and reflecting the result. Applying these rules $k$ times with efficient double-and-add algorithms (analogous to square-and-multiply in RSA) computes $Q = kG$ in $O(\log k)$ steps.

The security rests on the Elliptic Curve Discrete Logarithm Problem (ECDLP): given both $G$ and $Q$, find $k$. Unlike integer factorization, where the structure of the problem allows sub-exponential attacks via the GNFS, the best known algorithms for ECDLP run in fully exponential time with respect to the key size. This means a 256-bit ECC key provides the same 128-bit security level as a 3072-bit RSA key. A 384-bit ECC key matches a 7680-bit RSA key.

This size advantage translates directly into performance. ECDHE (Elliptic Curve Diffie-Hellman Ephemeral) handshakes are substantially faster than RSA-based equivalents, which is why TLS 1.3 mandates ECDHE for key exchange and why ECC is the algorithm of choice for modern deployments. NIST-approved curves are used in ECDSA (the Elliptic Curve Digital Signature Algorithm, specified in FIPS 186-5), ECDH for key agreement, and in embedded and mobile contexts where power efficiency is critical.

One important consideration: the security of ECC depends on the choice of curve. The use of NIST-standardized curves is recommended over custom or proprietary ones; historically, curves with poorly chosen parameters (such as those using a backdoored random number generator, as suspected in the case of Dual_EC_DRBG) can have weaknesses inserted by an adversary.
:::

%%%
---
unit: Trust
code: DSIG
title: Digital Signatures & Non-Repudiation
---
:::callout style=soft
A **digital signature** is a cryptographic mechanism that binds an identity to a message. Under **NIST FIPS 186-5**, digital signatures provide three security guarantees: authenticity, non-repudiation, and message integrity.
:::

:::flow
Alice hashes the plaintext message: $h = H(m)$ using SHA-256
Alice encrypts the hash with her private key to generate the signature: $s = \text{Encrypt}_{Priv}(h)$
Alice transmits the message $m$ and the signature $s$ to Bob
Bob hashes the received message: $h' = H(m)$
Bob decrypts the signature using Alice's public key: $h'' = \text{Decrypt}_{Pub}(s)$
Bob compares $h'$ and $h''$; if they match, the signature is verified
:::

:::image src="images/26_digital_signature_flow.png" alt="Two-lane diagram: left lane labeled 'Signing (Alice)' shows message M entering a SHA-256 hash function producing digest H, then H encrypted with Alice's private key producing signature S; right lane labeled 'Verification (Bob)' shows received message M re-hashed, and signature S decrypted with Alice's public key, and the two digests compared with a green checkmark for match or red X for failure" caption="Digital signature creation and verification: Alice signs with her private key; Bob verifies with Alice's public key. A mismatch in digests indicates either tampering or a wrong key." width=full
:::

:::notes
Digital signatures are the cryptographic equivalent of a handwritten signature but with considerably stronger security properties, because they are mathematically bound to both the signer's identity and the specific content of the document being signed. They are defined under NIST FIPS 186-5, which specifies three approved signature algorithms: DSA (now deprecated for new systems), RSA-based signatures under PKCS #1, and the Elliptic Curve Digital Signature Algorithm (ECDSA).

The signing process deliberately inverts the typical encryption workflow. In standard asymmetric encryption, Alice uses Bob's public key to encrypt a message, ensuring only Bob can decrypt it. In digital signing, Alice uses her own private key to produce the signature. Because only Alice possesses her private key, any signature that successfully verifies against Alice's public key proves that it came from Alice, or from someone who compromised her private key.

The three security properties delivered by digital signatures are distinct and important. First, message integrity: the signature is computed over a cryptographic hash of the message, not the message itself. When Bob verifies the signature, he independently hashes the message he received. If any bit of the message changed during transit, whether by malicious tampering or transmission error, his computed hash will not match the decrypted signature value, and verification will fail. Secure hash functions like SHA-256 and SHA-384 are designed to be collision-resistant, meaning it is computationally infeasible to find two different messages that produce the same hash.

Second, authenticity: the verification step uses Alice's public key, which is widely available. A signature that verifies correctly against Alice's public key proves that whoever created the signature had access to Alice's corresponding private key. Under the assumption that Alice has protected her private key, this proves the message came from Alice.

Third, non-repudiation: because only Alice could have produced the signature (assuming private key integrity), she cannot later deny having signed the message. Non-repudiation is a critical legal and compliance property. It is what makes digital signatures legally binding in frameworks like the U.S. ESIGN Act, the EU eIDAS regulation, and many international equivalents. It is also fundamental to code-signing, where developers sign software releases so users can verify that executables have not been modified since publication.

Why do we hash before signing? Signing an entire multi-megabyte document directly would require applying the slow asymmetric mathematical operation to potentially gigabytes of data. By first reducing the document to a fixed-size hash digest, 256 bits for SHA-256, 384 bits for SHA-384, we sign only 32 or 48 bytes regardless of document size, while retaining all three security properties. SHA-256 is the minimum hash algorithm approved for use with FIPS 186-5 signatures; SHA-1 and MD5 are cryptographically broken and must not be used.

Real-world applications include TLS certificate validation (the CA signs the certificate with its private key), software packages (vendors sign package hashes to prevent tampering), email security (S/MIME and PGP use digital signatures to authenticate sender identity), and financial systems (transaction approval requires digital signatures proving authorization).
:::

%%%
---
unit: Trust
code: X509
title: Digital Certificates & the X.509 Standard
---
:::callout style=soft
A public key is useless if its owner's identity cannot be verified. The **ITU-T X.509 standard** (RFC 5280) defines the format of **digital certificates**, which act as digital identity credentials binding a public key to an entity.
:::

::::columns ratio=1:2
::col::
:::list style=chips
- Subject Name
- Issuer (CA)
- Serial Number
- Validity Period
- Public Key Info
- Signature Algorithm
- CA Digital Signature
:::
::col::
:::table
| Certificate Field | Technical Description (RFC 5280) |
|---|---|
| **Subject** | The distinguished name (DN) of the certificate owner (e.g., CN=example.com) |
| **Issuer** | The Certificate Authority (CA) that validated the subject and signed the certificate |
| **Validity** | The NotBefore and NotAfter date stamps defining the active lifespan |
| **Subject Public Key** | The specific public key algorithm and raw key parameter block |
| **Signature Value** | The cryptographic signature generated by the Issuer's private key |
:::
::::
::::

:::image src="images/26_x509_certificate_anatomy.png" alt="Annotated diagram of an X.509 v3 digital certificate rendered as a document with colored callout arrows: Version field labeled 'v3 supports extensions'; Serial Number field labeled 'uniquely identifies cert within CA'; Validity Period showing NotBefore and NotAfter timestamps; Subject field showing CN=example.com O=Example Corp; Subject Public Key Info showing RSA 2048-bit key; Extensions block showing SAN, Key Usage; Signature Algorithm showing SHA256withRSA; Signature Value at the bottom labeled 'CA-signed digest proves authenticity'" caption="Anatomy of an X.509 v3 digital certificate as defined in RFC 5280. The CA's digital signature over all other fields binds the subject's identity to their public key." width=full
:::

:::notes
We have established that public keys can be distributed openly. However, this openness creates a significant impersonation vulnerability. If Mallory generates an RSA key pair and publishes the public key claiming it belongs to your bank, any user encrypting sensitive data for the bank would unknowingly send it to Mallory instead. Without a trusted mechanism to verify that a public key genuinely belongs to the entity claiming it, asymmetric cryptography is vulnerable to widespread impersonation attacks.

Digital certificates, formatted according to the ITU-T X.509 standard and detailed in RFC 5280, solve this problem by introducing a trusted third party: the Certificate Authority (CA). A digital certificate is essentially a signed identity document. It binds a specific public key to a specific entity, identified by a Distinguished Name (DN), by having a trusted CA sign the entire certificate using its own private key. When you receive a certificate, you verify the CA's signature to confirm authenticity.

The X.509 certificate format has evolved through several versions. X.509 v3, the current standard, adds a rich extensions framework that enables advanced use cases. The Subject Alternative Name (SAN) extension allows a single certificate to cover multiple domain names or IP addresses, which is how wildcard certificates (e.g., *.example.com) work. The Key Usage extension specifies the permitted operations for the public key, whether it can be used for digital signatures, key encapsulation, certificate signing, or a combination. The Extended Key Usage extension further constrains the certificate to specific application protocols, such as TLS server authentication or code signing.

The Validity Period deserves particular attention. Certificates are intentionally short-lived. The NotBefore and NotAfter fields bound the certificate to a specific operational window, after which it is considered expired. This limits the window during which a compromised private key can be abused. Modern best practice, strongly recommended by standards organizations and enforced by major browsers, is to issue TLS certificates with a maximum validity of 90 days. Certificate Authorities like Let's Encrypt issue 90-day certificates by default and provide automated renewal tools. Shorter lifetimes reduce the blast radius of key compromise and push organizations toward automated certificate management.

The Issuer field contains the Distinguished Name of the CA that signed the certificate. When your browser receives a certificate from a web server, it examines the Issuer to determine which CA signed it, then looks for that CA's certificate in its trusted store. This chain of trust is the foundation of the PKI system we will explore in the next slide. Certificate Transparency (RFC 6962) adds an additional layer of accountability: CAs are required to log every certificate they issue to public, append-only logs, allowing automated monitoring for mis-issued certificates.

Certificate revocation addresses the scenario where a certificate must be invalidated before its expiry date, most commonly because the private key has been compromised or the certificate was issued fraudulently. RFC 5280 defines Certificate Revocation Lists (CRLs), which are periodically published lists of serial numbers of revoked certificates, signed by the CA. RFC 6960 defines the Online Certificate Status Protocol (OCSP), which enables real-time status queries. Modern browsers implement OCSP Must-Staple, requiring servers to proactively include a fresh OCSP response with every TLS handshake, eliminating the delay of a separate revocation check.
:::

%%%
---
unit: Infrastructure
code: PKI
title: Public Key Infrastructure (PKI) Trust Chains
---
:::callout style=soft
**PKI** is the hardware, software, policies, and personnel required to create, manage, distribute, store, and revoke digital certificates. Trust in PKI is established hierarchically.
:::

:::code language=mermaid caption="The PKI trust hierarchy: Root CAs are explicitly trusted by operating systems and browsers via pre-installed root stores. Intermediate CAs are signed by Root CAs and do the day-to-day work of certificate issuance. Leaf certificates are signed by Intermediate CAs and installed on end servers. Revocation is handled via CRLs or OCSP lookups. This hierarchy means that compromising any single Intermediate CA exposes only the subset of certificates it issued, not the entire PKI ecosystem."
graph TD
    Root["Root CA (Self-signed, trusted in browser root store)"] --> Intermediate["Intermediate CA (Signed by Root CA)"]
    Intermediate --> Leaf["Leaf/End-Entity Certificate (Signed by Intermediate CA, e.g., web server)"]
    
    subgraph Revocation Check
        CRL["Certificate Revocation List (CRL)"]
        OCSP["Online Certificate Status Protocol (RFC 6960)"]
    end
:::

:::image src="images/26_pki_trust_chain.png" alt="Hierarchical tree diagram showing PKI chain of trust: at the top is a Root CA in a vault icon labeled 'offline, air-gapped, physically secured'; below it are two Intermediate CAs labeled 'online, issues leaf certs'; below each Intermediate are several Leaf Certificates for domains like bank.com and shop.com; connecting lines show 'signs' relationships; a side panel shows the browser checking the chain from leaf up to root against its local root store; a revocation arrow shows OCSP query to CA" caption="The PKI trust hierarchy in practice: Root CAs are kept offline for security. Intermediate CAs handle day-to-day certificate issuance. Browsers validate the complete chain from leaf to root." width=full
:::

:::notes
Public Key Infrastructure is the structural ecosystem that makes digital certificates operationally viable at global internet scale. PKI provides the organizational and technical framework for the entire lifecycle of digital certificates: generation, issuance, distribution, renewal, and revocation. It is not a single product or system but a collection of standards, roles, policies, and protocols working in coordination.

The PKI trust model is hierarchical. At the apex of this hierarchy sits the Root Certificate Authority. Root CAs are special in that their certificates are self-signed, there is no higher authority to vouch for them. Instead, their trustworthiness is established by the fact that operating system vendors and browser makers explicitly choose to include their public keys in a pre-installed root store. Microsoft, Apple, Mozilla, and Google each maintain their own root programs with strict admission criteria. Being included in these root programs requires CAs to meet detailed technical and policy requirements, including annual WebTrust audits by accredited external auditors.

Because Root CA private keys are the ultimate source of trust in the entire hierarchy, they are protected with extraordinary physical and logical security measures. Root CA operations are conducted in purpose-built, access-controlled facilities with multi-person authentication requirements (often requiring multiple key holders to be physically present simultaneously), Hardware Security Modules (HSMs) to store private keys in tamper-resistant hardware, and offline key storage, the root key is never connected to a network. Entire certificate issuance ceremonies are conducted offline with detailed ceremony scripts and independent witnesses.

For day-to-day certificate issuance, Root CAs sign the certificates of Intermediate Certificate Authorities (also called Subordinate CAs). Intermediate CAs are online and perform the actual work of validating domain ownership, issuing certificates to customers, and maintaining revocation lists. Using intermediates provides a critical security benefit: if an Intermediate CA's private key is compromised, only the certificates it issued are at risk. The Root CA can revoke the Intermediate CA's certificate, limiting the blast radius. In contrast, a Root CA compromise would undermine trust in every certificate in the hierarchy.

Your browser validates a certificate by building and verifying the complete chain of trust. Starting with the server's leaf certificate, the browser reads the Issuer field and locates the Intermediate CA's certificate (often provided by the server in the TLS handshake). It verifies the Intermediate's signature over the leaf certificate. It then checks the Intermediate's Issuer field and locates the Root CA's certificate in its local root store. It verifies the Root CA's signature over the Intermediate certificate. If every signature is valid, no certificate is expired, and no certificate is listed as revoked, the chain is trusted and the secure connection proceeds.

Revocation is a critical PKI function. When a private key is compromised, the corresponding certificate must be revoked before its expiry date. Certificate Revocation Lists (CRLs), defined in RFC 5280, are periodically published, CA-signed lists of revoked serial numbers. Browsers and operating systems can download CRLs, but they can be large and may lag behind real-time events. OCSP (Online Certificate Status Protocol, RFC 6960) provides real-time revocation checking by querying a CA-operated OCSP responder for a specific certificate's status. Certificate Transparency (RFC 9162) adds public, append-only logs of all issued certificates, enabling security researchers and domain owners to detect unauthorized certificates issued for their domains.
:::

%%%
---
unit: Synthesis
code: TLS
title: Hybrid Cryptography in TLS 1.3
---
:::callout style=soft
Asymmetric cryptography is computationally heavy (100 to 1000 times slower than symmetric encryption). **TLS 1.3** (RFC 8446) resolves this by using asymmetric cryptography for key agreement and authentication, then transitioning to symmetric cryptography for bulk data transfer.
:::

:::steps
**Client Hello:** Client sends supported cryptographic suites (e.g., ECDHE, AES-GCM) and a key share.
**Server Hello:** Server selects parameters, sends its key share, digital certificate, and digital signature.
**Key Agreement:** Both parties compute the shared secret using ECDH. The asymmetric phase is now complete.
**Symmetric Session:** A symmetric session key is derived (e.g., AES-256-GCM) to encrypt all subsequent application data.
:::

:::image src="images/26_tls_handshake_hybrid.png" alt="Two-column timeline diagram showing TLS 1.3 handshake: left column labeled 'Client' and right column labeled 'Server' with horizontal arrows showing message flow; arrow 1 from Client to Server labeled 'ClientHello: key share, cipher suites'; arrow 2 from Server to Client labeled 'ServerHello: key share, certificate, signature, Finished'; a horizontal dashed line after arrow 2 labeled 'Asymmetric Phase Complete, Shared Secret Derived'; arrows below show AES-GCM encrypted Application Data flowing in both directions labeled 'Symmetric Phase: high-speed encrypted data'" caption="TLS 1.3 handshake: the asymmetric phase (ECDHE key exchange + certificate authentication) establishes a shared secret in a single round trip. The symmetric phase (AES-256-GCM) handles all subsequent data at high speed." width=full
:::

:::notes
Asymmetric cryptographic operations are computationally expensive. RSA encryption and decryption require modular exponentiation with very large integers; even ECC, which is faster, involves multiple elliptic curve point multiplication operations. Benchmarks show that asymmetric operations run 100 to 1000 times slower than symmetric operations like AES-GCM. If a server streaming 4K video had to use RSA to encrypt every packet, it would be completely unable to sustain throughput. This is why modern secure communications use a hybrid model.

Transport Layer Security 1.3, defined in RFC 8446 and published in 2018, is the definitive modern example of hybrid cryptography in action. TLS 1.3 represents a major redesign over its predecessors. TLS 1.2 required two full round trips before data could flow; TLS 1.3 completes the handshake in a single round trip, and supports 0-RTT resumption for returning clients. TLS 1.2 supported many legacy algorithm combinations including RC4, DES, and SHA-1 based cipher suites; TLS 1.3 removes all these, mandating only modern authenticated encryption with associated data (AEAD) cipher suites.

The TLS 1.3 handshake proceeds as follows. In the ClientHello message, the client announces which cipher suites it supports (for example, TLS_AES_256_GCM_SHA384 with ECDHE using P-384) and proactively sends a key share, an ECDHE public key, for each group it supports. The server receives the ClientHello, selects the strongest mutually supported cipher suite, and responds with its own ECDHE key share, its X.509 digital certificate, and a digital signature over the handshake transcript using its private key. The server immediately derives the session key and sends an encrypted Finished message.

Both parties independently compute the ECDHE shared secret using the exchanged key shares. This secret is then processed through the TLS key schedule, a series of HKDF (HMAC-based Key Derivation Function) operations, to derive separate symmetric keys for encryption in each direction. From this point forward, all application data is encrypted with AES-256-GCM or ChaCha20-Poly1305, both of which are AEAD ciphers providing both confidentiality and integrity in a single pass.

The use of ephemeral key shares (the E in ECDHE) is essential for Perfect Forward Secrecy. Each TLS 1.3 session uses a freshly generated, ephemeral ECDHE key pair that is discarded after the handshake. This means that even if an attacker records encrypted TLS sessions now and later compromises the server's long-term private key, they cannot decrypt the recorded sessions. The session keys were derived from ephemeral material that no longer exists. This property is critical given that nation-state adversaries are known to conduct "record now, decrypt later" collection campaigns against encrypted traffic.

TLS 1.3 also authenticates the server, and optionally the client, through the digital certificate mechanism. When the client receives the server's certificate, it validates the chain of trust against its root store using the PKI mechanisms discussed in the previous slides. The server's digital signature over the handshake transcript proves that the server possessing the private key corresponding to the certificate's public key is the one you are talking to, preventing man-in-the-middle attacks. TLS 1.3 thus elegantly combines the scale and trust of asymmetric PKI with the performance efficiency of symmetric AEAD ciphers, achieving confidentiality, integrity, and authenticity at internet scale.
:::

%%%
---
unit: Summary
code: SUM
title: Cryptographic Agility & The Quantum Horizon
---
:::callout style=soft
The mathematical assumptions protecting RSA and ECC will not hold forever. Cryptographic agility is the capacity to transition to new algorithms without replacing the underlying application infrastructure.
:::

::::columns ratio=1:1
::col::
::::card heading="Shor's Algorithm & Threat"
:::list style=tight
- **The Quantum Risk:** Shor's algorithm solves prime factorization and discrete logarithms in polynomial time.
- **Vulnerable Algorithms:** RSA, ECC, DH, and ECDSA will be completely broken.
- **Symmetric Safety:** AES-256 remains secure (requires Grover's algorithm search).
:::
::::
::col::
::::card heading="Post-Quantum Cryptography (PQC)"
:::list style=tight
- **NIST PQC Standardization:** Initiated to select quantum-resistant algorithms.
- **Lattice-Based Math:** Hard problems based on high-dimensional vector spaces.
- **Standards:** ML-KEM (key encapsulation) and ML-DSA (signatures).
:::
::::
::::

:::image src="images/26_quantum_threat_timeline.png" alt="Timeline graphic showing three eras: left section labeled 'Classical Era (now)' with RSA and ECC icons marked as secure; center section labeled 'Harvest Now / Decrypt Later Threat' showing adversaries recording encrypted traffic today; right section labeled 'Post-Quantum Era' showing ML-KEM and ML-DSA icons; a vertical dashed line in the center is labeled 'Cryptographically Relevant Quantum Computer (CRQC)' with an arrow pointing right; below the timeline a bar chart compares classical vs quantum algorithm complexity" caption="The quantum cryptographic threat timeline: today's encrypted traffic is being archived for future decryption. Organizations must begin post-quantum migration before CRQCs become operational." width=full
:::

:::notes
We conclude today's class by examining the long-term horizon of asymmetric cryptography. The entire security of RSA, ECC, Diffie-Hellman, and ECDSA depends on the computational hardness of specific mathematical problems. For classical computers, these problems remain intractable at recommended key sizes. However, the emergence of quantum computing introduces an existential threat to these hardness assumptions.

In 1994, mathematician Peter Shor published a quantum algorithm, now known as Shor's algorithm, that can solve both the integer factorization problem and the discrete logarithm problem (including the elliptic curve variant) in polynomial time on a quantum computer. Unlike classical algorithms, which require exponential or sub-exponential time, Shor's algorithm operates in $O((\log n)^3)$ time. This means that a sufficiently powerful quantum computer could factor a 2048-bit RSA modulus in minutes or hours rather than millions of years. Every asymmetric algorithm discussed in today's lecture, RSA, ECDH, ECDSA, DSA, would become completely broken.

The critical question is timeline. Current quantum computers, even the most advanced systems from IBM and Google, operate with dozens to hundreds of noisy qubits. Breaking RSA-2048 is estimated to require millions of error-corrected logical qubits. Building a Cryptographically Relevant Quantum Computer (CRQC) of this scale involves extraordinary engineering challenges: qubit coherence times, error correction overhead, and physical cooling requirements remain formidable barriers. Expert estimates vary widely, with most projecting CRQCs are still 10 to 20 years away, though some assess a non-trivial probability within 10 years.

This timeline uncertainty itself creates a present danger known as "harvest now, decrypt later" (HNDL) attacks. Nation-state intelligence agencies are believed to be recording large volumes of encrypted network traffic today, archiving it for future decryption once quantum capability matures. Data that must remain confidential for decades, classified government communications, long-term financial records, medical histories, is therefore at risk even if CRQCs do not exist today.

In response, NIST launched the Post-Quantum Cryptography (PQC) standardization process in 2016, evaluating over 80 candidate algorithms. In 2024, NIST published the first set of finalized PQC standards. ML-KEM (Module-Lattice-Based Key Encapsulation Mechanism, from the CRYSTALS-Kyber submission) is standardized as FIPS 203 for key exchange. ML-DSA (Module-Lattice-Based Digital Signature Algorithm, from CRYSTALS-Dilithium) is standardized as FIPS 204 for digital signatures. These algorithms are based on the hardness of lattice mathematical problems, specifically the Learning With Errors (LWE) problem, which are believed to resist both classical and quantum attacks.

For symmetric algorithms, the quantum threat is less severe. Grover's algorithm can search an unsorted database of $N$ items in $\sqrt{N}$ steps, effectively halving the security strength of symmetric keys. AES-128 would provide only 64-bit security against a quantum attacker; AES-256 would provide 128-bit security, which remains adequate. Therefore, existing symmetric infrastructure requires only key length upgrades, not algorithm replacement.

Cryptographic agility is the organizational and technical capacity to swap cryptographic algorithms without rebuilding underlying applications. Organizations must begin building PQC readiness now: identifying all systems that use asymmetric cryptography, evaluating their exposure to HNDL attacks, and testing hybrid TLS configurations that combine classical and post-quantum key exchange. NIST SP 800-208 and the NSA's CNSA 2.0 suite provide roadmaps for this transition. Thank you, and I will see you in the next class, where we put these cryptographic tools into their broader architectural context.
:::

%%%
---
unit: Key Exchange
code: DH-DEEP
title: Diffie-Hellman Key Exchange, Step-by-Step Worked Example
---
:::callout style=soft
A **worked example** of Diffie-Hellman Key Exchange using small numbers makes the algebraic structure concrete. In production, the prime modulus $p$ is at least 2048 bits (RFC 3526 Group 14), but the logic is identical.
:::

:::steps
**Agree on public parameters:** Alice and Bob publicly agree on prime $p = 23$ and generator $g = 5$.
**Alice chooses private key:** $a = 6$. Computes public value $A = g^a \bmod p = 5^6 \bmod 23 = 8$. Sends $A = 8$ to Bob.
**Bob chooses private key:** $b = 15$. Computes public value $B = g^b \bmod p = 5^{15} \bmod 23 = 19$. Sends $B = 19$ to Alice.
**Alice computes shared secret:** $s = B^a \bmod p = 19^6 \bmod 23 = 2$.
**Bob computes shared secret:** $s = A^b \bmod p = 8^{15} \bmod 23 = 2$.
**Result:** Both Alice and Bob independently arrive at $s = 2$ without ever transmitting it. Eve, who only knows $p=23$, $g=5$, $A=8$, $B=19$, must solve the discrete logarithm to find $a$ or $b$ — computationally infeasible at real key sizes.
:::

:::image src="images/26_dh_worked_example.png" alt="Color-coded diagram of the Diffie-Hellman worked example: two columns, Alice on left and Bob on right; shared public row shows p=23 and g=5 in green; Alice's private secret a=6 shown in red, her computation 5^6 mod 23=8 in blue arrow going right; Bob's private secret b=15 shown in red, his computation 5^15 mod 23=19 in blue arrow going left; bottom row shows both independently computing the shared secret s=2 highlighted in gold; Eve in the middle can only see the blue values" caption="Diffie-Hellman Key Exchange illustrated with small numbers: both parties converge on the same shared secret using only their own private value and the other's public value, without ever transmitting the secret." width=full
:::

:::notes
Walking through a concrete numerical example dramatically aids understanding of Diffie-Hellman. The numbers here are deliberately small enough to compute by hand; in production RFC 3526 specifies standardized MODP groups with primes of 1536 to 8192 bits, and RFC 7919 defines FFDHE groups for TLS.

Start with the shared public parameters. Both Alice and Bob agree on a prime modulus $p = 23$ and a generator $g = 5$. These parameters are public and can be transmitted in the clear. The security of the scheme does not depend on their secrecy; it depends only on the hardness of the discrete logarithm problem in the group they define.

Alice selects her private key $a = 6$ at random and keeps it secret. She computes her public value $A = 5^6 \bmod 23$. Working through the modular arithmetic: $5^1 = 5$, $5^2 = 25 \equiv 2$, $5^3 = 10$, $5^6 = (5^3)^2 = 100 \equiv 100 - 4 \times 23 = 8$. Alice transmits $A = 8$ to Bob over an insecure channel.

Bob selects his private key $b = 15$ at random. He computes $B = 5^{15} \bmod 23$. Using repeated squaring: $5^8 \equiv 16$, $5^4 \equiv 4$, $5^2 \equiv 2$, $5^1 \equiv 5$; then $5^{15} = 5^8 \cdot 5^4 \cdot 5^2 \cdot 5^1 \equiv 16 \cdot 4 \cdot 2 \cdot 5 = 640 \equiv 640 - 27 \times 23 = 19$. Bob transmits $B = 19$ to Alice.

Now Alice computes $s = B^a \bmod p = 19^6 \bmod 23$. And Bob independently computes $s = A^b \bmod p = 8^{15} \bmod 23$. Both arrive at $s = 2$ — the shared secret, through different computations using only their own private key and the other party's public value. The mathematical property guaranteeing this is: $B^a = (g^b)^a = g^{ab} = (g^a)^b = A^b \pmod p$.

Eve, who intercepts all traffic, knows only $p = 23$, $g = 5$, $A = 8$, and $B = 19$. To recover the secret, she must either find $a$ such that $5^a \equiv 8 \pmod{23}$ or find $b$ such that $5^b \equiv 19 \pmod{23}$ — this is the discrete logarithm problem. With these tiny toy numbers, brute force is trivial. But with a 3072-bit prime (RFC 3526 Group 15), an adversary would need to evaluate roughly $2^{128}$ operations using the best known algorithms. At a rate of a trillion operations per second, this would take longer than the age of the universe.

Computing a Diffie-Hellman exchange by hand with small parameters makes the algebra tangible. If one party reuses a private exponent across sessions, perfect forward secrecy is lost, because a future compromise of that exponent allows decryption of all past sessions, which is why TLS 1.3 uses ephemeral Diffie-Hellman (DHE/ECDHE).
:::

%%%
---
unit: Algorithms
code: RSA-PADDING
title: RSA Padding Schemes, PKCS#1 v1.5 vs OAEP
---
:::callout style=soft
Raw RSA encryption is **mathematically malleable** and deterministic: encrypting the same plaintext always yields the same ciphertext. Padding schemes defined in **RFC 8017 (PKCS #1 v2.2)** add randomness and structural checks that prevent whole classes of chosen-ciphertext attacks.
:::

::::columns ratio=1:1
::col::
::::card heading="PKCS#1 v1.5 Padding (Legacy)"
:::list style=tight
- **Structure:** 0x00 || 0x02 || PS || 0x00 || M
- **Vulnerability:** Bleichenbacher (1998) padding oracle attack, millions of adaptive queries can decrypt any ciphertext.
- **Status:** Must NOT be used for new systems; legacy TLS ≤1.2 exposure via CVE-2012-5081 (ROBOT attack).
:::
::::
::col::
::::card heading="OAEP Padding (Current Standard)"
:::list style=tight
- **Structure:** MGF1-masked random seed XORed with padded message, both fields.
- **Security:** IND-CCA2 secure under the RSA assumption in the random oracle model.
- **Requirement:** NIST SP 800-131A mandates OAEP for all new RSA encryption use.
:::
::::
::::

:::image src="images/26_rsa_padding_comparison.png" alt="Side-by-side diagram: left panel shows PKCS#1 v1.5 byte layout with 0x00, 0x02, padding string PS, 0x00, message M, and a red warning badge showing 'Bleichenbacher Oracle Vulnerability'; right panel shows OAEP layout with seed block masked by MGF1, DB block containing hash, padding, and message M, all masked by MGF1, with a green 'IND-CCA2 Secure' badge; both diagrams show the output block being fed to RSA modular exponentiation" caption="PKCS#1 v1.5 padding is structurally predictable and vulnerable to padding oracle attacks. OAEP uses a random seed and mask-generating functions to achieve provable IND-CCA2 security." width=full
:::

:::notes
One of the most important and frequently misunderstood aspects of RSA is that the core mathematical operation, modular exponentiation, must never be applied directly to plaintext. Unpadded, textbook RSA has several dangerous properties that make it unusable in practice.

First, it is deterministic: $m^e \bmod n$ produces the same ciphertext every time for the same $m$. An attacker who can observe multiple ciphertexts can detect repeated messages, violating semantic security (also called IND-CPA security). Second, raw RSA is malleable: given a ciphertext $c = m^e \bmod n$, an attacker can produce $c' = (2^e \cdot c) \bmod n$, which is the encryption of $2m$, without knowing $m$. This property can be exploited in chosen-ciphertext scenarios.

The original padding standard, PKCS#1 v1.5 (published by RSA Laboratories in 1993 and still documented in RFC 8017 for backward compatibility), addressed determinism by prepending a pseudo-random padding string to the message before encryption. The structure is: 0x00 || 0x02 || PS || 0x00 || M, where PS is a string of at least 8 non-zero random bytes. The 0x02 type byte signals encryption padding (0x01 is used for signature padding). This adds randomness and also pads the message to the full modulus length.

However, in 1998, Daniel Bleichenbacher published a devastating attack: if a server reveals whether an RSA-decrypted value has a valid PKCS#1 v1.5 header (the first two bytes equal 0x00 0x02), an attacker can use this binary oracle to decrypt any captured ciphertext using roughly one million adaptive queries. The server does not need to return plaintext, merely accepting or rejecting the connection based on padding validity is sufficient. This is the Bleichenbacher padding oracle attack.

The ROBOT (Return Of Bleichenbacher's Oracle Threat) vulnerability, catalogued as CVE-2017-13099 and related CVEs, demonstrated in 2017 that major TLS implementations from F5, Citrix, Cisco, and others were still susceptible to Bleichenbacher-style attacks 19 years after the original disclosure, often because implementors added Bleichenbacher countermeasures incorrectly, creating timing side channels.

OAEP (Optimal Asymmetric Encryption Padding), specified in PKCS#1 v2.1 and mandated by NIST SP 800-131A, is the correct padding scheme for RSA encryption. OAEP uses a mask-generating function (MGF1, based on a hash function like SHA-256) and a random seed to create a two-field structure where both the message block and the seed are mutually masked by each other. This produces a ciphertext that is computationally indistinguishable from a random value and is provably IND-CCA2 secure in the random oracle model, meaning it resists adaptive chosen-ciphertext attacks including Bleichenbacher-style queries.

The lesson is broader than RSA: many cryptographic primitives are secure only when composed correctly with other elements, random padding, initialization vectors, authentication tags. Using a strong algorithm incorrectly is as dangerous as using a weak algorithm correctly, a recurring theme in applied cryptography.
:::

%%%
---
unit: Algorithms
code: ECC-CURVES
title: NIST Named Curves, Framework Detail
---
:::callout style=soft
Not all elliptic curves provide equivalent security. **NIST SP 800-186** and **FIPS 186-5** specify approved curves for federal systems; parameter choices directly determine resistance to known attacks.
:::

:::table
| Curve Name | NIST Name | Field Size | Security Strength | Common Applications |
|---|---|---|---|---|
| secp256r1 | P-256 | 256-bit prime | 128-bit | TLS 1.3, ECDSA, ECDH, JWT (ES256) |
| secp384r1 | P-384 | 384-bit prime | 192-bit | NSA Suite B, high-assurance TLS, ECDSA-P384 |
| secp521r1 | P-521 | 521-bit prime | 260-bit | TOP SECRET systems (NSA CNSA 1.0) |
| Curve25519 | — | 255-bit prime | ~128-bit | SSH, WireGuard, Signal Protocol, X25519 |
| Ed25519 | — | Edwards curve | ~128-bit | SSH keys, OpenPGP (RFC 8032), age encryption |
:::

:::image src="images/26_ecc_named_curves_comparison.png" alt="Grid of five elliptic curve diagrams side-by-side, each labeled with curve name and key parameters: P-256 shown as a curve over a 256-bit prime field with NIST badge; P-384 similarly labeled; P-521 with NSA classified systems badge; Curve25519 from Bernstein with 'constant-time, twist-secure' label and WireGuard and Signal logos; Ed25519 as a twisted Edwards curve with OpenPGP and SSH logos; a security-strength bar chart appears below comparing all five" caption="Approved NIST and IETF curves compared by field size, security strength, and typical deployment context. Curve25519 and Ed25519 are widely deployed in open-source and internet protocols due to their performance and resistance to implementation errors." width=full
:::

:::notes
The choice of elliptic curve matters enormously for both security and implementation quality. NIST SP 800-186, published in 2023, is the authoritative document specifying approved curves for federal use. It supersedes the earlier curve specifications in FIPS 186-4 and adds explicit approval of Curve25519 (for key agreement as X25519) and Ed25519 (for signatures).

The three classic NIST prime-field curves, P-256, P-384, and P-521, are defined using the short Weierstrass form $y^2 = x^3 + ax + b \pmod p$, where the specific coefficients and modulus $p$ were chosen through a process that has faced some criticism for lack of transparency in how the seed values were selected. However, no concrete weaknesses have been found in these curves after decades of intensive cryptanalysis. They remain the mandated choice for compliance with FIPS and NSA CNSA guidance.

P-256 (secp256r1) is by far the most widely deployed curve, providing 128-bit security at a 256-bit key size. It is used in TLS 1.3 for key agreement, in ECDSA for certificate signing (as SHA-256withECDSA), in JSON Web Tokens (ES256 algorithm), and in most modern systems. P-384 provides 192-bit security and is required for NSA Suite B systems protecting SECRET-level data. P-521, providing approximately 260-bit security, was required for TOP SECRET protection under CNSA 1.0, though CNSA 2.0 (2022) is transitioning toward post-quantum algorithms.

Curve25519, designed by Daniel J. Bernstein and published in 2006, uses a Montgomery-form curve specifically optimized for constant-time implementation. This is critically important: many ECC implementations have suffered timing side-channel attacks where the execution time of point multiplication leaked information about the private key. Curve25519's Montgomery ladder algorithm naturally takes the same number of steps regardless of the private key value, making constant-time implementation straightforward. It is used in WireGuard, the Signal Protocol (Double Ratchet), age encryption, and modern SSH clients.

Ed25519 is based on Edwards-curve arithmetic over the same field as Curve25519. Edwards-form point addition is both faster than Weierstrass-form and admits an even cleaner constant-time implementation. Ed25519 produces compact 64-byte signatures and 32-byte public keys, making it attractive for bandwidth-constrained contexts. It is specified in RFC 8032, supported in OpenSSH since version 6.5 (2014), adopted in OpenPGP (RFC 4880bis), and used in the age file encryption tool.

Implementation simplicity and resistance to timing attacks can matter more for a curve's real-world security than a slightly higher theoretical margin, because elliptic-curve side-channel failures, such as the nonce reuse behind the PlayStation 3 signing-key compromise, are often more dangerous than theoretical weaknesses in the mathematics.
:::

%%%
---
unit: Infrastructure
code: CERT-REVOKE
title: Certificate Revocation, CRL vs OCSP vs Stapling
---
:::callout style=soft
When a private key is compromised before certificate expiry, revocation must propagate to all relying parties quickly. **RFC 5280** (CRL) and **RFC 6960** (OCSP) define two complementary mechanisms with different trade-offs.
:::

:::table
| Mechanism | Freshness | Size / Latency | Privacy | Server-Side | Specification |
|---|---|---|---|---|---|
| **CRL** | Hours to days | Large binary file, slow download | Browser leaks nothing | No extra config | RFC 5280 |
| **OCSP** | Near-real-time | Single query per cert | CA sees which certs you check | Requires CA OCSP responder | RFC 6960 |
| **OCSP Stapling** | Bounded by response TTL (typically 24–48h) | No extra client request | Full privacy, CA never queried | Server pre-fetches & caches response | RFC 6961 |
| **OCSP Must-Staple** | Bounded by response TTL | Blocks connection if response absent | Full privacy | Server must provide response | RFC 7633 (X.509 extension) |
:::

:::image src="images/26_revocation_comparison.png" alt="Three-panel diagram comparing revocation mechanisms: left panel shows CRL workflow with CA publishing a large CRL file to a distribution point, browser downloading the full list, and checking a serial number; center panel shows OCSP where browser sends a single-certificate status request to OCSP responder and receives a signed 'Good/Revoked/Unknown' response; right panel shows OCSP Stapling where the web server pre-fetches a signed OCSP response and delivers it in the TLS handshake, with no direct CA contact by the browser" caption="Certificate revocation mechanisms compared: CRLs are comprehensive but bulky; OCSP enables per-certificate real-time checks but introduces privacy risks; OCSP Stapling lets servers pre-deliver signed status responses, eliminating the client-CA network round trip." width=full
:::

:::notes
Certificate revocation is one of the most operationally difficult problems in PKI, and it has significant implications for both security and user experience. When a private key is compromised, or when a certificate is discovered to have been fraudulently issued, all clients trusting that certificate must be notified, ideally before any further impersonation or decryption of intercepted traffic occurs.

Certificate Revocation Lists (CRLs), defined in RFC 5280, are the original revocation mechanism. A CRL is a signed list of revoked certificate serial numbers published periodically by the issuing CA. Browsers and operating systems download CRLs and check them against certificates they encounter. The fundamental problem with CRLs is latency and size. A large CA may issue millions of certificates; its CRL can grow to megabytes. Browsers that check CRLs on every TLS connection would add unacceptable latency. Most browsers therefore download CRLs infrequently, meaning a revoked certificate may continue to be accepted for hours or days after revocation.

OCSP (Online Certificate Status Protocol, RFC 6960) was introduced to address freshness. Rather than downloading a list, the browser sends a query for a single certificate to the CA's OCSP responder and receives a signed response: "good," "revoked," or "unknown." This is faster and scales to any certificate volume. However, OCSP has two significant drawbacks. First, it introduces a privacy risk: every time you visit a website, your browser contacts the issuing CA, revealing which sites you visit. Second, it adds latency to TLS handshakes; if the OCSP responder is slow or unreachable, browsers must either block the connection or fail-open (accept without verification).

OCSP Stapling (RFC 6961) elegantly solves both problems. Instead of the browser querying the CA, the web server periodically pre-fetches a signed OCSP response from the CA and includes it in the TLS handshake. The client receives a cryptographically valid status response with no additional network round trip and no privacy leak to the CA. OCSP responses are signed by the CA and include an expiry time (typically 24–48 hours), so a compromised server cannot forge them. The server must refresh them before they expire.

OCSP Must-Staple (RFC 7633) takes this further. It is an X.509 extension that, when present in a certificate, instructs browsers to reject the certificate if a stapled OCSP response is not provided in the TLS handshake. This closes the "fail-open" vulnerability: an attacker who intercepts traffic and blocks OCSP queries cannot prevent revocation from being enforced. However, misconfigured servers that fail to renew their stapled response before expiry will break for all clients, so Must-Staple adoption requires operational maturity.

The broader challenge is that neither CRLs nor OCSP provides truly instantaneous revocation at the scale of the internet. The move toward 90-day certificate lifetimes is partly motivated by the observation that short validity periods reduce the window during which a revoked certificate could be abused, complementing (rather than replacing) active revocation mechanisms.
:::

%%%
---
unit: Infrastructure
code: CT-LOGS
title: Certificate Transparency & Audit Logs
---
:::callout style=soft
**Certificate Transparency (CT)**, defined in **RFC 9162**, requires Certificate Authorities to log every issued certificate in publicly auditable, append-only logs, making unauthorized or mis-issued certificates detectable by domain owners and security researchers.
:::

:::flow
CA prepares a signed certificate for submission to one or more CT logs
CT log servers append the certificate and return a **Signed Certificate Timestamp (SCT)**, a cryptographic proof of inclusion
CA embeds the SCTs in the final certificate (or delivers them via TLS extension or OCSP response)
Browser checks that the certificate carries valid SCTs before trusting it
Domain owners and security researchers monitor CT logs for certificates issued for their domains
Mis-issued certificates are flagged; CAs are obligated to revoke them
:::

:::image src="images/26_certificate_transparency_flow.png" alt="Swimlane diagram with four rows, CA, CT Log, Browser, Domain Owner: CA row shows certificate preparation, submission to two CT logs, receipt of SCTs, and embedding SCTs in cert; CT Log row shows append-only log entries and Merkle tree root hash; Browser row shows receiving cert with SCTs, verifying SCTs against known log public keys, and accepting connection; Domain Owner row shows monitoring tool querying CT logs for their domain and receiving alert when unexpected cert appears" caption="Certificate Transparency in practice: every certificate must be logged before issuance; SCTs prove logging occurred; browsers reject certificates without valid SCTs; domain owners can monitor logs to detect unauthorized certificate issuance." width=full
:::

:::notes
Certificate Transparency was conceived in response to a series of PKI failures in the early 2010s. In 2011, the Dutch CA DigiNotar was breached and attackers used its infrastructure to issue fraudulent certificates for google.com, mozilla.com, and hundreds of other high-value domains. These rogue certificates could have enabled large-scale man-in-the-middle attacks against Iranian dissidents and journalists. The attack went undetected for weeks because there was no systematic way to discover unauthorized certificate issuance. DigiNotar was subsequently forced out of business, and its root was removed from all major browser root stores.

Google engineers Ben Laurie and Adam Langley proposed Certificate Transparency as a systemic remedy. The core idea is an append-only public log. Any certificate issued by a CA must be submitted to at least two independent CT logs before the certificate can be used. Logs are organized as Merkle hash trees: the root hash of the log is periodically signed and published, and any certificate's membership in the log can be efficiently proven with a logarithmic-length Merkle audit proof. Because logs are append-only and their state is publicly verifiable, tampering is detectable.

When a CA submits a certificate to a log, the log issues a Signed Certificate Timestamp (SCT), a cryptographically signed commitment that the certificate will be incorporated into the log within a specified merge delay (typically 24 hours). The CA embeds one or more SCTs in the final certificate. Browsers that implement CT enforcement, which Google Chrome requires for all certificates issued since April 2018, will reject certificates lacking valid SCTs from recognized log operators. Apple Safari enforces similar requirements.

The monitoring aspect is equally important. Domain owners can subscribe to CT monitoring services (or run their own log watchers using the CT APIs) and receive alerts when any certificate is issued for their domain. This allows organizations to detect mis-issuance within hours rather than weeks. Services like crt.sh provide a public search interface over aggregated CT log data.

Several important security incidents have been detected and remediated via CT monitoring. In 2017, Symantec was found to have issued thousands of test certificates without proper validation, which were detected via CT logs. This contributed to Google's decision to distrust Symantec's CA root entirely, forcing Symantec to sell its CA business to DigiCert. CT logs have also been used to detect Domain Validation bypass vulnerabilities, where CAs issued certificates for domains they had not properly validated ownership of (relevant CVEs include CVE-2022-0778 in OpenSSL, though that is a parsing vulnerability rather than a CT issue).

Certificate Transparency logs are a queryable audit trail of the certificate ecosystem: looking up an organization's domain typically returns dozens of certificates, including expired ones, wildcards and certificates from multiple CAs, which demonstrates the real visibility CT provides.
:::

%%%
---
unit: Trust
code: CODESIGN
title: Code Signing & Software Supply Chain Security
---
:::callout style=soft
**Code signing** applies digital signatures to software artifacts so that users and operating systems can verify that executables have not been modified since the developer signed them. This is the primary cryptographic defense against supply chain tampering.
:::

::::columns ratio=1:1
::col::
::::card heading="What Is Signed?"
:::list style=tight
- Windows Authenticode: PE/EXE/DLL, MSI installers, PowerShell scripts
- macOS: Mach-O binaries, app bundles, Xcode archives (notarization via Apple)
- Linux packages: RPM GPG signatures, Debian dpkg-sig, APT Release file
- Container images: Docker Content Trust (Notary v2), cosign (Sigstore)
- Software updates: Microsoft Windows Update, Apple Software Update, npm package provenance
:::
::::
::col::
::::card heading="Trust Chain for Code Signing"
:::list style=tight
- Developer generates a key pair; obtains a code-signing certificate from a trusted CA
- Signing tool (signtool.exe, codesign, gpg) hashes the artifact and signs the hash with the private key
- Signature and certificate are embedded in or distributed alongside the artifact
- OS/runtime verifies the signature, checks the certificate chain to a trusted root, and enforces policy
:::
::::
::::

:::image src="images/26_code_signing_supply_chain.png" alt="End-to-end supply chain diagram: Developer workstation box shows source code going through build pipeline; a code-signing CA box issues a time-stamped code-signing certificate; the signed binary flows through a distribution CDN; at the user end, Windows SmartScreen and macOS Gatekeeper icons show OS-level signature verification; a second branch shows a compromised CDN injecting a modified binary that fails signature verification, blocked by the OS with a red X warning dialog" caption="Code signing creates a cryptographic link from the developer's private key to the distributed artifact. Even if the distribution server is compromised, modified binaries fail signature verification at the endpoint." width=full
:::

:::notes
Code signing is the application of digital signature technology to software artifacts to guarantee authenticity and integrity throughout the software supply chain. This is critically important because the path from a developer's keyboard to an end user's system often passes through multiple intermediary systems, build servers, CI/CD pipelines, package registries, content delivery networks, any of which could be compromised by an attacker seeking to inject malicious code.

The SolarWinds attack of 2020 (CVE-2020-10148) illustrates the stakes vividly. Attackers who had compromised SolarWinds' build pipeline were able to inject malicious code (the SUNBURST backdoor) into the legitimate SolarWinds Orion software builds. Crucially, the malicious code was signed with SolarWinds' authentic code-signing certificate, because the attackers had compromised the build system that generated the signature, not stolen the private key directly. This attack affected approximately 18,000 organizations, including multiple US federal agencies, and remained undetected for approximately nine months.

On Windows, Authenticode is the code-signing framework. Developers obtain a code-signing certificate from a CA (Sectigo, DigiCert, and others sell them), sign their binaries using signtool.exe, and embed the signature in the Portable Executable (PE) header. Windows Defender SmartScreen and the User Account Control (UAC) system both consult Authenticode signatures. Unsigned code triggers warnings or blocks depending on policy. Extended Validation (EV) code-signing certificates require stricter identity vetting and provide additional trust signals, including immediate SmartScreen reputation establishment.

On macOS, Apple requires Gatekeeper approval for distributed software. Developers must both sign binaries with their Developer ID certificate and submit them to Apple's notarization service. Apple's notarization server scans the submission for known malware signatures and returns a notarization ticket. Gatekeeper checks for this ticket at launch. This creates an additional choke point, Apple can revoke notarization tickets for malicious software after the fact.

For Linux packages, the GPG (GNU Privacy Guard) ecosystem provides an open alternative to commercial CAs. Debian and RPM-based distributions sign repository metadata with GPG keys, and package managers verify these signatures before installation. The Sigstore project, backed by the Linux Foundation, Google, Red Hat, and Purdue University, is building a certificate-transparency-like append-only log (Rekor) specifically for software artifact signatures, enabling tamper-evident provenance tracking for open-source packages.

NIST SP 800-218 (Secure Software Development Framework) and EO 14028 (Executive Order on Improving the Nation's Cybersecurity, 2021) both mandate code signing and Software Bill of Materials (SBOM) requirements for US federal software procurement, reflecting the national security implications of supply chain integrity.
:::

%%%
---
unit: Algorithms
code: RSAECC-COMP
title: RSA vs ECC, Algorithm Comparison
---
:::callout style=soft
RSA and ECC are both widely deployed asymmetric algorithms but differ significantly in mathematical foundation, performance characteristics, key size requirements, and ecosystem deployment. Choosing between them requires evaluating your operational constraints against NIST SP 800-57 guidance.
:::

:::table
| Property | RSA | ECC (P-256 / Curve25519) |
|---|---|---|
| **Mathematical basis** | Integer factorization ($n = pq$) | Elliptic curve discrete logarithm |
| **NIST minimum key size (2030+)** | 3072 bits | 256 bits |
| **128-bit security key size** | 3072-bit modulus | 256-bit scalar |
| **Signature size** | 384 bytes (3072-bit) | 64 bytes (P-256/Ed25519) |
| **Key generation speed** | Slow (primality testing) | Fast (scalar selection) |
| **Signing speed** | Fast (small exponent $e=65537$) | Fast (double-and-add) |
| **Verification speed** | Very fast (small public exponent) | Moderate |
| **Standardization maturity** | Very high, RFC 8017, 45+ years | High, FIPS 186-5, SP 800-186 |
| **Quantum resistance** | Broken by Shor's algorithm | Broken by Shor's algorithm |
| **Typical deployment** | TLS certificates, legacy systems | TLS 1.3 key exchange, mobile, IoT |
:::

:::image src="images/26_rsa_vs_ecc_comparison.png" alt="Split infographic: left RSA panel shows a large lock icon with '3072 bits' label, a bar chart showing key generation time in milliseconds, certificate size comparison, and hardware power consumption in milliwatts; right ECC panel shows a smaller lock icon with '256 bits' label, the same charts showing dramatically smaller values, and logos of TLS 1.3, WireGuard, and smart card applications; a note at the bottom labels both as 'quantum-vulnerable'" caption="RSA vs ECC compared across practical operational dimensions. ECC dominates in key size, signature size, and computational efficiency; RSA retains advantages in standardization maturity and simplicity of certain verification operations." width=full
:::

:::notes
When designing a system that requires asymmetric cryptography, the choice between RSA and ECC is not merely academic, it has concrete implications for performance, bandwidth, power consumption, and implementation complexity. NIST SP 800-57 Part 1 provides the authoritative framework for comparing security strengths across algorithm families.

From a security equivalence standpoint, NIST SP 800-57 Table 2 establishes that a 3072-bit RSA key, a 256-bit ECC key (P-256 or Curve25519), and a 128-bit AES symmetric key all provide approximately 128 bits of security strength. This 12:1 key size ratio between RSA and ECC for equivalent security reflects the difference in the hardness of the underlying mathematical problems and has significant practical consequences.

Bandwidth and storage are affected substantially. A 3072-bit RSA public key requires 384 bytes. A P-256 public key requires 65 bytes in uncompressed format or 33 bytes compressed. An Ed25519 public key is exactly 32 bytes. RSA signatures are as large as the key modulus (384 bytes for 3072-bit RSA). ECDSA P-256 signatures are 64 bytes. This difference matters in constrained environments: smartcards have limited flash storage; IoT sensors operate over low-bandwidth radio protocols (LoRa, Zigbee) where sending 384 bytes in a single packet may not be possible.

Computational performance on server hardware strongly favors ECC for key agreement. Intel and ARM benchmarks consistently show that ECDHE key generation and agreement with P-256 runs 15–20 times faster than equivalent 3072-bit RSA operations. On embedded microcontrollers, this gap is even more pronounced because RSA's large integer arithmetic requires hardware multiplication support that many microcontrollers lack. ECC point multiplication can be implemented efficiently in pure software on resource-constrained devices.

RSA retains advantages in specific contexts. Verification with RSA's small public exponent ($e = 65537$) is extremely fast, just one modular exponentiation with a very small exponent. ECDSA verification requires two full scalar multiplications and is thus slower than RSA verification. For applications that verify signatures millions of times per second (such as a high-throughput API gateway checking JWT signatures), RSA may offer better throughput on the verification side. RSA is also simpler to implement correctly in a minimal context (though OAEP padding requirements complicate this).

Both algorithms share the same fundamental limitation: neither is resistant to quantum computing. Shor's algorithm breaks both integer factorization and the discrete logarithm problem (including ECDLP). Therefore, selecting between RSA and ECC for a new long-lived system requires also considering the post-quantum migration path, and whether the design supports cryptographic agility, the ability to swap algorithms without rebuilding the entire system.
:::

%%%
---
unit: Trust
code: CASESTUDY
title: Case Study, The DigiNotar Breach (2011)
---
:::callout style=soft
The 2011 compromise of Dutch CA **DigiNotar** is the canonical example of PKI failure. Attackers gained access to DigiNotar's HSMs and issued fraudulent certificates for over 500 domains, enabling mass surveillance of Iranian internet users before the breach was discovered weeks later.
:::

:::steps
**Breach:** Attackers infiltrated DigiNotar's network (likely via SQL injection and credential theft) and gained access to CA signing infrastructure, bypassing HSM controls.
**Fraudulent issuance:** Approximately 531 fraudulent certificates were issued for high-value domains including google.com, yahoo.com, microsoft.com, and sites operated by the Mossad and CIA.
**Exploitation:** Google users in Iran began receiving fraudulent google.com certificates, triggering HTTPS errors and alerting a software engineer. A Google engineer noticed anomalous certificates via Chrome's certificate pinning mechanism.
**Discovery:** On August 28, 2011, a user reported the suspicious google.com certificate on a security forum. Within 48 hours, browser vendors began revoking DigiNotar's root certificates.
**Revocation cascade:** Mozilla, Microsoft, and Google pulled DigiNotar from their root stores within days, instantly making every legitimate DigiNotar certificate untrusted. The Dutch government had used DigiNotar for government PKI, causing disruption to critical services.
**Aftermath:** DigiNotar filed for bankruptcy on September 20, 2011, six weeks after the breach became public.
:::

:::image src="images/26_diginotar_breach_timeline.png" alt="Timeline diagram with key events: May 2011 labeled 'Breach likely occurred'; July-August 2011 labeled 'Fraudulent certificates issued and used'; August 27 labeled 'User reports suspicious google.com cert'; August 29 labeled 'Mozilla, Microsoft, Google begin root removal'; September 3 labeled 'Dutch government advises citizens DigiNotar untrusted'; September 20 labeled 'DigiNotar bankruptcy'; an inset box shows a browser security error dialog with the DigiNotar certificate displayed" caption="The DigiNotar breach timeline: weeks passed between initial compromise and discovery because no systemic mechanism existed to detect unauthorized certificate issuance, a gap that Certificate Transparency was specifically designed to close." width=full
:::

:::notes
The DigiNotar case study deserves detailed attention because it illustrates almost every failure mode in PKI simultaneously: an inadequately secured CA infrastructure, insufficient monitoring, delayed response, and cascading impact when a CA root is revoked. It also directly motivated the development of Certificate Transparency and browser certificate pinning.

DigiNotar was a respected Dutch Certificate Authority founded in 1998. It held roots in all major browser and operating system trust stores. The Dutch government's PKI for Government (PKIoverheid) program, which issues certificates for government employees and services, was built on DigiNotar infrastructure. In 2011, DigiNotar was owned by VASCO Data Security.

The compromise is believed to have begun in May or June 2011. Post-incident forensics indicated that attackers (widely attributed to Iranian state actors based on circumstantial evidence and targets) gained access to DigiNotar's systems, possibly exploiting unpatched web application vulnerabilities. The investigators from Fox-IT (contracted to perform forensics) found that DigiNotar's systems had significant security deficiencies: insufficient network segmentation, inadequate logging, and poor access controls around the HSMs that stored CA private keys.

The fraudulent certificate for google.com, just one of 531 unauthorized certificates, was the thread that unraveled everything. Google's Chrome browser had implemented certificate pinning for google.com: a hardcoded list of expected public key hashes that Chrome would check against the certificate it received, regardless of whether the certificate otherwise validated correctly against the PKI chain. When a Chrome user in Iran connected to google.com using a fraudulent DigiNotar certificate, Chrome detected that the certificate's public key hash did not match the expected pin and flagged the error. The user reported the anomaly on a Chromium bug tracker thread on August 28, 2011.

The revocation cascade illustrates the double-edged nature of PKI's centralized trust model. On one hand, revoking a root CA is a powerful and decisive response, once DigiNotar's root was removed from trust stores, every DigiNotar-signed certificate became instantly untrusted. On the other hand, this caused significant collateral damage. The Dutch government had issued approximately 300,000 legitimate certificates under PKIoverheid through DigiNotar. Citizens trying to access government services received terrifying security errors. Emergency re-issuance of certificates through alternative CAs took weeks.

This case directly catalyzed several lasting changes in PKI policy. First, Google accelerated the development and deployment of Certificate Transparency, making it mandatory for Chrome in 2018. Second, browser vendors developed RFC 7469 (HTTP Public Key Pinning, now deprecated but conceptually important) and later trust-on-first-use (TOFU) mechanisms. Third, the CA/Browser Forum strengthened its Baseline Requirements for certificate issuance, including mandatory annual audits. The DigiNotar compromise, in which a breached certificate authority issued fraudulent certificates (including for Google domains) and was removed from browser trust stores, is a required case study in CA security standards.
:::

%%%
---
unit: Key Exchange
code: CHECKPOINT
title: Mid-Lecture Checkpoint, Concept Review
---
:::callout style=soft
Pause and consolidate. Before continuing to PKI failure cases and advanced topics, verify that the core concepts from the first half of this lecture are clear.
:::

:::list style=tight
- **Q1:** What is the difference between a one-way function and a trapdoor one-way function? Give one example from an asymmetric algorithm.
- **Q2:** Alice receives a message signed by Bob. She verifies it using Bob's public key and the signature matches. What three properties does this confirm?
- **Q3:** An RSA-2048 key provides roughly 112 bits of security. What ECC key size provides approximately equivalent security, and what is the ratio?
- **Q4:** In TLS 1.3, why does the server send its digital certificate AND a separate digital signature over the handshake transcript? Why not rely on the certificate alone?
- **Q5:** What is the difference between revocation via CRL and OCSP Stapling? Which provides better privacy, and why?
- **Q6:** Why does Perfect Forward Secrecy require ephemeral key pairs? Would using the same static ECDH key pair for multiple sessions undermine PFS?
:::

:::image src="images/26_checkpoint_concept_map.png" alt="Mind map connecting core concepts reviewed: center node 'Asymmetric Cryptography'; branches to 'Trapdoor Functions' with sub-nodes RSA, ECC, DH; branch to 'Digital Signatures' with sub-nodes Signing, Verification, FIPS 186-5; branch to 'PKI' with sub-nodes X.509, CRL, OCSP, CT; branch to 'Hybrid Crypto' with sub-node TLS 1.3; each branch has a colored question mark badge indicating the checkpoint question number" caption="Checkpoint concept map: use these questions to self-assess understanding before the advanced slides. Each question corresponds to a core concept from the first nine slides." width=full
:::

:::notes
This is a deliberate pause in the lecture. The first half covered the foundational theoretical and algorithmic content: trapdoor functions, RSA mechanics, ECC, digital signatures, X.509 certificates, PKI trust chains, and TLS 1.3. Before continuing to more applied and advanced material, it is worth consolidating these concepts.

Working through the six checkpoint questions:

Question 1: A one-way function is easy to compute forward but infeasible to invert. A trapdoor one-way function adds the property that inversion becomes easy given a specific secret (the trapdoor). In RSA, multiplying primes $p \times q$ is the one-way direction; factoring the product is the hard direction. The trapdoor is the knowledge of $p$ and $q$, which enables computing $\phi(n) = (p-1)(q-1)$ and then the private exponent $d$.

Question 2: A verified digital signature confirms: (a) integrity, the message has not been altered since signing, because the hash over the message matches the decrypted signature; (b) authenticity, the message was signed by someone possessing Bob's private key; and (c) non-repudiation, Bob cannot credibly deny signing the message, assuming private key integrity.

Question 3: RSA-2048 provides 112 bits of security. ECC-224 (P-224) provides approximately the same. The ratio is 2048/224 ≈ 9:1. For 128-bit security, the comparison is RSA-3072 vs ECC-256, a 12:1 ratio. As security requirements grow, the RSA key must grow much faster than the ECC key.

Question 4: The digital certificate proves the server's long-term identity (its public key belongs to the named domain, as verified by the CA). The separate signature over the handshake transcript proves that the server actively participated in this specific session using the corresponding private key. Without the per-session signature, an attacker could relay a legitimate certificate while using their own key for the actual key exchange, a form of certificate relay attack. Together, the certificate plus handshake signature provide both identity binding and proof of live participation.

Question 5: CRL requires the client to download a periodically-published list, which can be megabytes in size and has latency that means revoked certificates remain trusted for hours or days. OCSP Stapling has the server pre-fetch a signed OCSP response and include it in the TLS handshake; the client receives a fresh status proof with no additional network query, and, critically, the CA never learns which website the client visited. OCSP Stapling provides better privacy because there is no client-to-CA contact.

Question 6: PFS requires that session keys be derived from ephemeral material that is discarded after the session. If a static ECDH key pair is reused across sessions, then an attacker who later compromises that private key can derive the shared secret for every past session recorded while that key was in use. Ephemeral keys mean each session has a unique secret; even a total key compromise only threatens currently active sessions.

:::

%%%
---
unit: Infrastructure
code: HSM
title: Hardware Security Modules (HSMs) in PKI
---
:::callout style=soft
A **Hardware Security Module (HSM)** is a tamper-resistant physical device that generates, stores, and manages cryptographic keys entirely within its secure boundary. Private keys in an HSM can be used for operations but can never be exported in plaintext, providing protection even against privileged OS-level attackers.
:::

::::columns ratio=1:1
::col::
::::card heading="HSM Security Properties"
:::list style=tight
- **Key confinement:** Private key never leaves the HSM boundary in clear form
- **Tamper evidence/response:** Physical intrusion triggers key zeroization
- **FIPS 140-3 Level 3:** Required for federal key material (NIST SP 800-131A)
- **Performance:** Hardware-accelerated RSA, ECC, and AES operations
- **Audit logging:** Signed logs of all key usage events
:::
::::
::col::
::::card heading="Where HSMs Are Required"
:::list style=tight
- Root CA and Intermediate CA private key storage (CA/Browser Forum Baseline Requirements)
- TLS private key protection on high-security servers
- Code-signing key protection
- Payment HSMs (PCI DSS Requirement 3.7): PIN processing and card data encryption
- Government and military PKI (FIPS 140-3 Level 3 minimum)
:::
::::
::::

:::image src="images/26_hsm_architecture.png" alt="Diagram of an HSM appliance showing outer tamper-evident shell with sensors; inside a secure processor labeled 'cryptographic engine'; RAM labeled 'key storage (never leaves boundary)'; a battery-backed zeroization circuit labeled 'active tamper response'; external connections show USB and PCIe host interface with API calls going in and encrypted results coming out; a side panel shows the FIPS 140-3 validation certificate levels 1 through 4 with Level 3 highlighted for CA keys" caption="HSM architecture: the secure processor and key storage are physically isolated from the host system. Cryptographic operations are performed inside the HSM boundary; only results are exported. Tamper-detection circuits destroy keys if the enclosure is breached." width=full
:::

:::notes
Hardware Security Modules are the physical enforcement layer of PKI's trust model. We establish through mathematics and policy that CA private keys must remain secret. HSMs enforce this guarantee through hardware. They are not merely encrypted storage, they are active security processors that perform cryptographic operations internally and refuse to export private key material under any circumstances.

The FIPS 140-3 standard (the successor to FIPS 140-2) defines four security levels for cryptographic modules. Level 1 requires only correct implementation of approved algorithms, essentially any software running on standard hardware. Level 2 adds tamper-evidence: a module must show evidence (such as broken seal tape) if physically opened. Level 3 requires tamper-resistance and response: the module must actively resist unauthorized physical access and must zeroize (destroy) key material if intrusion is detected. Level 4 provides complete physical security envelope protection against environmental attacks. For Root CA keys, the CA/Browser Forum Baseline Requirements mandate HSMs validated at FIPS 140-2 Level 3 or Common Criteria EAL 4+ at minimum.

The security value of an HSM is best understood by contrasting it with software key storage. If an organization's CA private key is stored in an encrypted file on a server, an attacker who gains root (Administrator) access to that server can obtain the decrypted key by reading process memory, injecting code into the signing process, or abusing the OS's memory management. The attacker need never touch the encrypted file. An HSM eliminates this attack surface: even an OS-level compromise gives the attacker only the ability to request signing operations from the HSM, not to extract the underlying key material. The HSM is also isolated from the host bus, so hardware-level memory attacks are ineffective against the HSM's internal storage.

HSMs also provide rate limiting and access control on cryptographic operations. A CA HSM can be configured to require multi-person authentication (multiple operator cards simultaneously inserted) before performing a root signing operation, matching the offline ceremony requirements for Root CAs. It can log every signing operation with a tamper-evident audit trail.

Major HSM vendors include Thales (Luna HSM), Entrust nShield, AWS CloudHSM (a cloud-based HSM service), and Azure Dedicated HSM. Payment HSMs (such as the Thales payShield) are specialized for PIN processing and EMV card personalization in compliance with PCI DSS. Most modern cloud providers offer FIPS 140-2 Level 3 validated HSM services, making HSM-grade key protection accessible for smaller organizations that previously could not afford dedicated hardware.

SolarWinds is relevant to key protection too: attackers who compromised the build pipeline could sign software with the code-signing certificate even though the private key was nominally protected. HSMs prevent key extraction but cannot prevent abuse of signing if the process that triggers signing is itself compromised, so defense in depth requires both HSM key protection and strong controls on who and what can request a signing operation.
:::

%%%
---
unit: Trust
code: EMAIL-CRYPTO
title: Email Encryption, S/MIME and OpenPGP
---
:::callout style=soft
Two standards apply asymmetric cryptography to secure email: **S/MIME** (RFC 5751) uses the X.509 PKI trust model; **OpenPGP** (RFC 4880) uses a decentralized web-of-trust model. Both provide confidentiality and digital signatures.
:::

:::table
| Property | S/MIME (RFC 5751) | OpenPGP / GPG (RFC 4880) |
|---|---|---|
| **Trust model** | Hierarchical PKI, certificate from a CA | Web of trust, users sign each other's keys |
| **Key format** | X.509 certificate | OpenPGP keyblock (.asc / .gpg) |
| **Key discovery** | LDAP directories, corporate exchange | Key servers (keys.openpgp.org), manual |
| **Corporate support** | Excellent, integrated into Exchange, Outlook | Limited, plugin-based (Enigmail, Gpg4win) |
| **End-to-end encryption** | Yes | Yes |
| **NIST alignment** | SP 800-177 (Trustworthy Email) | Not explicitly mandated; common in open-source |
| **Deployment complexity** | Moderate, requires CA-issued cert per user | High, key exchange and trust management manual |
:::

:::image src="images/26_smime_pgp_comparison.png" alt="Split diagram: left panel shows S/MIME flow with Alice's email client, her S/MIME certificate from a trusted CA, encryption with Bob's CA-issued certificate public key, and decryption by Bob's client verifying the chain to a root CA; right panel shows OpenPGP flow with Alice and Bob's GPG keyring, a key-signing ceremony creating the web of trust, Alice encrypting to Bob's manually verified public key, and decryption and signature verification by Bob's GPG installation" caption="S/MIME and OpenPGP both deliver asymmetric encryption and digital signatures for email, but differ fundamentally in trust model: S/MIME inherits the hierarchical CA trust of the Web PKI; OpenPGP distributes trust through direct human verification and key-signing." width=full
:::

:::notes
Email is one of the oldest use cases for applied asymmetric cryptography, predating the World Wide Web. Despite decades of standardization effort, end-to-end email encryption remains underdeployed in practice, a fact that reflects both genuine usability challenges and the network effects required for any communication security system.

S/MIME (Secure/Multipurpose Internet Mail Extensions), specified in RFC 5751, brings the X.509 PKI model to email. Each participant obtains an email certificate from a trusted CA, some CAs offer free Class 1 S/MIME certificates for personal use; enterprise deployments typically integrate with Active Directory Certificate Services or a commercial CA. The certificate binds the user's email address to their public key, and the CA's signature vouches for this binding. To send an encrypted email to Bob, Alice retrieves Bob's S/MIME certificate, encrypts the message using a randomly generated symmetric session key, and wraps that key with RSA or ECDH using Bob's public key. Alice signs the message with her private key. Bob receives the message, verifies Alice's signature using her certificate (validating the CA chain), and decrypts the session key with his private key.

S/MIME integrates natively into Microsoft Outlook, Apple Mail, and most enterprise email clients without plugins, making it the standard for corporate and government secure email. NIST SP 800-177 provides guidance on trustworthy email implementation and recommends S/MIME for organizations requiring authenticated and encrypted communications.

OpenPGP, specified in RFC 4880 and implemented in GnuPG (GPG), takes a radically different approach: the web of trust. Instead of relying on CAs to vouch for key-identity bindings, PGP users sign each other's public keys after verifying identity in person or through other reliable means. If Alice has signed Bob's key, and Bob has signed Carol's key, a user who trusts Alice can transitively trust Carol's identity. The web of trust model is decentralized and censorship-resistant, which is why it is popular among journalists, security researchers, activists, and open-source developers.

In practice, the web of trust has significant usability challenges. Key exchange requires out-of-band identity verification. Key servers are unreliable and historically suffered from certificate flooding attacks (CVE-2019-13050) where attackers flooded a target's key with thousands of fake signatures, causing GPG to hang for hours when fetching the key. The newer keys.openpgp.org server addresses this by only accepting signatures that have been confirmed by the keyholder, moving partially toward a more curated model.

Neither S/MIME nor OpenPGP encrypts metadata: the sender, recipient, subject line, and delivery timestamps remain visible to email servers and any party with access to mail logs. For metadata-sensitive communications, Signal, ProtonMail, or similar services that minimize metadata exposure are more appropriate. NIST SP 800-177 discusses this limitation explicitly and notes that email encryption protects message confidentiality and integrity but not traffic analysis.
:::

%%%
---
unit: Infrastructure
code: SSH-KEYS
title: SSH Public Key Authentication
---
:::callout style=soft
**SSH (Secure Shell)**, specified in RFC 4253 and RFC 4252, uses asymmetric cryptography for host authentication and optionally for user authentication. Public key authentication eliminates password transmission and provides stronger security than password-based login.
:::

:::steps
**Key pair generation:** User generates a key pair on their local machine: `ssh-keygen -t ed25519 -C "user@host"` creates ~/.ssh/id_ed25519 (private) and ~/.ssh/id_ed25519.pub (public).
**Key deployment:** User copies public key to the server: `ssh-copy-id user@server` appends the public key to ~/.ssh/authorized_keys on the server.
**Connection initiation:** Client opens TCP connection and performs SSH key exchange (ECDH), establishing an encrypted channel.
**Server host key verification:** Client verifies the server's host key against its known_hosts file. If new, prompts for TOFU (trust on first use).
**User authentication:** Server sends a challenge. Client signs the challenge with the user's private key. Server verifies the signature against the public key in authorized_keys.
**Session established:** If verification succeeds, the user is authenticated without transmitting any secret.
:::

:::image src="images/26_ssh_public_key_auth.png" alt="Diagram of SSH public key authentication flow: left side shows client computer with private key locked in ~/.ssh/id_ed25519; right side shows server with authorized_keys file; numbered arrows show: 1 TCP connection; 2 ECDH key exchange establishing encrypted channel; 3 server presents host key, client checks known_hosts; 4 server issues challenge string; 5 client signs challenge with private key; 6 client sends signature; 7 server verifies signature against authorized_keys entry; 8 green 'Access Granted' label" caption="SSH public key authentication: the user's private key never leaves the client machine. Only a signature over a server-issued challenge is transmitted. The server verifies using the pre-installed public key." width=full
:::

:::notes
SSH public key authentication is one of the most elegant applied examples of asymmetric cryptography in daily use by security practitioners. It demonstrates how the mathematical properties we have studied, key pairs, digital signatures, challenge-response, combine into a practical, phishing-resistant authentication mechanism that millions of developers and administrators rely on every day.

The protocol, defined in RFC 4252 (SSH Authentication Protocol), supports multiple authentication methods including password (which transmits the password to the server, protected by the encrypted channel), keyboard-interactive, and publickey. The publickey method is strongly preferred because it eliminates the risk of password interception, server-side password database breaches, and password guessing attacks.

Key generation creates a key pair on the client. The private key is stored locally (and optionally protected with a passphrase, which encrypts the key file itself). The public key is a compact, shareable representation. For Ed25519 keys, the public key is only 68 bytes in OpenSSH format, making it trivial to distribute. Modern best practice recommends Ed25519 over RSA for SSH keys because of its smaller size, faster performance, and inherent protection against certain side-channel attacks through the Edwards-curve constant-time arithmetic.

Deployment copies the public key to the server's authorized_keys file. This file lists all public keys permitted to authenticate as a given user. Because only the public key is transmitted, disclosure of the authorized_keys file does not compromise security, an attacker would still need the corresponding private key to authenticate.

The authentication exchange is a challenge-response protocol. The server generates a fresh random challenge (a nonce). The client signs the concatenation of the session identifier and the challenge using the private key. The server verifies the signature using the registered public key. This proves key possession without transmitting any secret material. It also binds the authentication to the specific session, preventing replay attacks.

Host key verification via known_hosts addresses the server authentication side. When you first connect to a server, SSH records its host key fingerprint in ~/.ssh/known_hosts. On subsequent connections, if the fingerprint changes, indicating a potentially different server, possible replacement, or man-in-the-middle attack, SSH issues a stark warning. FIDO2/WebAuthn hardware security keys (YubiKey, SoloKey) can serve as SSH keys, storing the private key in tamper-resistant hardware so that even a compromised laptop cannot extract the key. OpenSSH 8.2 (2020) added native FIDO2 SSH key support.

The difference in key formats is striking: an Ed25519 public key is about 68 bytes on one line, while an RSA-4096 public key is several hundred bytes over multiple lines. An authorized_keys file stores only public keys, because the private key must never leave the client; storing private keys on the server would let anyone who compromised it impersonate every user.
:::

%%%
---
unit: Algorithms
code: MISCONCEPTIONS
title: Common Misconceptions in Asymmetric Cryptography
---
:::callout style=soft
Asymmetric cryptography is frequently misunderstood, even by practitioners. Correcting these misconceptions prevents dangerous design errors and implementation vulnerabilities.
:::

:::list style=tight
- **Misconception 1:** "Encrypting with a public key keeps data secret from the key's owner.", FALSE. The OWNER holds the private key and can always decrypt. Public key encryption keeps data secret from EVERYONE EXCEPT the key owner.
- **Misconception 2:** "A larger RSA key is always better.", MISLEADING. Beyond 4096 bits, RSA key generation and operations are very slow with minimal real security gain. NIST SP 800-57 recommends 3072 bits for post-2030 systems. Crypto agility (algorithm replacement) is more valuable than excessively large classical keys.
- **Misconception 3:** "My public key is private because I haven't shared it.", FALSE. A public key you haven't published is effectively a symmetric key. The entire benefit of asymmetric cryptography requires your public key to be discoverable; certificate transparency enforces this.
- **Misconception 4:** "Digital signatures encrypt the message.", FALSE. Standard digital signatures (ECDSA, RSA-PSS) do NOT encrypt the message. The message remains readable. Signing provides authenticity and integrity, not confidentiality.
- **Misconception 5:** "HTTPS means the website is safe and trustworthy.", FALSE. HTTPS means the connection is encrypted and the server's certificate was issued by a trusted CA for that domain. It says nothing about whether the site's content or operators are legitimate. Phishing sites routinely use HTTPS.
- **Misconception 6:** "Asymmetric encryption is used to encrypt bulk data in TLS.", FALSE. In TLS, asymmetric operations (ECDHE, certificate signatures) are used only during the handshake to authenticate and agree on a shared secret. Bulk data is encrypted with symmetric AES-GCM.
:::

:::image src="images/26_misconceptions_correction.png" alt="Six panels arranged in a grid, each with a red 'Myth' speech bubble and a green 'Reality' speech bubble: panel 1 shows the public key encryption recipient confusion; panel 2 shows a key size dial with a 'sweet spot' marker at 3072 bits; panel 3 shows a public key being published on a certificate pinboard; panel 4 shows a signed but plaintext-visible email message; panel 5 shows a phishing site with a padlock icon; panel 6 shows the TLS handshake with asymmetric phase versus the subsequent AES encrypted data phase" caption="Six common misconceptions about asymmetric cryptography and their corrections. Internalizing these distinctions prevents design errors and security vulnerabilities in systems that rely on cryptographic guarantees." width=full
:::

:::notes
Misconceptions about cryptography are dangerous precisely because they feel plausible. A developer who believes that signing a message also encrypts it will ship software that exposes sensitive data, expecting it to be confidential. A network engineer who believes HTTPS guarantees content trustworthiness will fail to educate users about phishing. Correcting these misconceptions at the conceptual level is as important as teaching the mechanics.

Misconception 1, the direction of public key encryption, is extremely common in students encountering asymmetric cryptography for the first time. The naming is counterintuitive: "public key encryption" sounds like it protects the key itself, when in fact it uses the key to protect the message. The correct mental model: if you want to send a secret to Bob, you use Bob's public key. Only Bob (with his private key) can read it. If you want to prove something came from you (signing), you use YOUR own private key. Anyone with your public key can verify it.

Misconception 2, the "bigger is always better" fallacy, leads organizations to mandate RSA-8192 keys that slow down TLS handshakes without providing meaningful practical benefit. The marginal security gain from 4096-bit RSA versus 3072-bit RSA against classical attacks is negligible, while the performance cost is significant. More importantly, both are vulnerable to quantum attacks. The correct response to quantum risk is algorithm replacement (ML-KEM/ML-DSA), not larger classical keys.

Misconception 4, that signatures encrypt, frequently appears in security requirements documents. A common misspecification is "all data must be signed and encrypted" when the author means "authenticated and encrypted." These are distinct operations and must be composed carefully. The correct pattern for confidential and authenticated communication is: encrypt the message with the recipient's public key (or a symmetric key encapsulated therein) AND sign the plaintext or ciphertext with the sender's private key. The ordering matters: sign-then-encrypt provides non-repudiation while keeping the signature itself confidential; encrypt-then-sign may expose the signature to context-stripping attacks.

Misconception 5, HTTPS as a trust indicator, has been extensively exploited. Phishing campaigns began routinely using HTTPS after free certificate issuance from Let's Encrypt became widespread around 2017. A 2019 APWG report found that more than 58% of phishing sites used HTTPS. Browsers have largely stopped displaying the padlock as a "safe" indicator; Chrome and Firefox now simply do not display warnings for HTTPS sites, reserving warnings for HTTP connections. Security awareness training must explicitly teach that the padlock means "connection is encrypted", not "this is a legitimate organization."

Almost everyone holds at least one PKI misconception initially, so correcting them without judgment, for example the belief that a certificate proves a site is trustworthy rather than merely that the connection is encrypted and the domain validated, is part of the learning.
:::

%%%
---
unit: Infrastructure
code: OPENSSL
title: Tool Spotlight, OpenSSL Command-Line Reference
---
:::callout style=soft
**OpenSSL** is the most widely deployed open-source cryptographic library and command-line toolkit. Proficiency with its CLI enables certificate inspection, key generation, TLS debugging, and manual validation, essential skills for any security practitioner.
:::

:::table
| Task | OpenSSL Command | Notes |
|---|---|---|
| Generate RSA-3072 private key | `openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out priv.pem` | PKCS#8 format; use -aes256 to password-encrypt |
| Generate EC P-256 key | `openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ec.pem` | NIST P-256 (secp256r1) |
| Create self-signed certificate | `openssl req -new -x509 -key priv.pem -out cert.pem -days 365` | Prompts for Subject DN fields |
| Inspect certificate fields | `openssl x509 -in cert.pem -text -noout` | Prints all fields including extensions |
| Verify certificate chain | `openssl verify -CAfile ca-bundle.pem cert.pem` | Returns OK or error details |
| Check TLS server live | `openssl s_client -connect example.com:443 -servername example.com` | Shows full certificate chain and cipher suite |
| Extract server certificate | `openssl s_client -connect example.com:443 </dev/null 2>/dev/null \| openssl x509 -text -noout` | Pipe to x509 for field inspection |
| Sign a file (RSA-PSS) | `openssl dgst -sha256 -sigopt rsa_padding_mode:pss -sign priv.pem -out sig.bin data.txt` | FIPS 186-5 preferred signature padding |
| Verify signature | `openssl dgst -sha256 -sigopt rsa_padding_mode:pss -verify pub.pem -signature sig.bin data.txt` | Returns "Verified OK" or failure |
:::

:::image src="images/26_openssl_tool_spotlight.png" alt="Terminal screenshot mockup showing several OpenSSL commands: first section shows key generation command with output showing key parameters; second section shows s_client connecting to a TLS server with certificate chain printed in structured text; third section shows x509 -text output with annotated fields pointing to Subject, Issuer, Validity, and Subject Public Key Info sections; color-coded annotations highlight the relevant output for each command" caption="OpenSSL command-line reference for common PKI and TLS tasks. The s_client command is particularly valuable for live debugging of certificate chain issues, cipher suite negotiation, and protocol version negotiation." width=full
:::

:::notes
OpenSSL is the backbone of internet cryptography. The libssl and libcrypto libraries underpin Apache, Nginx, OpenSSH, curl, and thousands of other critical infrastructure components. Knowing how to use the OpenSSL command-line interface is not merely a developer skill, it is essential forensic and diagnostic capability for security practitioners who need to inspect certificates, debug TLS connections, or verify cryptographic operations manually.

The `openssl s_client` command is arguably the most useful single command in the toolkit for security work. When run against a TLS server, it performs a complete TLS handshake and prints the full certificate chain, cipher suite, protocol version, and session parameters. This allows you to verify that a server presents the correct certificate, that the chain includes the expected intermediate CA, that the certificate has not expired, and that the server supports TLS 1.3. Adding `-verify_return_error` makes s_client return a non-zero exit code if certificate verification fails, enabling use in scripts.

The `openssl x509 -text -noout` command parses and prints every field of an X.509 certificate in human-readable format. This is essential for debugging mis-issuance, checking the Subject Alternative Names (to verify domain coverage), inspecting Key Usage extensions, and reading the CA Information Access extension (which contains the OCSP responder URL and CA certificate download URL embedded in the certificate itself).

The Heartbleed vulnerability (CVE-2014-0160) in OpenSSL 1.0.1 through 1.0.1f (2012–2014) is the most significant security incident involving OpenSSL and deserves mention in any OpenSSL discussion. A bounds-checking error in the TLS heartbeat extension implementation allowed an attacker to read up to 64KB of the server's process memory per request, without authentication. Over approximately two years, private keys, session tokens, passwords, and sensitive user data were exposed from hundreds of thousands of servers worldwide. The vulnerability was disclosed on April 7, 2014, simultaneously by a team at Google Security and by Codenomicon. The industry response, emergency patching of millions of servers, mandatory certificate re-issuance, and password reset campaigns, provided a vivid illustration of the systemic risk created by a single widely-deployed cryptographic library having a critical vulnerability.

The Log4Shell vulnerability (CVE-2021-44228, 2021) is a useful contrast: that was a Java library vulnerability rather than a cryptographic one, but it similarly illustrated the systemic risk of widely-deployed dependencies. The cryptographic lesson is that even mathematically sound algorithms can be rendered insecure by implementation errors in the libraries that implement them, reinforcing the importance of keeping cryptographic libraries patched and following advisories from NIST's National Vulnerability Database.

Inspecting a live TLS connection to a public domain shows the certificate chain: the server's leaf certificate, the intermediate CA that signed it, and the expiry dates. Reading that chain connects the abstract PKI hierarchy to a concrete, verifiable artifact.
:::

%%%
---
unit: Algorithms
code: KEYMGMT
title: Key Lifecycle Management, NIST SP 800-57
---
:::callout style=soft
Generating a strong key pair is only the beginning. **NIST SP 800-57 Part 1** defines the complete cryptographic key lifecycle: generation, establishment, storage, use, rotation, and destruction. Failures in any lifecycle phase can undermine mathematically sound cryptography.
:::

:::flow
**Generation:** Use a FIPS 140-3 validated RNG; generate keys inside an HSM where possible
**Registration:** Bind the public key to an identity via a CA-signed certificate (X.509 or otherwise)
**Establishment (Distribution):** Distribute the public key through authenticated channels; certificate chains provide this in PKI
**Storage:** Private key stored encrypted at rest; HSM for CA-class keys; passphrase-protected for user keys
**Use (Operational):** Each use of the private key should be logged; enforce rate limits and access controls
**Rotation:** Replace keys before the cryptoperiod expires (NIST SP 800-57 Table 1 defines cryptoperiods by algorithm and key type)
**Revocation:** Revoke certificate immediately upon compromise; publish CRL or update OCSP
**Archival:** Retain old keys only if needed to decrypt archival data; isolate from operational systems
**Destruction:** Securely zeroize all copies; verify deletion on storage media; document destruction
:::

:::image src="images/26_key_lifecycle_nist.png" alt="Circular lifecycle diagram with nine stages: Generation at top in green; clockwise to Registration (blue), Distribution (blue), Storage (yellow with HSM icon), Operational Use (green), Rotation (orange arrow), Revocation (red with CRL/OCSP icons), Archival (gray), Destruction (red with shredder icon); arrows connect each stage in sequence; a center badge shows NIST SP 800-57 Part 1 reference; side callouts note recommended cryptoperiods for each key type" caption="The NIST SP 800-57 key lifecycle: cryptographic security requires disciplined management at every phase, from generating keys with validated entropy to securely destroying all copies at end of life." width=full
:::

:::notes
Cryptographic keys are not static artifacts, they have lifetimes, and those lifetimes must be actively managed. A key generated with perfect entropy from a validated source and stored in an HSM can still be rendered useless by poor lifecycle management: keys that are never rotated, certificates that are never monitored for expiry, private keys stored in long-forgotten backup tapes, or key material that persists in swap files or cloud snapshots after "deletion."

NIST SP 800-57 Part 1 Rev. 5 is the authoritative lifecycle guidance document. It defines key types (private signature keys, public verification keys, symmetric encryption keys, etc.), lifecycle states (pre-activation, active, suspended, deactivated, compromised, destroyed), and recommended cryptoperiods, the maximum time a key should be used in any given state.

Cryptoperiods are perhaps the most operationally important concept. SP 800-57 Table 1 recommends, for example, that RSA/ECC private signature keys for general use have a cryptoperiod of one to three years. CA signing keys have shorter recommended cryptoperiods, often six months to two years for subordinate CAs, because their compromise has systemic impact. TLS session keys have a cryptoperiod measured in hours (the session duration). The rationale for limited cryptoperiods is multifold: it limits the exposure window if a key is compromised without detection; it forces regular re-validation of identity bindings; and it reduces the value of long-term stored ciphertext attacks.

Key generation quality is the foundation. NIST SP 800-133 specifies requirements for cryptographic key generation. The core requirement is that keys must be generated using an approved random bit generator (RBG) that is seeded with sufficient entropy from physical randomness sources. Several historical incidents trace to weak key generation: the 2008 discovery that Debian's OpenSSL packages had a broken random number generator that produced only 32,768 possible SSH keys per key type (CVE-2008-0166); the 2012 RSA key factorization study by Lenstra et al. that found millions of RSA public keys on the internet sharing prime factors due to low-entropy generation on embedded devices, meaning pairs of apparently independent keys could be factored by computing GCDs.

Key storage must match the sensitivity of the material. Private keys for individual users are typically stored in PKCS#8 encrypted PEM files, with a passphrase as the encryption key. CA private keys must be stored in HSMs. Cloud-based deployments should use cloud KMS services (AWS KMS, Azure Key Vault, GCP Cloud KMS), which provide HSM-backed storage and detailed audit logging of every key usage operation.

Key destruction at end-of-life is frequently neglected. Simply deleting a file does not remove key material from flash storage or SSDs; without cryptographic erasure or physical destruction, material may persist in wear-leveling blocks. NIST SP 800-88 Rev. 1 provides guidelines for media sanitization, including cryptographic erasure (encrypting the key material with a key that is then destroyed) and physical destruction for highest-sensitivity material.
:::

%%%
---
unit: Synthesis
code: PQC-MIGRATION
title: Post-Quantum Migration Planning
---
:::callout style=soft
**NIST FIPS 203, 204, and 205** (2024) finalize the first post-quantum cryptographic standards. Organizations must begin migration planning now, the "harvest now, decrypt later" threat means delay has immediate consequences for long-lived sensitive data.
:::

::::columns ratio=1:1
::col::
::::card heading="NIST PQC Standards (2024)"
:::list style=tight
- **FIPS 203, ML-KEM:** Key Encapsulation Mechanism (from CRYSTALS-Kyber). Replaces RSA-KEM and ECDH for key agreement.
- **FIPS 204, ML-DSA:** Digital Signature Algorithm (from CRYSTALS-Dilithium). Replaces ECDSA and RSA-PSS for signatures.
- **FIPS 205, SLH-DSA:** Stateless Hash-Based Signature Algorithm (from SPHINCS+). Alternative signature scheme based on hash functions.
:::
::::
::col::
::::card heading="Migration Phases (NSA CNSA 2.0)"
:::list style=tight
- **Phase 1 (Now–2025):** Inventory all asymmetric cryptography in use. Identify long-lived data requiring immediate protection (HNDL risk assessment).
- **Phase 2 (2025–2030):** Deploy hybrid TLS (classical + ML-KEM). Begin certificate migration. Test PQC performance.
- **Phase 3 (2030–2035):** Complete migration for all new systems. NSA CNSA 2.0 mandates ML-KEM and ML-DSA for national security systems.
:::
::::
::::

:::image src="images/26_pqc_migration_roadmap.png" alt="Gantt-style roadmap chart with three horizontal rows: top row 'Classical PKI' showing RSA and ECC bars running from 2024 to 2035 with a fade-out; middle row 'Hybrid Transition' showing combined classical+PQC bars from 2025 to 2033; bottom row 'PQC-Native' starting small in 2025 and growing to full coverage by 2035; a vertical red dashed line labeled 'CRQC Risk Window' spans 2030–2040; below the chart a legend explains FIPS 203 ML-KEM and FIPS 204 ML-DSA icons" caption="Post-quantum migration roadmap: the transition from classical to PQC cryptography requires parallel deployment of hybrid systems, inventory discovery, and phased migration, driven by NIST and NSA timelines." width=full
:::

:::notes
The post-quantum migration is not a future problem, it is a present one. The harvest-now-decrypt-later (HNDL) threat model requires organizations to assess which of their encrypted data must remain confidential for more than the anticipated CRQC timeline. Healthcare records subject to HIPAA must be protected for decades. Classified government communications may need protection for 25 years or more. Financial transaction records, legal communications, and intellectual property all have extended confidentiality requirements. For these categories of data, the relevant question is not "when will quantum computers arrive?" but "when was this data encrypted, and how long must it remain protected?"

NIST's 2024 PQC standards represent the culmination of an eight-year public competition that began in 2016 with 82 candidate algorithms from teams worldwide. The three finalized standards use distinct mathematical foundations. ML-KEM (FIPS 203) and ML-DSA (FIPS 204) are both based on module lattice problems, specifically the Module Learning With Errors (MLWE) problem, which are believed resistant to both classical and quantum attacks. SLH-DSA (FIPS 205) is based purely on the security of hash functions, providing a conservative backup in case lattice assumptions are broken. A fourth standard, FN-DSA (FIPS 206, based on FALCON), is expected to follow.

The hybrid transition approach is recommended by NIST IR 8413 and NSA CNSA 2.0 for the transition period. A hybrid key agreement combines a classical ECDH key exchange with an ML-KEM key encapsulation in a single protocol step; the two resulting shared secrets are combined through HKDF. This means an attacker would need to break both the classical and PQC algorithms to derive the session key. Hybrid approaches provide a safety net: if the PQC algorithm turns out to have an undiscovered vulnerability, the classical component still provides protection against classical attacks.

IETF has been working on hybrid TLS since 2022. RFC 9180 (HPKE, Hybrid Public Key Encryption) defines a construction that can incorporate PQC algorithms. Draft specifications for ML-KEM in TLS 1.3 (draft-ietf-tls-mlkem) and for hybrid X25519+ML-KEM (X25519MLKEM768) are in active development and have been experimentally deployed by Google Chrome and Cloudflare.

Key performance considerations: ML-KEM key sizes are larger than ECC equivalents. ML-KEM-768 (targeting NIST Security Level 2, roughly AES-192 equivalent) has a public key of 1184 bytes and a ciphertext of 1088 bytes, compared to 65 bytes for an ECDH P-256 public key. This has implications for certificate sizes and TLS handshake message sizes. ML-DSA-65 signatures are 3309 bytes versus 64 bytes for ECDSA P-256. These larger sizes require careful evaluation of bandwidth-constrained protocols (IoT, mobile) and performance-sensitive applications (high-frequency trading, CDN edge servers). That said, benchmarks show ML-KEM operations run at speeds competitive with RSA, and ML-DSA signing/verification is faster than RSA at equivalent security levels.

The post-quantum migration is underway in production: Google enabled a hybrid post-quantum key exchange (X25519MLKEM768) in Chrome in 2024, and Cloudflare reported that over 15% of its TLS traffic used hybrid post-quantum key exchange by early 2025.
:::

%%%
---
unit: Synthesis
code: TLS
title: Hybrid Cryptography in TLS 1.3
---
:::callout style=soft
Asymmetric cryptography is computationally heavy (100 to 1000 times slower than symmetric encryption). **TLS 1.3** (RFC 8446) resolves this by using asymmetric cryptography for key agreement and authentication, then transitioning to symmetric cryptography for bulk data transfer.
:::

:::steps
**Client Hello:** Client sends supported cryptographic suites (e.g., ECDHE, AES-GCM) and a key share.
**Server Hello:** Server selects parameters, sends its key share, digital certificate, and digital signature.
**Key Agreement:** Both parties compute the shared secret using ECDH. The asymmetric phase is now complete.
**Symmetric Session:** A symmetric session key is derived (e.g., AES-256-GCM) to encrypt all subsequent application data.
:::

:::image src="images/26_tls_handshake_hybrid.png" alt="Two-column timeline diagram showing TLS 1.3 handshake: left column labeled 'Client' and right column labeled 'Server' with horizontal arrows showing message flow; arrow 1 from Client to Server labeled 'ClientHello: key share, cipher suites'; arrow 2 from Server to Client labeled 'ServerHello: key share, certificate, signature, Finished'; a horizontal dashed line after arrow 2 labeled 'Asymmetric Phase Complete, Shared Secret Derived'; arrows below show AES-GCM encrypted Application Data flowing in both directions labeled 'Symmetric Phase: high-speed encrypted data'" caption="TLS 1.3 handshake: the asymmetric phase (ECDHE key exchange + certificate authentication) establishes a shared secret in a single round trip. The symmetric phase (AES-256-GCM) handles all subsequent data at high speed." width=full
:::

:::notes
Asymmetric cryptographic operations are computationally expensive. RSA encryption and decryption require modular exponentiation with very large integers; even ECC, which is faster, involves multiple elliptic curve point multiplication operations. Benchmarks show that asymmetric operations run 100 to 1000 times slower than symmetric operations like AES-GCM. If a server streaming 4K video had to use RSA to encrypt every packet, it would be completely unable to sustain throughput. This is why modern secure communications use a hybrid model.

Transport Layer Security 1.3, defined in RFC 8446 and published in 2018, is the definitive modern example of hybrid cryptography in action. TLS 1.3 represents a major redesign over its predecessors. TLS 1.2 required two full round trips before data could flow; TLS 1.3 completes the handshake in a single round trip, and supports 0-RTT resumption for returning clients. TLS 1.2 supported many legacy algorithm combinations including RC4, DES, and SHA-1 based cipher suites; TLS 1.3 removes all these, mandating only modern authenticated encryption with associated data (AEAD) cipher suites.

The TLS 1.3 handshake proceeds as follows. In the ClientHello message, the client announces which cipher suites it supports (for example, TLS_AES_256_GCM_SHA384 with ECDHE using P-384) and proactively sends a key share, an ECDHE public key, for each group it supports. The server receives the ClientHello, selects the strongest mutually supported cipher suite, and responds with its own ECDHE key share, its X.509 digital certificate, and a digital signature over the handshake transcript using its private key. The server immediately derives the session key and sends an encrypted Finished message.

Both parties independently compute the ECDHE shared secret using the exchanged key shares. This secret is then processed through the TLS key schedule, a series of HKDF (HMAC-based Key Derivation Function) operations, to derive separate symmetric keys for encryption in each direction. From this point forward, all application data is encrypted with AES-256-GCM or ChaCha20-Poly1305, both of which are AEAD ciphers providing both confidentiality and integrity in a single pass.

The use of ephemeral key shares (the E in ECDHE) is essential for Perfect Forward Secrecy. Each TLS 1.3 session uses a freshly generated, ephemeral ECDHE key pair that is discarded after the handshake. This means that even if an attacker records encrypted TLS sessions now and later compromises the server's long-term private key, they cannot decrypt the recorded sessions. The session keys were derived from ephemeral material that no longer exists. This property is critical given that nation-state adversaries are known to conduct "record now, decrypt later" collection campaigns against encrypted traffic.

TLS 1.3 also authenticates the server, and optionally the client, through the digital certificate mechanism. When the client receives the server's certificate, it validates the chain of trust against its root store using the PKI mechanisms discussed in the previous slides. The server's digital signature over the handshake transcript proves that the server possessing the private key corresponding to the certificate's public key is the one you are talking to, preventing man-in-the-middle attacks. TLS 1.3 thus elegantly combines the scale and trust of asymmetric PKI with the performance efficiency of symmetric AEAD ciphers, achieving confidentiality, integrity, and authenticity at internet scale.
:::

%%%
---
unit: Summary
code: SUM
title: Cryptographic Agility & The Quantum Horizon
---
:::callout style=soft
The mathematical assumptions protecting RSA and ECC will not hold forever. Cryptographic agility is the capacity to transition to new algorithms without replacing the underlying application infrastructure.
:::

::::columns ratio=1:1
::col::
::::card heading="Shor's Algorithm & Threat"
:::list style=tight
- **The Quantum Risk:** Shor's algorithm solves prime factorization and discrete logarithms in polynomial time.
- **Vulnerable Algorithms:** RSA, ECC, DH, and ECDSA will be completely broken.
- **Symmetric Safety:** AES-256 remains secure (requires Grover's algorithm search).
:::
::::
::col::
::::card heading="Post-Quantum Cryptography (PQC)"
:::list style=tight
- **NIST PQC Standardization:** Initiated to select quantum-resistant algorithms.
- **Lattice-Based Math:** Hard problems based on high-dimensional vector spaces.
- **Standards:** ML-KEM (key encapsulation) and ML-DSA (signatures).
:::
::::
::::

:::image src="images/26_quantum_threat_timeline.png" alt="Timeline graphic showing three eras: left section labeled 'Classical Era (now)' with RSA and ECC icons marked as secure; center section labeled 'Harvest Now / Decrypt Later Threat' showing adversaries recording encrypted traffic today; right section labeled 'Post-Quantum Era' showing ML-KEM and ML-DSA icons; a vertical dashed line in the center is labeled 'Cryptographically Relevant Quantum Computer (CRQC)' with an arrow pointing right; below the timeline a bar chart compares classical vs quantum algorithm complexity" caption="The quantum cryptographic threat timeline: today's encrypted traffic is being archived for future decryption. Organizations must begin post-quantum migration before CRQCs become operational." width=full
:::

:::notes
We conclude today's class by examining the long-term horizon of asymmetric cryptography. The entire security of RSA, ECC, Diffie-Hellman, and ECDSA depends on the computational hardness of specific mathematical problems. For classical computers, these problems remain intractable at recommended key sizes. However, the emergence of quantum computing introduces an existential threat to these hardness assumptions.

In 1994, mathematician Peter Shor published a quantum algorithm, now known as Shor's algorithm, that can solve both the integer factorization problem and the discrete logarithm problem (including the elliptic curve variant) in polynomial time on a quantum computer. Unlike classical algorithms, which require exponential or sub-exponential time, Shor's algorithm operates in $O((\log n)^3)$ time. This means that a sufficiently powerful quantum computer could factor a 2048-bit RSA modulus in minutes or hours rather than millions of years. Every asymmetric algorithm discussed in today's lecture, RSA, ECDH, ECDSA, DSA, would become completely broken.

The critical question is timeline. Current quantum computers, even the most advanced systems from IBM and Google, operate with dozens to hundreds of noisy qubits. Breaking RSA-2048 is estimated to require millions of error-corrected logical qubits. Building a Cryptographically Relevant Quantum Computer (CRQC) of this scale involves extraordinary engineering challenges: qubit coherence times, error correction overhead, and physical cooling requirements remain formidable barriers. Expert estimates vary widely, with most projecting CRQCs are still 10 to 20 years away, though some assess a non-trivial probability within 10 years.

This timeline uncertainty itself creates a present danger known as "harvest now, decrypt later" (HNDL) attacks. Nation-state intelligence agencies are believed to be recording large volumes of encrypted network traffic today, archiving it for future decryption once quantum capability matures. Data that must remain confidential for decades, classified government communications, long-term financial records, medical histories, is therefore at risk even if CRQCs do not exist today.

In response, NIST launched the Post-Quantum Cryptography (PQC) standardization process in 2016, evaluating over 80 candidate algorithms. In 2024, NIST published the first set of finalized PQC standards. ML-KEM (Module-Lattice-Based Key Encapsulation Mechanism, from the CRYSTALS-Kyber submission) is standardized as FIPS 203 for key exchange. ML-DSA (Module-Lattice-Based Digital Signature Algorithm, from CRYSTALS-Dilithium) is standardized as FIPS 204 for digital signatures. These algorithms are based on the hardness of lattice mathematical problems, specifically the Learning With Errors (LWE) problem, which are believed to resist both classical and quantum attacks.

For symmetric algorithms, the quantum threat is less severe. Grover's algorithm can search an unsorted database of $N$ items in $\sqrt{N}$ steps, effectively halving the security strength of symmetric keys. AES-128 would provide only 64-bit security against a quantum attacker; AES-256 would provide 128-bit security, which remains adequate. Therefore, existing symmetric infrastructure requires only key length upgrades, not algorithm replacement.

Cryptographic agility is the organizational and technical capacity to swap cryptographic algorithms without rebuilding underlying applications. Organizations must begin building PQC readiness now: identifying all systems that use asymmetric cryptography, evaluating their exposure to HNDL attacks, and testing hybrid TLS configurations that combine classical and post-quantum key exchange. NIST SP 800-208 and the NSA's CNSA 2.0 suite provide roadmaps for this transition. Thank you, and I will see you in the next class, where we put these cryptographic tools into their broader architectural context.
:::

%%%
---
unit: Synthesis
code: ARCH
title: Applied Cryptography Architecture Patterns
---
:::callout style=soft
Understanding individual algorithms is necessary but not sufficient. Secure systems combine cryptographic primitives in specific **patterns**, sign-then-encrypt, authenticated key exchange, sealed envelope, each offering distinct security guarantees.
:::

::::columns ratio=1:1
::col::
::::card heading="Sign-then-Encrypt"
:::list style=tight
- Sign the plaintext with sender's private key first
- Encrypt the signed message with recipient's public key (or encapsulated symmetric key)
- Recipient decrypts, then verifies signature
- Provides: Confidentiality + Authenticity + Non-repudiation
- Caveat: Signature is hidden inside ciphertext; recipient knows who signed but outer observer does not
:::
::::
::col::
::::card heading="Encrypt-then-MAC (Symmetric Pattern)"
:::list style=tight
- Encrypt plaintext with symmetric key (AES-CTR or AES-CBC)
- Compute MAC (HMAC-SHA256) over the ciphertext
- Append MAC to ciphertext
- Verify MAC before decrypting (prevents padding oracle attacks)
- Preferred over MAC-then-encrypt; used in TLS 1.2 with AEAD modes
:::
::::
::::

:::image src="images/26_crypto_architecture_patterns.png" alt="Two side-by-side flow diagrams: left diagram labeled 'Sign-then-Encrypt' shows plaintext entering SHA-256 hash, then signed with Alice's private key producing a signed message, then the entire signed message encrypted with Bob's public key producing ciphertext; arrows label each step with the security property provided; right diagram labeled 'Authenticated Encryption (AEAD)' shows plaintext and AAD entering AES-256-GCM producing ciphertext and authentication tag together in one pass, with a note 'single primitive provides both confidentiality and integrity'" caption="Two fundamental cryptographic composition patterns: Sign-then-Encrypt for asymmetric non-repudiation with confidentiality; Authenticated Encryption (AEAD) for symmetric bulk data where a single pass provides both confidentiality and integrity." width=full
:::

:::notes
One of the most important lessons in applied cryptography is that choosing good algorithms is only the beginning. How those algorithms are composed, the pattern in which they are combined, determines whether the resulting system has the intended security properties. The academic literature is full of examples of systems built from strong algorithms that were combined in ways that introduced catastrophic vulnerabilities.

The Sign-then-Encrypt pattern is the correct construction for non-repudiable confidential communication. The key ordering is critical: we sign first (over the plaintext), then encrypt (the signed message). When Alice receives the decrypted message and finds Bob's signature, she knows Bob signed this specific plaintext. An alternative pattern, Encrypt-then-Sign (encrypt first, then sign over the ciphertext), has a subtle problem: Bob's signature proves he signed a specific ciphertext, but it does not prove he knows what is inside it. An attacker could strip Bob's signature from one ciphertext, attach it to a different ciphertext, and claim Bob authorized the new content. While this attack requires the attacker to find or construct a ciphertext that decrypts to useful content (which is hard with OAEP padding), the principle that Sign-then-Encrypt gives stronger security properties is well-established.

AEAD (Authenticated Encryption with Associated Data) is the modern pattern for symmetric bulk data encryption. AES-256-GCM and ChaCha20-Poly1305 are both AEAD ciphers: they produce both ciphertext and an authentication tag in a single pass. The authentication tag is a MAC computed over both the ciphertext and optional additional data (AAD), data that is authenticated but not encrypted, such as packet headers. AEAD eliminates the need to separately apply a MAC, which historically led to vulnerabilities when implementors chose incorrect composition ordering (MAC-then-Encrypt, used in TLS 1.2 with CBC mode, is vulnerable to padding oracle attacks like POODLE because the MAC is checked only after decryption, allowing attackers to probe padding validity).

The Hybrid Encryption pattern, used in TLS and email encryption, combines asymmetric and symmetric cryptography: generate a random symmetric key (data encryption key, DEK), encrypt the DEK with the recipient's public key (key encapsulation), and encrypt the actual data with the DEK using AES-GCM. The recipient decapsulates the DEK using their private key, then decrypts the data. This is the pattern standardized in HPKE (RFC 9180) and PKCS#7/CMS for S/MIME.

The Key Wrap pattern (NIST SP 800-38F) addresses the specific need to protect cryptographic key material stored at rest or in transit. AES Key Wrap (AES-KW) encrypts a symmetric key using another symmetric key (a Key Encryption Key, KEK), with integrity protection designed to detect accidental or malicious modification. AWS KMS, Azure Key Vault, and GCP Cloud KMS all implement key wrapping internally to protect customer keys.

The Cryptographic Doom Principle (Thomas Ptacek) states that if you perform any cryptographic operation on a received message before verifying its MAC, that operation will somehow be used to attack you. This is why encrypt-then-MAC is correct and MAC-then-encrypt is dangerous: integrity must be verified before any work is done on the data.
:::

%%%
---
unit: Summary
code: FINAL-SUM
title: Class 26 Summary, Key Takeaways and Standards Reference
---
:::callout style=soft
Asymmetric cryptography solves the key distribution dilemma through trapdoor mathematics, enabling secure key exchange, digital identity, and non-repudiation at global scale. The standards landscape is actively evolving toward post-quantum algorithms.
:::

:::table
| Concept | Core Standard | Key Point |
|---|---|---|
| Trapdoor functions | NIST SP 800-57 | Basis of all asymmetric security: integer factorization, DLP, ECDLP |
| RSA | RFC 8017 (PKCS#1 v2.2) | Use OAEP padding; minimum 3072-bit keys for new systems |
| ECC | NIST SP 800-186, FIPS 186-5 | P-256 for 128-bit security; Curve25519 for high-performance contexts |
| Digital Signatures | FIPS 186-5 | SHA-256 minimum hash; ECDSA-P256 or Ed25519 recommended |
| X.509 Certificates | RFC 5280 | Binds public key to identity; check SAN, validity, key usage |
| PKI Trust Chains | RFC 5280, CA/B Forum Baseline Req. | Root → Intermediate → Leaf; validate full chain; check revocation |
| TLS 1.3 | RFC 8446 | Hybrid crypto: ECDHE for key exchange, AES-256-GCM for data |
| Revocation | RFC 5280 (CRL), RFC 6960 (OCSP) | Prefer OCSP Stapling; OCSP Must-Staple for high-security contexts |
| Post-Quantum | FIPS 203, 204, 205 (2024) | ML-KEM replaces ECDH; ML-DSA replaces ECDSA; begin hybrid deployment now |
:::

:::image src="images/26_class_summary_standards_map.png" alt="Visual standards map: a central node labeled 'Asymmetric Cryptography'; radiating branches to algorithm nodes (RSA, ECC, DH) each with their RFC or FIPS number; PKI branch leading to X.509, CRL, OCSP, CT each with RFC numbers; TLS 1.3 branch with RFC 8446; Post-Quantum branch with FIPS 203, 204, 205 highlighted in purple; bottom banner shows three key takeaways: '1. Math hardness is the root of all security', '2. PKI binds math to identity', '3. Hybrid crypto is the practical architecture'" caption="Class 26 standards reference map: the complete ecosystem of asymmetric cryptography from mathematical foundations through deployed protocols and the post-quantum transition." width=full
:::

:::notes
We have covered a significant amount of material in this lecture, from abstract mathematical foundations through deployed protocols and current standardization. Let me consolidate the key takeaways.

The foundational insight of asymmetric cryptography, developed by Diffie and Hellman in 1976 and implemented in RSA by 1977, was that mathematics could replace physical key distribution. By exploiting the asymmetry between easy and hard computational directions in trapdoor functions, two strangers on an open network can establish a shared secret without prior coordination. This insight underpins every secure internet connection, every HTTPS session, every software download you trust. It is not an exaggeration to call it one of the defining intellectual achievements of the 20th century.

The algorithms we studied, RSA and ECC, instantiate this insight in different mathematical structures. RSA uses integer factorization; ECC uses elliptic curve discrete logarithms. Both are secure at their recommended NIST key sizes. Both are vulnerable to quantum computing via Shor's algorithm. The migration to post-quantum algorithms (FIPS 203, 204, 205) is underway but will take a decade to complete.

PKI is the institutional and technical infrastructure that makes asymmetric cryptography useful at scale. Without the trust hierarchy of Root CAs, Intermediate CAs, and leaf certificates, without Certificate Transparency logs, revocation mechanisms, and the CA/Browser Forum Baseline Requirements, a mathematically perfect key pair would be useless for authenticating identities over the internet. PKI is where cryptography meets policy, law, organizational process, and human trust.

Digital signatures are the cryptographic primitive that enables non-repudiation: the ability to cryptographically prove that a specific private key signed a specific message. This property underpins legally binding electronic contracts (eIDAS, ESIGN Act), software distribution integrity (code signing), and authenticated communication at every level of the internet stack.

TLS 1.3 is the masterclass in applied cryptographic composition: asymmetric operations for key agreement and authentication, ephemeral key pairs for perfect forward secrecy, AEAD ciphers for bulk data, and HKDF for key derivation. Understanding this protocol end-to-end gives you a mental model you can apply to evaluate any new secure communication protocol.

The practical skills dimension, OpenSSL command-line usage, certificate inspection, revocation validation, key lifecycle management, transforms theoretical knowledge into operational capability. Security practitioners who can diagnose a certificate chain failure, interpret an OCSP response, and verify a digital signature at the command line are substantially more effective than those who understand the concepts abstractly but cannot apply them.

Looking ahead: the post-quantum transition is the defining cryptographic challenge of this decade. NIST's FIPS 203, 204, and 205 standards published in 2024 provide the algorithm choices. The engineering work of integrating these algorithms into TLS, certificates, code-signing, and PKI infrastructure is actively ongoing. Organizations that begin their cryptographic inventory and hybrid deployment planning now will be substantially better positioned than those who defer until quantum computers become operationally relevant. The harvest-now-decrypt-later threat means the cost of inaction is already accumulating for organizations with long-lived sensitive data.

Production deployment data, such as Cloudflare's and Google's hybrid TLS rollouts and the NIST post-quantum FAQ, makes the post-quantum transition concrete rather than speculative, which conveys its urgency better than theoretical timelines.
:::
