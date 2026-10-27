# 4.2.b, Multi-factor authentication

> **Unit 4 · 4.2 Authentication**
> **AP Learning Objective(s):** 4.2.A, 4.2.B
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain why single-factor (password-only) login is insufficient,
classify a described authentication method into its factor category, judge whether a login
attempt satisfies true multi-factor authentication, and identify which MFA methods are
phishing-resistant versus phishable.

## Lesson
A password is a single piece of evidence: if an attacker learns it, through phishing, a data
breach, or a guessed weak password, they can log in exactly as the real user, with no further
obstacle. Multi-factor authentication (MFA) closes this gap by requiring proof from two or more
independent *categories* of evidence before granting access. The categories matter more than the
count: security professionals group every authentication method into one of three factors, **something you know** (a password, a PIN, the answer to a security question), **something you
have** (a phone that receives a code, a hardware security key, a smart card), and **something you
are** (a fingerprint, a face scan, another biometric trait). True MFA requires at least two of
these *different* categories. Entering a password and then a second password is still only
"something you know" twice, it is not MFA, even though it feels like an extra step. This is one
of the most common misunderstandings students bring into a security role, so hold onto the
category framework, not the step count.

**Why single-factor fails.** Passwords are reused across sites, phished with convincing fake login
pages, guessed via credential-stuffing bots that try billions of breached password/username pairs,
and sometimes simply written down. Once a password leaks, it grants full access forever until
changed. MFA does not make passwords unnecessary, but it means a leaked password alone is not
enough, the attacker also needs the second factor, which is dramatically harder to steal at scale.

**Common MFA methods, from weakest to strongest.** *SMS one-time codes* text a numeric code to the
user's phone number. This is better than nothing, but the phone *number* is not tightly bound to
the phone itself: an attacker can perform a **SIM swap**, tricking or bribing a mobile carrier into
porting the victim's number to an attacker-controlled SIM, after which all SMS codes arrive on the
attacker's device. SMS codes can also be relayed through adversary-in-the-middle phishing kits that
sit between the victim and the real site, capturing the code in real time. *Authenticator-app codes*
(TOTP, Time-based One-Time Password, and its relative HOTP, HMAC-based One-Time Password) generate
a new six-digit code every 30 seconds from a shared secret stored only on the device; this removes
the SIM-swap risk but the code can still be phished and relayed the same way SMS can, because the
user is still capable of typing it into a fake site. *Push notifications* send an approve/deny
prompt to a registered app, convenient, but vulnerable to **MFA fatigue** (also called
**push bombing**): an attacker who already has the password repeatedly triggers login attempts
until an annoyed or confused user taps "Approve" just to make the notifications stop. *Hardware
security keys* using the **FIDO2/WebAuthn** standard (and its predecessor U2F) are considered
**phishing-resistant**: the key performs a cryptographic handshake tied to the exact website
domain, so even a perfect-looking fake login page cannot obtain a valid response, the key simply
will not respond to the wrong domain. *Biometrics* (fingerprint, face) are convenient
"something you are" factors, usually paired with a device unlock rather than sent over a network,
but they cannot be changed if the biometric template is ever compromised.

**Backup and recovery codes.** Because a lost phone or hardware key should not permanently lock
a user out, most MFA systems generate a set of one-time backup codes at enrollment. These are a
"something you have" factor (a printed or stored list) and must be protected like a password, anyone who finds them can bypass the phone or key entirely.

**Putting it together.** When evaluating whether a login attempt is real MFA, ask two questions:
(1) Do the presented factors come from two or more *different* categories? (2) If yes, is at least
one of those factors resistant to phishing and interception, or does the scheme rely on something
that can be relayed, SIM-swapped, or rubber-stamped by an exhausted user? The simulation and coding
problem in this skill both drill this two-question judgment on realistic login-attempt scenarios.

## Key terms
- **Multi-factor authentication (MFA)**, requiring proof from two or more distinct factor
  categories before granting access.
- **Factor category**, one of: knowledge (something you know), possession (something you have),
  inherence (something you are).
- **TOTP / HOTP**, Time-based / HMAC-based One-Time Password; authenticator-app codes generated
  from a shared secret.
- **FIDO2 / WebAuthn**, an open standard for hardware/platform security keys that cryptographically
  bind authentication to the requesting website domain, making it phishing-resistant.
- **SIM swapping**, an attacker fraudulently transfers a victim's phone number to a
  attacker-controlled SIM card, intercepting SMS-based codes.
- **MFA fatigue (push bombing)**, repeatedly sending push-approval prompts until the user approves
  one out of annoyance or confusion.
- **Phishing-resistant authentication**, a factor that cannot be captured and replayed by a fake
  login page, such as a FIDO2/WebAuthn hardware key.

## Common misconceptions
- "Entering two different passwords is two-factor authentication." → Both are "something you
  know", the same factor category twice. True MFA requires two *different* categories.
- "SMS-based MFA is just as strong as an authenticator app or hardware key." → SMS codes travel
  through the mobile carrier network and are vulnerable to SIM swapping and relay/phishing attacks
  that authenticator apps avoid, and that hardware keys are specifically designed to resist.
- "Approving a push notification always means the real user is logging in." → MFA fatigue attacks
  exploit the fact that a user may approve a prompt they did not initiate, just to stop repeated
  notifications; approval is not proof of intent unless the prompt shows context the user verifies.

## Try it
- **Simulation:** Evaluate a stream of login attempts, judging
  whether each satisfies true MFA and which is most phishing-resistant, reaching a perfect score.
- **Coding problem:** Implement a classifier that maps a list of presented
  authentication factors to an MFA-strength classification.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST (Digital Identity Guidelines, authentication factors), rebuilt as original prose
  above; see `vendor/web/nist/` notes.
- Reference: Wikiversity (authentication and MFA overview), cross-checked for accuracy.
- Practice: SANS Cyber Aces authentication modules, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/LetsDefend-Free-Cybersecurity-Resources`.
