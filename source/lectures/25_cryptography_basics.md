---
deck:
  title: Cryptography Basics
  kicker: Class 25
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 25
  description: Encryption, keys, and hashing, the mathematical foundations of confidentiality, integrity, and authenticity.
  topics: [Encryption, Symmetric Cryptography, Cryptographic Keys, Hashing, Key Stretching]
---

%%%
---
title: Cryptography Basics
cover: true
---
:::text class=sub
The Mathematical Bedrock of Information Security: Symmetric Ciphers, Hashing Primitives, and Key Entropy
:::
:::list style=chips
- Information Theory Foundations
- Symmetric Block & Stream Ciphers
- Cryptographic Hash Functions
- CIA Triad Enforcement
:::

:::image src="images/25_cover_cryptography_overview.png" alt="Conceptual overview diagram split into three labeled columns: left column shows a padlock icon over a data-flow arrow representing Encryption; center column shows a fingerprint icon over a fixed-length bit string representing Hashing; right column shows a key ring representing Key Management; at the bottom, arrows from all three columns converge into a CIA Triad triangle labeled Confidentiality, Integrity, Authenticity" caption="Cryptography provides three foundational security primitives, encryption, hashing, and key management, each enforcing a different property of the CIA Triad." width=full
:::

%%%
---
unit: Foundations
code: CRY
title: What Is Cryptography?
---
:::callout style=soft
**Cryptography** is the mathematical discipline of transforming information to secure communication and protect data assets in the presence of adversarial entities. It relies on computational hardness assumptions rather than security through obscurity.
:::

::::columns ratio=1:1
::col::
::::card heading="Core Cryptographic Objectives"
:::list style=tight
- **Confidentiality**: Ensuring unauthorized entities cannot read data (enforced via encryption).
- **Integrity**: Detecting unauthorized modifications to data (enforced via hash functions).
- **Authentication**: Verifying the identity of a communication entity (enforced via digital signatures).
- **Non-Repudiation**: Preventing a party from denying a past action (enforced via digital signatures).
:::
::::
::col::
::::card heading="Kerckhoffs's Principle"
:::callout style=line
A cryptosystem must remain secure even if everything about the system is public knowledge, except for the key. Modern cryptography relies on peer-reviewed, standardized algorithms (NIST, ISO).
:::
::::
::::

:::image src="images/25_cryptography_cia_objectives.png" alt="Four-quadrant diagram on a white background: top-left quadrant labeled Confidentiality with an encrypted data-stream icon; top-right labeled Integrity with a hash function and verified checksum icon; bottom-left labeled Authentication with an identity badge and digital signature; bottom-right labeled Non-Repudiation with a signed contract icon; the center of all four quadrants shows the word Cryptography with arrows pointing outward to each quadrant" caption="The four cryptographic security objectives, confidentiality, integrity, authentication, and non-repudiation, form the foundational requirements that all cryptographic systems are designed to fulfill." width=full
:::

:::notes
Cryptography is the scientific discipline that underpins almost all technical controls in cybersecurity. It is not merely the "scrambling" of text; it is a branch of applied mathematics combining number theory, abstract algebra, and information theory. Its primary goal is to allow secure communication over an insecure medium, such as the internet, where adversaries can intercept, modify, or inject data. NIST Special Publication 800-175B, "Guideline for Using Cryptographic Standards in the Federal Government," and ISO/IEC 18033 together define the approved primitives and deployment guidelines for modern cryptographic systems in both commercial and federal environments.

Modern cryptography is built on Kerckhoffs's principle, formulated by Auguste Kerckhoffs in 1883. This principle states that the security of a cryptosystem must depend solely on the secrecy of the key, not on keeping the algorithm secret. This is a critical departure from "security through obscurity." In modern security engineering, we use public, heavily audited algorithms standardized by bodies like the National Institute of Standards and Technology (NIST) and the International Organization for Standardization (ISO). Any algorithm whose security relies on its obscurity will quickly fail once its mechanism is reverse-engineered or leaked, a lesson repeatedly demonstrated when proprietary ciphers have been cracked within months of public disclosure.

Cryptography provides four essential security guarantees. Confidentiality ensures that data remains unreadable to unauthorized parties; without encryption, communications are exposed in cleartext, as occurred in the 2013 Target breach where unencrypted card data traversed internal network segments accessible to any compromised host. Integrity detects unauthorized modification; cryptographic hashes applied to software packages allowed security researchers to detect the SolarWinds Orion supply-chain compromise in 2020, where attackers had injected a backdoor (SUNBURST) into signed software builds. Authentication confirms the identity of communicating entities, preventing impersonation attacks that underpin man-in-the-middle exploits. Non-repudiation binds an action to a specific identity; under legal frameworks such as the U.S. Electronic Signatures in Global and National Commerce Act (ESIGN) and the EU eIDAS Regulation, cryptographic digital signatures carry legal weight equivalent to handwritten signatures and are required for legally binding electronic contracts, code-signing obligations, and regulated financial transactions.

Over the course of this lecture, we will study the mathematical primitives, specifically encryption algorithms and hash functions, that allow us to achieve these guarantees in production environments, protecting both data at rest and data in transit. These standards are not merely academic: compliance frameworks including PCI DSS (Requirement 3.5), HIPAA Security Rule (45 CFR §164.312), and GDPR Article 32 mandate specific cryptographic controls, and failure to implement them correctly has resulted in multi-billion dollar regulatory fines and reputational damage for major enterprises worldwide.
:::

%%%
---
unit: Foundations
code: MTH
title: "Mathematical Foundations: Modular Arithmetic"
---
:::callout style=soft
Most modern cryptographic algorithms rely on **modular arithmetic** (often called "clock arithmetic") and the properties of **prime numbers** to construct one-way functions and computational traps.
:::

::::columns ratio=1:1
::col::
::::card heading="Modular Arithmetic Properties"
:::list style=tight
- **Definition**: $a \equiv b \pmod n$ means $a - b$ is divisible by $n$.
- **Finite Fields**: Limits numbers to a fixed range $[0, n-1]$, preventing integer overflow and masking size information.
- **One-Way Functions**: While modular exponentiation ($g^x \pmod p$) is fast, computing the inverse ($x$ given $y = g^x \pmod p$) is the **Discrete Logarithm Problem**, which is computationally infeasible for large primes.
:::
::::
::col::
:::table
| Mathematical Problem | Complexity Class | Cryptographic Application |
|---|---|---|
| Prime Factorization | NP-Intermediate | RSA Cryptosystem |
| Discrete Logarithm | NP-Intermediate | Diffie-Hellman Key Exchange |
| Elliptic Curve Discrete Log | NP-Intermediate | ECDSA, ECDH (ECC) |
:::
::::

:::image src="images/25_modular_arithmetic_one_way.png" alt="Two-panel diagram: left panel shows modular exponentiation with input x, a forward arrow labeled 'Easy: compute g^x mod p in milliseconds', and the result y; right panel shows the same y with a steep upward arrow labeled 'Hard: Discrete Logarithm Problem, find x given g, p, and y, requires astronomical computation for large primes'; a wall labeled NP-Intermediate separates the two directions; a clock face in the corner illustrates the wrap-around property of modular arithmetic" caption="Modular exponentiation is computationally easy in the forward direction but infeasible to reverse. This asymmetry, the Discrete Logarithm Problem, is the mathematical foundation of Diffie-Hellman key exchange, DSA, and Elliptic Curve Cryptography." width=full
:::

:::notes
To appreciate how cryptography works, we must look at the underlying mathematics. Unlike classical ciphers, which relied on simple letter substitutions and transpositions, modern cryptography is built on modular arithmetic and number theory. These mathematical structures, formalized in NIST SP 800-186 for elliptic curve systems and NIST SP 800-131A for classical integer-based systems, provide the computational hardness properties that protect modern communications.

Modular arithmetic operates within a finite field of numbers. Instead of numbers increasing infinitely, they wrap around when they reach a modulus, $n$, much like a twelve-hour clock. If a clock reads 11 o'clock and you add 3 hours, you get 2, not 14. This wrapping property is highly valuable for cryptography. First, it ensures that all calculations result in numbers within a predictable, fixed range, making data storage and processing efficient. Second, it destroys size information, if you see a modular result, you cannot easily infer the size of the input numbers, adding a layer of mathematical obfuscation that hides structural information from an attacker.

More importantly, modular arithmetic allows us to construct one-way functions. These are functions that are easy to compute in one direction but extremely difficult to reverse. For example, in a large prime field, calculating $g^x \pmod p$ is computationally trivial, a modern processor can perform this operation in microseconds. However, if you are given the result $y$ and asked to find the exponent $x$, you must solve the Discrete Logarithm Problem. For prime numbers that are thousands of bits long, this calculation would require classical supercomputers billions of years, placing it firmly in the NP-Intermediate complexity class, hard but not proven NP-Complete.

The security of different cryptographic systems relies on different instances of this asymmetry. RSA depends on the difficulty of factoring large semiprime numbers, two large primes multiplied together. NIST SP 800-131A requires a minimum RSA key size of 2048 bits for near-term security, transitioning to 3072 bits for new deployments beyond 2030 to maintain equivalent security strength as factoring algorithms improve. Diffie-Hellman key exchange and the Digital Signature Algorithm (DSA) rely on the Discrete Logarithm Problem over finite prime fields; NIST recommends a minimum group size of 2048 bits. Elliptic Curve Cryptography, standardized under NIST SP 800-186 with approved curves including P-256, P-384, and P-521, provides equivalent strength to RSA at far smaller key sizes by operating on the Elliptic Curve Discrete Logarithm Problem (ECDLP), which is believed to be computationally harder per bit than the integer DLP. Understanding these mathematical foundations is essential for informed algorithm selection, compliance with federal mandates such as CNSA 2.0, and evaluating the quantum computing threat that specifically targets these hard problems.
:::

%%%
---
unit: Basics
code: ENC
title: "Cryptographic Transposition: Encryption & Decryption"
---
::::columns ratio=1:1
::col::
:::flow
Plaintext (P)
Encryption Algorithm (E) + Key (K)
Ciphertext (C)
Decryption Algorithm (D) + Key (K)
Plaintext (P)
:::
::col::
:::callout style=soft
**The Encryption Process**
$$\text{Encryption: } E_K(P) = C$$
$$\text{Decryption: } D_K(C) = P$$
The security of the ciphertext $C$ relies on the inability of an attacker to compute $P$ from $C$ without possession of the secret key $K$.
:::
::::
:::list heading="Core Terminology" style=plain
- **Plaintext ($P$)**: The original, unencrypted data.
- **Cipher ($E$/$D$)**: The mathematical algorithm used to encrypt and decrypt.
- **Key ($K$)**: A parameter that selects a specific permutation from the cipher's keyspace.
- **Ciphertext ($C$)**: The encrypted, unintelligible output of the encryption process.
:::

:::image src="images/25_encryption_decryption_model.png" alt="Horizontal flow diagram: far left is a document icon labeled Plaintext P; an arrow points to a processor box labeled Encryption Algorithm E with a key icon above labeled Key K; an arrow exits to a scrambled block labeled Ciphertext C; a second arrow continues through a processor box labeled Decryption Algorithm D with the same Key K above; the final arrow points to a matching document icon labeled Plaintext P; an adversary figure below the ciphertext arrow carries a red X indicating inability to recover P without K" caption="The fundamental encryption model: plaintext is transformed to ciphertext using a public algorithm and a secret key. The ciphertext is computationally secure against an adversary who lacks the key." width=full
:::

:::notes
Let's formalize the basic model of encryption and decryption. This process is a mathematical transformation governed by Kerckhoffs's principle: the algorithm is public; the key is secret. We start with plaintext, denoted as $P$, which represents the original, readable data. We pass this plaintext through an encryption algorithm, $E$, along with a cryptographic key, $K$. The output is ciphertext, denoted as $C$, which is a scrambled representation of the data that an adversary intercepting it cannot read.

To recover the plaintext, the recipient passes the ciphertext through a decryption algorithm, $D$, along with the correct key, $K$. Mathematically, $D_K(C) = P$. The encryption and decryption algorithms are public, standardized ciphers published by NIST (e.g., FIPS 197 for AES) and ISO (e.g., ISO/IEC 18033-3). The security of the system relies entirely on the secrecy of the key. This means the algorithm can be, and should be, published for public cryptanalytic scrutiny without compromising the data it protects.

If an attacker intercepts the ciphertext $C$ in transit, they cannot reverse the encryption function without the key, because the mathematical transformation is designed to be computationally irreversible without that specific key input. The key acts as a "trapdoor," providing the parameter needed to efficiently reverse the function. Without it, the attacker faces an exhaustive search of the entire keyspace.

The lifecycle of a key is governed by NIST SP 800-57, "Recommendation for Key Management," across three parts covering general guidance, best practices, and application-specific guidance. This standard defines key states, pre-activation, active, suspended, deactivated, compromised, and destroyed, and mandates that transitions between states be formally tracked. Keys must be generated using Cryptographically Secure Pseudo-Random Number Generators (CSPRNGs) as specified in NIST SP 800-90A, stored in tamper-resistant Hardware Security Modules (HSMs) meeting FIPS 140-3 Level 2 or higher requirements, and rotated on schedules that limit data exposure per key. In the 2017 WannaCry ransomware attack, approximately 200,000 systems were encrypted by malware exploiting the NSA's EternalBlue vulnerability (MS17-010). Many organizations failed to recover their data because they had no formal key management strategy, the ransomware held the only copy of the decryption key. Robust key management per SP 800-57, with organization-controlled keys backed up in HSMs, would have enabled recovery without paying attackers. ISO/IEC 11770 provides an international complement to NIST's key management guidance and is widely adopted outside the U.S. federal sphere.

Data classification under ISO/IEC 27001 Annex A Control 8.24 requires encrypting sensitive data both at rest and in transit. If the key is lost or destroyed without secure backup, encrypted data is permanently irrecoverable, a data loss scenario as irreversible as physical destruction of the only copy of a document.
:::

%%%
---
unit: Symmetric
code: SYM
title: "Symmetric Cryptography: Block vs. Stream Ciphers"
---
:::callout style=soft
**Symmetric Encryption** uses the same shared key for both encryption and decryption. Symmetric algorithms are highly efficient and are categorized into **block ciphers** and **stream ciphers**.
:::

::::columns ratio=1:1
::col::
::::card heading="Block Ciphers"
:::list style=tight
- **Mechanism**: Splits plaintext into fixed-size blocks (e.g., 128 bits) and encrypts each block.
- **Algorithms**: **AES** (FIPS 197), **3DES** (SP 800-67).
- **Modes of Operation**: Requires a mode to process multiple blocks securely:
  - *CBC (Cipher Block Chaining)*: Chains blocks; requires an Initialization Vector (IV).
  - *GCM (Galois/Counter Mode)*: Provides authenticated encryption (AEAD), ensuring integrity and confidentiality.
:::
::::
::col::
::::card heading="Stream Ciphers"
:::list style=tight
- **Mechanism**: Generates a continuous pseudorandom keystream and combines it with plaintext bit-by-bit (typically using XOR).
- **Algorithms**: **ChaCha20** (RFC 8439), **RC4** (deprecated due to bias).
- **Properties**: Extremely fast; ideal for real-time streaming media and low-power devices.
- **Critical Rule**: Never reuse a keystream (using the same key and nonce pair) or the cipher can be trivially broken.
:::
::::
::::

:::steps
1. **Split**: Divide plaintext into fixed 128-bit blocks; apply PKCS#7 padding to the final block if it is shorter than 128 bits.
2. **IV Generation**: Generate a cryptographically random 128-bit Initialization Vector (IV) using a CSPRNG (NIST SP 800-90A); the IV must be unique per encryption operation and per key.
3. **First Block XOR**: XOR the first plaintext block with the IV to produce a modified input block before AES encryption begins (CBC mode chaining).
4. **Block Encryption**: Pass the modified block through the AES key schedule with shared key $K$ — 10, 12, or 14 rounds for AES-128/192/256 respectively, to produce ciphertext block $C_1$.
5. **Chain**: XOR each subsequent plaintext block with the previous ciphertext block before encryption, creating the dependency chain that prevents identical plaintext blocks from producing identical ciphertext.
6. **Transmit**: Send the IV (unencrypted but uniquely generated per session) alongside all ciphertext blocks; the recipient uses the IV and shared key to reverse the chain during decryption.
:::

:::image src="images/25_block_vs_stream_cipher.png" alt="Two-panel comparison diagram: left panel labeled Block Cipher (AES-CBC) shows a row of 128-bit plaintext blocks each passed through an AES encryption box with key K, chained together with XOR gates and an IV at the start, producing ciphertext blocks; right panel labeled Stream Cipher (ChaCha20) shows a keystream ribbon XORed bit-by-bit with a plaintext stream to produce ciphertext; a red warning icon on the right panel notes 'Never reuse key+nonce, two-time pad attack'; both panels show the shared key K at the top" caption="Block ciphers (AES-CBC) process fixed-size chunks chained with an IV; stream ciphers (ChaCha20) XOR a continuous keystream against plaintext. Both produce ciphertext indistinguishable from random noise when properly implemented." width=full
:::

:::notes
Symmetric cryptography is the primary mechanism for bulk data encryption. It is characterized by the use of a single secret key that must be shared and kept confidential by both communicating parties. Because symmetric algorithms utilize fast mathematical operations, substitutions, permutations, and bitwise XORs organized into substitution-permutation networks, they run between 100 and 1,000 times faster than asymmetric operations, making them practical for encrypting large datasets and high-throughput network traffic.

Block ciphers break plaintext down into fixed-size blocks, typically 128 bits for AES. The Advanced Encryption Standard was selected by NIST through a public international competition finalized in 2001 and published as FIPS 197. AES supports key lengths of 128, 192, or 256 bits; NIST SP 800-131A requires AES-128 as the minimum and recommends AES-256 for data requiring long-term protection or classified up to SECRET under the NSA's CNSA 2.0 suite.

Because files and data streams are larger than a single 128-bit block, block ciphers require a "mode of operation" defined in NIST SP 800-38 series. Early Electronic Codebook (ECB) mode is critically insecure, identical plaintext blocks produce identical ciphertext blocks, leaking structural patterns. The canonical illustration of this failure is the "ECB penguin": encrypting a bitmap image using ECB mode produces ciphertext in which the penguin's outline remains clearly visible because pixel patterns in identical color regions produce identical ciphertext blocks. Modern deployments mandate Cipher Block Chaining (CBC) with a random, per-session IV (NIST SP 800-38A), or Galois/Counter Mode (GCM). GCM, specified in NIST SP 800-38D, provides Authenticated Encryption with Associated Data (AEAD), delivering both confidentiality and integrity verification in a single cryptographic pass, which is why it is required in TLS 1.3 cipher suites such as TLS_AES_256_GCM_SHA384.

