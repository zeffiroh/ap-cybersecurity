# 4.2.a, Passwords and password policies

> **Unit 4 · 4.2 Authentication**
> **AP Learning Objective(s):** 4.2.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Evaluate a password against a formal policy (length, complexity,
history, lockout) and explain why each rule reduces the risk of unauthorized access.

## Lesson
Authentication is the process of proving you are who you claim to be. The oldest and most
widespread mechanism is the password, a shared secret known only to the user and the system.
Despite decades of criticism, passwords remain ubiquitous, which makes understanding them
foundational to any cybersecurity curriculum. This skill covers what makes a password strong,
how organizations encode that strength into policy, and why each policy rule exists.

**What makes a password strong?**
Two factors dominate: length and unpredictability. An attacker who cannot get the password
from the server (via a breach or social engineering) will typically attempt one of two offline
attacks. A *brute-force* attack tries every possible character combination; a *dictionary* attack
tries words, names, and common substitutions (p@ssw0rd, abc123). Both attacks become
exponentially more expensive as password length increases. Adding one character to a ten-character
password multiplied by an alphabet of 95 printable characters multiplies the search space by 95.
Adding four characters multiplies it by roughly 81 million. Complexity rules, requiring uppercase,
digits, and symbols, were introduced to force users away from dictionary words, but they are not
a substitute for length. A long, random passphrase ("correct horse battery staple") is stronger
than a short, symbol-sprinkled word ("P@ssw0rd!") against every attack class.

**NIST SP 800-63B: the modern baseline**
The National Institute of Standards and Technology publishes guidelines that most US government
and enterprise policies follow. The 2017 revision (SP 800-63B) changed the conversation
significantly. Key recommendations:

- Minimum length of 8 characters for user-chosen passwords; 6 digits for PINs. Systems should
  allow up to at least 64 characters.
- Check candidate passwords against a list of known-compromised passwords (e.g., passwords found
  in public breach datasets). If the candidate matches, reject it and explain why, do not just
  say "too weak."
- Eliminate arbitrary complexity rules (mandatory uppercase, symbols, etc.) that push users toward
  predictable patterns (Password1!, Password2!...).
- Eliminate forced periodic rotation unless there is evidence of compromise. Forced rotation causes
  users to choose "Summer2024!" then "Fall2024!", a predictable family.
- Allow copy-paste and password manager use. Blocking paste makes passwords shorter and weaker.

**Account lockout policy**
A password policy also governs what happens when wrong passwords are presented. Lockout after
a threshold of failures (typically 3–10) prevents online guessing attacks, an attacker who
needs millions of tries cannot make them interactively. The policy specifies the *threshold*,
the *lockout duration* (e.g., 30 minutes, or indefinite until admin reset), and whether a
*delay* is introduced before each attempt after the first failure. Duration matters: too short
(10 seconds) is easily circumvented by scripted slow-guessing; too long or indefinite enables a
denial-of-service attack where an adversary deliberately locks out legitimate users.

**Password history and reuse**
Systems can store hashes of previous passwords and reject any candidate that matches the last
N passwords (typically 10–24). This prevents "password cycling," where users change from
Password1 to Password2 and back. Combined with banning common passwords, this significantly
raises the cost of maintaining a predictable sequence.

**Hashing and storage**
Passwords must never be stored in plaintext. The correct mechanism is a *salted cryptographic
hash* using a slow algorithm designed for passwords, such as bcrypt, scrypt, or Argon2. The
salt is a unique random value prepended to the password before hashing, which defeats precomputed
rainbow tables. Slow algorithms make each guess computationally expensive even if an attacker
steals the hash database. MD5 and SHA-1 are not acceptable for password storage, they are fast
general-purpose hashes, meaning an attacker with a GPU can test billions of candidates per second.

**Policy in practice: the simulation**
The coding problem (`problem/`) asks you to implement `validate_password(password, policy)`,
which checks a candidate string against a policy dictionary and returns a list of which rules it
violates. Working through this concretely reinforces what each rule does. The simulation
(the simulation) presents a password-creation interface where you observe how each policy parameter
changes the accept/reject decision.

**Connecting to the AP objective**
LO 4.2.A asks you to explain how authentication mechanisms protect systems. Password policy is
the first line of that protection: it defines the minimum acceptable credential strength and
forces users toward values an attacker cannot trivially guess or crack. Every rule in the policy
maps to an attack class it makes harder.

## Key terms
- **Authentication**, verifying the identity of a user or system before granting access.
- **Brute-force attack**, systematically trying every possible password until one succeeds.
- **Dictionary attack**, trying passwords from a list of common words, names, and patterns.
- **Salt**, a unique random value added to a password before hashing to defeat precomputed attacks.
- **Account lockout**, temporarily blocking an account after a threshold of failed login attempts.
- **Password policy**, a set of rules an organization enforces on the creation and management of passwords.
- **NIST SP 800-63B**, the US federal password guideline that underpins most modern enterprise policy.

## Common misconceptions
- "Complexity rules (uppercase + symbol) make passwords strong." -> Complexity rules push users toward
  predictable patterns (P@ssw0rd1). Length and unpredictability matter more. NIST removed mandatory
  complexity in 2017.
- "Changing your password every 90 days improves security." -> Forced rotation produces predictable
  families ("Spring2024!", "Summer2024!"). Rotate only when there is evidence of compromise.
- "Blocking copy-paste in the password field is a security feature." -> It forces shorter, weaker
  passwords and prevents password manager use. It is an anti-pattern.

## Try it
- **Simulation:** Adjust policy sliders and observe which
  candidate passwords are accepted or rejected; aim to find the minimum-length passphrase that
  beats every policy rule.
- **Coding problem:** Implement `validate_password(password, policy)` to return
  the list of policy rules a candidate password violates.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-63B (Digital Identity Guidelines), rebuilt as original prose above; see
  `vendor/web/nist/` notes.
- Reference: Wikiversity (Password security), supplementary definitions.
- Practice: SANS Cyber Aces password module, rebuilt locally as the simulation interaction.
- Repo: LetsDefend/Free-Cybersecurity-Resources -> `vendor/repos/letsdefend-free-cybersecurity-resources`.
