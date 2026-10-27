# 1.2.b, Weak authentication patterns; adversary dictionary construction

> **Unit 1 · 1.2 Suspicious Wi-Fi Login**
> **AP Learning Objective(s):** 1.2.B
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Evaluate a password against the core weakness criteria (length,
dictionary membership, character variety, and sequential/repeated patterns) and explain how
adversaries build and use wordlists to attack weak passwords.

## Lesson
A password is only as strong as the assumptions an attacker has to defeat in order to guess it.
When an attacker sits down to brute-force an account, they do not usually start at `aaaaaaa` and
try every possible combination, that is computationally expensive when the password space is
large. Instead, they start with what works: a dictionary.

**What is a dictionary attack?** A dictionary attack is a brute-force strategy that replaces
random guessing with structured guessing. The attacker uses a wordlist, a file containing
thousands to millions of candidate passwords ordered by likelihood. Real-world tools like hashcat
and John the Ripper ship with premade wordlists. The most famous is `rockyou.txt`, a 14-million-
password file leaked in the 2009 RockYou breach. It works so well because people keep choosing
the same passwords. If your password appears in that file, or could be derived from a word in it
by simple substitution (`p@ssw0rd`, `passw0rd!`), a dictionary attack will crack it in seconds.

**How adversaries build wordlists.** Attackers do not rely on generic wordlists alone. They
construct target-specific wordlists using:
- **Known breach data.** Leaked credential dumps (sorted by frequency) reveal which passwords
  are most common globally and within specific communities.
- **Target-specific information.** If the target has a public social profile, the attacker adds
  their name, hometown, pet name, birth year, and employer, all common password ingredients.
- **Mangling rules.** Tools apply transformation rules to every word: capitalize the first letter,
  append `1` or `!`, substitute `a` with `@` or `e` with `3`. These generate hundreds of
  variants per word, dramatically expanding the wordlist without requiring creative thinking.
- **Keyboard walks.** Sequential key patterns like `qwerty`, `asdfgh`, and `123456` appear so
  often in breach data that they have their own category. Attackers include them explicitly.

**The four weakness flags.** When analyzing a password for defensive purposes, four categories
of weakness stand out:

1. **Too short.** NIST SP 800-63B recommends a minimum of 8 characters for human-chosen passwords
   and 12 for production systems. The AP course uses 12 as the threshold. Every additional
   character multiplies the search space exponentially, going from 8 to 12 characters (assuming
   a mixed-character set) increases the combinations by a factor of roughly 10 million. Short
   passwords are cracked first.

2. **In the common dictionary.** Any password that appears verbatim in a well-known wordlist is
   trivially cracked regardless of what other criteria it meets. `password`, `letmein`,
   `iloveyou`, and `dragon` all pass naive "must contain uppercase and number" policies when
   combined with predictable substitutions, but they fail the dictionary check because attackers
   try them first.

3. **Only lowercase.** A password using only the 26 lowercase letters is drawn from a much
   smaller pool than one mixing uppercase, digits, and symbols. An attacker knows this and
   restricts their search space accordingly, cutting the time-to-crack by orders of magnitude.
   Real-world policy guidance (NIST SP 800-63B) has shifted away from mandatory complexity rules
   toward longer passphrases, but a purely lowercase short password still combines two weaknesses.

4. **Sequential or repeated characters.** Patterns like `aaa`, `111`, `abcabc`, and `qwerty`
   are explicitly included in every modern wordlist. Repeated characters reduce effective
   entropy; sequential patterns are guessed early in keyboard-walk attacks. A password that is
   otherwise long can still be weak if it is built from a repeated or sequential pattern.

**Why you need to know what the attacker sees.** Defenders who understand dictionary construction
can write better password policies: ban common words, require true length (not just complexity),
and implement breach-checking (verifying that a new password does not appear in known breach
databases). Services like HIBP (Have I Been Pwned) expose this check through an API, and
production systems are expected to use it. Understanding the attacker's tool also reveals why
security-through-obscurity substitutions (`p@ssword`) do not work, attackers include every
common substitution in their mangling rules.

**Practical policy implications.** The coding problem for this skill asks you to implement a
password weakness checker that applies all four rules. This is similar to the password-validation
logic used in real authentication backends. When a user chooses a password, the system checks it
against these rules and explains which ones it fails, helping the user choose a stronger secret
without just rejecting their input without explanation.

**A note on passphrases.** The strongest passwords are long random passphrases: four or more
random common words. Length dominates all other factors. A 20-character passphrase of common
words is exponentially harder to brute-force than an 8-character mixed-character password,
despite failing the complexity check. Teaching students to understand the math behind this, and
why length beats complexity, is one of the most lasting password-hygiene lessons in this course.

## Key terms
- **Dictionary attack**, brute-force strategy that tries passwords from a wordlist rather than
  exhaustive character combinations.
- **Wordlist / credential dictionary**, file of candidate passwords ordered by likelihood,
  built from breach data, common patterns, and target-specific words.
- **Mangling rules**, transformations (capitalize, substitute, append) applied to wordlist
  entries to generate variants.
- **Credential stuffing**, reusing username/password pairs from one breach to attack other
  services; made effective by password reuse.
- **Password entropy**, measure of how unpredictable a password is; increases with length and
  character variety, decreases with dictionary membership and patterns.

## Common misconceptions
- "Adding a number and symbol makes a password secure." → If the base word is in the dictionary,
  mangling rules will find the variant. Entropy comes from unpredictability and length.
- "Longer passwords are harder to remember, so shorter complex ones are better." → A four-word
  random passphrase is both longer and more memorable than `P@ssw0rd!`. Length wins on math.
- "The attacker needs the password file to run a dictionary attack." → Online dictionary attacks
  (directly against a login form) do not need the hash. Offline attacks on stolen hashes are
  faster, but the dictionary approach applies to both.

## Try it
- **Simulation:** Test passwords against the weakness checker
  and reach a score of 4 by correctly predicting which passwords will be flagged weak vs. strong.
- **Coding problem:** Implement `solve(password)` returning a weakness report dict.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: SANS Cyber Aces (password security module), principles rebuilt as original prose above.
- Reference: NIST SP 800-63B (Digital Identity Guidelines), length threshold and policy
  rationale; common-password ban rationale.
- Practice: Cybrary password-security exercises, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/LetsDefend-Free-Cybersecurity-Resources`.