Stream ciphers operate by generating a continuous pseudorandom keystream. ChaCha20, specified in RFC 8439 and designed by Daniel J. Bernstein, is a modern high-performance stream cipher that serves as the primary alternative to AES-GCM in TLS 1.3 for environments lacking hardware AES acceleration. The golden rule of stream ciphers is that a keystream must never be reused with the same key and nonce. When two different plaintexts are encrypted with an identical keystream, the "two-time pad", an attacker can XOR the two ciphertexts together to cancel the keystream, directly exposing the XOR of the two plaintexts. RC4, a formerly ubiquitous stream cipher, was formally deprecated after bias in its initial keystream bytes enabled practical attacks including POODLE (CVE-2014-3566) and the RC4 NOMORE attack (CVE-2015-2808), leading all major browsers to remove RC4 support by 2015 and TLS 1.3 to ban it entirely.
:::

%%%
---
unit: Keys
code: KEY
title: Cryptographic Keys and Information Entropy
---
:::callout style=soft
The strength of a cryptographic system depends on the length and randomness of its keys. Security strength is measured in **bits of entropy**, representing the size of the keyspace that an attacker must search via brute force.
:::

:::steps
1. **Entropy Generation**: Keys must be generated using a **Cryptographically Secure Pseudo-Random Number Generator (CSPRNG)** (NIST SP 800-90A) to ensure unpredictability.
2. **Keyspace Size**: A key size of $n$ bits yields a keyspace of $2^n$ possibilities. AES-256 has a keyspace of $2^{256}$ (approx. $1.1 \times 10^{77}$).
3. **Brute-Force Resistance**: A keyspace of $2^{128}$ is considered mathematically secure against brute-force attacks, as the energy required to compute it exceeds physical limits.
4. **Key Management**: Keys must be stored securely (in Hardware Security Modules - HSMs), rotated regularly, and destroyed per standards like **NIST SP 800-57**.
:::

:::image src="images/25_key_entropy_keyspace.png" alt="Infographic with three sections on a white background: left section shows a strength scale from 'Weak (40-bit DES, breakable in hours)' through '128-bit (AES minimum)' to 'Strong (256-bit AES, computationally infeasible)' as colored blocks; center section shows a lock icon with the formula 2^256 keyspace and a comparison note that 2^256 exceeds the estimated number of atoms in the observable universe (10^80); right section shows a horizontal key lifecycle flow: Generate via CSPRNG (SP 800-90A) → Store in HSM (FIPS 140-3) → Rotate per schedule (SP 800-57) → Destroy and verify erasure; a red X crosses out a code snippet using random() labeled 'NOT cryptographically secure'" caption="Cryptographic key strength depends on entropy: a 256-bit AES key produces a keyspace of 2²⁵⁶ possibilities. Key lifecycle management, from CSPRNG generation through verifiable destruction, is as critical as key length in maintaining security." width=full
:::

:::notes
In cryptography, the key is the absolute boundary of security. A common misconception is that security can be improved by using a secret, proprietary algorithm. In practice, proprietary algorithms have not received the decades of public cryptanalytic scrutiny that reveals weaknesses, and they are easily reverse-engineered once exposed. Instead, we rely on public, audited algorithms standardized by NIST and ISO, where security is concentrated entirely within the key, in accordance with Kerckhoffs's principle. This is why NIST publishes its cryptographic standards openly and invites international cryptanalysis.

The strength of a key is determined by its entropy, a measure of randomness and unpredictability quantified in bits. To generate secure keys, we must use a Cryptographically Secure Pseudo-Random Number Generator (CSPRNG), as specified in NIST SP 800-90A. Standard random number generators in programming languages, such as Python's random module or Java's Math.random(), are deterministic, seeded from predictable values, and can be predicted after observing a small number of outputs. Using them for key generation is a critical implementation vulnerability.

A landmark real-world example illustrates the catastrophic consequences of CSPRNG failures. CVE-2008-0166 documented a devastating bug introduced in 2006 into the Debian Linux OpenSSL package that inadvertently reduced the entropy used for RSA and DSA key generation from 2048 bits of randomness to approximately 15 bits, producing fewer than 32,768 unique key pairs for any given key length on affected systems. Attackers precomputed all possible keys and could instantly compromise any SSH host key, TLS certificate, or OpenVPN key generated on a Debian or Ubuntu system between 2006 and 2008. This single CSPRNG implementation error in a widely deployed library rendered strong cryptographic key lengths meaningless for millions of systems.

The size of the key determines the difficulty of a brute-force attack. A key length of $n$ bits means an attacker must search a keyspace of $2^n$ possible keys. NIST SP 800-57 establishes minimum security strengths for different protection periods: 112 bits is the minimum for near-term protection through 2030, 128 bits is the standard minimum for new symmetric systems, and 256 bits is recommended for long-term data protection and post-quantum safety margins. AES-256's keyspace of approximately $1.1 \times 10^{77}$ exceeds the estimated number of atoms in the observable universe (~$10^{80}$). Even a theoretical computer performing one trillion operations per second testing every key would require approximately $3.3 \times 10^{56}$ years to exhaust the AES-256 keyspace.

Because keys are the primary targets for attackers, far more frequently compromised through theft, misconfiguration, or insider threat than through brute force, managing their full lifecycle under NIST SP 800-57 is the most critical aspect of cryptographic engineering. Hardware Security Modules (HSMs) certified to FIPS 140-3 Level 2 or 3 provide tamper-resistant physical environments where key material is generated and used without ever being exposed to the general-purpose operating system. Key rotation limits the data volume encrypted under any single key, reducing blast radius if compromise occurs. Secure key destruction, overwriting storage with verified erasure per NIST SP 800-88, ensures that retired key material cannot be recovered from decommissioned storage media.
:::

%%%
---
unit: Hashing
code: HSH
title: Cryptographic Hash Functions
---
:::callout style=soft
A **cryptographic hash function** maps data of arbitrary size to a fixed-size bit string (the digest) in a deterministic, one-way manner. Hash functions must satisfy three primary security properties.
:::

::::columns ratio=1:1
::col::
::::card heading="Core Hash Properties"
:::list style=tight
- **Pre-image Resistance (One-Way)**: Given a digest $H$, it is computationally infeasible to find any input $x$ such that $hash(x) = H$.
- **Second Pre-image Resistance**: Given an input $x$, it is infeasible to find a different input $y$ such that $hash(y) = hash(x)$.
- **Collision Resistance**: It is infeasible to find any two distinct inputs $x$ and $y$ that yield the same digest ($hash(x) = hash(y)$).
:::
::::
::col::
:::code language=python caption="The Avalanche Effect in SHA-256"
import hashlib
# A single character change ('!' vs '?') 
# results in a completely different digest:
print(hashlib.sha256(b"Hello!").hexdigest())
# Output: 334d016f755cd6dc58c53a86e183...
print(hashlib.sha256(b"Hello?").hexdigest())
# Output: f831d17d12f3db7e0ebf9a12c8b0...
:::
::::

:::image src="images/25_hash_function_avalanche.png" alt="Diagram showing two input strings 'Hello!' and 'Hello?' entering separate SHA-256 hash function boxes; two completely different 256-bit hex strings emerge with no visual similarity; a comparison panel below highlights that one character changed (! vs ?) but approximately 128 of 256 output bits differ; a label reads 'Avalanche Effect, any input change causes ~50% of output bits to flip'; a secondary row shows four algorithms: MD5 (broken, 128-bit, red X), SHA-1 (broken, 160-bit, red X), SHA-256 (secure, FIPS 180-4, green check), SHA-3 (secure, FIPS 202, green check)" caption="The avalanche effect in SHA-256: a one-character input change produces a completely different 256-bit digest, ensuring attackers cannot infer plaintext structure by observing hash output patterns." width=full
:::

:::notes
While encryption is a two-way process designed to hide data, hashing is a one-way process designed to verify data. A cryptographic hash function takes an input of any length and compresses it into a fixed-length string of bits, known as a digest or hash value. Hashing is deterministic: the same input will always produce the exact same digest. This determinism, combined with the one-way property, makes hash functions ideal for integrity verification, digital signatures, and password storage. The SHA-2 family (SHA-224, SHA-256, SHA-384, SHA-512) is standardized in FIPS 180-4; the SHA-3 family (SHA3-256, SHA3-512) is standardized in FIPS 202.

To be secure, a hash function must meet three mathematical criteria. First, pre-image resistance: given only the digest $H$, it must be computationally infeasible to find any input $x$ such that $hash(x) = H$. This property prevents password database theft from directly exposing original passwords. Second, second pre-image resistance: given an input $x$ and its hash, it must be infeasible to find a different input $y$ that hashes to the same value. This prevents an attacker from substituting a malicious file that matches the hash of a legitimate one. Third, collision resistance: it must be infeasible to find any two distinct inputs that produce the same digest. The birthday paradox means collisions are statistically easier to find than pre-images, which is why collision resistance is the most stringent of the three properties and why output length matters.

Another critical property is the avalanche effect. Changing a single bit in the input must cause approximately half of all output bits to flip, unpredictably. This ensures that an attacker cannot make educated guesses or detect patterns in plaintext by observing the output. The Python example demonstrates this: changing only the final punctuation character in "Hello" produces two completely different 256-bit digests with no visible relationship.

The history of broken hash functions illustrates why algorithm selection is a security-critical decision. MD5, once widely used, was proven vulnerable to collision attacks in 2004 (Wang et al.; see also CVE-2004-2761 for specific implementations). In 2008, this technique was used to forge a legitimate Certificate Authority certificate, attackers produced two requests with the same MD5 hash, one for a legitimate domain and one for a rogue CA, allowing them to issue fraudulent certificates for any domain. SHA-1 was deprecated by NIST in 2011 after theoretical weaknesses were found, and in 2017 Google and CWI Amsterdam demonstrated the first practical SHA-1 collision ("SHAttered" attack), producing two PDF files with identical SHA-1 digests but different visual content. NIST now mandates SHA-256 or SHA-384 minimum for all new applications. For software integrity verification, Linux distribution ISO files, firmware updates, software packages, and code-signing, SHA-256 or SHA-3 digests published out-of-band by vendors allow recipients to confirm that downloads have not been tampered with, a control directly preventing supply-chain attacks of the SolarWinds type.
:::

%%%
---
unit: Hashing
code: CMP
title: "Hashing vs. Encryption: Password Storage"
---
:::callout style=soft
A common security failure is misapplying cryptographic primitives. Encryption and hashing serve distinct objectives and must not be confused, particularly in **password storage**.
:::

::::columns ratio=1:1
::col::
:::table
| Feature | Encryption (e.g., AES) | Hashing (e.g., SHA-256) |
|---|---|---|
| **Reversibility** | Reversible (requires key) | Irreversible (One-way) |
| **Objective** | Confidentiality | Integrity / Verification |
| **Output** | Variable size (matches input) | Fixed size (e.g., 256 bits) |
| **Keys** | Requires key management | Keyless primitive |
:::
::col::
::::card heading="Secure Password Storage Framework"
:::list style=tight
- **Never Encrypt Passwords**: If the encryption key is compromised, all user passwords can be decrypted.
- **Salt the Hash**: Append a unique, random string (the **salt**) to each password before hashing, rendering pre-computed dictionary attacks (rainbow tables) useless.
- **Key Stretching**: Use slow, iterative hash functions like **Argon2** (RFC 9106) or **bcrypt** to slow down brute-force attacks.
:::
::::
::::

:::steps
1. **Registration**: User submits password $P$; server generates a unique, cryptographically random salt $S$ of at least 16 bytes using a CSPRNG (NIST SP 800-63B §5.1.1.2).
2. **Salted Input**: Concatenate salt and password to form the combined input $S \| P$ before any hashing occurs.
3. **Key Stretching**: Apply Argon2id (RFC 9106) with memory ≥ 19 MiB and iteration count ≥ 2, or bcrypt with cost factor ≥ 10, to compute digest $H = \text{KDF}(S \| P)$.
4. **Storage**: Store only the tuple $(S, H)$ in the credential database, never the plaintext password, an encrypted password, or an unsalted hash.
5. **Login Verification**: Retrieve stored $(S, H)$ for the claimed username; recompute $H' = \text{KDF}(S \| P_{\text{input}})$ using the stored salt and the login submission.
6. **Access Decision**: Grant access if $H' = H$ using a constant-time comparison function; deny and log the failed attempt otherwise. The plaintext password is never persisted to storage at any point.
:::

:::image src="images/25_password_hashing_workflow.png" alt="Two-column process diagram: left column labeled Registration shows a password entry field, a salt generator labeled CSPRNG producing a random 16-byte salt, an Argon2id function box receiving both password and salt and labelled with memory and iteration parameters, and a database icon storing only the salt and hash; right column labeled Login Verification shows the same password entry, the stored salt retrieved from database, Argon2id recomputed with the same salt, and a constant-time comparison box with green checkmark for match or red X for mismatch; a crossed-out storage icon on the side reads 'Never store plaintext or encrypted passwords'" caption="Secure password storage workflow: a per-user random salt combined with a memory-hard key-derivation function (Argon2id or bcrypt) renders rainbow tables and GPU-accelerated brute-force attacks computationally impractical." width=full
:::

:::notes
Encryption and hashing are often confused because they both transform plaintext into unreadable data. However, their security objectives are completely different. Encryption is designed to maintain confidentiality and is reversible, it requires a key to decrypt the ciphertext back into plaintext. Hashing is designed to ensure integrity and is irreversible, there is no key that can "de-hash" a digest. Applying the wrong primitive to a use case creates a critical vulnerability.

This distinction is most consequential in password storage systems. A naive developer might encrypt passwords using AES, planning to decrypt them during login verification. However, if an attacker compromises the server and extracts the encryption key, through SQL injection, server misconfiguration, or insider access, they can instantly decrypt every password in the database. This attack is straightforward and requires no cryptographic sophistication once the key is obtained.

The correct approach is to hash passwords. When a user registers, we hash their password and store only the digest. During login, we hash the submitted password and compare it to the stored digest. However, simply applying SHA-256 without additional protection is still dangerously insufficient. Attackers precompute "rainbow tables", databases mapping millions of common passwords to their SHA-256 or MD5 hashes, and can crack an unsalted hash in seconds. The 2012 LinkedIn breach exposed 117 million user password hashes using unsalted SHA-1; within days of public release, crackers had recovered the majority of passwords using precomputed dictionaries. The 2009 RockYou breach exposed 32 million credentials stored in plaintext with no protection at all, directly producing the RockYou2021 wordlist that remains a staple of penetration testing to this day.

To build a secure password storage system, we must add a per-user random salt and use a memory-hard or computation-intensive key-derivation function (KDF). NIST SP 800-63B Section 5.1.1.2 specifies that memorized secrets shall be salted and hashed using a suitable one-way KDF. Argon2id, the winner of the 2015 Password Hashing Competition and standardized in RFC 9106, is the current OWASP and NIST preferred recommendation. It is memory-hard: requiring large amounts of RAM per hash computation dramatically limits the number of hashes an attacker can compute per second on GPUs and ASICs, because memory bandwidth becomes the bottleneck rather than compute throughput. bcrypt (minimum cost factor 10, increasing as hardware improves) remains acceptable for legacy systems. PBKDF2-SHA256 (NIST SP 800-132) with at least 600,000 iterations is approved for FIPS-compliant environments. The salt must be generated fresh for each user registration using a CSPRNG, sharing salts or using predictable salts like usernames defeats the purpose. Constant-time comparison during verification prevents timing side-channel attacks that could leak information about the hash comparison result.
:::

%%%
---
unit: CIA
code: TIE
title: Mapping Cryptography to the CIA Triad
---
:::callout style=soft
Cryptography is the technical implementation of the **CIA Triad** (Confidentiality, Integrity, Availability), mapping specific primitives to core security requirements.
:::

::::columns ratio=1:1
::col::
::::card heading="Confidentiality and Integrity"
:::list style=tight
- **Confidentiality**: Enforced by symmetric and asymmetric encryption.
  - *Data at Rest*: AES-256 (FIPS 197).
  - *Data in Transit*: TLS 1.3 (RFC 8446).
- **Integrity**: Enforced by cryptographic hash functions (SHA-256, SHA-3).
  - *Verification*: Checking downloaded file hashes against published digests.
:::
::::
::col::
::::card heading="Authenticity and Non-Repudiation"
:::list style=tight
- **Authenticity**: Enforced by Message Authentication Codes (MACs) and Digital Signatures.
  - *HMAC*: Combines a hash function with a shared key to authenticate messages.
- **Non-Repudiation**: Enforced by Asymmetric Digital Signatures (RSA/ECDSA).
  - *Mechanism*: Senders sign messages with their private key; recipients verify with the public key.
:::
::::
::::

:::image src="images/25_cia_cryptography_mapping.png" alt="Triangle diagram of the CIA Triad with three labeled corners: Confidentiality (top), Integrity (bottom-left), Authenticity and Non-Repudiation (bottom-right); from the Confidentiality corner, two arrows point to labeled boxes: AES-256 FIPS 197 (data at rest) and TLS 1.3 RFC 8446 (data in transit); from the Integrity corner, arrows point to SHA-256 FIPS 180-4 and SHA-3 FIPS 202 boxes; from the Authenticity corner, arrows point to HMAC-SHA256 RFC 2104 and ECDSA FIPS 186-5 boxes; a fourth arrow from the center points down to PKI and Certificate Authorities, labeled as the binding infrastructure for all three properties" caption="Cryptographic primitive mapping to the CIA Triad: each security objective requires a distinct mathematical tool. Confidentiality, integrity, and authenticity are enforced by encryption, hashing, and digital signatures respectively." width=full
:::

:::notes
To wrap up our technical look at cryptographic primitives, let's map them directly to the CIA Triad. This shows how abstract mathematical concepts translate into concrete security controls within enterprise architectures, as codified in ISO/IEC 27001:2022 (Information Security Management Systems) Annex A controls and NIST SP 800-53 Revision 5's SC (System and Communications Protection) control family.

Confidentiality ensures that data is only accessible to authorized users, enforced by encryption. For data at rest, this means AES-256 (FIPS 197) applied to database fields, disk volumes, and file archives. Regulatory frameworks mandating encryption at rest include HIPAA Security Rule (45 CFR §164.312(a)(2)(iv)), PCI DSS Requirement 3.5 for cardholder data, and GDPR Article 32 for personal data. For data in transit, TLS 1.3 (RFC 8446) encrypts the channel between client and server using an ECDHE key exchange and AES-256-GCM or ChaCha20-Poly1305 bulk encryption. The 2013 Target breach, in which attackers moved 40 million payment card records across Target's internal network, demonstrated the consequences of absent in-transit encryption on internal network segments, even when perimeter controls were in place.

