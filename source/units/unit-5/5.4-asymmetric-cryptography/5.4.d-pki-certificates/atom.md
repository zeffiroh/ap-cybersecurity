# 5.4.d, PKI and digital certificates

> **Unit 5 · 5.4 Asymmetric Cryptography**
> **AP Learning Objective(s):** 5.4.B, 5.4.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain what a digital certificate contains and why, describe how a
client walks a certificate chain up to a trusted root to decide whether to trust a public key, and
identify why and how certificates get revoked before their stated expiration.

## Lesson
5.4.a ended with a bootstrap problem it deliberately left unsolved: asymmetric cryptography lets you
hand your public key to anyone, but that only helps if the person receiving it can be sure the key
really belongs to who it claims. If an attacker can slip you a different public key while claiming
to be your bank, every guarantee from 5.4.a-5.4.c collapses, you would faithfully encrypt your
password with the attacker's key, or faithfully "verify" a signature the attacker forged with a
private key you never actually confirmed belonged to your bank. Public-key infrastructure (PKI) is
the system built to solve exactly this: not the math of key pairs and signatures, but the *trust*
problem of binding a specific public key to a specific real-world identity.

**What a certificate actually is.** A digital certificate is a small, signed document that binds a
public key to an identity. At minimum it contains: the **subject** (the identity being vouched for, a domain name, an organization, a person), the **subject's public key**, the **issuer** (who is
vouching for this binding), a **validity period** (`not_before` / `not_after` dates), and, this is
the part that makes the whole thing trustworthy, a **digital signature over all of those fields,
produced by the issuer's private key**. That last piece is exactly the sign/verify operation from
5.4.c: the issuer hashes the certificate's fields and signs the digest. Anyone holding the issuer's
public key can verify that signature and be confident the certificate has not been altered since the
issuer vouched for it.

**Who does the vouching: the chain of trust.** The issuer of a certificate is a Certificate Authority
(CA), an organization whose entire business is verifying identities and signing certificates that
bind public keys to them. But this just pushes the trust question up one level: why should you trust
the CA's public key? PKI answers this with a hierarchy rather than a single flat list of trusted
identities:

- A **root CA** sits at the top. Its certificate is self-signed (issuer and subject are the same
  entity), and its public key is pre-installed in your operating system's or browser's **trust
  store**, a curated list the OS/browser vendor maintains and updates, verified out-of-band (you
  did not personally vet the root CA; you trusted the OS vendor's vetting process when you installed
  it).
- The root CA rarely signs end-entity certificates directly (its private key is kept extremely well
  protected, often offline). Instead it signs **intermediate CA** certificates, delegating signing
  authority.
- The intermediate CA signs the actual **leaf certificate**, the one for `www.yourbank.example`
  that gets presented to your browser.

This produces a **chain**: leaf -> intermediate -> root. To validate it, a client verifies each
certificate's signature using the *next* certificate's public key, the leaf's signature is checked
against the intermediate's public key, the intermediate's signature is checked against the root's
public key, and confirms the chain terminates at a root already present in the trust store. If
every link verifies and the chain reaches a pre-trusted root, the client accepts the leaf's public
key as genuinely belonging to the claimed subject. This is precisely what the `problem/` exercise
implements: `validate_chain()` walks a chain leaf-first, checks that each certificate's `issuer`
field matches the next certificate's `subject`, verifies each signature with the issuer's public
key, and confirms the top of the chain is a member of a supplied `trusted_roots` store.

**What else gets checked along the way.** Beyond the signature chain, a client checks each
certificate's **validity window** (a certificate presented before `not_before` or after `not_after`
is rejected, this is why an expired certificate throws a browser warning) and **revocation status**.
Revocation exists because a certificate's stated expiration date might be years away, but the
situation that made it trustworthy can change immediately, most commonly, the subject's private key
is compromised (stolen, leaked, or the server hosting it is breached). A CA cannot "un-sign" an
already-issued certificate, so instead it publishes that the certificate should no longer be
trusted, via a **Certificate Revocation List (CRL)**, a periodically updated, CA-signed list of
revoked certificate serial numbers a client can download and check against, or via the **Online
Certificate Status Protocol (OCSP)**, where a client asks a CA-operated responder in real time
"is this specific certificate still good?" and gets a signed yes/no answer without downloading an
entire list. Either mechanism lets trust be withdrawn before the stated expiration date.

