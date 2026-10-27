# 5.3.b, Symmetric encryption and key management

> **Unit 5 · 5.3 Protecting Stored Data with Cryptography**
> **AP Learning Objective(s):** 5.3.A, 5.3.B
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain the mechanics of symmetric encryption, differentiate between ECB and secure modes of operation (like CBC and GCM), and describe the key lifecycle management principles necessary to protect keys from compromise.

## Lesson
When organizations need to protect the confidentiality of stored data (data-at-rest), they use symmetric cryptography. **Symmetric encryption** uses a single secret key for both encryption and decryption. Because the same key does both jobs, it must be kept secret; if an unauthorized party obtains the key, the protection is completely lost.

### Symmetric Ciphers and AES
Modern symmetric ciphers are **block ciphers**, which encrypt plaintext in fixed-size blocks (typically 128 bits). The industry standard for symmetric encryption is the **Advanced Encryption Standard (AES)**, established by NIST in 2001 (FIPS 197). AES replaced the outdated Data Encryption Standard (DES), which was vulnerable to brute-force attacks due to its short 56-bit key length. AES supports key sizes of 128, 192, and 256 bits, all of which are currently considered computationally secure against brute-force attacks.

### Modes of Operation
Because files and database fields are usually larger than a single 128-bit block, block ciphers require a **mode of operation** to encrypt arbitrary lengths of data. How blocks are chained together drastically affects security.

1. **Electronic Codebook (ECB) Mode (Insecure):** ECB mode encrypts each block of plaintext independently with the same key. If two blocks of plaintext are identical, their ciphertexts will be identical. This leaks patterns in the underlying data. The classic example is encrypting a bitmap image in ECB mode: the boundaries of the image remain clearly visible in the ciphertext. **ECB mode should never be used for multi-block data.**
2. **Cipher Block Chaining (CBC) Mode:** CBC mode resolves ECB's pattern leakage by XORing each plaintext block with the previous ciphertext block before encrypting it. To encrypt the first block, we use a random, non-secret block of data called an **Initialization Vector (IV)**. The IV must be unique for every encryption operation and unpredictable. If the same IV is reused with the same key to encrypt different plaintexts, an attacker can detect if the messages start with the same data.
3. **Galois/Counter Mode (GCM):** GCM mode turns a block cipher into a stream cipher by encrypting an incrementing counter and XORing the result with the plaintext. Importantly, GCM is an **Authenticated Encryption with Associated Data (AEAD)** mode. It provides both confidentiality and integrity verification (via an authentication tag). If an attacker tampers with the ciphertext, decryption fails.

### Symmetric Key Management Lifecycle
A cryptographic system is only as secure as its key management. The key management lifecycle dictates how keys are generated, stored, distributed, rotated, and retired.

```
       +------------+
       | Generate   | (CSPRNG, high entropy)
       +-----+------+
             |
             v
       +------------+
       |   Store    | (HSM, Secrets Manager, KEK/DEK)
       +-----+------+
             |
             v
       +------------+
       |   Rotate   | (Scheduled replacement)
       +-----+------+
             |
             v
       +------------+
       |   Retire   | (Cryptographic erasure)
       +------------+
```

1. **Generation:** Keys must be generated using a **Cryptographically Secure Pseudo-Random Number Generator (CSPRNG)** to ensure they have maximum entropy (unpredictability). Standard random libraries (like Python's `random` or C's `rand()`) use predictable algorithms and must never be used to generate keys. Instead, use OS-level entropy sources (e.g., `/dev/urandom` or Python's `secrets` module).
2. **Storage:** Keys must never be hardcoded in source code or stored in plaintext configuration files. Hardcoded keys are easily leaked via version control systems (like Git). Instead, keys should be stored in:
   - **Secrets Managers:** Dedicated software (e.g., HashiCorp Vault, AWS Secrets Manager) that encrypts keys at rest and controls access via role-based policies.
   - **Hardware Security Modules (HSMs):** Dedicated physical devices that perform cryptographic operations internally. Keys generated inside an HSM never leave the hardware in plaintext.
3. **Key wrapping (Envelope Encryption):** To manage large numbers of keys, systems use a hierarchy:
   - **Data Encryption Key (DEK):** A key used to encrypt the actual data (e.g., database columns).
   - **Key Encryption Key (KEK):** A key used to encrypt (wrap) the DEK.
   The wrapped DEK is stored next to the encrypted data, while the KEK is securely stored in an HSM or secrets manager. To decrypt data, the system sends the wrapped DEK to the HSM to be unwrapped by the KEK, retrieves the plaintext DEK, and decrypts the data.
4. **Rotation:** Keys should be rotated (replaced) regularly to limit the amount of data exposed if a single key is compromised. When a key is rotated, new data is encrypted with the new key.
5. **Retirement & Destruction:** When a key is retired, it must be securely destroyed (e.g., zeroed out in memory or deleted from the HSM). This is known as **cryptographic erasure**: without the key, the ciphertext is permanently unrecoverable.

## Key terms
- **Symmetric encryption**, a cryptographic system where the same key is used for both encryption and decryption.
- **Advanced Encryption Standard (AES)**, the standard symmetric block cipher used globally, supporting 128, 192, and 256-bit keys.
- **Block cipher**, a cipher that encrypts data in fixed-size blocks (e.g., 128 bits for AES).
- **Mode of operation**, an algorithm that defines how a block cipher encrypts data larger than a single block.
- **Initialization Vector (IV)**, a random block of data used to seed the first block of encryption in modes like CBC, ensuring unique ciphertexts.
- **CSPRNG**, Cryptographically Secure Pseudo-Random Number Generator; a generator that produces unpredictable numbers suitable for cryptography.
- **Key wrapping**, the process of encrypting a Data Encryption Key (DEK) with a Key Encryption Key (KEK) for secure storage.
- **HSM (Hardware Security Module)**, a physical device designed to securely generate, store, and manage cryptographic keys.

## Common misconceptions
- "Hardcoding a key in a private Git repository is safe." → Private repositories can be compromised, and any developer with clone access can copy the key. Keys should be stored in environment variables or secrets managers.
- "Reusing an IV is fine as long as the key is secret." → Reusing an IV allows attackers to perform frequency analysis or detect patterns, undermining confidentiality.
- "AES-ECB is secure because AES is strong." → Even with a strong cipher like AES, ECB mode encrypts identical plaintext blocks into identical ciphertext blocks, exposing data patterns.

## Try it
- **Simulation:** Configure encryption modes to protect sensitive medical images and inspect the pattern leakage of ECB vs CBC.
- **Coding problem:** Implement a key-wrapping helper that generates symmetric keys and encrypts/decrypts DEKs using KEKs via counter-mode keystream generation.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (6.858 Computer Systems Security, symmetric cryptography design), rebuilt locally.
- Reference: NIST SP 800-38A (Recommendation for Block Cipher Modes of Operation), rebuilt locally.
- Practice: SANS Cyber Aces Module 3 (key management principles), rebuilt as the simulation and problem/.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`