Integrity ensures that data has not been altered. Cryptographic hash functions enforce integrity through digest comparison. When a software vendor publishes a SHA-256 hash alongside a download, any corruption or tampering during download will produce a mismatching local hash. HMAC (Hash-based Message Authentication Code, RFC 2104) extends integrity to authenticated contexts: by combining a shared secret key with a hash function using the construction $\text{HMAC}(K, m) = H((K \oplus \text{opad}) \| H((K \oplus \text{ipad}) \| m))$, HMAC proves both that a message was not modified and that it originated from a party possessing the shared key. HMAC-SHA256 is used in AWS Signature Version 4 for API authentication headers, JWT token verification, and TLS record-layer integrity in TLS 1.2.

Authenticity and non-repudiation require asymmetric digital signatures, which we will study in depth in the next lecture. ECDSA (FIPS 186-5) and RSA signatures bind a message to a specific private-key holder, providing proof of origin. Non-repudiation carries legal significance under the EU eIDAS Regulation (Qualified Electronic Signatures) and the U.S. ESIGN Act, enabling electronically signed contracts, code-signing certificates that tie software releases to identified publishers, and audit trails where individual administrators' actions are signed and attributed. A single unifying insight from this lecture: no single cryptographic primitive satisfies all three CIA objectives. Encryption provides confidentiality but not integrity on its own. Hashing provides integrity but not confidentiality. Combining them, as TLS 1.3 does with AEAD ciphers providing both, achieves comprehensive data protection.
:::

%%%
---
unit: History
code: HIS
title: "From Caesar to Enigma: A History of Cryptographic Evolution"
---
:::callout style=soft
Understanding the failures of classical ciphers illustrates **why** modern cryptographic properties, large keyspaces, non-linearity, and diffusion, are necessary. Every broken cipher teaches a mathematical lesson still relevant today.
:::

:::table
| Era | Cipher | Attack Method | Fatal Weakness |
|---|---|---|---|
| 50 BCE | Caesar Cipher | Frequency Analysis | 26-key keyspace; no diffusion |
| 1467 CE | Vigenère Cipher | Kasiski Examination | Key repetition exposes periodicity |
| 1918 | ADFGVX (WWI German) | Known-plaintext | Short key + structural bias |
| 1939–1945 | Enigma (WWII German) | Bombe machine + cribs | Deterministic rotor structure; no P→P mapping |
| 1977 | DES (56-bit key) | Brute-force (EFF DES Cracker) | 56-bit keyspace exhausted in <24 hours by 1998 |
| 2001 | AES (FIPS 197) | None (currently) | No practical attack on full-round AES known |
:::

:::image src="images/25_cipher_history_timeline.png" alt="Horizontal timeline from 50 BCE to 2001 CE showing five cipher milestones: Caesar Cipher (50 BCE) with a shift wheel; Vigenère Cipher (1467) with a polyalphabetic square; Enigma Machine (1939) with a rotor diagram; DES (1977) with a 56-bit key icon and a red skull showing 'cracked 1998'; AES (2001) with a NIST seal and green checkmark; each milestone has a small icon indicating how it was broken; arrows from each broken cipher point right to the next stronger cipher, symbolizing how each failure drove the next advance" caption="The evolution of cryptography from Caesar's simple shift cipher to AES illustrates a 2,000-year arms race between cipher designers and cryptanalysts. Each broken cipher revealed a mathematical property that modern algorithms must satisfy." width=full
:::

:::notes
Modern cryptographic algorithms make more sense once you see the historical failures that motivated them. Each broken cipher was not simply a failure of effort, it was a failure to satisfy a specific mathematical security property that we now take for granted in modern designs.

The Caesar Cipher, used by Julius Caesar circa 50 BCE, substitutes each letter with a letter a fixed number of positions down the alphabet. Its entire keyspace consists of only 25 possible shifts (excluding the identity shift). An attacker can simply try all 25 possibilities in seconds, this is a brute-force attack against a trivially small keyspace. Writing out all 25 shifts of a Caesar-ciphered message makes the point that a 25-key keyspace is trivially exhaustible by hand, which is why keyspace size is the first measure of a cipher's strength.

The Vigenère Cipher improved on Caesar by using a repeating keyword to apply different shifts to different positions in the message, creating what appears to be a polyalphabetic substitution. For two centuries it was known as "le chiffre indéchiffrable." However, in 1863 Friedrich Kasiski published an attack exploiting the periodicity of the repeating key. By finding repeated ciphertext sequences and measuring the distances between them, an attacker can determine the key length. Once the key length is known, the cipher reduces to a series of independent Caesar ciphers solvable by frequency analysis of each position. This attack illustrated that key repetition is a structural weakness: cryptographic keys must be used in ways that do not expose their periodicity or length.

The German Enigma machine, used extensively in World War II, was a rotor-based electromechanical cipher considered unbreakable by its designers. However, several structural properties enabled the Allied codebreakers at Bletchley Park, including Alan Turing and Gordon Welchman, to break Enigma traffic systematically. First, Enigma's reflector ensured that no letter could encrypt to itself. This seemingly minor property allowed cryptanalysts to eliminate large portions of the keyspace by checking if a known "crib" (a suspected plaintext word) could be placed at a given position, if any letter of the crib matched its ciphertext letter, that position was invalid. Second, German operators frequently sent predictable messages ("WETTER" for weather reports, repeated message keys at the start of each transmission) providing known-plaintext material. The Bombe machine automated the search, reducing millions of possible Enigma settings to a manageable set of daily key candidates, ultimately playing a decisive role in the Allied victory. The Enigma case demonstrates that structural regularities in a cipher, even subtle ones like the no-self-encryption property, create exploitable weaknesses.

DES, the Data Encryption Standard with a 56-bit key, was withdrawn from use after the EFF (Electronic Frontier Foundation) built the DES Cracker machine in 1998 (costing approximately $250,000) and cracked a DES-encrypted message in under 24 hours, winning the RSA Labs DES Challenge II. By 2002, distributed computing projects cracked DES keys in under a week with commodity hardware. The 56-bit keyspace of $2^{56}$ (approximately 72 quadrillion keys) was no longer sufficient against advances in computing hardware. NIST deprecated single DES in 2005 (SP 800-131A) and withdrew Triple-DES (3DES) approval for new systems in 2023, mandating migration to AES. The DES story shows that key length requirements must continuously be re-evaluated against advances in computing power, a lesson that now motivates the transition to post-quantum cryptographic algorithms.
:::

%%%
---
unit: Symmetric
code: AES
title: "AES Deep Dive: The Substitution-Permutation Network"
---
:::callout style=soft
AES (Advanced Encryption Standard, FIPS 197) operates on 128-bit blocks through a **Substitution-Permutation Network (SPN)** of repeated rounds. Each round applies four transformations that together achieve **confusion** and **diffusion**.
:::

::::columns ratio=1:1
::col::
::::card heading="Four AES Round Operations"
:::list style=tight
- **SubBytes**: Each byte is replaced by its value in a fixed 16×16 S-Box derived from the multiplicative inverse in GF(2⁸), providing non-linearity (confusion).
- **ShiftRows**: Each row of the 4×4 state matrix is cyclically shifted left by 0, 1, 2, or 3 positions, providing inter-column diffusion.
- **MixColumns**: Each 4-byte column is multiplied by a fixed polynomial in GF(2⁸), spreading influence of each byte across the entire column (diffusion).
- **AddRoundKey**: The round key (derived from the master key via the AES key schedule) is XORed with the state, injecting key material.
:::
::::
::col::
:::table
| Key Size | Rounds | Security Strength | NIST Recommendation |
|---|---|---|---|
| AES-128 | 10 | 128 bits | Current minimum (SP 800-131A) |
| AES-192 | 12 | 192 bits | General use |
| AES-256 | 14 | 256 bits | Long-term / post-quantum margin |
:::
::::
::::

:::image src="images/25_aes_spn_round_structure.png" alt="Vertical flow diagram of one AES encryption round: a 4x4 grid of bytes labeled 'State' at the top passes through four sequential transformation boxes: (1) SubBytes, each byte maps through an S-Box lookup table shown as a 16x16 grid; (2) ShiftRows, row 0 unchanged, row 1 shifted left 1, row 2 shifted left 2, row 3 shifted left 3, visualized as sliding rows; (3) MixColumns, a matrix multiplication symbol in GF(2^8) over the four columns; (4) AddRoundKey, XOR symbol combining the state with the round key derived from the key schedule; the output 4x4 grid feeds into the next round; a round counter shows 'Round 1 of 14 (AES-256)'" caption="One AES-256 round: SubBytes provides non-linear confusion; ShiftRows and MixColumns provide inter-byte diffusion; AddRoundKey injects key material. After 14 rounds, every output bit depends on every input bit and every key bit." width=full
:::

:::notes
The Advanced Encryption Standard is the world's most widely deployed symmetric cipher, standardized by NIST in FIPS 197 following a public international competition that ran from 1997 to 2001, in which the Rijndael algorithm by Joan Daemen and Vincent Rijmen was selected from fifteen candidates after extensive public cryptanalysis. It is implemented in hardware acceleration instructions on virtually all modern CPUs (AES-NI on x86, and dedicated AES instructions on ARM Cortex-A and Apple Silicon), enabling encryption throughput of tens of gigabytes per second on commodity processors.

AES operates on a 4×4 matrix of bytes called the "state," representing the 128-bit block of data being encrypted. The encryption process consists of an initial round key addition, followed by 10, 12, or 14 repeated rounds depending on the key size (AES-128, AES-192, or AES-256 respectively), and a final round that omits the MixColumns step.

The four round operations achieve Claude Shannon's two fundamental goals for a secure cipher, confusion and diffusion, as described in his 1949 paper "Communication Theory of Secrecy Systems." Confusion obscures the relationship between the key and the ciphertext; diffusion spreads the influence of individual plaintext bits and key bits across the entire ciphertext output. SubBytes provides confusion: each byte is replaced using a bijective S-Box (substitution box) derived from computing multiplicative inverses in the finite field GF(2⁸) followed by an affine transformation. This substitution is highly non-linear, meaning it cannot be expressed as a simple linear function of the input, linear relationships are exactly what linear and differential cryptanalysis attacks exploit. ShiftRows provides inter-column diffusion by cyclically rotating the rows of the state matrix. MixColumns provides the strongest diffusion, multiplying each column by a fixed matrix in GF(2⁸), ensuring that after two rounds every output byte depends on every input byte, the "branch number" of MixColumns guarantees that any difference introduced in an input byte will spread to all four bytes of the output column.

The best known attacks against full-round AES are biclique attacks that provide only a marginal reduction in the brute-force effort required, for AES-128, the biclique attack reduces the search space from $2^{128}$ to approximately $2^{126.1}$, which is completely impractical. AES has no known practical attacks on its full round count. Related-key attacks exist against reduced-round variants under specific key schedule conditions, but these are not exploitable in correctly deployed systems. The AES key schedule, which derives round keys from the master key, is a side-channel target: timing variations in its execution on older CPUs without constant-time implementations enabled cache-timing attacks (CacheBleed, CVE-2016-0702). Hardware AES-NI instructions execute in constant time and remove this class of leak.
:::

%%%
---
unit: Symmetric
code: MOD
title: "AES Modes of Operation: ECB, CBC, CTR, and GCM Compared"
---
:::callout style=soft
A **mode of operation** defines how a block cipher processes multiple blocks of data. Mode selection is as security-critical as algorithm selection, ECB mode leaks structural information even with a perfect block cipher.
:::

:::table
| Mode | Parallelizable? | Provides Integrity? | IV Required? | NIST Standard | Recommended? |
|---|---|---|---|---|---|
| ECB (Electronic Codebook) | Yes | No | No | SP 800-38A | NEVER, insecure |
| CBC (Cipher Block Chaining) | Decrypt only | No | Yes (random) | SP 800-38A | Legacy systems only |
| CTR (Counter) | Yes | No | Yes (nonce) | SP 800-38A | Use with HMAC |
| GCM (Galois/Counter) | Yes | Yes (AEAD) | Yes (nonce, 96-bit) | SP 800-38D | **Preferred** |
| CCM | Limited | Yes (AEAD) | Yes | SP 800-38C | IoT/constrained devices |
:::

::::columns ratio=1:1
::col::
::::card heading="Why ECB is Broken, The ECB Penguin"
:::callout style=soft
Encrypting a bitmap image with AES in ECB mode produces a ciphertext in which the penguin's outline remains **clearly visible**, because identical 128-bit plaintext blocks (identical pixel regions) produce identical ciphertext blocks, leaking the structural patterns of the data. ECB must never be used.
:::
::::
::col::
::::card heading="GCM: AEAD in One Pass"
:::list style=tight
- GCM combines AES-CTR for encryption with a GHASH authenticator for integrity.
- Provides both **confidentiality** and **integrity** in a single cryptographic operation.
- Mandated in TLS 1.3 cipher suites: `TLS_AES_256_GCM_SHA384` and `TLS_AES_128_GCM_SHA256`.
- Nonce must be **unique per key**, nonce reuse under GCM is catastrophically insecure (recovers authentication key).
:::
::::
::::

:::image src="images/25_aes_modes_ecb_vs_gcm.png" alt="Three-panel comparison: left panel labeled ECB Mode shows a photograph of a penguin encrypted with AES-ECB where the penguin's silhouette is clearly visible in the ciphertext output, demonstrating structural leakage; center panel labeled CBC Mode shows chained blocks with an IV and arrows illustrating that each block's ciphertext depends on all previous blocks, with a note that decryption is parallelizable but encryption is sequential; right panel labeled GCM Mode shows two parallel paths, an AES-CTR encryption path and a GHASH authentication path, merging into an output labeled Ciphertext + Auth Tag (128 bits), with a note 'Single-pass AEAD, SP 800-38D'" caption="ECB mode leaks structural data patterns, as demonstrated by the ECB penguin. GCM (Galois/Counter Mode) provides authenticated encryption with associated data (AEAD) in a single cryptographic pass and is the required mode for TLS 1.3." width=full
:::

:::notes
The distinction between a block cipher and a mode of operation is fundamental to understanding secure implementation. AES itself is a permutation, it takes a 128-bit input and a key, and produces a 128-bit output. By itself, AES can only encrypt exactly one 128-bit block. A mode of operation defines the algorithm used to apply the block cipher iteratively to messages of arbitrary length, and it determines critically important security properties of the resulting encryption scheme.

Electronic Codebook (ECB) mode is the naive approach: simply apply AES independently to each 128-bit block. It is standardized only for completeness and must never be used for encrypting any structured data. The ECB penguin demonstration makes the weakness immediately apparent to anyone: encrypting a TUX Linux mascot bitmap image using AES-ECB produces ciphertext that retains the visual structure of the original image, because regions of uniform color produce identical 16-byte blocks of ciphertext. The pattern leakage from ECB has led to real-world vulnerabilities. CVE-2020-25508 documented an ECB mode vulnerability in a commercial network appliance where encrypted configuration file blocks leaked repeating patterns, enabling partial decryption of sensitive configuration data. NIST SP 800-38A notes explicitly that ECB "does not hide data patterns" and should not be used for confidentiality protection of any data with repeating block-aligned patterns.

Cipher Block Chaining (CBC) mode adds a dependency chain: before encrypting each block, it XORs the plaintext with the previous ciphertext block, or with a random Initialization Vector (IV) for the first block. This eliminates the identical-ciphertext-for-identical-plaintext weakness. However, CBC is vulnerable to padding oracle attacks, CVE-2014-3566 (POODLE) and CVE-2011-3389 (BEAST) both exploited CBC padding validation to decrypt TLS traffic byte-by-byte. CBC also does not provide integrity; an attacker who can flip bits in the ciphertext will flip predictable bits in the decrypted plaintext (bit-flipping attack).

GCM (Galois/Counter Mode), standardized in NIST SP 800-38D, is the current recommended standard for most applications. GCM internally combines AES in Counter mode (which turns AES into a stream cipher by encrypting a counter value and XORing the keystream with plaintext) with a GHASH universal hash function over GF(2¹²⁸) to produce a 128-bit authentication tag. This provides Authenticated Encryption with Associated Data (AEAD) in a single cryptographic pass: confidentiality and integrity are inseparable. GCM is parallelizable for both encryption and decryption, achieving maximum throughput with AES-NI hardware acceleration. The critical operational constraint for GCM is nonce uniqueness: if the same 96-bit nonce is ever reused under the same key, the authentication key (H = AES_K(0)) can be recovered algebraically, completely breaking the integrity guarantee. AWS, Google Cloud, and Azure all document their GCM nonce management practices as part of their envelope encryption key management specifications.

Counter mode (CTR) gives parallelizable encryption but no integrity; combining CTR with HMAC yields authenticated encryption in two passes, while GCM achieves it in one using hardware polynomial multiplication. For constrained IoT environments, CCM mode (SP 800-38C) provides authenticated encryption suited to 802.15.4 and Bluetooth Low Energy.
:::

%%%
---
unit: Symmetric
code: OTP
title: "The One-Time Pad: Perfect Secrecy and Its Limits"
---
:::callout style=soft
The **One-Time Pad (OTP)** is the only cipher proven to be **perfectly secret** (information-theoretically secure). Shannon proved in 1949 that it is unconditionally unbreakable, but its operational requirements make it impractical for most applications.
:::

::::columns ratio=1:1
::col::
::::card heading="Requirements for Perfect Secrecy"
:::list style=tight
- **Key Length = Message Length**: The key must be at least as long as the plaintext.
- **True Randomness**: The key must be generated from a true random source, not a PRNG.
- **Single Use**: The key must be used exactly once, any reuse breaks perfect secrecy.
- **Secure Distribution**: The key must be distributed securely before communication.
:::
::::
::col::
::::card heading="Why Reuse Destroys Secrecy"
:::callout style=soft
If two messages $P_1$ and $P_2$ are encrypted with the same key $K$:

$C_1 \oplus C_2 = (P_1 \oplus K) \oplus (P_2 \oplus K) = P_1 \oplus P_2$

The keys cancel, exposing the XOR of both plaintexts. With linguistic knowledge, both can be recovered, the "two-time pad" attack.
:::
::::
::::

:::image src="images/25_one_time_pad_xor.png" alt="Two-row XOR diagram: top row shows 8-bit plaintext '01001000' (letter H) XORed with a random 8-bit key '11010011' producing ciphertext '10011011'; bottom row shows the reverse, ciphertext '10011011' XORed with the same key '11010011' recovering the plaintext '01001000'; a sidebar shows the two-time pad attack: two ciphertexts C1 and C2 XORed together producing P1 XOR P2, with a red warning label; a small diagram shows historical OTP usage in a Moscow–Washington diplomatic hotline" caption="The One-Time Pad: XOR with a random key produces ciphertext with zero statistical correlation to the plaintext. Key reuse (the two-time pad) immediately exposes the XOR of both plaintexts, destroying all security." width=full
:::

:::notes
The One-Time Pad is the gold standard of theoretical cryptography. Invented in 1917 by Gilbert Vernam and Frank Miller and formalized mathematically by Claude Shannon in his landmark 1949 paper "Communication Theory of Secrecy Systems," the OTP is the only known cipher that is unconditionally, information-theoretically secure. This means it is secure not just against computationally limited adversaries, it is secure even against an adversary with unlimited computing power and time.