**A common failure mode.** A **self-signed certificate**, one where subject and issuer are the same
entity, and it is not present in the trust store, will fail chain validation, correctly: there is no
independent third party vouching for the binding, so a browser has no basis to trust it (this is why
browsers show a hard warning for self-signed certs on public sites, though self-signed certs are
routinely and safely used inside private/internal networks where the operator controls the trust
store directly). An **expired** or **revoked** certificate fails validation for a different reason:
the binding may once have been trustworthy, but the client has explicit information that it no
longer is.

Open the simulation to inspect several certificate chains, valid, expired, revoked, self-signed
untrusted, and one with a broken issuer/subject link, and decide TRUST or REJECT for each. The
coding problem in `problem/` has you implement the chain-walking validation logic directly, reusing
the small-number RSA sign/verify math from 5.4.b/5.4.c as the signature primitive.

## Key terms
- **Digital certificate**, a signed document binding a public key to a subject identity, issued and
  signed by a Certificate Authority.
- **Certificate Authority (CA)**, an organization that verifies identities and signs certificates
  vouching for the binding between a subject and its public key.
- **Root CA**, a CA whose self-signed certificate is pre-installed in an OS/browser trust store and
  trusted as the ultimate anchor of a chain.
- **Intermediate CA**, a CA whose certificate is signed by a root (or another intermediate) and
  which signs end-entity (leaf) certificates.
- **Chain of trust**, the sequence of signed certificates from a leaf up through intermediates to a
  trusted root, each link verified with the next certificate's public key.
- **Trust store**, the curated set of root CA public keys an OS or browser trusts out of the box.
- **Certificate Revocation List (CRL)**, a CA-signed, periodically updated list of revoked
  certificate serial numbers.
- **OCSP**, Online Certificate Status Protocol; a real-time query/response check of one
  certificate's revocation status against a CA-operated responder.

## Common misconceptions
- "A certificate proves the website is trustworthy/legitimate in a business sense." → It only proves
  that a CA verified the binding between the stated subject (usually just a domain name) and the
  public key presented. It says nothing about the site's content, intent, or safety.
- "Any self-signed certificate is inherently insecure." → Self-signed certificates use the same
  cryptography and can be perfectly secure once distributed and trusted through some other channel
  (e.g. manually installed on an internal network); the issue is that a random visitor's browser has
  no independent reason to trust it.
- "Revocation and expiration are the same thing." → Expiration is a scheduled, built-in end to a
  certificate's validity window. Revocation is an unscheduled, active withdrawal of trust before that
  date, typically because the private key was compromised.
- "The whole chain is checked with one signature." → Each certificate in the chain is signed and
  verified independently, using the public key of the certificate directly above it in the chain.

## Try it
- **Simulation:** Inspect several certificate chains and decide
  TRUST or REJECT for each scenario (valid, expired, revoked, untrusted self-signed root, broken
  chain link), reaching the target score.
- **Coding problem:** Implement `validate_chain()` (plus `compute_digest()`,
  `rsa_sign()`, `rsa_verify()`) to walk a leaf-to-root certificate chain and return whether it is
  valid, and why not if it isn't.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (6.875 / cryptography lectures), rebuilt as original prose above; see
  `vendor/web/mit-ocw/`.
- Reference: NIST SP 800-32 (Introduction to Public Key Technology and the Federal PKI
  Infrastructure).
- Practice: GeeksforGeeks (Public Key Infrastructure overview), rebuilt locally as the simulation
  interactive cases.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
