# 1.2.c, Strengthening authentication: length/complexity, randomness, MFA

> **Unit 1 · 1.2 Suspicious Wi-Fi Login**
> **AP Learning Objective(s):** 1.2.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain why password length and randomness are the primary drivers
of authentication strength, describe how Time-based One-Time Passwords work as a second factor,
and implement a TOTP verifier using only the standard library.

## Lesson
The previous atom showed what makes a password weak. This skill asks the harder question: what
makes authentication genuinely strong? The answer has three layers, length, randomness, and a
second factor, and understanding all three changes how you design and evaluate authentication
systems.

**Why length dominates complexity.** When a password is chosen uniformly at random from an
alphabet of size A and has length L, there are A^L possible passwords. Doubling the alphabet size
(say from 26 lowercase letters to 52 mixed-case letters) squares the space, adding one factor of
A. But increasing the length by one multiplies the space by another full factor of A. In practice,
every additional character matters more than adding a new character class. A 20-character
passphrase of common English words is exponentially harder to brute-force than a 10-character
mixed-case-plus-symbol password, even though the passphrase might "fail" a naive complexity
policy. NIST SP 800-63B (the federal digital identity guideline) explicitly moved away from
mandatory complexity rules for this reason: they push users toward predictable patterns
(`Password1!`) while giving a false sense of security.

**What randomness means in practice.** A password is only as strong as the process that generated
it. A human who picks "their dog's name plus birth year" is not drawing uniformly at random from
the available character space, they are drawing from a much smaller space of human-memorable
choices, which attackers model explicitly. True randomness means using a cryptographically secure
random number generator (Python's `secrets` module, a hardware RNG, or a password manager) to
generate a string the human could never have invented. Random passphrases (four or more words
sampled from a large wordlist) combine memorability with genuine entropy.

**The fundamental limit of passwords alone.** Even a genuinely random, long password is a single
secret that, once compromised, gives an attacker permanent access. Phishing, keyloggers, database
breaches, and shoulder surfing can all expose a password without breaking it
cryptographically. This is why modern authentication adds a second factor.

**Multi-Factor Authentication (MFA).** MFA requires a user to prove identity with two or more
factors from distinct categories:
- Something you **know**, a password or PIN
- Something you **have**, a hardware token, authenticator app, or SMS code
- Something you **are**, a biometric (fingerprint, face)

An attacker who steals only the password cannot authenticate unless they also control the second
factor. In practice, the most common second factor for web and Wi-Fi applications is a
Time-based One-Time Password (TOTP).

**How TOTP works.** TOTP is defined in RFC 6238, built on top of HMAC-based OTP (HOTP, RFC 4226).
The algorithm is deterministic and offline:

1. The user and server share a secret key K (a random byte string, usually 20 bytes).
2. Both compute the current time step T = floor(unix_timestamp / 30). The step changes every 30
   seconds so both parties are synchronized without communicating.
3. Both compute HMAC-SHA1(K, T encoded as an 8-byte big-endian integer).
4. A "dynamic truncation" extracts 4 bytes from the 20-byte HMAC output.
5. A modulo operation reduces those 4 bytes to a 6-digit number.
6. The server compares its computed code to the code the user submits. If they match, the
   second factor is verified.

The verifier only accepts codes for the current time step (no window drift). Because the step
changes every 30 seconds and the code space is only one million values, a code is valid for at
most 30 seconds and then becomes permanently invalid. An attacker who intercepts a valid code
cannot reuse it after the window closes.

**Why the shared secret matters.** The security of TOTP rests on the secret key K being known
only to the server and the authenticator app. During enrollment, the server generates K securely,
stores it, and transmits it to the app exactly once (usually via a QR code over HTTPS). After
that, K never travels over the network. The server's TOTP database is a high-value target, if K
values are leaked, an attacker can compute valid codes for any time step.

**Authenticator apps and hardware tokens.** Apps like Google Authenticator (open-source clone:
andOTP) and hardware tokens (YubiKey TOTP mode) implement the same algorithm. The app stores K
locally and computes the current code without any network connection, which is why TOTP works
even in airplane mode. This matters for offline environments like the school Wi-Fi scenario in
this unit.

**The coding problem.** The problem for this skill asks you to implement the TOTP verifier: given
a shared secret K (hex-encoded), a 6-digit code string, and a Unix timestamp t, return True if
the code matches what TOTP would produce for the 30-second step containing t. This requires
`hmac` and `hashlib` from the standard library and no external packages. Implementing it from
scratch gives you a concrete understanding of exactly what an authenticator app computes every
time you open it.

## Key terms
- **MFA (Multi-Factor Authentication)**, requiring two or more factors from distinct categories
  (know/have/are) before granting access.
- **TOTP (Time-based One-Time Password)**, a 6-digit code derived from HMAC-SHA1(secret, time_step),
  valid for one 30-second window, defined in RFC 6238.
- **HMAC (Hash-based Message Authentication Code)**, a construction that uses a cryptographic
  hash function and a secret key to produce an authentication tag.
- **Time step**, the integer floor(unix_timestamp / 30); changes every 30 seconds and
  synchronizes the server and authenticator without communication.
- **Dynamic truncation**, the RFC 4226 method of extracting 4 bytes from a 20-byte HMAC-SHA1
  output to produce a numeric OTP.
- **Entropy**, measure of unpredictability; in passwords, increases with length and randomness;
  in TOTP, comes from the secret key and the short validity window.

## Common misconceptions
- "MFA is unbreakable." → TOTP codes can be phished in real-time (the attacker relays the code
  immediately). MFA raises the bar dramatically but does not eliminate social engineering.
- "SMS codes and TOTP are the same security level." → SMS codes can be intercepted via SIM
  swapping; TOTP codes are computed locally and never sent over the phone network.
- "A password manager makes passwords weaker because one breach exposes everything." → A good
  password manager encrypts the vault with a master password; losing the vault file without the
  master key reveals nothing. The tradeoff is worthwhile for the unique-per-site passwords it
  enables.

## Try it
- **Simulation:** Work through an MFA enrollment and login flow,
  computing what the TOTP code should be for a given time step, and reach 4 correct to meet the
  objective.
- **Coding problem:** Implement `solve(secret, code, t)` verifying a 6-digit TOTP
  using stdlib hmac/hashlib, 30-second step, current step only.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-63B (Digital Identity Guidelines), length, complexity, and MFA
  recommendations; rebuilt as original prose above.
- Reference: NIST SP 800-63B Section 5.1 (memorized secrets) and RFC 6238 (TOTP), algorithm
  specification used in the coding problem.
- Practice: Cybrary MFA module exercises, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources -> `vendor/repos/LetsDefend-Free-Cybersecurity-Resources`.