The mechanism is simple: generate a key that is as long as the message and consists of truly random bits. XOR each bit of the plaintext with the corresponding bit of the key to produce the ciphertext. Because every possible plaintext of the given length is equally likely as the key ranges over all possible random values, an adversary who captures the ciphertext gains absolutely zero information about the plaintext, every possible decryption is equally probable.

Shannon proved this formally using the concept of perfect secrecy: a cipher is perfectly secret if and only if the probability distribution of the ciphertext is statistically independent of the plaintext, for every key distribution. The OTP is the only practical cipher known to achieve this. Shannon also proved that perfect secrecy is impossible to achieve with a key shorter than the message, which is why stream ciphers (which use a short key to expand a long pseudorandom keystream) provide only computational security, not information-theoretic security.

The two-time pad attack is the most famous practical demonstration of OTP misuse. During the Venona Project, U.S. cryptanalysts discovered that Soviet intelligence had reused OTP keys for thousands of encrypted diplomatic messages in the 1940s. By XORing pairs of ciphertexts known to share a key, analysts recovered the XOR of the underlying plaintexts. Skilled linguists then used crib-dragging, sliding known words or phrases across the XOR plaintext, to recover both messages simultaneously. Approximately 2,900 Soviet intelligence messages were ultimately decoded through this technique, exposing hundreds of Soviet intelligence sources including Julius Rosenberg and dozens of other spies embedded in the Manhattan Project. This case study from CVE-equivalent intelligence failures is one of the most important demonstrations in applied cryptography: perfect ciphers fail perfectly when their operational requirements are violated.

The practical constraints of the OTP, key length equal to message length, true randomness, single use, and secure prior distribution, make it impractical for Internet-scale communications where the parties may have never met and messages are continuous and of unpredictable length. These constraints are precisely what public-key cryptography and key exchange protocols (Diffie-Hellman, ECDH) were invented to overcome, solving the key distribution problem that the OTP cannot. The Moscow-Washington hotline (1963) reportedly used one-time-pad encryption for its most sensitive traffic, with couriers physically carrying key material between capitals, a reminder that for the highest-sensitivity cases the OTP remains the theoretically ideal choice when operational constraints allow.
:::

%%%
---
unit: Asymmetric
code: KDP
title: "The Key Distribution Problem"
---
:::callout style=soft
Symmetric encryption requires a **shared secret key**. But how do two parties who have never communicated before securely establish that secret over a **public, untrusted network**? This is the **Key Distribution Problem**, the central unsolved challenge of classical cryptography.
:::

:::flow
Alice wants to send encrypted data to Bob over the internet
Both need the same symmetric key (e.g., AES-256)
They cannot send the key in plaintext, Eve intercepts it
They cannot meet in person, this doesn't scale to millions of users
Solution: Diffie-Hellman Key Exchange, derive a shared secret without transmitting it
:::

::::columns ratio=1:1
::col::
::::card heading="Classical Solutions (All Inadequate)"
:::list style=tight
- **Physical Courier**: Key material carried in person. Secure but unscalable and slow.
- **Key Distribution Centers (KDC)**: Trusted third party distributes session keys (e.g., Kerberos). Creates a single point of failure.
- **Pre-shared Keys (PSK)**: Manually configured before deployment. Impractical for internet-scale communication between strangers.
:::
::::
::col::
::::card heading="Modern Solution: Public-Key Cryptography"
:::list style=tight
- **1976**: Diffie and Hellman publish "New Directions in Cryptography," introducing the concept of public-key cryptography.
- **Asymmetric Key Pairs**: Each party has a **public key** (shared openly) and a **private key** (kept secret).
- **Key Exchange**: Two parties can compute a shared secret using only public information, without ever transmitting the secret.
:::
::::
::::

:::image src="images/25_key_distribution_problem.png" alt="Network diagram illustrating the key distribution problem: Alice on the left wants to send a shared key to Bob on the right; a wiretap device labeled Eve sits on the network cable in the middle; three failed attempts are shown with red X marks: sending key in plaintext (intercepted), sending encrypted key (circular dependency, needs a key to encrypt a key), meeting in person (shows calendar icon labeled 'Unscalable for billions of users'); below a dividing line labeled '1976 Breakthrough', a Diffie-Hellman exchange diagram shows both parties combining public colors and private colors to arrive at the same shared color without Eve being able to determine the secret mix" caption="The key distribution problem: symmetric encryption requires a shared secret, but transmitting a secret over a public channel is circular. Diffie-Hellman (1976) solved this by enabling two parties to compute a shared secret without ever transmitting it." width=full
:::

:::notes
The key distribution problem is the central challenge that limited cryptography to government, diplomatic, and military contexts for most of human history. Classical symmetric ciphers, Caesar, Vigenère, Enigma, and even DES, all require that the communicating parties share a secret key before any secure communication can take place. But in a world where two strangers need to communicate securely over the internet without any prior contact, how can they establish a shared secret?

Consider the circularity of the problem. If Alice wants to send Bob a symmetric key, she needs to encrypt it to protect it from Eve the eavesdropper. But to encrypt it, she needs a key she has already shared with Bob. If they had already shared a key, they wouldn't need to distribute a new one. The problem is fundamentally circular. Classical solutions all involve either physical contact (exchanging keys in person), trusted third parties (Key Distribution Centers like Kerberos, used in enterprise Windows environments via Active Directory), or manual pre-configuration (pre-shared keys, used in legacy VPNs and IoT devices). All of these are unscalable for the internet.

The magnitude of the scaling problem is striking. The public Internet has billions of users who may want to establish secure connections with websites, email servers, and peers they have never contacted before. At any given moment, millions of new TLS connections are being established between users and servers that have never previously communicated. Each connection requires a fresh symmetric session key. A courier-based or KDC-based key distribution system simply cannot serve this scale.

In 1976, Whitfield Diffie and Martin Hellman published "New Directions in Cryptography," one of the most consequential papers in the history of mathematics and computer science. They proposed a radical idea: it might be possible for two parties to publicly exchange information that allows them to jointly compute a shared secret, without that information revealing the secret to an eavesdropper. This was the concept of public-key cryptography, and it solved the key distribution problem in a mathematically elegant way that scaled to billions of simultaneous users. Diffie and Hellman received the 2015 Turing Award, computing's highest honor, for this work. Ralph Merkle, who independently developed related concepts around the same time, contributed the concept of Merkle Puzzles as an early public-key exchange primitive.

The practical solution, the Diffie-Hellman key exchange protocol based on the Discrete Logarithm Problem, is what enables TLS, SSH, and every modern secure communication protocol to establish fresh session keys between strangers in milliseconds. Understanding this problem and its solution is essential for understanding why public-key cryptography exists and why asymmetric algorithms are used in combination with symmetric ones rather than alone.
:::

%%%
---
unit: Asymmetric
code: DHE
title: "Diffie-Hellman Key Exchange: Worked Example"
---
:::callout style=soft
**Diffie-Hellman (DH)** solves the key distribution problem using the hardness of the **Discrete Logarithm Problem**. Both parties derive the same shared secret using only **public exchanges**, the secret is never transmitted.
:::

:::steps
1. **Agree Publicly**: Alice and Bob agree on public parameters: a large prime $p$ and a generator $g$. These values are published, Eve can see them. Example (simplified): $p = 23$, $g = 5$.
2. **Alice's Private Key**: Alice chooses a secret integer $a = 6$. She computes her public value: $A = g^a \pmod p = 5^6 \pmod{23} = 8$. Alice sends $A = 8$ to Bob.
3. **Bob's Private Key**: Bob chooses a secret integer $b = 15$. He computes his public value: $B = g^b \pmod p = 5^{15} \pmod{23} = 19$. Bob sends $B = 19$ to Alice.
4. **Alice Computes Shared Secret**: Alice computes $s = B^a \pmod p = 19^6 \pmod{23} = 2$.
5. **Bob Computes Shared Secret**: Bob computes $s = A^b \pmod p = 8^{15} \pmod{23} = 2$.
6. **Shared Secret Established**: Both parties independently arrived at $s = 2$ without ever transmitting it. Eve knows $g, p, A, B$ but must solve the Discrete Logarithm Problem ($5^a \equiv 8 \pmod{23}$) to find $a$ — infeasible for production-sized primes of 2048+ bits.
:::

:::image src="images/25_diffie_hellman_exchange.png" alt="Two-column exchange diagram labeled Alice (left) and Bob (right) with a public channel shown as a horizontal line in the middle and Eve watching the channel; Step 1 shows public parameters p=23, g=5 on the public channel; Step 2 shows Alice computing A=8 from private a=6 and sending it across the channel; Step 3 shows Bob computing B=19 from private b=15 and sending it across; Step 4 shows Alice computing s=19^6 mod 23 = 2; Step 5 shows Bob computing s=8^15 mod 23 = 2; both show a shared secret = 2 in a green box; Eve's side shows all public values known but a red X labeled 'Cannot solve Discrete Logarithm'" caption="Diffie-Hellman key exchange in action: Alice and Bob each contribute a public value derived from their private secrets. They independently compute the same shared secret. Eve sees all transmitted values but cannot recover the secret without solving the Discrete Logarithm Problem." width=full
:::

:::notes
The Diffie-Hellman key exchange is one of the most elegant results in applied mathematics. The insight is that modular exponentiation, while easy to compute in one direction, is hard to reverse, and this asymmetry can be exploited so that two parties publicly exchange intermediate values that jointly determine a shared secret, without that secret ever appearing in the channel.

Let's walk through the simplified worked example. The public parameters $p = 23$ and $g = 5$ are chosen and published, Eve is allowed to see them, and in production TLS these values are specified in the protocol standards. Alice privately chooses $a = 6$ and computes $A = 5^6 \bmod 23$. Working out $5^6 = 15625$, and $15625 \div 23 = 679$ remainder $8$, so $A = 8$. Bob privately chooses $b = 15$ and computes $B = 5^{15} \bmod 23 = 19$. They exchange $A$ and $B$ over the public channel.

Alice now computes $B^a \bmod p = 19^6 \bmod 23$. Bob computes $A^b \bmod p = 8^{15} \bmod 23$. Due to the properties of modular exponentiation, both calculations produce the same result: $(g^b)^a \equiv (g^a)^b \equiv g^{ab} \pmod p$. In our example, $g^{ab} = 5^{90} \bmod 23 = 2$. Both parties have computed the shared secret $s = 2$ without ever transmitting it. Eve, observing $p = 23$, $g = 5$, $A = 8$, $B = 19$, must find $a$ from $5^a \equiv 8 \pmod{23}$ — this is the Discrete Logarithm Problem. For $p = 23$ this is trivially solvable, which is why production DH uses primes of at least 2048 bits (NIST SP 800-56A Revision 3), making the DLP computationally infeasible.

In production TLS 1.3, Ephemeral Elliptic Curve Diffie-Hellman (ECDHE) is used instead of classical finite-field DH. ECDHE uses the Elliptic Curve Discrete Logarithm Problem on NIST-approved curves (P-256, P-384, or X25519 per RFC 7748), providing equivalent security to 3072-bit finite-field DH with only 256-bit keys. The "ephemeral" (E) component is critical: TLS 1.3 mandates that DH key pairs be generated fresh for every connection and discarded afterward, this provides **perfect forward secrecy (PFS)**, ensuring that compromise of the server's long-term private key cannot be used to decrypt past recorded sessions. TLS 1.2 allowed non-ephemeral RSA key exchange (where the client encrypts the session key with the server's RSA public key), meaning an attacker who recorded past sessions could decrypt them retroactively after obtaining the private key. PFS in TLS 1.3 eliminates this risk entirely. NIST SP 800-52 Revision 2 mandates TLS 1.3 with ECDHE for all new federal TLS deployments.

Diffie-Hellman key exchange is often explained by mixing paint: both parties start from a shared public base color, each adds a private color and exchanges the result, then each adds its private color again to reach the same final color. Because the mixing (modular exponentiation) is hard to reverse, an eavesdropper who sees only the exchanged mixtures cannot derive the shared result without a private color.
:::

%%%
---
unit: Asymmetric
code: ECC
title: "Elliptic Curve Cryptography: Smaller Keys, Same Security"
---
:::callout style=soft
**Elliptic Curve Cryptography (ECC)** performs key exchange and digital signatures using the algebraic structure of elliptic curves over finite fields. ECC achieves **equivalent security to RSA with dramatically smaller key sizes**, reducing computational overhead and bandwidth.
:::

::::columns ratio=1:1
::col::
::::card heading="Key Size Comparison"
:::table
| Algorithm | Key Size | Security Strength |
|---|---|---|
| RSA | 2048 bits | 112 bits |
| RSA | 3072 bits | 128 bits |
| ECDH / ECDSA | 256 bits | 128 bits |
| ECDH / ECDSA | 384 bits | 192 bits |
:::
::::
::col::
::::card heading="NIST-Approved Elliptic Curves (SP 800-186)"
:::list style=tight
- **P-256 (secp256r1)**: 128-bit security. Default for HTTPS/TLS, code signing, and most ECDSA deployments.
- **P-384 (secp384r1)**: 192-bit security. Required for SECRET-level NSA CNSA 2.0 data.
- **P-521 (secp521r1)**: 260-bit security. TOP SECRET-level.
- **X25519 (Curve25519)**: 128-bit security. Faster and simpler; used in TLS 1.3 and Signal Protocol.
:::
::::
::::

:::image src="images/25_elliptic_curve_point_addition.png" alt="Graph of an elliptic curve y^2 = x^3 - 3x + 5 over real numbers on an xy plane; two points P and Q are marked on the curve with a secant line passing through them; the line intersects the curve at a third point labeled R-prime, which is then reflected across the x-axis to produce the result point R = P + Q, illustrating elliptic curve point addition; a sidebar shows the discrete version over a finite field as a scattered grid of points; a comparison bar chart shows key sizes: RSA-3072 = 3072 bits vs ECDH P-256 = 256 bits with equivalent 128-bit security level" caption="Elliptic curve point addition: the sum of two points P and Q is defined geometrically as the reflection of the third curve intersection. Repeated point addition (scalar multiplication) is easy to compute but hard to reverse, the Elliptic Curve Discrete Logarithm Problem (ECDLP)." width=full
:::

:::notes
Elliptic Curve Cryptography is the dominant asymmetric cryptographic technology in modern deployments, providing equivalent security to RSA and classical Diffie-Hellman at dramatically reduced key sizes, computational cost, and bandwidth requirements. ECC is the default key exchange and signature mechanism in TLS 1.3, the SSH protocol, the Signal messaging protocol, Bitcoin and Ethereum blockchain signatures, and iOS and Android code signing.

An elliptic curve over a finite field is defined by an equation of the form $y^2 \equiv x^3 + ax + b \pmod p$ (for prime fields), where $p$ is a large prime, and the coefficients $a$ and $b$ satisfy certain non-degeneracy conditions. The set of points satisfying this equation, together with a special "point at infinity" serving as the additive identity, forms a mathematical group under a geometrically-defined addition operation. To add two distinct points $P$ and $Q$ on the curve, draw a line through them; it intersects the curve at a third point, which is then reflected across the x-axis to produce the sum $P + Q$. Doubling a point $P$ uses the tangent line at $P$ instead.

This point addition operation is the foundation of ECC. Scalar multiplication, computing $kP$ for a large integer $k$ by repeated addition, is computationally efficient using the double-and-add algorithm, analogous to binary exponentiation. However, the inverse problem, given $Q = kP$, find $k$ — is the Elliptic Curve Discrete Logarithm Problem (ECDLP). No sub-exponential algorithm is known for the ECDLP on properly chosen curves, which is why ECC achieves higher security per bit than integer-based systems where index calculus attacks provide sub-exponential algorithms.

The key size advantage is dramatic. As the table shows, a 256-bit ECC key provides 128 bits of security, the same as a 3072-bit RSA key. This 12:1 ratio in key size translates to significant advantages in practice: smaller TLS handshake messages, faster key generation and digital signature operations, reduced storage requirements for certificates, and lower power consumption on mobile and IoT devices. Apple's Secure Enclave uses P-256 ECDH for device key wrapping; the Signal Protocol uses X25519 (Curve25519) for its Double Ratchet key agreement mechanism.

NIST SP 800-186 defines the approved curves for federal use. The "NIST curves" (P-256, P-384, P-521) are widely deployed but have faced academic scrutiny regarding their parameter generation process. Curve25519, designed by Daniel J. Bernstein using a verifiable random parameter generation process (and thus not susceptible to the "nothing-up-my-sleeve numbers" concern), has become the preferred alternative in high-security contexts and is mandated in several modern protocols including TLS 1.3 (via RFC 7748) and the NSA's CNSA 2.0 suite for key exchange. Concerns about how NIST curve constants were generated are a case study in cryptographic trust: even public standards benefit from transparency in how their parameters are derived, and the academic preference for Curve25519 shows that trust covers not just the mathematical structure but the parameter-selection process.
:::

%%%
---
unit: Asymmetric
code: SIG
title: "Digital Signatures: Authentication and Non-Repudiation"
---
:::callout style=soft
A **digital signature** is an asymmetric cryptographic mechanism that binds a message to a specific private key holder. It simultaneously provides **authentication** (verifying the sender's identity) and **non-repudiation** (preventing the sender from denying authorship).
:::

:::steps
1. **Key Generation**: Alice generates an asymmetric key pair, a private key $d$ (kept secret) and a public key $Q$ (published in a certificate). For ECDSA (FIPS 186-5), $Q = dG$ where $G$ is the curve base point.
2. **Digest Computation**: Alice computes the SHA-256 hash of the document: $H = \text{SHA-256}(\text{document})$.
3. **Signature Generation**: Alice signs the digest using her private key: $\sigma = \text{Sign}(d, H)$. For ECDSA, this produces two integers $(r, s)$ derived from a random nonce $k$ and the private key.
4. **Distribution**: Alice sends the document, the signature $\sigma$, and her public key certificate (binding $Q$ to her identity via CA vouching).
5. **Verification**: Bob receives the document and computes $H' = \text{SHA-256}(\text{document})$, then verifies $\text{Verify}(Q, H', \sigma) = \text{True}$.
6. **Security Guarantee**: If verification succeeds, the document was signed by the holder of the private key $d$ corresponding to $Q$. If the document was modified, $H' \neq H$ and verification fails.
:::

:::image src="images/25_digital_signature_flow.png" alt="Two-phase diagram: left phase labeled Signing shows Alice's private key d and the SHA-256 hash of a document feeding into an ECDSA Sign box producing signature (r, s); Alice then distributes the document plus signature over a network; right phase labeled Verification shows Bob receiving the document and signature, computing SHA-256 of the received document to get H-prime, and running ECDSA Verify with Alice's public key Q; a green checkmark output means the document is authentic and unmodified; a red X output means either the document was tampered with or the signature is invalid; an adversary below the network labeled Mallory attempts to modify the document but the verification step detects the tampering" caption="Digital signature flow (ECDSA): the signer uses a private key to sign a document's hash; any verifier with the corresponding public key can confirm authenticity and detect any post-signing modification." width=full
:::

