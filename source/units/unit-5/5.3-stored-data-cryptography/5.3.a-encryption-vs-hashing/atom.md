# 5.3.a, Encryption vs. hashing

> **Unit 5 · 5.3 Protecting Stored Data with Cryptography**
> **AP Learning Objective(s):** 5.3.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Distinguish encryption from hashing, explain the one-way
property that makes them suited for different jobs, and choose the correct control when a
scenario requires either confidentiality or integrity verification.

## Lesson
When a system needs to protect stored data, engineers reach for two very different tools:
encryption and hashing. On the surface both produce an unreadable-looking blob of bytes from
readable input. Below the surface they have opposite goals, and choosing the wrong one is a
common and costly mistake.

**What encryption does.** Encryption converts plaintext into ciphertext using a key. Given
the same key (or a matching key pair), the process is fully reversible, the ciphertext can
be decrypted back to the original plaintext. That reversibility is the whole point.
Encryption protects confidentiality: even if an attacker reads the ciphertext from disk or
over the wire, they learn nothing useful unless they also possess the key. A classic storage
example is a laptop with full-disk encryption. If the laptop is stolen, the thief sees only
random bytes; the authorized user, who knows the key, sees the normal filesystem.

**What hashing does.** A hash function takes an input of any size and produces a fixed-size
output called a digest (also called a hash or a checksum). The process is intentionally
one-way: there is no algorithm to reverse it. If someone hands you the digest
`2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824`, you cannot recover
the original string "hello" without guessing or brute force. Hash functions are designed so
that two slightly different inputs produce completely different digests, a property called
the avalanche effect. Hashing protects integrity: you store the digest alongside data and
recompute it later to detect any modification.

**The key question: do you need to get the original back?** That single question separates
the two controls. Passwords are the clearest example. A website needs to know whether your
login password matches what you registered, but it has no legitimate reason to ever see your
password again. If the site stored the password encrypted, a database breach plus key
compromise means full exposure of every user's password. Instead, sites store a hash of the
password (plus a salt, covered in 5.3.b). At login they hash your input and compare digests;
the original is never recovered. Contrast this with a payroll file: the company must be able
to read employee salary data whenever payroll runs, so it stores the data encrypted, not
hashed.

**Salting prevents precomputed attacks.** A naive hash of a common password like "password"
produces the same digest every time. Attackers precompute enormous tables of password-to-hash
pairs (rainbow tables) and look up any digest instantly. A salt is a random value appended
to the password before hashing, stored alongside the digest. Even if two users pick the same
password, their salts differ, so their digests differ, defeating the lookup table. Salted
hashing with a purpose-built algorithm (such as bcrypt, scrypt, or Argon2) is the accepted
standard for password storage. The coding problem in `problem/` has you implement salted
SHA-256 hashing and a matching verify function so you can see the mechanism directly.

**Digest algorithms in practice.** The SHA-2 family (SHA-256, SHA-512) is the current
standard for general-purpose hashing. MD5 and SHA-1 are deprecated for security use: both
have known collision vulnerabilities, meaning attackers can produce two different inputs with
the same digest, undermining integrity guarantees. For passwords, purpose-built slow
algorithms are preferred because their deliberate computational cost makes brute-force
guessing expensive even with modern hardware.

**Confusion to avoid.** Encoding (Base64, hex) is not encryption and not hashing: it is a
lossless format change, trivially reversed, and provides no security. Compression is not
encryption: ZIP files are not encrypted unless the format explicitly adds a cipher. Both are
common misconceptions that have led to real breaches.

**Where these controls live in the AP framework.** LO 5.3.A asks you to select
cryptographic controls appropriate to a given scenario. The decision tree is: if you need
confidentiality and must recover the original data, use encryption; if you need to verify
integrity or store a credential without ever recovering the original, use a hash. The
simulation (the simulation) presents a series of storage scenarios and asks you to classify each;
practice that classification until it feels automatic.

## Key terms
- **Encryption**, a reversible transformation of data using a key; protects confidentiality.
- **Decryption**, the reverse of encryption; requires the correct key.
- **Hash function**, a one-way function that maps any input to a fixed-size digest.
- **Digest**, the fixed-size output of a hash function (also called a hash or checksum).
- **Salt**, a random value mixed into input before hashing to defeat precomputed table attacks.
- **Rainbow table**, a precomputed table mapping common inputs to their digests, used for hash cracking.
- **Avalanche effect**, property where a tiny input change produces a drastically different digest.
- **Collision**, two distinct inputs that produce the same digest; a fatal weakness in a hash function.

## Common misconceptions
- "I can hash a file and recover it later." → Hashing is one-way; the digest cannot be reversed.
- "Encoding (Base64) is a form of encryption." → Encoding is a reversible format change with no key; it provides zero confidentiality.
- "MD5 is fine for passwords." → MD5 has known collision weaknesses and is very fast to brute-force; use bcrypt/scrypt/Argon2 for passwords.
- "Encryption and hashing both protect the same thing." → Encryption protects confidentiality (you need the original back); hashing protects integrity/authentication (you never need the original back).

## Try it
- **Simulation:** Classify eight storage scenarios as
  requiring encryption or hashing and reach a score of 6/8.
- **Coding problem:** Implement salted SHA-256 hashing and a constant-time
  verify function, then confirm it correctly accepts matching passwords and rejects mismatches.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (6.858 Computer Systems Security, lecture notes on cryptographic primitives), rebuilt as original prose above.
- Reference: NIST FIPS 180-4 (Secure Hash Standard), see vendor/web/nist/ notes.
- Practice: SANS Cyber Aces Module 3 (cryptography exercises), rebuilt locally as the simulation and problem/.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`