:::notes
Digital signatures are the cryptographic mechanism that most directly implements authentication and non-repudiation for the digital world. Unlike symmetric MACs (which require both parties to share a secret key and therefore cannot prove to a third party who created a message), digital signatures use asymmetric key pairs: the private key signs, and the corresponding public key verifies. Because only the private key holder can produce a valid signature, and the public key is published, any party who possesses the public key can independently verify the signature, creating a publicly verifiable proof of authorship.

The Electronic Signatures in Global and National Commerce Act (ESIGN Act, 2000) in the United States and the EU eIDAS Regulation (EU 910/2014) both recognize qualified digital signatures as legally equivalent to handwritten signatures for most commercial contracts. The eIDAS Regulation defines three levels of electronic signatures, with Qualified Electronic Signatures (QES) created using qualified certificates from EU Trust Service Providers (TSPs) carrying the highest legal weight. In practice, this means that ECDSA or RSA signatures on contracts, financial authorizations, and healthcare records can substitute for wet ink signatures in legally binding transactions, subject to jurisdiction-specific requirements.

The security of digital signatures rests on two foundations. First, hash function pre-image resistance: because the signer signs the SHA-256 hash of the document rather than the document itself (which is efficient for large documents), the integrity of the document is bound to the signature. If the document is modified after signing, its SHA-256 hash will change, causing signature verification to fail. Second, private key security: the signature can only be produced by the holder of the private key, so as long as the private key remains secret, the signature is unforgeable. Under the EU eIDAS Qualified Signature scheme, private keys for Qualified Electronic Signatures must be generated and stored in Qualified Signature Creation Devices (QSCDs), hardware security modules that prevent the private key from ever being extracted, analogous to FIPS 140-3 Level 3+ HSMs in the NIST framework.

ECDSA is specified in FIPS 186-5 for use with NIST-approved curves. A critical implementation vulnerability specific to ECDSA is the requirement for a cryptographically random, unique nonce $k$ in each signature generation. If the same nonce is reused in two signatures or the nonce has insufficient entropy, the private key can be algebraically recovered from the two signatures. This is not a theoretical concern: in 2010, the PlayStation 3's ECDSA implementation used a constant (non-random) nonce in its code signing system, allowing fail0verflow and geohot to extract Sony's ECDSA private key and sign arbitrary unsigned code, enabling the PS3 jailbreak. Sony subsequently sued multiple researchers. The fix, using a deterministic but securely derived nonce per RFC 6979, which derives $k$ deterministically from the private key and message hash, eliminates the nonce randomness requirement entirely and is now recommended practice. The PlayStation 3 signing-key compromise is a central example in cryptographic engineering: a single error, reusing the nonce in the ECDSA signature, turned a mathematically sound algorithm into a completely broken one, allowing the private key to be recovered.
:::

%%%
---
unit: Asymmetric
code: TLS
title: "TLS 1.3 Handshake: Cryptography in Action"
---
:::callout style=soft
**TLS 1.3 (RFC 8446)** combines all the cryptographic primitives studied so far, ECDHE, AES-GCM, SHA-256, and ECDSA, into a cohesive protocol providing **confidentiality, integrity, authentication, and perfect forward secrecy** for every HTTPS connection.
:::

:::flow
Client sends ClientHello with supported cipher suites and a ECDHE key share
Server sends ServerHello with chosen cipher suite (e.g., TLS_AES_256_GCM_SHA384) and its ECDHE key share
Both parties independently derive the same shared secret via ECDHE (HKDF-SHA256 key derivation)
Server sends its Certificate (containing ECDSA public key) and CertificateVerify (ECDSA signature over handshake transcript)
Client verifies Certificate against trusted CA root store; verifies CertificateVerify signature
Both parties derive session keys (write key, IV) from the shared secret using HKDF
Encrypted application data exchanged using AES-256-GCM with ephemeral session keys
:::

::::columns ratio=1:1
::col::
::::card heading="TLS 1.3 Improvements over TLS 1.2"
:::list style=tight
- **Mandatory PFS**: Only ECDHE and DHE key exchange, eliminates static RSA key exchange (no retrospective decryption).
- **Reduced Latency**: 1-RTT full handshake, 0-RTT resumption (with replay attack mitigations).
- **Banned Weak Algorithms**: No RC4, 3DES, SHA-1, MD5, RSA key exchange, or export ciphers.
- **Encrypted Handshake**: Server certificate is encrypted in transit (unlike TLS 1.2).
:::
::::
::col::
::::card heading="Approved TLS 1.3 Cipher Suites (RFC 8446)"
:::list style=tight
- `TLS_AES_256_GCM_SHA384`
- `TLS_AES_128_GCM_SHA256`
- `TLS_CHACHA20_POLY1305_SHA256`
:::
::::
::::

:::image src="images/25_tls13_handshake_flow.png" alt="Vertical sequence diagram with Client on the left and Server on the right: arrow 1 from Client to Server labeled ClientHello with key_share (X25519 public key) and supported_groups; arrow 2 from Server to Client labeled ServerHello with key_share (X25519 public key), then a dashed box labeled 'Both derive Handshake Secret via HKDF'; arrow 3 from Server to Client labeled Certificate (ECDSA cert chain) and CertificateVerify (ECDSA sig over handshake hash); arrow 4 from Server to Client labeled Finished (HMAC-SHA256 of handshake); arrow 5 from Client to Server labeled Finished; a dashed box labeled 'Both derive Application Traffic Keys via HKDF'; bidirectional arrow labeled Application Data (AES-256-GCM encrypted); a padlock icon marks the transition to encrypted traffic; all server certificate messages are shown in a shaded box labeled 'Encrypted in TLS 1.3'" caption="TLS 1.3 handshake: ECDHE establishes a shared secret in one round trip; HKDF derives session keys; ECDSA authenticates the server; AES-256-GCM encrypts application data. The ephemeral ECDHE keys ensure perfect forward secrecy for every session." width=full
:::

:::notes
TLS 1.3 (RFC 8446, finalized August 2018) is the culmination of decades of real-world cryptographic protocol engineering, incorporating lessons from numerous attacks against TLS 1.0, 1.1, and 1.2. Understanding a TLS 1.3 handshake is the best way to see how every primitive studied in this lecture works together in a production security protocol securing the majority of Internet traffic.

The TLS 1.3 handshake begins with a ClientHello message in which the client announces its supported protocol versions, cipher suites, and includes an ECDHE key share, its public value for the Diffie-Hellman exchange. For efficiency, TLS 1.3 includes the key share in the first message rather than waiting for the server's cipher suite selection, reducing the handshake to a single round trip (1-RTT). The server responds with its ServerHello containing its own ECDHE key share and the selected cipher suite. At this point, both parties independently compute the same shared secret (the ECDHE pre-master secret) using their own private key and the other party's public key share, then both apply the HKDF (HMAC-based Key Derivation Function, RFC 5869) with SHA-256 to derive a hierarchy of session keys: a handshake traffic secret for encrypting the rest of the handshake, and then application traffic secrets for encrypting data.

Server authentication occurs through the Certificate and CertificateVerify messages. The Certificate message contains the server's certificate chain up to a trusted root CA. The CertificateVerify message contains an ECDSA (or RSA-PSS) signature over the entire handshake transcript so far, critically, this signature binds the server's certificate to this specific handshake, preventing replay of certificates in man-in-the-middle attacks. The client verifies the certificate chain against its local trust store (containing root CA certificates pre-installed by the OS or browser), then verifies the CertificateVerify signature. If both checks pass, the client has cryptographically verified that it is talking to the legitimate owner of the server's domain.

TLS 1.3 made several breaking changes from TLS 1.2 that eliminated entire classes of attacks. Static RSA key exchange, where the client encrypts the session key with the server's RSA public key, was eliminated entirely. This eliminates the threat of "harvest now, decrypt later" attacks, where an adversary records encrypted TLS 1.2 traffic and retroactively decrypts it after obtaining the server's private key (through court order, hacking, or key compromise). With ECDHE-only key exchange, the ephemeral private keys are deleted immediately after the handshake, ensuring perfect forward secrecy. NIST SP 800-52 Revision 2 mandates TLS 1.3 for all federal agency servers, and PCI DSS 4.0 (released 2022) requires TLS 1.2 or higher (with 1.3 strongly preferred) for all cardholder data environment communications. Correct TLS server configuration disables TLS 1.0 and 1.1 (vulnerable to BEAST and POODLE), enables only the TLS 1.3 cipher suites, and turns on HSTS to prevent downgrade (SSL stripping) attacks.
:::

%%%
---
unit: Hashing
code: HMC
title: "HMAC: Authenticated Integrity with a Shared Key"
---
:::callout style=soft
**HMAC (Hash-based Message Authentication Code, RFC 2104)** combines a cryptographic hash function with a shared secret key to simultaneously verify **integrity** (the message was not modified) and **authenticity** (the message was created by a party knowing the shared key).
:::

::::columns ratio=1:1
::col::
::::card heading="HMAC Construction"
:::callout style=line
$$\text{HMAC}(K, m) = H\big((K \oplus \text{opad}) \| H((K \oplus \text{ipad}) \| m)\big)$$

- $K$: Secret key (padded to block size).
- $m$: Message.
- $\text{ipad}$: Inner padding $= 0x36$ repeated.
- $\text{opad}$: Outer padding $= 0x5C$ repeated.
- The double-hashing prevents length-extension attacks against the outer hash.
:::
::::
::col::
::::card heading="HMAC Applications"
:::list style=tight
- **AWS Signature Version 4**: All AWS API requests are signed with HMAC-SHA256, binding the request to the caller's secret access key.
- **JWT (JSON Web Tokens)**: HS256 algorithm uses HMAC-SHA256 to authenticate token claims.
- **TLS 1.2 Record Layer**: HMAC-SHA256 authenticates each TLS record.
- **IPsec**: HMAC-SHA256-128 provides authentication in ESP and AH headers (RFC 4868).
:::
::::
::::

:::image src="images/25_hmac_construction.png" alt="Flow diagram of the HMAC construction: at the top, key K is XORed with ipad (0x36 repeated) to produce K-ipad; K-ipad is concatenated with message m to form the inner input; inner input passes through Hash H (e.g., SHA-256) to produce inner hash; separately, K is XORed with opad (0x5C repeated) to produce K-opad; K-opad is concatenated with the inner hash; the concatenation passes through Hash H again to produce the final HMAC tag; a verification diagram shows the same process computed by the receiver who then compares their computed HMAC with the received HMAC using constant-time comparison" caption="HMAC construction: the message is hashed with the inner-padded key, then that inner hash is hashed again with the outer-padded key. The double-nesting prevents length-extension attacks and ties the output to possession of the shared key." width=full
:::

:::notes
Hash-based Message Authentication Codes (HMAC) solve an important limitation of raw hash functions: a hash like SHA-256 provides integrity (detecting modifications) but not authenticity (proving who created the message). Any attacker who intercepts a message and its SHA-256 digest can simply modify the message, recompute the SHA-256 hash, and forward both to the recipient. The recipient's hash check will pass, and they will have no indication the message was tampered with. HMAC addresses this by incorporating a secret key into the hash computation, so that only parties with knowledge of the shared key can produce or verify a valid HMAC tag.

The HMAC construction specified in RFC 2104 by Mihir Bellare, Ran Canetti, and Hugo Krawczyk is designed to be secure as long as the underlying hash function is a pseudorandom function. The double-hashing structure, applying the hash function twice, once with an inner-padded key and once with an outer-padded key, is specifically designed to prevent length-extension attacks. A length-extension attack against simple constructions like $H(K \| m)$ allows an attacker, knowing $H(K \| m)$ and the length of $K \| m$ but not $K$ itself, to compute $H(K \| m \| m')$ for any additional message content $m'$. This is because SHA-256 uses the Merkle-Damgård construction, where the hash state at the end of one hash can be continued as though it were computing a longer message. HMAC's outer hash layer prevents this: the inner hash produces an intermediate value that is then hashed again with the outer-padded key, meaning an attacker cannot extend the MAC without knowing $K$.

HMAC-SHA256 is ubiquitous in production authentication systems. AWS Signature Version 4 uses a chain of HMAC-SHA256 computations to sign all API requests, deriving a signing key from the secret access key, the date, the region, and the service name, meaning the signing key changes daily and is scoped to a specific service, limiting the blast radius of a signing key compromise. JSON Web Tokens (JWTs) using the HS256 algorithm apply HMAC-SHA256 to the base64url-encoded header and payload, preventing clients from modifying token claims such as user role or expiration time. A critical JWT vulnerability (CVE-2015-9235) involved implementations accepting tokens with the algorithm set to "none," bypassing HMAC verification entirely, a reminder that cryptographic protocol implementation must validate algorithm identifiers and reject insecure values even if the specification allows them as options.

The shared-key requirement is HMAC's primary limitation: both parties must possess the same secret key, meaning HMAC cannot provide non-repudiation (either party could have created the HMAC tag, so neither can prove to a third party that the other created it). For non-repudiation, asymmetric digital signatures (ECDSA, RSA-PSS) are required. In practice, TLS 1.3 replaces explicit HMAC for record-layer integrity with AEAD ciphers (AES-GCM, ChaCha20-Poly1305) that provide both confidentiality and integrity in a single cryptographic pass. However, HMAC remains the standard for API authentication, token signing, and key derivation (as HKDF uses HMAC as its underlying PRF).
:::

%%%
---
unit: Hashing
code: SHA
title: "SHA-256 Internals: The Merkle-Damgård Construction"
---
:::callout style=soft
SHA-256 (FIPS 180-4) is the industry-standard 256-bit hash function, built on the **Merkle-Damgård construction**: it iteratively compresses fixed-size blocks using a **compression function**, with the output of each step chained as input to the next.
:::

:::steps
1. **Preprocessing**: Pad the message to a multiple of 512 bits using SHA padding: append a single '1' bit, then '0' bits, then a 64-bit big-endian integer encoding the original message length in bits.
2. **Block Splitting**: Divide the padded message into 512-bit (64-byte) blocks $M_1, M_2, \ldots, M_n$.
3. **Initialize State**: Set the 256-bit internal state $H_0$ to the SHA-256 initial hash values, the fractional parts of the square roots of the first eight primes (the "nothing-up-my-sleeve" numbers).
4. **Compression Rounds**: For each block $M_i$, run 64 rounds of the SHA-256 compression function, which mixes the block's 16 32-bit words (expanded to 64 words via the SHA-256 message schedule) with the current state using bitwise operations, rotations, and additions modulo $2^{32}$.
5. **State Update**: Add the compression function output to the previous state $H_{i-1}$ (Davies-Meyer construction), producing the new state $H_i$.
6. **Final Digest**: After processing all blocks, concatenate the eight 32-bit state words $H_n$ to produce the 256-bit (32-byte) SHA-256 digest.
:::

:::image src="images/25_sha256_merkledamgard.png" alt="Horizontal chain diagram illustrating the Merkle-Damgård construction for SHA-256: five blocks labeled M1 through M4 and padding block are shown at the top; arrows from each block feed into a compression function box (f) alongside the current chaining value H; the first compression function receives the fixed IV (initial hash values); each compression function outputs a new 256-bit chaining value that feeds into the next function; the final chaining value after the last block is the SHA-256 digest; a magnified inset shows one compression function as 64 rounds of a mixing circuit with labeled operations: Ch, Maj, Sigma0, Sigma1, and additions mod 2^32" caption="SHA-256 uses the Merkle-Damgård construction: the message is broken into 512-bit blocks, each processed sequentially by the compression function with the running state chained as input. The final state is the 256-bit digest." width=full
:::

:::notes
Understanding SHA-256's internal structure helps explain both its security properties and its known limitations. SHA-256, part of the SHA-2 family standardized in FIPS 180-4, is the most widely deployed hash function in the world, used in TLS certificates, Bitcoin proof-of-work, Git commit hashes, code signing, and password hashing (as the underlying hash in PBKDF2 and HMAC-SHA256).

SHA-256 is built on the Merkle-Damgård construction, independently proposed by Ralph Merkle and Ivan Damgård in 1989. The central insight is that if you have a secure compression function that takes a fixed-size input and produces a fixed-size output, you can build a hash function for arbitrary-length inputs by iteratively applying the compression function, chaining the output of each invocation as the "state" input to the next. The message is padded to a multiple of the block size (512 bits for SHA-256), then split into blocks. The initial state $H_0$ is a fixed constant, specifically, the fractional parts of the square roots of the first eight prime numbers (2, 3, 5, 7, 11, 13, 17, 19). These "nothing-up-my-sleeve" numbers are chosen transparently to demonstrate that the constants are not backdoored.

Each 512-bit block is processed through 64 rounds of mixing operations that involve bitwise rotations, XOR, and conditional functions (Choice, Majority) operating on the eight 32-bit working variables. These non-linear operations create the confusion and diffusion properties that give SHA-256 its avalanche effect. The key schedule expands the sixteen 32-bit message words within each block into sixty-four 32-bit words using a linear recurrence, ensuring that each byte of the input influences many of the compression rounds.

The primary structural weakness of the Merkle-Damgård construction is the length-extension attack. Because the hash function's internal state after processing a message $m$ serves as the starting point for processing additional data, an attacker who knows $H(m)$ and the length of $m$ can compute $H(m \| \text{padding} \| m')$ for any chosen $m'$, without knowing $m$ itself. This breaks applications that use $H(K \| m)$ as a MAC, which is why HMAC uses a double-hash construction to block this attack. SHA-3 (FIPS 202), based on the Keccak sponge construction rather than Merkle-Damgård, is immune to length-extension attacks by design. For new MAC-based designs, using HMAC-SHA256 (RFC 2104) or switching to SHA-3 eliminates the length-extension concern. Git uses SHA-256 for its object content-addressing system (since Git 2.29, migrating from SHA-1), demonstrating that SHA-256 is a practical choice for integrity verification at internet scale. Bitcoin's proof of work applies SHA-256 twice, SHA-256(SHA-256(x)), which also mitigates length-extension attacks and adds a small margin against second-preimage attacks.
:::

%%%
---
unit: Hashing
code: HAP
title: "Hash Function Applications: Code Signing and Version Control"
---
:::callout style=soft
Cryptographic hashes are the backbone of **software supply chain integrity**. Code signing, package verification, and version control systems all depend on hash functions to detect unauthorized modifications between publication and execution.
:::

::::columns ratio=1:1
::col::
::::card heading="Code Signing Pipeline"
:::list style=tight
- **Developer signs**: Computes SHA-256 of compiled binary, signs digest with ECDSA private key.
- **CA vouches**: Code Signing Certificate (CSC) issued by a trusted CA binds developer identity to public key.
- **OS verifies**: Windows Authenticode, macOS Gatekeeper, and Linux IMA verify signatures before execution.
- **Timestamping**: RFC 3161 trusted timestamps bind the signature to a point in time, keeping signatures valid past certificate expiry.
:::
::::
::col::
::::card heading="Git Content-Addressing"
:::list style=tight
- **Every object is SHA-256 hashed**: Commits, files (blobs), and directories (trees) are stored under their hash.
- **Tamper-evident history**: Changing any historical commit changes its hash, which changes all descendant commit hashes, immediately detectable.
- **CVE mitigation**: SHAttered (SHA-1 collision) motivated Git's migration to SHA-256 (git 2.29+).
:::
::::
::::

:::image src="images/25_code_signing_pipeline.png" alt="Horizontal pipeline diagram with five stages: (1) Developer writes source code, icon of a keyboard; (2) Build system compiles binary and computes SHA-256 digest of the output file; (3) Developer's private key signs the digest with ECDSA producing a detached signature file; (4) Code Signing Certificate from a trusted CA binds developer identity to the public key, shown as a certificate icon with a CA seal; (5) End user's operating system (Windows Authenticode logo, macOS Gatekeeper logo) verifies the certificate chain and ECDSA signature before allowing the binary to execute; a red X bypass scenario shows unsigned code being blocked by the OS with an 'Unidentified Developer' dialog" caption="Code signing pipeline: the developer signs a SHA-256 hash of the binary with their ECDSA private key, bound to their identity by a CA-issued certificate. The OS verifies the signature at runtime, blocking tampered or unsigned executables." width=full
:::

:::notes
Cryptographic hash functions are the invisible foundation of software distribution security. Every time you download an application from the Apple App Store, install a Python package from PyPI, or receive an automatic Windows Update, hash functions and digital signatures are working together to verify that the software you execute is exactly the software that was published by the vendor, byte-for-byte identical, with no modifications introduced during transit or storage.

Code signing is the process of attaching a digital signature to executable software, binding the binary to a specific developer identity vouched for by a Certificate Authority. The signing process works as follows: the developer computes a SHA-256 (or SHA-384) hash of the compiled binary, then signs that hash with their ECDSA or RSA private key using a Code Signing Certificate issued by a trusted CA (such as DigiCert, Sectigo, or GlobalSign, which are themselves cross-signed by root CAs embedded in operating system trust stores). The resulting signature is attached to the binary, typically as an embedded Authenticode signature (Windows PE format), an embedded CMS signature (macOS Mach-O format), or a detached signature file (.asc for GPG-signed Linux packages).

At execution time, the operating system verifies the signature chain. Windows Authenticode checks that the code signing certificate is valid, not revoked (via OCSP or CRL check), chains to a trusted root, and that the ECDSA signature over the binary's hash verifies correctly. If any check fails, including if a single byte of the binary has been modified after signing, the OS displays an "Unknown Publisher" or blocks execution entirely, depending on the user's security policy. Microsoft's Smart App Control in Windows 11 further restricts execution to signed software with established reputation scores.

The SolarWinds SUNBURST attack (2020, CVE-2020-10148) is a critical case study in code signing's limitation and its proper application. Attackers compromised the SolarWinds Orion build system and injected malicious code into the source before compilation. Because the build system itself was compromised, the resulting binary was correctly signed with SolarWinds' legitimate code signing certificate, the signature was valid and the binary was not externally modified after signing. This demonstrates that code signing protects against supply chain tampering downstream of the build system, but cannot protect against a compromised build infrastructure. The response to SUNBURST has driven adoption of Supply Chain Levels for Software Artifacts (SLSA) framework and in-toto attestations, which cryptographically record and verify each step of the build pipeline from source to binary, enabling detection of build-time tampering even when the final artifact is correctly signed. Git's move from SHA-1 to SHA-256 (announced in Git 2.29) was driven by the SHAttered collision: two distinct source trees sharing a SHA-1 commit hash would let an attacker substitute an alternative repository with no detectable hash mismatch in systems that rely on SHA-1 for integrity.
:::

%%%
---
unit: Hashing
code: RBW
title: "Rainbow Tables and the Defense of Salting"
---
:::callout style=soft
A **rainbow table** is a precomputed data structure mapping millions of common passwords to their hash values, enabling instant lookup of unsalted hashes. **Salting** defeats rainbow tables by making each hash unique to the individual user.
:::

::::columns ratio=1:1
::col::
::::card heading="Rainbow Table Attack"
:::list style=tight
- **Precomputation Phase**: Attacker generates millions of (password → SHA-256 hash) pairs and stores them in a compressed chain structure.
- **Attack Phase**: For each stolen unsalted hash, perform a lookup in the rainbow table, match found in milliseconds.
- **Scale**: RainbowCrack can crack unsalted MD5/SHA-1 hashes covering all 8-character alphanumeric passwords in under one second using precomputed tables of a few gigabytes.
- **Trade-off**: Rainbow tables trade storage space for computation time (time-memory trade-off).
:::
::::
::col::
::::card heading="Salt Defense"
:::list style=tight
- **Random per-user salt**: Generate 16+ bytes of CSPRNG-generated salt per user at registration.
- **Stored with hash**: Salt is stored in plaintext alongside the hash, its purpose is uniqueness, not secrecy.
- **Defeats precomputation**: Each user's hash is now unique: SHA-256("password" + salt1) ≠ SHA-256("password" + salt2). No precomputed table can cover all possible salted combinations.
- **Remaining threat**: GPU brute-force of a single user's hash. Defense: use memory-hard KDFs (Argon2id).
:::
::::
::::

:::image src="images/25_rainbow_table_vs_salt.png" alt="Two-panel diagram: left panel labeled Rainbow Table Attack shows a stolen database of unsalted SHA-256 hashes on the left; an arrow labeled 'lookup' points to a rainbow table data structure (shown as a two-column table of passwords and hashes) on the right; a stopwatch icon shows 'milliseconds to find match'; below it a password 'password123' with its SHA-256 hash is highlighted in both the database and the rainbow table; right panel labeled Salted Hash shows two users with the same password 'password123'; user Alice has salt 'a3f7b2' making her stored hash unique, user Bob has salt 'd8c1e4' making his stored hash different; a rainbow table is shown with a red X and label 'No precomputed table can cover unique salt combinations'" caption="Rainbow table attack vs. salted hashing: unsalted hashes allow instant lookup from precomputed tables. Per-user random salts ensure each user's hash is cryptographically unique, forcing an attacker to brute-force each account individually." width=full
:::

:::notes
Rainbow tables represent the most common and historically devastating attack against password hash databases. They exploit a fundamental property of deterministic hash functions: given the same input, a hash function always produces the same output. If two users choose the same password "password123," an unsalted database will store identical SHA-256 hashes for both users. An attacker who steals the hash database can precompute a lookup table containing millions of common passwords and their SHA-256 hashes, then instantly find every user whose hash matches a known password by performing a simple table lookup.

The rainbow table, introduced by Philippe Oechslin in 2003, is an optimized time-memory trade-off data structure for this precomputation attack. Unlike a simple lookup table which requires storing every (password, hash) pair explicitly, a rainbow table uses chains of alternating hash and reduction function applications, allowing coverage of a much larger password space in a given amount of storage. Using rainbow tables generated by tools like RainbowCrack, an attacker can crack every unsalted MD5 or SHA-1 hash corresponding to an 8-character password using a table of approximately 2 gigabytes stored on a standard SSD, recovering each password in under a second. Free rainbow tables covering common password sets are available for download on the internet.

The defense against rainbow tables is salting: before hashing, append (or prepend) a unique, cryptographically random value (the salt) to each user's password. With a 128-bit (16-byte) random salt, there are $2^{128}$ possible salted variants of any given password. A rainbow table that covers all combinations of 8-character passwords with 128-bit salts would require more storage than exists in the entire observable universe, precomputation becomes impossible.

It is critical to understand that the salt is not a secret. It is stored in plaintext alongside the hash in the user database, and the attacker will obtain it when they steal the database. The salt's purpose is uniqueness, not secrecy. With the salt known, an attacker can still attempt to brute-force a specific user's password hash by computing KDF(salt + guessed_password) repeatedly. This is why salting alone is insufficient and must be combined with a memory-hard KDF like Argon2id: even knowing the salt, the attacker can only attempt a few hundred hashes per second on high-end hardware (versus billions of simple SHA-256 hashes per second), making brute-force of long passwords impractical. The 2012 LinkedIn breach (117 million unsalted SHA-1 hashes) and the 2013 Adobe breach (153 million accounts using a single global salt with 3DES encryption rather than proper hashing) are landmark case studies in the combined failure of salting and KDF selection that NIST SP 800-63B Section 5.1.1.2 is explicitly designed to prevent.
:::

%%%
---
unit: CaseStudy
code: CS1
title: "Case Study: LinkedIn 2012 Password Breach"
---
:::callout style=soft
In June 2012, LinkedIn suffered one of the most consequential password breaches in history: **117 million** user password hashes were stolen. The failure to salt hashes allowed mass credential recovery, illustrating exactly why NIST SP 800-63B's salting requirements exist.
:::

::::columns ratio=1:1
::col::
::::card heading="Timeline"
:::list style=tight
- **June 5, 2012**: LinkedIn's database is breached. Approximately 6.5 million unsalted SHA-1 hashes posted to a Russian forum.
- **June 6, 2012**: LinkedIn confirms breach; users are notified to reset passwords.
- **2016**: Breach full scope revealed, 117 million account records, including emails and unsalted SHA-1 hashes, sold on the dark web for 5 Bitcoin (~$2,200 at the time).
- **Post-breach**: LinkedIn migrated to salted bcrypt hashes. Fined £500,000 by UK ICO for inadequate security.
:::
::::
::col::
::::card heading="Technical Failure Analysis"
:::list style=tight
- **No salt**: Identical passwords produced identical hashes, rainbow tables cracked common passwords instantly.
- **SHA-1 (not a KDF)**: SHA-1 is designed to be fast; attackers achieved >10 billion SHA-1 hash attempts per second on GPUs.
- **No MFA**: Cracked passwords immediately enabled account takeover without additional factors.
- **Delayed detection**: No database activity monitoring detected the exfiltration in real time.
:::
::::
::::

:::image src="images/25_linkedin_breach_analysis.png" alt="Split diagram: left side labeled 'What LinkedIn Did (Insecure)' shows a user database icon with columns email and SHA-1 hash (no salt column); a GPU farm icon labeled 'Attacker' cracks hashes at 10 billion per second; a rainbow table icon shows common passwords recovered in seconds; cracked credentials feed into a dark web marketplace icon; right side labeled 'What Should Have Been Done (NIST SP 800-63B)' shows a database with email, salt, and Argon2id hash columns; the same GPU farm attempts brute-force but a clock shows '200 years per user with 10-char password'; GDPR and HIPAA compliance icons appear at the bottom right with a 'Protected' label" caption="LinkedIn 2012 breach analysis: unsalted SHA-1 hashes enabled instant rainbow table recovery of millions of passwords. NIST SP 800-63B-compliant Argon2id with per-user salt would have rendered the same stolen database practically useless to attackers." width=full
:::

:::notes
The 2012 LinkedIn breach is the canonical case study for cryptographic password storage failures. It illustrates in concrete terms how a single technical decision, choosing SHA-1 without salting instead of a proper memory-hard KDF, directly translated into the compromise of over 100 million user accounts and enabled widespread account takeover, credential stuffing attacks, and regulatory liability.

The breach occurred when attackers exploited an unpatched vulnerability (the exact initial vector was not publicly disclosed) to access LinkedIn's production database. The exported data contained approximately 117 million records, each consisting of an email address and an unsalted SHA-1 hash of the user's password. SHA-1 produces a 160-bit hash value and is designed to be computationally efficient, it can execute approximately 10 billion iterations per second on a high-end GPU (as of 2012 hardware; modern hardware exceeds this dramatically). Without salting, every instance of the same password produced the same hash across all users. An attacker could therefore crack common passwords once and recover credentials for every user who chose that password simultaneously.

The immediate consequence was devastating and rapid. Within 24 hours of the initial 6.5 million hash posting on the Russian forum InsidePro.com, community crackers had recovered over 4 million passwords. Tools like Hashcat, freely available, GPU-accelerated, could attempt all passwords in the RockYou wordlist (14 million entries) in under a second against an unsalted SHA-1 hash. Longer passwords in the top million most common password lists were recovered within hours. Users who had chosen genuinely random, long passwords were protected by entropy, not by LinkedIn's storage choice, their safety was incidental rather than designed.

The credential stuffing impact extended far beyond LinkedIn itself. Because many users reuse passwords across multiple services, the cracked LinkedIn credentials were tested against Gmail, banking platforms, corporate VPNs, and other services. This technique, credential stuffing, became a primary attack vector in the years following the breach, with the stolen LinkedIn dataset enabling attacks against Twitter, Dropbox, and dozens of other companies. Dropbox, for instance, disclosed in 2016 that a 2012 breach affecting 68 million accounts was traced to a LinkedIn employee whose Dropbox credentials matched their compromised LinkedIn password.

The regulatory response established important legal precedents for cryptographic adequacy under data protection law. The UK Information Commissioner's Office (ICO) fined LinkedIn £500,000 under the 1998 UK Data Protection Act, the maximum fine available at the time, for failing to implement adequate security measures for the personal data it held. Under GDPR (effective May 2018), the same failure would face fines of up to 4% of global annual turnover or €20 million, whichever is greater, a dramatically more severe penalty that has changed the cost-benefit calculus for security investments across the industry. LinkedIn's post-breach remediation included migrating all stored passwords to salted bcrypt hashes and implementing mandatory password resets for all affected accounts. The technical remediation was correct but arrived only after massive harm had already occurred.

The LinkedIn breach answers the common objection that proper cryptographic implementation is not worth the effort when the simpler approach "works": the cost of salting and switching from SHA-1 to bcrypt or Argon2id was negligible beside the fine, the reputational damage, the forced mass migration and the harm to users. NIST SP 800-63B Section 5.1.1.2 exists to prevent exactly this outcome.
:::

%%%
---
unit: Hashing
code: KST
title: "Key Stretching Comparison: Argon2id vs. bcrypt vs. PBKDF2"
---
:::callout style=soft
**Key stretching** functions (KDFs) are intentionally slow or memory-intensive, transforming a fast brute-force search into an impractical computation. Choosing the right KDF is a concrete engineering decision with direct security impact.
:::

:::table
| KDF | OWASP Minimum Config | GPU Attack Speed (2024) | Memory-Hard? | FIPS 140-3? | Recommended For |
|---|---|---|---|---|---|
| **Argon2id** (RFC 9106) | m=19 MiB, t=2, p=1 | ~10 H/s per GPU | Yes | No (use PBKDF2 in FIPS) | New systems, preferred |
| **bcrypt** | cost=10 | ~10,000 H/s per GPU | Partially | No | Legacy systems |
| **PBKDF2-SHA256** | 600,000 iterations | ~30,000 H/s per GPU | No | Yes (SP 800-132) | FIPS-compliant environments |
| **scrypt** (RFC 7914) | N=32768, r=8, p=1 | ~500 H/s per GPU | Yes | No | Alternative to Argon2 |
| **SHA-256 (unsalted)** | — | ~10,000,000,000 H/s per GPU | No | No | NEVER for passwords |
:::

:::callout style=soft
The difference between Argon2id (10 H/s) and unsalted SHA-256 (10,000,000,000 H/s) represents a **10⁹ fold** reduction in attacker throughput. A 10-character alphanumeric password takes 3 billion years to brute-force under Argon2id vs. **under 1 second** under unsalted SHA-256.
:::

:::image src="images/25_kdf_comparison_chart.png" alt="Horizontal bar chart comparing key stretching algorithms on a logarithmic scale: x-axis labeled 'GPU Hashes per Second' ranging from 1 to 10 billion; Argon2id bar reaches approximately 10 (leftmost, labeled 'Most Secure'); bcrypt bar reaches 10,000; scrypt bar reaches 500; PBKDF2-SHA256 bar reaches 30,000; plain SHA-256 bar extends fully to 10 billion (labeled 'Never Use for Passwords'); each bar is color-coded: green for Argon2id, yellow-green for bcrypt, yellow for scrypt, orange for PBKDF2, red for SHA-256; a second panel shows time to crack a random 10-character password for each algorithm" caption="KDF comparison by GPU attack throughput: Argon2id's memory-hardness reduces attacker throughput by a factor of one billion compared to plain SHA-256, making brute-force of properly chosen passwords computationally infeasible even against well-resourced attackers." width=full
:::

:::notes
Choosing the right key derivation function for password storage is not an academic exercise, it is a decision that directly determines whether a stolen credential database is catastrophic or merely an inconvenience to the attacker. The comparison table makes the security differences concrete by quantifying attacker throughput under each algorithm on modern GPU hardware, which represents the realistic threat model for a large-scale credential database attack.

Argon2id, standardized in RFC 9106 and winner of the 2015 Password Hashing Competition (PHC), is the current OWASP and NIST-preferred recommendation for new password storage systems. It has three variants: Argon2d (optimized against GPU attacks, but vulnerable to side-channel timing attacks), Argon2i (resistant to side-channel attacks but slightly weaker against GPU attacks), and Argon2id (a hybrid combining both approaches in sequence, providing the best overall security). The "id" variant is recommended for password hashing. Argon2id's security comes primarily from its memory hardness parameter: requiring each hash computation to access a configurable amount of RAM (OWASP minimum: 19 MiB, with 64 MiB recommended for high-security systems) means that the attacker's GPU, which has limited VRAM per computation core, can run far fewer parallel hash attempts than against a memory-free algorithm. A high-end GPU with 24 GB of VRAM can run at most ~1,000 simultaneous Argon2id computations at 19 MiB each, versus millions of simultaneous SHA-256 computations.

bcrypt was designed by Niels Provos and David Mazières in 1999 with the explicit goal of remaining slow on improving hardware by providing an adjustable cost factor. The cost factor doubles the work per increment: cost=10 performs 2¹⁰ = 1,024 iterations of the Blowfish key setup, while cost=11 performs 2,048. bcrypt has a critical limitation: it silently truncates passwords at 72 bytes, meaning passwords longer than 72 characters offer no additional security. Some implementations address this by pre-hashing the password with SHA-256 before passing it to bcrypt (the "bcrypt+SHA256" pattern used by Django, for example), though this introduces subtleties around null-byte handling. bcrypt also uses a fixed 4 KiB internal memory, making it less resistant to highly optimized GPU implementations than Argon2id.

PBKDF2-SHA256 (NIST SP 800-132) is the only FIPS 140-3 approved password KDF, making it the required choice for federal systems and environments mandating FIPS compliance. However, PBKDF2 is not memory-hard, it performs a fixed amount of computation per iteration with minimal memory, which means GPU-based attackers can run it faster per unit of hardware investment than Argon2id. The 600,000 iteration minimum recommended by OWASP (derived from the goal of requiring approximately 1 CPU-second per hash verification) translates to approximately 30,000 H/s on a high-end GPU, three times faster than bcrypt at cost=10 and three orders of magnitude faster than Argon2id. NIST is aware of PBKDF2's limitations and SP 800-63B acknowledges that memory-hard functions like Argon2id and scrypt are preferable where FIPS compliance is not required.

Key-derivation cost parameters must be tuned to hardware and raised as hardware improves. A bcrypt cost that needed 100 ms in 2012 may need only 10 ms on 2024 servers, reducing effective security, so systems should benchmark on their own hardware and target 100-500 ms of verification time for consumer authentication. OWASP's Password Storage Cheat Sheet gives current minimums.
:::

%%%
---
unit: Keys
code: HSM
title: "Tool Spotlight: Hardware Security Modules (HSMs)"
---
:::callout style=soft
A **Hardware Security Module (HSM)** is a tamper-resistant, dedicated cryptographic co-processor that stores and uses cryptographic keys in a physically and logically protected environment. HSMs ensure that key material **never appears in software-accessible memory**.
:::

::::columns ratio=1:1
::col::
::::card heading="HSM Security Properties"
:::list style=tight
- **Physical Tamper Resistance**: Enclosure detects physical intrusion (drilling, probing) and automatically erases key material (zeroization).
- **Logical Access Control**: Multi-person authorization ("M of N" schemes) for key administration operations.
- **FIPS 140-3 Certification**: Levels 1–4; Level 2+ requires tamper evidence; Level 3+ requires active tamper response with zeroization; Level 4 is the highest, covering environmental attacks.
- **Cryptographic Operations On-Chip**: Private keys never leave the HSM; operations (sign, decrypt) are performed inside the device.
:::
::::
::col::
::::card heading="Common HSM Deployments"
:::list style=tight
- **Certificate Authority Root Keys**: Root CA private keys for HTTPS PKI stored in HSMs to prevent key theft (DigiCert, Let's Encrypt).
- **TLS Private Keys**: Web server TLS private keys in network-attached HSMs (AWS CloudHSM, Azure Dedicated HSM, Thales Luna).
- **Payment Processing**: PCI PTS-certified HSMs (PIN Entry Devices, HSM modules) process and derive payment keys for EMV chip transactions.
- **Code Signing**: Developer code signing private keys stored in HSMs to prevent signing key exfiltration.
:::
::::
::::

:::image src="images/25_hsm_architecture.png" alt="Diagram of HSM architecture: a physical server on the left labeled Application Server sends a 'Sign this hash' request over a standard API (PKCS#11 or JCE) to a hardware device on the right labeled HSM; inside the HSM box, subcomponents are visible: a tamper-detection sensor layer, a secure processor labeled Cryptographic Engine, secure RAM labeled Key Store (keys never leave this boundary), and a battery-backed key zeroization circuit; an arrow from Cryptographic Engine labeled 'Signature only (key stays inside)' returns to the application server; a physical tamper indicator shows a broken seal icon with 'Zeroize all keys' trigger; FIPS 140-3 Level 3 badge displayed on the HSM" caption="HSM architecture: applications request cryptographic operations via standard APIs; the HSM performs operations internally and returns only the result. Private keys never cross the HSM boundary into general-purpose memory, preventing extraction by software-based attacks." width=full
:::

:::notes
Hardware Security Modules are specialized cryptographic devices that solve a fundamental problem in key management: if private keys exist in software-accessible memory on a general-purpose computer, they can be stolen by malware, memory-scraping attacks, hypervisor exploits, or cold-boot attacks. HSMs address this by ensuring that key material is generated, stored, and used exclusively within a tamper-resistant hardware boundary from which it cannot be extracted.

HSMs are certified under FIPS 140-3 (or its predecessor FIPS 140-2) at four security levels. Level 1 requires only correct cryptographic algorithm implementation with no physical security requirements. Level 2 adds tamper-evident physical design, seals or coatings that show evidence of physical intrusion attempts. Level 3 requires tamper-responsive design: the device must detect intrusion and automatically zeroize (overwrite) all stored key material. Level 4 provides the highest protection, including environmental attack protection (voltage, temperature, and electromagnetic attack resistance) and zeroization against probing through the enclosure. For most enterprise deployments, FIPS 140-3 Level 2 or Level 3 is specified.

HSMs expose their functionality through standardized APIs. PKCS#11 (Cryptoki, defined by OASIS) is the dominant cross-platform API, implemented by virtually all HSM vendors and integrated into OpenSSL, Java PKCS11 Provider, and most enterprise security middleware. The Java Cryptography Extension (JCE) framework with HSM-backed providers is widely used in Java enterprise environments. Microsoft CNG (Cryptography API: Next Generation) provides HSM integration for Windows PKI and code signing.

Cloud HSM services have democratized access to HSM-grade key management. AWS CloudHSM provides customer-dedicated FIPS 140-3 Level 3 HSM clusters managed by the customer with no AWS access to keys, distinguishing it from AWS KMS, which is a managed service where AWS operates the HSM infrastructure. Google Cloud HSM and Azure Dedicated HSM offer similar dedicated HSM offerings. For budget-constrained deployments, cloud KMS services (AWS KMS, Azure Key Vault HSM tier, Google Cloud KMS) provide HSM-backed key storage using shared HSM infrastructure at lower cost, with the cloud provider managing the hardware.

Critical infrastructure deployments mandate HSM use for the most sensitive key material. The Certificate Authority/Browser Forum's Baseline Requirements (section 6.2.7) require that CA root private keys be stored in HSMs meeting FIPS 140-2 Level 3 (or equivalent) requirements. The payment card industry's PCI PTS HSM Security Requirements define certification requirements for HSMs used in PIN processing and payment key management, separate from general-purpose FIPS certification. The 2011 RSA SecurID breach, in which attackers stole seed values from RSA's authentication system, demonstrated that HSM-based key storage reduces but does not eliminate risk, the HSM protects keys at rest and in use, but a compromised key management system or insider threat can still export encrypted key material under circumstances that pass access control checks. Defense-in-depth with HSMs, strong access controls, key ceremony procedures with N-of-M authorization, and comprehensive audit logging is required.
:::

%%%
---
unit: Keys
code: RNG
title: "Cryptographic Random Number Generation: CSPRNG Requirements"
---
:::callout style=soft
Cryptographic security depends entirely on unpredictable keys, nonces, IVs, and salts. **Cryptographically Secure Pseudo-Random Number Generators (CSPRNGs)** meet strict requirements for unpredictability; standard PRNGs do not and must never be used for cryptographic purposes.
:::

::::columns ratio=1:1
::col::
::::card heading="CSPRNG Requirements (NIST SP 800-90A)"
:::list style=tight
- **Unpredictability**: Output must be computationally indistinguishable from true randomness.
- **Forward Secrecy**: Compromise of the current state must not expose past outputs.
- **Backward Secrecy**: Compromise of the current state must not expose future outputs after reseeding.
- **Entropy Sources**: Must be seeded from high-entropy hardware sources (CPU timing jitter, hardware RNG, OS entropy pool).
:::
::::
::col::
::::card heading="Approved vs. Forbidden PRNGs"
:::table
| Source | Type | Cryptographic Use? |
|---|---|---|
| `/dev/urandom` (Linux) | OS CSPRNG | Yes |
| `os.urandom()` (Python) | OS CSPRNG | Yes |
| `crypto.randomBytes()` (Node.js) | OS CSPRNG | Yes |
| `secrets` module (Python) | OS CSPRNG | Yes |
| `random.random()` (Python) | LCG PRNG | **NEVER** |
| `Math.random()` (JavaScript) | PRNG | **NEVER** |
| `java.util.Random` | Linear Congruential | **NEVER** |
:::
::::
::::

:::image src="images/25_csprng_entropy_sources.png" alt="Architecture diagram of a Linux kernel CSPRNG: at the top, multiple entropy sources feed into a central entropy pool icon: CPU hardware RNG (RDRAND instruction), keyboard timing jitter, disk interrupt timing, network packet arrival timing, and hardware noise sources; the entropy pool feeds the ChaCha20-based CSPRNG within the kernel; two interface arrows emerge: /dev/urandom (for applications) and /dev/random (blocking until sufficient entropy); application code examples show os.urandom() in Python and crypto.randomBytes() in Node.js using the OS CSPRNG; at the bottom, a crossed-out code snippet shows random.random() with a red label 'Predictable, DO NOT use for keys'" caption="Linux CSPRNG architecture: multiple hardware entropy sources feed the kernel's ChaCha20-based entropy pool. Applications access cryptographic randomness through /dev/urandom or OS-level wrappers. Standard PRNGs are deterministic and unsuitable for any cryptographic purpose." width=full
:::

:::notes
Randomness is the foundation of all cryptographic security. Every cryptographic key, nonce, IV, salt, and challenge must be generated from a source that is computationally indistinguishable from true randomness, and whose output cannot be predicted by an adversary even after observing previous outputs. This requirement is non-negotiable: if an attacker can predict or enumerate the possible values of a key, nonce, or IV, they can break the cryptographic protections regardless of the underlying algorithm's mathematical strength.

Standard pseudo-random number generators (PRNGs), including Python's random module (based on the Mersenne Twister), JavaScript's Math.random(), and Java's java.util.Random (based on a Linear Congruential Generator), are fundamentally unsuitable for cryptographic use. They are designed for statistical uniformity and speed in simulation and gaming applications, not for cryptographic unpredictability. The Mersenne Twister's internal state can be fully reconstructed after observing as few as 624 consecutive 32-bit outputs; once reconstructed, all past and future outputs can be computed exactly. Linear Congruential Generators have even shorter crack times. These are not obscure academic vulnerabilities, they are standard features of the algorithms' designs.

CSPRNGs meet a strict set of security requirements formalized in NIST SP 800-90A Revision 1, which specifies three approved DRBG (Deterministic Random Bit Generator) designs: Hash_DRBG (based on SHA-256/SHA-512), HMAC_DRBG (based on HMAC-SHA256), and CTR_DRBG (based on AES-256-CTR). These designs provide computational security: an adversary with unlimited computing power but no knowledge of the internal state cannot distinguish their output from a true random oracle. The Linux kernel (version 5.17+) replaced its legacy ANSI X9.31 DRBG with a ChaCha20-based CSPRNG seeded from multiple hardware entropy sources, providing the operating system entropy pool used by /dev/urandom and the getrandom() syscall.

At the application layer, developers should always use OS-provided CSPRNG interfaces rather than implementing their own. Python's secrets module (introduced in Python 3.6 and specified in PEP 506) provides a clean CSPRNG interface with functions like secrets.token_bytes(), secrets.token_hex(), and secrets.randbelow() specifically designed for security-sensitive applications. The Node.js crypto.randomBytes() function wraps the OS CSPRNG. Go's crypto/rand package uses the OS CSPRNG. Java's java.security.SecureRandom with the "SUN" or platform-native provider wraps the OS CSPRNG; java.util.Random must never be used for cryptographic purposes.

The CVE-2008-0166 Debian OpenSSL entropy bug is the benchmark case study of CSPRNG failure at scale. A well-intentioned patch to suppress a Valgrind memory analysis warning inadvertently removed two lines of code that fed process ID entropy into OpenSSL's PRNG, leaving only the process ID itself (a value between 1 and 32,767 on typical Linux systems) as the PRNG seed for all key generation operations. The result was that every SSH host key, TLS certificate, and OpenVPN key generated on any Debian or Ubuntu system between September 2006 and May 2008 was one of at most 32,768 unique keys for any given key type and length. An attacker could precompute all 32,768 possible 2048-bit RSA private keys for any given key length in minutes, then instantly determine any affected private key given only the public key. The Debian project released patches in May 2008, but the remediation required regenerating every affected key and replacing every affected certificate, a massive operational undertaking for thousands of organizations. The Debian OpenSSL bug is a lesson in the unintended consequences of "safe" changes: a patch meant to make the code cleaner under a debugging tool reduced key entropy from 2048 bits to 15, making keys guessable. Security-critical code paths require cryptographic review for any change, however minor it appears.
:::

%%%
---
unit: PostQuantum
code: PQC
title: "Post-Quantum Cryptography: NIST PQC Standardization"
---
:::callout style=soft
**Quantum computers** running Shor's algorithm can break RSA, ECDSA, and Diffie-Hellman in polynomial time, threatening all currently deployed asymmetric cryptography. NIST has standardized the first post-quantum cryptographic algorithms (FIPS 203, 204, 205) for deployment before large-scale quantum computers arrive.
:::

::::columns ratio=1:1
::col::
::::card heading="Quantum Threat to Current Algorithms"
:::table
| Algorithm | Quantum Attack | Impact |
|---|---|---|
| RSA (all key sizes) | Shor's algorithm | Completely broken |
| ECDH / ECDSA | Shor's algorithm | Completely broken |
| AES-128 | Grover's algorithm | Security halved (→64 bits) |
| AES-256 | Grover's algorithm | Security reduced (→128 bits) |
| SHA-256 | Grover's algorithm | Security halved (→128 bits) |
| SHA-384/SHA-512 | Grover's algorithm | Remains adequate |
:::
::::
::col::
::::card heading="NIST PQC Standards (2024)"
:::list style=tight
- **FIPS 203, ML-KEM (Kyber)**: Lattice-based key encapsulation mechanism. Replaces ECDH/RSA for key exchange.
- **FIPS 204, ML-DSA (Dilithium)**: Lattice-based digital signature algorithm. Replaces ECDSA/RSA signatures.
- **FIPS 205, SLH-DSA (SPHINCS+)**: Hash-based digital signature. Conservative alternative signature scheme.
- **CNSA 2.0**: NSA mandate to transition National Security Systems to PQC algorithms by 2035.
:::
::::
::::

:::image src="images/25_post_quantum_threat_timeline.png" alt="Timeline diagram from 2024 to 2035 with three tracks: top track labeled 'Current State' shows RSA and ECDSA in green through 2024; middle track labeled 'Quantum Computer Progress' shows a curve from 'NISQ era (noisy, limited qubits)' in 2024 rising toward 'Cryptographically Relevant Quantum Computer (CRQC)' with a question mark around 2030–2035; bottom track labeled 'Migration Path' shows NIST FIPS 203/204/205 published in 2024, 'Hybrid deployment (classical + PQC)' from 2024–2030, and 'Full PQC migration' targeting 2035; a 'Harvest Now Decrypt Later' threat icon shows adversaries recording encrypted traffic today to decrypt with future quantum computers" caption="Post-quantum cryptography migration timeline: NIST finalized the first PQC standards (FIPS 203, 204, 205) in 2024. The NSA's CNSA 2.0 suite requires full migration of National Security Systems by 2035, before a cryptographically relevant quantum computer potentially becomes available." width=full
:::

:::notes
Post-quantum cryptography is the most significant cryptographic engineering challenge of the current decade. Quantum computers, leveraging quantum mechanical principles including superposition and entanglement, can run algorithms that are exponentially faster than classical computers for certain specific problem classes. Two quantum algorithms are of immediate concern for cryptography.

Shor's algorithm, developed by Peter Shor in 1994, solves the integer factorization problem and the Discrete Logarithm Problem in polynomial time on a quantum computer. This means that a sufficiently large, fault-tolerant quantum computer running Shor's algorithm could break RSA, ECDSA, ECDH, Diffie-Hellman, and every other asymmetric cryptographic algorithm deployed today, regardless of key size, in a matter of hours. The security of all currently deployed asymmetric cryptography depends on the classical computational hardness of these problems, which Shor's algorithm eliminates entirely in the quantum model.

Grover's algorithm, developed by Lov Grover in 1996, provides a quadratic speedup for unstructured database search, which translates to a square-root reduction in the effective key length for symmetric algorithms. AES-128 would have an effective 64-bit security level against Grover's algorithm, dangerously low. AES-256 would have an effective 128-bit security level, which remains adequate. SHA-256 would have an effective 128-bit pre-image resistance, borderline; SHA-384 and SHA-512 would retain adequate security. The practical implication for symmetric systems is to use AES-256 and SHA-384/SHA-512 for systems requiring long-term security, which provides quantum resistance for the symmetric layer.

NIST ran a multi-year Post-Quantum Cryptography (PQC) standardization competition beginning in 2016, evaluating 69 candidate algorithms from international teams. In August 2024, NIST published three final standards. FIPS 203 standardizes ML-KEM (Module Lattice Key Encapsulation Mechanism, based on the Kyber algorithm), which provides key exchange and key encapsulation using the hardness of the Module Learning With Errors (MLWE) problem on lattices. FIPS 204 standardizes ML-DSA (Module Lattice Digital Signature Algorithm, based on Dilithium), a lattice-based signature scheme. FIPS 205 standardizes SLH-DSA (Stateless Hash-based Digital Signature Algorithm, based on SPHINCS+), a conservative signature scheme whose security reduces to the properties of the hash function, with no lattice assumptions required.

The "Harvest Now Decrypt Later" (HNDL) attack is the most urgent practical threat. Nation-state adversaries and well-resourced attackers are recording encrypted network traffic today, particularly VPN traffic, government communications, and long-lived sensitive data, with the intention of decrypting it retroactively once a cryptographically relevant quantum computer (CRQC) becomes available, potentially within the next decade. This makes the PQC migration urgent even before quantum computers capable of breaking real-world cryptographic parameters are built. Data that must remain confidential for more than a decade is already at risk. The NSA's CNSA 2.0 directive mandates that National Security Systems complete migration to PQC algorithms for new hardware and software by 2025–2030, with full migration by 2035. Commercial organizations should begin hybrid deployments (running both classical and PQC algorithms in parallel) now, following guidance in NIST SP 800-227 (under development). Signal, Chrome (since version 116), Cloudflare and AWS have deployed hybrid classical-plus-post-quantum key exchange in production, combining X25519 with ML-KEM so that breaking a session requires breaking both the classical and the quantum-resistant algorithm.
:::

%%%
---
unit: Misconceptions
code: FAQ
title: "Common Misconceptions in Cryptography"
---
:::callout style=soft
Cryptography is frequently misunderstood by developers, executives, and security practitioners alike. Misapplying cryptographic concepts creates vulnerabilities that appear secure but fail under real attack conditions.
:::

:::table
| Misconception | Reality | Risk |
|---|---|---|
| "Encryption = security" | Encryption provides only confidentiality; integrity and authentication require additional primitives. | Attacker can modify encrypted data without knowledge of the key (bit-flipping attacks). |
| "My algorithm is secret, so it's secure" | Violates Kerckhoffs's principle. Proprietary ciphers lack peer review and are routinely broken. | Catastrophic failure upon algorithm exposure or reverse engineering. |
| "HTTPS means the site is safe" | HTTPS guarantees encryption and server identity; it does not validate the site's intent. Phishing sites use valid HTTPS certificates. | Users trust malicious sites because of padlock icon. |
| "Longer passwords are always safer" | Without key stretching, a 12-character password is nearly instantly crackable with GPU brute-force against simple SHA-256. | False sense of security without proper KDFs. |
| "Base64 encoding is encryption" | Base64 is an encoding scheme (losslessly reversible), not encryption. No secret key, no security. | Exposed secrets stored as Base64 in source code or config files. |
| "AES is broken if you use ECB mode" | AES itself is not broken; ECB mode misuses AES by processing blocks independently, leaking structure. | Structural pattern leakage; "ECB penguin" problem. |
:::

:::image src="images/25_crypto_misconceptions.png" alt="Six-panel myth-busting grid: each panel has a red 'MYTH' label on the top and a green 'REALITY' label on the bottom; panel 1: Myth 'HTTPS padlock = safe site' vs Reality 'HTTPS only encrypts the connection, not the site's intent'; panel 2: Myth 'Encryption protects integrity' vs Reality 'Need AEAD or HMAC for integrity'; panel 3: Myth 'Secret algorithm is more secure' vs Reality 'Kerckhoffs principle, algorithm must be public'; panel 4: Myth 'Base64 is encryption' vs Reality 'Base64 is reversible encoding with no key'; panel 5: Myth 'Long passwords are always safe' vs Reality 'Need KDF, SHA-256 cracked instantly on GPU'; panel 6: Myth 'AES is broken (ECB attack)' vs Reality 'ECB mode is broken, AES algorithm is secure'" caption="Six common cryptographic misconceptions: each combines a partial truth with a dangerous assumption. Cryptographic security requires understanding the precise boundaries of each primitive's security guarantee." width=full
:::

:::notes
Cryptographic misconceptions are dangerous precisely because they often contain a grain of truth that makes them plausible. Engineers and executives who do not specialize in security are particularly susceptible to reasoning by analogy from correct-sounding premises to incorrect conclusions. This slide addresses the most common and consequential misconceptions encountered in real deployments.

The most pervasive misconception is that encryption alone equals security. Encryption provides confidentiality: an attacker who intercepts ciphertext cannot read the plaintext without the key. But encryption by itself does not protect integrity. A Cipher Block Chaining (CBC) mode encryption scheme without authentication, for example, is vulnerable to bit-flipping attacks: an attacker who intercepts the ciphertext can flip specific bits in a ciphertext block, causing predictable, controlled changes in the decrypted plaintext without knowing the key. The 2011 BEAST attack (CVE-2011-3389) exploited predictable IV generation in TLS 1.0 CBC mode to recover session cookies through controlled plaintext injection and ciphertext observation, a demonstration of exactly this limitation. The fix requires AEAD modes (GCM) or explicit message authentication (HMAC) applied to the ciphertext before transmission, following the encrypt-then-MAC order (not MAC-then-encrypt, which is vulnerable in different ways).

The "HTTPS means safe" misconception is particularly harmful for end-user security education. HTTPS (TLS) provides encryption between the browser and the server, and authenticates the server's identity as the owner of a specific domain name. A phishing site at "secure-paypa1.com" can obtain a valid Let's Encrypt certificate and present a padlock in the browser. The connection is genuinely encrypted and the server is genuinely "secure-paypa1.com", but it is not "paypal.com," and the site's purpose is credential theft. The padlock authenticates the cryptographic channel, not the legitimacy of the website's purpose. Security awareness training must clearly distinguish between transport security (HTTPS) and trustworthiness of the server endpoint.

The Base64 misconception appears regularly in code reviews, where developers store API keys, JWT tokens, or password reset tokens in Base64 encoding and describe them as "obfuscated." Base64 is an RFC 4648 encoding scheme that converts binary data to ASCII text using a 64-character alphabet, it is trivially and completely reversible with no knowledge of any secret. echo "cGFzc3dvcmQ=" | base64 -d immediately returns "password." Any secret stored as Base64 is stored in plaintext from a security perspective. Similarly, "encryption" using XOR with a fixed key, ROT13, or similar simple transformations provides no security, these are encoding or obfuscation techniques, not cryptography.

The algorithm-secrecy misconception periodically re-emerges when vendors claim their proprietary encryption protects customer data. Real-world examples are abundant: the A5/1 cipher used in GSM mobile networks was kept secret but reverse-engineered within months of exposure; the Crypto-1 cipher used in MIFARE Classic smart cards (widely used in transit systems and access control) was kept proprietary but fully reverse-engineered by academic researchers and broken in practice, enabling cloning of billions of deployed cards (CVE-2008-1292). CSS (Content Scramble System) used to protect DVD content was similarly reverse-engineered after a leaked implementation, enabling the creation of DeCSS. Every proprietary cipher that has been exposed has been broken, a data point consistent with Kerckhoffs's principle that security must not depend on algorithm secrecy.
:::

%%%
---
unit: Compliance
code: CMP2
title: "Cryptography in Compliance Frameworks"
---
:::callout style=soft
Major regulatory and compliance frameworks mandate specific cryptographic controls. Understanding these requirements allows security engineers to implement cryptography that satisfies both technical and legal obligations simultaneously.
:::

:::table
| Framework | Relevant Control | Cryptographic Requirement |
|---|---|---|
| **PCI DSS 4.0** | Req 3.5, 4.2.1 | AES-256 for cardholder data at rest; TLS 1.2+ (1.3 preferred) for data in transit; no TLS 1.0/1.1 |
| **HIPAA Security Rule** | 45 CFR §164.312(a)(2)(iv) | Encryption of ePHI at rest and in transit (addressable, but effectively mandatory) |
| **GDPR** | Article 32 | "Encryption of personal data" explicitly listed as appropriate technical measure |
| **NIST SP 800-53 Rev 5** | SC-8, SC-12, SC-13, SC-28 | AES-256 (SC-13), FIPS-approved algorithms, key management per SP 800-57 |
| **ISO/IEC 27001:2022** | Annex A 8.24 | Cryptographic policy; key management lifecycle; algorithm selection guidance |
| **FedRAMP** | SC-28 | AES-256-GCM for data at rest; TLS 1.2+ for data in transit; FIPS 140-3 validated modules |
| **SOC 2 Type II** | CC6.7 (Logical access) | Encryption of data in transit and at rest; key management procedures audited |
:::

:::image src="images/25_compliance_framework_cryptography.png" alt="Radial diagram with 'Cryptographic Controls' in the center circle; seven framework badges radiate outward: PCI DSS 4.0 (payment cards), HIPAA (healthcare), GDPR (EU personal data), NIST SP 800-53 (federal), ISO 27001 (international), FedRAMP (cloud federal), SOC 2 (service orgs); each badge connects with a line to a cryptographic control cluster showing three consistent elements: AES-256 (data at rest), TLS 1.3 (data in transit), Key Mgmt (SP 800-57 / ISO 11770); a legend at the bottom notes that compliance requirements represent a floor, not a ceiling of security" caption="Cryptographic requirements across major compliance frameworks: while the specific controls and mandatory status vary, every major framework converges on AES-256 for data at rest, TLS 1.2+/1.3 for data in transit, and formal key management. Compliance is the security floor." width=full
:::

:::notes
Cryptographic compliance requirements are not merely bureaucratic mandates, they codify lessons learned from high-profile breaches into minimum-baseline controls that organizations must implement to avoid regulatory liability. Understanding which framework applies to your organization and what cryptographic controls it requires is a prerequisite for a compliant security architecture.

PCI DSS (Payment Card Industry Data Security Standard) Version 4.0, published by the PCI Security Standards Council and effective March 2025 for new requirements, is the primary framework for organizations that process, store, or transmit payment card data. Requirement 3.5 mandates that Primary Account Numbers (PANs) be rendered unreadable anywhere they are stored using one of: strong one-way hash functions (SHA-256 or greater), truncation, index tokens, or strong cryptography (AES-256). Requirement 4.2.1 mandates TLS 1.2 at minimum (with 1.3 strongly recommended) for all cardholder data transmitted over open, public networks, and explicitly prohibits the use of early SSL, TLS 1.0, and TLS 1.1 as "best practice" that became mandatory in PCI DSS 4.0. The PCI DSS does not specify an approved algorithm list independently but references NIST publications for algorithm selection.

HIPAA (Health Insurance Portability and Accountability Act) Security Rule classifies encryption of ePHI (electronic Protected Health Information) as an "addressable" rather than "required" implementation specification. However, "addressable" under HIPAA means that the covered entity must either implement the control or document why an equivalent alternative measure provides equivalent protection, in practice, regulators expect encryption to be present for ePHI at rest and in transit, and its absence must be justified in writing. OCR (Office for Civil Rights) enforcement actions have consistently found that encryption of ePHI at rest and in transit is the expected baseline. The 2015 Anthem breach (78.8 million records, no encryption at rest) and the 2020 Universal Health Services ransomware attack both resulted in significant regulatory scrutiny regarding ePHI encryption adequacy.

GDPR Article 32 requires "the pseudonymisation and encryption of personal data" as an example of appropriate technical measure, alongside other controls such as the ability to ensure ongoing confidentiality, integrity, availability, and resilience of processing systems. While GDPR does not mandate specific algorithms, supervisory authority enforcement guidance and the European Data Protection Board's (EDPB) recommendations consistently reference ENISA's (European Union Agency for Cybersecurity) algorithm recommendations, which align with NIST SP 800-131A in requiring AES-128 minimum, AES-256 preferred, RSA-2048 minimum transitioning to RSA-3072, and SHA-256 minimum.

Compliance is a minimum, not a ceiling. PCI DSS 4.0 permitting TLS 1.2 is not a recommendation to use it for new deployments, where TLS 1.3 is correct, and AES-128 meeting the FIPS minimum does not argue against AES-256 where performance allows. Implement compliance as the floor and exceed it where risk justifies.
:::

%%%
---
unit: Checkpoint
code: CHK
title: "Mid-Lecture Checkpoint: Cryptography Fundamentals"
---
:::callout style=soft
Pause and consolidate. Before we move to asymmetric cryptography, verify your understanding of the symmetric cryptography and hashing fundamentals covered so far.
:::

::::columns ratio=1:1
::col::
::::card heading="Knowledge Check Questions"
:::list style=tight
1. What two cryptographic properties does AES-256-GCM provide simultaneously that AES-256-CBC alone does not?
2. If an attacker steals a database of bcrypt hashes (cost=12) with per-user salts, can they use a rainbow table to crack them? Why or why not?
3. A developer uses `random.random()` in Python to generate AES session keys. What specific vulnerability does this introduce?
4. Explain why TLS 1.3 requires ECDHE key exchange instead of RSA key exchange for all sessions.
5. SHA-1 was deprecated not because it is "slow" but because of a specific cryptographic property failure. Which of the three hash properties failed first for SHA-1?
:::
::::
::col::
::::card heading="Concept Self-Assessment"
:::table
| Concept | Confident? | Review Slide |
|---|---|---|
| Kerckhoffs's Principle | ☐ Yes ☐ No | Slide 2 |
| Block vs. Stream Cipher | ☐ Yes ☐ No | Slide 5 |
| ECB mode weakness | ☐ Yes ☐ No | Slide 10 |
| CSPRNG vs. PRNG | ☐ Yes ☐ No | Slide 6 / Slide 19 |
| Hash function 3 properties | ☐ Yes ☐ No | Slide 7 |
| Salting purpose | ☐ Yes ☐ No | Slide 8 / Slide 15 |
| Argon2id vs bcrypt | ☐ Yes ☐ No | Slide 17 |
| HMAC vs raw hash | ☐ Yes ☐ No | Slide 12 |
| DH key exchange steps | ☐ Yes ☐ No | Slide 13 |
| Post-quantum threat | ☐ Yes ☐ No | Slide 20 |
:::
::::
::::

:::image src="images/25_checkpoint_cryptography.png" alt="Illustration of a student at a desk reviewing five labeled concept cards spread in front of them: 'Symmetric vs Asymmetric', 'Hash Properties', 'Key Entropy', 'Password KDFs', and 'CIA Triad Mapping'; a traffic-light self-assessment rubric in the top right shows red for 'Cannot explain without notes', yellow for 'Can explain with minor prompting', green for 'Can explain and give an example'; a clock in the corner shows a 5-minute review period; background shows a simplified mind-map connecting the five concept cards" caption="Checkpoint: five minutes of self-assessment on symmetric cryptography and hashing fundamentals. Use the concept self-assessment table to identify topics for review before proceeding to asymmetric cryptography." width=full
:::

:::notes
These questions review symmetric encryption, hash functions and key management, the prerequisites for the asymmetric cryptography covered next.

Let's walk through the answers. First: AES-256-GCM provides both confidentiality and integrity (authentication) in a single pass via the GHASH authenticator tag, whereas AES-256-CBC provides only confidentiality without integrity verification. An attacker can flip bits in CBC ciphertext and produce different but apparently valid plaintext, GCM detects this via the authentication tag. Second: No, a rainbow table cannot help against properly salted bcrypt hashes. Rainbow tables precompute all (password → hash) mappings without knowing the salt. With a unique, random salt for each user, even the same password produces a completely different bcrypt hash for each user, making precomputed tables useless. The attacker must brute-force each user's hash individually. Third: Python's random.random() uses the Mersenne Twister, a PRNG whose internal state can be reconstructed from 624 consecutive outputs. AES session keys generated with it are predictable to an adversary who observes enough outputs, enabling them to enumerate and test the small space of likely keys. The correct choice is secrets.token_bytes() or os.urandom(). Fourth: TLS 1.3 requires ECDHE (ephemeral) key exchange to ensure perfect forward secrecy. With static RSA key exchange (TLS 1.2), an attacker recording encrypted sessions could retroactively decrypt them after obtaining the server's RSA private key through any means. ECDHE generates fresh key pairs per session and discards them immediately, ensuring no past session can be decrypted even with the server's long-term private key. Fifth: SHA-1 failed collision resistance first, the 2017 SHAttered attack produced two PDF files with the same SHA-1 hash at a cost of approximately 110 GPU-years. Collision resistance is the most stringent and first-to-fail of the three hash properties, as the birthday paradox reduces the search space to $2^{n/2}$ for an $n$-bit hash (approximately $2^{80}$ for SHA-1), which modern GPU farms can reach in feasible time and cost.

:::

%%%
---
unit: Summary
code: SUM
title: Cryptography Basics Summary
---
:::pullquote
Confidentiality and integrity are two sides of the same coin, but they require different mathematical tools. Encryption hides the data; hashing verifies it hasn't changed.
:::

:::list style=chips
- Kerckhoffs's Principle (Algorithm Openness)
- Symmetric Ciphers (Block vs. Stream)
- Cryptographic Key Entropy (CSPRNG)
- Hash Functions (Pre-image & Collision Resistance)
- Salted Password Hashing (Argon2, bcrypt)
:::

:::image src="images/25_summary_cryptography_primitives.png" alt="Summary mind-map diagram: central node labeled 'Cryptography Basics' branches outward to five leaf clusters: (1) Kerckhoffs's Principle, public algorithm, secret key, open standards; (2) Symmetric Ciphers, AES-256 block cipher (FIPS 197) and ChaCha20 stream cipher (RFC 8439); (3) Key Entropy, CSPRNG (SP 800-90A), keyspace 2^256, HSM storage (FIPS 140-3); (4) Hash Functions, SHA-256 (FIPS 180-4) and SHA-3 (FIPS 202) with three core properties listed; (5) Password Hashing, Argon2id (RFC 9106) and bcrypt with per-user salt icon; connecting lines show which CIA Triad property each cluster enforces" caption="Class 25 concept map: five foundational cryptographic primitives and their governing standards. Each maps to a specific security control within the CIA Triad and compliance frameworks including NIST SP 800-53 and ISO/IEC 27001." width=full
:::

:::notes
In today's lecture, we established the foundational building blocks of modern cryptography. We learned that modern cryptography relies on the mathematical complexity of problems such as prime factorization, the Discrete Logarithm Problem, and the Elliptic Curve Discrete Logarithm Problem rather than algorithm secrecy, a principle articulated by Auguste Kerckhoffs in 1883 and formalized in modern standards including NIST SP 800-175B and ISO/IEC 18033. Every algorithm discussed today is publicly defined and subject to decades of international cryptanalytic scrutiny; their security is mathematical, not obscurity-dependent. Closed, proprietary algorithms consistently fail when exposed, as illustrated by the rapid defeat of CSS (Content Scramble System) used for DVD copy protection and the A5/1 cipher used in early GSM mobile networks.

We explored symmetric encryption, comparing block ciphers and stream ciphers. AES (FIPS 197) is the global standard for bulk encryption, operating in modes including CBC (NIST SP 800-38A) and GCM (NIST SP 800-38D). ChaCha20 (RFC 8439) provides a high-performance alternative stream cipher for environments lacking hardware AES acceleration, now mandated alongside AES-GCM in TLS 1.3. We analyzed why mode selection is as critical as algorithm selection, ECB mode's failure to mask data patterns produced the "ECB penguin" demonstration, and the deprecation of RC4 (CVE-2015-2808) after the POODLE and BEAST attacks demonstrated that implementation-level vulnerabilities can undermine theoretically strong key lengths.

We examined cryptographic key entropy and the CSPRNG requirement (NIST SP 800-90A). The Debian OpenSSL entropy bug (CVE-2008-0166) stands as a cautionary case study demonstrating that a single implementation error in a random number generator can reduce a 2048-bit RSA key's security to 15 bits, rendering the strongest key lengths meaningless. Key lifecycle management under NIST SP 800-57 and storage in FIPS 140-3 certified HSMs are operational requirements, not optional enhancements.

We studied cryptographic hash functions and their three core security properties, pre-image resistance, second pre-image resistance, and collision resistance. The deprecation of MD5 (collision attacks demonstrated 2004; CVE-2004-2761) and SHA-1 (practical "SHAttered" collision 2017) illustrates that hash function security must be continuously re-evaluated. Current standards mandate SHA-256 (FIPS 180-4) or SHA-3 (FIPS 202) for new systems.

We analyzed password storage as a case study in correct primitive selection. Real-world breaches, LinkedIn (2012, 117 million unsalted SHA-1 hashes), RockYou (2009, 32 million plaintext passwords), and Adobe (2013, 153 million poorly encrypted credentials), demonstrate that applying encryption instead of salted hashing, or using fast hashes instead of memory-hard KDFs, has enabled mass credential compromise. NIST SP 800-63B mandates Argon2id (RFC 9106) or equivalent memory-hard functions with per-user salts.

In the next lecture, we solve the key distribution problem left open by symmetric cryptography. Asymmetric cryptography, and specifically the Diffie-Hellman key exchange protocol and the RSA cryptosystem, allow two parties who have never met to agree on a shared secret over a monitored public channel, enabling the HTTPS and TLS-encrypted internet communications that secure global commerce and communications today.
:::
